import logging
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def get_load_sales(engine: Engine) -> pd.DataFrame:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando carregamento dos dados de vendas.")

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
        df = pd.read_sql(query, engine)

        return df

    except SQLAlchemyError as error:
        logger.error(f"Erro ao executar consulta SQL: {error}")
        raise

    except Exception as error:
        logger.exception(f"Erro inesperado ao carregar vendas: {error}")
        raise
