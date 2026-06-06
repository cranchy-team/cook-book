<div align="center">
   <img src="docs/public/logo.png" alt="logo.png" width="200" height="200" />
   <h1>Cook Book 🍳</h1>
   <p><b><i>Веб-приложение для ведения личной книги рецептов ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚</i></b></p>
      <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" height="35"></a>
      <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" height="35"></a>
      <a href="https://go.dev/"><img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" height="35"></a>
      <a href="https://gin-gonic.com/"><img src="https://img.shields.io/badge/Gin-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Gin" height="35"></a>
      <a href="https://vuejs.org/"><img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue.js" height="35"></a>
      <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" height="35"></a>
      <br />
      <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" height="35"></a>
      <a href="https://nginx.org/"><img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx" height="35"></a>
      <a href="https://swagger.io/"><img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger" height="35"></a>
      <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" height="35"></a>
      <a href="https://plantuml.com/"><img src="https://img.shields.io/badge/plantuml-e75480?style=for-the-badge&logo=uml" alt="PlantUML" height="35"></a>
      <a href="LICENSE.md"><img src="https://img.shields.io/badge/MIT-yellow?style=for-the-badge&logo=readme&logoColor=white" alt="MIT" height="35"></a>
</div>

---

## Общее описание

**Cook Book** - это веб-приложение для ведения личной книги рецептов с аутентификацией, загрузкой фото и избранным. Здесь юзеры могут:

- зарегистрироваться и войти в аккаунт (JWT в httpOnly cookies);
- добавлять, редактировать и удалять свои рецепты;
- загружать квадратные фото для рецептов;
- добавлять рецепты в избранное;
- искать рецепты по названию и ингредиентам;
- фильтровать по сложности и дате публикации;
- использовать интерфейс на русском или английском языке.

Приложение спроектировано в рамках MSA с общей базой данных PostgreSQL.

### Диаграмма прецидентов

<details open>
   <summary><b>Нажмите, чтобы скрыть/показать диаграмму</b></summary>
   <img src="docs/diagrams/диаграмма_прецедентов.png" alt="Диаграмма прецедентов" />
   <br>
   <sub><i>Рис 1. Диаграмма прецедентов: возможности юзера в системе</sub></i>
</details>

---

## Стек технологий

### Бэкенд

- **Auth Service**: Go 1.25 + Gin + GORM + golang-migrate
- **Recipe Service**: Python 3.12 + FastAPI + SQLAlchemy + Alembic
- **База данных**: PostgreSQL 18.4
- **Документация API**: Swagger/OpenAPI 3.0

### Фронтенд

- Vue 3 + Vuetify 3
- Vue Router + Pinia + Vue I18n
- Axios для запросов к API
- CropperJS для подготовки фото

### Деплой

- Docker + Docker Compose
- Nginx для раздачи статики и проксирования запросов

---

## Архитектура

Проект состоит из трех основных сервисов и одной БД:

1. **Auth Service** - отвечает за регистрацию, авторизацию и управление юзерами;
2. **Recipe Service** - управляет рецептами, избранным, загрузкой фото и поиском;
3. **Frontend** - Vue SPA;
4. **PostgreSQL** - общая БД для обоих сервисов;
5. **Adminer** - веб-интерфейс для работы с БД.

### Диаграмма компонентов

<details open>
   <summary><b>Нажмите, чтобы скрыть/показать диаграмму</b></summary>
   <img src="docs/diagrams/диаграмма_компонентов.png" alt="Диаграмма компонентов" />
   <br>
   <sub><i>Рис 2. Диаграмма компонентов: компоненты системы и их взаимосвязи</sub></i>
</details>

---

## Быстрый старт

### Требования

- Docker
- docker-compose

### Шаги запуска

1. Склонируйте репо или скачайте проект:

   ```bash
   git clone https://github.com/cranchy-team/cook-book.git
   cd cook-book
   ```

2. Создайте в корне проекта файл `.env` и заполните его **вашими** данными по образцу [.env.example](.env.example "образец .env"):

   ```bash
   POSTGRES_USER=dev
   POSTGRES_PASSWORD=dev123
   POSTGRES_DB=cookbook
   DATABASE_URL=postgres://dev:dev123@postgres:5432/cookbook?sslmode=disable
   JWT_SECRET=i-am-so-super-pupper-drupper-im-the-front-girl-in-round-secret-key-here
   AUTH_SERVICE_PORT=8000
   RECIPE_SERVICE_PORT=8080
   ADMINER_PORT=8081
   ENVIRONMENT=development
   ```

3. Запустите проект с помощью docker-compose:

   ```bash
   docker-compose up --build
   ```

4. После успешного запуска откройте в браузере:

- Фронт: <http://localhost>
- Swagger сервиса `auth`: <http://localhost/swagger/index.html>
- Swagger сервиса `recipe`: <http://localhost/docs>
- Adminer: <http://localhost:8081>

5. Чтобы остановить проект:

   ```bash
   docker-compose down
   ```

6. Если нужно также удалить `volumes`:

   ```bash
   docker-compose down -v
   ```

---

## Основные URL

| Сервис / Ссылка                       | Описание                                 |
| ------------------------------------- | ---------------------------------------- |
| <http://localhost>                    | Фронтенд приложения                      |
| <http://localhost/swagger/index.html> | Документация Auth Service (Swagger UI)   |
| <http://localhost/docs>               | Документация Recipe Service (Swagger UI) |
| <http://localhost/redoc>              | Документация Recipe Service (Redoc)      |
| <http://localhost:8081>               | Adminer (веб-интерфейс для PostgreSQL)   |

---

## Разработка

### Структура проекта

```text
cook-book/
├── auth/                # Go-сервис аутентификации
├── recipe/              # FastAPI-сервис рецептов
├── frontend/            # Vue-фронтенд
├── docs/                # Документация и диаграммы
├── docker-compose.yml   # Конфиг docker-compose
└── .env                 # Переменные окружения
```

### Миграции

- **Auth Service**: Использует `golang-migrate`, миграции в `auth/migrations/`
- **Recipe Service**: Использует `Alembic`, миграции в `recipe/migrations/`

---

## Команда

| Роль                                                           | Имя                                                                   |
| -------------------------------------------------------------- | --------------------------------------------------------------------- |
| Product Owner, Team Lead, BA x SA, Go-разработчик, DevOps      | [Владислав Кедин](https://github.com/MindlessMuse666 "Сырная власть") |
| Python-разработчик (FastAPI), Фронтенд-разработчик (Vue 3), QA | [Кирилл Букарев](https://github.com/bukabtw "Звенящая пошлость")      |

---

## Лицензия

Проект распространяется под лицензией [MIT License](LICENSE.md).

---

<div align="center">
  <img src="docs/public/logo.png" alt="logo.png" width="100" height="100" />
  <br>
  <sub><b>Cook Book // Веб-приложение для управления рецептами</b></sub>
  <br>
  <sup><i>Made with love by <a href="https://github.com/cranchy-team" target="_blank">MindlessMuse666 x bukabtw</a></i></sup>
</div>
