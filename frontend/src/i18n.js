import { createI18n } from 'vue-i18n'

const messages = {
  ru: {
    nav: {
      recipes: 'Рецепты',
      favorites: 'Избранное',
      login: 'Войти',
      register: 'Регистрация',
      logout: 'Выход'
    },
    close: 'Закрыть',
    auth: {
      login: 'Вход',
      register: 'Регистрация',
      email: 'Email',
      password: 'Пароль',
      submit: 'Войти',
      registerSubmit: 'Зарегистрироваться',
      noAccount: 'Нет аккаунта?',
      hasAccount: 'Уже есть аккаунт?',
      error: 'Ошибка входа',
      success: 'Успешный вход'
    },
    recipes: {
      title: 'Рецепты',
      create: 'Создать рецепт',
      edit: 'Редактировать рецепт',
      delete: 'Удалить рецепт',
      deleteConfirm: 'Вы уверены?',
      titleLabel: 'Название',
      ingredients: 'Ингредиенты',
      steps: 'Шаги приготовления',
      cookingTime: 'Время (мин)',
      difficulty: 'Сложность',
      difficultyEasy: 'Легко',
      difficultyMedium: 'Средне',
      difficultyHard: 'Сложно',
      image: 'Фото',
      uploadImage: 'Загрузить фото',
      noRecipes: 'У вас пока нет рецептов',
      search: 'Поиск рецептов...',
      filter: 'Фильтр',
      save: 'Сохранить',
      cancel: 'Отмена',
      created: 'Рецепт создан',
      updated: 'Рецепт обновлён',
      deleted: 'Рецепт удалён'
    },
    favorites: {
      title: 'Избранное',
      empty: 'Список избранного пуст',
      added: 'Добавлено в избранное',
      removed: 'Удалено из избранного'
    }
  },
  en: {
    nav: {
      recipes: 'Recipes',
      favorites: 'Favorites',
      login: 'Login',
      register: 'Register',
      logout: 'Logout'
    },
    close: 'Close',
    auth: {
      login: 'Login',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      submit: 'Login',
      registerSubmit: 'Register',
      noAccount: "Don't have an account?",
      hasAccount: 'Already have an account?',
      error: 'Login error',
      success: 'Login successful'
    },
    recipes: {
      title: 'Recipes',
      create: 'Create Recipe',
      edit: 'Edit Recipe',
      delete: 'Delete Recipe',
      deleteConfirm: 'Are you sure?',
      titleLabel: 'Title',
      ingredients: 'Ingredients',
      steps: 'Steps',
      cookingTime: 'Cooking Time (min)',
      difficulty: 'Difficulty',
      difficultyEasy: 'Easy',
      difficultyMedium: 'Medium',
      difficultyHard: 'Hard',
      image: 'Image',
      uploadImage: 'Upload Image',
      noRecipes: 'You have no recipes yet',
      search: 'Search recipes...',
      filter: 'Filter',
      save: 'Save',
      cancel: 'Cancel',
      created: 'Recipe created',
      updated: 'Recipe updated',
      deleted: 'Recipe deleted'
    },
    favorites: {
      title: 'Favorites',
      empty: 'Your favorites list is empty',
      added: 'Added to favorites',
      removed: 'Removed from favorites'
    }
  }
}

export default createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages
})
