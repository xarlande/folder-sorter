pub mod config;
pub mod file_organizer;

pub use config::{Config, load_config};
pub use file_organizer::{organize_file, organize_files};
