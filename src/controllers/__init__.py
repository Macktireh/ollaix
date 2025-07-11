from litestar import get


@get("/health", summary="Health Check", description="Checks API health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
