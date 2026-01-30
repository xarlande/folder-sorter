use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub rules: HashMap<String, Vec<String>>,
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

pub fn load_config() -> Config {
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
