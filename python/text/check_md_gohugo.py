import os
import sys
import re
from typing import List, Dict
import yaml


def check_header_fields(front_matter: Dict, file) -> List[str]:
    errors = []

    # required fields
    required_fields = {"draft", "title", "date", "description", "tags"}

    # Check if all required fields are present
    for field in required_fields:
        if field not in front_matter:
            errors.append(f"Missing required field '{field}' in front matter")

    # Check if all required fields except 'draft' are not empty
    for field in required_fields - {"draft"}:
        if not front_matter.get(field):
            errors.append(f"Field '{field}' cannot be empty")

    return errors


def check_header(content: str, file) -> List[str]:
    """
    Check if the markdown file has a valid Hugo front matter at the very
    beginning. For example:

    ---
    date: "2025-03-01"
    draft: false
    title: 'AI and Machine Learning'
    description: 'An introduction to AI and Machine Learning'
    tags:
        - AI
        - Machine Learning
    ---

    Args:
        content: String content of the markdown file
        file: File name for error reporting

    Returns:
        List of error messages
    """
    errors = []

    # Check if the file starts with a front matter pattern
    front_matter_pattern = r"^---\r?\n(.*?)\r?\n---\r?\n"
    match = re.match(front_matter_pattern, content, re.DOTALL)

    if not match:
        errors.append("Header is missing or invalid")
        return errors

    # Extract and validate its content
    yaml_content = match.group(1)

    # Try to parse the YAML content
    try:
        front_matter = yaml.safe_load(yaml_content)

        # Check if front_matter is a dictionary (should be for valid YAML)
        if not isinstance(front_matter, dict):
            errors.append("Front matter doesn't contain valid YAML content")
            return errors

        # Check front matter fields
        errors.extend(check_header_fields(front_matter, file))
    except yaml.YAMLError:
        errors.append("Invalid YAML in Hugo front matter")

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
            content = f.read()
        output_file = {"file": file, "errors": []}
        output_file["errors"].extend(check_header(content, file))
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
        print("No errors found.")
        exit(0)

    print("Errors found:")
    for file in output:
        if file["errors"]:
            print("-" * 50)
            print(file["file"])
            for error in file["errors"]:
                print(error)
    exit(1)
