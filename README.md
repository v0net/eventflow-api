# EventFlow API

[English](#english) | [Русский](#русский)

---

## English

Asynchronous REST API service for event management, ticket booking, and seat availability tracking. Developed following clean architecture principles, transactional integrity, and N+1 query prevention.

### Tech Stack
* **Language & Framework:** Python 3.12, FastAPI (Pydantic v2)
* **Database & ORM:** PostgreSQL 16, SQLAlchemy 2.0 (AsyncSession)
* **Migrations:** Alembic
* **Security:** Passlib (bcrypt), PyJWT (Bearer token)
* **Containerization:** Docker, Docker Compose
* **Testing:** Pytest, pytest-asyncio, HTTPX

### Project Architecture
```text
eventflow-backend/
├── app/
│   ├── api/v1/endpoints/  # Routes: auth, events, tickets
│   ├── core/              # Config (pydantic-settings), JWT, and bcrypt
│   ├── db/                # DeclarativeBase, async engine, and get_db
│   ├── models/            # SQLAlchemy models (User, Event, Ticket)
│   ├── schemas/           # Pydantic v2 validation DTOs
│   └── services/          # Business logic service layer
├── alembic/               # Async schema migration scripts
├── tests/                 # Integration tests with SQLite in-memory
├── Dockerfile             # Optimized image with layer caching
└── docker-compose.yml     # Multi-container configuration
```

---

## Русский

Асинхронный REST API сервис для управления мероприятиями, бронирования билетов и учета свободных мест. Разработан с соблюдением принципов чистой архитектуры, транзакционной целостности и предотвращения проблемы N+1 запросов.

### Технологический стек
* **Язык & Фреймворк:** Python 3.12, FastAPI (Pydantic v2)
* **База данных & ORM:** PostgreSQL 16, SQLAlchemy 2.0 (AsyncSession)
* **Миграции:** Alembic
* **Безопасность:** Passlib (bcrypt), PyJWT (Bearer token)
* **Контейнеризация:** Docker, Docker Compose
* **Тестирование:** Pytest, pytest-asyncio, HTTPX

### Архитектура проекта
```text
eventflow-backend/
├── app/
│   ├── api/v1/endpoints/  # Маршруты: auth, events, tickets
│   ├── core/              # Настройки (pydantic-settings), JWT и bcrypt
│   ├── db/                # DeclarativeBase, асинхронный движок и get_db
│   ├── models/            # SQLAlchemy-модели (User, Event, Ticket)
│   ├── schemas/           # Валидационные DTO на Pydantic v2
│   └── services/          # Сервисный слой бизнес-логики
├── alembic/               # Скрипты асинхронных миграций схемы
├── tests/                 # Интеграционные тесты с SQLite in-memory
├── Dockerfile             # Оптимизированный образ с кэшированием слоев
└── docker-compose.yml     # Мультиконтейнерная конфигурация
```