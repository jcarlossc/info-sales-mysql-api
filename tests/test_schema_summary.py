import pytest
from pydantic import ValidationError

from info_sales_mysql_api.api.schema.schema_summary import SalesSummary


def create_summary() -> dict:
    return {
        "metadata": {
            "rows": 100,
            "columns": 12,
            "products": 20,
            "sellers": 5,
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31",
            },
        },
        "kpis": {
            "revenue": 10000.0,
            "profit": 2500.0,
            "orders": 80,
            "items_sold": 350,
            "average_ticket": 125.0,
            "average_discount": 8.5,
            "margin": 25.0,
        },
        "products": {
            "top_revenue": {"Notebook": 5000.0},
            "top_quantity": {"Mouse": 150},
            "lowest_revenue": {"Cabo": 20.0},
        },
        "categories": {
            "revenue": {"Eletrônicos": 8000.0},
            "quantity": {"Eletrônicos": 250},
        },
        "sellers": {
            "revenue": {"Carlos": 5000.0},
            "orders": {"Carlos": 45},
            "profit": {"Carlos": 1200.0},
        },
        "geography": {
            "states": {"SP": 7000.0},
            "cities": {"São Paulo": 5000.0},
        },
        "time": {
            "year": {2024: 10000.0},
            "month": {"January": 1200.0},
            "weekday": {"Monday": 1800.0},
        },
        "payments": {
            "methods": {"PIX": 5000.0},
        },
        "status": {
            "orders": {"Concluído": 80},
        },
    }


def test_sales_summary_should_create_model() -> None:
    summary = SalesSummary(**create_summary())

    assert summary.metadata.rows == 100
    assert summary.kpis.revenue == 10000.0
    assert summary.products.top_quantity["Mouse"] == 150


def test_sales_summary_should_raise_validation_error() -> None:
    summary = create_summary()

    del summary["metadata"]["rows"]

    with pytest.raises(ValidationError):
        SalesSummary(**summary)
