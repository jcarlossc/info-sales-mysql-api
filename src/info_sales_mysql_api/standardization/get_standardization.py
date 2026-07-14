import logging
from pathlib import Path
import pandas as pd

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def standardize_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza padronização dos dados de vendas.

    Etapas executadas:
    - valida colunas obrigatórias
    - converte tipos de dados
    - remove espaços extras
    - padroniza texto

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto de vendas.

    Returns
    -------
    pd.DataFrame
        DataFrame padronizado.

    Raises
    ------
    KeyError
        Quando colunas obrigatórias estão ausentes.

    ValueError
        Quando transformação falha.

    Exception
        Para erros inesperados.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Iniciando padronização dos dados.")

    # Configura caminhos
    config_path = Path("config")

    configs = load_all_configs(config_path)

    # Colunas a serem padronizadas
    required_columns = configs["db"]["columns"]

    try:
        # Verifica se todas as colunas
        # necessárias existem.
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            logger.warning(f"Colunas ausentes: {missing}")

            raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

        integer_columns = [
            required_columns["venda_id"],
            required_columns["vendedor_id"],
            required_columns["produto_id"],
            required_columns["quantidade"],
        ]

        # Converte colunas para inteiro.
        for column in integer_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

        # Converte datas.
        df[required_columns["data_venda"]] = pd.to_datetime(
            df[required_columns["data_venda"]], errors="coerce"
        )

        numeric_cols = [
            required_columns["desconto"],
            required_columns["valor_venda"],
            required_columns["valor_compra"],
        ]

        # Converte variáveis numéricas.
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

        # Remove espaços extras
        # e padroniza textos.
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip().str.lower()

        logger.info("Padronização concluída.")

        return df

    except KeyError as error:
        logger.warning(f"Erro de estrutura: {error}")
        raise

    except ValueError as error:
        logger.error(f"Erro de transformação: {error}")
        raise

    except Exception as error:
        logger.exception(f"Erro inesperado durante padronização: {error}")
        raise
