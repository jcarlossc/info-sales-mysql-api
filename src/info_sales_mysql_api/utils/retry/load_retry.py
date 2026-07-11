import time
from typing import Any, Callable


def retry_connect(
    connect: Callable[[], Any],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
    """
    Tenta executar uma função de conexão várias vezes.

    Parameters
    ----------
    connect : Callable
        Função responsável por criar a conexão.
    max_attempts : int, optional
        Número máximo de tentativas.
    delay : float, optional
        Tempo de espera entre as tentativas, em segundos.

    Returns
    -------
    Any
        Objeto retornado pela função de conexão.

    Raises
    ------
    Exception
        Relança a última exceção caso todas as tentativas falhem.
    """

    # Executa a quantidade máxima de tentativas.
    for attempt in range(max_attempts):
        try:
            # Retorna a conexão caso obtenha sucesso.
            return connect()

        except Exception:
            # Se ainda houver tentativas restantes, aguarda.
            if attempt < max_attempts - 1:
                time.sleep(delay)
            else:
                # Relança a exceção na última tentativa.
                raise
