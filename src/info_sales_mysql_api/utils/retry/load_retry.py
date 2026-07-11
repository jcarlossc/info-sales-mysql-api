import time
from typing import Any, Callable


def retry_connect(
    connect: Callable[[], Any],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
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
