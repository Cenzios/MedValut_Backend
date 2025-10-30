from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.core.database import get_engine, get_sessionmaker

# Middleware
from app.middleware.http_logger import HTTPLoggerMiddleware
from app.middleware.version_middleware import VersionMiddleware

# Exception Handlers
from app.utils.exception_handler import (
    all_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

# Scripts
from app.scripts.create_table_script import create_table_script

# Seed
from app.seed.seed import run_seeds

# Routes
from app.modules.master_data import controllers as master_data_controller
# from app.modules.user import controllers as user_controller
from app.modules.auth import controllers as auth_controller


# ----------------------- FastAPI App Setup -----------------------
app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION)

app = FastAPI(default_response_class=ORJSONResponse)


# ----------------------- Middleware -----------------------
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(VersionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------- Exception Handlers -----------------------
app.add_exception_handler(Exception, all_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# ----------------------- Routes -----------------------
@app.get("/")
async def health_check():
    return {
        "success": True,
        "message": "Service is healthy.",
        "environment": settings.ENVIRONMENT,
        "app": settings.APP_NAME,
    }


@app.get("/api/health/check")
async def health_check():
    return {
        "success": True,
        "message": "Service is healthy.",
        "environment": settings.ENVIRONMENT,
        "app": settings.APP_NAME,
    }


app.include_router(master_data_controller.router)
app.include_router(auth_controller.router)
# app.include_router(user_controller.router)


# ----------------------- Startup Event -----------------------
@app.on_event("startup")
async def startup_event():
    engine = get_engine()
    SessionLocal = get_sessionmaker()

    # Test DB connection
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)
        return  # Stop startup if DB is unreachable

    # Create tables if not exist
    try:
        await create_table_script(engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print("❌ Failed to create database tables:", e)
        return

    # Run seed data
    try:
        async with SessionLocal() as session:
            await run_seeds(session)
        print("✅ Seed data successfully applied!")
    except Exception as seed_error:
        print("⚠️ Seed data failed:", seed_error)
