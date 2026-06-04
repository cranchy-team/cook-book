# cook-book: тестовые данные

## 1. Тестовые пользователи (Auth Service)

### Регистрация нового пользователя

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### Авторизация пользователя

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }' -c cookies.txt
```

### Получение профиля пользователя

```bash
curl -X GET http://localhost:8000/api/v1/auth/profile \
  -b cookies.txt
```

### Смена пароля

```bash
curl -X POST http://localhost:8000/api/v1/auth/change-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "old_password": "testpassword123",
    "new_password": "newtestpassword123"
  }'
```

### Выход из системы

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -b cookies.txt
```

---

## 2. Тестовые рецепты (Recipe Service)

### Создание нового рецепта

```bash
curl -X POST http://localhost:8080/api/v1/recipes \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Омлет с овощами",
    "ingredients": "3 яйца, 50 мл молока, 1 помидор, 50 г шампиньонов, соль, перец",
    "steps": "1. Взбей яйца с молоком. 2. Нарежь овощи. 3. Обжари овощи. 4. Залей яйцами и жди до готовности.",
    "cooking_time": 15,
    "difficulty": "easy"
  }'
```

### Получение списка рецептов

```bash
curl -X GET http://localhost:8080/api/v1/recipes \
  -b cookies.txt
```

### Получение рецепта по ID

```bash
curl -X GET http://localhost:8080/api/v1/recipes/{recipe_id} \
  -b cookies.txt
```

### Обновление рецепта

```bash
curl -X PUT http://localhost:8080/api/v1/recipes/{recipe_id} \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Омлет с овощами и сыром",
    "ingredients": "3 яйца, 50 мл молока, 1 помидор, 50 г шампиньонов, 30 г сыра, соль, перец",
    "steps": "1. Взбей яйца с молоком. 2. Нарежь овощи. 3. Обжари овощи. 4. Залей яйцами, посыпь сыром и жди до готовности.",
    "cooking_time": 15,
    "difficulty": "easy"
  }'
```

### Удаление рецепта

```bash
curl -X DELETE http://localhost:8080/api/v1/recipes/{recipe_id} \
  -b cookies.txt
```

---

## 3. Избранное

### Добавление рецепта в избранное

```bash
curl -X POST http://localhost:8080/api/v1/favorites/{recipe_id} \
  -b cookies.txt
```

### Получение списка избранных рецептов

```bash
curl -X GET http://localhost:8080/api/v1/favorites \
  -b cookies.txt
```

### Удаление рецепта из избранного

```bash
curl -X DELETE http://localhost:8080/api/v1/favorites/{recipe_id} \
  -b cookies.txt
```

---

## 4. Доступные значения сложности

- `easy` - Легко
- `medium` - Средне
- `hard` - Сложно
