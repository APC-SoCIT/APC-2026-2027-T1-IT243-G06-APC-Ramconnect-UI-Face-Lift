<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <label class="block text-sm font-bold text-slate-800">
          Target Academic Program / Course <span class="text-rose-600">*</span>
        </label>
        <p class="text-xs text-slate-500">
          Click a degree program to inspect career prospects and course specializations.
        </p>
      </div>
      <span v-if="selectedId" class="text-xs bg-amber-100 text-amber-900 font-bold px-2.5 py-1 rounded-md border border-amber-300">
        Selected: {{ selectedId }}
      </span>
    </div>

    <!-- Course Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
      <div 
        v-for="course in courses" 
        :key="course.id"
        @click="selectCourse(course.id)"
        :class="[
          'relative p-4 rounded-xl border-2 transition-all cursor-pointer text-left',
          selectedId === course.id 
            ? 'border-apc-gold bg-amber-50/60 shadow-md ring-2 ring-apc-gold/20' 
            : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm'
        ]"
      >
        <!-- Selection Check Icon -->
        <div class="flex items-start justify-between">
          <span class="text-xs font-black px-2 py-0.5 rounded bg-apc-navy text-white tracking-wide">
            {{ course.id }}
          </span>
          <div 
            :class="[
              'w-5 h-5 rounded-full flex items-center justify-center border transition-colors',
              selectedId === course.id ? 'bg-apc-gold border-apc-gold text-apc-navy' : 'border-slate-300'
            ]"
          >
            <Check v-if="selectedId === course.id" class="w-3.5 h-3.5 stroke-[3]" />
          </div>
        </div>

        <h4 class="mt-2.5 font-bold text-slate-900 text-sm leading-snug line-clamp-2">
          {{ course.name }}
        </h4>
        <p class="mt-1 text-xs text-slate-600 line-clamp-2">
          {{ course.description }}
        </p>

        <!-- Career Prospects Preview Button -->
        <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between">
          <span class="text-[11px] text-slate-400 font-medium">Quota: {{ course.quota || 100 }} slots</span>
          <button 
            type="button" 
            @click.stop="openPreview(course)"
            class="text-[11px] font-semibold text-apc-navy hover:text-apc-goldDark flex items-center space-x-1"
          >
            <span>Career Info</span>
            <Info class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Career Opportunities Modal (Progressive Disclosure) -->
    <div v-if="previewCourse" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 relative">
        <button 
          @click="previewCourse = null" 
          class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-full hover:bg-slate-100"
        >
          <X class="w-5 h-5" />
        </button>

        <div class="flex items-center space-x-2">
          <span class="text-xs font-black bg-apc-gold text-apc-navy px-2.5 py-1 rounded">
            {{ previewCourse.id }}
          </span>
          <span class="text-xs text-slate-500 font-medium">{{ previewCourse.level }}</span>
        </div>

        <h3 class="mt-2 font-bold text-lg text-slate-900">
          {{ previewCourse.name }}
        </h3>
        <p class="mt-2 text-xs text-slate-600 leading-relaxed">
          {{ previewCourse.description }}
        </p>

        <div class="mt-4 pt-4 border-t border-slate-100">
          <h4 class="text-xs font-bold uppercase tracking-wider text-apc-navy flex items-center space-x-1.5">
            <Briefcase class="w-3.5 h-3.5 text-apc-gold" />
            <span>Career Prospects & Industry Outcomes</span>
          </h4>
          <div class="mt-2.5 flex flex-wrap gap-1.5">
            <span 
              v-for="(job, idx) in previewCourse.outcomes" 
              :key="idx"
              class="text-xs bg-slate-100 text-slate-800 font-medium px-2.5 py-1 rounded-md border border-slate-200"
            >
              {{ job }}
            </span>
          </div>
        </div>

        <div class="mt-6 flex items-center justify-end space-x-3">
          <a 
            v-if="previewCourse.info_url"
            :href="previewCourse.info_url" 
            target="_blank" 
            class="text-xs text-slate-600 hover:text-apc-navy flex items-center space-x-1 font-semibold"
          >
            <span>Learn on apc.edu.ph</span>
            <ExternalLink class="w-3.5 h-3.5" />
          </a>
          <button 
            type="button" 
            @click="selectCourse(previewCourse.id); previewCourse = null"
            class="bg-apc-navy hover:bg-apc-navyLight text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors"
          >
            Select Program
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Check, Info, X, Briefcase, ExternalLink } from 'lucide-vue-next';

const props = defineProps({
  courses: {
    type: Array,
    required: true
  },
  modelValue: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);
const selectedId = ref(props.modelValue);
const previewCourse = ref(null);

function selectCourse(id) {
  selectedId.value = id;
  emit('update:modelValue', id);
}

function openPreview(course) {
  previewCourse.value = course;
}
</script>
