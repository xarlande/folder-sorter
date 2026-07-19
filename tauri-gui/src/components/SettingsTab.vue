<script setup lang="ts">
import { ref } from 'vue';
import { useConfig } from '../composables/useConfig';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Settings, RefreshCw, RotateCcw, FileText, CheckCircle2 } from '@lucide/vue';

const { loadConfig, resetToDefaultConfig } = useConfig();
const feedbackMsg = ref<string>('');

const reloadConfig = async (): Promise<void> => {
  await loadConfig();
  feedbackMsg.value = 'Конфігурацію перезавантажено з диска.';
  setTimeout(() => {
    feedbackMsg.value = '';
  }, 3000);
};

const resetConfig = async (): Promise<void> => {
  await resetToDefaultConfig();
  feedbackMsg.value = 'Правила скинуто до дефолтних.';
  setTimeout(() => {
    feedbackMsg.value = '';
  }, 3000);
};
</script>

<template>
  <div class="flex flex-col gap-6 animate-in fade-in duration-300">
    <Card class="border-border bg-card/80 backdrop-blur-md shadow-sm">
      <CardHeader class="pb-4 border-b border-border/60">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <Settings class="w-5 h-5 text-primary" />
            <CardTitle class="text-base font-semibold">Налаштування застосунку</CardTitle>
          </div>
          <span v-if="feedbackMsg" class="text-xs text-emerald-400 font-semibold flex items-center gap-1.5 animate-in fade-in">
            <CheckCircle2 class="w-3.5 h-3.5" />
            <span>{{ feedbackMsg }}</span>
          </span>
        </div>
        <CardDescription class="mt-1">
          Управління файлами конфігурації та скидання налаштувань.
        </CardDescription>
      </CardHeader>

      <CardContent class="flex flex-col gap-6 pt-6">
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
            <FileText class="w-3.5 h-3.5" />
            <span>Шлях до файлу конфігурації (TOML):</span>
          </label>
          <Input
            type="text"
            readonly
            value="~/.foldersorter/cleaner_config.toml"
            class="font-mono text-xs select-text max-w-md bg-muted/30"
          />
        </div>

        <div class="flex flex-wrap items-center gap-3 pt-2">
          <Button @click="reloadConfig" variant="secondary" size="default" class="flex items-center gap-2">
            <RefreshCw class="w-4 h-4" />
            <span>Перезавантажити з диска</span>
          </Button>

          <Button @click="resetConfig" variant="destructive" size="default" class="flex items-center gap-2">
            <RotateCcw class="w-4 h-4" />
            <span>Скинути дефолтні правила</span>
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

