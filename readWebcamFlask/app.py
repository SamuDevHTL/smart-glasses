from flask import Flask, render_template, request, jsonify
import cv2
import pytesseract
import numpy as np
from PIL import Image
import base64
import io
import time

app = Flask(__name__)

# Global variables
last_frame = None
last_ocr_time = 0
ocr_interval = 1000  # milliseconds
frame_quality = 50  # JPEG quality (1-100)

def preprocess_image(frame):
    """Preprocess the image for better text detection."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    return Image.fromarray(gray)

def perform_ocr(frame):
    """Perform OCR on the frame and return the text."""
    processed_image = preprocess_image(frame)
    text = pytesseract.image_to_string(processed_image)
    return text.strip()

def process_image(image_data):
    """Process the image data from the client."""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perform OCR at specified interval
        current_time = time.time() * 1000
        if current_time - last_ocr_time >= ocr_interval:
            text = perform_ocr(frame)
            return text
        return None
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_frame():
    global last_ocr_time
    try:
        data = request.get_json()
        image_data = data.get("image")
        if not image_data:
            return jsonify({"status": "error", "message": "No image data received"})
        
        text = process_image(image_data)
        if text is not None:
            last_ocr_time = time.time() * 1000
            return jsonify({
                "status": "success",
                "text": text
            })
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/set_interval", methods=["POST"])
def set_interval():
    global ocr_interval
    try:
        data = request.get_json()
        interval = int(data.get("interval", 1000))
        if 100 <= interval <= 5000:
            ocr_interval = interval
            return jsonify({"status": "success", "interval": interval})
    except (ValueError, TypeError):
        pass
    return jsonify({"status": "error", "message": "Invalid interval"})

@app.route("/set_quality", methods=["POST"])
def set_quality():
    global frame_quality
    try:
        data = request.get_json()
        quality = int(data.get("quality", 50))
        if 1 <= quality <= 100:
            frame_quality = quality
            return jsonify({"status": "success", "quality": quality})
    except (ValueError, TypeError):
        pass
    return jsonify({"status": "error", "message": "Invalid quality"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 