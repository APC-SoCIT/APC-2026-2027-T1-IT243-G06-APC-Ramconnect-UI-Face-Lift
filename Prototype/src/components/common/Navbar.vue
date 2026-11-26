<template>
  <header class="bg-apc-navy border-b border-white/10 sticky top-0 z-40 backdrop-blur-md bg-opacity-95">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        <!-- Logo & Title -->
        <div class="flex items-center space-x-3 sm:space-x-4">
          <router-link to="/" class="flex items-center space-x-3 group">
            <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-apc-navy flex items-center justify-center border-2 border-apc-gold shadow-md group-hover:scale-105 transition-transform">
              <svg viewBox="0 0 100 100" class="w-8 h-8 text-apc-gold">
                <circle cx="50" cy="50" r="46" fill="#0B1E3D" stroke="#FDB813" stroke-width="3"/>
                <path d="M50 20 L75 75 L60 75 L50 48 L40 75 L25 75 Z" fill="#FDB813" />
                <circle cx="50" cy="38" r="8" fill="#0B1E3D" stroke="#FDB813" stroke-width="2"/>
              </svg>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-white font-bold tracking-tight text-base sm:text-lg">Asia Pacific College</span>
                <span class="text-xs bg-apc-gold text-apc-navy font-extrabold px-1.5 py-0.5 rounded shadow-sm uppercase tracking-wider">RamConnect</span>
              </div>
              <p class="text-slate-300 text-xs hidden sm:block">Online Admissions & Student Intake Portal</p>
            </div>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-6 text-sm font-medium">
          <router-link to="/" class="text-slate-200 hover:text-apc-gold transition-colors py-1">Home</router-link>
          <router-link to="/inquire" class="text-slate-200 hover:text-apc-gold transition-colors py-1">Inquire</router-link>
          <router-link :to="authStore.isApplicant ? '/portal' : '/apply'" class="text-slate-200 hover:text-apc-gold transition-colors py-1">Apply Now</router-link>
          
          <!-- Persistent link to main APC website (Resolves Appendix I Feedback) -->
          <a href="https://apc.edu.ph" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-white flex items-center space-x-1 text-xs border border-white/20 px-2.5 py-1 rounded-full hover:border-apc-gold transition-colors">
            <span>apc.edu.ph</span>
            <ExternalLink class="w-3 h-3" />
          </a>

          <!-- User Portal / Staff Links -->
          <div class="flex items-center space-x-3 pl-4 border-l border-white/10">
            <template v-if="authStore.isAuthenticated">
              <router-link v-if="authStore.isStaff" to="/staff" class="text-xs font-semibold bg-apc-gold/20 text-apc-gold border border-apc-gold/40 px-3 py-1.5 rounded-lg hover:bg-apc-gold hover:text-apc-navy transition-all flex items-center space-x-1.5">
                <ShieldCheck class="w-4 h-4" />
                <span>Staff CRM</span>
              </router-link>
              <router-link v-else to="/portal" class="text-xs font-semibold bg-apc-gold text-apc-navy px-3.5 py-1.5 rounded-lg hover:bg-apc-goldDark transition-colors shadow-sm">
                My Application
              </router-link>
              <button @click="handleLogout" class="text-slate-400 hover:text-red-300 text-xs font-medium py-1">
                Log Out
              </button>
            </template>
            <template v-else>
              <router-link to="/login" class="text-slate-200 hover:text-white text-xs font-semibold px-3 py-1.5">
                Log In
              </router-link>
              <router-link to="/apply" class="text-xs font-bold bg-apc-gold text-apc-navy px-4 py-2 rounded-lg hover:bg-apc-goldDark transition-all shadow-md">
                Start Application
              </router-link>
            </template>
          </div>
        </nav>

        <!-- Mobile Menu Button -->
        <div class="flex md:hidden items-center space-x-2">
          <router-link v-if="authStore.isAuthenticated && !authStore.isStaff" to="/portal" class="text-xs font-bold bg-apc-gold text-apc-navy px-3 py-1.5 rounded-lg">
            Portal
          </router-link>
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-slate-300 hover:text-white p-2 focus:outline-none">
            <Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-apc-navyLight border-b border-white/10 px-4 pt-3 pb-5 space-y-3">
      <router-link @click="mobileMenuOpen = false" to="/" class="block text-slate-200 hover:text-apc-gold font-medium py-2">Home</router-link>
      <router-link @click="mobileMenuOpen = false" to="/inquire" class="block text-slate-200 hover:text-apc-gold font-medium py-2">Inquire</router-link>
      <router-link @click="mobileMenuOpen = false" :to="authStore.isApplicant ? '/portal' : '/apply'" class="block text-slate-200 hover:text-apc-gold font-medium py-2">Apply Online</router-link>
      <a href="https://apc.edu.ph" target="_blank" class="flex items-center justify-between text-slate-400 py-2 border-t border-white/10 text-xs">
        <span>Visit Main Website (apc.edu.ph)</span>
        <ExternalLink class="w-3.5 h-3.5" />
      </a>
      
      <div class="pt-3 border-t border-white/10 space-y-2">
        <template v-if="authStore.isAuthenticated">
          <router-link v-if="authStore.isStaff" @click="mobileMenuOpen = false" to="/staff" class="block w-full text-center bg-apc-gold text-apc-navy font-bold py-2.5 rounded-lg">
            Staff CRM Dashboard
          </router-link>
          <router-link v-else @click="mobileMenuOpen = false" to="/portal" class="block w-full text-center bg-apc-gold text-apc-navy font-bold py-2.5 rounded-lg">
            My Applicant Portal
          </router-link>
          <button @click="handleLogout" class="block w-full text-center text-slate-300 hover:text-red-400 py-2 text-sm">
            Sign Out ({{ authStore.user?.email }})
          </button>
        </template>
        <template v-else>
          <router-link @click="mobileMenuOpen = false" to="/login" class="block w-full text-center border border-white/30 text-white font-medium py-2 rounded-lg">
            Log In
          </router-link>
          <router-link @click="mobileMenuOpen = false" to="/apply" class="block w-full text-center bg-apc-gold text-apc-navy font-bold py-2.5 rounded-lg">
            Register & Apply
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import { ExternalLink, ShieldCheck, Menu, X } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();
const mobileMenuOpen = ref(false);

function handleLogout() {
  authStore.logout();
  mobileMenuOpen.value = false;
  router.push('/');
}
</script>
