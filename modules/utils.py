import gc
import json
import os
import shutil
import imageio_ffmpeg as ffmpeg


class EditorUtils:
    @staticmethod
    def cleanup_temp(temp_folder_path: str = "temp/"):
        if not os.path.exists(temp_folder_path):
            print(f"The folder '{temp_folder_path}' does not exist.")
            return

        # Iterate through the contents of the temp folder
        for item in os.listdir(temp_folder_path):
            item_path = os.path.join(temp_folder_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    # Remove file or symlink
                    os.unlink(item_path)
                    print(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    # Remove directory and its contents
                    shutil.rmtree(item_path)
                    print(f"Deleted directory: {item_path}")
            except Exception as e:
                print(f"Failed to delete {item_path}. Reason: {e}")

    @staticmethod
    def load_json(json_file_path: str):
        try:
            # Open and read the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: The file '{json_file_path}' does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
        return None
    
    @staticmethod
    def get_filenames_in_directory(directory, file_extension=None):
        """
        Get a list of filenames in a specified directory.
        
        :param directory: Path to the directory to list files from.
        :param file_extension: Optional file extension filter (e.g., ".mp3").
        :return: List of filenames in the directory.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        # List all files in the directory
        filenames = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))  # Only include files
        ]

        # Filter by file extension if specified
        if file_extension:
            filenames = [f for f in filenames if f.lower().endswith(file_extension.lower())]

        return filenames
    
    @staticmethod
    def get_folders_in_directory(directory):
        """
        Get a list of folder names in a specified directory.

        :param directory: Path to the directory to list folders from.
        :return: List of folder names in the directory.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        # List all folders in the directory
        folder_names = [
            f for f in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, f))  # Only include folders
        ]

        return folder_names

    @staticmethod
    def cleanup_file_readers():
        for obj in gc.get_objects():
            if "FFMPEG" in str(type(obj)):  # Check if "FFMPEG" is in the type string
                try:
                    obj.close()
                except Exception:
                    pass  # Ignore errors if already closed

        gc.collect()