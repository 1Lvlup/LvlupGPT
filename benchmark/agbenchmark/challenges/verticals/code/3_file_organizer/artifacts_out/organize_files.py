import argparse
import os
import shutil

def organize_files(directory_path):
    # Define a dictionary of file type groups with their corresponding file extensions
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
                        old_path = entry.path  # Full path of the current file
                        new_path = os.path.join(directory_path, folder_name, entry.name)
                        if old_path != new_path:  # Prevent moving the file if the paths are the same
                            shutil.move(old_path, new_path)  # Move the file
                            print(f"Moved {entry.name} to {folder_name}")
                        break
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # Create an ArgumentParser object to define the script's arguments
    parser = argparse.ArgumentParser(
        description="Organize files in a directory based on their file types"
    )

    # Define the directory_path argument
    parser.add_argument(
        "--directory_path",
        type=str,
        required=True,
        help="The path of the directory to be organized",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the organize_files function with the provided directory_path
    organize_files(args.directory_path)
