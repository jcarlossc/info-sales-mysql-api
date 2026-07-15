import pandas as pd

from info_sales_mysql_api.cleanning.data_clean import validate_sales_data


def test_validate_sales_data():
    df = pd.DataFrame(
        {
            "venda_id": [1, None],
            "vendedor_id": [10, None],
            "produto_id": [100, None],
            "data_venda": [
                "2026-07-15",
                "2026-07-16",
            ],
            "quantidade": [2, 3],
            "categoria": ["Mouse", None],
            "valor_compra": [100, 200],
            "valor_venda": [150, 250],
            "desconto": [10, None],
            "nome_vendedor": ["Carlos", None],
            "nome_produto": ["Notebook", None],
            "cidade": ["Recife", None],
            "estado": ["PE", None],
            "forma_pagamento": ["Pix", None],
            "status": ["Concluída", None],
        }
    )

    result = validate_sales_data(df)

    # IDs preenchidos.
    assert result["venda_id"].isna().sum() == 0
    assert result["produto_id"].isna().sum() == 0
    assert result["vendedor_id"].isna().sum() == 0

    # Desconto preenchido.
    assert result["desconto"].isna().sum() == 0

    # Texto preenchido.
    assert result["cidade"].isna().sum() == 0

    assert "não informado" in result["cidade"].values
