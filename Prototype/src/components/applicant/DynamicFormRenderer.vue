<template>
  <div class="space-y-8">
    <div 
      v-for="section in sections" 
      :key="section.section_id"
      class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 apc-card-shadow"
    >
      <!-- Section Header -->
      <div class="border-b border-slate-100 pb-4 mb-6">
        <h3 class="text-base sm:text-lg font-bold text-slate-900 flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-apc-gold"></span>
          <span>{{ section.title }}</span>
        </h3>
        <p v-if="section.description" class="text-xs text-slate-500 mt-1">
          {{ section.description }}
        </p>
      </div>

      <!-- Section Fields Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div 
          v-for="field in section.fields" 
          :key="field.formfield_id"
          :class="field.field_width === 'full' ? 'sm:col-span-2' : 'sm:col-span-1'"
          class="space-y-1.5"
        >
          <label :for="`field-${field.field_key}`" class="block text-xs font-bold text-slate-700">
            {{ field.label }}
            <span v-if="field.field_required" class="text-rose-600">*</span>
          </label>

          <!-- Select Field -->
          <div v-if="field.field_type === 'select'" class="relative">
            <select
              :id="`field-${field.field_key}`"
              :name="field.field_key"
              v-model="model[field.field_key]"
              :required="field.field_required"
              class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold focus:border-apc-gold outline-none transition-all"
            >
              <option value="" disabled>{{ field.field_placeholder || 'Select an option' }}</option>
              <option 
                v-for="(opt, oIdx) in field.field_options" 
                :key="oIdx" 
                :value="opt"
              >
                {{ opt }}
              </option>
            </select>
          </div>

          <!-- Date Field -->
          <input
            v-else-if="field.field_type === 'date'"
            :id="`field-${field.field_key}`"
            :name="field.field_key"
            type="date"
            v-model="model[field.field_key]"
            :autocomplete="autocompleteFor(field.field_key)"
            :required="field.field_required"
            class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold focus:border-apc-gold outline-none transition-all"
          />

          <!-- Textarea Field -->
          <textarea
            v-else-if="field.field_type === 'textarea'"
            :id="`field-${field.field_key}`"
            :name="field.field_key"
            v-model="model[field.field_key]"
            :required="field.field_required"
            :placeholder="field.field_placeholder"
            rows="3"
            class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold focus:border-apc-gold outline-none transition-all"
          ></textarea>

          <!-- Text/Email/Tel Input -->
          <input
            v-else
            :id="`field-${field.field_key}`"
            :name="field.field_key"
            :type="field.field_type || 'text'"
            v-model="model[field.field_key]"
            :autocomplete="autocompleteFor(field.field_key)"
            :spellcheck="field.field_type === 'email' ? 'false' : undefined"
            :autocapitalize="field.field_type === 'email' ? 'none' : undefined"
            :required="field.field_required"
            :placeholder="field.field_placeholder"
            class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg px-3.5 py-2.5 text-slate-900 focus:bg-white focus:ring-2 focus:ring-apc-gold focus:border-apc-gold outline-none transition-all"
          />

          <p v-if="field.field_help_text" class="text-[11px] text-slate-400">
            {{ field.field_help_text }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const AUTOCOMPLETE_MAP = {
  first_name: 'given-name',
  middle_name: 'additional-name',
  last_name: 'family-name',
  birth_date: 'bday',
  email: 'email',
  mobile: 'tel',
  home_address: 'street-address',
  city: 'address-level2',
  nationality: 'country-name'
};

function autocompleteFor(key) {
  return AUTOCOMPLETE_MAP[key] || 'off';
}

const props = defineProps({
  sections: {
    type: Array,
    required: true
  },
  model: {
    type: Object,
    required: true
  }
});
</script>
