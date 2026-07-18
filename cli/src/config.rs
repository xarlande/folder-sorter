use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use crate::error::SorterError;

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub(crate) rules: HashMap<String, Vec<String>>,
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

pub(crate) const CONFIG_FILE_NAME: &str = "cleaner_config.toml";

pub fn load_config() -> Result<Config, SorterError> {
    if Path::new(CONFIG_FILE_NAME).exists() {
        let content = fs::read_to_string(CONFIG_FILE_NAME)?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    } else {
        let config = Config::default();
        let toml_string = toml::to_string(&config)?;
        fs::write(CONFIG_FILE_NAME, toml_string)?;
        println!("Створено файл конфігурації: {}", CONFIG_FILE_NAME);
        Ok(config)
    }
}
