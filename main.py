from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from contextlib import asynccontextmanager
from shared.exceptions import APIException
import httpx
import logging
import sys
import producers.routes as producer_routes
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield

description = """
#### Key Features:
"""

app = FastAPI(
    title="Kafka Notifications",
    description=description,
    version="1.0.0",
    lifespan=lifespan
)


logger = logging.getLogger("app") 
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

handler.setFormatter(formatter)
logger.addHandler(handler)

@app.exception_handler(Exception)
@app.exception_handler(APIException)
async def exception_handler(request: Request, exc: APIException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    location = ["server"]
    type = "server_error"
    msg = "An unexpected error occurred. Please try again later."

    if isinstance(exc, APIException) :
        status_code = exc.status_code
        location = [exc.location, exc.field]
        type = exc.type_
        msg = exc.msg
    else:
        logger.error(
            f"INTERNAL ERROR - "
            f"Env: {settings.app_env} - "
            f"Method: {request.method} - "
            f"URL: {request.url} - "
            f"Error: {str(exc)}"
        )
            
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": [{
                "loc": location,
                "msg": msg,
                "type": type
            }]
        }
    )

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}


app.include_router(producer_routes.router)
