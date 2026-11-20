<template>
  <div class="flex flex-col md:flex-row min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="bg-white border-b border-slate-200 px-4 sm:px-6 py-3.5 sm:py-4">
        <h1 class="text-base sm:text-xl font-bold text-slate-900">Academic Programs & Quotas</h1>
        <p class="text-[11px] sm:text-xs text-slate-500">Manage degree slot quotas, active intake status, and career prospects</p>
      </header>

      <main class="flex-1 p-6 space-y-6 overflow-y-auto max-w-5xl">
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-700">Offered Degree Programs</span>
            <span class="text-xs text-slate-500">Changes reflect immediately across applicant CoursePicker</span>
          </div>

          <div class="divide-y divide-slate-100">
            <div 
              v-for="prog in courses" 
              :key="prog.id"
              class="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div class="space-y-1 max-w-md">
                <div class="flex items-center space-x-2">
                  <span class="text-xs font-black bg-apc-navy text-white px-2 py-0.5 rounded font-mono">
                    {{ prog.id }}
                  </span>
                  <h3 class="font-bold text-sm text-slate-900">{{ prog.name }}</h3>
                </div>
                <p class="text-xs text-slate-500 leading-relaxed">{{ prog.description }}</p>

                <div class="flex flex-wrap gap-1 pt-1">
                  <span 
                    v-for="(job, jIdx) in prog.outcomes" 
                    :key="jIdx"
                    class="text-[10px] bg-slate-100 text-slate-700 font-semibold px-2 py-0.5 rounded"
                  >
                    {{ job }}
                  </span>
                </div>
              </div>

              <!-- Quota & Active Status Controls -->
              <div class="flex items-center space-x-4 self-end sm:self-center">
                <div class="text-right">
                  <label class="block text-[11px] text-slate-400 font-bold uppercase">Intake Quota</label>
                  <input 
                    type="number" 
                    v-model.number="prog.quota" 
                    @change="handleUpdate(prog)"
                    class="w-20 text-xs font-bold text-center border border-slate-300 rounded-lg px-2 py-1 bg-slate-50 focus:bg-white outline-none"
                  />
                </div>

                <div class="text-right">
                  <label class="block text-[11px] text-slate-400 font-bold uppercase">Accepting Apps</label>
                  <button 
                    @click="prog.active = !prog.active; handleUpdate(prog)"
                    :class="prog.active ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'"
                    class="text-xs font-bold px-3 py-1 rounded-lg transition-colors"
                  >
                    {{ prog.active ? 'Active' : 'Closed' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StaffSidebar from '../../components/staff/StaffSidebar.vue';
import { useSiteSettingsStore } from '../../stores/siteSettings';
import { api } from '../../api/client';

const siteStore = useSiteSettingsStore();
const courses = ref([]);

onMounted(async () => {
  await siteStore.fetchAll();
  courses.value = JSON.parse(JSON.stringify(siteStore.courses));
});

async function handleUpdate(prog) {
  await api.updateCourse(prog.id, prog);
}
</script>
