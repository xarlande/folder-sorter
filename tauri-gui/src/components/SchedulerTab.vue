<script setup>
import { ref } from 'vue';

const isSchedulerEnabled = ref(false);
const selectedInterval = ref('60');
</script>

<template>
  <div class="flex flex-col gap-6 animate-fadeIn">
    <div class="glass-panel p-5 rounded-2xl flex flex-col gap-5 shadow-xl">
      <div class="border-b border-white/10 pb-4">
        <h2 class="text-sm font-semibold text-white flex items-center gap-2">
          <span>⏰</span> Автоматичне сортування за розкладом
        </h2>
        <p class="text-xs text-gray-400 mt-1">
          Налаштуйте системний фоновий розклад для автоматичного впорядкування файлів.
        </p>
      </div>

      <!-- Toggle Switch -->
      <div class="flex items-center gap-3">
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="isSchedulerEnabled" class="sr-only peer" />
          <div class="w-11 h-6 bg-white/10 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
          <span class="ml-3 text-xs font-semibold text-white">
            Увімкнути фоновий розклад
          </span>
        </label>
      </div>

      <!-- Interval Selector -->
      <div class="flex flex-col gap-2 max-w-xs">
        <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Інтервал запуску:</label>
        <select
          v-model="selectedInterval"
          class="glass-input rounded-xl px-3.5 py-2 text-xs text-white bg-[#0d111c] focus:outline-none"
        >
          <option value="15">Кожні 15 хвилин</option>
          <option value="30">Кожні 30 хвилин</option>
          <option value="60">Щогодини</option>
          <option value="360">Кожні 6 годин</option>
          <option value="1440">Один раз на добу</option>
        </select>
      </div>

      <!-- Help Note -->
      <div class="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4 text-xs text-indigo-300 flex items-start gap-2.5 leading-relaxed">
        <span>💡</span>
        <span>
          При активації сортувальник зареєструє нативне системне завдання у фоновому планивальнику вашої ОС (macOS launchd, Windows Task Scheduler або Linux Cron).
        </span>
      </div>
    </div>
  </div>
</template>
