<script setup lang="ts">
import { ref } from 'vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Clock, Lightbulb } from '@lucide/vue';

const isSchedulerEnabled = ref<boolean>(false);
const selectedInterval = ref<string>('60');
</script>

<template>
  <div class="flex flex-col gap-6 animate-in fade-in duration-300">
    <Card class="border-border bg-card/80 backdrop-blur-md shadow-sm">
      <CardHeader class="pb-4 border-b border-border/60">
        <div class="flex items-center gap-2">
          <Clock class="w-5 h-5 text-primary" />
          <CardTitle class="text-base font-semibold">Автоматичне сортування за розкладом</CardTitle>
        </div>
        <CardDescription>
          Налаштуйте системний фоновий розклад для автоматичного впорядкування файлів.
        </CardDescription>
      </CardHeader>

      <CardContent class="flex flex-col gap-6 pt-6">
        <!-- Toggle Switch -->
        <div class="flex items-center gap-3">
          <Switch id="scheduler-toggle" v-model="isSchedulerEnabled" />
          <label for="scheduler-toggle" class="text-xs font-semibold text-foreground cursor-pointer select-none">
            Увімкнути фоновий розклад
          </label>
        </div>

        <!-- Interval Selector -->
        <div class="flex flex-col gap-2 max-w-xs">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Інтервал запуску:
          </label>
          <Select v-model="selectedInterval">
            <SelectTrigger class="w-full text-xs font-medium">
              <SelectValue placeholder="Оберіть інтервал" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="15">Кожні 15 хвилин</SelectItem>
              <SelectItem value="30">Кожні 30 хвилин</SelectItem>
              <SelectItem value="60">Щогодини</SelectItem>
              <SelectItem value="360">Кожні 6 годин</SelectItem>
              <SelectItem value="1440">Один раз на добу</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Help Note -->
        <div class="bg-primary/10 border border-primary/20 rounded-xl p-4 text-xs text-primary/90 flex items-start gap-3 leading-relaxed">
          <Lightbulb class="w-4 h-4 shrink-0 mt-0.5" />
          <span>
            При активації сортувальник зареєструє нативне системне завдання у фоновому планивальнику вашої ОС (macOS launchd, Windows Task Scheduler або Linux Cron).
          </span>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

