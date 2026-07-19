"""FolderSorter GUI Application Entry Point."""

from foldersorter.ui.app import FolderSorterApp


def main() -> None:
    """Main application execution function."""
    app = FolderSorterApp()
    app.mainloop()


if __name__ == "__main__":
    main()