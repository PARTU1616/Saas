import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { useAuthStore } from 'stores/auth'

  const api = axios.create({
  baseURL: 'http://127.0.0.1:8080',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()

  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }

  return config
})

api.interceptors.response.use(
  res => res,
  async error => {
    const auth = useAuthStore()

    if (error.response?.status === 401 && auth.refreshToken) {
      try {
        const res = await api.post('/auth/refresh', {
          refresh_token: auth.refreshToken
        })

        auth.accessToken = res.data.access_token
        localStorage.setItem('access_token', auth.accessToken)

        error.config.headers.Authorization =
          `Bearer ${auth.accessToken}`

        return api(error.config)
      } catch {
        auth.logout()
      }
    }

    return Promise.reject(error)
  }
)



export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }
