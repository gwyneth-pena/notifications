import asyncio
from consumers.plugins.db import Base, engine
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse    
from sqlalchemy import text
from contextlib import asynccontextmanager
from producers.plugins.kafka_producer import KafkaProducer
from shared.exceptions import APIException
import httpx
import logging
import sys
import producers.routes as producer_routes
import consumers.routes as consumer_routes
from config import settings
from consumers.notif_consumer import consume_notification, stop_event

def init_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        Base.metadata.create_all(bind=engine)
        print("Connected to database")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(init_db)

    http_client = httpx.AsyncClient()
    app.state.http_client = http_client

    kafka_producer = KafkaProducer()
    app.state.kafka_producer = kafka_producer

    stop_event.clear()

    email_worker = asyncio.create_task(
        asyncio.to_thread(
            consume_notification, 
            group_id="email-notification-group", 
            topic=settings.kafka_topics['email']
        )
    )
    
    push_worker = asyncio.create_task(
        asyncio.to_thread(
            consume_notification, 
            group_id="push-notification-group", 
            topic=settings.kafka_topics['push']
        )
    )

    yield 
    stop_event.set()
    app.state.kafka_producer.flush(timeout=5)
    await asyncio.gather(email_worker, push_worker)
    await app.state.http_client.aclose()

description = """
#### Key Features:
- Send notifications to Kafka
- Consume notifications from Kafka
- Retry failed notifications
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


app.include_router(consumer_routes.router)
app.include_router(producer_routes.router)
