import os
from dotenv import load_dotenv
import create_shopping_list
import send_ingredients_to_openai
import move_temp_to_trash
import process_recipe
from modify_recipe import modify_recipe  # Import modify_recipe correctly

# Get the root directory of the application (the directory where this script is located)
root_directory = os.path.dirname(os.path.abspath(__file__))

# Define the paths for the 'temp' and 'trash' folders
temp_folder_path = os.path.join(root_directory, 'temp')
trash_folder_path = os.path.join(root_directory, 'trash')

def main():
    # Load environment variables
    load_dotenv()

    # Check and create 'temp' and 'trash' directories if they don't exist
    for folder_path in [temp_folder_path, trash_folder_path]:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

    # Retrieve the API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("API key not found. Please ensure it is set in the .env file under 'OPENAI_API_KEY'.")
        return

    while True:
        # Get and process the initial recipe input
        recipe_input = process_recipe.get_recipe_input()

        # Check if recipe_input is valid (not None or empty)
        if recipe_input:
            try:
                # Process the recipe input and get the JSON file path
                json_file_path = process_recipe.process_recipe(recipe_input)
                
                # Modify the recipe JSON file as needed
                if json_file_path:  # Check if a valid path was returned
                    modify_recipe(json_file_path)
                else:
                    print("No JSON file path returned from process_recipe.")
            except Exception as e:
                print(f"Error processing recipe input: {e}")
                break
        else:
            print("No input provided. Exiting.")
            break

        # Ask if the user wants to add another recipe or continue
        next_action = input("\nIf you would like to add another recipe, please enter it now. Otherwise, hit Enter to continue:\n")

        # If the user hits Enter without inputting anything, break the loop
        if not next_action.strip():
            break
        
        # Otherwise, process the next recipe input
        if next_action:
            try:
                json_file_path = process_recipe.process_recipe(next_action)
                if json_file_path:  # Check if a valid path was returned
                    modify_recipe(json_file_path)
                else:
                    print("No JSON file path returned from process_recipe.")
            except Exception as e:
                print(f"Error processing next recipe input: {e}")
                break

    # Call the function to create a shopping list once the loop ends
    print("Creating shopping list...")
    try:
        create_shopping_list.process_and_merge_ingredients(temp_folder_path)

        # Define the input file path for the merged list
        input_file_path = os.path.join(temp_folder_path, 'mergedlist.json')

        # Send the merged ingredients list to OpenAI using the API key
        send_ingredients_to_openai.send_ingredients_list_to_openai(input_file_path, api_key)
    except Exception as e:
        print(f"Error creating shopping list or sending ingredients: {e}")

    # Move temporary files to trash
    try:
        move_temp_to_trash.move_temp_to_trash()
    except Exception as e:
        print(f"Error moving temporary files to trash: {e}")

if __name__ == '__main__':
    main()
