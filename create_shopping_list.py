import os
import json
from send_recipe_to_openai import send_recipe_to_openai
from dotenv import load_dotenv

def process_and_merge_ingredients(folder_path):
    # Get the root directory of the application (the directory where this script is located)
    load_dotenv()
    root_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the 'temp' folder
    output_directory = os.path.join(root_directory, 'temp')
    
    merged_ingredients = []

    # Process each .txt file in the specified folder
    #for filename in os.listdir(folder_path):
    #    if filename.endswith('.txt'):
    #        file_path = os.path.join(folder_path, filename)
    #        print(f"Processing file: {file_path}")
    #        
    #        # Call the modified connect_to_openai_api function
    #        send_recipe_to_openai(file_path, os.getenv('OPENAI_API_KEY'), disable_streaming=None)

    # After all files have been processed, merge the ingredients
    for filename in os.listdir(output_directory):
        if filename.endswith('.json'):
            json_file_path = os.path.join(output_directory, filename)
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                merged_ingredients.extend(data.get('ingredients', []))
    
    # Sort ingredients by aisle and name
    merged_ingredients.sort(key=lambda x: (x.get('aisle', '').lower(), x.get('ingredient', '').lower()))

    # Create a merged JSON object
    merged_json = {
        "ingredients": merged_ingredients
    }

    # Save the merged ingredients to a new JSON file
    merged_json_file_path = os.path.join(output_directory, 'mergedlist.json')
    with open(merged_json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(merged_json, json_file, indent=4)

    print(f"Merged JSON file successfully saved to {merged_json_file_path}")

# Example usage:
#folder_path = '/path/to/your/txt/files'
#process_and_merge_recipe_ingredients(folder_path)
