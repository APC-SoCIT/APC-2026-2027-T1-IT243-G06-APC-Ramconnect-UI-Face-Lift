<template>
  <div class="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-sm flex justify-end animate-fade-in">
    <div class="w-full max-w-2xl bg-white shadow-2xl flex flex-col h-full transform transition-transform">
      <!-- Drawer Header -->
      <div class="p-6 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div>
          <div class="flex items-center space-x-2">
            <span class="text-xs font-mono font-bold bg-apc-navy text-white px-2 py-0.5 rounded">
              {{ applicant.appform_id }}
            </span>
            <StatusBadge :status="applicant.status" />
          </div>
          <h3 class="mt-2 text-xl font-bold text-slate-900">
            {{ applicant.first_name }} {{ applicant.middle_name ? applicant.middle_name + ' ' : '' }}{{ applicant.last_name }}
          </h3>
          <p class="text-xs text-apc-navy font-semibold">{{ applicant.course_name }} ({{ applicant.course_id }})</p>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600 p-2 rounded-full hover:bg-slate-200">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Drawer Body -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- Status & Evaluation Action Box -->
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-300">
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3 flex items-center space-x-1.5">
            <CheckCircle class="w-4 h-4 text-emerald-600" />
            <span>Admissions Officer Evaluation Controls</span>
          </h4>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
            <button
              @click="setStatus('Qualified')"
              :class="applicant.status === 'Qualified' ? 'ring-2 ring-emerald-500 bg-emerald-600 text-white' : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100'"
              class="py-2.5 px-3 rounded-lg text-xs font-bold border border-emerald-300 transition-all text-center"
            >
              Qualify
            </button>
            <button
              @click="setStatus('Incomplete Dossier')"
              :class="applicant.status === 'Incomplete Dossier' ? 'ring-2 ring-orange-500 bg-orange-600 text-white' : 'bg-orange-50 text-orange-800 hover:bg-orange-100'"
              class="py-2.5 px-3 rounded-lg text-xs font-bold border border-orange-300 transition-all text-center"
            >
              Incomplete
            </button>
            <button
              @click="setStatus('Under Review')"
              :class="applicant.status === 'Under Review' ? 'ring-2 ring-blue-500 bg-blue-600 text-white' : 'bg-blue-50 text-blue-800 hover:bg-blue-100'"
              class="py-2.5 px-3 rounded-lg text-xs font-bold border border-blue-300 transition-all text-center"
            >
              Under Review
            </button>
            <button
              @click="setStatus('Rejected')"
              :class="applicant.status === 'Rejected' ? 'ring-2 ring-rose-500 bg-rose-600 text-white' : 'bg-rose-50 text-rose-800 hover:bg-rose-100'"
              class="py-2.5 px-3 rounded-lg text-xs font-bold border border-rose-300 transition-all text-center"
            >
              Reject
            </button>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">
              Officer Remarks / Required Resubmissions (Rendered on Applicant's Portal):
            </label>
            <textarea
              v-model="notes"
              rows="3"
              placeholder="e.g. Please re-upload legible copy of Form 137 or PSA Birth Certificate..."
              class="w-full text-xs bg-white border border-slate-300 rounded-lg p-3 text-slate-900 focus:ring-2 focus:ring-apc-gold outline-none"
            ></textarea>
          </div>

          <div class="mt-3 flex justify-end">
            <button
              @click="saveEvaluation"
              class="bg-apc-navy hover:bg-apc-navyLight text-white font-bold text-xs px-5 py-2.5 rounded-lg transition-colors shadow-sm"
            >
              Save Dossier Evaluation
            </button>
          </div>
        </div>

        <!-- Student ID & Official Record if Enrolled -->
        <div v-if="applicant.status === 'Enrolled'" class="p-4 rounded-xl bg-amber-50 border border-amber-300">
          <div class="flex items-center space-x-2 text-amber-900 font-bold text-xs">
            <Award class="w-4 h-4 text-apc-goldDark" />
            <span>Official Institutional Student Record</span>
          </div>
          <div class="mt-2 grid grid-cols-2 gap-3 text-xs">
            <div>
              <span class="text-slate-500 text-[11px] block">Allocated Student ID:</span>
              <span class="font-mono font-bold text-slate-900">{{ applicant.student_id || '2026-10492' }}</span>
            </div>
            <div>
              <span class="text-slate-500 text-[11px] block">M365 Student Email:</span>
              <span class="font-mono font-bold text-slate-900">{{ applicant.student_email }}</span>
            </div>
          </div>
        </div>

        <!-- Applicant Profile Details -->
        <div>
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Applicant Personal Information</h4>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Email Address</span>
              <span class="font-semibold text-slate-800 break-all">{{ applicant.email }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Mobile Phone</span>
              <span class="font-semibold text-slate-800">{{ applicant.mobile }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Date of Birth</span>
              <span class="font-semibold text-slate-800">{{ applicant.birth_date || 'N/A' }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Sex / Nationality</span>
              <span class="font-semibold text-slate-800">{{ applicant.sex || 'N/A' }} / {{ applicant.nationality || 'Filipino' }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Entry Status</span>
              <span class="font-semibold text-slate-800">{{ applicant.entry_status || 'Freshman' }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Intake Term</span>
              <span class="font-semibold text-slate-800">{{ applicant.acad_year }}, {{ applicant.term }}</span>
            </div>
            <div class="col-span-2 sm:col-span-3 p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Residential Address</span>
              <span class="font-semibold text-slate-800">{{ applicant.home_address }}, {{ applicant.city }}</span>
            </div>
          </div>
        </div>

        <!-- Academic Background -->
        <div>
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Academic Background</h4>
          <div class="grid grid-cols-3 gap-3 text-xs">
            <div class="col-span-2 p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Previous School</span>
              <span class="font-semibold text-slate-800">{{ applicant.prev_school || 'N/A' }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Sector / Year</span>
              <span class="font-semibold text-slate-800">{{ applicant.prev_school_sector }} ({{ applicant.prev_school_year }})</span>
            </div>
          </div>
        </div>

        <!-- Dynamic Form Builder Answers -->
        <div v-if="applicant.answers && Object.keys(applicant.answers).length">
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Additional Form Questionnaire Responses</h4>
          <div class="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-2 text-xs">
            <div v-for="(val, key) in applicant.answers" :key="key" class="flex justify-between py-1 border-b border-slate-200 last:border-0">
              <span class="font-medium text-slate-500 capitalize">{{ key.replace(/_/g, ' ') }}:</span>
              <span class="font-bold text-slate-800">{{ val }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import StatusBadge from '../common/StatusBadge.vue';
import { X, CheckCircle, Award } from 'lucide-vue-next';

const props = defineProps({
  applicant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'status-updated']);

const targetStatus = ref(props.applicant.status);
const notes = ref(props.applicant.officer_notes || '');

function setStatus(st) {
  targetStatus.value = st;
}

function saveEvaluation() {
  emit('status-updated', {
    appform_id: props.applicant.appform_id,
    status: targetStatus.value,
    officer_notes: notes.value
  });
}
</script>
