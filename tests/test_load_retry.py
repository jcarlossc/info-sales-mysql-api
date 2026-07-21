import pytest

from info_sales_mysql_api.utils.retry.load_retry import retry_connect


def test_retry_connect_success_first_attempt():
    """
    Verifica se a conexão é retornada quando
    a primeira tentativa é bem-sucedida.
    """

    # Simula uma conexão realizada com sucesso.
    def fake_connect():
        return "conectado"

    # Executa a função.
    result = retry_connect(fake_connect)

    # Verifica se o retorno é o esperado.
    assert result == "conectado"


def test_retry_connect_success_after_retry(monkeypatch):
    """
    Verifica se a função realiza novas tentativas
    até obter sucesso na conexão.
    """

    # Evita que o teste aguarde durante o time.sleep().
    monkeypatch.setattr("time.sleep", lambda _: None)

    # Contador de tentativas.
    attempts = {"count": 0}

    def fake_connect():
        # Incrementa a quantidade de chamadas.
        attempts["count"] += 1

        # As duas primeiras tentativas falham.
        if attempts["count"] < 3:
            raise Exception("Erro de conexão")

        # A terceira tentativa obtém sucesso.
        return "conectado"

    # Executa a função.
    result = retry_connect(
        fake_connect,
        max_attempts=3,
        delay=0,
    )

    # Verifica se a conexão foi retornada.
    assert result == "conectado"

    # Verifica se foram realizadas três tentativas.
    assert attempts["count"] == 3


def test_retry_connect_all_attempts_fail(monkeypatch):
    """
    Verifica se a função relança a exceção após
    todas as tentativas de conexão falharem.
    """

    # Evita espera durante o teste.
    monkeypatch.setattr("time.sleep", lambda _: None)

    # Contador de tentativas.
    attempts = {"count": 0}

    def fake_connect():
        # Conta cada tentativa de conexão.
        attempts["count"] += 1

        # Simula falha em todas as tentativas.
        raise Exception("Erro de conexão")

    # Verifica se a exceção é propagada.
    with pytest.raises(Exception, match="Erro de conexão"):
        retry_connect(
            fake_connect,
            max_attempts=3,
            delay=0,
        )

    # Verifica se todas as tentativas foram executadas.
    assert attempts["count"] == 3
