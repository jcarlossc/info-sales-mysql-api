import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from info_sales_mysql_api.pipeline.pipeline_service import run_pipeline
from info_sales_mysql_api.api.schema.schema_summary import SalesSummary
from info_sales_mysql_api.utils.loggers.logger import setup_logger
from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs

# Recupera logger do módulo atual para
# rastreamento do fluxo de execução.
logger = logging.getLogger(__name__)

logger.info("Criando logger.")

# Configura caminhos
config_path = Path("config")

# Busca arquivo yaml
configs = load_all_configs(config_path)

# Configura logs
setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

# Cria um roteador responsável pelos endpoints relacionados
# ao resumo consolidado das vendas.
router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)


# Endpoint GET para consulta do resumo consolidado das vendas.
@router.get(
    "",
    response_model=SalesSummary,
    summary="Resumo geral das vendas",
    description="Retorna os principais indicadores de desempenho calculados a partir da base de vendas.",
)
def get_summary_router() -> SalesSummary:
    """
    Retorna um resumo consolidado da base de vendas.

    O endpoint disponibiliza os principais indicadores utilizados em
    dashboards e análises gerenciais.

    Inclui:

    - Metadados da base
    - KPIs
    - Produtos
    - Categorias
    - Vendedores
    - Geografia
    - Série temporal
    - Formas de pagamento
    - Status dos pedidos

    Returns
    -------
    SalesSummary
        Resumo completo das métricas da base de vendas.

    Raises
    ------
    HTTPException
        Caso ocorra algum erro durante a geração do resumo.
    """

    logger.info("Recebida requisição GET /summary")

    try:
        # Gera o dicionário contendo todas as métricas.
        summary = run_pipeline()

        logger.info("Resumo gerado com sucesso.")

        # Valida a estrutura utilizando o schema Pydantic.
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


# Endpoint GET para consulta de sections.
@router.get(
    "/{section}",
    summary="Retorna uma seção do resumo",
)
def get_summary_section(section: str) -> Any:
    """
    Retorna uma seção específica do resumo.

    Exemplos
    --------
    /summary/kpis

    /summary/products

    /summary/categories
    """

    logger.info("Recebida requisição GET /summary/%s", section)

    try:
        summary = run_pipeline()

        if section not in summary:
            raise HTTPException(
                status_code=404,
                detail=f"Seção '{section}' não encontrada.",
            )

        return summary[section]

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Erro inesperado.")

        raise HTTPException(
            status_code=500,
            detail="Erro interno.",
        ) from error


# Endpoint GET para consulta de itens.
@router.get(
    "/{section}/{item}",
    summary="Retorna um item da seção",
)
def get_summary_item(
    section: str,
    item: str,
) -> Any:
    """
    Retorna um item específico de uma seção.

    Exemplos
    --------
    /summary/kpis/margin

    /summary/products/top_revenue

    /summary/geography/states
    """

    logger.info(
        "Recebida requisição GET /summary/%s/%s",
        section,
        item,
    )

    try:
        summary = run_pipeline()

        if section not in summary:
            raise HTTPException(
                status_code=404,
                detail=f"Seção '{section}' não encontrada.",
            )

        if item not in summary[section]:
            raise HTTPException(
                status_code=404,
                detail=f"Item '{item}' não encontrado.",
            )

        return summary[section][item]

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Erro inesperado.")

        raise HTTPException(
            status_code=500,
            detail="Erro interno.",
        ) from error
