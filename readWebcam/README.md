# Webcam OCR Program

A Python program that uses your computer's webcam to perform real-time Optical Character Recognition (OCR). It continuously scans for text in the webcam feed and displays the extracted text in the terminal.

## Features

- Real-time text detection from webcam feed
- Updates text every second
- Clears terminal to prevent spamming
- Image preprocessing for better text detection
- Simple interface with live webcam preview

## Requirements

1. Python 3.x
2. Tesseract OCR Engine
   - Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   - Make sure to add Tesseract to your system PATH

3. Python packages (install using `pip install -r requirements.txt`):
   - opencv-python
   - pytesseract
   - Pillow
   - numpy

## Installation

1. Clone or download this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure Tesseract OCR is installed and accessible in your system PATH

## Usage

1. Run the program:
   ```bash
   python readWebcam.py
   ```

2. The program will:
   - Open your webcam
   - Show a live preview window
   - Continuously scan for text
   - Update the terminal with detected text every second
   - Only update when new text is detected

3. To quit the program:
   - Press 'q' in the webcam preview window

## Tips for Better Text Detection

- Ensure good lighting conditions
- Hold text steady in front of the camera
- Keep text parallel to the camera
- Use clear, printed text when possible
- Make sure text is large enough to be readable

## Troubleshooting

If text detection is poor:
1. Check lighting conditions
2. Ensure Tesseract OCR is properly installed
3. Try adjusting the distance between the camera and text
4. Make sure the text is in focus
