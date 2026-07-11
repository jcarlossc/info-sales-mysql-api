from typing import Dict, Any
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from info_sales_mysql_api.utils.config_env.Settings import Settings


def get_engine(config: Dict[str, Any]) -> Engine:
    logger = logging.getLogger(__name__)

    settings = Settings()

    logger.info("Iniciando criação da engine.")

    conn = (
        f"mysql+pymysql://"
        f"{settings.mysql_user}:"
        f"{settings.mysql_password}@"
        f"{settings.mysql_host}:"
        f"{settings.mysql_port}/"
        f"{settings.mysql_database}"
    )

    engine = create_engine(conn)

    logger.info("Engine criada com sucesso.")

    return engine
