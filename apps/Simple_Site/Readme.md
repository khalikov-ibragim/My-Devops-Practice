# ТОК — фронтенд интернет-магазина техники

Чистый HTML/CSS/JS, без сборщиков и фреймворков. Готов к докеризации и подключению своего бэкенда.

## Структура

```
tok-store/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── data.js     # моковые товары — удалить, когда данные придут с бэкенда
│   ├── api.js       # ЕДИНАЯ точка входа для сетевых запросов (сейчас — моки)
│   ├── cart.js       # состояние корзины (сейчас — localStorage)
│   └── app.js        # рендер интерфейса и обработчики событий
├── Dockerfile         # опционально: nginx, отдаёт статику
└── nginx.conf
```

## Запуск локально

Просто открыть `index.html` в браузере, либо поднять любой статический сервер:

```bash
python3 -m http.server 8080
# или
npx serve .
```

## Подключение бэкенда

Всё сетевое взаимодействие уже собрано в `js/api.js` — остальной код с ним не связан
напрямую. Чтобы подключить свой бэкенд:

1. В `js/api.js` поставь `CONFIG.USE_MOCK_API = false`.
2. Раскомментируй и допиши `fetch`-запросы в функциях `getProducts`, `login`,
   `register`, `logout`, `checkout` — там уже оставлены заготовки под нужные
   эндпоинты и формат данных.
3. Товары (`js/data.js`) можно удалить целиком, когда `GET /api/products`
   начнёт отдавать те же по форме объекты (`id`, `name`, `category`, `price`,
   `specs`, `rating`, `reviews`, `badge`, `oldPrice`).
4. Корзина сейчас живёт в `localStorage` (`js/cart.js`). Для MVP этого
   достаточно; если нужно хранить корзину на сервере — например, в Redis по
   `session_id` — замени реализацию внутри `cart.js`, интерфейс (`add`,
   `remove`, `setQty`, `getItems`, `getTotal`) можно оставить прежним, чтобы
   `app.js` не трогать.

Ожидаемые данные на пользователя, для ориентира по PostgreSQL-схеме:

- **users**: id, name, email, password_hash, created_at
- **products**: id, name, category, price, old_price, specs, rating, reviews, badge
- **orders** / **order_items**: id, user_id, items (product_id, qty, price), created_at
- Redis подойдёт под сессии (`session_id → user_id`) и/или под серверную корзину.

## Докер (опционально)

Если решишь, что фронтенд тоже должен быть отдельным сервисом в
`docker-compose.yml`, в комплекте есть `Dockerfile` и `nginx.conf`
(nginx отдаёт статику и, при необходимости, проксирует `/api` на бэкенд).

Пример блока для твоего `docker-compose.yml`:

```yaml
services:
  frontend:
    build: ./tok-store
    ports:
      - "8080:80"
    depends_on:
      - backend

  # backend, postgres (с volume под данные) и redis — твоя часть задания
```

Всё остальное (сам бэкенд, PostgreSQL, Redis, volume для данных БД) — как и
договаривались, за тобой.
