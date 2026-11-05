import os
import sys
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QFrame, QComboBox, QPlainTextEdit
)

from main import run_conversion, set_log_widget, set_convert_button, show_message_func
from main import set_main_window
class GreenSquareWidget(QWidget):
    def __init__(self, parent=None, color="gray"):
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(20, 20)  # Square size

    def update_color(self, color_name):
        self._color = QColor(color_name)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.PRODUCT_NAME = "FLOWBIT"
        self.current_year = datetime.now().year
        self.BUILD_NUMBER = "1002"
        self.VERSION_FULL = "1.0.3"

        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.setWindowIcon(QIcon(self.resource_path("assets/logo.ico")))
        self.setWindowTitle("Selectable Layout Counter")
        self.setFixedSize(600, 150)
        self.init_ui()
        set_main_window(self)  # ✅ Register self as main window

    def init_ui(self):
        layout = QVBoxLayout()

        # File inputs
        self.file1_input = QLineEdit(self)
        file1_button = QPushButton("Browse", self)
        file1_button.clicked.connect(lambda: self.select_file_pdf(self.file1_input))
        file1_layout = QHBoxLayout()
        file1_layout.addWidget(QLabel("PDF File:"))
        file1_layout.addWidget(self.file1_input)
        file1_layout.addWidget(file1_button)

        # ComboBox
        layout_combo = QHBoxLayout()
        layout_combo.addWidget(QLabel("Choose color:"))
        self.combo = QComboBox()
        self.combo.addItem("Select color")
        self.combo.addItem("All colors", "all")
        self.combo.addItem("Black", "blk")
        self.combo.addItem("Red", "red")
        self.combo.addItem("Green", "green")
        self.combo.addItem("Blue", "blue")
        self.combo.addItem("Orange", "orange")
        self.combo.addItem("White", "white")
        self.combo.addItem("Yellow", "yellow")
        self.combo.addItem("Purple", "purple")
        self.combo.currentIndexChanged.connect(self.option_changed)
        layout_combo.addWidget(self.combo)

        self.color_preview = GreenSquareWidget(self)
        layout_combo.addWidget(self.color_preview)

        # Export button
        self.convert_button = QPushButton("Export XLSX", self)
        self.convert_button.setEnabled(False)  # 🔒 Disabled by default
        self.convert_button.clicked.connect(self.convert_doc)
        set_convert_button(self.convert_button)  # ✅ Register log widget

        # Log area
        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        set_log_widget(self.log_area)  # ✅ Register log widget


        layout.addLayout(file1_layout)
        # layout.addLayout(file2_layout)
        layout.addLayout(layout_combo)
        layout.addWidget(self.log_area)
        self.log_area.setVisible(False)
        layout.addWidget(self.convert_button)

        # Footer line
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Version label
        label_text = f"{self.PRODUCT_NAME} © {self.current_year} All rights reserved. Build {self.BUILD_NUMBER} Version {self.VERSION_FULL}"
        label = QLabel(label_text, self)
        layout.addWidget(label)

        self.setLayout(layout)

    def option_changed(self, index):
        self.color = self.combo.itemData(index)
        if self.color:
            self.color_preview.update_color(self.color)
            self.refresh_log_widget()
        else:
            self.color_preview.update_color("gray")
            self.refresh_log_widget()

    def refresh_log_widget(self):
        self.log_area.clear()
        self.log_area.setVisible(True)
        pdf_path = self.file1_input.text()
        if pdf_path:
            output_file = None
            # output_dir = os.path.dirname(pdf_path)
            # output_file = os.path.join(output_dir, "output.xlsx")
            run_conversion(pdf_path, output_file, self.color)
        else:
            msg = "Please select a PDF file."
            show_message_func(msg)
            #self.log_area.appendPlainText("Please select a PDF file.")

    def select_file_pdf(self, input_field):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            input_field.setText(file_path)

    def select_directory(self, input_field):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory_path:
            input_field.setText(directory_path)

    def convert_doc(self):
        pdf_path = self.file1_input.text()
        color = self.color
        if pdf_path:
            output_dir = os.path.dirname(pdf_path)
            output_file = os.path.join(output_dir, "output.xlsx")
            run_conversion(pdf_path, output_file, color)
        else:
            print("Please select a PDF file.")

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSelector()
    window.show()
    sys.exit(app.exec())
