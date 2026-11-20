<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <!-- Application Top Banner -->
    <section class="apc-navy-gradient text-white py-10 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto text-center space-y-2">
        <span class="text-xs font-bold uppercase tracking-wider text-apc-gold bg-white/10 px-3 py-1 rounded-full border border-white/20">
          Official Online Admission
        </span>
        <h1 class="text-2xl sm:text-4xl font-extrabold tracking-tight">
          Begin Your Journey at Asia Pacific College
        </h1>
        <p class="text-xs sm:text-sm text-slate-300 max-w-xl mx-auto">
          Academic Year 2026–2027 Admission Intake. Complete the details below to register your applicant profile and submit your dossier.
        </p>
      </div>
    </section>

    <!-- Main Application Container -->
    <main class="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-10 space-y-8">
      <!-- Data Privacy Notice Box (Matches Paper's Design) -->
      <div class="bg-white rounded-2xl p-6 border border-slate-200 apc-card-shadow">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-full bg-amber-100 text-amber-900 flex items-center justify-center shrink-0 mt-0.5">
            <ShieldCheck class="w-4 h-4 text-apc-goldDark" />
          </div>
          <div class="space-y-2 text-xs">
            <h3 class="font-bold text-slate-900 text-sm">Data Privacy Notice & Consent</h3>
            <p class="text-slate-600 leading-relaxed">
              {{ siteStore.settings.privacy_notice || 'APC collects and maintains personal data as part of its records management process in accordance with Republic Act 10173 (Data Privacy Act of 2012).' }}
            </p>
            <div class="pt-2 flex items-start space-x-2">
              <input 
                type="checkbox" 
                id="apply-consent" 
                v-model="consentGiven" 
                class="mt-0.5 rounded border-slate-300 text-apc-navy focus:ring-apc-gold"
              />
              <label for="apply-consent" class="text-[11px] text-slate-700 font-medium">
                {{ siteStore.settings.privacy_consent || 'I have read and understood the collection, processing, and management of my personal data along with the policies stated in the APC Data Privacy Policy.' }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- 1. Interactive Course Picker -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 apc-card-shadow">
          <CoursePicker 
            :courses="siteStore.courses" 
            v-model="selectedCourseId" 
          />
        </div>

        <!-- 2. Dynamic Schema Form Sections -->
        <DynamicFormRenderer 
          :sections="siteStore.formSections" 
          :model="formData" 
        />

        <!-- Error Message If Incomplete -->
        <div v-if="validationError" class="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold flex items-center space-x-2">
          <AlertCircle class="w-4 h-4 shrink-0" />
          <span>{{ validationError }}</span>
        </div>

        <!-- Submission Action -->
        <div class="bg-white rounded-2xl p-6 border border-slate-200 apc-card-shadow flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h4 class="font-bold text-slate-900 text-xs sm:text-sm">Ready to Register Dossier?</h4>
            <p class="text-[11px] text-slate-500">You will be redirected to your personal dashboard to track evaluation standing.</p>
          </div>
          <button 
            type="submit" 
            :disabled="isSubmitting || !consentGiven"
            class="w-full sm:w-auto bg-apc-navy hover:bg-apc-navyLight text-white font-bold text-xs px-8 py-3.5 rounded-xl shadow-lg transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span v-if="isSubmitting">Submitting Application...</span>
            <span v-else>Submit Application & View Status</span>
            <ArrowRight v-if="!isSubmitting" class="w-4 h-4 text-apc-gold" />
          </button>
        </div>
      </form>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSiteSettingsStore } from '../stores/siteSettings';
import { useAuthStore } from '../stores/auth';
import { api } from '../api/client';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';
import CoursePicker from '../components/applicant/CoursePicker.vue';
import DynamicFormRenderer from '../components/applicant/DynamicFormRenderer.vue';
import { ShieldCheck, AlertCircle, ArrowRight } from 'lucide-vue-next';

const siteStore = useSiteSettingsStore();
const authStore = useAuthStore();
const router = useRouter();

const selectedCourseId = ref('BSCS');
const consentGiven = ref(true);
const isSubmitting = ref(false);
const validationError = ref('');

const formData = reactive({
  acad_term: 'AY 2026-2027, Term 1',
  app_level: 'College/Undergraduate',
  entry_status: 'Freshman',
  first_name: '',
  middle_name: '',
  last_name: '',
  birth_date: '2007-01-01',
  sex: 'Male',
  nationality: 'Filipino',
  email: '',
  mobile: '',
  home_address: '',
  city: '',
  prev_school: '',
  prev_school_sector: 'Public',
  prev_school_year: '2025'
});

onMounted(async () => {
  await siteStore.fetchAll();
  if (authStore.user) {
    formData.email = authStore.user.email || '';
    if (authStore.user.full_name) {
      const parts = authStore.user.full_name.split(' ');
      formData.first_name = parts[0] || '';
      formData.last_name = parts.slice(1).join(' ') || '';
    }
  }
});

async function handleSubmit() {
  validationError.value = '';
  if (!selectedCourseId.value) {
    validationError.value = 'Please select your target degree program above.';
    return;
  }
  if (!formData.first_name || !formData.last_name || !formData.email || !formData.mobile) {
    validationError.value = 'Please fill out all required name, email, and contact fields.';
    return;
  }
  if (!consentGiven.value) {
    validationError.value = 'Please confirm the Data Privacy consent before proceeding.';
    return;
  }

  isSubmitting.value = true;
  try {
    const payload = {
      course_id: selectedCourseId.value,
      ...formData,
      answers: { ...formData }
    };

    const res = await api.createApplication(payload);
    
    // Auto-login applicant if not logged in
    if (!authStore.isAuthenticated) {
      authStore.login(formData.email, 'user123');
    }

    router.push({ name: 'portal', query: { app_id: res.appform_id } });
  } catch (e) {
    console.error(e);
    validationError.value = 'Failed to submit application. Please verify your details.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>
