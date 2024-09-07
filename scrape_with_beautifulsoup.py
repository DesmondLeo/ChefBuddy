import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def scrape_with_beautifulsoup(url, return_filepath=False):
    print(f"Attempting to scrape {url} for ingredients using beautifulsoup.")
    save_path = None
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

        # Set up a session with retry strategy
        session = requests.Session()
        retries = Retry(total=1, backoff_factor=1, status_forcelist=[502, 503, 504, 522, 524])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # Send a GET request to the URL with headers and a timeout
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the path from the URL and convert it to a valid filename
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        filename = (path_parts[-1] if path_parts[-1] else 'default') + '.txt'
        filename = unquote(filename).replace('/', '_').replace('\\', '_')  # Sanitize the filename

        # Define keywords to search for in headers
        ingredient_keywords = ["ingredients"]
        instruction_keywords = ["method", "instructions", "directions", "steps", "preparation"]

        # Find all headers (h1, h2, h3, etc.)
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        text_content = ""

        def is_content_sufficient(section):
            """Check if the content of the section has more than 10 words."""
            text = section.get_text(separator='\n').strip()
            word_count = len(text.split())
            return word_count > 10

        for header in headers:
            header_text = header.get_text().strip().lower()

            # Check for ingredients or instructions sections
            if any(keyword in header_text for keyword in ingredient_keywords + instruction_keywords):
                parent_section = header.find_parent(['section', 'div', 'span'], class_=True)
                while parent_section and not is_content_sufficient(parent_section):
                    parent_section = parent_section.find_parent(['section', 'div', 'span'], class_=True)

                if parent_section and is_content_sufficient(parent_section):
                    # Append only the text content of the section
                    text_content += parent_section.get_text(separator='\n').strip() + "\n\n"
                    print(f"Section found and added to text: {parent_section.name}")  # Debug print

        # Check if text_content is empty or only contains insufficient content
        if not text_content.strip():
            text_content = "NO TEXT FOUND"

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
            file.write(text_content)

        print(f"Recipe sections successfully saved to {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
        # Save "NO TEXT FOUND" in case of a request error
        save_path = handle_no_text_found(url)

    except IOError as e:
        print(f"Error occurred while saving the file: {e}")
        save_path = handle_no_text_found(url)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        save_path = handle_no_text_found(url)
    
    if return_filepath:
        return(save_path)

def handle_no_text_found(url):
    """Handle saving 'NO TEXT FOUND' when an error occurs."""
    # Get the root directory of the application (the directory where this script is located)
    root_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the 'temp' folder
    temp_folder_path = os.path.join(root_directory, 'temp')

    # Ensure the 'temp' folder exists
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    # Extract the path from the URL and convert it to a valid filename
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    filename = (path_parts[-1] if path_parts[-1] else 'default') + '.txt'
    filename = unquote(filename).replace('/', '_').replace('\\', '_')  # Sanitize the filename

    # Define the full path where the file will be saved in the 'temp' folder
    save_path = os.path.join(temp_folder_path, filename)

    # Save "NO TEXT FOUND" to the file
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write("NO TEXT FOUND")
    print(f"'NO TEXT FOUND' saved to {save_path} to be picked up by the Selenium processor.")

    return save_path

# Example usage:
# scrape_and_save_beautifulsoup('https://chejorge.com/2020/07/24/vegan-dan-dan-noodles/')
