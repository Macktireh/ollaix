import os

from litestar.exceptions import ImproperlyConfiguredException


def get_env_var(key: str, default: str | None = None) -> str:
    """Get an environment variable."""
    value = os.getenv(key, default)
    if value is None:
        raise ImproperlyConfiguredException(f"Missing environment variable: {key}")
    return value
