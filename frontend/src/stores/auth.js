import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isLoading = ref(false)

  const isLoggedIn = computed(() => !!user.value)

  const login = async (email, password) => {
    try {
      isLoading.value = true
      const response = await authApi.post('/auth/login', { email, password })
      user.value = response.data
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (email, password) => {
    try {
      isLoading.value = true
      const response = await authApi.post('/auth/register', { email, password })
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await authApi.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
    }
  }

  const fetchUser = async () => {
    try {
      isLoading.value = true
      const response = await authApi.get('/auth/profile')
      user.value = response.data
      return user.value
    } catch (error) {
      console.error('Fetch user error:', error)
      user.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUser
  }
})
