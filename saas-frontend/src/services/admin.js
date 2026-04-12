import { api } from 'boot/axios'

export function getAdminStats() {
  return api.get('/admin/stats')
}
