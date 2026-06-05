# Cook Book: Фронтенд - Комментарии по разработке

## Обзор

Этот документ содержит требования и рекомендации по доработке фронтенд-части приложения Cook Book. Фронтенд построен на Vue 3 + Vuetify 3 и взаимодействует с двумя микросервисами: Auth Service (Go) и Recipe Service (Python/FastAPI).

---

## Общие требования

### Технический стек

- Vue 3 (Composition API)
- Vuetify 3
- Vue Router
- Pinia
- Vue I18n
- Axios
- CropperJS
- Nginx (для деплоя)

### Архитектурные принципы

- Соблюдать существующую структуру проекта
- Использовать компонентный подход
- Корректно обрабатывать ошибки API
- Обеспечить адаптивность
- Поддерживать интернационализацию

---

## API интеграция

### Auth Service (Go)

Базовый URL: `/api/v1/auth`

| Метод | Эндпоинт | Описание | Аутентификация |
|-------|----------|----------|----------------|
| POST | `/register` | Регистрация | Нет |
| POST | `/login` | Вход (устанавливает cookies) | Нет |
| POST | `/logout` | Выход (очищает cookies) | Да |
| GET | `/profile` | Получение профиля | Да |
| POST | `/change-password` | Смена пароля | Да |

### Recipe Service (Python/FastAPI)

Базовый URL: `/api/v1`

| Метод | Эндпоинт | Описание | Аутентификация |
|-------|----------|----------|----------------|
| POST | `/recipes/` | Создать рецепт | Да |
| GET | `/recipes/` | Получить список рецептов | Да |
| GET | `/recipes/{recipe_id}` | Получить рецепт по ID | Да |
| PUT | `/recipes/{recipe_id}` | Обновить рецепт | Да |
| DELETE | `/recipes/{recipe_id}` | Удалить рецепт | Да |
| POST | `/recipes/{recipe_id}/upload-image` | Загрузить фото рецепта | Да |
| POST | `/favorites/{recipe_id}` | Добавить в избранное | Да |
| DELETE | `/favorites/{recipe_id}` | Удалить из избранного | Да |
| GET | `/favorites/` | Получить список избранных | Да |
| GET | `/favorites/{recipe_id}/status` | Проверить статус избранного | Да |

### Важные моменты API

- Все запросы к защищенным эндпоинтам должны отправлять cookies (`withCredentials: true`)
- Пагинация реализована через курсор (заголовок `X-Next-Cursor`)
- Изображения доступны по пути `/uploads/{filename}`

---

## Задачи по доработке

### 1. Настройка запуска с моковыми данными (dev-среда)

**Требования:**

- Настроить механизм работы с существующими моковыми данными для dev-среды
- Моки находятся в [docs/test/test-recipe.json](test/test-recipe.json)
- Моки должны позволять протестировать пагинацию, поиск, фильтрацию
- Переключение между реальным API и моками должно быть удобным
- Моковые данные должны быть презентабельными для демонстраций

**Важно:**
Необходимо исправить формат моков под API:

- `difficulty` должен быть `"easy"`, `"medium"`, `"hard"` (не "Легкий", "Средний")
- `cooking_time` вместо `cookingTime`
- Для тестирования можно добавить `image_path` (например, `"омлет_с_сыром_и_помидорами.png"`)

**Рекомендации:**

1. Скопировать моки в `frontend/src/api/mocks/recipes.json`
2. Использовать переменную окружения `VITE_USE_MOCK_DATA=true/false`
3. Создать отдельный модуль с моками в `src/api/mocks/`:
   - `src/api/mocks/index.js` - точка входа
   - `src/api/mocks/recipes.js` - логика работы с рецептами
   - `src/api/mocks/auth.js` - логика аутентификации
4. Модифицировать `src/api/client.js` для переключения между реальным API и моками
5. В dev-среде при ошибках API показывать полезную информацию для отладки

**Пример структуры моков (исправленный):**

```json
[
    {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Омлет с сыром и помидорами",
        "ingredients": "3 яйца\n50 мл молока\n50 г твёрдого сыра (чеддер или пармезан)\n1 средний помидор\nСоль, перец по вкусу\n1 ст. л. сливочного масла",
        "steps": "1. Яйца взбить с молоком, солью и перцем.\n2. Помидор нарезать тонкими кружочками, сыр натереть.\n3. На разогретую сковороду с маслом вылить яичную смесь.\n4. Сверху выложить помидоры и посыпать сыром.\n5. Накрыть крышкой и жарить на среднем огне 5–7 минут до готовности.\n6. Сложить омлет пополам, подавать горячим.",
        "cooking_time": 15,
        "difficulty": "easy",
        "image_path": "омлет_с_сыром_и_помидорами.png",
        "created_at": "2025-04-01T10:00:00+03:00",
        "updated_at": "2025-04-01T10:00:00+03:00"
    }
]
```

---

### 2. Логаут с перебросом на экран логина

**Текущая проблема:**

- При логауте не происходит редирект на страницу входа

**Требования:**

- После успешного логаута пользователь должен быть перенаправлен на `/login`
- Очистить все пользовательские данные из Pinia store
- Очистить локальное хранилище (кроме настроек языка)

---

### 3. Отступы и анимации

**Требования:**

- Установить единые отступы между компонентами (использовать spacing систему Vuetify)
- Добавить плавные анимации переходов между страницами
- Анимировать появление/исчезновение карточек рецептов
- Обеспечить консистентность отступов на всех экранах

**Рекомендации:**

- Использовать классы `ma-`, `pa-`, `mx-`, `px-` и т.д.
- Добавить `<transition>` компонент вокруг `<router-view>`
- Использовать готовые анимации Vuetify или создать свои

---

### 4. Основной цвет

**Требования:**

- Оставить текущий коралловый цвет как primary
- Не менять цветовую схему без согласования
- Использовать цвета через Vuetify theme

---

### 5. Header (sticky)

**Требования:**

- Header должен быть sticky (при прокрутке остается сверху)
- Слева: логотип/название "Cook Book"
- Справа: кнопка выбора языка, навигационные кнопки (Рецепты, Избранное, Вход/Регистрация).

**Важно:** сам header должен быть прозрачным, но кнопки на нём - всегда видимыми. при наведении на header его цвет становится полупрозрачным.

---

### 6. Интернационализация (i18n) - добавить языки

**Требования:**

- Добавить поддержку казахского (`kk`) и японского (`ja`) языков
- По умолчанию - русский (`ru`)
- Перевести все статические тексты, кнопки, плейсхолдеры, сообщения об ошибках
- Контент рецептов (названия, ингредиенты, шаги) **не переводить**
- Сохранять выбранный язык в `localStorage`

**Рекомендации:**

- Добавить переводы в `src/i18n.js`
- Обновить переключатель языков в header
- Проверить, что все тексты в компонентах используют `$t()`

---

### 7. Загрузка фотографий рецептов

**Требования:**

- Поддерживать форматы: PNG, JPG, JPEG, WEBP
- Валидация перед отправкой на сервер
- Проверить, что CropperJS корректно обрезает фото в квадрат (1:1)
- Ограничить размер файла (рекомендуется до 5-10 МБ)
- Показывать превью загруженного фото
- Обрабатывать ошибки загрузки

**Валидация:**

```javascript
const allowedTypes = ['image/png', 'image/jpeg', 'image/webp']
const maxSize = 5 * 1024 * 1024 // 5 МБ
```

---

### 8. Красивые отступы

**Требования:**

- Проверить и нормализовать отступы на всех страницах
- Использовать сеточную систему Vuetify (`v-container`, `v-row`, `v-col`)
- Обеспечить хороший визуальный баланс
- Адаптировать отступы для мобильных устройств

---

### 9. Анимации

**Требования:**

- Добавить единые анимации для всех интерактивных элементов
- Анимировать hover эффекты для кнопок и карточек
- Анимировать появление тостов (snackbar)
- Анимировать переходы между страницами
- Не перегружать интерфейс лишними анимациями

---

### 10. Конфетти при успешном создании рецепта

**Требования:**

- После успешного создания рецепта показать анимацию конфетти
- Анимация должна быть заметной, но не навязчивой
- Длительность - около 3-5 секунд

**Рекомендации по реализации:**
Использовать библиотеку `canvas-confetti` - это популярное и простое решение.

---

### 11. Кастомная страница 404

**Требования:**

- Создать красивую страницу 404 (Not Found)
- Страница должна соответствовать дизайну приложения
- Добавить кнопку "Вернуться на главную"
- Поддержать все языки

**Рекомендации:**

- Создать компонент `src/views/NotFoundView.vue`
- Добавить маршрут в роутер
- Использовать иллюстрацию или иконку для визуального интереса

---

### 12. Кастомный алерт подтверждения удаления

**Требования:**

- Создать компонент модального окна для подтверждения удаления рецепта
- Сообщение: "Вы точно хотите удалить этот рецепт?" (с переводами)
- Кнопки: "Отмена" и "Удалить" (красная)
- Компонент должен быть переиспользуемым

**Рекомендации:**

- Создать `src/components/DeleteConfirmDialog.vue`
- Использовать `v-dialog` из Vuetify
- Принимать через props: `v-model:show`, `title`, `message`
- Эмитить события: `confirm`, `cancel`

---

### 13. Исправить ошибку при создании рецепта

**Текущая проблема:**

- После создания рецепта показывается ошибка, но рецепт создается
- Нет логирования ошибок
- После создания ничего не происходит

**Требования:**

- Добавить детальное логирование ошибок (в консоль)
- Проверить цепочку запросов (создание рецепта -> загрузка фото)
- После успешного создания показывать тост и перенаправлять
- Если произошла ошибка при загрузке фото - рецепт все равно должен быть создан (без фото)
- Показывать пользователю понятное сообщение об ошибке

**Отладка:**
Проверить:

1. Корректность URL для запросов
2. Формат данных, отправляемых на сервер
3. Обработку ответа сервера
4. Наличие cookies при запросе

---

### 14. Исправить страницу детального просмотра рецепта

**Текущая проблема:**

- Страница детального просмотра рецепта пустая

**Требования:**

- Загружать рецепт по ID из маршрута
- Показывать все данные рецепта:
  - Фото (если есть)
  - Название
  - Ингредиенты
  - Шаги приготовления
  - Время приготовления
  - Сложность
  - Дата создания
- Кнопки:
  - "Редактировать" (только для владельца)
  - "Удалить" (только для владельца)
  - "Добавить/удалить из избранного"
  - "Назад"
- Поддерживать все языки

---

### 15. Футер

**Требования:**

- Футер **не создавать**

---

### 16. Hover эффекты и единые анимации

**Требования:**

- Создать единые hover эффекты для кнопок
- Создать единые hover эффекты для карточек рецептов
- Анимировать состояние "избранное"
- Обеспечить консистентность всех интерактивных элементов

**Рекомендации:**

- Использовать CSS-классы или Vuetify модификаторы
- Для карточек: увеличение масштаба, тень при hover
- Для кнопок: изменение цвета, легкая анимация

---

### 17. Работа с Nginx

**Требования:**

- Менять текущую конфигурацию `nginx.conf` только при необходимости
- Убедиться, что все прокси правила корректные
- Проверить, что SPA routing работает (`try_files $uri $uri/ /index.html`)
- Убедиться, что статика (изображения) доступна по `/uploads/`

Текущая конфигурация корректна и соответствует техническому заданию.

---

## Рекомендации по реализации

### Общие советы

1. Начните с баг-фиксов
2. Затем добавьте базовые фичи (i18n, 404, алерт подтверждения)
3. После этого переходите к визуальным улучшениям (отступы, анимации)
4. Последними добавляйте "визуальный сахар" (конфетти, hover эффекты)

### Тестирование

- Проверять работу на разных разрешениях экрана
- Тестировать переключение языков
- Проверять все сценарии: регистрация, вход, создание/редактирование/удаление рецептов, избранное
- Проверять работу с реальным API и с моками

---

## Наглядное руководство по отдельным фичам

### Как правильно настроить моковые данные

1. Скопировать файл `docs/test/test-recipe.json` в `frontend/src/api/mocks/recipes.json`
2. Исправить формат моков под API:
   - Заменить `difficulty`: "Легкий" → "easy", "Средний" → "medium"
   - Заменить `cookingTime` → `cooking_time`
   - Добавить `image_path` для рецептов (использовать файлы из `recipe/static/uploads/`)
3. Создать `src/api/mocks/index.js`
4. Создать `src/api/mocks/recipes.js` с логикой работы с рецептами (поиск, фильтрация, пагинация)
5. Создать `src/api/mocks/auth.js` с моками аутентификации
6. Модифицировать `src/api/client.js` для переключения между реальным API и моками
7. Добавить переменную `VITE_USE_MOCK_DATA=true` в `.env`

**Пример `src/api/mocks/recipes.js`:**

```javascript
import mockRecipes from './recipes.json'

let recipes = [...mockRecipes]

export const mockGetRecipes = (params) => {
  let result = [...recipes]
  
  // Поиск
  if (params.search) {
    const searchLower = params.search.toLowerCase()
    result = result.filter(r => 
      r.title.toLowerCase().includes(searchLower) ||
      r.ingredients.toLowerCase().includes(searchLower)
    )
  }
  
  // Фильтр по сложности
  if (params.difficulty) {
    result = result.filter(r => r.difficulty === params.difficulty)
  }
  
  // Сортировка по дате
  result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  
  // Пагинация (простая версия)
  const limit = params.limit || 12
  const hasNext = result.length > limit
  const nextCursor = hasNext ? 'next-page-mock' : null
  
  return {
    data: result.slice(0, limit),
    headers: {
      'x-next-cursor': nextCursor
    }
  }
}

export const mockGetRecipe = (id) => {
  return recipes.find(r => r.id === id)
}

export const mockCreateRecipe = (data) => {
  const newRecipe = {
    ...data,
    id: crypto.randomUUID(),
    user_id: 'mock-user-id',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    image_path: null
  }
  recipes.unshift(newRecipe)
  return newRecipe
}
```

**Пример модификации `src/api/client.js`:**

```javascript
import axios from 'axios'
import { mockGetRecipes, mockGetRecipe, mockCreateRecipe } from './mocks/recipes'

// Определяем базовые URL для разных окружений
const isDocker = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
const useMockData = import.meta.env.VITE_USE_MOCK_DATA === 'true'
const protocol = window.location.protocol
const host = window.location.host

let authBaseURL = isDocker 
  ? `${protocol}//${host}/api/v1` 
  : 'http://localhost:8000/api/v1'

let recipeBaseURL = isDocker 
  ? `${protocol}//${host}/api/v1` 
  : 'http://localhost:8080/api/v1'

// Реальный API
const realAuthApi = axios.create({
  baseURL: authBaseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

const realRecipeApi = axios.create({
  baseURL: recipeBaseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Мок API
const mockApi = {
  get: async (url, config) => {
    if (url.includes('/recipes/') && url !== '/recipes/') {
      const id = url.split('/recipes/')[1]
      const recipe = mockGetRecipe(id)
      if (!recipe) throw { response: { status: 404, data: { detail: 'Рецепт не найден' } } }
      return { data: recipe }
    }
    if (url.includes('/recipes/')) {
      return mockGetRecipes(config?.params)
    }
    return { data: {} }
  },
  post: async (url, data) => {
    if (url.includes('/recipes/')) {
      return { data: mockCreateRecipe(data) }
    }
    return { data: {} }
  },
  put: async () => ({ data: {} }),
  delete: async () => ({ status: 204 })
}

// Выбираем, какой API использовать
export const authApi = useMockData ? mockApi : realAuthApi
export const recipeApi = useMockData ? mockApi : realRecipeApi

// Интерцепторы для реального API
if (!useMockData) {
  authApi.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        console.error('Auth error:', error.response.data)
      }
      return Promise.reject(error)
    }
  )

  recipeApi.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        console.error('Recipe API auth error:', error.response.data)
      }
      return Promise.reject(error)
    }
  )
}
```

### Как добавить новые языки в i18n

1. Открыть `src/i18n.js`
2. Добавить новые объекты `kk` и `ja` в `messages`
3. Перевести все ключи
4. Обновить переключатель языков в `App.vue`
5. Обновить условие проверки языка в `App.vue`

### Как создать переиспользуемый компонент подтверждения

1. Создать `src/components/DeleteConfirmDialog.vue`
2. Использовать `v-dialog`
3. Пример структуры:

```vue
<template>
  <v-dialog v-model:show="show" width="500">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions>
        <v-btn @click="$emit('cancel')">{{ $t('recipes.cancel') }}</v-btn>
        <v-btn color="error" @click="$emit('confirm')">{{ $t('recipes.delete') }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
defineProps(['show', 'title', 'message'])
defineEmits(['confirm', 'cancel'])
</script>
```

### Как правильно обработать создание рецепта

1. Сначала отправить запрос на создание рецепта (без фото)
2. Получить `recipe_id` из ответа
3. Если есть фото - отправить отдельный запрос на загрузку
4. Если загрузка фото не удалась - не отображать ошибку, а просто оставить рецепт без фото
5. Показать тост об успехе
6. Запустить конфетти
7. Перенаправить на страницу рецептов

---

## Ссылки и ресурсы

- [Vue 3 Documentation](https://vuejs.org/)
- [Vuetify 3 Documentation](https://vuetifyjs.com/)
- [canvas-confetti](https://github.com/catdad/canvas-confetti)
- [Cropper.js](https://github.com/fengyuanchen/cropperjs)
- [Техническое задание](./tech-task.md)
- [Swagger Auth Service](http://localhost/swagger/index.html)
- [Swagger Recipe Service](http://localhost/docs)
