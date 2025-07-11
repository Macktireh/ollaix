from http import HTTPStatus

from litestar.testing import AsyncTestClient


class TestHealthEndpoint:
    """Tests for the health endpoint."""

    async def test_health_check(self, test_client: AsyncTestClient) -> None:
        """Test the health check endpoint."""
        response = await test_client.get("/health")
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert data["status"] == "healthy"
