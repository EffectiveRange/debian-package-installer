import os
import shutil
from difflib import Differ
from pathlib import Path

TEST_RESOURCE_ROOT = str(Path(os.path.dirname(__file__)).absolute())
TEST_FILE_SYSTEM_ROOT = str(Path(TEST_RESOURCE_ROOT).joinpath('test_root').absolute())
RESOURCE_ROOT = str(Path(TEST_RESOURCE_ROOT).parent.absolute())


def delete_directory(directory: str) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def create_directory(directory: str) -> None:
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def copy_file(source: str, destination: str) -> None:
    create_directory(os.path.dirname(destination))
    shutil.copy(source, destination)


def create_file(file: str, content: str) -> None:
    create_directory(os.path.dirname(file))
    with open(file, 'w') as f:
        f.write(content)


def compare_files(file1: str, file2: str) -> bool:
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    return compare_lines(lines1, lines2)


def compare_lines(lines1: list[str], lines2: list[str]) -> bool:
    all_lines_match = True

    for line in Differ().compare(lines1, lines2):
        if not line.startswith('?'):
            print(line.strip('\n'))
        if line.startswith(('-', '+', '?')):
            all_lines_match = False

    return all_lines_match
