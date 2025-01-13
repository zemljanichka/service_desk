from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import MessageSchema, FastMail, MessageType, ConnectionConfig
import os
import imaplib
import email
from email import utils, header
from bs4 import BeautifulSoup
import base64

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


read_conf = {
    "mail_address": os.environ.get("MAIL_ADDRESS", "email.ttest@ya.ru"),
    "mail_password": os.environ.get("MAIL_PASSWORD", "******"),
    "mail_server": os.environ.get("IMAP_MAIL_SERVER", "imap.yandex.ru"),
}


@app.post("/send_email")
async def send_email(email_address: str = Body(), subject: str = Body(), body: str = Body()):
    message = MessageSchema(subject=subject, recipients=[email_address], body=body, subtype=MessageType.plain)
    fm = FastMail(send_conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}


@app.get("/read")
async def read_email():
    imap = imaplib.IMAP4_SSL(read_conf["mail_server"])
    imap.login(read_conf["mail_address"], read_conf["mail_password"])
    imap.select("INBOX")
    mail_num = imap.uid('search', "UNSEEN", "ALL")[1][0].split(b' ')
    response = []
    for mail in mail_num:
        res, msg = imap.uid('fetch', mail, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        mail_response = {"ts_created": email.utils.parsedate_to_datetime(msg["Date"]), "email": msg["Return-path"]}
        if msg["Subject"]:
            letter_subject = email.header.decode_header(msg["Subject"])[0][0]
        else:
            letter_subject = None
        if isinstance(letter_subject, bytes):
            letter_subject.decode()
        mail_response["subject"] = letter_subject
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
            mail_body += BeautifulSoup(val, "lxml").text.replace('\n', " ").replace('\r', " ").strip(" ")
        mail_response["body"] = mail_body
        if not mail_response["subject"] and not mail_response["body"]:
            continue
        response.append(mail_response)
    return response
