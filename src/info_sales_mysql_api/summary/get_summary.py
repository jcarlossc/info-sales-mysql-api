from __future__ import annotations
import logging
from pathlib import Path
import pandas as pd

from info_sales_mysql_api.utils.load_yaml.loader_yaml import load_all_configs


def create_sales_summary(df: pd.DataFrame) -> dict:
    """
    Cria um resumo analítico completo do conjunto de dados de vendas.

    A função calcula indicadores (KPIs) e produz análises por
    produto, categoria, vendedor, localização geográfica,
    período, forma de pagamento e status dos pedidos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados das vendas.

    Returns
    -------
    dict
        Dicionário contendo todas as métricas calculadas.

    Raises
    ------
    TypeError
        Caso o parâmetro informado não seja um DataFrame.

    ValueError
        Caso o DataFrame esteja vazio.

    KeyError
        Caso alguma coluna obrigatória não exista.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Iniciando criação de métrica e KPIs.")

    # Configura caminhos
    config_path = Path("config")

    try:
        configs = load_all_configs(config_path)

        # Verifica colunas a serem calculadas
        required_columns = configs["db"]["columns"]

        missing = [col for col in required_columns if col not in df.columns]

        # Verifica df é instância de DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df deve ser um pandas.DataFrame.")

        # Verifica df está vazio
        if df.empty:
            raise ValueError("O DataFrame está vazio.")

        # Verifica se todas as colunas
        # necessárias existem.
        if missing:
            logger.warning(f"Colunas ausentes: {missing}")

            raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

        # Colunas derivadas utilizadas em praticamente todas as análises.
        df["faturamento"] = df["valor_venda"] * df["quantidade"] - df["desconto"]

        df["lucro"] = (df["valor_venda"] - df["valor_compra"]) * df["quantidade"]

        df["ano"] = df["data_venda"].dt.year
        df["mes"] = df["data_venda"].dt.month_name()
        df["dia_semana"] = df["data_venda"].dt.day_name()

        # Dicionário com as métricas e KPIs
        summary = {
            "metadata": {
                "rows": len(df),
                "columns": len(df.columns),
                "products": df["nome_produto"].nunique(),
                "sellers": df["nome_vendedor"].nunique(),
                "period": {
                    "start": str(df["data_venda"].min()),
                    "end": str(df["data_venda"].max()),
                },
            },
            "kpis": {
                "revenue": round(df["faturamento"].sum(), 2),
                "profit": round(df["lucro"].sum(), 2),
                "orders": len(df),
                "items_sold": int(df["quantidade"].sum()),
                "average_ticket": round(
                    df["faturamento"].sum() / len(df),
                    2,
                ),
                "average_discount": round(
                    df["desconto"].mean(),
                    2,
                ),
                "margin": round(
                    (df["lucro"].sum() / df["faturamento"].sum()) * 100,
                    2,
                ),
            },
            "products": {
                "top_revenue": (
                    df.groupby("nome_produto")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .round(2)
                    .head(10)
                    .to_dict()
                ),
                "top_quantity": (
                    df.groupby("nome_produto")["quantidade"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                    .to_dict()
                ),
                "lowest_revenue": (
                    df.groupby("nome_produto")["faturamento"]
                    .sum()
                    .sort_values()
                    .round(2)
                    .head(10)
                    .to_dict()
                ),
            },
            "categories": {
                "revenue": (
                    df.groupby("categoria")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .to_dict()
                ),
                "quantity": (
                    df.groupby("categoria")["quantidade"]
                    .sum()
                    .sort_values(ascending=False)
                    .to_dict()
                ),
            },
            "sellers": {
                "revenue": (
                    df.groupby("nome_vendedor")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .round(2)
                    .to_dict()
                ),
                "orders": (
                    df.groupby("nome_vendedor")
                    .size()
                    .sort_values(ascending=False)
                    .to_dict()
                ),
                "profit": (
                    df.groupby("nome_vendedor")["lucro"]
                    .sum()
                    .sort_values(ascending=False)
                    .round(2)
                    .to_dict()
                ),
            },
            "geography": {
                "states": (
                    df.groupby("estado")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .to_dict()
                ),
                "cities": (
                    df.groupby("cidade")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(20)
                    .to_dict()
                ),
            },
            "time": {
                "year": (df.groupby("ano")["faturamento"].sum().to_dict()),
                "month": (df.groupby("mes")["faturamento"].sum().to_dict()),
                "weekday": (df.groupby("dia_semana")["faturamento"].sum().to_dict()),
            },
            "payments": {
                "methods": (
                    df.groupby("forma_pagamento")["faturamento"]
                    .sum()
                    .sort_values(ascending=False)
                    .to_dict()
                )
            },
            "status": {"orders": (df["status"].value_counts().to_dict())},
        }

        logger.info("Término da criação de métrica e KPIs.")

        return summary

    except (TypeError, ValueError, KeyError):
        logger.exception("Erro de validação.")
        raise

    except Exception:
        logger.exception("Erro inesperado durante criação do resumo.")
        raise
