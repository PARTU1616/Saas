export const routes = [

  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  },
  {
    path: '/admin/users',
    component: () => import('pages/AdminUsersPage.vue'),
    meta: { requiresAuth: true, requiresRole: 'ADMIN' }
  },
  {
    path: '/admin',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', component: () => import('pages/AdminDashboard.vue') }
    ]
  },
  {
    path: '/forgot-password',
    component: () => import('pages/ForgotPassword.vue')
  },
  {
    path: '/reset-password',
    component: () => import('pages/ResetPassword.vue')
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  }




]
