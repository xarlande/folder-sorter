import { ref, provide, inject, type InjectionKey, type Ref } from 'vue';
import type { AppConfig } from '../types/sorter';
import { fetchConfig, saveConfig as saveConfigApi } from '../services/configService';

export interface UseConfigReturn {
  config: Ref<AppConfig>;
  isLoadingConfig: Ref<boolean>;
  loadConfig: () => Promise<void>;
  saveConfig: () => Promise<boolean>;
  resetToDefaultConfig: () => Promise<void>;
}

const ConfigKey: InjectionKey<UseConfigReturn> = Symbol('ConfigState');

export function createConfigStore(): UseConfigReturn {
  const config = ref<AppConfig>({ rules: {} });
  const isLoadingConfig = ref<boolean>(true);

  const loadConfig = async (): Promise<void> => {
    try {
      isLoadingConfig.value = true;
      config.value = await fetchConfig();
    } catch (err) {
      console.error('Error loading config:', err);
    } finally {
      isLoadingConfig.value = false;
    }
  };

  const saveConfig = async (): Promise<boolean> => {
    try {
      await saveConfigApi(config.value);
      return true;
    } catch (err) {
      console.error('Error saving config:', err);
      throw err;
    }
  };

  const resetToDefaultConfig = async (): Promise<void> => {
    config.value = {
      rules: {
        'Зображення': ['jpg', 'png', 'jpeg', 'gif', 'svg'],
        'Відео': ['mp4', 'mkv', 'mov', 'avi'],
        'Музика': ['mp3', 'wav', 'flac'],
        'Документи': ['pdf', 'doc', 'docx', 'txt'],
        'Архіви': ['zip', 'rar', '7z', 'tar'],
        'Програми': ['exe', 'msi', 'deb'],
      },
    };
    await saveConfig();
  };

  const store: UseConfigReturn = {
    config,
    isLoadingConfig,
    loadConfig,
    saveConfig,
    resetToDefaultConfig,
  };

  provide(ConfigKey, store);
  return store;
}

export function useConfig(): UseConfigReturn {
  const store = inject(ConfigKey);
  if (!store) {
    throw new Error('useConfig must be used within a component tree provided with createConfigStore');
  }
  return store;
}
