import axios from 'axios'

// Определяем базовые URL для разных окружений
const isDocker = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
const protocol = window.location.protocol
const host = window.location.host

let authBaseURL = isDocker 
  ? `${protocol}//${host}/api/v1` 
  : 'http://localhost:8000/api/v1'

let recipeBaseURL = isDocker 
  ? `${protocol}//${host}/api/v1` 
  : 'http://localhost:8080/api/v1'

export const authApi = axios.create({
  baseURL: authBaseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const recipeApi = axios.create({
  baseURL: recipeBaseURL,
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
