<script setup lang="ts">
import { onMounted } from 'vue';
import { useConfig } from '../composables/useConfig';
import { useSorter } from '../composables/useSorter';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  FolderInput,
  FolderOutput,
  FolderOpen,
  Play,
  Loader2,
  Terminal,
  Trash2,
} from '@lucide/vue';

const { config } = useConfig();
const {
  sourceDir,
  targetDir,
  isDryRun,
  isSorting,
  sortStatus,
  statusColor,
  metrics,
  logs,
  activeCategoriesCount,
  clearLogs,
  browseSource,
  browseTarget,
  startSorting,
  initDefaultFolder,
} = useSorter(config);

onMounted(() => {
  initDefaultFolder();
});
</script>

<template>
  <div class="flex flex-col gap-6 animate-in fade-in duration-300">
    <!-- Folder Selectors Card -->
    <Card class="border-border bg-card/80 backdrop-blur-md shadow-sm">
      <CardHeader class="pb-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <FolderInput class="w-5 h-5 text-primary" />
            <CardTitle class="text-base font-semibold">Вибір каталогів для сортування</CardTitle>
          </div>
          <Badge variant="outline" class="font-mono text-[11px]">
            Автоматичне сортування
          </Badge>
        </div>
        <CardDescription>
          Вкажіть папку з файлами, які потрібно впорядкувати, та папку призначення.
        </CardDescription>
      </CardHeader>

      <CardContent class="flex flex-col gap-5 pt-0">
        <!-- Source Directory Input -->
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Вхідна папка (Джерело):
          </label>
          <div class="flex gap-2">
            <Input
              v-model="sourceDir"
              type="text"
              placeholder="Виберіть папку для прибирання (наприклад, Завантаження)..."
              class="flex-1 font-mono text-xs select-text"
            />
            <Button @click="browseSource" variant="secondary" size="default" class="flex items-center gap-2">
              <FolderOpen class="w-4 h-4" />
              <span>Огляд</span>
            </Button>
          </div>
        </div>

        <!-- Target Directory Input -->
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Папка призначення (Опціонально):
          </label>
          <div class="flex gap-2">
            <Input
              v-model="targetDir"
              type="text"
              placeholder="Залиште порожнім для сортування у тій самій папці..."
              class="flex-1 font-mono text-xs select-text"
            />
            <Button @click="browseTarget" variant="secondary" size="default" class="flex items-center gap-2">
              <FolderOutput class="w-4 h-4" />
              <span>Огляд</span>
            </Button>
          </div>
        </div>

        <!-- Dry Run Options Toggle -->
        <div class="flex items-center gap-3 pt-2">
          <Switch id="dry-run" v-model="isDryRun" />
          <label for="dry-run" class="text-xs font-medium text-foreground cursor-pointer select-none">
            Режим перевірки (Dry Run) — показати зміни без фактичного переміщення файлів
          </label>
        </div>
      </CardContent>
    </Card>

    <!-- Metrics Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card class="p-4 bg-card/50">
        <div class="flex flex-col gap-1">
          <span class="text-2xl font-bold font-mono text-foreground">{{ metrics.total }}</span>
          <span class="text-xs text-muted-foreground font-medium">Знайдено файлів</span>
        </div>
      </Card>

      <Card class="p-4 bg-card/50">
        <div class="flex flex-col gap-1">
          <span class="text-2xl font-bold font-mono text-primary">{{ metrics.organized }}</span>
          <span class="text-xs text-muted-foreground font-medium">Оброблено файлів</span>
        </div>
      </Card>

      <Card class="p-4 bg-card/50">
        <div class="flex flex-col gap-1">
          <span class="text-2xl font-bold font-mono text-purple-400">{{ activeCategoriesCount }}</span>
          <span class="text-xs text-muted-foreground font-medium">Активних категорій</span>
        </div>
      </Card>

      <Card class="p-4 bg-card/50">
        <div class="flex flex-col gap-1">
          <span :class="['text-sm font-bold truncate', statusColor]">{{ sortStatus }}</span>
          <span class="text-xs text-muted-foreground font-medium">Статус системи</span>
        </div>
      </Card>
    </div>

    <!-- Action Button -->
    <div class="flex justify-end">
      <Button
        @click="startSorting"
        :disabled="isSorting"
        size="lg"
        class="font-semibold gap-2 shadow-md hover:shadow-lg transition-all"
      >
        <Loader2 v-if="isSorting" class="w-4 h-4 animate-spin" />
        <Play v-else class="w-4 h-4 fill-current" />
        <span>{{ isSorting ? 'Сортування...' : 'Почати прибирання' }}</span>
      </Button>
    </div>

    <!-- Log Console Glass Panel -->
    <Card class="border-border bg-card/80 backdrop-blur-md">
      <CardHeader class="py-3 px-4 flex flex-row items-center justify-between border-b border-border/60">
        <div class="flex items-center gap-2">
          <Terminal class="w-4 h-4 text-primary" />
          <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Консоль результатів</span>
        </div>
        <Button @click="clearLogs" variant="ghost" size="sm" class="h-7 text-xs flex items-center gap-1.5 text-muted-foreground hover:text-foreground">
          <Trash2 class="w-3.5 h-3.5" />
          <span>Очистити</span>
        </Button>
      </CardHeader>

      <CardContent class="p-3">
        <ScrollArea class="h-48 rounded-md bg-muted/40 border border-border/40 p-3 font-mono text-xs select-text">
          <div class="flex flex-col gap-2">
            <div v-for="(log, idx) in logs" :key="idx" class="flex gap-2.5 items-start leading-relaxed">
              <span class="text-muted-foreground text-[11px]">[{{ log.time }}]</span>

              <Badge
                v-if="log.type === 'moved'"
                variant="default"
                class="bg-emerald-500/15 text-emerald-400 border-emerald-500/30 text-[10px] uppercase font-mono px-1.5 py-0"
              >ПЕРЕМІЩЕНО</Badge>

              <Badge
                v-else-if="log.type === 'error'"
                variant="destructive"
                class="text-[10px] uppercase font-mono px-1.5 py-0"
              >ПОМИЛКА</Badge>

              <Badge
                v-else-if="log.type === 'dry'"
                variant="secondary"
                class="text-[10px] uppercase font-mono px-1.5 py-0"
              >DRY RUN</Badge>

              <Badge
                v-else
                variant="outline"
                class="text-[10px] uppercase font-mono px-1.5 py-0"
              >ІНФО</Badge>

              <span class="text-foreground flex-1 leading-snug">{{ log.message }}</span>
            </div>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  </div>
</template>

