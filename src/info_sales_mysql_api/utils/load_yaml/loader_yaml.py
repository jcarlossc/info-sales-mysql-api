import yaml
from pathlib import Path
from typing import Dict, Any                                          

def load_all_configs(config_path: Path) -> Dict[str, Any]:

    configs: Dict[str, Any] = {}

    if not config_path.exists():
        raise FileNotFoundError(
            f"Diretório de configuração não encontrado: {config_path}"
        )

    if not config_path.is_dir():
        raise NotADirectoryError(
            f"Caminho informado não é diretório: {config_path}"
        )

    for file in config_path.glob("*.yaml"):
        with open(file, "r", encoding="utf-8") as f:
            configs[file.stem] = yaml.safe_load(f)

    return configs

