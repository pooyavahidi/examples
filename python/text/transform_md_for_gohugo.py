import os
import sys
import re
import argparse
from typing import List, Dict
import yaml


def check_header_fields(front_matter: Dict, file, **kwargs) -> List[str]:
    errors = []

    # required fields
    required_fields = {"draft", "title", "date", "description", "tags"}

    # Check if all required fields are present
    for field in required_fields:
        if field not in front_matter:
            errors.append(f"Missing required field '{field}' in front matter")
        if field == "description":
            errors.extend(check_description(front_matter.get(field)))

    # Check if all required fields except 'draft' are not empty
    for field in required_fields - {"draft"}:
        if not front_matter.get(field):
            errors.append(f"Field '{field}' cannot be empty")

    return errors


def check_description(description: str) -> List[str]:
    """Validate the description field in the front matter."""
    errors = []
    if not description:
        errors.append("description cannot be empty")
    elif len(description) < 50:
        errors.append("description should be at least 50 characters long")
    elif len(description) > 150:
        errors.append("description should be at most 150 characters long")
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


def check_title(content: str, file, **kwargs) -> List[str]:
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


def transform_links(content: str, file, domain: str, **kwargs) -> List[str]:
    """
    - If the URL starts with http(s)://<domain>, drop that part so the path
      becomes absolute (e.g. '/images/foo.png').
    - If the link is a plain relative path (e.g. 'images/foo.png'), prefix it
      with '../' to be relative to the current file.
    - Every modification including domain stripping or '../' prefixing, is
      captured in the `changes` list so it can be reported and applied.

    For example, this function changes this:
    ![](images/image1.png)
    to:
    ![](../images/image1.png)

    Or this:
    [](https://domain/page1)
    to:
    [](/page1)

    """
    changes = []
    # Get prefix, url, suffix
    # Example: [prefix](url)
    pattern = r"(\[.*?\]\()([^)]+)(\))"
    modified_content = content

    for match in re.finditer(pattern, content):
        prefix, path, suffix = match.groups()
        original_link = match.group(0)
        new_path = path

        # Remove the protocol + domain if present
        domain_regex = rf"^https?://{re.escape(domain)}"
        if re.match(domain_regex, new_path):
            new_path = re.sub(domain_regex, "", new_path, count=1)
            # Ensure the resulting path is absolute
            if not new_path.startswith("/"):
                new_path = "/" + new_path

        # Add ../ for plain relative paths
        if not new_path.startswith(("/", "../", "http://", "https://")):
            new_path = f"../{new_path}"

        # Record and apply the change (if any)
        if new_path != path:
            new_link = f"{prefix}{new_path}{suffix}"
            changes.append({"old": original_link, "new": new_link})
            modified_content = modified_content.replace(
                original_link, new_link
            )

    return changes, modified_content


def transform_internal_links(content: str, file, **kwargs) -> List[str]:
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


def check_header(content: str, file, **kwargs) -> List[str]:
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


def process_files(
    markdown_files, checkers, transformers, dry_run=False, **kwargs
) -> List[Dict]:
    output = []
    for file in markdown_files:
        with open(file, "r", encoding="utf-8") as freader:
            content = freader.read()
        output_file = {"file": file, "errors": [], "changes": []}

        if checkers:
            for checker in checkers:
                output_file["errors"].extend(checker(content, file, **kwargs))

        # If there are errors, skip the transformation
        if output_file["errors"]:
            output.append(output_file)
            continue

        if transformers:
            for transformer in transformers:
                changes, content = transformer(content, file, **kwargs)
                output_file["changes"].extend(changes)

        # Save the modified content back to the file
        if not dry_run:
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
    # Example: python check_markdown.py /path/to/directory
    # If no argument is provided, the current directory is used.
    parser = argparse.ArgumentParser(
        description="Process markdown files for Hugo."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to directory containing markdown files",
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to remove from links",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run checks and changes without modifying files",
    )
    args = parser.parse_args()

    path = args.path
    domain = args.domain
    dry_run = args.dry_run

    markdown_files = get_all_markdown_files(path)

    if not markdown_files:
        print("No markdown files found.")
        sys.exit(0)

    print(f"Processing markdown files in {path} ...")
    output = process_files(
        markdown_files=markdown_files,
        checkers=[check_header, check_title],
        transformers=[transform_links, transform_internal_links],
        dry_run=dry_run,
        domain=domain,
    )

    has_errors = any(file["errors"] for file in output)
    has_changes = any(file["changes"] for file in output)

    if has_errors or has_changes:
        print_errors_and_changes(output)

    if has_errors:
        print("\033[91mErrors found.\033[0m")
        sys.exit(1)
    else:
        print("\033[92mNo errors found.\033[0m")
        sys.exit(0)
