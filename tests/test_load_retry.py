from info_sales_mysql_api.utils.retry.load_retry import retry_connect


def test_retry_connect_success_first_attempt():
    """
    Deve retornar a conexão na primeira tentativa.
    """

    def fake_connect():
        return "Conectado"

    result = retry_connect(fake_connect)

    assert result == "Conectado"

    def test_retry_connect_success_after_retries(monkeypatch):
        """
        Deve conectar após falhas iniciais.
        """

        attempts = {"count": 0}

        def fake_connect():
            attempts["count"] += 1

            if attempts["count"] < 3:
                raise ConnectionError()

            return "Conectado"

        monkeypatch.setattr(
            "time.sleep",
            lambda _: None,
        )

        result = retry_connect(
            fake_connect,
            max_attempts=3,
            delay=0,
        )

        assert result == "Conectado"

        assert attempts["count"] == 3
