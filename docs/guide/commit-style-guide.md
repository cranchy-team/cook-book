<div align="center">
  <img src="../public/logo.png" alt="logo.png" width="200" height="200" />
  <h1>Cook Book</h1>
  <p><b><i>Руководство по стилю коммитов (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧</i></b></p>
  <p align="center">
    <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"></a>
    <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://www.conventionalcommits.org/"><img src="https://img.shields.io/badge/Conventional_Commits-FE5196?style=for-the-badge&logo=conventionalcommits&logoColor=white" alt="Conventional Commits"></a>
  </p>
</div>

---

## 1. Общие сведения

### 1.1. Структура сообщения

`<type>(<scope>): <краткое описание>`

### 1.2. Правила оформления

1. Длина заголовка коммита не должна превышать 72 символов;
2. Текст коммита на русском языке;
3. Все буквы должны быть строчными;
4. Вместо буквы `ё` в тексте коммита используется буква `е`;

---

## 2. Типы коммитов (type)

| Тип      | Назначение                                                              |
| -------- | ----------------------------------------------------------------------- |
| feat     | Новая функциональность (новая фича, эндпоинт, компонент)                |
| fix      | Исправление бага                                                        |
| refactor | Переработка кода без изменения внешнего поведения                       |
| docs     | Изменения в документации                                                |
| chore    | Рутинные задачи: обновление зависимостей, настройка сборки              |
| style    | Форматирование, пробелы, точки с запятой - не влияет на логику          |
| ci       | Изменения в конфигурациях CI/CD (GitHub Actions, `.gitignore`, линтеры) |
| perf     | Изменения, направленные на повышение производительности                 |
| build    | Изменения в системе сборки или внешних зависимостях (Docker, npm, pip)  |
| test     | Добавление или обновление тестов (юнит-, интеграционных)                |

---

## 3. Области (scope)

Области соответствуют основным компонентам cook-book. При необходимости можно добавлять новые, но перечисленные ниже - стандартные.

| Область    | Описание                                                                     |
| ---------- | ---------------------------------------------------------------------------- |
| infra      | Инфраструктура: Docker, docker-compose, переменные окружения, настройка сети |
| auth       | Auth Service (Go): регистрация, авторизация, JWT, пользователи               |
| recipe     | Recipe Service (FastAPI): CRUD рецептов, избранное, поиск, загрузка фото     |
| fe         | Фронтенд (Vue 3 + Vuetify): компоненты, роутинг, i18n, состояние             |
| docs       | Документация (README, техническое задание, руководство по работе)            |
| db         | База данных: миграции Alembic, golang-migrate, схемы PostgreSQL              |
| config     | Конфигурационные файлы (.env, .toml)                                         |

---

## 4. Примеры корректных сообщений

- `feat(auth): добавлен эндпоинт смены пароля`
- `feat(recipe): добавлено управление избранным`
- `fix(recipe): обработка отсутствия фото рецепта`
- `fix(auth): исправлено время жизни refresh токена`
- `docs(work-guide): добавлено руководство по ветвлению`
- `refactor(recipe): использован cursor пагинация`
- `style(fe): форматирование компонентов vuetify`
- `perf(recipe): добавлен индекс на рецептах по user_id и created_at`
- `ci(github): добавлен воркфлоу линтинга для go-сервисов`
- `test(recipe): добавлены тесты для сервиса избранного`
- `chore(deps): обновление alembic до версии 1.12`
- `build(docker): добавлен healthcheck для auth-service`

---

<div align="center">
  <img src="../public/logo.png" alt="logo.png" width="100" height="100" />
  <br>
  <sub><b>Cook Book // Руководство по стилю коммитов</b></sub>
  <br>
  <sup><i>Made with love by <a href="https://github.com/cranchy-team" target="_blank">MindlessMuse666 x bukabtw</a></i></sup>
</div>
