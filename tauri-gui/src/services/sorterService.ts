import { invoke } from '@tauri-apps/api/core';
import type { SortSummary } from '../types/sorter';

export async function runSorting(
  sourceDir: string,
  targetDir: string,
  dryRun: boolean
): Promise<SortSummary> {
  try {
    return await invoke<SortSummary>('run_sorting', {
      sourceDir: sourceDir.trim(),
      targetDir: targetDir.trim(),
      dryRun,
    });
  } catch (error) {
    console.error('Failed to run sorting command:', error);
    throw new Error(typeof error === 'string' ? error : 'Sorting operation failed');
  }
}

export async function getDefaultDownloadsFolder(): Promise<string> {
  try {
    return await invoke<string>('get_default_downloads_folder');
  } catch (error) {
    console.error('Failed to get default downloads folder:', error);
    return '';
  }
}
