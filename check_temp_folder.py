import os

def initialise_temp_folder():
    # Get the root directory of the application (the directory where this script is located)
    root_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the 'temp' folder
    temp_folder_path = os.path.join(root_directory, 'temp')

    # Check if the 'temp' folder exists
    if not os.path.exists(temp_folder_path):
        # If it doesn't exist, create the 'temp' folder
        os.makedirs(temp_folder_path)
        print(f"'temp' folder created at {temp_folder_path}.")
    else:
        print(f"'temp' folder already exists at {temp_folder_path}.")