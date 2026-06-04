import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'recipes',
    component: () => import('@/views/RecipesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: () => import('@/views/FavoritesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recipes/create',
    name: 'create-recipe',
    component: () => import('@/views/RecipeCreateView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recipes/:id/edit',
    name: 'edit-recipe',
    component: () => import('@/views/RecipeEditView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recipes/:id',
    name: 'recipe-detail',
    component: () => import('@/views/RecipeDetailView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth && !token) {
    next({ name: 'login' })
  } else if ((to.name === 'login' || to.name === 'register') && token) {
    next({ name: 'recipes' })
  } else {
    next()
  }
})

export default router
