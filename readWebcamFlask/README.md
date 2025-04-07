# Webcam OCR Application

A Flask-based web application that performs real-time OCR (Optical Character Recognition) using your device's camera. The application works on both desktop and mobile devices, supporting both front and back cameras.

## Features

- Real-time camera feed with OCR processing
- Support for both front and back cameras
- Mobile device compatibility
- Adjustable OCR processing interval
- Configurable image quality
- Modern, responsive UI
- Error handling and status feedback

## Requirements

- Python 3.7 or higher
- Flask
- OpenCV (cv2)
- Pytesseract
- NumPy
- Pillow

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd readWebcamFlask
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
   - Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Grant camera permissions when prompted.

4. Use the interface:
   - Click "Start" to begin camera feed
   - Select front or back camera using the dropdown
   - Adjust OCR interval and image quality as needed
   - Click "Stop" to end the session

## Mobile Device Usage

1. Make sure your phone and computer are on the same network
2. Find your computer's local IP address
3. Access the application using:
```
http://<your-computer-ip>:5000
```
4. The application will automatically select the back camera on mobile devices

## Configuration

- **OCR Interval**: Adjust how often OCR is performed (100-5000ms)
- **Image Quality**: Control the quality of captured images (1-100%)
- **Camera Selection**: Switch between front and back cameras

## Troubleshooting

1. **Camera not working**:
   - Ensure you've granted camera permissions
   - Check if another application is using the camera
   - Try switching between front and back cameras

2. **OCR not detecting text**:
   - Adjust the image quality
   - Ensure good lighting conditions
   - Try different camera angles

3. **Mobile device issues**:
   - Access the application over HTTPS
   - Ensure both devices are on the same network
   - Check your firewall settings

## Security Notes

- The application requires camera access
- All processing is done locally on the server
- No images are stored permanently
- HTTPS is recommended for production use
