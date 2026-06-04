import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, recipeApi } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = computed(() => !!token.value)

  const login = async (email, password) => {
    try {
      const response = await authApi.post('/login', { email, password })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', token.value)
      return response.data
    } catch (error) {
      throw error
    }
  }

  const register = async (email, password) => {
    try {
      const response = await authApi.post('/register', { email, password })
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authApi.post('/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  const fetchUser = async () => {
    try {
      const response = await authApi.get('/me')
      user.value = response.data
      return user.value
    } catch (error) {
      console.error('Fetch user error:', error)
      return null
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUser
  }
})
