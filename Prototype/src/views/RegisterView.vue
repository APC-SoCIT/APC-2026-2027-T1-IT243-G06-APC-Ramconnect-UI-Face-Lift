<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <main class="flex-1 flex items-center justify-center p-4 sm:p-6 py-12">
      <div class="max-w-md w-full bg-white rounded-3xl p-8 sm:p-10 border border-slate-200 apc-card-shadow space-y-6">
        <div class="text-center space-y-2">
          <div class="w-12 h-12 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black mx-auto shadow">
            APC
          </div>
          <h2 class="text-2xl font-bold text-slate-900">Create Applicant Account</h2>
          <p class="text-xs text-slate-500">Sign up to apply and track your admissions status in real time</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Full Legal Name</label>
            <input 
              type="text" 
              v-model="fullName" 
              required 
              placeholder="e.g. Juan Santos Dela Cruz" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
            <input 
              type="email" 
              v-model="email" 
              required 
              placeholder="name@email.com" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              v-model="password" 
              required 
              minlength="6"
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
            <span v-if="isSubmitting">Creating Account...</span>
            <span v-else>Register & Proceed</span>
          </button>
        </form>

        <div class="pt-4 border-t border-slate-100 text-center text-xs text-slate-500">
          Already have an account? 
          <router-link to="/login" class="text-apc-navy font-bold hover:underline">Log In</router-link>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';

const authStore = useAuthStore();
const router = useRouter();

const fullName = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isSubmitting = ref(false);

async function handleRegister() {
  errorMessage.value = '';
  isSubmitting.value = true;
  try {
    await authStore.register(email.value, fullName.value, password.value);
    router.push('/apply');
  } catch (e) {
    errorMessage.value = e.message || 'Registration failed. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>
