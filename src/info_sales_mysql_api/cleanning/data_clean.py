import logging
from pathlib import Path
import pandas as pd

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def validate_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza testes de qualidade e limpeza dos dados de vendas.

    Regras aplicadas
    ----------------
    - Gera IDs para identificadores nulos.
    - Remove registros com datas obrigatórias nulas.
    - Remove registros com valores numéricos obrigatórios nulos.
    - Preenche desconto nulo com zero.
    - Preenche colunas textuais nulas com "não informado".
    - Remove registros duplicados.
    - Verifica valores negativos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame previamente padronizado.

    Returns
    -------
    pd.DataFrame
        DataFrame validado.

    Raises
    ------
    ValueError
        Quando existir valor negativo em colunas obrigatórias.

    Exception
        Para erros inesperados durante a validação.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Iniciando limpeza dos dados.")

    # Configura caminhos
    config_path = Path("config")

    configs = load_all_configs(config_path)

    # Colunas a serem testadas e limpas
    required_columns = configs["db"]["columns"]

    missing = [col for col in required_columns if col not in df.columns]

    try:
        # Verifica se todas as colunas
        # necessárias existem.
        if missing:
            logger.warning(f"Colunas ausentes: {missing}")

            raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

        # Colunas a serem testadas e convertidas em integer
        required_id_columns = [
            required_columns["venda_id"],
            required_columns["vendedor_id"],
            required_columns["produto_id"],
        ]

        # Colunas a serem testadas e convertidas em datetime
        required_date_columns = [
            required_columns["data_venda"],
        ]

        # Colunas a serem testadas e convertidas em float
        required_numeric_columns = [
            required_columns["quantidade"],
            required_columns["valor_compra"],
            required_columns["valor_venda"],
        ]

        # Colunas a serem testadas e convertidas em float
        optional_numeric_columns = [
            required_columns["desconto"],
        ]

        # Colunas a serem testadas e convertidas em string
        text_columns = [
            required_columns["nome_vendedor"],
            required_columns["nome_produto"],
            required_columns["cidade"],
            required_columns["estado"],
            required_columns["forma_pagamento"],
            required_columns["status"],
            required_columns["categoria"],
        ]

        logger.info("Iniciando teste limpeza de valores nulos.")

        # Testa e converte nulos em integer
        for column in required_id_columns:
            null_mask = df[column].isna()

            null_count = df[column].isna().sum()

            if null_count > 0:
                logger.warning(
                    "A coluna '%s' possui %d valor(es) nulo(s).",
                    column,
                    null_count,
                )

                next_id = int(df[column].max(skipna=True) or 0) + 1

                df.loc[null_mask, column] = range(
                    next_id,
                    next_id + null_count,
                )

                df[column] = df[column].astype("Int64")

            else:
                logger.info(
                    "A coluna '%s' não possui valores nulos.",
                    column,
                )

        # Testa e apaga nulos
        for column in required_date_columns:
            null_mask = df["data_venda"].isna()

            null_count = null_mask.sum()

            if null_count > 0:
                logger.warning(
                    "Removendo %d registro(s) com data nula.",
                    null_count,
                )

                df = df.dropna(subset=["data_venda"])

            else:
                logger.info(
                    "A coluna '%s' não possui valores nulos.",
                    column,
                )

        # Testa e apaga nulos
        for column in required_numeric_columns:
            null_mask = df[column].isna()

            null_count = null_mask.sum()

            if null_count > 0:
                logger.warning(
                    "Removendo %d registro(s) com '%s' nulo.",
                    null_count,
                    column,
                )

                df = df.dropna(subset=[column])

            else:
                logger.info(
                    "A coluna '%s' não possui valores nulos.",
                    column,
                )

        # Testa e converte nulos para 0
        for column in optional_numeric_columns:
            null_count = df[column].isna().sum()

            if null_count > 0:
                logger.warning(
                    "A coluna '%s' possui %d valor(es) nulo(s). Aplicando valor padrão 0.",
                    column,
                    null_count,
                )

                df[column] = df[column].fillna(0)

            else:
                logger.info(
                    "A coluna '%s' não possui valores nulos.",
                    column,
                )

        # Testa e converte nulos para 'não informado'
        for column in text_columns:
            null_count = df[column].isna().sum()

            if null_count > 0:
                logger.warning(
                    "Coluna '%s' possui %d valor(es) nulo(s). Aplicando 'não informado'.",
                    column,
                    null_count,
                )

                df[column] = df[column].fillna("não informado")

            else:
                logger.info(
                    "A coluna '%s' não possui valores nulos.",
                    column,
                )

        logger.info("Iniciando teste e limpeza de valores duplicados.")

        # Testa e somente recupera primeiro registro duplicado
        for column in required_id_columns:
            duplicated = df.duplicated(subset=["venda_id"])

            duplicate_count = duplicated.sum()

            if duplicate_count > 0:
                logger.warning(
                    "Foram encontrados %d registro(s) duplicado(s). Removendo duplicatas.",
                    duplicate_count,
                )

                df = df.drop_duplicates(
                    subset=["venda_id"],
                    keep="first",
                )

            else:
                logger.info(
                    "A coluna '%s' não possui valores duplicados.",
                    column,
                )

        logger.info("Iniciando teste e limpeza de valores negativos.")

        # Testa e converte negativos em positivos
        for column in required_numeric_columns:
            negative_count = (df[column] < 0).sum()

            if negative_count > 0:
                logger.error(
                    "A coluna '%s' possui %d valor(es) negativo(s).",
                    column,
                    negative_count,
                )

                df[column] = df[column].abs()

            logger.info(
                "A coluna '%s' não possui valores negativos.",
                column,
            )

        return df

    except ValueError as error:
        logger.error(
            "Erro de validação: %s",
            error,
        )
        raise

    except KeyError as error:
        logger.error(
            "Coluna obrigatória não encontrada: %s",
            error,
        )
        raise

    except Exception as error:
        logger.exception(
            "Erro inesperado durante validação:",
            error,
        )
        raise
