from pathlib import Path

# import pandas as pd
import logging

from info_sales_mysql_api.utils.loggers.logger import setup_logger
from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def run_pipeline() -> None:
    logger = logging.getLogger(__name__)

    # conn = None

    logger.info("Carregando arquivos de configutação.")

    config_path = Path("config")

    configs = load_all_configs(config_path)

    logger.info("Criando logger.")

    setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

    logger.info("### Iniciando pipeline de vendas. ###")
