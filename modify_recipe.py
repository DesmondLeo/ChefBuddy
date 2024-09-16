import json
import re

def modify_recipe(file_path, operation=None, ingredient_id=None, quantity=None, unittype=None, ingredient_name=None, multiplier=None):
    """
    Modify the JSON file of a recipe's ingredients based on user input or provided arguments.

    Args:
        file_path (str): The file path to the JSON file containing recipe ingredients.
        operation (str, optional): The operation to perform ('ADD', 'DELETE', 'MODIFY', 'MODIFY_ALL').
        ingredient_id (int, optional): The ID of the ingredient to delete or modify.
        quantity (str, optional): The quantity for adding or modifying an ingredient.
        unittype (str, optional): The unit type for adding or modifying an ingredient.
        ingredient_name (str, optional): The name of the ingredient to add or modify.
        multiplier (float, optional): The multiplier to adjust all quantities in the recipe.

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
        for ingredient in ingredients:
            quantity_display = ingredient['quantity'] if ingredient['quantity'] is not None else ''
            unit_display = ingredient['unittype'] if ingredient['unittype'] is not None else ''
            print(f"ID {ingredient['ID']} - {ingredient['ingredient']}: {quantity_display} {unit_display}")
    
    def add_ingredient(ingredient_name, quantity, unittype):
        new_id = max([ingredient['ID'] for ingredient in ingredients], default=0) + 1
        ingredients.append({
            'ingredient': ingredient_name, 
            'quantity': quantity, 
            'unittype': unittype,
            "aisle": "Unknown",
            'ID': new_id
        })
        display_ingredients(ingredients)

    def delete_ingredient(ingredient_id):
        nonlocal ingredients
        ingredients = [ingredient for ingredient in ingredients if ingredient['ID'] != ingredient_id]
        display_ingredients(ingredients)
    
    def modify_ingredient(ingredient_id, new_quantity=None, new_unittype=None, new_ingredient_name=None):
        for ingredient in ingredients:
            if ingredient['ID'] == ingredient_id:
                if new_quantity is not None:
                    ingredient['quantity'] = new_quantity
                if new_unittype is not None:
                    ingredient['unittype'] = new_unittype
                if new_ingredient_name is not None:
                    ingredient['ingredient'] = new_ingredient_name
                break
        else:
            print(f"Ingredient with ID {ingredient_id} not found.")
        display_ingredients(ingredients)
    
    def modify_all_quantities(multiplier):
        for ingredient in ingredients:
            try:
                if ingredient['quantity'] is not None:
                    # Attempt to convert the quantity to a float and multiply
                    original_quantity = float(ingredient['quantity'])
                    ingredient['quantity'] = str(round(original_quantity * multiplier, 2))  # Round for cleaner output
            except ValueError:
                # If quantity is not a number (e.g., "to taste"), skip modification
                print(f"Skipping non-numeric quantity for ingredient: {ingredient['ingredient']}")
        display_ingredients(ingredients)

    # Handle passed arguments for direct modification
    if operation:
        operation = operation.lower()
        if operation == 'add' and ingredient_name and (quantity is not None or unittype is not None):
            add_ingredient(ingredient_name, quantity, unittype)
        elif operation == 'delete' and ingredient_id is not None:
            delete_ingredient(ingredient_id)
        elif operation == 'modify' and ingredient_id is not None:
            modify_ingredient(ingredient_id, quantity, unittype, ingredient_name)
        elif operation == 'modify_all' and multiplier is not None:
            modify_all_quantities(multiplier)
        else:
            print("Invalid arguments provided for operation.")
    else:
        # Interactive mode if no arguments are passed
        while True:
            display_ingredients(ingredients)
            print("\nAvailable commands:")
            print(">> Add --ingredient \"{INGREDIENT_NAME}\" --quantity \"{QUANTITY}\" --unit \"{UNITTYPE}\"")
            print(">> Modify --id {ID} [--quantity \"{QUANTITY}\"] [--unit \"{UNITTYPE}\"] [--ingredient \"{INGREDIENT_NAME}\"]")
            print("   You can modify any combination of fields for the Modify command.")
            print(">> Delete --id {ID}")
            print(">> Modify_All --multiplier {MULTIPLIER}")
            print("Enter 'Done' when finished.\n")
            
            command = input("Enter your command: ").strip()
            
            # Check for 'Done' command explicitly
            if command.lower() == 'done':
                break
            
            # Refined regex patterns to match commands with IDs and optional fields
            delete_pattern = r'^delete\s+--id\s+(\d+)$'
            modify_pattern = r'^modify\s+--id\s+(\d+)(?:\s+--quantity\s+"([^"]*)")?(?:\s+--unit\s+"([^"]*)")?(?:\s+--ingredient\s+"([^"]*)")?$'
            add_pattern = r'^add\s+--ingredient\s+"([^"]+)"(?:\s+--quantity\s+"([^"]*)")?(?:\s+--unit\s+"([^"]*)")?$'
            modify_all_pattern = r'^modify_all\s+--multiplier\s+([\d.]+)$'
            
            # Parse commands for delete, modify, add, modify_all
            delete_match = re.match(delete_pattern, command, re.IGNORECASE)
            modify_match = re.match(modify_pattern, command, re.IGNORECASE)
            add_match = re.match(add_pattern, command, re.IGNORECASE)
            modify_all_match = re.match(modify_all_pattern, command, re.IGNORECASE)
            
            if delete_match:
                delete_ingredient(int(delete_match.group(1)))
            
            elif modify_match:
                ingredient_id = int(modify_match.group(1))
                new_quantity = modify_match.group(2)
                new_unittype = modify_match.group(3)
                new_ingredient_name = modify_match.group(4)
                modify_ingredient(ingredient_id, new_quantity, new_unittype, new_ingredient_name)
            
            elif add_match:
                ingredient_name = add_match.group(1)
                new_quantity = add_match.group(2)
                new_unittype = add_match.group(3)
                add_ingredient(ingredient_name, new_quantity, new_unittype)
            
            elif modify_all_match:
                multiplier = float(modify_all_match.group(1))
                modify_all_quantities(multiplier)
            
            else:
                print("Invalid command format. Please follow the instructions above.")
    
    # Update the original recipe JSON with the modified ingredients
    recipe_json['ingredients'] = ingredients
    
    # Save the modified JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(recipe_json, file, indent=2)
    
    print("\nRecipe updated successfully.")

# Example usage:
# Modify the recipe stored in the JSON file programmatically:
# modify_recipe('recipe.json', 'ADD', ingredient_name='Sugar', quantity='2', unittype='cups')
# modify_recipe('recipe.json', 'DELETE', ingredient_id=2)
# modify_recipe('recipe.json', 'MODIFY', ingredient_id=3, quantity='1', unittype='liter', ingredient_name='Milk')
# modify_recipe('recipe.json', 'MODIFY_ALL', multiplier=0.5)
