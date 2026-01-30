use clap::Parser;

mod config;
mod file_organizer;

use config::load_config;
use file_organizer::organize_files;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    path: String,

    #[arg(short, long)]
    output: Option<String>,
}

fn main() {
    let args = Args::parse();
    let config = load_config();

    let source_dir = args.path;
    let target_dir = args.output.unwrap_or_else(|| source_dir.clone());

    organize_files(&source_dir, &target_dir, &config);
}
