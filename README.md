# EventFlow API

[English](#english) | [Русский](#русский)

---

## English

Asynchronous REST API for event management and ticket booking, built with FastAPI, PostgreSQL, and SQLAlchemy 2.0.

### Key Features

* **Authentication & Authorization** — JWT access tokens, bcrypt password hashing (via Passlib), and protected endpoints.
* **Event Management** — event creation, retrieval, owner-only deletion, capacity limits, and paginated listing.
* **Ticket Booking** — seat reservation, duplicate-booking prevention, user ticket listing, and cancellation.
* **Transactional Booking Flow** — capacity and duplicate checks are performed within the same database transaction as the reservation write.
* **Data Validation** — request and response validation using Pydantic v2.
* **Async Persistence** — SQLAlchemy 2.0 AsyncSession with PostgreSQL and asyncpg, eager loading (`joinedload`) to prevent N+1 queries.
* **Database Migrations** — schema versioning with Alembic (async engine).
* **Testing** — integration test suite covering auth and booking flows, using pytest, pytest-asyncio, and HTTPX against an in-memory SQLite database.

### Tech Stack

| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.12 |
| **Framework** | FastAPI |
| **Validation** | Pydantic v2 |
| **Database** | PostgreSQL 16 |
| **ORM** | SQLAlchemy 2.0 AsyncIO |
| **Driver** | asyncpg |
| **Authentication** | PyJWT, Passlib (bcrypt) |
| **Migrations** | Alembic |
| **Testing** | Pytest, pytest-asyncio, HTTPX |
| **Containerization** | Docker, Docker Compose |

### Architecture

The application follows a layered architecture that separates HTTP transport, business logic, and persistence concerns:

```text
app/
├── main.py             # FastAPI app instance and startup config
├── api/
│   ├── deps.py         # Shared dependencies (DB session, current user)
│   └── v1/
│       ├── router.py   # API v1 route aggregation
│       └── endpoints/  # Route handlers: auth, events, tickets
├── core/               # Configuration and security
├── db/                 # Database connection and sessions
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic request/response schemas
└── services/           # Business logic
alembic/                # Database migrations
tests/                  # API and integration tests
```

HTTP handlers delegate business operations to service classes, keeping business logic isolated and testable. FastAPI dependency injection is used for database sessions and authentication dependencies.

### Booking & Transactional Flow

Ticket booking is handled within a single database transaction:

1. Target event and existing user bookings are validated within the transaction.
2. Available capacity is checked against `total_seats`.
3. The reservation is created and committed in the same session transaction.

This keeps the capacity check and the reservation write in one atomic unit of work, and blocks duplicate bookings for the same user/event pair at the application level.

### API Overview

Base path: `/api/v1`

* **Auth**
  * `POST /auth/register` — Register a new user
  * `POST /auth/login` — Authenticate and obtain JWT access token
  * `GET /auth/me` — Current user profile
* **Events**
  * `POST /events` — Create event
  * `GET /events` — List events with pagination (`skip`, `limit`)
  * `GET /events/{event_id}` — Get event details
  * `DELETE /events/{event_id}` — Delete event (owner only)
* **Tickets**
  * `POST /tickets` — Book a ticket
  * `GET /tickets/my` — List current user tickets
  * `DELETE /tickets/{ticket_id}` — Cancel ticket booking
* **System**
  * `GET /health` — Health check endpoint (root level: `/health`)

### Quick Start

**Prerequisites:** Docker, Docker Compose

```bash
git clone https://github.com/v0net/eventflow-api.git
cd eventflow-api

docker compose up --build -d
docker compose exec web alembic upgrade head
```

Database URL and secret key for local development are pre-configured in `docker-compose.yml`. To use different values, edit the `environment` section of the `web` service directly.

* **API:** http://localhost:8000
* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc
* **OpenAPI Schema:** http://localhost:8000/api/v1/openapi.json

Health check:
```bash
curl http://localhost:8000/health
```

### Testing

The test suite uses pytest, pytest-asyncio, and HTTPX against an in-memory SQLite database. It covers a full end-to-end flow: user registration, login, event creation, ticket booking, and duplicate-booking rejection.

```bash
pytest -v

# or inside Docker:
docker compose exec web pytest -v
```

### License

MIT

---

## Русский

Асинхронный REST API для управления мероприятиями и бронирования билетов, построенный на FastAPI, PostgreSQL и SQLAlchemy 2.0.

### Ключевые возможности

* **Аутентификация и авторизация** — JWT access-токены, хеширование паролей bcrypt (через Passlib), защищённые эндпоинты.
* **Управление мероприятиями** — создание, получение, удаление доступно только владельцу, лимиты вместимости, пагинация.
* **Бронирование билетов** — резервирование мест, защита от дублей, список билетов пользователя, отмена бронирования.
* **Транзакционный флоу бронирования** — проверка вместимости и дублей выполняется в той же транзакции БД, что и запись бронирования.
* **Валидация данных** — валидация запросов и ответов через Pydantic v2.
* **Асинхронный доступ к БД** — SQLAlchemy 2.0 AsyncSession с PostgreSQL и asyncpg, eager loading (`joinedload`) для предотвращения N+1 запросов.
* **Миграции БД** — версионирование схемы через Alembic (асинхронный движок).
* **Тестирование** — интеграционные тесты, покрывающие сценарии аутентификации и бронирования, на pytest, pytest-asyncio и HTTPX с in-memory SQLite.

### Технологический стек

| Категория | Технология |
| :--- | :--- |
| **Язык** | Python 3.12 |
| **Фреймворк** | FastAPI |
| **Валидация** | Pydantic v2 |
| **База данных** | PostgreSQL 16 |
| **ORM** | SQLAlchemy 2.0 AsyncIO |
| **Драйвер** | asyncpg |
| **Аутентификация** | PyJWT, Passlib (bcrypt) |
| **Миграции** | Alembic |
| **Тестирование** | Pytest, pytest-asyncio, HTTPX |
| **Контейнеризация** | Docker, Docker Compose |

### Архитектура

Приложение построено по слоистой архитектуре, разделяющей HTTP-транспорт, бизнес-логику и работу с БД:

```text
app/
├── main.py             # Точка входа FastAPI и конфигурация запуска
├── api/
│   ├── deps.py         # Общие зависимости (сессия БД, текущий пользователь)
│   └── v1/
│       ├── router.py   # Агрегация маршрутов API v1
│       └── endpoints/  # Обработчики маршрутов: auth, events, tickets
├── core/               # Конфигурация и безопасность
├── db/                 # Подключение к БД и сессии
├── models/             # ORM-модели SQLAlchemy
├── schemas/            # Pydantic-схемы запросов/ответов
└── services/           # Бизнес-логика
alembic/                # Миграции БД
tests/                  # API и интеграционные тесты
```

HTTP-обработчики делегируют бизнес-операции сервисным классам, что делает логику изолированной и тестируемой. Для сессий БД и аутентификации используется dependency injection FastAPI.

### Бронирование и транзакционность

Бронирование билета выполняется в рамках одной транзакции БД:

1. Внутри транзакции проверяются мероприятие и существующие бронирования пользователя.
2. Доступная вместимость сопоставляется с `total_seats`.
3. Резервирование создаётся и фиксируется в рамках той же сессионной транзакции.

Это объединяет проверку вместимости и запись бронирования в единую атомарную операцию и исключает повторное бронирование для одной и той же пары пользователь/мероприятие на уровне приложения.

### Обзор API

Базовый путь: `/api/v1`

* **Аутентификация**
  * `POST /auth/register` — регистрация нового пользователя
  * `POST /auth/login` — вход и получение JWT access-токена
  * `GET /auth/me` — профиль текущего пользователя
* **Мероприятия**
  * `POST /events` — создание мероприятия
  * `GET /events` — список мероприятий с пагинацией (`skip`, `limit`)
  * `GET /events/{event_id}` — получение мероприятия по ID
  * `DELETE /events/{event_id}` — удаление мероприятия (только владелец)
* **Билеты**
  * `POST /tickets` — бронирование билета
  * `GET /tickets/my` — список билетов текущего пользователя
  * `DELETE /tickets/{ticket_id}` — отмена бронирования
* **Системные**
  * `GET /health` — проверка работоспособности (root-эндпоинт: `/health`)

### Быстрый старт

**Требования:** Docker, Docker Compose

```bash
git clone https://github.com/v0net/eventflow-api.git
cd eventflow-api

docker compose up --build -d
docker compose exec web alembic upgrade head
```

URL базы данных и секретный ключ для локальной разработки уже заданы в `docker-compose.yml`. Чтобы использовать другие значения, отредактируйте секцию `environment` сервиса `web` напрямую.

* **API:** http://localhost:8000
* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc
* **OpenAPI схема:** http://localhost:8000/api/v1/openapi.json

Проверка работоспособности:
```bash
curl http://localhost:8000/health
```

### Тестирование

Тестовый набор использует pytest, pytest-asyncio и HTTPX с in-memory SQLite. Он покрывает полный сквозной сценарий: регистрацию пользователя, вход, создание мероприятия, бронирование билета и отклонение повторного бронирования.

```bash
pytest -v

# или внутри Docker:
docker compose exec web pytest -v
```

### Лицензия

MIT