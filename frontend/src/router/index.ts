import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/surveys/create',
      name: 'create-survey',
      component: () => import('../views/CreateSurveyView.vue'),
    },
    {
      path: '/surveys/:id/take',
      name: 'take-survey',
      component: () => import('../views/TakeSurveyView.vue'),
    },
    {
      path: '/analytics',
      name: 'my-surveys',
      component: () => import('../views/MySurveyView.vue'),
    },
    {
      path: '/analytics/:id',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
    },
  ],
})

export default router
