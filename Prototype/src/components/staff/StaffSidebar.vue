<template>
  <aside class="w-64 bg-apc-navy border-r border-white/10 text-slate-300 flex flex-col min-h-screen shrink-0">
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
    <nav class="flex-1 p-4 space-y-6 text-xs">
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
import { useAuthStore } from '../../stores/auth';
import { Inbox, Users, FileCode, GraduationCap, Palette, ExternalLink, LogOut } from 'lucide-vue-next';

const authStore = useAuthStore();
</script>
