import os
import re
import shutil


def update_imports(file_path: str) -> None:
    """
    Updates import statements in a given Python file.

    This function reads a file line by line, identifies import statements that
    start with 'from energy_manager.', and modifies them to replace it with
    'from src_copy.energy_manager.'. The updated contents are then written back
    to the same file, effectively modifying it in place.

    Args:
        file_path: Path to the file that needs to be updated.

    """
    with open(file_path, "r") as f:
        content = f.readlines()

    updated_content = []
    for line in content:
        modified_line = re.sub(
            r'^(from\s+energy_manager\.)',
            r'from src_copy.energy_manager.',
            line
        )
        updated_content.append(modified_line)

    with open(file_path, "w") as f:
        f.writelines(updated_content)

def modify_imports(src_copy: str) -> None:
    """
    Modifies the imports in Python files within a specified directory tree.

    This function iterates through all files in a given directory and subdirectories,
    identifies Python files, and applies a modification to their imports using
    the `update_imports` function. The intended purpose is to ensure that all
    imports in the identified Python files conform to a specific format or standard.

    Args:
        src_copy: The root directory path where Python files are located and whose
            imports need to be modified.

    """
    for root, _, files in os.walk(src_copy):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_imports(file_path)


def copy_and_modify_imports(src, src_copy):
    """
    Copies the contents of the source directory to a new location and modifies imports
    within the copied files.

    This function checks if the source directory exists, copies its contents to the
    destination directory (overwriting existing files), and performs modifications on
    the imports in the copied files. If the source directory does not exist or an
    error occurs during the process, an appropriate message is printed.

    Args:
        src (str): The path to the source directory to be copied.
        src_copy (str): The destination directory where the source directory will
            be copied to, with modifications to the imports.
    """
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return

    try:
        shutil.copytree(src, src_copy, dirs_exist_ok=True)
        print(f"Copied contents from '{src}' to '{src_copy}', overwriting existing files.")
        modify_imports(src_copy)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    copy_and_modify_imports(src="src", src_copy="src_copy",)

