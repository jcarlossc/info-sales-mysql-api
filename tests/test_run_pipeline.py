from unittest.mock import MagicMock

from info_sales_mysql_api.pipeline.pipeline_service import run_pipeline


def test_run_pipeline_success(monkeypatch):
    fake_engine = MagicMock()

    fake_df = MagicMock()
    fake_df.__len__.return_value = 100

    expected = {
        "kpis": {
            "revenue": 1000.0,
        }
    }

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.Settings",
        lambda: MagicMock(),
    )

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.retry_connect",
        lambda *args, **kwargs: fake_engine,
    )

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.get_load_sales",
        lambda engine: fake_df,
    )

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.standardize_sales_data",
        lambda df: fake_df,
    )

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.validate_sales_data",
        lambda df: fake_df,
    )

    monkeypatch.setattr(
        "info_sales_mysql_api.pipeline.pipeline_service.create_sales_summary",
        lambda df: expected,
    )

    result = run_pipeline()

    assert result == expected

    fake_engine.dispose.assert_called_once()
