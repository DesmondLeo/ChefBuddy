import pytesseract
from PIL import Image
import os
import cv2
import numpy as np

def adjust_contrast(gray_image):
    alpha = 1.5  # Contrast control (1.0-3.0). Adjust as needed.
    beta = 0     # Brightness control (0-100). Adjust as needed.
    adjusted = cv2.convertScaleAbs(gray_image, alpha=alpha, beta=beta)
    return adjusted

def preprocess_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if img is None:
        raise ValueError(f"Failed to load image from path: {image_path}. Please check the file format and path.")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adjust contrast
    gray = adjust_contrast(gray)
    # Optionally save the image for debugging
    # cv2.imwrite('gray_contrast.png', gray)

    # Apply adaptive thresholding to binarize the image
    binary = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        15, 3  # Adjusted parameters
    )
    # Optionally save the image for debugging
    # cv2.imwrite('binary.png', binary)

    # Remove noise by applying median blur
    denoised = cv2.medianBlur(binary, 3)
    # Optionally save the image for debugging
    # cv2.imwrite('denoised.png', denoised)

    # Return the processed image in PIL format
    return Image.fromarray(denoised)

def scrape_text_from_image(image_path):
    try:
        # Verify the image path exists
        if not os.path.exists(image_path):
            print(f"Image file not found at path: {image_path}")
            return None

        # Preprocess the image to improve OCR results
        img = preprocess_image(image_path)

        # Set Tesseract configuration for better accuracy
        custom_config = r'--oem 3 --psm 3'

        # Extract text from the image using Tesseract with custom configuration
        text = pytesseract.image_to_string(img, config=custom_config)

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
# scrape_text_from_image('/path/to/your/image.jpg')
