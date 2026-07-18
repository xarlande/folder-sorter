use thiserror::Error;

#[derive(Error, Debug)]
pub enum SorterError {
    #[error("Помилка вводу-виводу (I/O): {0}")]
    Io(#[from] std::io::Error),

    #[error("Помилка десеріалізації конфігурації: {0}")]
    TomlDe(#[from] toml::de::Error),

    #[error("Помилка серіалізації конфігурації: {0}")]
    TomlSer(#[from] toml::ser::Error),

    #[error("Некоректне або відсутнє ім'я файлу для шляху: {0}")]
    InvalidFileName(String),

    #[error("Некоректна назва файлу (file stem) для шляху: {0}")]
    InvalidFileStem(String),
}
