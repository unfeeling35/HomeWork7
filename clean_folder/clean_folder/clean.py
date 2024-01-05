import os
import shutil
import zipfile
import sys

from .sort import normalize, remove_empty_folders, organize_files




def main():
    if len(sys.argv) != 2:
        print("Usage: clean-folder <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        sys.exit(1)

    organize_files(folder_path)
    print("Folder sorting completed successfully.")

if __name__ == "__main__":
    main()

