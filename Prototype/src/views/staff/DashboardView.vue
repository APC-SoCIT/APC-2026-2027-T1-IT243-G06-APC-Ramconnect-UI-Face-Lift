<template>
  <div class="flex min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top Bar -->
      <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">Inquiries CRM Dashboard</h1>
          <p class="text-xs text-slate-500">Manage incoming prospective student inquiries, consultations, and CRM notes</p>
        </div>
        <div class="flex items-center space-x-3">
          <router-link to="/inquire" target="_blank" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center space-x-1">
            <span>View Public Form</span>
            <ExternalLink class="w-3.5 h-3.5" />
          </router-link>
        </div>
      </header>

      <!-- Main Body -->
      <main class="flex-1 p-6 space-y-6 overflow-y-auto">
        <!-- KPI Metrics Grid -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span class="text-[11px] text-slate-400 font-bold uppercase tracking-wider block">Total Inquiries</span>
            <span class="text-2xl font-black text-slate-900 mt-1 block">{{ stats.total_inquiries }}</span>
          </div>
          <div class="bg-white p-4 rounded-xl border border-amber-200 bg-amber-50/50 shadow-sm">
            <span class="text-[11px] text-amber-800 font-bold uppercase tracking-wider block">New / Unhandled</span>
            <span class="text-2xl font-black text-amber-900 mt-1 block">{{ stats.new_inquiries }}</span>
          </div>
          <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span class="text-[11px] text-slate-400 font-bold uppercase tracking-wider block">Submitted Apps</span>
            <span class="text-2xl font-black text-slate-900 mt-1 block">{{ stats.total_applications }}</span>
          </div>
          <div class="bg-white p-4 rounded-xl border border-emerald-200 bg-emerald-50/40 shadow-sm">
            <span class="text-[11px] text-emerald-800 font-bold uppercase tracking-wider block">Qualified</span>
            <span class="text-2xl font-black text-emerald-900 mt-1 block">{{ stats.qualified_applications }}</span>
          </div>
          <div class="bg-white p-4 rounded-xl border border-purple-200 bg-purple-50/40 shadow-sm">
            <span class="text-[11px] text-purple-800 font-bold uppercase tracking-wider block">Enrolled Paid</span>
            <span class="text-2xl font-black text-purple-900 mt-1 block">{{ stats.enrolled_applications }}</span>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-1.5 overflow-x-auto pb-1 sm:pb-0">
            <button 
              v-for="st in ['All', 'New', 'Contacted', 'Scheduled', 'Closed']"
              :key="st"
              @click="activeStatus = st; loadInquiries()"
              :class="activeStatus === st ? 'bg-apc-navy text-white font-bold' : 'bg-slate-50 text-slate-600 hover:bg-slate-100 font-medium'"
              class="text-xs px-3.5 py-1.5 rounded-lg transition-colors shrink-0"
            >
              {{ st }}
            </button>
          </div>

          <span class="text-xs text-slate-400 font-medium">
            Showing {{ inquiries.length }} prospective inquiry tickets
          </span>
        </div>

        <!-- Inquiries Table -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase tracking-wider">
                  <th class="p-4">Reference</th>
                  <th class="p-4">Applicant Name</th>
                  <th class="p-4">Program Interest</th>
                  <th class="p-4">Contact</th>
                  <th class="p-4">Consultation Mode</th>
                  <th class="p-4">Status</th>
                  <th class="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr 
                  v-for="inq in inquiries" 
                  :key="inq.inquiry_id"
                  @click="openInquiry(inq)"
                  class="hover:bg-amber-50/50 cursor-pointer transition-colors"
                >
                  <td class="p-4 font-mono font-bold text-apc-navy">
                    {{ inq.inquiry_id }}
                  </td>
                  <td class="p-4">
                    <span class="font-bold text-slate-900 block">{{ inq.first_name }} {{ inq.last_name }}</span>
                    <span class="text-[11px] text-slate-500">{{ inq.email }}</span>
                  </td>
                  <td class="p-4 font-semibold text-slate-800">
                    {{ inq.program_interest || 'General' }}
                  </td>
                  <td class="p-4 text-slate-600">
                    {{ inq.mobile }}
                  </td>
                  <td class="p-4 capitalize">
                    <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium text-[11px]">
                      {{ inq.visit_mode }}
                    </span>
                  </td>
                  <td class="p-4">
                    <StatusBadge :status="inq.status" />
                  </td>
                  <td class="p-4 text-right">
                    <button 
                      @click.stop="openInquiry(inq)"
                      class="text-xs font-bold text-apc-navy hover:text-apc-goldDark bg-slate-50 hover:bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 transition-colors"
                    >
                      Open CRM
                    </button>
                  </td>
                </tr>
                <tr v-if="!inquiries.length">
                  <td colspan="7" class="p-8 text-center text-slate-400">
                    No inquiries found matching this filter.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>

    <!-- Slide-over CRM Drawer Component -->
    <InquiryDrawer 
      v-if="selectedInquiry" 
      :inquiry="selectedInquiry"
      @close="selectedInquiry = null"
      @status-updated="handleStatusUpdated"
      @note-added="handleNoteAdded"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StaffSidebar from '../../components/staff/StaffSidebar.vue';
import StatusBadge from '../../components/common/StatusBadge.vue';
import InquiryDrawer from '../../components/staff/InquiryDrawer.vue';
import { api } from '../../api/client';
import { ExternalLink } from 'lucide-vue-next';

const inquiries = ref([]);
const activeStatus = ref('All');
const selectedInquiry = ref(null);
const stats = ref({
  total_inquiries: 0,
  new_inquiries: 0,
  total_applications: 0,
  qualified_applications: 0,
  enrolled_applications: 0
});

onMounted(() => {
  loadInquiries();
  loadStats();
});

async function loadInquiries() {
  inquiries.value = await api.getInquiries(activeStatus.value);
}

async function loadStats() {
  const inqs = await api.getInquiries('All');
  const apps = await api.getApplicants();
  stats.value = {
    total_inquiries: inqs.length,
    new_inquiries: inqs.filter(i => i.status === 'New').length,
    total_applications: apps.length,
    qualified_applications: apps.filter(a => a.status === 'Qualified').length,
    enrolled_applications: apps.filter(a => a.status === 'Enrolled').length
  };
}

function openInquiry(inq) {
  selectedInquiry.value = inq;
}

async function handleStatusUpdated({ inquiry_id, status }) {
  await api.updateInquiryStatus(inquiry_id, status);
  if (selectedInquiry.value && selectedInquiry.value.inquiry_id === inquiry_id) {
    selectedInquiry.value.status = status;
  }
  await loadInquiries();
  await loadStats();
}

async function handleNoteAdded({ inquiry_id, comment }) {
  const res = await api.addInquiryNote(inquiry_id, comment);
  if (selectedInquiry.value && selectedInquiry.value.inquiry_id === inquiry_id) {
    if (!selectedInquiry.value.notes) selectedInquiry.value.notes = [];
    selectedInquiry.value.notes.push(res.note);
  }
}
</script>
