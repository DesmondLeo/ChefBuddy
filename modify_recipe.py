import json
import re

def modify_recipe(file_path):
    """
    Modify the JSON file of a recipe's ingredients based on user input in a single command.
    
    Args:
        file_path (str): The file path to the JSON file containing recipe ingredients.
        
    Returns:
        None: The function updates the JSON file directly.
    """
    
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        recipe_json = json.load(file)
    
    ingredients = recipe_json.get('ingredients', [])
    
    # Helper function to display the ingredients
    def display_ingredients(ingredients):
        print("\nCurrent Ingredients:")
        for i, ingredient in enumerate(ingredients, start=1):
            print(f"{i}. {ingredient['ingredient']}: {ingredient['quantity']}")
    
    display_ingredients(ingredients)
    
    # Instructions for modifying the recipe
    print("\n\nDo you want to modify this recipe? If so, use the following commands to edit this recipe:")
    print(">> Delete \"{INGREDIENT_NAME}\"")
    print(">> Change \"{INGREDIENT_NAME}\" to \"{QUANTITY}\"")
    print(">> Add \"{INGREDIENT_NAME}\" Quantity \"{QUANTITY}\"")
    print("Enter 'Done' when finished.")
    
    while True:
        command = input("Enter the modification you would like to make or type 'Done' to exit: ").strip()
        
        if command.lower() == 'done':
            break
        
        # Regex patterns to match commands with ingredients and quantities in quotes
        delete_pattern = r'^delete\s+"([^"]+)"$'
        change_pattern = r'^change\s+"([^"]+)"\s+to\s+"([^"]+)"$'
        add_pattern = r'^add\s+"([^"]+)"\s+quantity\s+"([^"]+)"$'
        
        # Parse commands for delete, change, add
        delete_match = re.match(delete_pattern, command, re.IGNORECASE)
        change_match = re.match(change_pattern, command, re.IGNORECASE)
        add_match = re.match(add_pattern, command, re.IGNORECASE)
        
        if delete_match:
            # Extract ingredient name to delete
            ingredient_name = delete_match.group(1)
            ingredients = [ingredient for ingredient in ingredients if ingredient['ingredient'].lower() != ingredient_name.lower()]
            display_ingredients(ingredients)
        
        elif change_match:
            # Extract ingredient name and new quantity to change
            ingredient_name = change_match.group(1)
            new_quantity = change_match.group(2)
            
            # Find and update the ingredient's quantity
            for ingredient in ingredients:
                if ingredient['ingredient'].lower() == ingredient_name.lower():
                    ingredient['quantity'] = new_quantity
                    break
            else:
                print(f"Ingredient '{ingredient_name}' not found.")
            display_ingredients(ingredients)
        
        elif add_match:
            # Extract ingredient name and quantity to add
            new_ingredient = add_match.group(1)
            new_quantity = add_match.group(2)
            ingredients.append({'ingredient': new_ingredient, 'quantity': new_quantity})
            display_ingredients(ingredients)
        
        else:
            print("Invalid command. Please use 'Delete \"{INGREDIENT_NAME}\"', 'Change \"{INGREDIENT_NAME}\" to \"{QUANTITY}\"', or 'Add \"{INGREDIENT_NAME}\" Quantity \"{QUANTITY}\"'.")
    
    # Update the original recipe JSON with the modified ingredients
    recipe_json['ingredients'] = ingredients
    
    # Save the modified JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(recipe_json, file, indent=2)
    
    print("\nRecipe updated successfully.")

# Example usage
# Assuming the file path to the JSON file is 'recipe.json'
# file_path = 'recipe.json'

# Modify the recipe stored in the JSON file
# modify_recipe(file_path)
