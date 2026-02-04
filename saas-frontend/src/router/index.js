import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import { useAuthStore } from 'stores/auth'

export default function (/* { ssrContext } */) {
  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createWebHistory(import.meta.env.BASE_URL),
  })

    Router.beforeEach((to) => {
  const auth = useAuthStore()

  if (auth.accessToken && !auth.user) {
    auth.setUserFromToken()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

 if (to.meta.requiresAdmin && auth.user?.role !== 'ADMIN') {
    return '/'
  }
})


  return Router
}
