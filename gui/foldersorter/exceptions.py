"""Domain exceptions for FolderSorter application."""


class FolderSorterError(Exception):
    """Base exception class for all FolderSorter errors."""

    pass


class ConfigurationError(FolderSorterError):
    """Raised when loading or saving configuration fails."""

    pass


class SchedulerError(FolderSorterError):
    """Raised when interacting with system schedulers fails."""

    pass


class CLIBinaryError(FolderSorterError):
    """Raised when CLI binary discovery fails."""

    pass


class CompilationError(FolderSorterError):
    """Raised when compiling the Rust CLI binary fails."""

    pass
