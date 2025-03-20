import sys
import pytesseract
import pyperclip
import pyttsx3
import cv2
import numpy as np
from PIL import Image, ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from fpdf import FPDF

# Set Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class SnippingTool(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.screen_rect = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(self.screen_rect)
        self.setWindowTitle('Snipping Tool')
        self.setWindowOpacity(0.3)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.begin, self.end = QtCore.QPoint(), QtCore.QPoint()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        x1, y1 = min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y())
        x2, y2 = max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y())
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        text = self.main_window.extract_text_with_format(img)
        self.main_window.display_extracted_text(text)
        self.main_window.show()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced OCR Tool")
        self.setGeometry(100, 100, 700, 500)

        main_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.snip_button = QtWidgets.QPushButton("Snipping Tool")
        self.snip_button.clicked.connect(self.open_snipping_tool)
        button_layout.addWidget(self.snip_button)

        self.upload_button = QtWidgets.QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(self.upload_button)

        self.dark_mode_button = QtWidgets.QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        button_layout.addWidget(self.dark_mode_button)

        self.language_dropdown = QtWidgets.QComboBox()
        self.language_dropdown.addItems(["English (eng)", "Hindi (hin)", "Gujarati (guj)"])
        main_layout.addWidget(self.language_dropdown)

        self.text_display = QtWidgets.QTextEdit()
        self.text_display.setMinimumHeight(250)
        self.text_display.textChanged.connect(self.update_word_count)
        main_layout.addWidget(self.text_display)

        self.word_count_label = QtWidgets.QLabel("Word Count: 0")
        main_layout.addWidget(self.word_count_label)

        bottom_buttons = QtWidgets.QHBoxLayout()
        main_layout.addLayout(bottom_buttons)

        self.copy_button = QtWidgets.QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        bottom_buttons.addWidget(self.copy_button)

        self.save_button = QtWidgets.QPushButton("Save as PDF")
        self.save_button.clicked.connect(self.save_as_pdf)
        bottom_buttons.addWidget(self.save_button)

        self.speak_button = QtWidgets.QPushButton("Read Aloud")
        self.speak_button.clicked.connect(self.text_to_speech)
        bottom_buttons.addWidget(self.speak_button)

        self.undo_button = QtWidgets.QPushButton("Undo")
        self.undo_button.clicked.connect(self.text_display.undo)
        bottom_buttons.addWidget(self.undo_button)

        self.redo_button = QtWidgets.QPushButton("Redo")
        self.redo_button.clicked.connect(self.text_display.redo)
        bottom_buttons.addWidget(self.redo_button)

    def open_snipping_tool(self):
        self.hide()
        self.snip_tool = SnippingTool(self)
        self.snip_tool.show()

    def open_file_dialog(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.process_image(file_path)

    def get_selected_language(self):
        return self.language_dropdown.currentText().split("(")[1][:-1]

    def process_image(self, file_path):
        img = Image.open(file_path)
        text = self.extract_text_with_format(img)
        self.display_extracted_text(text)

    def extract_text_with_format(self, image):
        img_cv = np.array(image)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
        custom_config = r'--oem 3 --psm 6 preserve_interword_spaces=1'
        return pytesseract.image_to_string(gray, lang=self.get_selected_language(), config=custom_config)

    def display_extracted_text(self, text):
        self.text_display.setText(text)
        pyperclip.copy(text)

    def copy_to_clipboard(self):
        pyperclip.copy(self.text_display.toPlainText())

    def save_as_pdf(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, self.text_display.toPlainText())
            pdf.output(file_path)

    def text_to_speech(self):
        engine = pyttsx3.init()
        engine.say(self.text_display.toPlainText())
        engine.runAndWait()

    def toggle_dark_mode(self):
        dark_mode = "background-color: #2E2E2E; color: white;"
        light_mode = "background-color: white; color: black;"
        self.central_widget.setStyleSheet(dark_mode if self.central_widget.styleSheet() != dark_mode else light_mode)

    def update_word_count(self):
        self.word_count_label.setText(f"Word Count: {len(self.text_display.toPlainText().split())}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
