import os
import json
import re
import openai
from dotenv import load_dotenv

def send_recipe_to_openai(file_path, disable_streaming=None, return_json_filepath=False):
    """
    Sends recipe content to OpenAI API, processes the response, and optionally returns the JSON file path.
    
    Args:
        file_path (str): The path to the input file (.html or .txt) containing the recipe.
        disable_streaming (bool, optional): If set, disables streaming response from OpenAI.
        return_json_filepath (bool, optional): If True, the function returns the JSON file path.
        
    Returns:
        str or None: Returns the JSON file path if return_json_filepath is True; otherwise, returns None.
    """

    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Determine file type and read content
    if file_path.endswith('.html') or file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            dynamic_content = file.read()
    else:
        raise ValueError("Unsupported file type. Please use a .html or .txt file.")

    # Extract recipe name from filename as a fallback
    filename = os.path.basename(file_path)
    recipe_name_from_filename = os.path.splitext(filename)[0].replace('-', ' ').title()

    # The base prompt with clear JSON delimiters and instructions
    base_prompt = (
        f"Below is a text extraction from the contents of a website or image. Please extract information from this file following these steps in order:\n"
        f"1. Identify the recipe name. If the recipe name is not found in the content, use '{recipe_name_from_filename}' as the recipe name.\n"
        f"2. Identify each individual ingredient required for the recipe.\n"
        f"3. For each ingredient, only extract the name of the ingredient and remove any preparation instructions associated with them, such as details on how it should be prepared (e.g., chopped, diced) or its purpose (e.g., to make a soup).\n"
        f"4. For each ingredient, standardize the unit type into one of the following standardized units:\n"
        f"   - Volume: teaspoon (tsp), tablespoon (tbsp), cup, fluid ounce (fl oz), milliliter (ml), liter (l), pint (pt), quart (qt), gallon (gal).\n"
        f"   - Weight: gram (g), kilogram (kg), ounce (oz), pound (lb).\n"
        f"   - Count: piece, clove, slice, whole, bunch, head, stalk, stick, can, jar.\n"
        f"   - Miscellaneous measurable units: dash, pinch, drop, splash.\n"
        f"5. For immeasurable or qualitative units such as 'to taste', 'as needed', 'a handful', place these in the 'unittype' field, and set the 'quantity' field to null or leave it empty. If a standard measurable unit is used with a fraction or decimal value, ensure the quantity is converted to a decimal format (e.g., 1.5 instead of fractions like ½).\n"
        f"6. Handle singular and plural forms consistently (e.g., 'clove' and 'cloves' should be standardized as 'clove').\n"
        f"7. Categorize each ingredient into one of the following shopping aisles and label it accordingly:\n"
        f"---list starts here---\n"
        f"Produce\n"
        f"Fresh meats\n"
        f"Cooked Meats\n"
        f"Milk/Butter/Cream/Cheese/Yoghurts\n"
        f"Eggs/Sugar/Bread/Baking goods\n"
        f"Oil/Jam/Tinned fruit/Honey/Spices/Stock\n"
        f"Sauces/Mayonnaise/Pickles/Rice/Pulses\n"
        f"Tinned Foods/Pasta/Soups\n"
        f"Dried fruits, seeds & nuts\n"
        f"Coffee/Cereal\n"
        f"Biscuits/Chocolate/Sweets/Tea\n"
        f"Fizzy drinks/Crackers/Nuts/Crisps\n"
        f"Cordials/Bottled water\n"
        f"Wine/Beer/Cider\n"
        f"Other\n"
        f"---list ends here---\n"
        f"Return the information enclosed between [JSON_START] and [JSON_END] in the following JSON format:\n"
        f"[JSON_START]\n"
        f"{{\n"
        f"  \"recipeName\": \"Example Recipe Name\",\n"
        f"  \"ingredients\": [\n"
        f"    {{ \"quantity\": \"X\", \"unittype\": \"unit(s)\", \"ingredient\": \"Ingredient 1\", \"aisle\": \"Aisle Name\" }},\n"
        f"    {{ \"quantity\": \"null\", \"unittype\": \"to taste\", \"ingredient\": \"Ingredient 2\", \"aisle\": \"Aisle Name\" }},\n"
        f"    {{ \"quantity\": \"X\", \"unittype\": \"unit(s)\", \"ingredient\": \"Ingredient 3\", \"aisle\": \"Aisle Name\" }}\n"
        f"  ]\n"
        f"}}\n"
        f"[JSON_END]\n\n"
        f"Below is the content to be processed:\n\n"
    )

    # Combine base prompt with dynamic content
    final_prompt = base_prompt + dynamic_content

    if disable_streaming:
        # If disable_streaming is set, generate response without streaming
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chef's bot assistant looking to extract ingredients from a recipe to create shopping list."},
                {"role": "user", "content": final_prompt}
            ],
            stream=False  # Disable streaming
        )

        # Collect the full response
        full_response = response['choices'][0]['message']['content']

    else:
        # Stream the response as it is being generated
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chef's bot assistant looking to extract ingredients from a recipe to create shopping list."},
                {"role": "user", "content": final_prompt}
            ],
            stream=True  # Enable streaming
        )

        # Stream the response as it is being generated
        full_response = ""
        for chunk in response:
            chunk_text = chunk['choices'][0]['delta'].get('content', '')
            print(chunk_text, end='')  # Print each chunk of text as it arrives
            full_response += chunk_text

        print("\n\nFull response received.")

    # Extract JSON content between [JSON_START] and [JSON_END]
    json_match = re.search(r'\[JSON_START\](.*?)\[JSON_END\]', full_response, re.DOTALL)
    if not json_match:
        print("Failed to locate JSON delimiters in the response.")
        return None if return_json_filepath else None

    json_content = json_match.group(1).strip()

    # Parse the JSON output
    try:
        result_json = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON. Error: {e}")
        return None if return_json_filepath else None

    # If recipeName is empty, use the name from the filename
    if not result_json.get('recipeName') or result_json['recipeName'] == "{{recipe_name_from_filename}}":
        result_json['recipeName'] = recipe_name_from_filename

    # Assign sequential IDs to each ingredient
    for index, ingredient in enumerate(result_json.get('ingredients', []), start=1):
        ingredient['ID'] = index

    # Define the path for saving the JSON file in the same folder as the source file
    source_directory = os.path.dirname(file_path)
    json_file_name = os.path.splitext(filename)[0] + '.json'
    json_file_path = os.path.join(source_directory, json_file_name)

    # Save the JSON content to a file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(result_json, json_file, indent=4)

    print(f"\nJSON content successfully saved to {json_file_path}")

    # Return the JSON file path if requested
    if return_json_filepath:
        return json_file_path

    return None
