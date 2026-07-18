import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from info_sales_mysql_api.pipeline.pipeline_service import run_pipeline
from info_sales_mysql_api.api.schema.schema_summary import SalesSummary
from info_sales_mysql_api.utils.loggers.logger import setup_logger
from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs

logger = logging.getLogger(__name__)

logger.info("Criando logger.")

config_path = Path("config")

configs = load_all_configs(config_path)

setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)


@router.get(
    "",
    response_model=SalesSummary,
    summary="Resumo geral das vendas",
    description="Retorna os principais indicadores de desempenho calculados a partir da base de vendas.",
)
def get_summary_router() -> SalesSummary:
    logger.info("Recebida requisição GET /summary")

    try:
        summary = run_pipeline()

        logger.info("Resumo gerado com sucesso.")

        return SalesSummary(**summary)

    except ValidationError as error:
        logger.error(
            "Erro de validação do schema: %s",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail="Erro ao validar a estrutura da resposta.",
        ) from error

    except Exception as error:
        logger.exception("Erro inesperado ao gerar resumo das vendas.")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a requisição.",
        ) from error
