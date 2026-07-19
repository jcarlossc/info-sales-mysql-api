import logging

from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader

from info_sales_mysql_api.utils.config_env.Settings import Settings

logger = logging.getLogger(__name__)

# Header esperado em todas as requisições protegidas.
api_key_header = APIKeyHeader(
    name="X-API-Key",
)


def validate_api_key(
    api_key: str = Security(api_key_header),
) -> str:
    """
    Valida a API Key enviada pelo cliente.

    A chave deve ser enviada no header HTTP ``X-API-Key``.
    Caso a chave seja inválida, uma exceção HTTP 401 é lançada.

    Args:
        api_key:
            API Key enviada pelo cliente.

    Returns:
        A própria API Key quando a autenticação é bem-sucedida.

    Raises:
        HTTPException:
            Caso a API Key seja inválida.
    """

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
