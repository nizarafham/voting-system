import { createRouter, createWebHistory } from 'vue-router';
import LoginUser from '../components/LoginUser.vue';
import VerifyToken from '../components/VerifyToken.vue';
import VoteUser from '../components/VoteUser.vue';

const routes = [
  { path: '/', component: LoginUser },
  { path: '/verify-token', component: VerifyToken },
  { path: '/vote', component: VoteUser, props: true }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
