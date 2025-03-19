import sys
import pytesseract
from PIL import Image, ImageGrab
import pyperclip
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np

# Set the Tesseract-OCR path explicitly
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class SnippingTool(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        screen = QtWidgets.QApplication.primaryScreen()
        self.screen_rect = screen.availableGeometry()
        self.setGeometry(self.screen_rect)
        self.setWindowTitle('Snipping Tool')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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

        try:
            text = pytesseract.image_to_string(img, lang='eng')
            self.main_window.display_extracted_text(text)
        except Exception as e:
            self.main_window.display_extracted_text(f'OCR Error: {e}')

        self.main_window.show()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Snipping Tool")
        self.setGeometry(100, 100, 600, 450)

        # Layout Setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Left Panel
        self.left_panel = QtWidgets.QVBoxLayout()

        self.snip_button = QtWidgets.QPushButton("Snipping Tool")
        self.snip_button.clicked.connect(self.open_snipping_tool)
        self.left_panel.addWidget(self.snip_button)

        self.drop_area = QtWidgets.QPushButton("Drop Image / Click to Upload")
        self.drop_area.setStyleSheet("border: 2px dashed gray; padding: 40px;")
        self.drop_area.clicked.connect(self.open_file_dialog)
        self.left_panel.addWidget(self.drop_area)

        self.close_button = QtWidgets.QPushButton("Exit")
        self.close_button.setStyleSheet("color: red; font-weight: bold;")
        self.close_button.clicked.connect(self.close_application)
        self.left_panel.addWidget(self.close_button)

        layout.addLayout(self.left_panel)

        # Right Panel
        self.text_display = QtWidgets.QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("border: 1px solid black; padding: 10px;")
        layout.addWidget(self.text_display, 1)

    def open_snipping_tool(self):
        self.hide()
        self.snip_tool = SnippingTool(self)
        self.snip_tool.show()

    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg)",
                                                             options=options)
        if file_path:
            self.process_image(file_path)
            QtWidgets.QMessageBox.information(self, "Image Uploaded", "Image successfully uploaded for OCR processing.")

    def display_extracted_text(self, text):
        self.text_display.setText(f"Extracted Text:\n{text}")
        pyperclip.copy(text)

    def process_image(self, file_path):
        img = Image.open(file_path)
        try:
            text = pytesseract.image_to_string(img, lang='eng')
            self.display_extracted_text(text)
        except Exception as e:
            self.display_extracted_text(f'OCR Error: {e}')

    def close_application(self):
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
