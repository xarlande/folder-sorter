use folder_sorter::{load_config_from_path, save_config_to_path, Config, SortSummary};
use std::path::{Path, PathBuf};

fn get_config_path() -> PathBuf {
    if let Some(home) = std::env::var_os("HOME").or_else(|| std::env::var_os("USERPROFILE")) {
        PathBuf::from(home)
            .join(".foldersorter")
            .join(folder_sorter::CONFIG_FILE_NAME)
    } else {
        PathBuf::from(folder_sorter::CONFIG_FILE_NAME)
    }
}

#[tauri::command]
fn get_config() -> Result<Config, String> {
    let path = get_config_path();
    load_config_from_path(&path).map_err(|e| e.to_string())
}

#[tauri::command]
fn save_config(config: Config) -> Result<(), String> {
    let path = get_config_path();
    save_config_to_path(&config, &path).map_err(|e| e.to_string())
}

#[tauri::command]
fn run_sorting(
    source_dir: String,
    target_dir: String,
    dry_run: bool,
) -> Result<SortSummary, String> {
    let path = get_config_path();
    let config = load_config_from_path(&path).map_err(|e| e.to_string())?;

    let src = Path::new(&source_dir);
    let target = if target_dir.trim().is_empty() {
        src
    } else {
        Path::new(&target_dir)
    };

    folder_sorter::organize_files_with_summary(src, target, &config, dry_run)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn get_default_downloads_folder() -> String {
    if let Some(home) = std::env::var_os("HOME").or_else(|| std::env::var_os("USERPROFILE")) {
        PathBuf::from(home)
            .join("Downloads")
            .to_string_lossy()
            .into_owned()
    } else {
        String::new()
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_notification::init())
        .invoke_handler(tauri::generate_handler![
            get_config,
            save_config,
            run_sorting,
            get_default_downloads_folder
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

