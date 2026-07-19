use crate::config::Config;
use crate::error::SorterError;
use std::fs;
use std::path::Path;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SortAction {
    pub file_name: String,
    pub category: String,
    pub from_path: String,
    pub to_path: String,
    pub status: String,
    pub error_message: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SortSummary {
    pub total_files: usize,
    pub moved_files: usize,
    pub dry_run: bool,
    pub actions: Vec<SortAction>,
}

pub fn organize_files<P1: AsRef<Path>, P2: AsRef<Path>>(
    source_dir: P1,
    target_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<(), SorterError> {
    organize_files_with_summary(source_dir, target_dir, config, dry_run).map(|_| ())
}

pub fn organize_files_with_summary<P1: AsRef<Path>, P2: AsRef<Path>>(
    source_dir: P1,
    target_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<SortSummary, SorterError> {
    let source_path = source_dir.as_ref();
    let target_path = target_dir.as_ref();

    if dry_run {
        println!("🔍 РЕЖИМ ПЕРЕВІРКИ (Dry Run): Зміни не будуть застосовані.");
    }
    println!("Починаю прибирання: {:?} -> {:?}", source_path, target_path);

    let entries = fs::read_dir(source_path)?;
    let mut actions = Vec::new();
    let mut total_files = 0;
    let mut moved_files = 0;

    for entry in entries {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            if let Some(file_name) = path.file_name() {
                let file_name_str = file_name.to_string_lossy();
                if file_name_str.starts_with('.') || file_name_str == crate::config::CONFIG_FILE_NAME {
                    continue;
                }
            }
            total_files += 1;
            match organize_file_detailed(&path, target_path, config, dry_run) {
                Ok(action) => {
                    if action.status == "moved" || action.status == "dry_run" {
                        moved_files += 1;
                    }
                    actions.push(action);
                }
                Err(e) => {
                    eprintln!("Помилка при обробці {:?}: {}", path, e);
                }
            }
        }
    }

    println!("Прибирання завершено!");
    Ok(SortSummary {
        total_files,
        moved_files,
        dry_run,
        actions,
    })
}


pub fn organize_file<P1: AsRef<Path>, P2: AsRef<Path>>(
    file_path: P1,
    base_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<(), SorterError> {
    organize_file_detailed(file_path, base_dir, config, dry_run).map(|_| ())
}

pub fn organize_file_detailed<P1: AsRef<Path>, P2: AsRef<Path>>(
    file_path: P1,
    base_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<SortAction, SorterError> {
    let file_path = file_path.as_ref();
    let base_dir = base_dir.as_ref();

    let ext_str = file_path
        .extension()
        .map(|ext| ext.to_string_lossy().to_lowercase())
        .unwrap_or_default();

    let mut category = "Інше";

    for (folder_name, extensions) in &config.rules {
        if extensions.contains(&ext_str) {
            category = folder_name;
            break;
        }
    }

    let destination_dir = base_dir.join(category);

    if !dry_run {
        fs::create_dir_all(&destination_dir)?;
    }

    let file_name = file_path
        .file_name()
        .ok_or_else(|| SorterError::InvalidFileName(file_path.to_string_lossy().into_owned()))?;

    let mut destination_path = destination_dir.join(file_name);

    // Обробка дублікатів
    if destination_path.exists() {
        let file_stem = file_path
            .file_stem()
            .ok_or_else(|| SorterError::InvalidFileStem(file_path.to_string_lossy().into_owned()))?;
        
        let ext_str = file_path
            .extension()
            .map(|ext| ext.to_string_lossy().into_owned())
            .unwrap_or_default();

        let mut counter = 1;

        while destination_path.exists() {
            let new_name = if ext_str.is_empty() {
                format!("{} ({})", file_stem.to_string_lossy(), counter)
            } else {
                format!("{} ({}).{}", file_stem.to_string_lossy(), counter, ext_str)
            };
            destination_path = destination_dir.join(new_name);
            counter += 1;
        }
    }

    let file_name_str = file_name.to_string_lossy().into_owned();
    let from_str = file_path.to_string_lossy().into_owned();
    let to_str = destination_path.to_string_lossy().into_owned();

    if dry_run {
        println!(
            "[Dry Run] Буде переміщено: {:?} -> {:?}",
            file_name, destination_path
        );
        Ok(SortAction {
            file_name: file_name_str,
            category: category.to_string(),
            from_path: from_str,
            to_path: to_str,
            status: "dry_run".to_string(),
            error_message: None,
        })
    } else {
        match move_file(file_path, &destination_path) {
            Ok(_) => {
                println!("Переміщено: {:?} -> {:?}", file_name, destination_path);
                Ok(SortAction {
                    file_name: file_name_str,
                    category: category.to_string(),
                    from_path: from_str,
                    to_path: to_str,
                    status: "moved".to_string(),
                    error_message: None,
                })
            }
            Err(e) => {
                let err_msg = e.to_string();
                eprintln!("Помилка переміщення {:?}: {}", file_name, err_msg);
                Ok(SortAction {
                    file_name: file_name_str,
                    category: category.to_string(),
                    from_path: from_str,
                    to_path: to_str,
                    status: "error".to_string(),
                    error_message: Some(err_msg),
                })
            }
        }
    }
}


fn move_file(from: &Path, to: &Path) -> std::io::Result<()> {
    if fs::rename(from, to).is_err() {
        fs::copy(from, to)?;
        fs::remove_file(from)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::Config;
    use tempfile::tempdir;
    use std::fs::File;

    #[test]
    fn test_organize_files_basic() {
        let temp_dir = tempdir().unwrap();
        let src_path = temp_dir.path().join("source");
        let dest_path = temp_dir.path().join("dest");

        fs::create_dir(&src_path).unwrap();
        fs::create_dir(&dest_path).unwrap();

        // Create test files
        File::create(src_path.join("image.jpg")).unwrap();
        File::create(src_path.join("video.mp4")).unwrap();
        File::create(src_path.join("document.txt")).unwrap();
        File::create(src_path.join("no_extension")).unwrap();
        File::create(src_path.join(".hidden_file")).unwrap();
        File::create(src_path.join(crate::config::CONFIG_FILE_NAME)).unwrap();

        let mut config = Config::default();
        // Modify rules for testing
        config.rules.insert(
            "Зображення".to_string(),
            vec!["jpg".to_string()],
        );
        config.rules.insert(
            "Відео".to_string(),
            vec!["mp4".to_string()],
        );
        config.rules.insert(
            "Документи".to_string(),
            vec!["txt".to_string()],
        );

        organize_files(&src_path, &dest_path, &config, false).unwrap();

        // Verify sorted files
        assert!(dest_path.join("Зображення/image.jpg").exists());
        assert!(dest_path.join("Відео/video.mp4").exists());
        assert!(dest_path.join("Документи/document.txt").exists());
        assert!(dest_path.join("Інше/no_extension").exists());

        // Verify ignored files are NOT moved and still exist in source
        assert!(src_path.join(".hidden_file").exists());
        assert!(src_path.join(crate::config::CONFIG_FILE_NAME).exists());
        assert!(!dest_path.join("Інше/.hidden_file").exists());
    }

    #[test]
    fn test_organize_files_duplicates() {
        let temp_dir = tempdir().unwrap();
        let src_path = temp_dir.path().join("source");
        let dest_path = temp_dir.path().join("dest");

        fs::create_dir(&src_path).unwrap();
        fs::create_dir(&dest_path).unwrap();

        // Pre-create duplicate targets in destination
        let dest_img_dir = dest_path.join("Зображення");
        fs::create_dir_all(&dest_img_dir).unwrap();
        File::create(dest_img_dir.join("image.jpg")).unwrap();

        // Create test file in source
        File::create(src_path.join("image.jpg")).unwrap();

        let mut config = Config::default();
        config.rules.insert(
            "Зображення".to_string(),
            vec!["jpg".to_string()],
        );

        organize_files(&src_path, &dest_path, &config, false).unwrap();

        // Verify duplicate renaming
        assert!(dest_img_dir.join("image.jpg").exists());
        assert!(dest_img_dir.join("image (1).jpg").exists());
    }
}
