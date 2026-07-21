import pytest

# from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from info_sales_mysql_api.database.connection.get_connection import get_engine
from info_sales_mysql_api.utils.config_env.Settings import Settings


# Verifica se a função retorna uma Engine.
def test_get_engine_success(monkeypatch, mock_settings):
    """
    Deve criar e retornar uma Engine quando as configurações
    estiverem corretas.
    """

    fake_engine = object()

    def fake_create_engine(connection_string):
        assert connection_string == "mysql+pymysql://usuario:senha@localhost:3306/banco"
        return fake_engine

    monkeypatch.setattr(
        "info_sales_mysql_api.database.connection.get_connection.create_engine",
        fake_create_engine,
    )

    engine = get_engine(mock_settings)

    assert engine is fake_engine


# Verifica se a função propaga SQLAlchemyError
def test_get_engine_sqlalchemy_error(monkeypatch, mock_settings):
    """
    Deve lançar SQLAlchemyError caso ocorra erro
    durante a criação da Engine.
    """

    def fake_create_engine(connection_string):
        raise SQLAlchemyError("Erro de conexão")

    monkeypatch.setattr(
        "info_sales_mysql_api.database.connection.get_connection.create_engine",
        fake_create_engine,
    )

    with pytest.raises(SQLAlchemyError):
        get_engine(mock_settings)


# Cria um objeto Settings com valores fictícios
@pytest.fixture
def mock_settings():
    settings = Settings.model_construct(
        api_key="123",
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="banco",
        mysql_user="usuario",
        mysql_password="senha",
    )

    return settings
