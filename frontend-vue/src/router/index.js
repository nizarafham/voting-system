import { createRouter, createWebHistory } from 'vue-router';
import LoginUser from '../components/LoginUser.vue';
import VerifyToken from '../components/VerifyToken.vue';
import VoteUser from '../components/VoteUser.vue';

const routes = [
  { path: '/', component: LoginUser },
  { path: '/verify-token', component: VerifyToken, meta: { requiresAuth: true } },
  { path: '/vote', component: VoteUser, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Middleware untuk mengecek apakah user sudah login sebelum masuk ke halaman tertentu
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/'); // Redirect ke halaman login jika belum login
  } else {
    next();
  }
});

export default router;
