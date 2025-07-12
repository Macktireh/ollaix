from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.exceptions import HTTPException, ImproperlyConfiguredException, ValidationException

from config.exception_handler import app_exception_handler
from config.settings import CORS_ALLOWED_ORIGINS, DEBUG, openapi_config
from routes import routes

cors_config = CORSConfig(allow_origins=CORS_ALLOWED_ORIGINS)


app = Litestar(
    route_handlers=routes,
    openapi_config=openapi_config,
    debug=DEBUG,
    cors_config=cors_config,
    exception_handlers={
        HTTPException: app_exception_handler,
        ImproperlyConfiguredException: app_exception_handler,
        ValidationException: app_exception_handler,
    },
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
