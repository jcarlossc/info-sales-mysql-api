import pandas as pd
import pytest

from info_sales_mysql_api.cleanning.data_clean import validate_sales_data


@pytest.fixture
def fake_config():
    return {
        "db": {
            "columns": {
                "venda_id": "venda_id",
                "vendedor_id": "vendedor_id",
                "produto_id": "produto_id",
                "data_venda": "data_venda",
                "quantidade": "quantidade",
                "valor_compra": "valor_compra",
                "valor_venda": "valor_venda",
                "desconto": "desconto",
                "nome_vendedor": "nome_vendedor",
                "nome_produto": "nome_produto",
                "cidade": "cidade",
                "estado": "estado",
                "forma_pagamento": "forma_pagamento",
                "status": "status",
                "categoria": "categoria",
            }
        }
    }


@pytest.fixture
def sales_df():
    return pd.DataFrame(
        {
            "venda_id": [1],
            "vendedor_id": [10],
            "produto_id": [100],
            "data_venda": [pd.Timestamp("2024-01-01")],
            "quantidade": [2],
            "valor_compra": [50],
            "valor_venda": [100],
            "desconto": [5],
            "nome_vendedor": ["Carlos"],
            "nome_produto": ["Notebook"],
            "cidade": ["Recife"],
            "estado": ["PE"],
            "forma_pagamento": ["Pix"],
            "status": ["Pago"],
            "categoria": ["Informática"],
        }
    )


# DataFrame válido
def test_validate_sales_data_success(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    result = validate_sales_data(sales_df)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1


# DataFrame vazio
def test_validate_sales_data_empty_df(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    empty_df = sales_df.iloc[0:0]

    with pytest.raises(ValueError):
        validate_sales_data(empty_df)


# Coluna obrigatória ausente
def test_validate_sales_data_missing_column(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df = sales_df.drop(columns=["categoria"])

    with pytest.raises(KeyError):
        validate_sales_data(sales_df)


# Gera IDs para valores nulos
def test_generate_missing_ids(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "produto_id"] = None

    result = validate_sales_data(sales_df)

    assert result["produto_id"].isna().sum() == 0


# Remove datas nulas
def test_remove_null_dates(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "data_venda"] = pd.NaT

    result = validate_sales_data(sales_df)

    assert result.empty


# Remove valores numéricos nulos
def test_remove_null_numeric(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "valor_venda"] = None

    result = validate_sales_data(sales_df)

    assert result.empty


# Desconto vira zero
def test_fill_discount_with_zero(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "desconto"] = None

    result = validate_sales_data(sales_df)

    assert result.loc[0, "desconto"] == 0


# Texto vira "não informado"
def test_fill_text_columns(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "cidade"] = None

    result = validate_sales_data(sales_df)

    assert result.loc[0, "cidade"] == "não informado"


# Remove duplicados
def test_remove_duplicates(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    duplicated = pd.concat(
        [sales_df, sales_df],
        ignore_index=True,
    )

    result = validate_sales_data(duplicated)

    assert len(result) == 1


# Valores negativos
def test_convert_negative_values(
    monkeypatch,
    fake_config,
    sales_df,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    sales_df.loc[0, "valor_venda"] = -100

    result = validate_sales_data(sales_df)

    assert result.loc[0, "valor_venda"] == 100


# Objeto que não é DataFrame
def test_invalid_dataframe(
    monkeypatch,
    fake_config,
):
    monkeypatch.setattr(
        "info_sales_mysql_api.cleanning.data_clean.load_all_configs",
        lambda _: fake_config,
    )

    with pytest.raises(TypeError):
        validate_sales_data([])
