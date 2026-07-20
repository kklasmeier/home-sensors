import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.database import check_database_connection
from api.openapi_meta import API_DESCRIPTION, OPENAPI_TAGS
from api.routes import garage, hvac, logs, sensors, sump_pump

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Home Sensors API on %s:%s", settings.api_host, settings.api_port)
    if check_database_connection():
        logger.info("Database connection verified")
    else:
        logger.error("Database connection failed")
    yield
    logger.info("Shutting down Home Sensors API")


app = FastAPI(
    title="Home Sensors API",
    description=API_DESCRIPTION,
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=OPENAPI_TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router, prefix="/api/v1")
app.include_router(garage.router, prefix="/api/v1")
app.include_router(sump_pump.router, prefix="/api/v1")
app.include_router(hvac.router, prefix="/api/v1")
app.include_router(logs.router, prefix="/api/v1")


@app.get(
    "/",
    summary="API index",
    description="Returns API name, version, and links to interactive documentation.",
)
def root():
    return {
        "message": "Home Sensors API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
