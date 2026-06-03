<div align="center">
  <img src="../public/logo.png" alt="logo.png" width="200" height="200" />
  <h1>Cook Book</h1>
  <p><b><i>Полезные и интересные команды (*^_^*)</i></b></p>
  <p align="center">
    <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"></a>
    <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://www.conventionalcommits.org/"><img src="https://img.shields.io/badge/Conventional_Commits-FE5196?style=for-the-badge&logo=conventionalcommits&logoColor=white" alt="Conventional Commits"></a>
  </p>
</div>

---

## Сводная таблица полезных команд

| Команда | Домен | Описание | Примечание |
| ------- | ----- | -------- | ---------- |
| `gh auth login` | GitHub CLI | Аутентификация пользователя в GitHub CLI. | Позволяет войти через браузер или по токену веб-сессии (PAT). |
| `gh workflow list` | GitHub CLI | Просмотр списка всех существующих workflows (рабочих процессов) в текущем репозитории. | Отображает название, состояние (ID/Active) и файл конфигурации. |
| `gh workflow run ci.yml --ref <название-ветки>` | GitHub CLI | Ручной запуск рабочего процесса GitHub Actions (в нашем случае [ci.yml](../../.github/workflows/ci.yml)) для конкретной ветки. | Полезно для тестирования CI/CD пайплайнов без необходимости делать коммит. |
| `git checkout -b <название-ветки>` | Git | Создание новой локальной ветки с указанным именем и автоматический переход на нее. | Сочетает в себе команды `git branch` и `git checkout`. |
| `node -e "console.log(require('crypto').randomBytes(64).toString('base64'))"` | Runtime (Node.js) | Генерация случайной криптографической строки длиной 64 байта, закодированной в формат Base64. | Мы используем для создания секретных ключей. |

---

<div align="center">
  <img src="../public/logo.png" alt="logo.png" width="100" height="100" />
  <br>
  <sub><b>Cook Book // Полезные и интересные команды</b></sub>
  <br>
  <sup><i>Made with love by <a href="https://github.com/cranchy-team" target="_blank">MindlessMuse666 x bukabtw</a></i></sup>
</div>
