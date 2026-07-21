import pandas as pd
import pytest

from info_sales_mysql_api.summary.get_summary import create_sales_summary


def test_create_sales_summary_success(monkeypatch, sales_dataframe):
    """
    Verifica se o resumo de vendas é criado corretamente
    para um DataFrame válido.
    """

    # Simula o carregamento das configurações YAML.
    monkeypatch.setattr(
        "info_sales_mysql_api.summary.get_summary.load_all_configs",
        lambda _: {"db": {"columns": list(sales_dataframe.columns)}},
    )

    # Executa a função.
    summary = create_sales_summary(sales_dataframe)

    # Verifica se o retorno é um dicionário.
    assert isinstance(summary, dict)

    # Verifica se as principais seções existem.
    assert "metadata" in summary
    assert "kpis" in summary
    assert "products" in summary
    assert "categories" in summary
    assert "payments" in summary

    # Verifica alguns indicadores.
    assert summary["metadata"]["rows"] == len(sales_dataframe)
    assert summary["kpis"]["orders"] == len(sales_dataframe)

    # Receita e lucro devem ser positivos.
    assert summary["kpis"]["revenue"] > 0
    assert summary["kpis"]["profit"] > 0


def test_create_sales_summary_empty_dataframe(monkeypatch):
    """
    Verifica se ValueError é lançado quando
    o DataFrame está vazio.
    """

    df = pd.DataFrame()

    monkeypatch.setattr(
        "info_sales_mysql_api.summary.get_summary.load_all_configs",
        lambda _: {"db": {"columns": []}},
    )

    with pytest.raises(ValueError):
        create_sales_summary(df)


@pytest.fixture
def sales_dataframe():
    """
    Cria um DataFrame válido para utilização
    nos testes do resumo de vendas.
    """

    return pd.DataFrame(
        {
            "data_venda": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "quantidade": [2, 3],
            "valor_compra": [20, 30],
            "valor_venda": [50, 80],
            "desconto": [5, 10],
            "cidade": ["Recife", "Olinda"],
            "estado": ["PE", "PE"],
            "status": ["Pago", "Pago"],
            "forma_pagamento": ["PIX", "Cartão"],
            "nome_produto": ["Notebook", "Mouse"],
            "categoria": ["Informática", "Informática"],
            "nome_vendedor": ["Carlos", "Maria"],
        }
    )


def test_create_sales_summary_unexpected_error(monkeypatch, sales_dataframe):
    """
    Verifica se erros inesperados são propagados
    pela função.
    """

    monkeypatch.setattr(
        "info_sales_mysql_api.summary.get_summary.load_all_configs",
        lambda _: {"db": {"columns": list(sales_dataframe.columns)}},
    )

    def fake_groupby(*args, **kwargs):
        raise RuntimeError("Erro inesperado")

    monkeypatch.setattr(
        pd.DataFrame,
        "groupby",
        fake_groupby,
    )

    with pytest.raises(RuntimeError):
        create_sales_summary(sales_dataframe)
