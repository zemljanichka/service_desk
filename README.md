# ServiceDesk 

## В рамках задания было реализовано:

- Два FastAPI сервиса:
  - Сервис для взаимодействия с почтовым сервисом
  - Сервис для работы с заявками пользователей
- Отложенные задачи с использованием Dramatiq и APScheduler (Redis в качестве брокера):
  - Отправка писем
  - Чтение непрочитанных писем раз в 30 секунд с записью в СУБД
- Тесты с использованием pytest (pytest-asyncio)
- Работа с СУБД PostgreSQL с использованием ORM - SQLAlchemy
- Фронтенд (HTML/Jinja/JS/Bootstrap5) для тестирования и демонстрации функционала
- Авторизация с помощью JWT-токена
- Контейнеризация с использованием docker, docker-compose

## Запуск приложения

```shell
docker-compose up --build
```

Документация Swagger/OpenAPI доступна по адресу:

`http://localhost:8002/docs` - для сервиса обработки заявлений

`http://localhost:8004/docs` - для почтового сервиса

## Запуск тестов

Для запуска тестов необходимо поднять тестовый PostgreSQL:

```shell
docker-compose -f docker-compose.tests.yaml up --build test_postgresql
```

И запустить тесты с помощью pytest:

```shell
cd api_service
pytest .
```

## Запуск линтеров

```shell
black -l 120 .
isort .
mypy . --explicit-package-bases --ignore-missing --exclude venv
```

## Тестовый сервер

Доступен тестовый сервер с фронтендом по адресу:

`http://104.248.140.209:8002/docs` - для Swagger сервиса по обработке заявок

`http://104.248.140.209:8004/docs` - для Swagger почтового сервиса

`http://104.248.140.209:8002/frontend` - для фронтенда на сервере

## Использованный стэк

- Python 3.12
- FastAPI
- Dramatiq (broker - Redis)
- SQLAlchemy + PostgreSQL
- Docker, docker-compose
- Деплой в Digital Ocean (Ubuntu 22.04)
- HTML/CSS/JS
