import pandas as pd
from unittest.mock import patch

from info_sales_mysql_api.database.query.load_sales import get_load_sales


def test_get_load_sales_retorna_dataframe():
    """
    Verifica se a função retorna um DataFrame
    quando a consulta SQL retorna dados.
    """

    # Arrange (Preparação)

    # Cria um DataFrame falso simulando
    # o retorno do banco de dados.
    dados_mock = pd.DataFrame(
        {
            "vendas_id": [1],
            "nome_produto": ["Notebook"],
            "quantidade": [2],
            "vendedor": ["Carlos"],
        }
    )

    # Cria um engine falso.
    # Como não vamos acessar banco real,
    # qualquer objeto serve.
    engine_mock = "engine_teste"

    # Substitui temporariamente pd.read_sql
    # pela nossa função falsa.
    with patch(
        "info_sales_mysql_api.database.query.load_sales.pd.read_sql"
    ) as mock_sql:
        # Define o retorno da consulta simulada
        mock_sql.return_value = dados_mock

        # Act (Execução)

        resultado = get_load_sales(engine_mock)

        # Assert (Verificação)

        # Verifica se retornou um DataFrame
        assert isinstance(resultado, pd.DataFrame)

        # Verifica se possui registros
        assert len(resultado) == 1

        # Verifica se a coluna esperada existe
        assert "nome_produto" in resultado.columns
