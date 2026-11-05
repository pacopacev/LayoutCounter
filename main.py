import fitz
import pymupdf as pdf
from collections import Counter
import pandas as pd
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

# Global variable to store the references
_log_widget = None
_convert_button_widget = None
_main_window = None

def set_main_window(window):
    global _main_window
    _main_window = window

def show_message_func(message):
    msg_box = QMessageBox(_main_window)  # ✅ Set parent window
    try:
        msg_box.setWindowIcon(QIcon(resource_path("assets/logo.ico")))
    except Exception as e:
        print(f"Icon load failed: {e}")
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle("Info")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

def set_log_widget(widget):
    global _log_widget
    _log_widget = widget

def set_convert_button(widget):
    global _convert_button_widget
    _convert_button_widget = widget

def get_log_widget():
    return _log_widget

def log_message(text):
    if _log_widget:

        _log_widget.appendPlainText(str(text))
        _log_widget.setVisible(True)
        _log_widget.ensureCursorVisible()

        # ⬇️ Resize the parent window to accommodate the log area
        parent = _log_widget.window()
        if parent:
            parent.setMinimumHeight(550)
            parent.adjustSize()
    else:
        print(text)

def int_to_rgb(color_int):
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return r, g, b

def is_search_color(r, g, b, request_color):
    if request_color == "orange":
        return 220 <= r <= 255 and 100 <= g <= 180 and 0 <= b <= 80
    elif request_color == "blk":
        return r <= 50 and g <= 50 and b <= 50
    elif request_color == "green":
        return 0 <= r <= 100 and 120 <= g <= 255 and 0 <= b <= 100
    elif request_color == "yellow":
        return 200 <= r <= 255 and 200 <= g <= 255 and 0 <= b <= 80
    elif request_color == "white":
        return r >= 240 and g >= 240 and b >= 240
    elif request_color == "purple":
        return 120 <= r <= 255 and 0 <= g <= 100 and 120 <= b <= 255
    elif request_color == "blue":
        return 0 <= r <= 100 and 0 <= g <= 100 and 180 <= b <= 255
    elif request_color == "red":
        return 180 <= r <= 255 and 0 <= g <= 100 and 0 <= b <= 100
    elif request_color == "all":
        return True
    return False

def run_conversion(pdf_path, excel_output_path, request_color):
    try:
        doc = pdf.open(pdf_path)
        if not doc:
            log_message("Error: Cannot open PDF file.")
            return

        green_segments = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        color = span.get("color", 0)
                        r, g, b = int_to_rgb(color)
                        if is_search_color(r, g, b, request_color):
                            text = span["text"].strip()
                            if text:
                                green_segments.append(text)

        counter = Counter(green_segments)

        if counter and excel_output_path:
            try:
                df = pd.DataFrame(counter.items(), columns=["Word", "Count"])
                df.to_excel(excel_output_path, index=False)
                show_message_func(f"Excel file saved to:\n{excel_output_path}")
            except Exception as e:
                log_message(f"Error saving to Excel: {e}")
                show_message_func("Failed to save the Excel file.")
            #return  # ✅ Stop after export

        if not counter:
            show_message_func("No matching text found with the selected color.")
            return
        elif counter and excel_output_path is None:
            _convert_button_widget.setEnabled(True)
            for text, count in counter.most_common():
                log_message(f"{repr(text)}: {count}")

    except Exception as e:
        log_message(f"Error in run_conversion: {e}")

def resource_path(relative_path):
    import sys
    import os
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
