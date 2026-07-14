import logging
from pathlib import Path
import pandas as pd

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def standardize_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando padronização dos dados.")

    config_path = Path("config")

    configs = load_all_configs(config_path)

    required_columns = configs["db"]["columns"]

    integer_columns = [
        required_columns["venda_id"],
        required_columns["vendedor_id"],
        required_columns["produto_id"],
        required_columns["quantidade"],
    ]

    for column in integer_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    df[required_columns["data_venda"]] = pd.to_datetime(
        df[required_columns["data_venda"]], errors="coerce"
    )

    numeric_cols = [
        required_columns["desconto"],
        required_columns["valor_venda"],
        required_columns["valor_compra"],
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        required_columns["nome_vendedor"],
        required_columns["nome_produto"],
        required_columns["forma_pagamento"],
        required_columns["cidade"],
        required_columns["estado"],
        required_columns["status"],
    ]

    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.lower()

    return df
