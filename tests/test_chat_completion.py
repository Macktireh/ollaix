import json
from http import HTTPStatus
from typing import Any

import pytest
from litestar.testing import AsyncTestClient


class TestChatCompletion:
    """Basic tests for chat completion endpoint."""

    async def test_chat_completion(
        self, test_client: AsyncTestClient, base_chat_request: dict[str, Any]
    ) -> None:
        """Test chat completion without streaming."""
        payload = {**base_chat_request, "stream": False}

        response = await test_client.post("/v1/chat/completions", json=payload)

        assert response.status_code == HTTPStatus.CREATED

        data = response.json()
        assert data["object"] == "chat.completion"
        assert data["model"] == "dummy-model:1.0"
        assert "id" in data
        assert "created" in data
        assert isinstance(data["choices"], list)
        assert len(data["choices"]) > 0

    async def test_chat_completion_choice_structure(
        self, test_client: AsyncTestClient, simple_chat_request: dict[str, Any]
    ) -> None:
        """Test the structure of the choice in the response."""
        response = await test_client.post("/v1/chat/completions", json=simple_chat_request)

        assert response.status_code == HTTPStatus.CREATED

        data = response.json()
        choice = data["choices"][0]

        assert choice["index"] == 0
        assert choice["message"]["role"] == "assistant"
        assert isinstance(choice["message"]["content"], str)
        assert len(choice["message"]["content"]) > 0
        assert choice["finish_reason"] == "stop"


class TestChatCompletionStreaming:
    """Tests for streaming functionality."""

    async def test_chat_completion_streaming(
        self, test_client: AsyncTestClient, base_chat_request: dict[str, Any]
    ) -> None:
        """Test chat completion with streaming."""
        payload = {**base_chat_request, "stream": True}

        response = await test_client.post("/v1/chat/completions", json=payload)

        assert response.status_code == HTTPStatus.CREATED
        assert response.headers.get("content-type") == "application/json"

        # Check that response is streaming
        content = response.text
        assert content.startswith("data:")
        assert "[DONE]" in content

    async def test_streaming_chunks_structure(
        self, test_client: AsyncTestClient, simple_chat_request: dict[str, Any]
    ) -> None:
        """Test the structure of streaming chunks."""
        payload = {**simple_chat_request, "stream": True}

        response = await test_client.post("/v1/chat/completions", json=payload)

        assert response.status_code == HTTPStatus.CREATED

        # Parse streaming chunks
        content = response.text
        lines = content.strip().split("\n")
        data_lines = [line for line in lines if line.startswith("data:")]

        assert len(data_lines) > 0

        # Check first non-[DONE] chunk
        first_data_line = next(line for line in data_lines if not line.endswith("[DONE]"))
        chunk_json = json.loads(first_data_line.replace("data: ", ""))

        assert chunk_json["object"] == "chat.completion.chunk"
        assert chunk_json["model"] == "dummy-model:1.0"
        assert "id" in chunk_json
        assert "created" in chunk_json
        assert isinstance(chunk_json["choices"], list)

    async def test_streaming_content_chunks(
        self, test_client: AsyncTestClient, simple_chat_request: dict[str, Any]
    ) -> None:
        """Test that streaming produces content chunks."""
        payload = {**simple_chat_request, "stream": True}

        response = await test_client.post("/v1/chat/completions", json=payload)

        assert response.status_code == HTTPStatus.CREATED

        # Extract content chunks
        content = response.text
        lines = content.strip().split("\n")
        data_lines = [line for line in lines if line.startswith("data:")]

        content_chunks = []
        for line in data_lines:
            if not line.endswith("[DONE]"):
                try:
                    chunk_data = json.loads(line.replace("data: ", ""))
                    if chunk_data["choices"] and chunk_data["choices"][0].get("delta", {}).get(
                        "content"
                    ):
                        content_chunks.append(chunk_data["choices"][0]["delta"]["content"])
                except json.JSONDecodeError:
                    pass

        assert len(content_chunks) > 0
        assert all(isinstance(chunk, str) for chunk in content_chunks)

    @pytest.mark.parametrize("stream_value", [True, False])
    async def test_both_streaming_modes(
        self, test_client: AsyncTestClient, simple_chat_request: dict[str, Any], stream_value: bool
    ) -> None:
        """Parametrized test for both streaming and non-streaming modes."""
        payload = {**simple_chat_request, "stream": stream_value}

        response = await test_client.post("/v1/chat/completions", json=payload)

        assert response.status_code == HTTPStatus.CREATED

        if stream_value:
            # Streaming mode
            assert response.headers.get("content-type") == "application/json"
            assert "data:" in response.text
            assert "[DONE]" in response.text
        else:
            # Non-streaming mode
            data = response.json()
            assert data["object"] == "chat.completion"
            assert data["model"] == "dummy-model:1.0"
            assert len(data["choices"]) > 0
