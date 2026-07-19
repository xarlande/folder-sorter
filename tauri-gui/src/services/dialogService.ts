import { open } from '@tauri-apps/plugin-dialog';

export async function selectFolder(title: string): Promise<string | null> {
  try {
    const selected = await open({
      directory: true,
      multiple: false,
      title,
    });
    if (typeof selected === 'string') {
      return selected;
    }
    return null;
  } catch (error) {
    console.error('Folder selection dialog error:', error);
    throw new Error(typeof error === 'string' ? error : 'Failed to open directory dialog');
  }
}
