# PyLinkShort

PyLinkShort – сервис сокращения ссылок, позволяющий пользователям создавать, редактировать, удалять и получать аналитику по своим коротким URL. Проект реализован на FastAPI для backend, а также Streamlit для frontend. В качестве бд для сервиса используется PostgreSQL и Redis для кэширования. Сервис поддерживает регистрацию пользователей, создание кастомных alias-ссылок (с возможностью ограничения времени жизни ссылок) и дополнительные функции, например, удаление неиспользуемых ссылок и историю истекших ссылок.

**Пользовательский интерфейс для работы с сервисом представлен на этой странице:** https://pylinkshort-webpage.onrender.com

## Функциональные возможности сервиса

### Обязательные функции ДЗ:
- **Создание, удаление, изменение и получение информации по короткой ссылке:**
  - `POST /api/links` – создание новой ссылки с возможностью указания кастомного alias и времени жизни.
  - `GET /{short_code}` – публичный редирект, который ищет оригинальный URL по short_code и перенаправляет пользователя.
  - `PUT /api/links/{short_code}` – обновление оригинального URL и срока жизни.
  - `DELETE /api/links/{short_code}` – удаление ссылки.
- **Статистика по ссылке:**
  - `GET /api/links/{short_code}/stats` – возвращает оригинальный URL, дату создания, количество переходов и дату последнего использования.
- **Поиск ссылки по оригинальному URL:**
  - `GET /api/links/search?original_url={url}` – поиск записи по исходному URL.
- **Регистрация и управление аккаунтом:**
  - `POST /api/auth/register` – регистрация нового пользователя.
  - `POST /api/auth/login` – вход в систему (с установкой cookie-сессии).
  - `GET /api/auth/profile` – получение профиля текущего пользователя.
  - `DELETE /api/auth/user` – удаление аккаунта (с каскадным удалением всех связанных ссылок).

### Дополнительные функции:
- **Кэширование популярных ссылок:**  
  Redis используется для кэширования данных перенаправления, что ускоряет обработку запросов.
- **Автоматическое удаление неиспользуемых ссылок:**  
  (Функциональность может быть дополнительно реализована в виде фоновой задачи.)
- **Отображение аналитики:**  
  Frontend-часть (на Streamlit) позволяет просматривать статистику переходов по ссылкам (общее количество переходов, построение графиков).

## Стэк сервиса

- **Backend:** FastAPI, Uvicorn, SQLAlchemy, psycopg2, python-dotenv, passlib, Redis, Pydantic.
- **Frontend:** Streamlit, Requests, Pandas.
- **База данных:** PostgreSQL (Render Managed PostgreSQL в продакшене).
- **Кэширование:** Redis.
- **Контейнеризация:** Docker, Docker Compose.

## Структура проекта

```
PyLinkShort/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env              # Для локального тестирования
│   └── app/
│       ├── init.py
│       ├── main.py
│       ├── api/
│       │   ├── init.py
│       │   ├── auth.py
│       │   └── links.py
│       ├── core/
│       │   ├── init.py
│       │   ├── cache.py
│       │   ├── config.py
│       │   ├── database.py
│       │   └── security.py
│       ├── models/
│       │   ├── init.py
│       │   ├── user.py
│       │   └── link.py
│       ├── schemas/
│       │   ├── init.py
│       │   ├── user.py
│       │   └── link.py
│       └── services/
│           ├── init.py
│           ├── analytics.py
│           └── shortener.py
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── secrets.toml      # Для локального тестирования
│   └── app.py
├── docker-compose.yml    # Для локального тестирования
└── README.md
```

## Локальное тестирование

1. **Настройка переменных окружения для локального запуска:**  
   В файле `backend/.env` укажите следующие значения по шаблону:
   ```env
   DATABASE_URL=postgresql://urlshort:urlshortpass@localhost:5432/urlshort_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=YOUR_SECRET_KEY
   SESSION_TTL=86400
   INACTIVITY_DAYS=90
   ```
   
Важно, чтобы PostgreSQL и Redis были запущены на локальной машине.

2.	**Отдельный запуск backend:**
Перейдите в папку backend и выполните:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступно по ссылке http://localhost:8000 в случае локального тестирования

3.	**Отдельный запуск frontend:**
Перейдите в папку frontend и выполните:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

Frontend-приложение будет доступно по ссылке http://localhost:8501 в случае локального тестирования.

4.	**Тестирование API:**
 
Используйте Postman или Postman‑коллекцию (см. раздел ниже) согласно документации API Swagger `API_URL/docs`.

5. **Docker Compose**

Для сборки сервиса воедино был написан Docker Compose файл для локального тестирования.

Шаблон docker-compose.yml:

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: urlshort_db
    environment:
      POSTGRES_USER: urlshort
      POSTGRES_PASSWORD: urlshortpass
      POSTGRES_DB: urlshort_db
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - internal

  redis:
    image: redis:7-alpine
    container_name: urlshort_redis
    ports:
      - "6379:6379"
    networks:
      - internal

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: urlshort_backend
    env_file:
      - ./backend/.env
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    networks:
      - internal

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: urlshort_frontend
    ports:
      - "8501:8501"
    depends_on:
      - api
    networks:
      - internal

networks:
  internal:
    driver: bridge

volumes:
  db_data:
```

Запустить все сервисы можно командой:

```bash
docker-compose up --build
```

## Тестирование API
Примеры запросов к API через Postman (где API_URL - base url сервиса API):

### 1. Register User
 - **Endpoint**: `{{API_URL}}/api/auth/register`
 - **Method**: `POST`
 - **Headers**:
 - **Content-Type**: `application/json`
 - **Body**:

```json
{
  "username": "testuser",
  "password": "testpass",
  "email": "testuser@example.com"
}
```

> **Expected Response:** `HTTP 201 Created, JSON с данными пользователя (например, id, username, email, created_at).`

### 2. Login User
 - **Endpoint**: `{{API_URL}}/api/auth/login`
 - **Method:** `POST`
 - **Headers:**
 - **Content-Type:** application/json
 - **Body:**
```json
{
  "username": "testuser",
  "password": "testpass"
}
```

> **Expected Response:** `HTTP 200 OK, JSON с сообщением об успешном входе и данными пользователя.`
> `Cookie с именем session_id сохраняется для дальнейших запросов.`

### 3. Get Profile
 - **Endpoint:** `{{API_URL}}/api/auth/profile`
 - **Method:** `GET`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)

> **Expected Response:** `HTTP 200 OK, JSON с данными профиля пользователя.`

### 4. Create Link
 - **Endpoint:** `{{API_URL}}/api/links`
 - **Method:** `POST`
 - **Headers:**
 - **Content-Type:** `application/json`
 - **Cookie:** `session_id={{session_id}}`
 - **Body:**

```json
{
  "original_url": "https://example.com/very-long-url",
  "custom_alias": "testalias",
  "expires_in_days": 30
}
```

> **Expected Response:** `HTTP 201 Created, JSON с данными ссылки (включая поле short_code)`.

### 5. List Links
 - **Endpoint:** `{{API_URL}}/api/links`
 - **Method:** `GET`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)

> **Expected Response:** `HTTP 200 OK, JSON-массив объектов ссылок, созданных пользователем.`

### 6. Get Link by short_code
 - **Endpoint:** `{{API_URL}}/api/links/{{short_code}}`
 - **Method:** `GET`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)

> **Expected Response:** `HTTP 200 OK, JSON с данными ссылки для указанного short_code.`

### 7. Update Link
 - **Endpoint:** `{{API_URL}}/api/links/{{short_code}}`
 - **Method:** `PUT`
 - **Headers:**
 - **Content-Type:** `application/json`
 - **Cookie:** `session_id={{session_id}}`
 - **Body:**

```json
{
  "original_url": "https://example.com/updated-url",
  "expires_in_days": 60
}
```

> **Expected Response:** `HTTP 200 OK, JSON с обновлёнными данными ссылки.`

### 8. Get Link Stats
 - **Endpoint:** `{{API_URL}}/api/links/{{short_code}}/stats`
 - **Method:** `GET`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)
 - **Expected Response:** `HTTP 200 OK, JSON со статистикой (поля: original_url, created_at, access_count, last_accessed).`

### 9. Search Link by Original URL
 - **Endpoint:** `{{API_URL}}/api/links/search?original_url=https://example.com/very-long-url`
 - **Method:** `GET`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)

> **Expected Response:** `HTTP 200 OK, JSON с полями short_code и original_url.`

### 10. Public Redirect
 - **Endpoint:** `{{API_URL}}/{{short_code}}`
 - **Method:** GET
 - **Headers:** (нет)
 - **Body:** (нет)
 -

> **Expected Response:** `HTTP 302 (или 307) Redirect. Заголовок Location с оригинальным URL.`
> Note: Для тестирования нужно отключить автоматическое следование (automatic redirect follow) редиректам в Postman.

### 11. Delete Link
 - **Endpoint:** `{{API_URL}}/api/links/{{short_code}}`
 - **Method:** `DELETE`
 - **Headers:**
 - **Cookie:** `session_id={{session_id}}`
 - **Body:** (нет)

>**Expected Response:** `HTTP 204 No Content.`
> Note: После удаления повторный запрос к этому short_code должен вернуть 404.

### 12. Delete User (Account)
- **Endpoint:** `{{API_URL}}/api/auth/user`
- **Method:** `DELETE`
- **Headers:**
- **Cookie:** `session_id={{session_id}}`
- **Body:** (нет)

> **Expected Response:** `HTTP 200 OK, JSON с сообщением:`

```json
{
  "message": "Пользователь удалён"
}
```

> После удаления аккаунта дальнейшие запросы, требующие аутентификации, должны возвращать 401 Unauthorized.

## HW4 Тестирование API

Что покрывает папка `tests`:
 -  Регистрацию, логин, ошибки
 -  Проверку сессии
 -  CRUD для ссылок
 -  Отдельно hash_password, verify_password, short_code, analytics
 -  Валидацию ошибок

Для того чтобы протестировать API с помощью Docker-системы необходимо:

1. Склонировать репозиторий
```bash
git clone git@github.com:DAChernikov/PyLinkShort.git
```

2. Перейти в корень репозитория:
```bash
cd PyLinkShort
```

3. Выполнить следующую команду:

```bash
docker-compose -f docker-compose.test.yml up --build
```

В результате запустится Docker-приложение с тестированием API. По окончанию тестирования, в консоль будет выведен результат. Пример результата тестирования приведен в файле `coverage.html` в корне репозитория.

## Deploy на Render

Проект был задеплойен в интернет с помощью платформы [Render](https://dashboard.render.com/). 
На основе кода этого репозитория, в этой платформе было развернуто 4 компонента сервиса:

1. FastAPI сервис (backend): API_URL: https://pylinkshort.onrender.com
2. StreamLit сервис (frontend, пользовательский интерфейс): [PyLinkShort_webpage](https://pylinkshort-webpage.onrender.com)
3. PostgreSQL DB: `postgresql://@dpg-cvjarqemcj7s73ean8u0-a.oregon-postgres.render.com/db_zfxs`
4. Redis (key-value store): `redis://red-cvjb0s8gjchc739ams20:6379`

## Автор проекта

Автор этого проекта - Черников Данила (https://t.me/dachernikov), студент НИУ ВШЭ по направлению обучения "Искусственный Интеллект"
