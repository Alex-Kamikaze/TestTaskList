import logging
import os
import signal
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from api.endpoints.tasks import router as tasks_router
from api.endpoints.statuses import router as status_router
from core.config import dev_settings, prod_settings
from db.session.db_session import engine
from db.entities.models import Base

load_dotenv()

debug = bool(os.environ.get("DEBUG"))
if debug:
    settings = dev_settings
else:
    settings = prod_settings

logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

server = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Setting up debug database...")

    if debug:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    logger.info("Finishing setup for debug database...")

    yield

    logger.info("Shutting down application...")
    engine.dispose()
    logger.info("Database connections closed.")


app = FastAPI(title="TestTask", version="1.0", lifespan=lifespan)


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database Error: {str(exc)}")

    return JSONResponse(status_code=500, content={"detail": "Internal Database Error"})


@app.get("/health")
async def healthcheck():
    return {"health": "ok"}


app.include_router(tasks_router, prefix="/tasks")
app.include_router(status_router, prefix="/status")


def signal_handler(sig, frame):
    logger.info("Received interrupt signal. Shutting down...")
    if server:
        server.should_exit = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    config = uvicorn.Config(
        "main:app", port=settings.PORT, host=settings.HOST, reload=debug
    )
    server = uvicorn.Server(config)

    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        logger.info("Server shutdown complete")
