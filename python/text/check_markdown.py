import os
import sys
import re
from typing import List, Dict


def line_err(line, line_number, message) -> List[str]:
    errors = []
    errors.append(f">>> Line {line_number} - {message}")
    errors.append(line)
    return errors


def check_missing_images(lines: List[str], file_dir: str) -> List[str]:
    errors = []
    for i, line in enumerate(lines, start=1):
        matches = re.findall(r"!\[.*?\]\((.*?)\)", line)
        for match in matches:
            if not match:
                errors.extend(
                    line_err(line, i, "Found an image without a link")
                )
                continue
            # The path inside the parentheses should be a valid relative path
            image_path = os.path.join(file_dir, match.strip("()"))
            if not os.path.exists(image_path):
                errors.extend(line_err(line, i, f"Image not found: {match}"))
    return errors


def check_missing_links(lines: List[str]) -> List[str]:
    errors = []
    for i, line in enumerate(lines, start=1):
        matches = re.findall(r"\[.*?\]\((.*?)\)", line)
        for match in matches:
            if not match:
                errors.extend(line_err(line, i, "Found a link without a URL"))

    return errors


def get_all_markdown_files(path):
    """Get all markdown files recursively"""

    markdown_files = []
    for root, _, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".md"):
                markdown_files.append(os.path.join(root, name))
    return markdown_files


def check_files(markdown_files) -> List[Dict]:
    output = []
    for file in markdown_files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        output_file = {"file": file, "errors": []}
        output_file["errors"].extend(
            check_missing_images(lines, os.path.dirname(file))
        )
        output_file["errors"].extend(check_missing_links(lines))
        output.append(output_file)

    return output


if __name__ == "__main__":
    # Run the script with the path to the directory as an argument.
    # Example: python check_markdown.py /path/to/directory
    # If no argument is provided, the current directory is used.
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()

    markdown_files = get_all_markdown_files(path)

    if not markdown_files:
        print("No markdown files found.")
        sys.exit(0)

    print(f"Checking markdown files in {path} ...")
    output = check_files(markdown_files)

    if not any(file["errors"] for file in output):
        print("\033[92mNo errors found.\033[0m")  # Green text
        sys.exit(0)

    for file in output:
        if file["errors"]:
            print("-" * 50)
            print(file["file"], "\n")
            for error in file["errors"]:
                print(error)
    print("\033[91mErrors found.\033[0m")  # Red text
    sys.exit(1)
