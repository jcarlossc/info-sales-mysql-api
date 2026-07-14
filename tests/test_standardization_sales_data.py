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
