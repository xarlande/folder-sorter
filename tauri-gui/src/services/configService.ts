import { invoke } from '@tauri-apps/api/core';
import type { AppConfig } from '../types/sorter';

export async function fetchConfig(): Promise<AppConfig> {
  try {
    return await invoke<AppConfig>('get_config');
  } catch (error) {
    console.error('Failed to fetch config from Tauri backend:', error);
    throw new Error(typeof error === 'string' ? error : 'Failed to load configuration');
  }
}

export async function saveConfig(config: AppConfig): Promise<void> {
  try {
    await invoke<void>('save_config', { config });
  } catch (error) {
    console.error('Failed to save config to Tauri backend:', error);
    throw new Error(typeof error === 'string' ? error : 'Failed to save configuration');
  }
}
