import axios from 'axios'

export const authApi = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const recipeApi = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

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
