<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-sm animate-fade-in">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 relative">
      <button 
        @click="$emit('close')" 
        class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-full hover:bg-slate-100"
      >
        <X class="w-5 h-5" />
      </button>

      <!-- Modal Header -->
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center">
          <CreditCard class="w-5 h-5" />
        </div>
        <div>
          <h3 class="font-bold text-base text-slate-900">Settle Reservation Fee</h3>
          <p class="text-xs text-slate-500">Secure your academic slot at Asia Pacific College</p>
        </div>
      </div>

      <!-- Fee Box -->
      <div class="mt-5 p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-between">
        <div>
          <span class="text-xs text-amber-900 font-medium block">Total Payable Amount</span>
          <span class="text-xs text-slate-500">Official Slot Reservation Fee</span>
        </div>
        <span class="text-xl font-extrabold text-amber-950 font-mono">
          ₱{{ Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
        </span>
      </div>

      <form @submit.prevent="handleSubmit" class="mt-5 space-y-4">
        <!-- Payment Method -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Payment Channel</label>
          <select 
            v-model="form.bank" 
            required 
            class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-apc-gold outline-none"
          >
            <option value="BDO Unibank (Online Bills Payment)">BDO Unibank (Online Bills Payment)</option>
            <option value="Land Bank of the Philippines">Land Bank of the Philippines</option>
            <option value="GCash / Maya (e-Wallet Transfer)">GCash / Maya (e-Wallet Transfer)</option>
            <option value="BPI Express Online">BPI Express Online</option>
            <option value="SM Bills Payment Counter">SM Bills Payment Counter</option>
          </select>
        </div>

        <!-- Account / Sender Name -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Account Holder / Remitter Name</label>
          <input 
            type="text" 
            v-model="form.account_name" 
            required 
            placeholder="e.g. Juan Dela Cruz" 
            class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:ring-2 focus:ring-apc-gold outline-none"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <!-- Last 4 Digits -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Last 4 Digits / Suffix</label>
            <input 
              type="text" 
              v-model="form.account_last4" 
              required 
              maxlength="4" 
              placeholder="e.g. 4821" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>

          <!-- Reference Number -->
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Bank Reference No.</label>
            <input 
              type="text" 
              v-model="form.reference_number" 
              required 
              placeholder="e.g. REF-983142" 
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:ring-2 focus:ring-apc-gold outline-none"
            />
          </div>
        </div>

        <p class="text-[11px] text-slate-400 leading-snug">
          Payments are electronically validated against the APC finance clearing ledger. An official student confirmation packet will be issued upon processing.
        </p>

        <!-- Submit Buttons -->
        <div class="pt-2 flex items-center justify-end space-x-3">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 rounded-lg"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-5 py-2.5 rounded-lg transition-colors shadow-md disabled:opacity-50 flex items-center space-x-1.5"
          >
            <span v-if="isSubmitting">Processing Payment...</span>
            <span v-else>Confirm & Pay ₱{{ Number(amount).toLocaleString() }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { X, CreditCard } from 'lucide-vue-next';

const props = defineProps({
  amount: {
    type: Number,
    default: 5000.00
  }
});

const emit = defineEmits(['close', 'paid']);
const isSubmitting = ref(false);

const form = reactive({
  bank: 'BDO Unibank (Online Bills Payment)',
  account_name: '',
  account_last4: '',
  reference_number: ''
});

async function handleSubmit() {
  isSubmitting.value = true;
  try {
    emit('paid', {
      bank: form.bank,
      account_name: form.account_name,
      account_last4: form.account_last4,
      reference_number: form.reference_number,
      amount: props.amount
    });
  } finally {
    isSubmitting.value = false;
  }
}
</script>
