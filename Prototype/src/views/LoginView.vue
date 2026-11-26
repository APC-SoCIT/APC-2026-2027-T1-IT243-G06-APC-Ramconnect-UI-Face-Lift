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
          <h2 class="text-2xl font-bold text-slate-900">
            {{ isApplicantOnly ? 'Applicant Portal Sign In' : (isStaffOnly ? 'Admissions Staff Sign In' : 'Sign In to RamConnect') }}
          </h2>
          <p class="text-xs text-slate-500">
            {{ isApplicantOnly ? 'Sign in with your registered applicant email to track your application status' : 'Access your applicant portal or staff management dashboard' }}
          </p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="login-email" class="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
            <input 
              id="login-email"
              name="email"
              type="email" 
              v-model="email" 
              autocomplete="username"
              autocorrect="off"
              autocapitalize="none"
              spellcheck="false"
              required 
              placeholder="e.g. applicant@gmail.com" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div>
            <label for="login-password" class="block text-xs font-bold text-slate-700 mb-1">Password</label>
            <div class="relative">
              <input 
                id="login-password"
                name="password"
                :type="showPassword ? 'text' : 'password'" 
                v-model="password" 
                autocomplete="current-password"
                required 
                placeholder="••••••••" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg pl-3.5 pr-10 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                :aria-pressed="showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                class="absolute inset-y-0 right-0 px-3 flex items-center text-slate-500 hover:text-slate-800"
              >
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div v-if="errorMessage" role="alert" class="p-3 bg-rose-50 border border-rose-200 rounded-lg text-rose-800 text-xs font-semibold">
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
          <router-link to="/apply" class="text-apc-navy font-bold hover:underline">Start an Application</router-link>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';
import { Eye, EyeOff } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const errorMessage = ref('');
const isSubmitting = ref(false);

const isApplicantOnly = computed(() => String(route.query.redirect || '').startsWith('/portal'));
const isStaffOnly = computed(() => String(route.query.redirect || '').startsWith('/staff'));

async function handleLogin() {
  errorMessage.value = '';
  isSubmitting.value = true;
  try {
    await authStore.login(email.value, password.value, {
      disallowStaff: isApplicantOnly.value,
      requireStaff: isStaffOnly.value
    });
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
