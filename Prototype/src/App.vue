<template>
  <div class="min-h-screen flex flex-col font-sans">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useSiteSettingsStore } from './stores/siteSettings';

const siteStore = useSiteSettingsStore();

onMounted(() => {
  siteStore.fetchAll();
});
</script>
