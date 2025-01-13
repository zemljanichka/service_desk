from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import MessageSchema, FastMail, MessageType, ConnectionConfig
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

send_conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "email.ttest@ya.ru"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", "********"),
    MAIL_FROM=os.environ.get("MAIL_ADDRESS", "email.ttest@ya.ru"),
    MAIL_PORT=os.environ.get("SMTP_MAIL_PORT", 587),
    MAIL_SERVER=os.environ.get("SMTP_MAIL_SERVER", "smtp.yandex.ru"),
    MAIL_STARTTLS=os.environ.get("SMTP_MAIL_STARTTLS", True),
    MAIL_SSL_TLS=os.environ.get("SMTP_MAIL_SSL_TLS", False),
)


@app.post("/send_email")
async def send_email(email_address: str = Body(), subject: str = Body(), body: str = Body()):
    message = MessageSchema(subject=subject, recipients=[email_address], body=body, subtype=MessageType.plain)
    fm = FastMail(send_conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}


@app.get("/read")
async def read_email():
    pass
