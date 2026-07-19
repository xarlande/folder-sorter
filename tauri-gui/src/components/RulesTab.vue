<script setup>
import { ref, inject } from 'vue';

const config = inject('config');
const saveConfig = inject('saveConfig');
const loadConfig = inject('loadConfig');

const newTagInputs = ref({});
const isSaving = ref(false);
const saveFeedback = ref('');

const removeTag = (category, ext) => {
  if (config.value.rules[category]) {
    config.value.rules[category] = config.value.rules[category].filter(x => x !== ext);
  }
};

const addTag = (category) => {
  const val = (newTagInputs.value[category] || '').trim().toLowerCase().replace(/^\./, '');
  if (val && config.value.rules[category]) {
    if (!config.value.rules[category].includes(val)) {
      config.value.rules[category].push(val);
    }
    newTagInputs.value[category] = '';
  }
};

const addCategory = () => {
  const name = prompt('Введіть назву нової категорії (наприклад, "Книги"):');
  if (name && name.trim()) {
    const catName = name.trim();
    if (!config.value.rules[catName]) {
      config.value.rules[catName] = [];
    }
  }
};

const deleteCategory = (category) => {
  if (confirm(`Видалити категорію "${category}"?`)) {
    delete config.value.rules[category];
  }
};

const handleSave = async () => {
  try {
    isSaving.value = true;
    await saveConfig();
    saveFeedback.value = 'Правила успішно збережено!';
    setTimeout(() => { saveFeedback.value = ''; }, 3000);
  } catch (err) {
    alert('Помилка збереження правил!');
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <div class="flex flex-col gap-6 animate-fadeIn">
    <div class="glass-panel p-5 rounded-2xl flex flex-col gap-5 shadow-xl">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-white/10 pb-4">
        <div>
          <h2 class="text-sm font-semibold text-white flex items-center gap-2">
            <span>🎯</span> Редактор категорій та розширень
          </h2>
          <p class="text-xs text-gray-400 mt-1">
            Налаштуйте правила розподілу файлів за відповідними папками.
          </p>
        </div>

        <div class="flex items-center gap-3">
          <span v-if="saveFeedback" class="text-xs text-emerald-400 font-semibold animate-pulse">
            {{ saveFeedback }}
          </span>
          <button
            @click="addCategory"
            class="px-3.5 py-2 bg-white/10 hover:bg-white/15 border border-white/10 rounded-xl text-xs font-semibold text-white transition-all duration-150"
          >
            + Категорія
          </button>
          <button
            @click="handleSave"
            :disabled="isSaving"
            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-indigo-600/30 transition-all duration-150 active:scale-95"
          >
            💾 {{ isSaving ? 'Збереження...' : 'Зберегти правила' }}
          </button>
        </div>
      </div>

      <!-- Rules Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="(extensions, category) in config.rules"
          :key="category"
          class="glass-card p-4 rounded-xl flex flex-col gap-3 border border-white/5 hover:border-white/10 transition-all duration-200"
        >
          <div class="flex items-center justify-between">
            <span class="font-bold text-sm text-white flex items-center gap-2">
              📂 {{ category }}
            </span>
            <button
              @click="deleteCategory(category)"
              class="text-[11px] text-rose-400 hover:text-rose-300 hover:bg-rose-500/20 px-2 py-0.5 rounded transition-all duration-150"
            >
              Видалити
            </button>
          </div>

          <!-- Tags List -->
          <div class="flex flex-wrap gap-1.5 min-h-[36px]">
            <span
              v-for="ext in extensions"
              :key="ext"
              class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-indigo-500/15 border border-indigo-500/30 text-indigo-300 rounded-lg text-xs font-mono"
            >
              .{{ ext }}
              <button
                @click="removeTag(category, ext)"
                class="text-rose-400 hover:text-rose-300 font-bold text-xs"
              >×</button>
            </span>
          </div>

          <!-- Add Tag Input -->
          <div class="flex gap-2 mt-1">
            <input
              v-model="newTagInputs[category]"
              @keyup.enter="addTag(category)"
              type="text"
              placeholder="Додати розширення..."
              class="flex-1 glass-input rounded-lg px-2.5 py-1.5 text-xs text-white placeholder-gray-500 focus:outline-none"
            />
            <button
              @click="addTag(category)"
              class="px-3 py-1.5 bg-white/10 hover:bg-white/20 border border-white/10 rounded-lg text-xs font-bold text-white transition-all duration-150"
            >+</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
