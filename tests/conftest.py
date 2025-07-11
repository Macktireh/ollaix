from collections.abc import AsyncIterator
from typing import Any

import pytest
from litestar.testing import AsyncTestClient

from src.main import app


@pytest.fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient]:
    """Fixture to create an asynchronous test client."""
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def base_chat_request() -> dict[str, Any]:
    """Base payload for chat completion tests."""
    return {
        "model": "dummy-model:1.0",
        "messages": [
            {"role": "user", "content": "Hello, what's your name?"},
            {
                "role": "assistant",
                "content": "Hello ! I'm an AI assistant. How can I help you today?",
            },
            {"role": "user", "content": "Perfect! Can you help me with some Python code?"},
        ],
    }


@pytest.fixture
def simple_chat_request() -> dict[str, Any]:
    """Simple chat request for basic tests."""
    return {
        "model": "dummy-model:1.0",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False,
    }


@pytest.fixture
def chat_request_with_system() -> dict[str, Any]:
    """Chat request with system message."""
    return {
        "model": "dummy-model:1.0",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
            {"role": "user", "content": "Tell me more about it."},
        ],
        "stream": False,
    }
