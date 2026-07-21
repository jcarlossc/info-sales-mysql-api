import pandas as pd
import pytest
from sqlalchemy.exc import SQLAlchemyError

from info_sales_mysql_api.database.query.load_sales import get_load_sales


def test_get_load_sales_success(monkeypatch):
    """
    Verifica se a função retorna um DataFrame
    quando a consulta SQL é executada com sucesso.
    """

    # DataFrame simulado retornado pela consulta.
    expected_df = pd.DataFrame(
        {
            "venda_id": [1, 2],
            "produto_id": [10, 20],
            "quantidade": [5, 3],
        }
    )

    # Simula a execução da consulta SQL.
    def fake_read_sql(query, engine):
        return expected_df

    # Substitui temporariamente o pandas.read_sql.
    monkeypatch.setattr(pd, "read_sql", fake_read_sql)

    # Engine fictícia (não será utilizada).
    engine = object()

    # Executa a função.
    result = get_load_sales(engine)

    # Verifica se o DataFrame retornado é o esperado.
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_load_sales_empty_dataframe(monkeypatch):
    """
    Verifica se ValueError é lançado quando
    a consulta retorna um DataFrame vazio.
    """

    # Simula retorno vazio da consulta.
    empty_df = pd.DataFrame()

    def fake_read_sql(query, engine):
        return empty_df

    monkeypatch.setattr(pd, "read_sql", fake_read_sql)

    engine = object()

    # Verifica se a exceção correta é lançada.
    with pytest.raises(ValueError, match="Nenhum registro encontrado"):
        get_load_sales(engine)


def test_get_load_sales_sqlalchemy_error(monkeypatch):
    """
    Verifica se SQLAlchemyError é propagado
    quando ocorre erro durante a consulta SQL.
    """

    # Simula erro do SQLAlchemy.
    def fake_read_sql(query, engine):
        raise SQLAlchemyError("Erro de conexão")

    monkeypatch.setattr(pd, "read_sql", fake_read_sql)

    engine = object()

    # Verifica se a exceção é propagada.
    with pytest.raises(SQLAlchemyError):
        get_load_sales(engine)


def test_get_load_sales_unexpected_error(monkeypatch):
    """
    Verifica se erros inesperados são propagados
    pela função.
    """

    # Simula erro inesperado.
    def fake_read_sql(query, engine):
        raise RuntimeError("Erro inesperado")

    monkeypatch.setattr(pd, "read_sql", fake_read_sql)

    engine = object()

    # Verifica se a exceção é propagada.
    with pytest.raises(RuntimeError):
        get_load_sales(engine)
