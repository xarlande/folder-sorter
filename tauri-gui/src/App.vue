<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { TabType } from './types/sorter';
import { createConfigStore } from './composables/useConfig';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, Sliders, Clock, Settings, FolderSync } from '@lucide/vue';

import SorterTab from './components/SorterTab.vue';
import RulesTab from './components/RulesTab.vue';
import SchedulerTab from './components/SchedulerTab.vue';
import SettingsTab from './components/SettingsTab.vue';

const activeTab = ref<TabType>('sorter');
const { loadConfig } = createConfigStore();

onMounted(() => {
  loadConfig();
});
</script>

<template>
  <div class="flex flex-col h-screen w-screen overflow-hidden select-none bg-background text-foreground">
    <!-- Top Bar Navigation Header -->
    <header class="flex items-center justify-between px-6 py-3 border-b border-border bg-card/60 backdrop-blur-md z-50">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-primary/10 border border-primary/20 text-primary flex items-center justify-center shadow-sm">
          <FolderSync class="w-5 h-5" />
        </div>
        <div>
          <h1 class="font-bold text-base tracking-tight text-foreground">
            FolderSorter
          </h1>
          <div class="text-[10px] text-muted-foreground font-mono tracking-wide uppercase font-medium">
            Автоматичне прибирання
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <Tabs v-model="activeTab" class="w-auto">
        <TabsList class="grid grid-cols-4 bg-muted/60 p-1 border border-border/50 rounded-xl">
          <TabsTrigger value="sorter" class="flex items-center gap-2 text-xs font-medium transition-all">
            <Sparkles class="w-3.5 h-3.5" />
            <span>Сортування</span>
          </TabsTrigger>

          <TabsTrigger value="rules" class="flex items-center gap-2 text-xs font-medium transition-all">
            <Sliders class="w-3.5 h-3.5" />
            <span>Правила</span>
          </TabsTrigger>

          <TabsTrigger value="scheduler" class="flex items-center gap-2 text-xs font-medium transition-all">
            <Clock class="w-3.5 h-3.5" />
            <span>Планувальник</span>
          </TabsTrigger>

          <TabsTrigger value="settings" class="flex items-center gap-2 text-xs font-medium transition-all">
            <Settings class="w-3.5 h-3.5" />
            <span>Налаштування</span>
          </TabsTrigger>
        </TabsList>
      </Tabs>
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

