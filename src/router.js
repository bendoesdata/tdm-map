import { createRouter, createWebHistory } from 'vue-router';

import HomePage from './pages/HomePage.vue';
import CaseStudiesPage from './pages/CaseStudiesPage.vue';
import AboutPage from './pages/AboutPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/case-studies', component: CaseStudiesPage },
  { path: '/about', component: AboutPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
