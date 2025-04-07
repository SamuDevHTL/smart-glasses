import cv2
import pytesseract
import numpy as np
from PIL import Image
import time
import os

def preprocess_image(frame):
    """
    Preprocess the image to improve text detection.
    
    Args:
        frame: OpenCV image frame
        
    Returns:
        PIL Image: Preprocessed image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Apply dilation to connect text components
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    
    # Convert to PIL Image
    return Image.fromarray(gray)

def capture_and_extract_text():
    """
    Continuously capture from webcam and extract text using OCR.
    Updates the terminal with new text every second.
    """
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return "Error: Could not open webcam"
        
        print("Press 'q' to quit")
        print("Scanning for text...")
        
        last_text = ""
        last_update = time.time()
        
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not capture frame")
                break
            
            # Display the frame
            cv2.imshow('Webcam - Press q to quit', frame)
            
            # Check if it's time to update (every 1 second)
            current_time = time.time()
            if current_time - last_update >= 1.0:
                # Preprocess the image
                processed_image = preprocess_image(frame)
                
                # Extract text using pytesseract
                text = pytesseract.image_to_string(processed_image)
                text = text.strip()
                
                # Only update if the text has changed
                if text != last_text:
                    # Clear the terminal
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Press 'q' to quit")
                    print("\nExtracted Text:")
                    print("-" * 50)
                    print(text)
                    print("-" * 50)
                    last_text = text
                
                last_update = current_time
            
            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the webcam
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    print("Webcam OCR Program")
    print("------------------")
    capture_and_extract_text()

if __name__ == "__main__":
    main() 