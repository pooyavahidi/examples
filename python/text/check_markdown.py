import os
import sys
import re


def check_missing_images(file):
    print(f"Check missing images in {file}")
    with open(file, "r") as f:
        content = f.read()
        matches = re.findall(r"!\[.*?\](\(.*?\))?", content)
        for match in matches:
            print(f"Found {match}")

    print("-" * 50)


def get_all_markdown_files(path):
    markdown_files = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".md"):
                markdown_files.append(os.path.join(root, name))
    return markdown_files


def check_files(markdown_files):
    for file in markdown_files:
        check_missing_images(file)


if __name__ == "__main__":
    # The first argument is the path to the directory.
    # If not provided, the current directory is used.
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()

    markdown_files = get_all_markdown_files(path)
    if len(markdown_files) == 0:
        print("No markdown files found.")
        sys.exit(0)

    print(f"Checking markdown files in {path} ...")
    check_files(markdown_files)
