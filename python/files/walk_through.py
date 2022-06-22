import os


def get_dirs(path):
    dir_paths = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            dir_paths.append(os.path.join(root, d))
    return dir_paths


def get_files(path):
    file_paths = []
    for root, dirs, files in os.walk(path):
        for f in files:
            file_paths.append(os.path.join(root, f))
    return file_paths


def print_items(items):
    for i in items:
        print(i)


if __name__ == "__main__":
    path = os.getcwd()

    dirs = get_dirs(path)
    print_items(dirs)

    files = get_files(path)
    print_items(files)
