from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import init_db
from src.routes.health import router as health_route
from src.routes.agent import router as agent_router
from src.routes.telegram import router as telegram_router
from src.routes.user import router as user_router
from src import config
from src import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting application: {app.title} {app.version}")

    await init_db()
    logger.info("Application startup complete")

    yield

    logger.info("Application shutdown initiated")


app = FastAPI(
    title="Mental Health Support Agent",
    description="AI agent to support people.",
    version=config.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_route)
app.include_router(agent_router)
app.include_router(telegram_router)
app.include_router(user_router)
