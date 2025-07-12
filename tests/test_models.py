from http import HTTPStatus

from litestar.testing import AsyncTestClient


class TestModelsEndpoint:
    """Tests for the models endpoint."""

    async def test_get_available_models(self, test_client: AsyncTestClient) -> None:
        """Test retrieving the list of available models."""
        response = await test_client.get("/v1/models")

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["object"] == "list"
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

    async def test_models_present(self, test_client: AsyncTestClient) -> None:
        """Test that the models are present in the list."""
        response = await test_client.get("/v1/models")

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        model_ids = [model["id"] for model in data["data"]]
        models = ["gemini-2.0-flash", "qwen3:1.7b", "deepseek-r1:1.5b", "dummy-model:1.0"]
        assert all(model in model_ids for model in models)
