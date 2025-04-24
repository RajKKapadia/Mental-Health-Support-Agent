from fastapi import APIRouter, status

from src.schemas.health import HealthResponse
from src import config

router = APIRouter(prefix=f"/api/{config.API_VERSION}", tags=["HOME"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def get_health():
    return HealthResponse(message="ALL IS WELL", status=status.HTTP_200_OK)
