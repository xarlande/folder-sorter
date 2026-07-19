export type TabType = 'sorter' | 'rules' | 'scheduler' | 'settings';

export interface AppConfig {
  rules: Record<string, string[]>;
}

export type ActionStatus = 'moved' | 'dry_run' | 'error' | string;

export interface SortAction {
  file_name: string;
  category: string;
  from_path: string;
  to_path: string;
  status: ActionStatus;
  error_message?: string | null;
}

export interface SortSummary {
  total_files: number;
  moved_files: number;
  dry_run: boolean;
  actions: SortAction[];
}

export type LogType = 'info' | 'moved' | 'error' | 'dry';

export interface LogEntry {
  time: string;
  type: LogType;
  message: string;
}

export interface SortMetrics {
  total: number;
  organized: number;
}
