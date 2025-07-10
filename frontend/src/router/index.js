import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { guestOnly: true, layout: 'AuthLayout' }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { guestOnly: true, layout: 'AuthLayout' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/user/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/itinerary/new',
    name: 'createItinerary',
    component: () => import('../views/itinerary/CreateItineraryView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/itinerary/my-list',
    name: 'itineraryList',
    component: () => import('../views/itinerary/ItineraryListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/itinerary/:id',
    name: 'itineraryResult',
    component: () => import('../views/itinerary/ItineraryResultView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/:catchAll(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/auth'); // @ adalah alias ke src/
  const authStore = useAuthStore();

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.guestOnly)) {
    if (authStore.isAuthenticated) {
      next({ name: 'home' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
