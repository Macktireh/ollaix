from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from schemas.chat_schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ModelInfo,
    ModelsResponse,
)


class AIServiceInterface(ABC):
    """Abstract interface for AI services."""

    available_models: list[str] = []
    provider_name: str

    @abstractmethod
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Generates a completion chat response."""
        pass

    @abstractmethod
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, Any]:
        """Generates a stream of completion chat responses."""
        pass

    @abstractmethod
    def get_model_info(self) -> list[ModelInfo]:
        """Returns information on supported models."""
        pass

    @staticmethod
    def get_all_models() -> ModelsResponse:
        """Returns all available models of all services."""
        from services.dummy_service import DummyService
        from services.gemini_service import GeminiService
        from services.ollama_service import OllamaService

        ollama_service = OllamaService()
        gemini_service = GeminiService()
        dummy_service = DummyService()

        all_models = []
        all_models.extend(ollama_service.get_model_info())
        all_models.extend(gemini_service.get_model_info())
        all_models.extend(dummy_service.get_model_info())

        return ModelsResponse(data=all_models)
