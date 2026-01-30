use clap::Parser;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    path: String,

    #[arg(short, long)]
    output: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    rules: HashMap<String, Vec<String>>,
}

impl Default for Config {
    fn default() -> Self {
        let mut rules = HashMap::new();
        rules.insert(
            "Зображення".to_string(),
            vec!["jpg", "png", "jpeg", "gif", "svg"]
                .into_iter()
                .map(String::from)
                .collect(),
        );
        rules.insert(
            "Відео".to_string(),
            vec!["mp4", "mkv", "mov", "avi"]
                .into_iter()
                .map(String::from)
                .collect(),
        );
        rules.insert(
            "Музика".to_string(),
            vec!["mp3", "wav", "flac"]
                .into_iter()
                .map(String::from)
                .collect(),
        );
        rules.insert(
            "Документи".to_string(),
            vec!["pdf", "doc", "docx", "txt"]
                .into_iter()
                .map(String::from)
                .collect(),
        );
        rules.insert(
            "Архіви".to_string(),
            vec!["zip", "rar", "7z", "tar"]
                .into_iter()
                .map(String::from)
                .collect(),
        );
        rules.insert(
            "Програми".to_string(),
            vec!["exe", "msi", "deb"]
                .into_iter()
                .map(String::from)
                .collect(),
        );

        Config { rules }
    }
}

fn load_config() -> Config {
    let config_path = "cleaner_config.toml";
    if Path::new(config_path).exists() {
        let content = fs::read_to_string(config_path).expect("Не вдалося прочитати конфіг");
        toml::from_str(&content).expect("Помилка парсингу конфігу")
    } else {
        let config = Config::default();
        let toml_string = toml::to_string(&config).unwrap();
        fs::write(config_path, toml_string).expect("Не вдалося створити файл конфігурації");
        println!("Створено файл конфігурації: {}", config_path);
        config
    }
}

fn main() {
    let args = Args::parse();
    let config = load_config();

    let source_dir = args.path;
    let target_dir = args.output.unwrap_or_else(|| source_dir.clone());

    println!("Починаю прибирання: {} -> {}", source_dir, target_dir);

    let entries = fs::read_dir(&source_dir).expect("Не вдалося відкрити папку");

    for entry in entries {
        let entry = entry.unwrap();
        let path = entry.path();

        if path.is_file() {
            organize_file(&path, &target_dir, &config);
        }
    }

    println!("Прибирання завершено!");
}

fn organize_file(file_path: &Path, base_dir: &str, config: &Config) {
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

        fs::create_dir_all(&destination_dir).unwrap();

        let file_name = file_path.file_name().unwrap();
        let destination_path = Path::new(&destination_dir).join(file_name);

        match fs::rename(file_path, &destination_path) {
            Ok(_) => println!("Переміщено: {:?} -> {}", file_name, category),
            Err(e) => eprintln!("Помилка переміщення {:?}: {}", file_name, e),
        }
    }
}
