import pytesseract
from PIL import Image
import os

def scrape_text_from_image(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Extract text from the image using Tesseract
        text = pytesseract.image_to_string(img)
        
        # Get the root directory of the application (the directory where this script is located)
        root_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the path for the 'temp' folder
        temp_folder_path = os.path.join(root_directory, 'temp')

        # Ensure the 'temp' folder exists
        if not os.path.exists(temp_folder_path):
            os.makedirs(temp_folder_path)

        # Get the base name of the image file (without extension)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Define the path for the text file in the 'temp' folder
        text_file_path = os.path.join(temp_folder_path, base_name + '.txt')
        
        # Save the extracted text to the text file
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        
        print(f"Text successfully extracted and saved to {text_file_path}")
        return text_file_path

    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None  # Return None in case of an error

# Example usage:
# scrape_text_from_image('/path/to/your/image.png')
