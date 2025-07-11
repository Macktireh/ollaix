from litestar import get
from litestar.controller import Controller

from schemas.chat_schemas import (
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
