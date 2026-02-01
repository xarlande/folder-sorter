use crate::config::Config;
use std::fs;
use std::path::Path;

pub fn organize_files(source_dir: &str, target_dir: &str, config: &Config, dry_run: bool) {
    if dry_run {
        println!("🔍 РЕЖИМ ПЕРЕВІРКИ (Dry Run): Зміни не будуть застосовані.");
    }
    println!("Починаю прибирання: {} -> {}", source_dir, target_dir);

    let entries = fs::read_dir(source_dir).expect("Не вдалося відкрити папку");

    for entry in entries {
        let entry = entry.unwrap();
        let path = entry.path();

        if path.is_file() {
            organize_file(&path, target_dir, config, dry_run);
        }
    }

    println!("Прибирання завершено!");
}

pub fn organize_file(file_path: &Path, base_dir: &str, config: &Config, dry_run: bool) {
    if let Some(extension) = file_path.extension() {
        let ext_str = extension.to_str().unwrap().to_lowercase();

        let mut category = "Інше";

        for (folder_name, extensions) in &config.rules {
            if extensions.contains(&ext_str) {
                category = folder_name;
                break;
            }
        }

        let destination_dir = format!("{}/{}", base_dir, category);

        if !dry_run {
            fs::create_dir_all(&destination_dir).unwrap();
        }

        let file_name = file_path.file_name().unwrap();
        let mut destination_path = Path::new(&destination_dir).join(file_name);

        // Обробка дублікатів
        if destination_path.exists() {
            let file_stem = file_path.file_stem().unwrap().to_string_lossy();
            let extension = file_path.extension().unwrap().to_string_lossy();
            let mut counter = 1;

            while destination_path.exists() {
                let new_name = format!("{} ({}).{}", file_stem, counter, extension);
                destination_path = Path::new(&destination_dir).join(new_name);
                counter += 1;
            }
        }

        if dry_run {
            println!(
                "[Dry Run] Буде переміщено: {:?} -> {:?}",
                file_name, destination_path
            );
        } else {
            match fs::rename(file_path, &destination_path) {
                Ok(_) => println!("Переміщено: {:?} -> {:?}", file_name, destination_path),
                Err(e) => eprintln!("Помилка переміщення {:?}: {}", file_name, e),
            }
        }
    }
}
