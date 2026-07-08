import logging
from typing import Dict, Any
from pathlib import Path


def setup_logger(logging_config: Dict[str, Any], log_file: str) -> None:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, logging_config["logging"]["level"], logging.INFO)

    logging.basicConfig(
        level=level,
        format=logging_config["logging"]["format"],
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    logging.info("Logger configurado com sucesso.")
