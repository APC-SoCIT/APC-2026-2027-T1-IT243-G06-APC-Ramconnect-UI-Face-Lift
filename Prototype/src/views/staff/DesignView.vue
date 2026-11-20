<template>
  <div class="flex min-h-screen bg-slate-100">
    <StaffSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">Site Designer & CMS Studio</h1>
          <p class="text-xs text-slate-500">Edit portal headlines, colors, announcements, and reservation fee with live device preview</p>
        </div>
        <button 
          @click="saveChanges" 
          :disabled="isSaving"
          class="text-xs bg-apc-gold hover:bg-apc-goldDark text-apc-navy font-bold px-5 py-2.5 rounded-lg shadow-sm flex items-center space-x-1.5 transition-colors disabled:opacity-50"
        >
          <Save class="w-4 h-4" />
          <span v-if="isSaving">Publishing...</span>
          <span v-else>Publish Changes Live</span>
        </button>
      </header>

      <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-y-auto">
        <!-- Editor Controls (Left 5 Cols) -->
        <div class="lg:col-span-5 space-y-6">
          <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 border-b border-slate-100 pb-2">
              Portal Headlines & Announcements
            </h3>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Hero Main Headline</label>
              <input 
                type="text" 
                v-model="settings.headline" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:bg-white outline-none"
              />
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Welcome Card Title</label>
              <input 
                type="text" 
                v-model="settings.welcome_title" 
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:bg-white outline-none"
              />
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Admission Announcement Copy</label>
              <textarea 
                v-model="settings.welcome_text" 
                rows="3"
                class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:bg-white outline-none"
              ></textarea>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Slot Reservation Fee (PHP)</label>
              <div class="relative">
                <span class="absolute left-3 top-2 text-xs font-bold text-slate-400">₱</span>
                <input 
                  type="number" 
                  v-model.number="settings.reservation_fee" 
                  class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg pl-7 pr-3 py-2 text-slate-900 font-bold focus:bg-white outline-none font-mono"
                />
              </div>
            </div>
          </div>

          <!-- Color Customizer -->
          <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 border-b border-slate-100 pb-2">
              APC Brand Palette (80% Gold, 20% Navy)
            </h3>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">APC Gold</label>
                <div class="flex items-center space-x-2">
                  <input type="color" v-model="settings.gold_color" class="w-8 h-8 rounded border border-slate-300 cursor-pointer" />
                  <input type="text" v-model="settings.gold_color" class="w-full text-xs font-mono uppercase bg-slate-50 border border-slate-300 rounded px-2 py-1" />
                </div>
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">APC Navy</label>
                <div class="flex items-center space-x-2">
                  <input type="color" v-model="settings.navy_color" class="w-8 h-8 rounded border border-slate-300 cursor-pointer" />
                  <input type="text" v-model="settings.navy_color" class="w-full text-xs font-mono uppercase bg-slate-50 border border-slate-300 rounded px-2 py-1" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Preview Frame (Right 7 Cols) -->
        <div class="lg:col-span-7 flex flex-col">
          <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex items-center justify-between mb-4">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Live Viewport Preview</span>
            <div class="flex items-center space-x-2 bg-slate-100 p-1 rounded-lg">
              <button 
                @click="previewMode = 'desktop'" 
                :class="previewMode === 'desktop' ? 'bg-white shadow-sm text-slate-900 font-bold' : 'text-slate-500'"
                class="text-xs px-3 py-1 rounded flex items-center space-x-1.5 transition-all"
              >
                <Monitor class="w-3.5 h-3.5" />
                <span>Desktop</span>
              </button>
              <button 
                @click="previewMode = 'mobile'" 
                :class="previewMode === 'mobile' ? 'bg-white shadow-sm text-slate-900 font-bold' : 'text-slate-500'"
                class="text-xs px-3 py-1 rounded flex items-center space-x-1.5 transition-all"
              >
                <Smartphone class="w-3.5 h-3.5" />
                <span>Mobile</span>
              </button>
            </div>
          </div>

          <!-- Preview Container -->
          <div class="flex-1 flex items-center justify-center bg-slate-200 rounded-2xl p-4 overflow-hidden min-h-[480px]">
            <div 
              :class="previewMode === 'mobile' ? 'w-[360px] h-[640px] rounded-3xl border-8 border-slate-800' : 'w-full h-full rounded-xl border border-slate-300'"
              class="bg-white shadow-2xl overflow-y-auto transform transition-all duration-300 flex flex-col"
            >
              <!-- Mini Header -->
              <div class="bg-apc-navy p-3 flex items-center justify-between text-white border-b border-white/10 shrink-0">
                <div class="flex items-center space-x-2">
                  <div class="w-6 h-6 rounded-full bg-apc-gold text-apc-navy flex items-center justify-center font-black text-[10px]">APC</div>
                  <span class="text-[11px] font-bold">RamConnect</span>
                </div>
                <span class="text-[10px] text-apc-gold font-mono font-bold">Preview</span>
              </div>

              <!-- Mini Hero -->
              <div class="p-5 apc-navy-gradient text-white space-y-3">
                <h2 class="text-sm sm:text-base font-extrabold leading-tight text-apc-gold">
                  {{ settings.headline }}
                </h2>
                <div class="bg-white text-slate-900 rounded-xl p-3 text-[11px] shadow">
                  <span class="font-bold block text-apc-navy">{{ settings.welcome_title }}</span>
                  <p class="text-slate-600 mt-1 leading-snug">{{ settings.welcome_text }}</p>
                  <div class="mt-2 text-right">
                    <span class="text-[10px] font-bold text-amber-900 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                      Fee: ₱{{ Number(settings.reservation_fee || 5000).toLocaleString() }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Mini Schedule -->
              <div class="p-4 bg-amber-50 border-b border-amber-200 text-center">
                <span class="text-[10px] font-bold uppercase text-amber-900">Admission Period AY 2026-2027</span>
                <p class="text-[11px] font-mono font-bold text-apc-navy mt-0.5">17 April – 15 May 2026</p>
              </div>

              <!-- Mini Promo -->
              <div class="p-4 space-y-2 text-xs flex-1">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Featured Grants</span>
                <div class="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                  <span class="font-bold text-slate-800 text-[11px] block">President's Scholarship</span>
                  <span class="text-[10px] text-slate-500">100% full tuition support</span>
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
import { reactive, ref, onMounted } from 'vue';
import StaffSidebar from '../../components/staff/StaffSidebar.vue';
import { useSiteSettingsStore } from '../../stores/siteSettings';
import { api } from '../../api/client';
import { Save, Monitor, Smartphone } from 'lucide-vue-next';

const siteStore = useSiteSettingsStore();
const previewMode = ref('desktop');
const isSaving = ref(false);

const settings = reactive({
  headline: '',
  welcome_title: '',
  welcome_text: '',
  reservation_fee: 5000.00,
  gold_color: '#FDB813',
  navy_color: '#0B1E3D'
});

onMounted(async () => {
  await siteStore.fetchAll();
  Object.assign(settings, siteStore.settings);
});

async function saveChanges() {
  isSaving.value = true;
  try {
    await api.saveSiteSettings(settings);
    await siteStore.updateSettings(settings);
    alert("Site branding and settings published successfully!");
  } catch (e) {
    alert("Failed to save settings.");
  } finally {
    isSaving.value = false;
  }
}
</script>
