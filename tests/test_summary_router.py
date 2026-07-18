from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from info_sales_mysql_api.api.routes.summary_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def summary_mock():
    return {
        "metadata": {
            "rows": 100,
            "columns": 20,
            "products": 10,
            "sellers": 5,
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31",
            },
        },
        "kpis": {
            "revenue": 10000.0,
            "profit": 2500.0,
            "orders": 100,
            "items_sold": 350,
            "average_ticket": 100.0,
            "average_discount": 5.5,
            "margin": 25.0,
        },
        "products": {
            "top_revenue": {"Notebook": 5000},
            "top_quantity": {"Mouse": 100},
            "lowest_revenue": {"Cabo": 20},
        },
        "categories": {
            "revenue": {"Informática": 10000},
            "quantity": {"Informática": 350},
        },
        "sellers": {
            "revenue": {"Carlos": 10000},
            "orders": {"Carlos": 100},
            "profit": {"Carlos": 2500},
        },
        "geography": {
            "states": {"SP": 5000},
            "cities": {"São Paulo": 5000},
        },
        "time": {
            "year": {2024: 10000},
            "month": {"January": 10000},
            "weekday": {"Monday": 2500},
        },
        "payments": {
            "methods": {"PIX": 6000},
        },
        "status": {
            "orders": {"Concluído": 100},
        },
    }
