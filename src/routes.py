from litestar import Router

from controllers import health_check
from controllers.chat_controller import ChatController

chat_router = Router(
    path="/v1",
    route_handlers=[ChatController],
)

routes = [health_check, chat_router]
