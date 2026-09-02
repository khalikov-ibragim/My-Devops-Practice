# API Parser

Учебный Python-скрипт: обращается к публичному API (JSONPlaceholder), забирает
список пользователей и выгружает нужные поля в CSV-файл.

## Стек

- Python 3, библиотеки `requests` и `csv` (стандартная)

## Что делает

1. Отправляет GET-запрос к `https://jsonplaceholder.typicode.com/users`
2. Преобразует ответ в JSON
3. Записывает в `python_trending.csv` колонки:
   `Username, Name, Email, Phone`

## Запуск

```bash
pip install requests
python src/Parser_API.py
```

На выходе появится `python_trending.csv` в текущей директории.

## Идеи для развития

- Параметризовать URL и имя выходного файла через аргументы (`argparse`)
- Обрабатывать ошибки сети/HTTP-статусы (`response.raise_for_status()`)
- Запускать по расписанию через cron
