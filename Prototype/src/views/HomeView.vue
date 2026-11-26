<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <!-- Hero Section (Gradient & High Contrast) -->
    <section class="apc-navy-gradient text-white pt-10 pb-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
        <!-- Left Hero Copy -->
        <div class="lg:col-span-7 space-y-5 text-center lg:text-left">
          <div class="inline-flex items-center space-x-2 bg-white/10 border border-white/20 px-3.5 py-1.5 rounded-full text-xs font-semibold text-apc-gold backdrop-blur-md">
            <Sparkles class="w-4 h-4 text-apc-gold" />
            <span>Academic Year 2026–2027 Admissions Now Open</span>
          </div>

          <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
            Your industry-based <br class="hidden sm:block"/>
            <span class="text-apc-gold">learning begins here!</span>
          </h1>

          <p class="text-base sm:text-lg text-slate-300 font-medium max-w-xl mx-auto lg:mx-0">
            Real Projects. Real Learning. Asia Pacific College bridges academic excellence with industry immersion through corporate partnerships with IBM and the SM Foundation.
          </p>

          <!-- Hero Image Preview (from paper mockups) -->
          <div class="relative rounded-2xl overflow-hidden border border-white/20 shadow-2xl max-w-lg mx-auto lg:mx-0 group">
            <img 
              :src="siteStore.settings.hero_image || 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80'" 
              alt="APC Campus and Students"
              class="w-full h-48 sm:h-56 object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-apc-navy via-transparent to-transparent"></div>
            <div class="absolute bottom-3 left-4 right-4 flex items-center justify-between text-xs text-slate-300">
              <span class="font-bold text-white">APC Magallanes Campus</span>
              <span class="text-apc-gold font-medium">HyFlex Onsite & Online</span>
            </div>
          </div>
        </div>

        <!-- Right Action Card (The Core Intake Hub from Mockups) -->
        <div class="lg:col-span-5">
          <div class="bg-white rounded-3xl p-6 sm:p-8 text-slate-900 shadow-2xl border border-slate-100 relative">
            <div class="flex items-center space-x-3 pb-4 border-b border-slate-100">
              <div class="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center font-black text-apc-navy text-sm">
                APC
              </div>
              <div>
                <h3 class="text-base sm:text-lg font-bold text-slate-900">
                  {{ siteStore.settings.welcome_title || 'Welcome to Asia Pacific College!' }}
                </h3>
                <p class="text-xs text-slate-500">Official RamConnect Online Portal</p>
              </div>
            </div>

            <!-- Welcome Text / Notice -->
            <div class="mt-4 p-3.5 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-950 leading-relaxed">
              <span class="font-bold block mb-1">📢 Admission Announcement:</span>
              {{ siteStore.settings.welcome_text }}
            </div>

            <!-- 3 Main Action CTAs -->
            <div class="mt-6 space-y-3">
              <!-- Inquire -->
              <router-link 
                to="/inquire"
                class="w-full flex items-center justify-between bg-apc-gold hover:bg-apc-goldDark text-apc-navy font-bold text-sm px-5 py-3.5 rounded-xl shadow-md transition-transform hover:-translate-y-0.5"
              >
                <div class="text-left">
                  <div class="text-xs text-apc-navy/80 uppercase font-semibold">Have Questions?</div>
                  <div class="font-extrabold">Inquire Online</div>
                </div>
                <ArrowRight class="w-5 h-5 text-apc-navy" />
              </router-link>

              <!-- Apply Now -->
              <router-link 
                :to="authStore.isApplicant ? '/portal' : '/apply'"
                class="w-full flex items-center justify-between bg-apc-navy hover:bg-apc-navyLight text-white font-bold text-sm px-5 py-3.5 rounded-xl shadow-md transition-transform hover:-translate-y-0.5"
              >
                <div class="text-left">
                  <div class="text-xs text-slate-300 uppercase font-semibold">{{ authStore.isApplicant ? 'Application Active' : 'Ready to Register?' }}</div>
                  <div class="font-extrabold">{{ authStore.isApplicant ? 'Go to My Dashboard' : 'Apply for AY 2026–2027' }}</div>
                </div>
                <ArrowRight class="w-5 h-5 text-apc-gold" />
              </router-link>

              <!-- Portal Login / Status -->
              <router-link 
                to="/portal"
                class="w-full flex items-center justify-between bg-slate-50 hover:bg-slate-100 text-slate-800 font-bold text-sm px-5 py-3.5 rounded-xl border border-slate-300 transition-colors"
              >
                <div class="text-left">
                  <div class="text-xs text-slate-500 uppercase font-semibold">Existing Applicant?</div>
                  <div class="font-extrabold text-slate-900">Track My Application Status</div>
                </div>
                <UserCheck class="w-5 h-5 text-slate-600" />
              </router-link>
            </div>

            <!-- Mode Notice -->
            <div class="mt-5 pt-4 border-t border-slate-100 text-[11px] text-slate-500 flex items-center justify-between">
              <span>Learning Mode: <strong>HyFlex (Onsite & Online)</strong></span>
              <router-link to="/login" class="text-apc-navy font-bold hover:underline">Staff Login →</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Schedule Milestones Bar (Centerpiece from Mockups) -->
    <section class="max-w-6xl mx-auto px-4 sm:px-6 -mt-10 relative z-20 w-full">
      <div class="bg-amber-100/95 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-amber-300 text-amber-950">
        <h3 class="text-xs font-bold uppercase tracking-wider text-center text-amber-900 mb-5 flex items-center justify-center space-x-1.5">
          <Calendar class="w-4 h-4 text-apc-goldDark" />
          <span>{{ siteStore.settings.schedule_title || 'Admission Timeline AY 2026-2027' }}</span>
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-amber-200">
          <div v-for="m in siteStore.milestones" :key="m.id" class="pt-4 md:pt-0 md:px-4">
            <span class="text-sm sm:text-base font-extrabold text-apc-navy block font-mono">
              {{ m.date_text }}
            </span>
            <span class="text-xs font-bold text-slate-800 mt-1 block">
              {{ m.title }}
            </span>
            <p v-if="m.description" class="text-[11px] text-slate-600 mt-0.5">
              {{ m.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Opportunities & Promos Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold uppercase tracking-wider text-apc-goldDark bg-amber-50 px-3 py-1 rounded-full border border-amber-200">
          Discover Opportunities
        </span>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-3">
          Opportunities Waiting For You
        </h2>
        <p class="text-xs sm:text-sm text-slate-600 mt-2">
          Scholarships, institutional grants, and corporate sponsorships designed to empower high-achieving and deserving students.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
        <div 
          v-for="promo in siteStore.promos" 
          :key="promo.promo_id"
          class="bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-lg transition-all group flex flex-col"
        >
          <div class="h-44 overflow-hidden relative">
            <img 
              :src="promo.promo_image" 
              :alt="promo.promo_title" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent"></div>
          </div>
          <div class="p-6 flex-1 flex flex-col justify-between">
            <div>
              <div class="w-6 h-1 bg-apc-gold rounded-full mb-3"></div>
              <h3 class="font-bold text-base text-slate-900 group-hover:text-apc-navy transition-colors">
                {{ promo.promo_title }}
              </h3>
              <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                {{ promo.promo_body }}
              </p>
            </div>
            <div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
              <a 
                :href="promo.promo_link || 'https://apc.edu.ph'" 
                target="_blank" 
                class="text-xs font-bold text-apc-navy hover:text-apc-goldDark flex items-center space-x-1"
              >
                <span>Learn Requirements</span>
                <ChevronRight class="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Application Do's & Don'ts (Directly from Mockups) -->
    <section class="bg-white border-y border-slate-200 py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
          <h2 class="text-xl sm:text-2xl font-bold text-slate-900">Application Guidelines & Do's and Don'ts</h2>
          <p class="text-xs text-slate-500 mt-1">Follow these standards to ensure your application dossier is evaluated without delay.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start space-x-3">
            <div class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
              <Check class="w-3.5 h-3.5 stroke-[3]" />
            </div>
            <div>
              <h4 class="font-bold text-slate-800">Valid and Secured Email Address</h4>
              <p class="text-slate-500 mt-0.5">Your email is necessary for status updates, interview schedules, and official student credential provisioning.</p>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start space-x-3">
            <div class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
              <Check class="w-3.5 h-3.5 stroke-[3]" />
            </div>
            <div>
              <h4 class="font-bold text-slate-800">Working PH Mobile Number</h4>
              <p class="text-slate-500 mt-0.5">Admissions officers contact applicants and guardians directly to clarify missing documents and schedule interviews.</p>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start space-x-3">
            <div class="w-6 h-6 rounded-full bg-rose-100 text-rose-800 flex items-center justify-center shrink-0 mt-0.5">
              <X class="w-3.5 h-3.5 stroke-[3]" />
            </div>
            <div>
              <h4 class="font-bold text-slate-800">No Multiple Or Duplicate Accounts</h4>
              <p class="text-slate-500 mt-0.5">Creating multiple accounts will flag duplicate identity conflicts and delay your verification process.</p>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start space-x-3">
            <div class="w-6 h-6 rounded-full bg-rose-100 text-rose-800 flex items-center justify-center shrink-0 mt-0.5">
              <X class="w-3.5 h-3.5 stroke-[3]" />
            </div>
            <div>
              <h4 class="font-bold text-slate-800">Security of Access Credentials</h4>
              <p class="text-slate-500 mt-0.5">Never disclose your password or portal token. Staff will never ask for your account password.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useSiteSettingsStore } from '../stores/siteSettings';
import { useAuthStore } from '../stores/auth';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';
import { Sparkles, ArrowRight, UserCheck, Calendar, ChevronRight, Check, X } from 'lucide-vue-next';

const siteStore = useSiteSettingsStore();
const authStore = useAuthStore();

onMounted(() => {
  siteStore.fetchAll();
});
</script>
