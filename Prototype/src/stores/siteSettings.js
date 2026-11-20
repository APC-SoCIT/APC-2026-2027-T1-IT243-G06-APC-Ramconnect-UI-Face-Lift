import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '../api/client';

export const useSiteSettingsStore = defineStore('siteSettings', () => {
  const settings = ref({});
  const courses = ref([]);
  const milestones = ref([]);
  const promos = ref([]);
  const formSections = ref([]);
  const isLoading = ref(true);

  async function fetchAll() {
    isLoading.value = true;
    try {
      const [s, c, m, p, f] = await Promise.all([
        api.getSettings(),
        api.getCourses(),
        api.getMilestones(),
        api.getPromos(),
        api.getFormSchema()
      ]);
      settings.value = s;
      courses.value = c;
      milestones.value = m;
      promos.value = p;
      formSections.value = f;
    } catch (e) {
      console.error("Error loading site settings", e);
    } finally {
      isLoading.value = false;
    }
  }

  async function updateSettings(newSettings) {
    settings.value = { ...settings.value, ...newSettings };
    await api.saveSiteSettings(settings.value);
  }

  async function updateFormSections(newSections) {
    formSections.value = newSections;
    await api.saveFormSections(newSections);
  }

  return {
    settings,
    courses,
    milestones,
    promos,
    formSections,
    isLoading,
    fetchAll,
    updateSettings,
    updateFormSections
  };
});
