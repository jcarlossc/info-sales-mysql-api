import pandas as pd
import pytest


@pytest.fixture
def sales_dataframe():
    return pd.DataFrame(
        {
            "valor_venda": [100, 200],
            "valor_compra": [60, 120],
            "quantidade": [2, 1],
            "desconto": [10, 20],
            "data_venda": pd.to_datetime(
                [
                    "2024-01-10",
                    "2024-02-10",
                ]
            ),
            "nome_produto": ["A", "B"],
            "categoria": ["X", "Y"],
            "nome_vendedor": ["Carlos", "Ana"],
            "estado": ["SP", "RJ"],
            "cidade": ["São Paulo", "Rio"],
            "forma_pagamento": ["PIX", "Cartão"],
            "status": ["Concluído", "Concluído"],
        }
    )
