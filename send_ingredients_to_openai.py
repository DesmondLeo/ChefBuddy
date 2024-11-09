import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def send_ingredients_list_to_openai(input_file_path, api_key):
    # Set the OpenAI API key

    # Read the input JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_data = json.load(file)

    # Create the prompt for OpenAI
    base_prompt = (
        "You are given a JSON list of ingredients with quantities and aisles. "
        "Your task is to create a final shopping list that sums up the quantities "
        "of identical ingredients and organizes them by aisle. The result should be a single list where each ingredient "
        "appears only once with its total quantity, and the ingredients are grouped by aisle.\n\n"
        "If any ingredient has \"aisle\": \"Unknown\", use the following aisles list from the initial step to correctly categorize the ingredient:\n"
        "---list starts here---\n"
        "Produce\n"
        "Fresh meats\n"
        "Cooked Meats\n"
        "Milk/Butter/Cream/Cheese/Yoghurts\n"
        "Eggs/Sugar/Bread/Baking goods\n"
        "Oil/Jam/Tinned fruit/Honey/Spices/Stock\n"
        "Sauces/Mayonnaise/Pickles/Rice/Pulses\n"
        "Tinned Foods/Pasta/Soups\n"
        "Dried fruits, seeds & nuts\n"
        "Coffee/Cereal\n"
        "Biscuits/Chocolate/Sweets/Tea\n"
        "Fizzy drinks/Crackers/Nuts/Crisps\n"
        "Cordials/Bottled water\n"
        "Wine/Beer/Cider\n"
        "Other\n"
        "---list ends here---\n\n"
        "If the correct aisle cannot be confidently determined, categorize it as 'Other'.\n\n"
        "It is **critical** that you return the output **only** between the markers [JSON_START] and [JSON_END]. "
        "Make sure the output is enclosed in these exact markers.\n\n"
        "Please return the final list in the following JSON format, organized by aisle:\n"
        "[JSON_START]\n"
        "{\n"
        "  \"shoppingList\": {\n"
        "    \"Aisle 1\": [\n"
        "      {\"ingredient\": \"Ingredient 1\", \"totalQuantity\": \"X unit(s)\"},\n"
        "      {\"ingredient\": \"Ingredient 2\", \"totalQuantity\": \"X unit(s)\"}\n"
        "    ],\n"
        "    \"Aisle 2\": [\n"
        "      {\"ingredient\": \"Ingredient 3\", \"totalQuantity\": \"X unit(s)\"}\n"
        "    ]\n"
        "  }\n"
        "}\n"
        "[JSON_END]\n\n"
        "Below is the list of ingredients:\n\n"
    )


    # Convert the input data to a string to append to the prompt
    ingredient_list = json.dumps(input_data, indent=4)
    final_prompt = base_prompt + ingredient_list

    # Call OpenAI's API with streaming enabled
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are chef's assistant and are responsible for creating a single, organized shopping lists from a list of ingredients listed for multiple recipes."},
            {"role": "user", "content": final_prompt}
        ],
        stream=True  # Enable streaming
    )

    # Stream the response as it is being generated
    full_response = ""
    print("\nStreaming Response:")
    for chunk in response:
        try:
            # Ensure we are accessing a dictionary or object with 'content' attribute
            chunk_delta = chunk.choices[0].delta
            chunk_text = chunk_delta.content if hasattr(chunk_delta, 'content') else ''
        except (KeyError, AttributeError) as e:
            # Print the error to help diagnose any issues
            print(f"Error accessing content in chunk: {e}")
            chunk_text = ''

        print(chunk_text, end='')  # Print each chunk of text as it arrives
        full_response += chunk_text if chunk_text is not None else ''

    print("\n\nFull response received.")

    # Try to extract JSON content between [JSON_START] and [JSON_END]
    json_match = re.search(r'\[JSON_START\](.*?)\[JSON_END\]', full_response, re.DOTALL)

    if not json_match:
        print("Failed to locate JSON delimiters in the response.")
        # Try to extract JSON-like content from the raw response
        json_start = full_response.find("{")
        json_end = full_response.rfind("}")
        if json_start != -1 and json_end != -1:
            json_content = full_response[json_start:json_end+1].strip()
            print("Extracted JSON-like content:\n", json_content)
        else:
            print("Failed to extract JSON-like content.")
            return
    else:
        json_content = json_match.group(1).strip()

    # Parse the JSON output
    try:
        shopping_list = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON. Error: {e}")
        return

    # Save the final shopping list JSON file
    output_folder = os.path.dirname(input_file_path)
    json_file_name = 'final_shopping_list.json'
    json_file_path = os.path.join(output_folder, json_file_name)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(shopping_list, json_file, indent=4)

    print(f"\nFinal shopping list successfully saved to {json_file_path}")

    # Print out the shopping list in the specified format with Aisle names in all caps
    print("\nFormatted Shopping List:")
    for aisle, items in shopping_list.get('shoppingList', {}).items():
        print(f"{aisle.upper()}")  # Print the aisle name in all caps
        for item in items:
            quantity = item.get('totalQuantity', 'N/A')
            ingredient = item.get('ingredient', 'N/A')
            print(f"{quantity} {ingredient}")
        print()  # Add an empty line between aisles for clarity

# Example usage:
# input_file_path = '/Users/michelleleo/Downloads/Output/mergedlist.json'
# send_merged_list_to_openai(input_file_path)