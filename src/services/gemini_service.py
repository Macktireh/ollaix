import json
from collections.abc import AsyncGenerator
from typing import Any, override

from google.genai import Client, types
from google.genai.errors import APIError
from litestar.exceptions import (
    HTTPException,
    ImproperlyConfiguredException,
    ValidationException,
)

from config.settings import GEMINI_API_KEY
from schemas.chat_schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamChunk,
    ChatMessage,
    ModelInfo,
)
from services.ai_service_interface import AIServiceInterface


class GeminiService(AIServiceInterface):
    """Service to interact with Gemini."""

    available_models = ["gemini-2.0-flash"]
    provider_name = "gemini"

    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise ImproperlyConfiguredException("GEMINI_API_KEY is not configured")
        self.client = Client(api_key=GEMINI_API_KEY)

    @override
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        if request.model not in self.available_models:
            raise ValidationException(f"Model '{request.model}' is not available for Gemini")

        messages = self._convert_messages(request.messages)
        system_instruction = self._extract_system_instruction(request.messages)

        config = types.GenerateContentConfig(
            temperature=request.temperature,
            top_p=request.top_p,
            max_output_tokens=request.max_tokens,
            system_instruction=system_instruction,
        )
        try:
            response = self.client.models.generate_content(
                model=request.model,
                contents=messages,
                config=config,
            )

            content = response.text if response.text else ""

            return ChatCompletionResponse(
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": content,
                        },
                        "finish_reason": "stop",
                    }
                ],
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count
                    if response.usage_metadata
                    else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count
                    if response.usage_metadata
                    else 0,
                    "total_tokens": response.usage_metadata.total_token_count
                    if response.usage_metadata
                    else 0,
                },
            )
        except APIError as e:
            raise HTTPException(
                detail=e.message if e.message else "Internal Server Error", status_code=e.code
            ) from e

    @override
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, Any]:
        if request.model not in self.available_models:
            raise ValueError(f"Modèle '{request.model}' non disponible pour Gemini")

        messages = self._convert_messages(request.messages)
        system_instruction = self._extract_system_instruction(request.messages)

        config = types.GenerateContentConfig(
            temperature=request.temperature,
            top_p=request.top_p,
            max_output_tokens=request.max_tokens,
            system_instruction=system_instruction,
        )
        try:
            response_stream = self.client.models.generate_content_stream(
                model=request.model,
                contents=messages,
                config=config,
            )

            for chunk in response_stream:
                if chunk.text:
                    stream_chunk = ChatCompletionStreamChunk(
                        model=request.model,
                        choices=[
                            {
                                "index": 0,
                                "delta": {
                                    "role": "assistant",
                                    "content": chunk.text,
                                },
                                "finish_reason": None,
                            }
                        ],
                    )
                    yield f"data: {json.dumps(stream_chunk.__dict__, default=str)}\n\n"

            # Chunk final
            final_chunk = ChatCompletionStreamChunk(
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            )
            yield f"data: {json.dumps(final_chunk.__dict__, default=str)}\n\n"
            yield "data: [DONE]\n\n"
        except APIError as e:
            raise HTTPException(
                detail=e.message if e.message else "Internal Server Error", status_code=e.code
            ) from e

    @override
    def get_model_info(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                id="gemini-2.0-flash",
                name="Gemini 2.0 Flash",
                description="Google's ultra-fast multimodal model with massive context support, ideal for long documents and fast generation.",  # noqa: E501
                provider="google",
                context_length=1000000,
            ),
        ]

    def _convert_messages(self, messages: list[ChatMessage]) -> list[str]:
        """Converts messages to Gemini format (excludes system messages)."""
        return [message.content for message in messages if message.role != "system"]

    def _extract_system_instruction(self, messages: list[ChatMessage]) -> str:
        """Extracts the system instruction from the messages."""
        system_messages = [message.content for message in messages if message.role == "system"]
        return " ".join(system_messages) if system_messages else ""
