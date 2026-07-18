import logging
from functools import partial

from info_sales_mysql_api.database.connection.get_connection import get_engine
from info_sales_mysql_api.utils.config_env.Settings import Settings
from info_sales_mysql_api.utils.retry.load_retry import retry_connect
from info_sales_mysql_api.database.query.load_sales import get_load_sales
from info_sales_mysql_api.standardization.get_standardization import (
    standardize_sales_data,
)
from info_sales_mysql_api.cleanning.data_clean import validate_sales_data
from info_sales_mysql_api.summary.get_summary import create_sales_summary


def run_pipeline() -> dict:
    """
    Executa o pipeline completo de processamento das vendas.

    O pipeline realiza as seguintes etapas:

    1. Carrega as configurações da aplicação.
    2. Configura o sistema de logs.
    3. Estabelece conexão com o banco MySQL.
    4. Carrega os dados de vendas.
    5. Padroniza os dados.
    6. Valida a qualidade dos dados.
    7. Calcula os KPIs e métricas.
    8. Finaliza a conexão.

    Returns
    -------
    dict
        Dicionário contendo o resumo consolidado das vendas.

    Raises
    ------
    Exception
        Caso ocorra algum erro durante o pipeline.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    # Inicializa engine
    engine = None

    try:
        # Representa as configurações da aplicação(.env).
        settings = Settings()

        logger.info("### Iniciando pipeline de vendas. ###")

        logger.info("Criando conexão com banco.")

        engine = retry_connect(
            partial(get_engine, settings),
            max_attempts=5,
            delay=3,
        )

        logger.info("Carregando vendas.")

        df = get_load_sales(engine)

        logger.info("Padronizando dados.")

        df = standardize_sales_data(df)

        logger.info("Limpeza dos dados.")

        df = validate_sales_data(df)

        logger.info("Calculando KPIs.")

        summary_dict = create_sales_summary(df)

        logger.info(f"Finalizando pipeline com {len(df)} registros.")

        return summary_dict

    except Exception:
        logger.exception("Erro durante a execução do pipeline.")
        raise

    finally:
        if engine is not None:
            engine.dispose()

            logger.info("Conexão encerrada.")
