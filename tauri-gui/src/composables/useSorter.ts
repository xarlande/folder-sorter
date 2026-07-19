import { ref, shallowRef, computed, type Ref } from 'vue';
import type { LogEntry, LogType, SortMetrics, AppConfig } from '../types/sorter';
import { runSorting, getDefaultDownloadsFolder } from '../services/sorterService';
import { selectFolder } from '../services/dialogService';

export function useSorter(configRef: Ref<AppConfig>) {
  const sourceDir = ref<string>('');
  const targetDir = ref<string>('');
  const isDryRun = ref<boolean>(true);

  const isSorting = ref<boolean>(false);
  const sortStatus = ref<string>('Готовий');
  const statusColor = ref<string>('text-emerald-400');

  const metrics = ref<SortMetrics>({
    total: 0,
    organized: 0,
  });

  // Performance optimization for logs using shallowRef
  const logs = shallowRef<LogEntry[]>([
    { time: new Date().toLocaleTimeString(), type: 'info', message: 'FolderSorter готовий до прибирання.' },
  ]);

  const activeCategoriesCount = computed(() => {
    return Object.keys(configRef.value.rules || {}).length;
  });

  const addLog = (message: string, type: LogType = 'dry') => {
    const time = new Date().toLocaleTimeString();
    logs.value = [...logs.value, { time, type, message }];
  };

  const clearLogs = () => {
    logs.value = [];
  };

  const browseSource = async () => {
    try {
      const selected = await selectFolder('Виберіть вхідну папку для прибирання');
      if (selected) {
        sourceDir.value = selected;
      }
    } catch (err) {
      addLog(`Помилка відкриття діалогу: ${err}`, 'error');
    }
  };

  const browseTarget = async () => {
    try {
      const selected = await selectFolder('Виберіть папку призначення');
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
      const summary = await runSorting(sourceDir.value, targetDir.value, isDryRun.value);

      metrics.value.total = summary.total_files;
      metrics.value.organized = summary.moved_files;

      if (summary.actions.length === 0) {
        addLog('У цій папці не знайдено відповідних файлів.', 'info');
      } else {
        summary.actions.forEach((action) => {
          const type: LogType =
            action.status === 'moved' ? 'moved' : action.status === 'error' ? 'error' : 'dry';
          addLog(`${action.file_name} ➔ [${action.category}] (${action.to_path})`, type);
        });
        addLog(
          `Прибирання завершено! Оброблено: ${summary.moved_files} з ${summary.total_files}`,
          'info'
        );
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

  const initDefaultFolder = async () => {
    try {
      const defaultDownloads = await getDefaultDownloadsFolder();
      if (defaultDownloads) {
        sourceDir.value = defaultDownloads;
      }
    } catch (err) {
      console.error('Failed to initialize default downloads folder:', err);
    }
  };

  return {
    sourceDir,
    targetDir,
    isDryRun,
    isSorting,
    sortStatus,
    statusColor,
    metrics,
    logs,
    activeCategoriesCount,
    addLog,
    clearLogs,
    browseSource,
    browseTarget,
    startSorting,
    initDefaultFolder,
  };
}
