from info_sales_mysql_api.api.dependencies.api_key import validate_api_key
import pytest
from fastapi import HTTPException

from unittest.mock import patch


# Substitui a classe Settings por um objeto simulado durante o teste.
@patch("info_sales_mysql_api.api.dependencies.api_key.Settings")
def test_validate_api_key_success(mock_settings):
    mock_settings.return_value.api_key = "abc123"

    result = validate_api_key(api_key="abc123")

    assert result == "abc123"


# Substitui a classe Settings por um objeto simulado durante o teste.
@patch("info_sales_mysql_api.api.dependencies.api_key.Settings")
def test_validate_api_key_invalid(mock_settings):
    mock_settings.return_value.api_key = "abc123"

    with pytest.raises(HTTPException) as exc:
        validate_api_key(api_key="errada")

    assert exc.value.status_code == 401
    assert exc.value.detail == "API Key inválida."


# Substitui a classe Settings por um objeto simulado para testar o caminho de exceção.
@patch("info_sales_mysql_api.api.dependencies.api_key.Settings")
def test_validate_api_key_raise_http_exception(mock_settings):
    mock_settings.return_value.api_key = "api-key-correta"

    with pytest.raises(HTTPException):
        validate_api_key(api_key="api-key-incorreta")
