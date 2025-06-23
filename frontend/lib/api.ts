import axios, { InternalAxiosRequestConfig } from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000',
})

// ✅ Add Authorization to every request (JSON or FormData)
instance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.set('Authorization', `Bearer ${token}`)
  }
  return config
})

export default instance
