import asyncio
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "email"

TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_user,
    MAIL_PASSWORD=settings.email_pass,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=(settings.app_env == "prod"),
    TEMPLATE_FOLDER=TEMPLATE_DIR
)

class EmailSender:
    def __init__(self):
        self.__fastmail = FastMail(email_conf)

    async def send_async(self, email: str, subject: str, template_file_name: str, template_data: dict):
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            template_body=template_data,
            subtype=MessageType.html
        )
        await self.__fastmail.send_message(message, template_name=template_file_name)

    def send(self, email: str, subject: str, template_file_name: str, template_data: dict):
        asyncio.run(self.send_async(email, subject, template_file_name, template_data))