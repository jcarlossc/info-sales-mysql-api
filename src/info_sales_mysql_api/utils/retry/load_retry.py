import time
from typing import Any, Callable


def retry_connect(
    connect: Callable[[], Any],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
    for attempt in range(max_attempts):
        try:
            return connect()

        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(delay)
            else:
                raise
