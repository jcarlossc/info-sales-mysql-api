from __future__ import annotations
import logging
import pandas as pd


def create_sales_summary(df: pd.DataFrame) -> dict:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando criação de métrica e KPIs.")

    df = df.copy()

    df["faturamento"] = df["valor_venda"] * df["quantidade"] - df["desconto"]

    df["lucro"] = (df["valor_venda"] - df["valor_compra"]) * df["quantidade"]

    df["ano"] = df["data_venda"].dt.year
    df["mes"] = df["data_venda"].dt.month_name()
    df["dia_semana"] = df["data_venda"].dt.day_name()

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
