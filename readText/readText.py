from PIL import Image
import pytesseract
import os
import pytesseract

def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(img)
        
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def main():
    # Get the image path from user input
    image_path = input("Enter the path to your image file: ")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print("Error: File not found!")
        return
    
    # Extract text
    extracted_text = extract_text_from_image(image_path)
    
    # Print the extracted text
    print("\nExtracted Text:")
    print("-" * 50)
    print(extracted_text)
    print("-" * 50)

if __name__ == "__main__":
    main() 