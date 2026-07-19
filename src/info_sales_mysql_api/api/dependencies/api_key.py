import logging

from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader

from info_sales_mysql_api.utils.config_env.Settings import Settings

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(
    name="X-API-Key",
)


def validate_api_key(
    api_key: str = Security(api_key_header),
) -> str:
    logger.info("Iniciando validação da chave de API.")

    settings = Settings()

    if api_key != settings.api_key:
        logger.warning("Tentativa de acesso com API Key inválida.")

        raise HTTPException(
            status_code=401,
            detail="API Key inválida.",
        )

    logger.info("API Key validada com sucesso.")

    return api_key
