from datetime import datetime

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from database import AssignmentModel


def get_token(username: str, password: str, client: TestClient) -> str:
    r = client.post('/operator/login', json={'username': username, 'password': password})
    assert r.status_code == 200
    token = r.json().get('token')
    assert token is not None
    return token



@pytest.mark.asyncio()
async def test_login(client, test_operator):
    assert get_token('test', 'test', client)


@pytest.mark.asyncio()
async def test_get_me_by_token(client, test_operator):
    token = get_token('test', 'test', client)

    r = client.get("/operator/me", headers={'token': token})
    assert r.status_code == 200
    assert r.json()['username'] == 'test'


@pytest.mark.asyncio()
async def test_frontend_rendering(client, test_operator):
    r = client.get('/frontend/')
    assert r.headers.get('Content-Type') == 'text/html; charset=utf-8'
    assert r.status_code == 200, 'homepage is not working'


@pytest_asyncio.fixture()
async def test_assignment():
    yield await AssignmentModel.insert(
        email='test@mail.ru',
        subject='test subject',
        ts_created=datetime.now(),
        body='hello this is test',
    )
    await AssignmentModel.delete(AssignmentModel.email == 'test@mail.ru')


def check_assignment_status(assignment_id, client, token, status):
    r = client.get(f'/assignments/{assignment_id}', headers={"token": token})
    assert r.status_code == 200
    assert r.json().get('status') == status


@pytest.mark.asyncio()
async def test_assignment_full_cycle(client, test_operator, test_assignment):
    token = get_token('test', 'test', client)

    # 1. Получаем список всех заявок, статус изначально pending
    r = client.get('/assignments/', headers={"token": token})
    assert r.status_code == 200
    assert len(r.json()) == 1, 'failed to show list of all assignments'
    check_assignment_status(test_assignment.id, client, token, 'pending')

    # 2. Забираем в работу, статус processing
    r = client.post(f'/assignments/take?assignment_id={test_assignment.id}', headers={"token": token})
    assert r.status_code == 200
    check_assignment_status(test_assignment.id, client, token, 'processing')

    # 3. Оператор закрывает обращение, статус closed
    r = client.post(f'/assignments/close_assignment?assignment_id={test_assignment.id}', headers={"token": token})
    assert r.status_code == 200
    check_assignment_status(test_assignment.id, client, token, 'closed')
