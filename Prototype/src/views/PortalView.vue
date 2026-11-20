<template>
  <div class="min-h-screen flex flex-col bg-apc-surface">
    <Navbar />

    <main class="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-10 space-y-8">
      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="w-10 h-10 border-4 border-slate-200 border-t-apc-navy rounded-full animate-spin mx-auto"></div>
        <p class="text-xs text-slate-500 mt-4">Loading your applicant dossier...</p>
      </div>

      <!-- No Application Found -->
      <div v-else-if="!application" class="bg-white rounded-3xl p-10 text-center border border-slate-200 apc-card-shadow space-y-4">
        <div class="w-16 h-16 rounded-full bg-amber-100 text-amber-900 flex items-center justify-center mx-auto">
          <FileQuestion class="w-8 h-8" />
        </div>
        <h2 class="text-xl font-bold text-slate-900">No Active Application Found</h2>
        <p class="text-xs text-slate-600 max-w-md mx-auto">
          You haven't submitted an admission application for Academic Year 2026-2027 yet.
        </p>
        <router-link to="/apply" class="inline-flex items-center space-x-2 bg-apc-navy text-white text-xs font-bold px-6 py-3 rounded-xl shadow-md hover:bg-apc-navyLight transition-colors">
          <span>Start Online Application</span>
          <ArrowRight class="w-4 h-4 text-apc-gold" />
        </router-link>
      </div>

      <!-- Active Application Dashboard -->
      <div v-else class="space-y-6">
        <!-- Header Card -->
        <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 apc-card-shadow flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center space-x-2.5">
              <span class="text-xs font-mono font-bold bg-apc-navy text-white px-2.5 py-0.5 rounded">
                {{ application.appform_id }}
              </span>
              <StatusBadge :status="application.status" />
            </div>
            <h1 class="text-2xl font-bold text-slate-900 mt-2">
              {{ application.first_name }} {{ application.last_name }}
            </h1>
            <p class="text-xs text-slate-500 mt-0.5">
              Target Program: <strong class="text-apc-navy">{{ application.course_name }} ({{ application.course_id }})</strong>
            </p>
          </div>

          <!-- Pay Reservation Button (When Qualified) -->
          <div v-if="application.status === 'Qualified'" class="text-right">
            <span class="text-[11px] text-emerald-800 font-bold block mb-1">🎉 You are Qualified!</span>
            <button 
              @click="showPaymentModal = true"
              class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-5 py-3 rounded-xl shadow-lg transition-transform hover:-translate-y-0.5 flex items-center space-x-2"
            >
              <CreditCard class="w-4 h-4" />
              <span>Pay Reservation Fee (₱{{ Number(application.payment_amount || 5000).toLocaleString() }})</span>
            </button>
          </div>

          <!-- Already Enrolled Badge -->
          <div v-else-if="application.status === 'Enrolled'" class="p-3 bg-amber-50 border border-amber-300 rounded-xl text-left">
            <span class="text-[10px] text-amber-900 font-bold uppercase tracking-wider block">Official Enrollment Confirmed</span>
            <span class="font-mono font-bold text-sm text-apc-navy block mt-0.5">ID: {{ application.student_id }}</span>
            <span class="font-mono text-xs text-slate-600 block">{{ application.student_email }}</span>
          </div>
        </div>

        <!-- Visual Admission Stage Stepper -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 apc-card-shadow">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-6">
            Admissions Intake Evaluation Pipeline
          </h3>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <!-- Stage 1 -->
            <div :class="['p-4 rounded-xl border text-center transition-all', isStagePassed(1) ? 'bg-emerald-50 border-emerald-300 text-emerald-950' : 'bg-slate-50 border-slate-200 text-slate-400']">
              <div class="w-7 h-7 rounded-full mx-auto flex items-center justify-center font-bold text-xs mb-2" :class="isStagePassed(1) ? 'bg-emerald-600 text-white' : 'bg-slate-300 text-slate-600'">
                1
              </div>
              <h4 class="font-bold text-xs">Submitted</h4>
              <p class="text-[11px] mt-0.5 text-slate-500">Dossier Received</p>
            </div>

            <!-- Stage 2 -->
            <div :class="['p-4 rounded-xl border text-center transition-all', isStagePassed(2) ? 'bg-emerald-50 border-emerald-300 text-emerald-950' : (application.status === 'Under Review' ? 'bg-blue-50 border-blue-300 text-blue-950 font-bold' : 'bg-slate-50 border-slate-200 text-slate-400')]">
              <div class="w-7 h-7 rounded-full mx-auto flex items-center justify-center font-bold text-xs mb-2" :class="isStagePassed(2) ? 'bg-emerald-600 text-white' : (application.status === 'Under Review' ? 'bg-blue-600 text-white' : 'bg-slate-300 text-slate-600')">
                2
              </div>
              <h4 class="font-bold text-xs">Under Review</h4>
              <p class="text-[11px] mt-0.5 text-slate-500">Document Verification</p>
            </div>

            <!-- Stage 3 -->
            <div :class="['p-4 rounded-xl border text-center transition-all', isStagePassed(3) ? 'bg-emerald-50 border-emerald-300 text-emerald-950' : (application.status === 'Qualified' ? 'bg-emerald-100 border-emerald-400 font-bold' : 'bg-slate-50 border-slate-200 text-slate-400')]">
              <div class="w-7 h-7 rounded-full mx-auto flex items-center justify-center font-bold text-xs mb-2" :class="isStagePassed(3) || application.status === 'Qualified' ? 'bg-emerald-600 text-white' : 'bg-slate-300 text-slate-600'">
                3
              </div>
              <h4 class="font-bold text-xs">Qualified</h4>
              <p class="text-[11px] mt-0.5 text-slate-500">Eligible for Reservation</p>
            </div>

            <!-- Stage 4 -->
            <div :class="['p-4 rounded-xl border text-center transition-all', application.status === 'Enrolled' ? 'bg-amber-100 border-amber-400 text-amber-950 font-bold' : 'bg-slate-50 border-slate-200 text-slate-400']">
              <div class="w-7 h-7 rounded-full mx-auto flex items-center justify-center font-bold text-xs mb-2" :class="application.status === 'Enrolled' ? 'bg-apc-navy text-apc-gold' : 'bg-slate-300 text-slate-600'">
                4
              </div>
              <h4 class="font-bold text-xs">Enrolled</h4>
              <p class="text-[11px] mt-0.5 text-slate-500">Student Profile Synced</p>
            </div>
          </div>
        </div>

        <!-- Officer Notice / Alert Banner -->
        <div v-if="application.officer_notes" class="p-5 rounded-2xl bg-amber-50 border border-amber-200">
          <div class="flex items-start space-x-3">
            <div class="w-7 h-7 rounded-full bg-amber-200 text-amber-900 flex items-center justify-center shrink-0 mt-0.5">
              <Bell class="w-4 h-4" />
            </div>
            <div>
              <h4 class="text-xs font-bold text-amber-950 uppercase tracking-wide">Admissions Officer Evaluation Remarks</h4>
              <p class="text-xs text-slate-800 mt-1 leading-relaxed whitespace-pre-wrap">{{ application.officer_notes }}</p>
            </div>
          </div>
        </div>

        <!-- Official Student Credentials Card (when Enrolled) -->
        <div v-if="application.status === 'Enrolled'" class="bg-gradient-to-br from-apc-navy to-apc-navyLight text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-white/10 space-y-4">
          <div class="flex items-center space-x-2.5">
            <Award class="w-5 h-5 text-apc-gold" />
            <h3 class="text-lg font-bold">Official APC Student Confirmation</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed max-w-xl">
            Congratulations! Your reservation fee payment has been validated by the APC Finance Office. Your profile is synchronized with RAMPortal (SIS) and Microsoft 365.
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
            <div class="p-3.5 bg-white/10 rounded-xl border border-white/10">
              <span class="text-[11px] text-apc-gold uppercase font-bold block">Assigned Student ID</span>
              <span class="text-lg font-mono font-bold">{{ application.student_id }}</span>
            </div>
            <div class="p-3.5 bg-white/10 rounded-xl border border-white/10 sm:col-span-2">
              <span class="text-[11px] text-apc-gold uppercase font-bold block">APC Institutional Microsoft 365 Account</span>
              <span class="text-base font-mono font-bold">{{ application.student_email }}</span>
            </div>
          </div>
        </div>

        <!-- Application Summary Card -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 apc-card-shadow space-y-4">
          <h3 class="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">Dossier Overview</h3>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div>
              <span class="text-slate-400 block text-[11px]">Intake Term</span>
              <span class="font-semibold text-slate-800">{{ application.acad_year }}, {{ application.term }}</span>
            </div>
            <div>
              <span class="text-slate-400 block text-[11px]">Entry Status</span>
              <span class="font-semibold text-slate-800">{{ application.entry_status }}</span>
            </div>
            <div>
              <span class="text-slate-400 block text-[11px]">Registered Mobile</span>
              <span class="font-semibold text-slate-800">{{ application.mobile }}</span>
            </div>
            <div>
              <span class="text-slate-400 block text-[11px]">Previous School</span>
              <span class="font-semibold text-slate-800">{{ application.prev_school || 'Not specified' }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Payment Modal Component -->
    <PaymentModal 
      v-if="showPaymentModal" 
      :amount="application?.payment_amount || 5000"
      @close="showPaymentModal = false"
      @paid="handlePayment"
    />

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { api } from '../api/client';
import Navbar from '../components/common/Navbar.vue';
import Footer from '../components/common/Footer.vue';
import StatusBadge from '../components/common/StatusBadge.vue';
import PaymentModal from '../components/applicant/PaymentModal.vue';
import { FileQuestion, ArrowRight, CreditCard, Bell, Award } from 'lucide-vue-next';

const route = useRoute();
const authStore = useAuthStore();

const application = ref(null);
const isLoading = ref(true);
const showPaymentModal = ref(false);

onMounted(async () => {
  await loadApplication();
});

async function loadApplication() {
  isLoading.value = true;
  try {
    const userEmail = authStore.user?.email || null;
    application.value = await api.getMyApplication(userEmail);
  } catch (e) {
    console.error(e);
  } finally {
    isLoading.value = false;
  }
}

function isStagePassed(stageNum) {
  if (!application.value) return false;
  const s = application.value.status;
  if (s === 'Enrolled') return true;
  if (stageNum === 1) return true;
  if (stageNum === 2 && ['Under Review', 'Qualified'].includes(s)) return true;
  if (stageNum === 3 && ['Qualified'].includes(s)) return true;
  return false;
}

async function handlePayment(paymentData) {
  if (!application.value) return;
  try {
    const res = await api.payReservationFee(application.value.appform_id, paymentData);
    application.value = res.application;
    showPaymentModal.value = false;
  } catch (e) {
    alert("Payment verification failed. Please check reference details.");
  }
}
</script>
