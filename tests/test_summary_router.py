import pytest

from fastapi.testclient import TestClient
from unittest.mock import patch
from info_sales_mysql_api.main import app
from info_sales_mysql_api.api.dependencies.api_key import validate_api_key


@pytest.fixture
def client():
    app.dependency_overrides[validate_api_key] = lambda: "abc123"

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def summary_mock():
    """
    Retorna um resumo simulado utilizado nos testes.
    """
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


# Simula a execução do pipeline.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary(mock_pipeline, client, summary_mock):
    """
    Deve retornar o resumo completo das vendas.
    """
    mock_pipeline.return_value = summary_mock

    response = client.get("/summary")

    assert response.status_code == 200
    assert response.json()["kpis"]["revenue"] == 10000.0
    assert response.json()["metadata"]["rows"] == 100


# Simula a execução do pipeline.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_section(mock_pipeline, client, summary_mock):
    """
    Deve retornar uma seção específica do resumo.
    """
    mock_pipeline.return_value = summary_mock

    response = client.get("/summary/kpis")

    assert response.status_code == 200
    assert response.json()["margin"] == 25.0


# Simula a execução do pipeline.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_item(mock_pipeline, client, summary_mock):
    """
    Deve retornar um item específico de uma seção.
    """
    mock_pipeline.return_value = summary_mock

    response = client.get("/summary/kpis/margin")

    assert response.status_code == 200
    assert response.json() == 25.0


# Simula erro de validação do schema.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_validation_error(mock_pipeline, client):
    mock_pipeline.return_value = {}

    response = client.get("/summary")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro ao validar a estrutura da resposta."


# Simula erro inesperado no pipeline.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_internal_error(mock_pipeline, client):
    mock_pipeline.side_effect = Exception("Erro")

    response = client.get("/summary")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno ao processar a requisição."


# Simula uma seção inexistente.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_section_not_found(mock_pipeline, client):
    mock_pipeline.return_value = {"kpis": {}}

    response = client.get("/summary/inexistente")

    assert response.status_code == 404


# Simula erro ao consultar uma seção.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_section_internal_error(mock_pipeline, client):
    mock_pipeline.side_effect = Exception("Erro")

    response = client.get("/summary/kpis")

    assert response.status_code == 500


# Simula uma seção inexistente.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_item_section_not_found(mock_pipeline, client):
    mock_pipeline.return_value = {"kpis": {}}

    response = client.get("/summary/outra/faturamento")

    assert response.status_code == 404


# Simula um item inexistente.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_item_not_found(mock_pipeline, client):
    mock_pipeline.return_value = {"kpis": {"lucro": 100}}

    response = client.get("/summary/kpis/faturamento")

    assert response.status_code == 404


# Simula erro ao consultar um item.
@patch("info_sales_mysql_api.api.routes.summary_router.run_pipeline")
def test_get_summary_item_internal_error(mock_pipeline, client):
    mock_pipeline.side_effect = Exception("Erro")

    response = client.get("/summary/kpis/lucro")

    assert response.status_code == 500
