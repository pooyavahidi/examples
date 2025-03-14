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


def mask_code_blocks(content: str) -> str:
    """
    Remove code block content from markdown. This replaces code with spaces but
    keeps all newlines intact.

    Args:
        content: String content of the markdown file

    Returns:
        Content with code blocks masked (replaced with spaces while keeping
        structure intact)
    """

    def replace_with_spaces(match):
        # Keep the backticks and newlines, but replace the rest with spaces
        text = match.group(0)
        # Preserve the opening and closing backticks and all newlines
        return re.sub(r"[^\n`]", " ", text)

    # Match all code blocks (including the backticks and language identifier)
    code_block_pattern = r"```.*?```"

    return re.sub(
        code_block_pattern, replace_with_spaces, content, flags=re.DOTALL
    )


def check_title(content: str, file) -> List[str]:
    """
    Check if the markdown should not have any title in the content.
    """
    errors = []
    pattern = r"^# .+"
    content_without_code = mask_code_blocks(content)

    matches = re.finditer(pattern, content_without_code, re.MULTILINE)

    # Add matches to errors if found
    for match in matches:
        matched_title = match.group(0)
        errors.append(f"Title should not be in the content: '{matched_title}'")

    return errors


def transform_image_links(content: str, file) -> List[str]:
    """
    Transform the images url by adding `../` at the beginning of the image url.

    For example, change this:
    ![](images/image1.png)

    to this:
    ![](../images/image1.png)
    """
    changes = []
    pattern = r"(!\[.*?\]\()(.+?)(\))"
    matches = re.findall(pattern, content)

    # If no image links found, return empty changes list
    if not matches:
        return changes, content

    modified_content = content
    for prefix, path, suffix in matches:
        # Skip if path already starts with '../' or is a URL
        if (
            path.startswith("../")
            or path.startswith("http://")
            or path.startswith("https://")
        ):
            continue

        old_link = f"{prefix}{path}{suffix}"
        new_link = f"{prefix}../{path}{suffix}"

        # Record the change
        changes.append({"old": old_link, "new": new_link})
        modified_content = modified_content.replace(old_link, new_link)

    return changes, modified_content


def transform_internal_links(content: str, file) -> List[str]:
    """
    Transform the internal links by dropping `..` and add `.md` extension.

    For example, change this:
    [link](../path/file1.md#section)

    To this:
    [link](/path/file1#section)
    """

    changes = []
    pattern = r"(\[.*?\]\()(\.\.\/)(.*?)(\.md)(#.*?)(\))"
    matches = re.findall(pattern, content)

    # If no internal links found, return empty changes list
    if not matches:
        return changes, content

    modified_content = content
    for prefix, dots, filename, extension, section, suffix in matches:
        old_link = f"{prefix}{dots}{filename}{extension}{section}{suffix}"
        new_link = f"{prefix}/{filename}{section}{suffix}"

        # Record the change
        changes.append({"old": old_link, "new": new_link})
        modified_content = modified_content.replace(old_link, new_link)

    return changes, modified_content


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


def process_files(markdown_files, checkers, transformers) -> List[Dict]:
    output = []
    for file in markdown_files:
        with open(file, "r", encoding="utf-8") as freader:
            content = freader.read()
        output_file = {"file": file, "errors": [], "changes": []}

        if checkers:
            for checker in checkers:
                output_file["errors"].extend(checker(content, file))

        # If there are errors, skip the transformation
        if output_file["errors"]:
            output.append(output_file)
            continue

        if transformers:
            for transformer in transformers:
                changes, content = transformer(content, file)
                output_file["changes"].extend(changes)

        # Save the modified content back to the file
        with open(file, "w", encoding="utf-8") as fwriter:
            fwriter.write(content)

        output.append(output_file)

    return output


def print_errors_and_changes(output):
    for file in output:
        print("-" * 50)
        print(file["file"])
        if file["errors"]:
            print("Errors:")
            for i in range(len(file["errors"])):
                print(f"{i+1}. {file['errors'][i]}\n")
        if file["changes"]:
            print("Changes:")
            for i in range(len(file["changes"])):
                print(f"{i+1}. {file['changes'][i]}\n")


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

    print(f"Processing markdown files in {path} ...")
    output = process_files(
        markdown_files=markdown_files,
        checkers=[check_header, check_title],
        transformers=[transform_image_links, transform_internal_links],
    )

    has_errors = any(file["errors"] for file in output)
    has_changes = any(file["changes"] for file in output)

    if not has_errors and not has_changes:
        print("No errors or changes.")
        sys.exit(0)

    print_errors_and_changes(output)

    if has_errors:
        sys.exit(1)
