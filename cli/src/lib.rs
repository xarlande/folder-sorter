#![deny(unsafe_code)]

pub mod config;
pub mod error;
pub mod file_organizer;

pub use config::{Config, load_config, load_config_from_path, save_config, save_config_to_path, CONFIG_FILE_NAME};
pub use error::SorterError;
pub use file_organizer::{
    organize_file, organize_file_detailed, organize_files, organize_files_with_summary,
    SortAction, SortSummary,
};


