# FastAPI App

Минимальное FastAPI-приложение — учебный пример развёртывания Python-API в контейнере.

## Стек

- Python, FastAPI, uvicorn
- Dockerfile (простой, без multi-stage)

## Что умеет

Единственный эндпоинт:

| Метод | Путь | Ответ |
|-------|------|-------|
| GET   | `/`  | JSON с данными пользователя |

## Запуск

```bash
# Локально
pip install -r requirements.txt
uvicorn main:data --host 0.0.0.0 --port 8000

# Докер
podman build -t fastapi-app .
podman run -p 8000:8000 fastapi-app
```

Swagger-документация доступна на http://localhost:8000/docs.

## Предложения по улучшению

1. **Закрепить версию Python** в Dockerfile: `FROM python` → лучше `FROM python:3.12-slim`.
2. Добавить `.dockerignore` (исключить `__pycache__`, `.venv`, `*.pyc`), чтобы не
   раздувать образ.
3. Перейти на `pip freeze > requirements.txt` и зафиксировать версии зависимостей.
4. В ответе эндпоинта — статичные данные; для учебного простого API это ок, но для
   прода подойдёт Pydantic-модель и БД.
