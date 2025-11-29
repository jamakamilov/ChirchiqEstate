# Telegram Real Estate Bot (Zillow-like)

Бот для работы с объявлениями недвижимости: создание, модерация, публикация в канале, ручные оплаты, комиссии, рекомендации.

## Технологии
- Python 3.11
- aiogram 3.x
- SQLAlchemy (async)
- PostgreSQL (локально можно использовать SQLite)
- Docker + docker-compose

## Структура
Проект содержит:
- `main.py` — точка входа
- `database.py` — инициализация БД
- `models/` — SQLAlchemy модели
- `handlers/` — обработчики команд и FSM для создания объявлений
- `admin/` — админские обработчики
- `services/` — карты, рекомендации, платежи (ручные)
- `locales/` — переводы (uz, ru, en)
- `Dockerfile`, `docker-compose.yml`

## Установка (локально)
1. Склонируйте репозиторий.
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt