<script setup lang="ts">
import { ref } from 'vue';
import { useConfig } from '../composables/useConfig';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Folder,
  Plus,
  Trash2,
  Save,
  Loader2,
  CheckCircle2,
  Sliders,
  X,
} from '@lucide/vue';

const { config, saveConfig } = useConfig();

const newCategoryName = ref<string>('');
const isAddingCategory = ref<boolean>(false);
const newTagInputs = ref<Record<string, string>>({});
const isSaving = ref<boolean>(false);
const saveFeedback = ref<string>('');

const removeTag = (category: string, ext: string): void => {
  if (config.value.rules[category]) {
    config.value.rules[category] = config.value.rules[category].filter((x) => x !== ext);
  }
};

const addTag = (category: string): void => {
  const inputVal = newTagInputs.value[category] || '';
  const val = inputVal.trim().toLowerCase().replace(/^\./, '');
  if (val && config.value.rules[category]) {
    if (!config.value.rules[category].includes(val)) {
      config.value.rules[category].push(val);
    }
    newTagInputs.value[category] = '';
  }
};

const submitNewCategory = (): void => {
  const name = newCategoryName.value.trim();
  if (name) {
    if (!config.value.rules[name]) {
      config.value.rules[name] = [];
    }
    newCategoryName.value = '';
    isAddingCategory.value = false;
  }
};

const deleteCategory = (category: string): void => {
  delete config.value.rules[category];
};

const handleSave = async (): Promise<void> => {
  try {
    isSaving.value = true;
    await saveConfig();
    saveFeedback.value = 'Правила успішно збережено!';
    setTimeout(() => {
      saveFeedback.value = '';
    }, 3000);
  } catch (err) {
    saveFeedback.value = 'Помилка збереження правил!';
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <div class="flex flex-col gap-6 animate-in fade-in duration-300">
    <Card class="border-border bg-card/80 backdrop-blur-md shadow-sm">
      <CardHeader class="pb-4 border-b border-border/60">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <Sliders class="w-5 h-5 text-primary" />
              <CardTitle class="text-base font-semibold">Редактор категорій та розширень</CardTitle>
            </div>
            <CardDescription class="mt-1">
              Налаштуйте правила розподілу файлів за відповідними папками.
            </CardDescription>
          </div>

          <div class="flex items-center gap-3">
            <span v-if="saveFeedback" class="text-xs text-emerald-400 font-semibold flex items-center gap-1.5 animate-in fade-in">
              <CheckCircle2 class="w-3.5 h-3.5" />
              <span>{{ saveFeedback }}</span>
            </span>

            <Button
              v-if="!isAddingCategory"
              @click="isAddingCategory = true"
              variant="outline"
              size="sm"
              class="flex items-center gap-1.5"
            >
              <Plus class="w-4 h-4" />
              <span>Категорія</span>
            </Button>

            <Button
              @click="handleSave"
              :disabled="isSaving"
              size="sm"
              class="flex items-center gap-1.5 shadow-sm"
            >
              <Loader2 v-if="isSaving" class="w-4 h-4 animate-spin" />
              <Save v-else class="w-4 h-4" />
              <span>{{ isSaving ? 'Збереження...' : 'Зберегти правила' }}</span>
            </Button>
          </div>
        </div>

        <!-- Inline Form for New Category -->
        <div v-if="isAddingCategory" class="flex items-center gap-2 pt-3 animate-in fade-in duration-200">
          <Input
            v-model="newCategoryName"
            @keyup.enter="submitNewCategory"
            type="text"
            placeholder="Назва нової категорії (наприклад, Книги)..."
            class="max-w-xs text-xs font-medium"
            autoFocus
          />
          <Button @click="submitNewCategory" size="sm" class="flex items-center gap-1 text-xs">
            <span>Додати</span>
          </Button>
          <Button @click="isAddingCategory = false" variant="ghost" size="sm" class="p-2">
            <X class="w-4 h-4 text-muted-foreground" />
          </Button>
        </div>
      </CardHeader>

      <CardContent class="pt-6">
        <!-- Rules Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card
            v-for="(extensions, category) in config.rules"
            :key="category"
            class="p-4 bg-muted/20 border-border/60 flex flex-col gap-3 hover:border-border transition-all"
          >
            <div class="flex items-center justify-between">
              <span class="font-semibold text-sm flex items-center gap-2 text-foreground">
                <Folder class="w-4 h-4 text-primary" />
                <span>{{ category }}</span>
              </span>
              <Button
                @click="deleteCategory(category)"
                variant="ghost"
                size="sm"
                class="h-7 px-2 text-xs text-destructive hover:text-destructive hover:bg-destructive/10"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </Button>
            </div>

            <!-- Tags List -->
            <div class="flex flex-wrap gap-1.5 min-h-[36px] items-center">
              <Badge
                v-for="ext in extensions"
                :key="ext"
                variant="secondary"
                class="font-mono text-xs py-0.5 px-2 flex items-center gap-1.5 bg-primary/10 text-primary border border-primary/20"
              >
                <span>.{{ ext }}</span>
                <button
                  @click="removeTag(category, ext)"
                  class="hover:text-destructive font-bold text-xs leading-none transition-colors"
                >×</button>
              </Badge>
            </div>

            <!-- Add Tag Input -->
            <div class="flex gap-2 mt-1">
              <Input
                v-model="newTagInputs[category]"
                @keyup.enter="addTag(category)"
                type="text"
                placeholder="Додати розширення..."
                class="flex-1 text-xs font-mono h-8"
              />
              <Button
                @click="addTag(category)"
                variant="outline"
                size="sm"
                class="h-8 px-2.5"
              >
                <Plus class="w-3.5 h-3.5" />
              </Button>
            </div>
          </Card>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

