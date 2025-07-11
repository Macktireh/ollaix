import json
from collections.abc import AsyncGenerator
from typing import Any, override

from ollama import AsyncClient

from config.settings import OLLAMA_MODEL_HOSTS
from schemas.chat_schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamChunk,
    ChatMessage,
    ModelInfo,
)
from services.ai_service_interface import AIServiceInterface


class OllamaService(AIServiceInterface):
    """Service to interact with Ollama."""

    available_models = ["gemma3:1b", "qwen3:1.7b", "deepseek-r1:1.5b"]
    provider_name = "ollama"

    def _get_client(self, model: str) -> AsyncClient:
        if model not in self.available_models:
            raise ValueError(f"Modèle '{model}' non disponible pour Ollama")
        return AsyncClient(host=OLLAMA_MODEL_HOSTS[model])

    @override
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        client = self._get_client(request.model)
        messages = self._convert_messages(request.messages)

        response = await client.chat(
            model=request.model,
            messages=messages,
            stream=False,
            options={
                "temperature": request.temperature,
                "top_p": request.top_p,
                "num_predict": request.max_tokens,
            }
            if any([request.temperature, request.top_p, request.max_tokens])
            else None,
        )

        return ChatCompletionResponse(
            model=request.model,
            choices=[
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response["message"]["content"],
                    },
                    "finish_reason": "stop",
                }
            ],
            usage={
                "prompt_tokens": response.get("prompt_eval_count", 0),
                "completion_tokens": response.get("eval_count", 0),
                "total_tokens": response.get("prompt_eval_count", 0)
                + response.get("eval_count", 0),
            },
        )

    @override
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, Any]:
        client = self._get_client(request.model)
        messages = self._convert_messages(request.messages)

        async for chunk in await client.chat(
            model=request.model,
            messages=messages,
            stream=True,
            options={
                "temperature": request.temperature,
                "top_p": request.top_p,
                "num_predict": request.max_tokens,
            }
            if any([request.temperature, request.top_p, request.max_tokens])
            else None,
        ):
            if chunk.get("message", {}).get("content"):
                stream_chunk = ChatCompletionStreamChunk(
                    model=request.model,
                    choices=[
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant",
                                "content": chunk["message"]["content"],
                            },
                            "finish_reason": None,
                        }
                    ],
                )
                yield f"data: {json.dumps(stream_chunk.__dict__, default=str)}\n\n"

            if chunk.get("done", False):
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

    @override
    def get_model_info(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                id="qwen3:1.7b",
                name="Qwen 3 1.7B",
                description="A lightweight and efficient language model by Alibaba, suitable for a wide range of general NLP tasks.",  # noqa: E501
                provider="ollama",
                context_length=32768,
            ),
            ModelInfo(
                id="deepseek-r1:1.5b",
                name="DeepSeek R1 1.5B",
                description="A 1.5B-parameter model optimized for reasoning and coding tasks, designed for high-performance inference.",  # noqa: E501
                provider="ollama",
                context_length=32768,
            ),
            ModelInfo(
                id="gemma3:1b",
                name="Gemma 3 1B",
                description="",  # noqa: E501
                provider="ollama",
                context_length=32768,
            ),
        ]

    def _convert_messages(self, messages: list[ChatMessage]) -> list[dict[str, str]]:
        """Converts messages to Ollama format."""
        return [{"role": message.role, "content": message.content} for message in messages]
