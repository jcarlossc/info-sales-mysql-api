import logging
from pathlib import Path
import pandas as pd

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def validate_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando limpeza dos dados.")

    config_path = Path("config")

    configs = load_all_configs(config_path)

    required_columns = configs["db"]["columns"]

    missing = [col for col in required_columns if col not in df.columns]

    try:
        if missing:
            logger.warning(f"Colunas ausentes: {missing}")

            raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

        logger.info("Iniciando teste e/ou limpeza de valores nulos.")

        required_id_columns = [
            required_columns["venda_id"],
            required_columns["vendedor_id"],
            required_columns["produto_id"],
        ]

        required_date_columns = [
            required_columns["data_venda"],
        ]

        required_numeric_columns = [
            required_columns["quantidade"],
            required_columns["valor_compra"],
            required_columns["valor_venda"],
        ]

        optional_numeric_columns = [
            required_columns["desconto"],
        ]

        text_columns = [
            required_columns["nome_vendedor"],
            required_columns["nome_produto"],
            required_columns["cidade"],
            required_columns["estado"],
            required_columns["forma_pagamento"],
            required_columns["status"],
        ]

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

        logger.info("Iniciando teste e/ou limpeza de valores duplicados.")

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

        logger.info("Iniciando teste e/ou limpeza de valores negativos.")

        for column in required_numeric_columns:
            negative_count = (df[column] < 0).sum()

            if negative_count > 0:
                logger.error(
                    "A coluna '%s' possui %d valor(es) negativo(s).",
                    column,
                    negative_count,
                )

                raise ValueError(f"A coluna '{column}' contém valores negativos.")

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
