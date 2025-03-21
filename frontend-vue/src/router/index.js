import { createRouter, createWebHistory } from 'vue-router';
import LoginUser from '../components/LoginUser.vue';
import VerifyToken from '../components/VerifyToken.vue';
import VoteUser from '../components/VoteUser.vue';

const routes = [
  { path: '/', component: LoginUser },
  { 
    path: '/verify-token', 
    component: VerifyToken, 
    meta: { requiresAuth: true, requiresValidSession: true } 
  },
  { 
    path: '/vote', 
    component: VoteUser, 
    meta: { requiresAuth: true, requiresValidSession: true } 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Enhanced middleware with session validation
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const sessionTime = localStorage.getItem('sessionTime');
  const sessionNim = localStorage.getItem('sessionNim');
  const currentTime = new Date().getTime();
  
  // Check for session timeout (30 minutes)
  const isSessionValid = sessionTime && (currentTime - parseInt(sessionTime)) < 30 * 60 * 1000;

  // Clear any invalid sessions
  if (!isSessionValid && isLoggedIn) {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('sessionTime');
    localStorage.removeItem('sessionNim');
  }

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/'); // Redirect to login if not logged in
  } 
  else if (to.meta.requiresValidSession) {
    // For verify-token route, check if NIM in URL matches the one in session
    if (to.path === '/verify-token') {
      const queryNim = to.query.nim;
      
      if (!queryNim || queryNim !== sessionNim) {
        next('/'); // Redirect if NIM doesn't match or is missing
        return;
      }
    }
    
    // For vote route, check if user parameter exists
    if (to.path === '/vote' && !to.query.user) {
      next('/'); // Redirect if user data is missing
      return;
    }
    
    next(); // Allow if all checks pass
  } 
  else {
    next(); // Allow for non-protected routes
  }
});

export default router;