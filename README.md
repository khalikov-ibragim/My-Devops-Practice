# My-Devops-Practice

Монорепозиторий с моими учебными DevOps-проектами: приложения, упакованные в
контейнеры через Podman/Docker Compose, инфраструктурные заготовки и скрипты
для администрирования.

Каждый каталог — самостоятельный проект. Структура:

```
My-Devops-Practice/
├── apps/        учебные приложения (контейнеризация через podman-compose)
├── infra/       инфраструктура: Docker, Compose, Ansible (пополняется)
└── tools/       вспомогательные bash-скрипты
```

## Приложения (apps/)

| Проект              | Стек                                             | Что это                          |
|---------------------|--------------------------------------------------|----------------------------------|
| `chat-messenger`    | Node.js, Express, Socket.IO, Postgres, Redis     | чат в реальном времени           |
| `file-gallery`      | Node.js, Express, Postgres, MinIO (S3)           | галерея загрузки изображений     |
| `Simple_Site`       | FastAPI (Python), Postgres, nginx, pgAdmin       | интернет-магазин электроники     |
| `fastapi-app`       | FastAPI, uvicorn                                 | минимальный API-пример           |
| `api-parser`        | Python (requests + csv)                          | парсер API и выгрузка в CSV      |

## Инфраструктура (infra/)

- `docker/` — готовые Dockerfile-примеры (пополняется)
- `docker-compose/` — примеры compose-файлов (пополняется)
- `ansible/` — плейбуки (пополняется)

## Скрипты (tools/)

- `backup.sh` — простой скрипт резервного копирования
- `Nginx_Logs.sh` — проверка/анализ логов nginx

## Как запускать

Каждое приложение поднимается через `podman-compose` (или `docker-compose`) из
своей папки, например:

```bash
cd apps/chat-messenger
podman-compose up -d
```

> Перед запуском скопируй `.env.example` → `.env` и заполни значения, если такой
> файл присутствует в проекте.

## Почему Podman

Поднимаю учебные стенды через rootless Podman + `podman-compose` — это удобно на
RedOS/RedHat-подобных системах без демона Docker. Большинство проектов совместимо
с `docker-compose` практически без изменений (см. заметки в README каждого приложения).

## Дорожная карта

- [ ] CI/CD (GitHub Actions): сборка образов по пушу, деплой
- [ ] Наполнить `infra/ansible` первыми плейбуками
- [ ] Мониторинг (Prometheus + Grafana)
- [ ] Добавить `.env.example` во все приложения с секретами
