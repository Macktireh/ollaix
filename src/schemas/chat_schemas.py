from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from litestar.dto import DataclassDTO


@dataclass
class ChatMessage:
    """Represents a message in a conversation."""

    role: Literal["assistant", "user", "system"]
    content: str


@dataclass
class ChatCompletionRequest:
    """Request for cat completion."""

    model: str
    messages: list[ChatMessage]
    stream: bool = False
    max_tokens: int | None = None
    temperature: float | None = None
    top_p: float | None = None


@dataclass
class ChatCompletionResponse:
    """Response from a cat completion."""

    id: UUID = field(default_factory=uuid4)
    object: Literal["chat.completion"] = "chat.completion"
    created: datetime = field(default_factory=datetime.now)
    model: str = ""
    choices: list[dict] = field(default_factory=list)
    usage: dict | None = None


@dataclass
class ChatCompletionStreamChunk:
    """Data chunk for streaming."""

    id: UUID = field(default_factory=uuid4)
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: datetime = field(default_factory=datetime.now)
    model: str = ""
    choices: list[dict] = field(default_factory=list)


@dataclass
class ModelInfo:
    """Information on a language model."""

    id: str
    name: str
    description: str
    provider: Literal["dummy", "ollama", "google"]
    context_length: int | None = None


@dataclass
class ModelsResponse:
    """Answer containing the list of models."""

    object: Literal["list"] = "list"
    data: list[ModelInfo] = field(default_factory=list)


@dataclass
class ErrorResponse:
    """Standardized error response."""

    error: dict[str, str]


# DTOs for automatic validation
ChatCompletionRequestDTO = DataclassDTO[ChatCompletionRequest]
ChatCompletionResponseDTO = DataclassDTO[ChatCompletionResponse]
ModelsResponseDTO = DataclassDTO[ModelsResponse]
