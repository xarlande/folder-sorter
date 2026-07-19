<script setup>
import { inject } from 'vue';

const loadConfig = inject('loadConfig');
const saveConfig = inject('saveConfig');
const config = inject('config');

const reloadConfig = async () => {
  await loadConfig();
  alert('Конфігурацію перезавантажено з диска.');
};

const resetConfig = async () => {
  if (confirm('Скинути конфігурацію до дефолтних категорій?')) {
    config.value = {
      rules: {
        "Зображення": ["jpg", "png", "jpeg", "gif", "svg"],
        "Відео": ["mp4", "mkv", "mov", "avi"],
        "Музика": ["mp3", "wav", "flac"],
        "Документи": ["pdf", "doc", "docx", "txt"],
        "Архіви": ["zip", "rar", "7z", "tar"],
        "Програми": ["exe", "msi", "deb"]
      }
    };
    await saveConfig();
    alert('Правила скинуто до дефолтних.');
  }
};
</script>

<template>
  <div class="flex flex-col gap-6 animate-fadeIn">
    <div class="glass-panel p-5 rounded-2xl flex flex-col gap-5 shadow-xl">
      <div class="border-b border-white/10 pb-4">
        <h2 class="text-sm font-semibold text-white flex items-center gap-2">
          <span>⚙️</span> Налаштування застосунку
        </h2>
        <p class="text-xs text-gray-400 mt-1">
          Управління файлами конфігурації та скидання налаштувань.
        </p>
      </div>

      <div class="flex flex-col gap-2">
        <label class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Шлях до файлу конфігурації (TOML):</label>
        <input
          type="text"
          readonly
          value="~/.foldersorter/cleaner_config.toml"
          class="glass-input rounded-xl px-3.5 py-2 text-xs text-gray-300 select-text"
        />
      </div>

      <div class="flex items-center gap-3 pt-2">
        <button
          @click="reloadConfig"
          class="px-4 py-2.5 bg-white/10 hover:bg-white/15 border border-white/10 rounded-xl text-xs font-semibold text-white transition-all duration-150 active:scale-95 flex items-center gap-2"
        >
          <span>🔄</span> Перезавантажити з диска
        </button>

        <button
          @click="resetConfig"
          class="px-4 py-2.5 bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/30 rounded-xl text-xs font-semibold text-rose-300 transition-all duration-150 active:scale-95 flex items-center gap-2"
        >
          <span>⚠️</span> Скинути дефолтні правила
        </button>
      </div>
    </div>
  </div>
</template>
