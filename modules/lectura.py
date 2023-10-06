from tkinter import filedialog
import json


def cargar_json(text_widget):
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos bizdata", "*.bizdata")]
    )
    if file_path:
        with open(file_path, "r") as json_file:
            json_content = json_file.read()
            text_widget.delete(
                "1.0", "end"
            )  # Borra el contenido existente en el widget Text
            text_widget.insert(
                "1.0", json_content
            )  # Inserta el contenido JSON en el widget Text
            return file_path
    return None
