from pathlib import Path
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class FileReadResult:
    success: bool
    content: str = ""
    error: str = ""


def read_file_input(filepath: str | None) -> FileReadResult:
    if filepath is None:
        return FileReadResult(success=False, error="No file path was provided.")

    path = Path(filepath)

    if not path.exists():
        return FileReadResult(success=False, error=f"Path '{path}' does not exist.")

    if not path.is_file():
        return FileReadResult(success=False, error=f"'{path}' exists but is not a file.")

    try:
        content = path.read_text(encoding='utf-8').strip()
        return FileReadResult(success=True, content=content)
    except UnicodeDecodeError:
        return FileReadResult(success=False, error=f"'{path}' is not a valid text file (UTF-8).")
    except OSError as e:
        return FileReadResult(success=False, error=f"Error reading '{path}': {e}")