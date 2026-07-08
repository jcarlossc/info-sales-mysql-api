import logging
from typing import Dict, Any
from pathlib import Path


def setup_logger(logging_config: Dict[str, Any], log_file: str) -> None:
    try:
        # Garante que a pasta existe
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # Obtém o nível de logging definido na configuração.
        # Caso o nível não exista, utiliza INFO como padrão.
        level = getattr(logging, logging_config["logging"]["level"], logging.INFO)

        # Configura o sistema de logging da aplicação.
        # logging.basicConfig inicializa o logger raiz (root logger)
        # com os parâmetros definidos.
        logging.basicConfig(
            # Define o nível mínimo de mensagens que serão registradas.
            level=level,
            # Define o formato das mensagens de log.
            # Normalmente inclui timestamp, nível do log, módulo e mensagem.
            format=logging_config["logging"]["format"],
            # Define os handlers responsáveis por enviar os logs
            # para diferentes destinos.
            handlers=[
                # FileHandler grava os logs em arquivo para posterior auditoria
                # e análise de execução do pipeline.
                logging.FileHandler(log_file, encoding="utf-8"),
                # StreamHandler envia os logs para o console (stdout),
                # permitindo acompanhar a execução em tempo real.
                logging.StreamHandler(),
            ],
        )

        logging.info("Logger configurado com sucesso.")

    except (KeyError, TypeError) as error:
        raise ValueError(f"CONFIG_ERROR: configuração inválida -> {error}") from error

    except OSError as error:
        raise OSError(
            f"FILE_ERROR: erro no arquivo de log '{log_file}' -> {error}"
        ) from error
