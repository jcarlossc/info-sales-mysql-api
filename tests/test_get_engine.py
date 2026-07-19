from unittest.mock import MagicMock

from info_sales_mysql_api.database.connection.get_connection import get_engine
from info_sales_mysql_api.utils.config_env.Settings import Settings


def test_get_engine_connection_string(monkeypatch):
    """
    Deve montar corretamente a string de conexão.
    """

    settings = Settings(
        api_key="abc123",
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="empresa",
        mysql_user="root",
        mysql_password="123456",
    )

    fake_engine = MagicMock()

    received = {}

    def fake_create_engine(conn):
        received["conn"] = conn
        return fake_engine

    monkeypatch.setattr(
        "info_sales_mysql_api.database.connection.get_connection.create_engine",
        fake_create_engine,
    )

    get_engine(settings)

    assert received["conn"] == "mysql+pymysql://root:123456@localhost:3306/empresa"
