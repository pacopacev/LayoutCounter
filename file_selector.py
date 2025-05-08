import os
import sys
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QFrame
)
from PyQt6.uic.properties import QtGui

from main import run_conversion  # Import the function from main.py

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()

        # Hide maximize button by removing resizing
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.setWindowIcon(QIcon(self.resource_path("assets/logo.ico")))
        self.setWindowTitle("Layout Counter")
        # Prevent resizing (hides maximize button)
        self.setFixedSize(600, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # First file input (PDF)
        self.file1_input = QLineEdit(self)
        file1_button = QPushButton("Browse", self)
        file1_button.clicked.connect(lambda: self.select_file_pdf(self.file1_input))

        file1_layout = QHBoxLayout()
        file1_layout.addWidget(QLabel("PDF File:"))
        file1_layout.addWidget(self.file1_input)
        file1_layout.addWidget(file1_button)

        # Second file input (Directory for Excel Output)
        self.file2_input = QLineEdit(self)
        file2_button = QPushButton("Browse", self)
        file2_button.clicked.connect(lambda: self.select_directory(self.file2_input))

        file2_layout = QHBoxLayout()
        file2_layout.addWidget(QLabel("Excel Output Directory:"))
        file2_layout.addWidget(self.file2_input)
        file2_layout.addWidget(file2_button)

        # Convert button
        convert_button = QPushButton("Convert", self)
        convert_button.clicked.connect(self.convert_doc)  # Call the convert function

        layout.addLayout(file1_layout)
        layout.addLayout(file2_layout)
        layout.addWidget(convert_button)

        # Add a horizontal line (QFrame)
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)  # Horizontal line
        line.setFrameShadow(QFrame.Shadow.Sunken)  # Sunken line effect
        layout.addWidget(line)

        # Create a label
        current_year = self.get_current_year()
        label = QLabel(f"© {current_year} Plambe. All rights reserved", self)
        layout.addWidget(label)

        self.setLayout(layout)

    def select_file_pdf(self, input_field: QLineEdit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            input_field.setText(file_path)

    def select_directory(self, input_field: QLineEdit):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory for Output")
        if directory_path:
            input_field.setText(directory_path)

    def convert_doc(self):
        # Get the file paths from the input fields
        pdf_path = self.file1_input.text()
        excel_dir = self.file2_input.text()

        # Debugging print to verify the paths
        print(f"PDF Path: {pdf_path}")
        print(f"Excel Output Directory: {excel_dir}")

        if pdf_path and excel_dir:
            # Define the output file path by appending 'output.xlsx' to the directory path
            output_file = f"{excel_dir}/output.xlsx"
            print(f"Output File: {output_file}")  # Debug print to verify output file path
            run_conversion(pdf_path, output_file)  # Call the conversion logic from main.py
        else:
            print("Both file paths must be selected.")

    def get_current_year(self):
        # Get the current year
        current_year = datetime.now().year
        return current_year

    def resource_path(self, relative_path):
        import sys
        import os
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
