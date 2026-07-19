<script setup>
import { ref, onMounted, provide } from 'vue';
import { invoke } from '@tauri-apps/api/core';

import SorterTab from './components/SorterTab.vue';
import RulesTab from './components/RulesTab.vue';
import SchedulerTab from './components/SchedulerTab.vue';
import SettingsTab from './components/SettingsTab.vue';

const activeTab = ref('sorter');
const config = ref({ rules: {} });
const isLoadingConfig = ref(true);

const loadConfig = async () => {
  try {
    isLoadingConfig.value = true;
    config.value = await invoke('get_config');
  } catch (err) {
    console.error('Помилка завантаження конфігурації:', err);
  } finally {
    isLoadingConfig.value = false;
  }
};

const saveConfig = async () => {
  try {
    await invoke('save_config', { config: config.value });
    return true;
  } catch (err) {
    console.error('Помилка збереження конфігурації:', err);
    throw err;
  }
};

provide('config', config);
provide('loadConfig', loadConfig);
provide('saveConfig', saveConfig);

onMounted(() => {
  loadConfig();
});
</script>

<template>
  <div class="flex flex-col h-screen overflow-hidden select-none bg-[#0b0d14]">
    <!-- Top Bar Navigation Header -->
    <header class="flex items-center justify-between px-6 py-3.5 bg-[#0b0d14]/90 backdrop-blur-md border-b border-white/10 z-50">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center text-xl shadow-lg shadow-indigo-500/30">
          📁
        </div>
        <div>
          <h1 class="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
            FolderSorter
          </h1>
          <div class="text-[10px] text-indigo-400 font-mono tracking-wide uppercase font-semibold">Автоматичне прибирання</div>

        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex p-1 gap-1 bg-white/5 border border-white/10 rounded-xl">
        <button
          @click="activeTab = 'sorter'"
          :class="[
            'px-4 py-2 text-xs font-medium rounded-lg transition-all duration-200 flex items-center gap-2',
            activeTab === 'sorter'
              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-500/50'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span>⚡</span> Сортування
        </button>

        <button
          @click="activeTab = 'rules'"
          :class="[
            'px-4 py-2 text-xs font-medium rounded-lg transition-all duration-200 flex items-center gap-2',
            activeTab === 'rules'
              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-500/50'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span>🎯</span> Правила
        </button>

        <button
          @click="activeTab = 'scheduler'"
          :class="[
            'px-4 py-2 text-xs font-medium rounded-lg transition-all duration-200 flex items-center gap-2',
            activeTab === 'scheduler'
              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-500/50'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span>⏰</span> Планувальник
        </button>

        <button
          @click="activeTab = 'settings'"
          :class="[
            'px-4 py-2 text-xs font-medium rounded-lg transition-all duration-200 flex items-center gap-2',
            activeTab === 'settings'
              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-500/50'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span>⚙️</span> Налаштування
        </button>
      </nav>
    </header>

    <!-- Main Dynamic Content Container -->
    <main class="flex-1 p-6 overflow-y-auto">
      <keep-alive>
        <SorterTab v-if="activeTab === 'sorter'" />
        <RulesTab v-else-if="activeTab === 'rules'" />
        <SchedulerTab v-else-if="activeTab === 'scheduler'" />
        <SettingsTab v-else-if="activeTab === 'settings'" />
      </keep-alive>
    </main>
  </div>
</template>
