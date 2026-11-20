import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('apc_ramconnect_user') || 'null'));
  const token = ref(localStorage.getItem('apc_ramconnect_token') || '');

  const isAuthenticated = computed(() => !!user.value);
  const isStaff = computed(() => {
    if (!user.value) return false;
    const role = user.value.role;
    return ['admission_officer', 'marketing_admin', 'registrar', 'itro_admin'].includes(role);
  });
  const isApplicant = computed(() => user.value?.role === 'applicant');

  async function login(email, password) {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (res.ok) {
        const data = await res.json();
        user.value = data;
        token.value = data.token || 'mock_token';
        localStorage.setItem('apc_ramconnect_user', JSON.stringify(data));
        localStorage.setItem('apc_ramconnect_token', token.value);
        return data;
      }
    } catch (e) {}

    // Fallback authentication
    let role = 'applicant';
    let fullName = email.split('@')[0];
    if (email.endsWith('@apc.edu.ph') || email.includes('admin') || email.includes('staff')) {
      role = 'admission_officer';
      fullName = 'Maria Santos (Admissions Lead)';
    } else {
      fullName = 'Juan Dela Cruz';
    }

    const mockUser = {
      id: 'u-' + Math.random().toString(36).substring(2, 9),
      email,
      full_name: fullName,
      role,
      token: 'mock_token_' + role
    };

    user.value = mockUser;
    token.value = mockUser.token;
    localStorage.setItem('apc_ramconnect_user', JSON.stringify(mockUser));
    localStorage.setItem('apc_ramconnect_token', token.value);
    return mockUser;
  }

  async function register(email, full_name, password) {
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, full_name, password })
      });
      if (res.ok) {
        const data = await res.json();
        user.value = data;
        token.value = data.token || 'mock_token';
        localStorage.setItem('apc_ramconnect_user', JSON.stringify(data));
        localStorage.setItem('apc_ramconnect_token', token.value);
        return data;
      }
    } catch (e) {}

    const mockUser = {
      id: 'u-' + Math.random().toString(36).substring(2, 9),
      email,
      full_name,
      role: email.endsWith('@apc.edu.ph') ? 'admission_officer' : 'applicant',
      token: 'mock_token_applicant'
    };
    user.value = mockUser;
    token.value = mockUser.token;
    localStorage.setItem('apc_ramconnect_user', JSON.stringify(mockUser));
    localStorage.setItem('apc_ramconnect_token', token.value);
    return mockUser;
  }

  function logout() {
    user.value = null;
    token.value = '';
    localStorage.removeItem('apc_ramconnect_user');
    localStorage.removeItem('apc_ramconnect_token');
  }

  return {
    user,
    token,
    isAuthenticated,
    isStaff,
    isApplicant,
    login,
    register,
    logout
  };
});
