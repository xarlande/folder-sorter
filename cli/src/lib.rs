#![deny(unsafe_code)]

pub mod config;
pub mod error;
pub mod file_organizer;

pub use config::{Config, load_config};
pub use error::SorterError;
pub use file_organizer::{organize_file, organize_files};
