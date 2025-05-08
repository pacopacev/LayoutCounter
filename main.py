import PyPDF2
from collections import Counter
import re
import pandas as pd
import os
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def count_words(text):
    try:
        words = re.findall(r'\b\w+\b', text.lower())
        return Counter(words)
    except Exception as e:
        print(f"Error counting words: {e}")
        return Counter()


def save_to_excel(word_counts, output_file):
    try:
        df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])
        df.to_excel(output_file, index=False)
        print(f"Word counts have been saved to {output_file}")
        msg = f"Word counts have been saved to {output_file}"
        show_message_func(msg)
    except Exception as e:
        print(f"Error saving to Excel: {e}")


def run_conversion(pdf_path, excel_output_path):
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)

        if not text:
            print("No text extracted from PDF.")
            return

        # Count the words in the text
        word_counts = count_words(text)

        # Ensure the directory exists where the Excel file will be saved
        directory = os.path.dirname(excel_output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist

        # Save the result to an Excel file
        save_to_excel(word_counts, excel_output_path)

    except Exception as e:
        print(f"Error in run_conversion: {e}")

def show_message_func(message):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(resource_path("assets/logo.ico")))
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle("Info")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Show the message box
    msg_box.exec()

def resource_path(relative_path):
    import sys
    import os
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)