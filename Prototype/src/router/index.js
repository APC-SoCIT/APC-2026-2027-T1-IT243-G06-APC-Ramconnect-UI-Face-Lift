import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

import HomeView from '../views/HomeView.vue';
import InquireView from '../views/InquireView.vue';
import ApplyView from '../views/ApplyView.vue';
import PortalView from '../views/PortalView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';

import DashboardView from '../views/staff/DashboardView.vue';
import ApplicantsView from '../views/staff/ApplicantsView.vue';
import FormBuilderView from '../views/staff/FormBuilderView.vue';
import ProgramsView from '../views/staff/ProgramsView.vue';
import DesignView from '../views/staff/DesignView.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/inquire', name: 'inquire', component: InquireView },
  { path: '/apply', name: 'apply', component: ApplyView },
  { path: '/portal', name: 'portal', component: PortalView, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  
  // Staff CRM & CMS Hub
  { path: '/staff', name: 'staff-dashboard', component: DashboardView, meta: { requiresStaff: true } },
  { path: '/staff/applicants', name: 'staff-applicants', component: ApplicantsView, meta: { requiresStaff: true } },
  { path: '/staff/form-builder', name: 'staff-form-builder', component: FormBuilderView, meta: { requiresStaff: true } },
  { path: '/staff/programs', name: 'staff-programs', component: ProgramsView, meta: { requiresStaff: true } },
  { path: '/staff/design', name: 'staff-design', component: DesignView, meta: { requiresStaff: true } },
  
  // Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    return { top: 0 };
  }
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresStaff) {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } });
    }
    if (!authStore.isStaff) {
      return next({ name: 'portal' });
    }
  }

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } });
    }
  }

  next();
});

export default router;
