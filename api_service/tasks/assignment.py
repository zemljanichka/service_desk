import asyncio

import dramatiq
import requests
from services import AssignmentService
from schemas import AssignmentEmail


@dramatiq.actor()
def send_mail(email: str, subject: str, body: str | None = None):
    try:
        r = requests.post("http://email_service:8004/send_email",
                          json={'email_address': email, 'subject': subject, 'body': body})
        if not r.ok:
            raise Exception('Failed to send message: ', r.json())
    except Exception as e:
        print('Error while sending message')
        raise Exception from e


async def read_mail_async():
    try:
        response = requests.get("http://email_service:8004/read")
        if not response.ok:
            raise Exception('Failed to read messages')
        assignments_data: list[AssignmentEmail] = response.json()

        for assignment_data in assignments_data:
            await AssignmentService.create_assignment(assignment_data)
            send_mail.send(assignment_data["email"], assignment_data["subject"])
    except Exception as e:
        print('Error while reading message')
        raise Exception from e


@dramatiq.actor
def read_mail():
    asyncio.run(read_mail_async())
