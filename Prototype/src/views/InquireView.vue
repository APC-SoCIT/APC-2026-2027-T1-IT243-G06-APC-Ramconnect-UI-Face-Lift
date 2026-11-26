<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <!-- Header Banner -->
    <section class="apc-navy-gradient text-white py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto text-center space-y-3">
        <span class="text-xs font-bold uppercase tracking-wider text-apc-gold bg-white/10 px-3 py-1 rounded-full border border-white/20">
          Admissions Inquiry
        </span>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight">
          Have Questions About APC?
        </h1>
        <p class="text-xs sm:text-sm text-slate-300 max-w-xl mx-auto">
          Connect directly with an Admissions Officer. Fill out your details below and our team will get in touch with you shortly.
        </p>
      </div>
    </section>

    <!-- Main Content Form / Success Card -->
    <main class="flex-1 max-w-3xl w-full mx-auto px-4 sm:px-6 py-10">
      <!-- Success State -->
      <div v-if="submittedRef" class="bg-white rounded-3xl p-8 sm:p-10 border border-slate-200 apc-card-shadow text-center space-y-6">
        <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto">
          <CheckCircle2 class="w-10 h-10" />
        </div>
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
            Inquiry Ticket Created
          </span>
          <h2 class="text-2xl font-extrabold text-slate-900 mt-3">Thank you for reaching out!</h2>
          <p class="text-xs text-slate-600 mt-2 max-w-md mx-auto">
            Your inquiry has been logged directly into our admissions CRM pipeline. An admissions counselor will reach out via email or phone.
          </p>
        </div>

        <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 inline-block text-left min-w-[280px]">
          <span class="text-[11px] text-slate-400 block uppercase font-bold tracking-wider">Your Tracking Reference</span>
          <span class="text-xl font-black text-apc-navy font-mono">{{ submittedRef }}</span>
          <p class="text-[11px] text-slate-500 mt-1">Keep this code handy if you visit campus or call admissions.</p>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
          <router-link :to="authStore.isApplicant ? '/portal' : '/apply'" class="w-full sm:w-auto bg-apc-gold hover:bg-apc-goldDark text-apc-navy font-bold text-xs px-6 py-3 rounded-xl shadow transition-colors">
            {{ authStore.isApplicant ? 'Go to My Dashboard' : 'Proceed to Online Application' }}
          </router-link>
          <button @click="resetForm" class="w-full sm:w-auto border border-slate-300 text-slate-700 hover:bg-slate-100 font-semibold text-xs px-6 py-3 rounded-xl transition-colors">
            Submit Another Inquiry
          </button>
        </div>
      </div>

      <!-- Inquiry Form -->
      <div v-else class="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 apc-card-shadow space-y-6">
        <div class="border-b border-slate-100 pb-4">
          <h2 class="text-lg font-bold text-slate-900">Prospective Student Inquiry Form</h2>
          <p class="text-xs text-slate-500 mt-0.5">Fields marked with an asterisk (<span class="text-rose-600">*</span>) are required.</p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Name Row -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">First Name <span class="text-rose-600">*</span></label>
              <input 
                type="text" 
                v-model="form.first_name" 
                required 
                placeholder="e.g. Juan" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Last Name <span class="text-rose-600">*</span></label>
              <input 
                type="text" 
                v-model="form.last_name" 
                required 
                placeholder="e.g. Dela Cruz" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
          </div>

          <!-- Contact Row -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Email Address <span class="text-rose-600">*</span></label>
              <input 
                type="email" 
                v-model="form.email" 
                required 
                placeholder="name@email.com" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Mobile Number <span class="text-rose-600">*</span></label>
              <input 
                type="tel" 
                v-model="form.mobile" 
                required 
                placeholder="09171234567" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
          </div>

          <!-- Parent / Guardian Row -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Parent / Guardian Name</label>
              <input 
                type="text" 
                v-model="form.guardian_name" 
                placeholder="Optional" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Guardian Contact Number</label>
              <input 
                type="tel" 
                v-model="form.guardian_contact" 
                placeholder="Optional" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              />
            </div>
          </div>

          <!-- Program Interest & Visit Mode -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Program of Interest</label>
              <select 
                v-model="form.program_interest"
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              >
                <option value="">Select a Program</option>
                <option v-for="c in siteStore.courses" :key="c.id" :value="c.id">
                  {{ c.name }} ({{ c.id }})
                </option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Preferred Consultation Mode</label>
              <select 
                v-model="form.visit_mode"
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
              >
                <option value="onsite">On-Campus Visit (Makati)</option>
                <option value="online">Online Consultation (MS Teams)</option>
              </select>
            </div>
          </div>

          <!-- Message / Question -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Your Question or Inquiry <span class="text-rose-600">*</span></label>
            <textarea 
              v-model="form.question" 
              required 
              rows="4" 
              placeholder="Ask about admissions requirements, tuition fees, scholarships, or credit transfer..." 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            ></textarea>
          </div>

          <!-- Data Privacy Consent -->
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-start space-x-2.5">
            <input 
              type="checkbox" 
              id="privacy" 
              v-model="privacyConsent" 
              required 
              class="mt-0.5 rounded border-slate-300 text-apc-navy focus:ring-apc-gold"
            />
            <label for="privacy" class="text-[11px] text-slate-600 leading-tight">
              I agree to the collection and processing of my contact information in accordance with Republic Act 10173 (Data Privacy Act of 2012) and APC's privacy guidelines.
            </label>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="w-full bg-apc-navy hover:bg-apc-navyLight text-white font-bold text-xs py-3.5 rounded-xl shadow-md transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span v-if="isSubmitting">Submitting Inquiry...</span>
            <span v-else>Submit Online Inquiry</span>
            <Send v-if="!isSubmitting" class="w-4 h-4 text-apc-gold" />
          </button>
        </form>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useSiteSettingsStore } from '../stores/siteSettings';
import { useAuthStore } from '../stores/auth';
import { api } from '../api/client';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';
import { CheckCircle2, Send } from 'lucide-vue-next';

const siteStore = useSiteSettingsStore();
const authStore = useAuthStore();
const isSubmitting = ref(false);
const submittedRef = ref(null);
const privacyConsent = ref(false);

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  mobile: '',
  guardian_name: '',
  guardian_contact: '',
  program_interest: '',
  visit_mode: 'onsite',
  preferred_date: '',
  question: ''
});

onMounted(() => {
  siteStore.fetchAll();
});

async function handleSubmit() {
  if (!privacyConsent.value) return;
  isSubmitting.value = true;
  try {
    const res = await api.createInquiry(form);
    submittedRef.value = res.reference_id || 'INQ-' + Math.floor(10000 + Math.random() * 90000);
  } catch (e) {
    console.error(e);
  } finally {
    isSubmitting.value = false;
  }
}

function resetForm() {
  submittedRef.value = null;
  privacyConsent.value = false;
  Object.assign(form, {
    first_name: '',
    last_name: '',
    email: '',
    mobile: '',
    guardian_name: '',
    guardian_contact: '',
    program_interest: '',
    visit_mode: 'onsite',
    preferred_date: '',
    question: ''
  });
}
</script>
