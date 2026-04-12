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
    path: '/admin',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', component: () => import('pages/AdminDashboard.vue') },
      { path: 'users', component: () => import('pages/admin/UsersPage.vue') }
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
