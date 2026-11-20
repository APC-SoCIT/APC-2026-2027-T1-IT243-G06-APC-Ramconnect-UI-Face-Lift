<template>
  <div class="flex min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">Admission Form Builder</h1>
          <p class="text-xs text-slate-500">Dynamically configure intake sections and questions without writing code</p>
        </div>
        <div class="flex items-center space-x-3">
          <button 
            @click="addSection" 
            class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-2 rounded-lg flex items-center space-x-1.5 transition-colors"
          >
            <Plus class="w-4 h-4" />
            <span>Add Section</span>
          </button>
          <button 
            @click="publishForm" 
            :disabled="isSaving"
            class="text-xs bg-apc-gold hover:bg-apc-goldDark text-apc-navy font-bold px-5 py-2 rounded-lg shadow-sm flex items-center space-x-1.5 transition-colors disabled:opacity-50"
          >
            <Save class="w-4 h-4" />
            <span v-if="isSaving">Publishing...</span>
            <span v-else>Save & Publish Changes</span>
          </button>
        </div>
      </header>

      <main class="flex-1 p-6 space-y-6 overflow-y-auto max-w-5xl">
        <!-- Notification toast -->
        <div v-if="successMsg" class="p-3 bg-emerald-50 border border-emerald-300 rounded-xl text-emerald-800 text-xs font-bold flex items-center justify-between">
          <span>{{ successMsg }}</span>
          <button @click="successMsg = ''" class="text-emerald-700 hover:text-emerald-900"><X class="w-4 h-4" /></button>
        </div>

        <!-- Sections List -->
        <div 
          v-for="(sec, sIdx) in sections" 
          :key="sec.section_id || sIdx"
          class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden"
        >
          <!-- Section Header / Controls -->
          <div class="p-5 bg-slate-50/80 border-b border-slate-200 flex items-center justify-between">
            <div class="flex-1 max-w-lg mr-4">
              <input 
                type="text" 
                v-model="sec.title" 
                class="font-bold text-slate-900 text-sm bg-transparent border-b border-transparent hover:border-slate-300 focus:border-apc-gold focus:bg-white px-1.5 py-0.5 rounded outline-none w-full"
                placeholder="Section Title..."
              />
              <input 
                type="text" 
                v-model="sec.description" 
                class="text-xs text-slate-500 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-apc-gold focus:bg-white px-1.5 py-0.5 rounded outline-none w-full mt-1"
                placeholder="Section guidance description..."
              />
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="addField(sIdx)"
                class="text-xs bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold px-2.5 py-1.5 rounded-lg flex items-center space-x-1"
              >
                <Plus class="w-3.5 h-3.5" />
                <span>Add Question</span>
              </button>
              <button 
                @click="removeSection(sIdx)" 
                class="text-slate-400 hover:text-rose-600 p-1.5 rounded"
                title="Remove Section"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Section Fields Table -->
          <div class="divide-y divide-slate-100">
            <div 
              v-for="(field, fIdx) in sec.fields" 
              :key="field.formfield_id || fIdx"
              class="p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-slate-50/50"
            >
              <div class="flex items-center space-x-3 flex-1">
                <span v-if="field.field_locked" class="p-1.5 bg-slate-100 text-slate-500 rounded" title="Core Required Field">
                  <Lock class="w-3.5 h-3.5" />
                </span>
                <span v-else class="text-slate-300 cursor-move">
                  <GripVertical class="w-4 h-4" />
                </span>

                <div class="flex-1 space-y-1">
                  <input 
                    type="text" 
                    v-model="field.label" 
                    class="font-semibold text-xs text-slate-800 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-apc-gold px-1 rounded outline-none w-full"
                  />
                  <div class="flex items-center space-x-3 text-[11px] text-slate-400">
                    <span>Key: <code class="bg-slate-100 px-1 rounded text-slate-600">{{ field.field_key }}</code></span>
                    <span>Type: <strong>{{ field.field_type }}</strong></span>
                  </div>
                </div>
              </div>

              <!-- Field Type & Option Controls -->
              <div class="flex items-center space-x-2">
                <select 
                  v-model="field.field_type" 
                  class="text-xs bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 text-slate-700 outline-none"
                >
                  <option value="text">Short Text</option>
                  <option value="email">Email</option>
                  <option value="tel">Phone / Tel</option>
                  <option value="select">Dropdown Select</option>
                  <option value="date">Date</option>
                  <option value="textarea">Long Textarea</option>
                </select>

                <label class="flex items-center space-x-1 text-xs text-slate-600 cursor-pointer">
                  <input type="checkbox" v-model="field.field_required" class="rounded border-slate-300 text-apc-navy" />
                  <span>Required</span>
                </label>

                <button 
                  v-if="!field.field_locked" 
                  @click="removeField(sIdx, fIdx)"
                  class="text-slate-400 hover:text-rose-600 p-1.5"
                  title="Remove Field"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
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
import { Plus, Save, Trash2, Lock, GripVertical, X } from 'lucide-vue-next';

const siteStore = useSiteSettingsStore();
const sections = ref([]);
const isSaving = ref(false);
const successMsg = ref('');

onMounted(async () => {
  await siteStore.fetchAll();
  sections.value = JSON.parse(JSON.stringify(siteStore.formSections));
});

function addSection() {
  sections.value.push({
    section_id: 'sec-' + Date.now(),
    title: 'New Information Section',
    description: 'Add instructions for applicants',
    sort_order: sections.value.length + 1,
    fields: []
  });
}

function removeSection(sIdx) {
  if (confirm("Remove this section and all its questions?")) {
    sections.value.splice(sIdx, 1);
  }
}

function addField(sIdx) {
  const count = sections.value[sIdx].fields.length + 1;
  sections.value[sIdx].fields.push({
    formfield_id: 'field-' + Date.now(),
    label: `Custom Question ${count}`,
    field_key: `custom_field_${count}`,
    field_type: 'text',
    field_options: [],
    field_required: false,
    field_help_text: '',
    field_placeholder: '',
    field_width: 'half',
    field_sort_order: count,
    field_locked: false
  });
}

function removeField(sIdx, fIdx) {
  sections.value[sIdx].fields.splice(fIdx, 1);
}

async function publishForm() {
  isSaving.value = true;
  try {
    await api.saveFormSections(sections.value);
    await siteStore.updateFormSections(sections.value);
    successMsg.value = 'Form published successfully! New schema will reflect on /apply immediately.';
    setTimeout(() => { successMsg.value = ''; }, 4000);
  } catch (e) {
    alert("Failed to publish form.");
  } finally {
    isSaving.value = false;
  }
}
</script>
