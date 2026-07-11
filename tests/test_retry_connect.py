from info_sales_mysql_api.utils.retry.load_retry import retry_connect


def test_retry_connect_success():
    """Deve retornar a conexão quando não ocorre erro."""

    def connect():
        return "conectado"

    assert retry_connect(connect, delay=0) == "conectado"
