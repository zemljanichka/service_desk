import base64
import email
import imaplib
import os
import pathlib
from email import header, utils

from bs4 import BeautifulSoup
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

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
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", "********"),  # type: ignore
    MAIL_FROM=os.environ.get("MAIL_ADDRESS", "email.ttest@ya.ru"),
    MAIL_PORT=os.environ.get("SMTP_MAIL_PORT", 587),  # type: ignore
    MAIL_SERVER=os.environ.get("SMTP_MAIL_SERVER", "smtp.yandex.ru"),
    MAIL_STARTTLS=os.environ.get("SMTP_MAIL_STARTTLS", True),  # type: ignore
    MAIL_SSL_TLS=os.environ.get("SMTP_MAIL_SSL_TLS", False),  # type: ignore
    TEMPLATE_FOLDER=pathlib.Path("./"),
)

read_conf = {
    "mail_address": os.environ.get("MAIL_ADDRESS", "email.ttest@ya.ru"),
    "mail_password": os.environ.get("MAIL_PASSWORD", "******"),
    "mail_server": os.environ.get("IMAP_MAIL_SERVER", "imap.yandex.ru"),
}

default_body = "Обращение принято в работу"


@app.post("/send_email")
async def send_email(email_address: str = Body(), subject: str = Body(), body: str = Body(default_body)):
    """Отправка email-сообщения по SMTP"""
    message = MessageSchema(
        subject=subject, recipients=[email_address], template_body={"body": body}, subtype=MessageType.html
    )
    fm = FastMail(send_conf)
    await fm.send_message(message, template_name="./email_template.html")
    return {"message": "email has been sent"}


@app.get("/read")
async def read_email():
    """Чтение всех непрочитанных сообщений"""
    imap = imaplib.IMAP4_SSL(read_conf["mail_server"])
    imap.login(read_conf["mail_address"], read_conf["mail_password"])
    imap.select("INBOX")
    mail_num = imap.uid("search", "UNSEEN", "ALL")[1][0]
    if not mail_num:
        return []
    mail_num = mail_num.split(b" ")
    response = []
    for mail in mail_num:
        # NOTE: Чтение письма по id
        res, msg = imap.uid("fetch", mail, "(RFC822)")
        msg = email.message_from_bytes(msg[0][1])
        # NOTE: Получение времени и адреса отправителя
        mail_response = {"ts_created": email.utils.parsedate_to_datetime(msg["Date"]), "email": msg["Return-path"]}
        # NOTE: Получение темы письма
        if msg["Subject"]:
            letter_subject = email.header.decode_header(msg["Subject"])[0][0]
        else:
            letter_subject = None
        if isinstance(letter_subject, bytes):
            letter_subject.decode()
        mail_response["subject"] = letter_subject
        # NOTE: Получение текста письма
        payload = msg.get_payload()
        body = []
        try:
            for data in payload:
                body.append(base64.b64decode(data.get_payload()).decode())
        except:
            if isinstance(payload, str):
                body = [payload]
        mail_body = ""
        for val in body:
            mail_body += BeautifulSoup(val, "lxml").text.replace("\n", " ").replace("\r", " ").strip(" ")
        mail_response["body"] = mail_body
        if not mail_response["subject"] and not mail_response["body"]:
            continue
        response.append(mail_response)
    return response
