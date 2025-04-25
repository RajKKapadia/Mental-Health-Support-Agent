import logging

import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src import config
from src.models.base import Base

logger = logging.getLogger(__name__)

DB_USERNAME = config.DB_USERNAME
DB_PASSWORD = config.DB_PASSWORD
DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_PORT = config.DB_PORT

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
logger.info(
    f"Connecting to database: postgresql+asyncpg://{DB_USERNAME}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    logger.debug("Creating new database session")
    try:
        async with AsyncSessionLocal() as session:
            yield session
            logger.debug("Database session closed")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise


SQLALCHEMY_DATABASE_URL_SYNC = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine_sync = create_engine(
    url=SQLALCHEMY_DATABASE_URL_SYNC, echo=True, pool_pre_ping=True
)

SessionLocal = sessionmaker(
    engine_sync,
)


async def init_db():
    try:
        logger.info("Checking if database exists")
        dsn = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/postgres"

        # Improved connection with timeout
        sys_conn: asyncpg.connection.Connection = await asyncpg.connect(
            dsn, timeout=5.0
        )

        try:
            db_exists = await sys_conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)",
                config.DB_NAME,
            )
            if not db_exists:
                try:
                    await sys_conn.execute(f'CREATE DATABASE "{config.DB_NAME}"')
                    logger.info(f"Database '{config.DB_NAME}' created successfully")
                except Exception as e:
                    if "already exists" not in str(e):
                        logger.error(f"Error creating database: {e}")
                        raise
            else:
                logger.info(f"Database '{config.DB_NAME}' already exists")

        finally:
            await sys_conn.close()

    except asyncpg.PostgresError as pg_err:
        logger.error(f"PostgreSQL-specific error: {pg_err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        raise
    try:
        async with engine.begin() as conn:
            logger.info("Creating database tables if they don't exist")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created or already exist")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
