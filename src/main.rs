use clap::Parser;
use std::fs;
use std::path::Path;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Шлях до папки з файлами, які потрібно розсортувати (Джерело)
    #[arg(short, long)]
    path: String,

    /// Шлях до папки, куди будуть переміщені відсортовані файли (Призначення).
    /// Якщо не вказано, файли будуть сортуватися всередині папки-джерела.
    #[arg(short, long)]
    output: Option<String>,
}

fn main() {
    let args = Args::parse();
    let source_dir = args.path;
    let target_dir = args.output.unwrap_or_else(|| source_dir.clone());

    println!("Починаю прибирання: {} -> {}", source_dir, target_dir);

    let entries = fs::read_dir(&source_dir).expect("Не вдалося відкрити папку");

    for entry in entries {
        let entry = entry.unwrap();
        let path = entry.path();

        if path.is_file() {
            organize_file(&path, &target_dir);
        }
    }

    println!("Прибирання завершено!");
}

fn organize_file(file_path: &Path, base_dir: &str) {
    if let Some(extension) = file_path.extension() {
        let ext_str = extension.to_str().unwrap().to_lowercase();

        let category = match ext_str.as_str() {
            "jpg" | "png" | "jpeg" | "gif" | "svg" => "Зображення",
            "mp4" | "mkv" | "mov" | "avi" => "Відео",
            "mp3" | "wav" | "flac" => "Музика",
            "pdf" | "doc" | "docx" | "txt" => "Документи",
            "zip" | "rar" | "7z" | "tar" => "Архіви",
            "exe" | "msi" | "deb" => "Програми",
            _ => "Інше",
        };

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
