from litestar import Router
from litestar.di import Provide

from controllers import health_check
from controllers.chat_controller import ChatController
from services.gemini_service import GeminiService
from services.ollama_service import OllamaService

chat_router = Router(
    path="/v1",
    dependencies={
        "ollama_service": Provide(OllamaService, sync_to_thread=False),
        "gemini_service": Provide(GeminiService, sync_to_thread=False),
    },
    route_handlers=[ChatController],
)

routes = [health_check, chat_router]
