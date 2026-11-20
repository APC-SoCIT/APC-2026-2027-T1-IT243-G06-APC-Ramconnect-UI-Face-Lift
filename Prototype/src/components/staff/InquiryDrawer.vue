<template>
  <div class="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-sm flex justify-end animate-fade-in">
    <div class="w-full max-w-xl bg-white shadow-2xl flex flex-col h-full transform transition-transform">
      <!-- Drawer Header -->
      <div class="p-6 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div>
          <div class="flex items-center space-x-2">
            <span class="text-xs font-mono font-bold bg-apc-navy text-white px-2 py-0.5 rounded">
              {{ inquiry.inquiry_id }}
            </span>
            <StatusBadge :status="inquiry.status" />
          </div>
          <h3 class="mt-2 text-lg font-bold text-slate-900">
            {{ inquiry.first_name }} {{ inquiry.last_name }}
          </h3>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600 p-2 rounded-full hover:bg-slate-200">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Drawer Content -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- Status Action Card -->
        <div class="p-4 rounded-xl bg-amber-50 border border-amber-200">
          <label class="block text-xs font-bold text-amber-950 mb-1.5 uppercase tracking-wide">
            Update Inquiry Pipeline Status
          </label>
          <div class="flex items-center space-x-2">
            <select 
              v-model="currentStatus" 
              class="flex-1 text-xs bg-white border border-amber-300 rounded-lg px-3 py-2 text-slate-900 font-semibold focus:ring-2 focus:ring-apc-gold outline-none"
            >
              <option value="New">New</option>
              <option value="Contacted">Contacted</option>
              <option value="Scheduled">Scheduled (On-Campus)</option>
              <option value="Closed">Closed / Converted</option>
            </select>
            <button 
              @click="handleStatusUpdate" 
              :disabled="isUpdating"
              class="bg-apc-navy hover:bg-apc-navyLight text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors shadow disabled:opacity-50"
            >
              Save Status
            </button>
          </div>
        </div>

        <!-- Contact Information -->
        <div>
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Applicant & Inquiry Details</h4>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Email Address</span>
              <span class="font-semibold text-slate-800 break-all">{{ inquiry.email }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Mobile Phone</span>
              <span class="font-semibold text-slate-800">{{ inquiry.mobile }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Program of Interest</span>
              <span class="font-bold text-apc-navy">{{ inquiry.program_interest || 'General Admissions' }}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Visit Preference</span>
              <span class="font-semibold text-slate-800 capitalize">{{ inquiry.visit_mode }} ({{ inquiry.preferred_date || 'TBD' }})</span>
            </div>
            <div v-if="inquiry.guardian_name" class="col-span-2 p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span class="text-slate-400 block text-[11px]">Parent / Guardian Contact</span>
              <span class="font-semibold text-slate-800">{{ inquiry.guardian_name }} ({{ inquiry.guardian_contact || 'No phone provided' }})</span>
            </div>
          </div>
        </div>

        <!-- Inquiry Question -->
        <div>
          <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Prospective Inquiry Message</h4>
          <div class="p-4 bg-slate-100 rounded-xl text-xs text-slate-800 leading-relaxed border border-slate-200">
            {{ inquiry.question }}
          </div>
        </div>

        <!-- CRM Interaction History & Notes -->
        <div class="pt-4 border-t border-slate-200">
          <h4 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center space-x-1.5">
            <MessageSquare class="w-4 h-4 text-apc-gold" />
            <span>Admissions Officer CRM Notes</span>
          </h4>

          <!-- Note Form -->
          <div class="space-y-2 mb-4">
            <textarea
              v-model="newNote"
              rows="3"
              placeholder="Log phone call outcome, email correspondence, or campus tour notes..."
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-3 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold outline-none"
            ></textarea>
            <div class="flex justify-end">
              <button
                @click="handleAddNote"
                :disabled="!newNote.trim() || isAddingNote"
                class="bg-apc-gold hover:bg-apc-goldDark text-apc-navy font-bold text-xs px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
              >
                Log Interaction Note
              </button>
            </div>
          </div>

          <!-- Note Timeline -->
          <div v-if="inquiry.notes && inquiry.notes.length" class="space-y-2.5">
            <div 
              v-for="note in inquiry.notes" 
              :key="note.note_id"
              class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs"
            >
              <div class="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                <span class="font-bold text-slate-700">{{ note.author_name }}</span>
                <span>{{ formatDate(note.created_at) }}</span>
              </div>
              <p class="text-slate-800 whitespace-pre-wrap">{{ note.comment }}</p>
            </div>
          </div>
          <div v-else class="text-center py-6 text-xs text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200">
            No officer interaction notes logged yet.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import StatusBadge from '../common/StatusBadge.vue';
import { X, MessageSquare } from 'lucide-vue-next';

const props = defineProps({
  inquiry: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'status-updated', 'note-added']);

const currentStatus = ref(props.inquiry.status);
const newNote = ref('');
const isUpdating = ref(false);
const isAddingNote = ref(false);

function handleStatusUpdate() {
  emit('status-updated', {
    inquiry_id: props.inquiry.inquiry_id,
    status: currentStatus.value
  });
}

function handleAddNote() {
  if (!newNote.value.trim()) return;
  emit('note-added', {
    inquiry_id: props.inquiry.inquiry_id,
    comment: newNote.value.trim()
  });
  newNote.value = '';
}

function formatDate(isoStr) {
  if (!isoStr) return '';
  return new Date(isoStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
</script>
