import re
from pathlib import Path
from typing import List, Optional


def get_files(
    dir_path: str,
    include_names: Optional[List[str]] = None,
    exclude_names: Optional[List[str]] = None,
    recursive: bool = True,
    ignore_errors: bool = False,
) -> List[Path]:
    """Returns a list of files in the dir_path directory.

    Args:
        dir_path: The directory to search for files.
        include_names: A list of regular expressions to match the filenames.
        by default, all files are included i.e. include_patterns=[".*"].
        exclude_names: A list of regular expressions to exclude the
            filenames.
        recursive: If True, search recursively in the dir_path directory.
        default is True.
        ignore_errors: If True, ignore any errors while searching for files.
    """

    files = []

    # Check if the dir_path exists
    if not dir_path or not Path(dir_path).exists():
        if ignore_errors:
            return files

        raise FileNotFoundError(f"Directory {dir_path} does not exist.")

    # If include_patterns is None, then include all files
    if include_names is None:
        include_names = [r".*"]

    # Get files based on the value of recursive
    if recursive:
        paths = list(Path(dir_path).rglob("*"))
    else:
        paths = list(Path(dir_path).glob("*"))

    for path in paths:
        # Skip directories or other non-files
        if not path.is_file():
            continue

        should_include = any(
            re.search(pattern, path.name) for pattern in include_names
        )
        if not should_include:
            continue

        if exclude_names:
            should_exclude = any(
                re.search(pattern, path.name) for pattern in exclude_names
            )
            if should_exclude:
                continue

        files.append(path)

    return files
