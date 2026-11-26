import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const USER_KEY = 'apc_ramconnect_user';
const TOKEN_KEY = 'apc_ramconnect_token';
const STAFF_ROLES = ['admission_officer', 'marketing_admin', 'registrar', 'itro_admin'];

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'));
  const token = ref(localStorage.getItem(TOKEN_KEY) || '');

  const isAuthenticated = computed(() => !!user.value);
  const isStaff = computed(() => !!user.value && STAFF_ROLES.includes(user.value.role));
  const isApplicant = computed(() => user.value?.role === 'applicant');

  // Keep session synchronized across tabs so only one account stays signed in per browser
  if (typeof window !== 'undefined' && !window.__apcAuthStorageBound) {
    window.__apcAuthStorageBound = true;
    window.addEventListener('storage', (e) => {
      if (e.key === USER_KEY) {
        user.value = e.newValue ? JSON.parse(e.newValue) : null;
      } else if (e.key === TOKEN_KEY) {
        token.value = e.newValue || '';
      }
    });
  }

  function setSession(userData) {
    user.value = userData;
    token.value = userData?.token || 'mock_token';
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
    localStorage.setItem(TOKEN_KEY, token.value);
  }

  function validateRoleConstraint(role, options = {}) {
    const staff = STAFF_ROLES.includes(role);
    if (options.disallowStaff && staff) {
      throw new Error('Staff accounts cannot log in through the Applicant Status portal. Please use Staff Login.');
    }
    if (options.requireStaff && !staff) {
      throw new Error('Applicant accounts cannot access the Staff Dashboard.');
    }
  }

  async function login(email, password, options = {}) {
    if (user.value) {
      throw new Error('Another account is already signed in. Please log out first.');
    }

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (res.ok) {
        const data = await res.json();
        validateRoleConstraint(data.role, options);
        setSession(data);
        return data;
      }
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Invalid email or password.');
    } catch (e) {
      // Only fall back when the network request itself fails (offline preview)
      if (!(e instanceof TypeError)) {
        throw e;
      }
    }

    // Offline demo fallback
    const cleanEmail = email.trim().toLowerCase();
    let mockUser = null;
    if (cleanEmail === 'admissions@apc.edu.ph' && password === 'admin123') {
      mockUser = { id: 'u-admin-1', email: cleanEmail, full_name: 'Maria Santos (Admissions Lead)', role: 'admission_officer', token: 'mock_token_admission_officer' };
    } else if (cleanEmail === 'applicant@gmail.com' && password === 'user123') {
      mockUser = { id: 'u-app-1', email: cleanEmail, full_name: 'Juan Dela Cruz', role: 'applicant', token: 'mock_token_applicant' };
    }
    if (!mockUser) {
      throw new Error('Invalid email or password.');
    }
    validateRoleConstraint(mockUser.role, options);
    setSession(mockUser);
    return mockUser;
  }

  async function register(email, full_name, password) {
    if (user.value) {
      throw new Error('Another account is already signed in. Please log out first.');
    }
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, full_name, password })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Registration failed.');
    }
    const data = await res.json();
    setSession(data);
    return data;
  }

  function logout() {
    user.value = null;
    token.value = '';
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(TOKEN_KEY);
  }

  return {
    user,
    token,
    isAuthenticated,
    isStaff,
    isApplicant,
    setSession,
    login,
    register,
    logout
  };
});
