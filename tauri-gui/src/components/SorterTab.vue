<script setup>
import { ref, inject, computed, onMounted } from 'vue';
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-dialog';

const config = inject('config');

const sourceDir = ref('');
const targetDir = ref('');
const isDryRun = ref(true);

const isSorting = ref(false);
const sortStatus = ref('Готовий');
const statusColor = ref('text-emerald-400');

const metrics = ref({
  total: 0,
  organized: 0,
});

const logs = ref([
  { time: new Date().toLocaleTimeString(), type: 'info', message: 'FolderSorter готовий до прибирання.' }
]);


const activeCategoriesCount = computed(() => {
  return Object.keys(config.value.rules || {}).length;
});

const addLog = (message, type = 'dry') => {
  const time = new Date().toLocaleTimeString();
  logs.value.push({ time, type, message });
};

const clearLogs = () => {
  logs.value = [];
};

const browseSource = async () => {
  try {
    const selected = await open({
      directory: true,
      multiple: false,
      title: 'Виберіть вхідну папку для прибирання'
    });
    if (selected) {
      sourceDir.value = selected;
    }
  } catch (err) {
    addLog(`Помилка відкриття діалогу: ${err}`, 'error');
  }
};

const browseTarget = async () => {
  try {
    const selected = await open({
      directory: true,
      multiple: false,
      title: 'Виберіть папку призначення'
    });
    if (selected) {
      targetDir.value = selected;
    }
  } catch (err) {
    addLog(`Помилка відкриття діалогу: ${err}`, 'error');
  }
};

const startSorting = async () => {
  if (!sourceDir.value.trim()) {
    alert('Будь ласка, вкажіть вхідну папку!');
    return;
  }

  isSorting.value = true;
  sortStatus.value = 'Сортування...';
  statusColor.value = 'text-amber-400';

  addLog(`Розпочинаю прибирання папки: ${sourceDir.value} (Dry Run: ${isDryRun.value})`, 'info');

  try {
    const summary = await invoke('run_sorting', {
      sourceDir: sourceDir.value.trim(),
      targetDir: targetDir.value.trim(),
      dryRun: isDryRun.value,
    });

    metrics.value.total = summary.total_files;
    metrics.value.organized = summary.moved_files;

    if (summary.actions.length === 0) {
      addLog('У цій папці не знайдено відповідних файлів.', 'info');
    } else {
      summary.actions.forEach(action => {
        const type = action.status === 'moved' ? 'moved' : (action.status === 'error' ? 'error' : 'dry');
        addLog(`${action.file_name} ➔ [${action.category}] (${action.to_path})`, type);
      });
      addLog(`Прибирання завершено! Оброблено: ${summary.moved_files} з ${summary.total_files}`, 'info');
    }

    sortStatus.value = 'Завершено успішно';
    statusColor.value = 'text-emerald-400';
  } catch (err) {
    addLog(`Помилка виконання: ${err}`, 'error');
    sortStatus.value = 'Помилка';
    statusColor.value = 'text-rose-400';
  } finally {
    isSorting.value = false;
  }
};

onMounted(async () => {
  try {
    const defaultDownloads = await invoke('get_default_downloads_folder');
    if (defaultDownloads) {
      sourceDir.value = defaultDownloads;
    }
  } catch (e) {
    console.error(e);
  }
});
</script>

<template>
  <div class="flex flex-col gap-6 animate-fadeIn">
    <!-- Folder Selectors Glass Panel -->
    <div class="glass-panel p-5 rounded-2xl flex flex-col gap-4 shadow-xl">
      <div class="flex items-center justify-between border-b border-white/10 pb-3">
        <h2 class="text-sm font-semibold text-white flex items-center gap-2">
          <span>📁</span> Вибір каталогів для сортування
        </h2>
        <span class="text-xs text-gray-400 font-mono">Автоматичне сортування</span>

      </div>

      <!-- Source Directory Input -->
      <div class="flex flex-col gap-1.5">
        <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Вхідна папка (Джерело):</label>
        <div class="flex gap-2">
          <input
            v-model="sourceDir"
            type="text"
            placeholder="Виберіть папку для прибирання (наприклад, Завантаження)..."
            class="flex-1 glass-input rounded-xl px-3.5 py-2 text-xs text-white placeholder-gray-500 focus:outline-none select-text"
          />
          <button
            @click="browseSource"
            class="px-4 py-2 bg-white/10 hover:bg-white/15 border border-white/10 rounded-xl text-xs font-semibold text-white transition-all duration-200 flex items-center gap-1.5 active:scale-95"
          >
            <span>📂</span> Огляд
          </button>
        </div>
      </div>

      <!-- Target Directory Input -->
      <div class="flex flex-col gap-1.5">
        <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Папка призначення (Опціонально):</label>
        <div class="flex gap-2">
          <input
            v-model="targetDir"
            type="text"
            placeholder="Залиште порожнім для сортування у тій самій папці..."
            class="flex-1 glass-input rounded-xl px-3.5 py-2 text-xs text-white placeholder-gray-500 focus:outline-none select-text"
          />
          <button
            @click="browseTarget"
            class="px-4 py-2 bg-white/10 hover:bg-white/15 border border-white/10 rounded-xl text-xs font-semibold text-white transition-all duration-200 flex items-center gap-1.5 active:scale-95"
          >
            <span>📂</span> Огляд
          </button>
        </div>
      </div>

      <!-- Dry Run Options Toggle -->
      <div class="flex items-center gap-3 pt-2">
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="isDryRun" class="sr-only peer" />
          <div class="w-11 h-6 bg-white/10 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
          <span class="ml-3 text-xs font-medium text-gray-300">
            Режим перевірки (Dry Run) — не переміщувати файли фактично
          </span>
        </label>
      </div>
    </div>

    <!-- Metrics Cards Grid -->
    <div class="grid grid-cols-4 gap-4">
      <div class="glass-card p-4 rounded-xl flex flex-col justify-between">
        <span class="text-2xl font-bold text-white font-mono">{{ metrics.total }}</span>
        <span class="text-xs text-gray-400 font-medium">Знайдено файлів</span>
      </div>
      <div class="glass-card p-4 rounded-xl flex flex-col justify-between">
        <span class="text-2xl font-bold text-indigo-400 font-mono">{{ metrics.organized }}</span>
        <span class="text-xs text-gray-400 font-medium">Оброблено файлів</span>
      </div>
      <div class="glass-card p-4 rounded-xl flex flex-col justify-between">
        <span class="text-2xl font-bold text-purple-400 font-mono">{{ activeCategoriesCount }}</span>
        <span class="text-xs text-gray-400 font-medium">Активних категорій</span>
      </div>
      <div class="glass-card p-4 rounded-xl flex flex-col justify-between">
        <span :class="['text-base font-bold truncate', statusColor]">{{ sortStatus }}</span>
        <span class="text-xs text-gray-400 font-medium">Статус системи</span>
      </div>
    </div>

    <!-- Action Button -->
    <div class="flex justify-end">
      <button
        @click="startSorting"
        :disabled="isSorting"
        class="px-6 py-3.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 transition-all duration-200 flex items-center gap-2"
      >
        <span v-if="isSorting" class="animate-spin">⏳</span>
        <span v-else>🚀</span>
        <span>{{ isSorting ? 'Сортування...' : 'Почати прибирання' }}</span>
      </button>
    </div>

    <!-- Log Console Glass Panel -->
    <div class="glass-panel p-4 rounded-2xl flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-semibold text-gray-300 uppercase tracking-wider flex items-center gap-2">
          <span>🖥️</span> Консоль результатів
        </h3>
        <button
          @click="clearLogs"
          class="px-2.5 py-1 text-[11px] bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-gray-400 hover:text-white transition-all duration-150"
        >
          Очистити
        </button>
      </div>

      <div class="bg-[#07090e] border border-white/10 rounded-xl p-3.5 h-48 overflow-y-auto font-mono text-xs flex flex-col gap-2 select-text">
        <div v-for="(log, idx) in logs" :key="idx" class="flex gap-2.5 items-start leading-relaxed animate-fadeIn">
          <span class="text-gray-500 text-[11px]">[{{ log.time }}]</span>
          
          <span
            v-if="log.type === 'moved'"
            class="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold uppercase"
          >ПЕРЕМІЩЕНО</span>

          <span
            v-else-if="log.type === 'error'"
            class="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-bold uppercase"
          >ПОМИЛКА</span>

          <span
            v-else
            class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold uppercase"
          >DRY RUN</span>

          <span class="text-gray-200 flex-1">{{ log.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
