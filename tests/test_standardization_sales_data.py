import pandas as pd
import pytest

from info_sales_mysql_api.standardization.get_standardization import (
    standardize_sales_data,
)


@pytest.fixture
def sales_dataframe():
    """Cria um DataFrame de exemplo."""

    return pd.DataFrame(
        {
            "venda_id": ["1"],
            "vendedor_id": ["10"],
            "produto_id": ["100"],
            "quantidade": ["2"],
            "categoria": ["Mouse"],
            "data_venda": ["2026-07-14"],
            "desconto": ["10.5"],
            "valor_venda": ["150.75"],
            "valor_compra": ["120.50"],
            "nome_vendedor": [" Carlos "],
            "nome_produto": [" Notebook "],
            "forma_pagamento": [" Cartão "],
            "cidade": [" Recife "],
            "estado": [" PE "],
            "status": [" Concluída "],
        }
    )


def test_standardize_sales_data_success(monkeypatch, sales_dataframe):
    """
    Verifica se o DataFrame é padronizado corretamente.
    """

    # Configuração simulada carregada do YAML.
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: {
            "db": {
                "columns": {
                    "venda_id": "venda_id",
                    "vendedor_id": "vendedor_id",
                    "produto_id": "produto_id",
                    "quantidade": "quantidade",
                    "categoria": "categoria",
                    "data_venda": "data_venda",
                    "valor_compra": "valor_compra",
                    "valor_venda": "valor_venda",
                    "desconto": "desconto",
                    "nome_vendedor": "nome_vendedor",
                    "nome_produto": "nome_produto",
                    "forma_pagamento": "forma_pagamento",
                    "cidade": "cidade",
                    "estado": "estado",
                    "status": "status",
                }
            }
        },
    )

    # Executa a função.
    df = standardize_sales_data(sales_dataframe)

    # Verifica tipos numéricos.
    assert str(df["venda_id"].dtype) == "Int64"
    assert str(df["quantidade"].dtype) == "Int64"

    # Verifica conversão de datas.
    assert pd.api.types.is_datetime64_any_dtype(df["data_venda"])

    # Verifica padronização de texto.
    assert df.loc[0, "nome_vendedor"] == "carlos"
    assert df.loc[0, "cidade"] == "recife"


@pytest.fixture
def fake_config():
    """Simula o retorno do arquivo YAML."""

    return {
        "db": {
            "columns": {
                "venda_id": "venda_id",
                "vendedor_id": "vendedor_id",
                "produto_id": "produto_id",
                "quantidade": "quantidade",
                "categoria": "categoria",
                "data_venda": "data_venda",
                "desconto": "desconto",
                "valor_venda": "valor_venda",
                "valor_compra": "valor_compra",
                "nome_vendedor": "nome_vendedor",
                "nome_produto": "nome_produto",
                "forma_pagamento": "forma_pagamento",
                "cidade": "cidade",
                "estado": "estado",
                "status": "status",
            }
        }
    }


def test_standardize_sales_data(monkeypatch, sales_dataframe, fake_config):
    """Testa a padronização dos dados."""

    monkeypatch.setattr(
        "info_sales_mysql_api.standardization.get_standardization.load_all_configs",
        lambda _: fake_config,
    )

    df = standardize_sales_data(sales_dataframe)

    assert str(df["venda_id"].dtype) == "Int64"
    assert str(df["quantidade"].dtype) == "Int64"

    assert pd.api.types.is_datetime64_any_dtype(df["data_venda"])

    assert df.loc[0, "nome_vendedor"] == "carlos"
    assert df.loc[0, "nome_produto"] == "notebook"
    assert df.loc[0, "cidade"] == "recife"


def test_standardize_sales_data_missing_columns(monkeypatch):
    """
    Verifica se KeyError é lançado quando
    existem colunas obrigatórias ausentes.
    """

    df = pd.DataFrame({"venda_id": [1]})

    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: {
            "db": {
                "columns": {
                    "venda_id": "venda_id",
                    "quantidade": "quantidade",
                }
            }
        },
    )

    with pytest.raises(KeyError):
        standardize_sales_data(df)


def test_standardize_sales_data_unexpected_error(
    monkeypatch,
    sales_dataframe,
):
    """
    Verifica se erros inesperados são propagados.
    """

    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: {"db": {"columns": {...}}},
    )

    def fake_datetime(*args, **kwargs):
        raise RuntimeError("Erro inesperado")

    monkeypatch.setattr(pd, "to_datetime", fake_datetime)

    with pytest.raises(RuntimeError):
        standardize_sales_data(sales_dataframe)
