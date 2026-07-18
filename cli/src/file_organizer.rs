use crate::config::Config;
use crate::error::SorterError;
use std::fs;
use std::path::Path;

pub fn organize_files<P1: AsRef<Path>, P2: AsRef<Path>>(
    source_dir: P1,
    target_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<(), SorterError> {
    let source_path = source_dir.as_ref();
    let target_path = target_dir.as_ref();

    if dry_run {
        println!("🔍 РЕЖИМ ПЕРЕВІРКИ (Dry Run): Зміни не будуть застосовані.");
    }
    println!("Починаю прибирання: {:?} -> {:?}", source_path, target_path);

    let entries = fs::read_dir(source_path)?;

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
            organize_file(&path, target_path, config, dry_run)?;
        }
    }

    println!("Прибирання завершено!");
    Ok(())
}

pub fn organize_file<P1: AsRef<Path>, P2: AsRef<Path>>(
    file_path: P1,
    base_dir: P2,
    config: &Config,
    dry_run: bool,
) -> Result<(), SorterError> {
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

    if dry_run {
        println!(
            "[Dry Run] Буде переміщено: {:?} -> {:?}",
            file_name, destination_path
        );
    } else {
        match move_file(file_path, &destination_path) {
            Ok(_) => println!("Переміщено: {:?} -> {:?}", file_name, destination_path),
            Err(e) => eprintln!("Помилка переміщення {:?}: {}", file_name, e),
        }
    }

    Ok(())
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
