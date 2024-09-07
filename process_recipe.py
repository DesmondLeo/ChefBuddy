import os
import re
import scrape_with_beautifulsoup
import scrape_with_selenium
import scrape_text_from_image
import send_recipe_to_openai

# Get the root directory of the application (the directory where this script is located)
root_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path for the 'temp' folder
output_directory = os.path.join(root_directory, 'temp')

def is_valid_url(url):
    """Check if the input is a valid HTTP or HTTPS URL."""
    url_pattern = re.compile(r'^(http|https)://[^\s]+$')
    return bool(url_pattern.match(url))

def is_valid_filepath(filepath):
    """Check if the input is a valid file path (Mac or PC)."""
    return os.path.isfile(filepath)

def get_recipe_input():
    """Prompt the user for input and validate it as a URL or file path."""
    while True:
        recipe_input = input("\n\nPlease provide the full HTTP/HTTPS link or the file path to the recipe you would like to analyse, otherwise hit enter to skip this step:\n")

        if not recipe_input.strip():
            print("\nNo input provided. Continuing wtih remaining steps.")
            return None
                
        if is_valid_url(recipe_input):
            return recipe_input
        elif is_valid_filepath(recipe_input):
            return recipe_input
        else:
            print("\nInvalid input. Please enter a valid URL or file path.")
            print("Examples of valid inputs:")
            print("  - URL: http://example.com/recipe")
            print("  - File path (Mac): /Users/username/Documents/recipe.txt")
            print("  - File path (PC): C:\\Users\\username\\Documents\\recipe.txt\n")

def process_recipe(recipe_input):
    """Process a single recipe input by scraping and sending it to OpenAI."""
    save_path = None  # Initialize save_path to ensure it's defined in all branches

    if is_valid_url(recipe_input):
        # URL input: Attempt to scrape the recipe using BeautifulSoup
        save_path = scrape_with_beautifulsoup.scrape_with_beautifulsoup(recipe_input, return_filepath=True)

        # Validate if the scraping worked by checking the file contents
        if save_path and os.path.exists(save_path):
            with open(save_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"Content of {os.path.basename(save_path)}:\n{content}")
                
                # If the content contains "NO TEXT FOUND", use Selenium to scrape
                if "NO TEXT FOUND" in content:
                    print(f"'NO TEXT FOUND' detected, reprocessing with Selenium: {recipe_input}")
                    save_path = scrape_with_selenium.scrape_with_selenium(recipe_input)
        else:
            print(f"File at {save_path} does not exist. Scraping might have failed.")
    
    elif is_valid_filepath(recipe_input):
        # File path input: Process the file using the image text extraction function
        save_path = scrape_text_from_image.scrape_text_from_image(recipe_input)

    # If save_path was set and file exists, send the recipe to OpenAI for further processing
    if save_path and os.path.exists(save_path):
        print(f"Sending the processed recipe file {os.path.basename(save_path)} to OpenAI for analysis.")
        send_recipe_to_openai.send_recipe_to_openai(save_path)
    else:
        print("No valid file path available to send to OpenAI.")
