from http import HTTPStatus

from litestar.testing import AsyncTestClient


class TestChatCompletionValidation:
    """Tests for request validation."""

    async def test_invalid_model(self, test_client: AsyncTestClient) -> None:
        """Test with non-existent model."""
        invalid_model_request = {
            "model": "non-existent-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False,
        }
        response = await test_client.post("/v1/chat/completions", json=invalid_model_request)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_empty_messages(self, test_client: AsyncTestClient) -> None:
        """Test with empty messages list."""
        empty_messages_request = {
            "model": "dummy-model:1.0",
            "messages": [],
            "stream": False,
        }
        response = await test_client.post("/v1/chat/completions", json=empty_messages_request)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_invalid_message_role(self, test_client: AsyncTestClient) -> None:
        """Test with invalid message role."""
        invalid_role_request = {
            "model": "dummy-model:1.0",
            "messages": [{"role": "invalid_role", "content": "Hello"}],
            "stream": False,
        }
        response = await test_client.post("/v1/chat/completions", json=invalid_role_request)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_missing_model_field(self, test_client: AsyncTestClient) -> None:
        """Test with missing model field."""
        payload = {
            "messages": [{"role": "user", "content": "Hello"}],
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_missing_messages_field(self, test_client: AsyncTestClient) -> None:
        """Test with missing messages field."""
        payload = {
            "model": "dummy-model:1.0",
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_invalid_message_structure(self, test_client: AsyncTestClient) -> None:
        """Test with invalid message structure."""
        payload = {
            "model": "dummy-model:1.0",
            "messages": [{"content": "Hello"}],
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_missing_message_content(self, test_client: AsyncTestClient) -> None:
        """Test with missing message content."""
        payload = {
            "model": "dummy-model:1.0",
            "messages": [{"role": "user"}],
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_empty_message_content(self, test_client: AsyncTestClient) -> None:
        """Test with empty message content."""
        payload = {
            "model": "dummy-model:1.0",
            "messages": [{"role": "user", "content": ""}],
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        # Empty content should be allowed, test that it doesn't crash
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_empty_role(self, test_client: AsyncTestClient) -> None:
        """Test with empty role."""
        payload = {
            "model": "dummy-model:1.0",
            "messages": [{"role": "", "content": "Hello"}],
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_invalid_stream_type(self, test_client: AsyncTestClient) -> None:
        """Test with invalid stream parameter type."""
        payload = {
            "model": "dummy-model:1.0",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": "ok",
        }

        response = await test_client.post("/v1/chat/completions", json=payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
