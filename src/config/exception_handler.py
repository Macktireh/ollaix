from http import HTTPStatus

from litestar import Request, Response
from litestar.exceptions import HTTPException, ImproperlyConfiguredException, ValidationException

ExceptionType = HTTPException | ImproperlyConfiguredException | ValidationException


def get_http_status_code(exc: ExceptionType) -> HTTPStatus:
    match exc:
        case ValidationException():
            return HTTPStatus.UNPROCESSABLE_ENTITY
        case ImproperlyConfiguredException():
            return HTTPStatus.INTERNAL_SERVER_ERROR
        case HTTPException():
            return HTTPStatus(exc.status_code)
        case _:
            return HTTPStatus.INTERNAL_SERVER_ERROR


def get_exception_detail(exc: ExceptionType) -> str:
    if isinstance(exc, ImproperlyConfiguredException):
        return "Internal Server Error"
    return getattr(exc, "detail", str(exc))


def app_exception_handler(request: Request, exc: ExceptionType) -> Response:
    """Exception handler for the application."""
    status_code = get_http_status_code(exc)
    return Response(
        content={
            "status_code": status_code,
            "detail": get_exception_detail(exc),
        },
        status_code=status_code,
    )
