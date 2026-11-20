<template>
  <!-- Mobile Top Bar (Visible only on mobile < md) -->
  <div class="md:hidden bg-apc-navy border-b border-white/10 px-4 py-3 flex items-center justify-between text-white sticky top-0 z-30 shadow-md">
    <div class="flex items-center space-x-2.5">
      <div class="w-8 h-8 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black text-xs shadow">
        APC
      </div>
      <div>
        <h2 class="text-white font-bold text-xs tracking-tight">Staff CRM Hub</h2>
        <span class="text-[10px] text-apc-gold font-medium block">Admissions & CMS</span>
      </div>
    </div>

    <button 
      @click="mobileDrawerOpen = true"
      class="text-slate-300 hover:text-white p-2 rounded-lg bg-white/10 hover:bg-white/15 transition-colors focus:outline-none"
      aria-label="Open staff menu"
    >
      <Menu class="w-5 h-5" />
    </button>
  </div>

  <!-- Mobile Off-Canvas Drawer (Overlay on mobile) -->
  <div 
    v-if="mobileDrawerOpen" 
    class="md:hidden fixed inset-0 z-50 flex bg-slate-900/70 backdrop-blur-sm animate-fade-in"
    @click.self="mobileDrawerOpen = false"
  >
    <div class="w-72 max-w-[85vw] bg-apc-navy text-slate-300 flex flex-col h-full shadow-2xl border-r border-white/10">
      <!-- Drawer Header -->
      <div class="p-4 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black text-xs shadow">
            APC
          </div>
          <div>
            <h2 class="text-white font-bold text-xs tracking-tight">Staff Navigation</h2>
            <span class="text-[10px] text-apc-gold font-medium">{{ authStore.user?.role || 'Staff' }}</span>
          </div>
        </div>
        <button @click="mobileDrawerOpen = false" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Drawer Nav Links -->
      <nav class="flex-1 p-4 space-y-5 text-xs overflow-y-auto">
        <div>
          <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
            Intake & Student CRM
          </span>
          <div class="space-y-1">
            <router-link 
              to="/staff" 
              @click="mobileDrawerOpen = false"
              exact-active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
              class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
            >
              <Inbox class="w-4 h-4" />
              <span>Inquiries Dashboard</span>
            </router-link>
            
            <router-link 
              to="/staff/applicants" 
              @click="mobileDrawerOpen = false"
              active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
              class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
            >
              <Users class="w-4 h-4" />
              <span>Applicant Dossiers</span>
            </router-link>
          </div>
        </div>

        <div>
          <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
            Content & No-Code CMS
          </span>
          <div class="space-y-1">
            <router-link 
              to="/staff/form-builder" 
              @click="mobileDrawerOpen = false"
              active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
              class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
            >
              <FileCode class="w-4 h-4" />
              <span>Admission Form Builder</span>
            </router-link>

            <router-link 
              to="/staff/programs" 
              @click="mobileDrawerOpen = false"
              active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
              class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
            >
              <GraduationCap class="w-4 h-4" />
              <span>Programs & Quotas</span>
            </router-link>

            <router-link 
              to="/staff/design" 
              @click="mobileDrawerOpen = false"
              active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
              class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
            >
              <Palette class="w-4 h-4" />
              <span>Site Designer & Theme</span>
            </router-link>
          </div>
        </div>

        <div>
          <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
            Portals & Links
          </span>
          <div class="space-y-1">
            <router-link 
              to="/" 
              @click="mobileDrawerOpen = false"
              class="flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 transition-colors"
            >
              <span>Public Website</span>
              <ExternalLink class="w-3.5 h-3.5" />
            </router-link>
            <a 
              href="https://apc.edu.ph" 
              target="_blank" 
              class="flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 transition-colors"
            >
              <span>apc.edu.ph Portal</span>
              <ExternalLink class="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </nav>

      <!-- Drawer Profile -->
      <div class="p-4 border-t border-white/10 bg-apc-navyLight/40 flex items-center justify-between">
        <div class="flex items-center space-x-2 truncate">
          <div class="w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-white shrink-0">
            {{ authStore.user?.full_name ? authStore.user.full_name[0] : 'S' }}
          </div>
          <div class="truncate">
            <p class="text-xs font-semibold text-white truncate">{{ authStore.user?.full_name || 'Staff' }}</p>
            <span class="text-[10px] text-apc-gold font-medium uppercase">{{ authStore.user?.role || 'Staff' }}</span>
          </div>
        </div>
        <button @click="authStore.logout(); mobileDrawerOpen = false; $router.push('/login')" class="text-slate-400 hover:text-red-400 p-1 rounded">
          <LogOut class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>

  <!-- Desktop Permanent Sidebar (Visible on md+) -->
  <aside class="hidden md:flex flex-col w-64 bg-apc-navy border-r border-white/10 text-slate-300 min-h-screen shrink-0 sticky top-0 h-screen">
    <!-- Brand / Header -->
    <div class="p-5 border-b border-white/10 flex items-center space-x-3">
      <div class="w-9 h-9 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black text-sm shadow">
        APC
      </div>
      <div>
        <h2 class="text-white font-bold text-sm tracking-tight">Staff CRM Hub</h2>
        <span class="text-[11px] text-apc-gold font-medium">Admissions & CMS</span>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 p-4 space-y-6 text-xs overflow-y-auto">
      <div>
        <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
          Intake & Student CRM
        </span>
        <div class="space-y-1">
          <router-link 
            to="/staff" 
            exact-active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
            class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
          >
            <Inbox class="w-4 h-4" />
            <span>Inquiries Dashboard</span>
          </router-link>
          
          <router-link 
            to="/staff/applicants" 
            active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
            class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
          >
            <Users class="w-4 h-4" />
            <span>Applicant Dossiers</span>
          </router-link>
        </div>
      </div>

      <div>
        <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
          Content & No-Code CMS
        </span>
        <div class="space-y-1">
          <router-link 
            to="/staff/form-builder" 
            active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
            class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
          >
            <FileCode class="w-4 h-4" />
            <span>Admission Form Builder</span>
          </router-link>

          <router-link 
            to="/staff/programs" 
            active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
            class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
          >
            <GraduationCap class="w-4 h-4" />
            <span>Programs & Quotas</span>
          </router-link>

          <router-link 
            to="/staff/design" 
            active-class="bg-apc-gold text-apc-navy font-bold shadow-sm"
            class="flex items-center space-x-2.5 px-3 py-2.5 rounded-lg text-slate-200 hover:bg-white/10 transition-colors"
          >
            <Palette class="w-4 h-4" />
            <span>Site Designer & Theme</span>
          </router-link>
        </div>
      </div>

      <div>
        <span class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 block mb-2">
          Portals & Links
        </span>
        <div class="space-y-1">
          <router-link 
            to="/" 
            class="flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 transition-colors"
          >
            <span>Public Website</span>
            <ExternalLink class="w-3.5 h-3.5" />
          </router-link>
          <a 
            href="https://apc.edu.ph" 
            target="_blank" 
            class="flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:bg-white/5 transition-colors"
          >
            <span>apc.edu.ph Portal</span>
            <ExternalLink class="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </nav>

    <!-- Officer Profile Box -->
    <div class="p-4 border-t border-white/10 bg-apc-navyLight/40 flex items-center justify-between">
      <div class="flex items-center space-x-2.5 truncate">
        <div class="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-white shrink-0">
          {{ authStore.user?.full_name ? authStore.user.full_name[0] : 'S' }}
        </div>
        <div class="truncate">
          <p class="text-xs font-semibold text-white truncate">{{ authStore.user?.full_name || 'Admissions Staff' }}</p>
          <span class="text-[10px] text-apc-gold font-medium uppercase">{{ authStore.user?.role || 'Staff' }}</span>
        </div>
      </div>
      <button @click="authStore.logout(); $router.push('/login')" class="text-slate-400 hover:text-red-400 p-1 rounded">
        <LogOut class="w-4 h-4" />
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { Inbox, Users, FileCode, GraduationCap, Palette, ExternalLink, LogOut, Menu, X } from 'lucide-vue-next';

const authStore = useAuthStore();
const mobileDrawerOpen = ref(false);
</script>
