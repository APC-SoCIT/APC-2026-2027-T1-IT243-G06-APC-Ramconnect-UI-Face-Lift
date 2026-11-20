<template>
  <span :class="badgeClasses" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold shadow-sm">
    <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="dotClasses"></span>
    {{ status }}
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  status: {
    type: String,
    default: 'Submitted'
  }
});

const badgeClasses = computed(() => {
  switch (props.status) {
    case 'Qualified':
      return 'bg-emerald-50 text-emerald-800 border border-emerald-300';
    case 'Enrolled':
      return 'bg-amber-100 text-amber-900 border border-amber-400 font-bold';
    case 'Under Review':
      return 'bg-blue-50 text-blue-800 border border-blue-200';
    case 'Incomplete Dossier':
      return 'bg-orange-50 text-orange-800 border border-orange-300';
    case 'Rejected':
      return 'bg-rose-50 text-rose-800 border border-rose-300';
    case 'Contacted':
      return 'bg-cyan-50 text-cyan-800 border border-cyan-200';
    case 'Scheduled':
      return 'bg-purple-50 text-purple-800 border border-purple-200';
    case 'Closed':
      return 'bg-slate-100 text-slate-700 border border-slate-300';
    case 'New':
    case 'Submitted':
    default:
      return 'bg-indigo-50 text-indigo-800 border border-indigo-200';
  }
});

const dotClasses = computed(() => {
  switch (props.status) {
    case 'Qualified': return 'bg-emerald-500';
    case 'Enrolled': return 'bg-amber-500 animate-pulse';
    case 'Under Review': return 'bg-blue-500';
    case 'Incomplete Dossier': return 'bg-orange-500';
    case 'Rejected': return 'bg-rose-500';
    case 'Contacted': return 'bg-cyan-500';
    case 'Scheduled': return 'bg-purple-500';
    case 'Closed': return 'bg-slate-400';
    case 'New':
    case 'Submitted':
    default: return 'bg-indigo-500';
  }
});
</script>
