from typing import Annotated

from litestar import get, post
from litestar.controller import Controller
from litestar.exceptions import ValidationException
from litestar.params import Body
from litestar.response import Stream

from schemas.chat_schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ModelsResponse,
)
from services.ai_service_interface import AIServiceInterface


class ChatController(Controller):
    path = "/"
    tags = ["Chat"]

    @get(
        "/models",
        summary="List available models",
        description="Returns a list of all available language models from supported services.",
    )
    async def get_available_models(self) -> ModelsResponse:
        """Fetches all available language models from the registered AI services."""
        return AIServiceInterface.get_all_models()

    @post(
        "/chat/completions",
        summary="Chat completion",
        description="Generates a chat completion response with optional streaming support.",
    )
    async def chat_completion(
        self,
        data: Annotated[
            ChatCompletionRequest,
            Body(
                title="Chat completion request",
                description="Payload containing the chat messages and model configuration.",
            ),
        ],
        ollama_service: AIServiceInterface,
        gemini_service: AIServiceInterface,
    ) -> Stream | ChatCompletionResponse:
        """
        Generates a response for a chat completion request.

        Supports streaming if `stream=True` is provided in the request.
        Automatically routes to the appropriate backend service based on the requested model.
        """
        if not data.messages:
            raise ValidationException("Messages list cannot be empty.")

        for message in data.messages:
            if not message.content:
                raise ValidationException("Message content cannot be empty.")
            if not message.role:
                raise ValidationException("Message role cannot be empty.")

        if not isinstance(data.stream, bool):
            raise ValidationException("Stream parameter must be a boolean.")

        service = self._get_service_for_model(
            data.model, ollama_service, gemini_service
        )

        if data.stream:
            return Stream(service.chat_completion_stream(data))  # type: ignore
        return await service.chat_completion(data)

    def _get_service_for_model(
        self,
        model: str,
        ollama_service: AIServiceInterface,
        gemini_service: AIServiceInterface,
    ) -> AIServiceInterface:
        """
        Determines the appropriate AI service to handle the request based on the selected model.

        Raises:
            ValidationException: If the provided model is not supported by any service.
        """
        if model in ollama_service.available_models:
            return ollama_service
        if model in gemini_service.available_models:
            return gemini_service

        raise ValidationException(f"Model '{model}' is not available.")
