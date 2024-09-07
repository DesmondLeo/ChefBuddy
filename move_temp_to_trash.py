import os
import shutil
from datetime import datetime

# Get the root directory of the application (the directory where this script is located)
root_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path for the 'temp' folder
temp_folder_path = os.path.join(root_directory, 'temp')

# Define the path for the 'trash' folder
trash_folder_path = os.path.join(root_directory, 'trash')

def move_temp_to_trash():
    """Move all files from the 'temp' folder to the 'trash' folder, appending a timestamp to each file."""
    # Ensure the 'trash' folder exists
    if not os.path.exists(trash_folder_path):
        os.makedirs(trash_folder_path)
    
    # Move each file from 'temp' to 'trash'
    for filename in os.listdir(temp_folder_path):
        temp_file_path = os.path.join(temp_folder_path, filename)

        # Generate a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Separate the filename and its extension
        base_name, extension = os.path.splitext(filename)

        # Create a new filename with the timestamp appended
        new_filename = f"{base_name}_{timestamp}{extension}"
        trash_file_path = os.path.join(trash_folder_path, new_filename)
        
        # Move the file to the trash folder with the new name
        shutil.move(temp_file_path, trash_file_path)
        #print(f"Moved {temp_file_path} to {trash_file_path}")

    print('cache cleared. Temp folder emptied.')

# Example usage:
# move_temp_to_trash()
