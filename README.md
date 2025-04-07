# Smart Glasses OCR Applications

A collection of OCR (Optical Character Recognition) applications that can extract text from images and live webcam feed. This repository contains two main applications:

1. **Image OCR**: Extracts text from static images
2. **Webcam OCR**: Real-time text extraction from webcam feed

## Features

### Image OCR
- Extract text from image files
- Simple command-line interface
- Supports various image formats

### Webcam OCR
- Real-time text detection from webcam feed
- Modern PyQt6 GUI with dark theme
- Adjustable OCR interval
- Live webcam preview
- Continuous text updates

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
   - PyQt6

## Installation

1. Clone or download this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure Tesseract OCR is installed and accessible in your system PATH

## Usage

### Image OCR
1. Navigate to the `readText` directory
2. Run the program:
   ```bash
   python readText.py
   ```
3. Enter the path to your image file when prompted

### Webcam OCR
1. Navigate to the `readWebcam` directory
2. Run the application:
   ```bash
   python webcam_ocr_app_qt.py
   ```
3. Use the interface:
   - Click "Start" to begin webcam capture and OCR
   - Adjust OCR interval using the spin box
   - View detected text in the right panel
   - Click "Stop" to stop the webcam
   - Close the window to exit

## Tips for Better Text Detection

- Ensure good lighting conditions
- Hold text steady in front of the camera
- Keep text parallel to the camera
- Use clear, printed text when possible
- Make sure text is large enough to be readable
- For webcam OCR, adjust the interval based on your needs (lower for faster updates, higher for better performance)

## Troubleshooting

If text detection is poor:
1. Check lighting conditions
2. Ensure Tesseract OCR is properly installed
3. Try adjusting the distance between the camera and text
4. Make sure the text is in focus
5. For webcam issues:
   - Check if your webcam is properly connected
   - Ensure no other application is using the webcam
   - Try restarting the application

## Project Structure

```
smart-glasses/
├── readText/
│   ├── readText.py
│   └── requirements.txt
├── readWebcam/
│   ├── webcam_ocr_app_qt.py
│   └── requirements.txt
└── README.md
```

## License

This project is open source and available under the MIT License. 