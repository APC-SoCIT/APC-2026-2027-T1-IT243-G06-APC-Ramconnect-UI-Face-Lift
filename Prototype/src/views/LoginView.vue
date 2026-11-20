<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <main class="flex-1 flex items-center justify-center p-4 sm:p-6 py-12">
      <div class="max-w-md w-full bg-white rounded-3xl p-8 sm:p-10 border border-slate-200 apc-card-shadow space-y-6">
        <!-- Brand Seal & Title -->
        <div class="text-center space-y-2">
          <div class="w-12 h-12 rounded-full bg-apc-navy border-2 border-apc-gold text-apc-gold flex items-center justify-center font-black mx-auto shadow">
            APC
          </div>
          <h2 class="text-2xl font-bold text-slate-900">Sign In to RamConnect</h2>
          <p class="text-xs text-slate-500">Access your applicant portal or staff management dashboard</p>
        </div>

        <!-- Quick Demo Switcher -->
        <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs space-y-2">
          <span class="font-bold text-amber-950 block text-[11px] uppercase tracking-wider">Quick Fill Demo Accounts:</span>
          <div class="flex items-center gap-2">
            <button 
              type="button" 
              @click="fillDemo('applicant')" 
              class="flex-1 bg-white hover:bg-amber-100 text-amber-900 border border-amber-300 font-semibold py-1.5 px-2.5 rounded-lg text-center transition-colors"
            >
              Applicant
            </button>
            <button 
              type="button" 
              @click="fillDemo('staff')" 
              class="flex-1 bg-apc-navy hover:bg-apc-navyLight text-white font-semibold py-1.5 px-2.5 rounded-lg text-center transition-colors"
            >
              Admissions Staff
            </button>
          </div>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
            <input 
              type="email" 
              v-model="email" 
              required 
              placeholder="e.g. applicant@gmail.com" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              v-model="password" 
              required 
              placeholder="••••••••" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div v-if="errorMessage" class="p-3 bg-rose-50 border border-rose-200 rounded-lg text-rose-800 text-xs font-semibold">
            {{ errorMessage }}
          </div>

          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="w-full bg-apc-navy hover:bg-apc-navyLight text-white font-bold text-xs py-3 rounded-xl shadow-md transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span v-if="isSubmitting">Authenticating...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <div class="pt-4 border-t border-slate-100 text-center text-xs text-slate-500">
          New applicant? 
          <router-link to="/register" class="text-apc-navy font-bold hover:underline">Create an Account</router-link>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isSubmitting = ref(false);

function fillDemo(type) {
  if (type === 'staff') {
    email.value = 'admissions@apc.edu.ph';
    password.value = 'admin123';
  } else {
    email.value = 'applicant@gmail.com';
    password.value = 'user123';
  }
}

async function handleLogin() {
  errorMessage.value = '';
  isSubmitting.value = true;
  try {
    const user = await authStore.login(email.value, password.value);
    const redirect = route.query.redirect;
    if (redirect) {
      router.push(redirect);
    } else if (authStore.isStaff) {
      router.push('/staff');
    } else {
      router.push('/portal');
    }
  } catch (e) {
    errorMessage.value = e.message || 'Invalid credentials. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>
