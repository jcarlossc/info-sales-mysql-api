from info_sales_mysql_api.api.dependencies.api_key import validate_api_key


def test_validate_api_key_success(monkeypatch):
    """
    Deve retornar a API Key quando ela for válida.
    """

    monkeypatch.setattr(
        "info_sales_mysql_api.api.dependencies.api_key.settings",
        type(
            "FakeSettings",
            (),
            {"api_key": "abc123"},
        )(),
    )

    result = validate_api_key(
        api_key="abc123",
    )

    assert result == "abc123"
