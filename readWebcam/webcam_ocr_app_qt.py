import sys
import cv2
import pytesseract
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                            QFrame, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QImage, QPixmap

class WebcamThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.cap = None
        
    def run(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)
            QThread.msleep(30)  # ~30 FPS
        
        if self.cap:
            self.cap.release()
    
    def stop(self):
        self.running = False
        self.wait()

class WebcamOCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam OCR")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize variables
        self.webcam_thread = None
        self.ocr_timer = QTimer()
        self.ocr_timer.timeout.connect(self.perform_ocr)
        
        # Set up the UI
        self.setup_ui()
        
        # Apply custom dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2d5af1;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b6bff;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QPushButton#stopButton {
                background-color: #f12d2d;
            }
            QPushButton#stopButton:hover {
                background-color: #ff3b3b;
            }
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #ffffff;
            }
            QSpinBox {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for webcam and controls
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        # Webcam display
        self.webcam_label = QLabel()
        self.webcam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.webcam_label.setMinimumSize(640, 480)
        self.webcam_label.setStyleSheet("background-color: #2b2b2b;")
        left_layout.addWidget(self.webcam_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_webcam)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_webcam)
        self.stop_button.setEnabled(False)
        
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)
        left_layout.addLayout(controls_layout)
        
        # Right panel for text display and settings
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        # Settings
        settings_layout = QHBoxLayout()
        
        self.ocr_interval = QSpinBox()
        self.ocr_interval.setRange(100, 5000)
        self.ocr_interval.setValue(1000)
        self.ocr_interval.setSuffix(" ms")
        
        settings_layout.addWidget(QLabel("OCR Interval:"))
        settings_layout.addWidget(self.ocr_interval)
        right_layout.addLayout(settings_layout)
        
        # Text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        right_layout.addWidget(self.text_display)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
    def start_webcam(self):
        self.webcam_thread = WebcamThread()
        self.webcam_thread.frame_ready.connect(self.update_webcam)
        self.webcam_thread.start()
        
        self.ocr_timer.start(self.ocr_interval.value())
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
    def stop_webcam(self):
        if self.webcam_thread:
            self.webcam_thread.stop()
            self.webcam_thread = None
        
        self.ocr_timer.stop()
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Clear webcam display
        self.webcam_label.clear()
        self.webcam_label.setText("Webcam Stopped")
        
    def update_webcam(self, frame):
        # Convert frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert frame to QImage
        height, width = frame_rgb.shape[:2]
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(self.webcam_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.webcam_label.setPixmap(scaled_pixmap)
        
    def preprocess_image(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = np.ones((1, 1), np.uint8)
        gray = cv2.dilate(gray, kernel, iterations=1)
        return Image.fromarray(gray)
        
    def perform_ocr(self):
        if self.webcam_thread and self.webcam_thread.cap is not None:
            ret, frame = self.webcam_thread.cap.read()
            if ret:
                processed_image = self.preprocess_image(frame)
                text = pytesseract.image_to_string(processed_image)
                text = text.strip()
                
                if text:
                    self.text_display.setPlainText(text)
    
    def closeEvent(self, event):
        self.stop_webcam()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = WebcamOCRApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 