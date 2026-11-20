<template>
  <div class="flex min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">Applicant Dossier Evaluation</h1>
          <p class="text-xs text-slate-500">Review student credentials, verify requirements, and transition qualification standing</p>
        </div>
      </header>

      <main class="flex-1 p-6 space-y-6 overflow-y-auto">
        <!-- Search and Filter Bar -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="relative w-full sm:w-80">
            <Search class="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="loadApplicants"
              placeholder="Search by student name, email, or course..."
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg pl-9 pr-3 py-2 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <div class="flex items-center space-x-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
            <button 
              v-for="st in ['All', 'Submitted', 'Under Review', 'Incomplete Dossier', 'Qualified', 'Enrolled']"
              :key="st"
              @click="activeStatus = st; loadApplicants()"
              :class="activeStatus === st ? 'bg-apc-navy text-white font-bold' : 'bg-slate-50 text-slate-600 hover:bg-slate-100 font-medium'"
              class="text-xs px-3 py-1.5 rounded-lg transition-colors shrink-0"
            >
              {{ st }}
            </button>
          </div>
        </div>

        <!-- Applicants Table -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold uppercase tracking-wider">
                  <th class="p-4">App ID</th>
                  <th class="p-4">Applicant Name</th>
                  <th class="p-4">Program / Track</th>
                  <th class="p-4">Entry Status</th>
                  <th class="p-4">Previous School</th>
                  <th class="p-4">Status</th>
                  <th class="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr 
                  v-for="app in applicants" 
                  :key="app.appform_id"
                  @click="openDossier(app)"
                  class="hover:bg-amber-50/50 cursor-pointer transition-colors"
                >
                  <td class="p-4 font-mono font-bold text-apc-navy">
                    {{ app.appform_id }}
                  </td>
                  <td class="p-4">
                    <span class="font-bold text-slate-900 block">{{ app.first_name }} {{ app.last_name }}</span>
                    <span class="text-[11px] text-slate-500">{{ app.email }}</span>
                  </td>
                  <td class="p-4">
                    <span class="font-bold text-apc-navy block">{{ app.course_id }}</span>
                    <span class="text-[11px] text-slate-500 truncate max-w-[200px] block">{{ app.course_name }}</span>
                  </td>
                  <td class="p-4 text-slate-700">
                    {{ app.entry_status }}
                  </td>
                  <td class="p-4 text-slate-600 truncate max-w-[180px]">
                    {{ app.prev_school || 'N/A' }}
                  </td>
                  <td class="p-4">
                    <StatusBadge :status="app.status" />
                  </td>
                  <td class="p-4 text-right">
                    <button 
                      @click.stop="openDossier(app)"
                      class="text-xs font-bold text-apc-navy hover:text-apc-goldDark bg-slate-50 hover:bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 transition-colors"
                    >
                      Evaluate Dossier
                    </button>
                  </td>
                </tr>
                <tr v-if="!applicants.length">
                  <td colspan="7" class="p-8 text-center text-slate-400">
                    No applicants found matching this search or filter.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>

    <!-- Applicant Dossier Drawer Component -->
    <ApplicantDossierDrawer 
      v-if="selectedApplicant" 
      :applicant="selectedApplicant"
      @close="selectedApplicant = null"
      @status-updated="handleDossierUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StaffSidebar from '../../components/staff/StaffSidebar.vue';
import StatusBadge from '../../components/common/StatusBadge.vue';
import ApplicantDossierDrawer from '../../components/staff/ApplicantDossierDrawer.vue';
import { api } from '../../api/client';
import { Search } from 'lucide-vue-next';

const applicants = ref([]);
const searchQuery = ref('');
const activeStatus = ref('All');
const selectedApplicant = ref(null);

onMounted(() => {
  loadApplicants();
});

async function loadApplicants() {
  applicants.value = await api.getApplicants(searchQuery.value, activeStatus.value);
}

function openDossier(app) {
  selectedApplicant.value = app;
}

async function handleDossierUpdated({ appform_id, status, officer_notes }) {
  await api.updateApplicantStatus(appform_id, status, officer_notes);
  if (selectedApplicant.value && selectedApplicant.value.appform_id === appform_id) {
    selectedApplicant.value.status = status;
    selectedApplicant.value.officer_notes = officer_notes;
  }
  await loadApplicants();
}
</script>
