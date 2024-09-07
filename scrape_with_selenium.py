from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_content_sufficient(section):
    """Check if the content of the section is more than two lines or two list items."""
    text_lines = section.get_text(separator='\n').strip().splitlines()
    list_items = section.find_all('li')
    return len(text_lines) > 2 or len(list_items) > 2

def scrape_with_selenium(url):
    print(f"Attempting to scrape {url} for ingredients using Selenium.")
    
    # Set up the Selenium WebDriver (e.g., Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the webpage
        driver.get(url)
        time.sleep(3)  # Wait for the page to fully load (adjust as necessary)
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the filename from the URL
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        filename = (path_parts[-1] if path_parts[-1] else 'default') + '.txt'  # Handle empty filename
        filename = filename.replace('/', '_').replace('\\', '_')  # Sanitize the filename
        
        # Initialize a list to store the text sections
        text_sections = []

        # Define keywords to search for in headers
        ingredient_keywords = ["ingredients"]
        instruction_keywords = ["method", "instructions", "directions", "steps"]

        # Find all headers (h1, h2, h3, etc.)
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for header in headers:
            header_text = header.get_text().strip().lower()

            # Check for ingredients or instructions sections
            if any(keyword in header_text for keyword in ingredient_keywords + instruction_keywords):
                parent_section = header.find_parent(['section', 'div', 'span'], class_=True)
                while parent_section and not is_content_sufficient(parent_section):
                    parent_section = parent_section.find_parent(['section', 'div', 'span'], class_=True)

                if parent_section and is_content_sufficient(parent_section):
                    # Extract text from the section and add it to the list
                    text_sections.append(parent_section.get_text(separator='\n').strip())
                    print(f"Section found and added to text file: {parent_section.name}")  # Debug print

        # Join the text sections into a single string with two newlines separating them
        full_text = "\n\n".join(text_sections)

        # Check if text_content is empty or only contains insufficient content
        if not full_text.strip():
            full_text = "NO TEXT FOUND"

        # Get the root directory of the application (the directory where this script is located)
        root_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the path for the 'temp' folder
        temp_folder_path = os.path.join(root_directory, 'temp')

        # Ensure the 'temp' folder exists
        if not os.path.exists(temp_folder_path):
            os.makedirs(temp_folder_path)

        # Define the full path where the file will be saved in the 'temp' folder
        save_path = os.path.join(temp_folder_path, filename)

        # Save the text content to the file
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(full_text)

        print(f"Recipe sections successfully saved to {save_path}")
        return save_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None in case of an error

    finally:
        driver.quit()

# Example usage:
# scrape_with_selenium('https://www.madewithlau.com/recipes/vegetable-lo-mein')
