<template>
  <div class="flex flex-col md:flex-row min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="bg-white border-b border-slate-200 px-4 sm:px-6 py-3.5 sm:py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 class="text-base sm:text-xl font-bold text-slate-900 leading-snug">Applicant Dossier Evaluation</h1>
          <p class="text-[11px] sm:text-xs text-slate-500 mt-0.5">Review student credentials, verify requirements, and transition qualification standing</p>
        </div>
      </header>

      <main class="flex-1 p-3.5 sm:p-6 space-y-4 sm:space-y-6 overflow-y-auto">
        <!-- Search and Filter Bar -->
        <div class="bg-white p-3.5 sm:p-4 rounded-xl sm:rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          <div class="relative w-full md:w-80">
            <Search class="w-4 h-4 absolute left-3.5 top-2.5 text-slate-400" />
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="loadApplicants"
              placeholder="Search by student name, email, or course..."
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg pl-9 pr-3 py-2 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <!-- Wrapped Filter Pills (zero horizontal scrollbar) -->
          <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
            <button 
              v-for="st in ['All', 'Submitted', 'Under Review', 'Incomplete Dossier', 'Qualified', 'Enrolled']"
              :key="st"
              @click="activeStatus = st; loadApplicants()"
              :class="activeStatus === st ? 'bg-apc-navy text-white font-bold shadow-sm' : 'bg-slate-50 text-slate-600 hover:bg-slate-100 font-medium border border-slate-200'"
              class="text-xs px-2.5 sm:px-3 py-1.5 rounded-lg transition-colors"
            >
              {{ st }}
            </button>
          </div>
        </div>

        <!-- Applicants Container -->
        <div class="bg-white rounded-xl sm:rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <!-- Mobile Cards View (Visible on < sm) -->
          <div class="sm:hidden divide-y divide-slate-100">
            <div 
              v-for="app in applicants" 
              :key="'m-app-' + app.appform_id"
              @click="openDossier(app)"
              class="p-4 space-y-2.5 hover:bg-amber-50/40 active:bg-amber-100/50 cursor-pointer transition-colors"
            >
              <div class="flex items-center justify-between">
                <span class="font-mono font-bold text-xs text-apc-navy bg-slate-100 px-2 py-0.5 rounded">
                  {{ app.appform_id }}
                </span>
                <StatusBadge :status="app.status" />
              </div>

              <div>
                <h4 class="font-bold text-sm text-slate-900">{{ app.first_name }} {{ app.last_name }}</h4>
                <p class="text-xs text-slate-500">{{ app.email }} • {{ app.entry_status }}</p>
              </div>

              <div class="p-2.5 bg-slate-50 rounded-lg border border-slate-100 text-xs">
                <span class="font-bold text-apc-navy block">{{ app.course_id }}</span>
                <span class="text-[11px] text-slate-600 block truncate">{{ app.course_name }}</span>
              </div>

              <div class="flex items-center justify-between pt-1">
                <span class="text-[11px] text-slate-400 truncate max-w-[180px]">{{ app.prev_school || 'School unlisted' }}</span>
                <button 
                  @click.stop="openDossier(app)"
                  class="font-bold text-xs text-apc-navy hover:text-apc-goldDark bg-slate-100 px-3 py-1 rounded-md"
                >
                  Evaluate →
                </button>
              </div>
            </div>

            <div v-if="!applicants.length" class="p-8 text-center text-xs text-slate-400">
              No applicants found matching this filter.
            </div>
          </div>

          <!-- Desktop / Tablet Table View (Visible on sm+) -->
          <div class="hidden sm:block overflow-x-auto">
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
