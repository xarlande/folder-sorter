import os
import sys
import shutil
import platform
import subprocess

def log(msg):
    print(f"\n=== {msg} ===")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. Compile Rust CLI
    log("Building Rust CLI in Release Mode...")
    cli_dir = os.path.abspath(os.path.join(script_dir, "..", "cli"))
    if not os.path.exists(cli_dir):
        print(f"Error: CLI folder not found at {cli_dir}")
        sys.exit(1)
        
    try:
        subprocess.check_call(["cargo", "build", "--release"], cwd=cli_dir)
        print("Rust CLI compiled successfully!")
    except Exception as e:
        print(f"Error compiling Rust CLI: {e}")
        sys.exit(1)
        
    # Find compiled CLI binary
    is_windows = platform.system() == "Windows"
    binary_name = "folder-sorter.exe" if is_windows else "folder-sorter"
    cli_bin_path = os.path.join(cli_dir, "target", "release", binary_name)
    
    if not os.path.exists(cli_bin_path):
        print(f"Error: Compiled CLI binary not found at {cli_bin_path}")
        sys.exit(1)
        
    # 2. Check and Install PyInstaller
    log("Checking PyInstaller dependency...")
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("PyInstaller not found. Installing now...")
        try:
            # Install PyInstaller using current environment's pip/uv
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully!")
        except Exception as e:
            print(f"Error installing PyInstaller: {e}")
            sys.exit(1)
            
    # 3. Package with PyInstaller
    log("Packaging Application with PyInstaller...")
    
    # Setup PyInstaller arguments
    # On Windows, path separator is ';', on Unix it is ':'
    separator = ";" if is_windows else ":"
    add_binary_arg = f"{cli_bin_path}{separator}."
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--name", "FolderSorter",
        "--add-binary", add_binary_arg,
        "--clean",
        "--noconfirm",
        "main.py"
    ]
    
    # On macOS, package as a .app bundle
    if platform.system() == "Darwin":
        # PyInstaller generates a .app bundle automatically on macOS with --noconsole
        pass
        
    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        log("SUCCESS: Standalone application built successfully!")
        
        dist_dir = os.path.join(script_dir, "dist")
        if is_windows:
            app_path = os.path.join(dist_dir, "FolderSorter.exe")
            print(f"Executable is located at: {app_path}")
            # Archive it
            zip_path = os.path.join(dist_dir, "FolderSorter-Windows")
            shutil.make_archive(zip_path, 'zip', root_dir=dist_dir, base_dir="FolderSorter.exe")
            print(f"Archived to: {zip_path}.zip")
        elif platform.system() == "Darwin":
            app_path = os.path.join(dist_dir, "FolderSorter.app")
            print(f"macOS App Bundle is located at: {app_path}")
            # Archive the .app directory
            zip_path = os.path.join(dist_dir, "FolderSorter-macOS")
            shutil.make_archive(zip_path, 'zip', root_dir=dist_dir, base_dir="FolderSorter.app")
            print(f"Archived to: {zip_path}.zip")
        else:
            app_path = os.path.join(dist_dir, "FolderSorter")
            print(f"Linux binary is located at: {app_path}")
            # Archive it
            tar_path = os.path.join(dist_dir, "FolderSorter-Linux.tar.gz")
            import tarfile
            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(app_path, arcname="FolderSorter")
            print(f"Archived to: {tar_path}")
            
    except Exception as e:
        print(f"Error packaging application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
