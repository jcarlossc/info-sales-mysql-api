import logging
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def get_load_sales(engine: Engine) -> pd.DataFrame:
    """
    Carrega dados consolidados de vendas
    a partir do banco de dados.

    A consulta realiza junção entre tabelas
    de vendas, produtos e vendedores para
    construção da base analítica.

    Parameters
    ----------
    engine : Engine
        Instância SQLAlchemy Engine utilizada
        para comunicação com banco.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo dados de vendas.

    Raises
    ------
    SQLAlchemyError
        Quando ocorre falha na consulta SQL.

    ValueError
        Quando o resultado retornado está vazio.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Iniciando carregamento dos dados de vendas.")

    # Consulta utilizada para consolidar
    # informações de vendas, produtos e vendedores.
    query = """

    SELECT
    v.venda_id,
    v.data_venda,
    v.quantidade,
    v.valor_compra,
    v.valor_venda,
    v.forma_pagamento,
    v.desconto,
    v.cidade,
    v.estado,
    v.status,

    p.produto_id,
    p.nome_produto,
    p.categoria,

    vd.vendedor_id,
    vd.nome_vendedor

    FROM vendas AS v

    INNER JOIN produtos AS p
        ON v.produto_id = p.produto_id

    INNER JOIN vendedor AS vd
        ON v.vendedor_id = vd.vendedor_id;
    """

    try:
        # Executa consulta SQL e converte
        # resultado para DataFrame Pandas.
        df = pd.read_sql(query, engine)

        # Evita continuar pipeline
        # com base vazia.
        if df.empty:
            logger.warning("Consulta retornou dataset vazio.")

            raise ValueError("Nenhum registro encontrado.")

        logger.info(f"{len(df)} registros carregados.")

        return df

    except SQLAlchemyError as error:
        logger.error(f"Erro ao executar consulta SQL: {error}")
        raise

    except Exception as error:
        logger.exception(f"Erro inesperado ao carregar vendas: {error}")
        raise
