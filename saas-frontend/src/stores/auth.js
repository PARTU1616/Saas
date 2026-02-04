import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { api } from 'boot/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isAdmin: (state) => state.user?.role === 'ADMIN'
  },

  actions: {
    setUserFromToken() {
      if (!this.accessToken) return

      const decoded = jwtDecode(this.accessToken)

      this.user = {
        id: decoded.sub,
        org_id: decoded.org_id,
        role: decoded.role
      }
    },

    async login(email, password) {
      const res = await api.post('/auth/login', { email, password })

      this.accessToken = res.data.access_token
      this.refreshToken = res.data.refresh_token

      localStorage.setItem('access_token', this.accessToken)
      localStorage.setItem('refresh_token', this.refreshToken)

      // Store user info from response
      this.user = {
        role: res.data.role,
        org_id: res.data.org_id,
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null

      localStorage.clear()
    }
  }
})
