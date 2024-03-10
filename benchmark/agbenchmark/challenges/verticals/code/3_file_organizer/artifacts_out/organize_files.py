import argparse
import os
import shutil


def organize_files(directory_path):
    # Define file type groups
    file_types = {
        "images": [".png", ".jpg", ".jpeg"],
        "documents": [".pdf", ".docx", ".txt"],
        "audio": [".mp3", ".wav", ".flac"],
    }

    # Create the folders if they don't exist
    for folder_name in file_types.keys():
        folder_path = os.path.join(directory_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Traverse through all files and folders in the specified directory
    try:
        for entry in os.scandir(directory_path):
            if entry.is_file():
                # Get file extension
                file_extension = os.path.splitext(entry.name)[1]

                # Move files to corresponding folders
                for folder_name, extensions in file_types.items():
                    if file_extension in extensions:
                        old_path = entry.path
                        new_path = os.path.join(directory_path, folder_name, entry.name)
                        if old_path != new_path:
                            shutil.move(old_path, new_path)
                            print(f"Moved {entry.name} to {folder_name}")
                        break
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files in a directory based on their file types"
    )
    parser.add_argument(
        "--directory_path",
        type=str,
        required=True,
        help="The path of the directory to be organized",
    )

    args = parser.parse_args()

    organize_files(args.directory_path)
