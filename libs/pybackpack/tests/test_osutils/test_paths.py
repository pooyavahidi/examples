import pytest
from pybackpack.osutils.paths import get_files


# Using pytest tempdir fixture which creates a temporary directory and
# automatically cleans it up after the test.
def setup_files_and_dirs(tmpdir):
    # Create dir1 with some sample files and directories

    dir1 = tmpdir.mkdir("dir1")
    dir1.join("file1.yml").write("content")
    dir1.join("file2.yaml").write("content")
    dir1.join("file1.dev.yml").write("content")
    dir1.join("file2.dev.yaml").write("content")
    dir1.join("file3.txt").write("content")
    dir1.join("file4.py").write("content")
    dir1.join("file5.yamld").write("content")

    # Add a subdirectory
    dir1_sub1 = dir1.mkdir("dir1_sub1")
    dir1_sub1.join("file1.txt").write("content")
    dir1_sub1.join("file2.txt").write("content")

    return tmpdir


def test_get_files_all_files(tmpdir):
    base_dir = setup_files_and_dirs(tmpdir)

    # Get all the files
    files = get_files(base_dir)
    assert len(files) == 9

    # Get all files from an unknown directory, produce error
    with pytest.raises(FileNotFoundError):
        get_files("unknown")

    # Ignore errors and return empty list
    files = get_files("unknown", ignore_errors=True)
    assert len(files) == 0
    files = get_files("", ignore_errors=True)
    assert len(files) == 0
    files = get_files(None, ignore_errors=True)
    assert len(files) == 0


def test_get_files(tmpdir):
    base_dir = setup_files_and_dirs(tmpdir).join("dir1")

    # Get all the yaml files
    files = get_files(base_dir, include_patterns=[r".*\.ya?ml$"])
    assert len(files) == 4
    assert {"file3.txt", "file4.py"} not in {file.name for file in files}

    # Get all the files except txt and py files
    files = get_files(base_dir, exclude_patterns=[r".*\.txt", r".*\.py"])
    assert len(files) == 5
    assert {"file3.txt", "file4.py"} not in {file.name for file in files}

    # Get all the yaml files except the ones with dev in the name
    files = get_files(
        base_dir,
        include_patterns=[r".*\.ya?ml$"],
        exclude_patterns=[r".*dev.*"],
    )
    assert len(files) == 2
    assert {"file1.dev.yml", "file2.dev.yaml"} not in {
        file.name for file in files
    }

    # Finding no files with the given patterns
    files = get_files(base_dir, include_patterns=[r".*\.cpp"])
    assert len(files) == 0

    # All *.txt files in all directories
    files = get_files(base_dir, include_patterns=[r".*\.txt"])
    assert len(files) == 3

    # Find a particular file
    file_name = "file3"
    files = get_files(base_dir, include_patterns=[rf"{file_name}\.txt"])
    assert len(files) == 1
