from fastapi import FastAPI

from info_sales_mysql_api.main import app


def test_app_is_fastapi_instance():
    """
    Verifica se a aplicação foi criada corretamente.
    """

    assert isinstance(app, FastAPI)
