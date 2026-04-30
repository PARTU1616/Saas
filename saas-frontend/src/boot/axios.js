import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { useAuthStore } from 'stores/auth'

const api = axios.create({
  baseURL: 'http://prathameshgalugade.in',
})

export default boot(({ app }) => {
  api.interceptors.request.use((config) => {
    const auth = useAuthStore()
    if (auth.accessToken) {
      config.headers.Authorization = `Bearer ${auth.accessToken}`
    }
    return config
  })
  app.config.globalProperties.$api = api
})

export { api }
