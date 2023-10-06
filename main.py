import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from modules.lectura import cargar_json
from modules.aLexico import Analizador

# C:\Users\mesoi\Downloads
text = ""
with open(
    "C:\\Users\\mesoi\\Downloads\\prueba2.bizdata",
    "r",
) as json_file:
    text = json_file.read()
    analizado = Analizador()
    analizado.analizar(text)
    analizado.imprimir()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1066x645")
        self.resizable(0, 0)

        sv_ttk.set_theme("dark")
        Contendio(self)
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Montserrat SemiBold", 11), border=0)
        self.style.configure("TButton1.TButton", foreground="#c2c3c4")
        self.style.configure("TLabel", font=("Montserrat SemiBold", 11))
        self.configure(bg="#080b0f")
        self.mainloop()


class Contendio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=40, pady=6, fill="x", side="top")
        self.style = ttk.Style()
        self.style.configure("My.TFrame")
        self.config(style="My.TFrame")
        self.crear_menu_superior()
        self.crear_medio()
        self.crear_final()
        self.archivo_actual = None

    def crear_menu_superior(self):
        panel_superior = tk.Frame()
        panel_superior.pack(padx=2, pady=3, fill="x", side="top")
        panel_superior.configure(bg="#080b0f")

        style_menu = ttk.Style()
        # style_menu.configure("Nuevo.TButton", font=("Montserrat SemiBold", 12))
        style_menu.configure("Nuevo.TMenubutton", font=("Montserrat SemiBold", 12))
        menu_button = ttk.Menubutton(
            panel_superior, text="Reportes", compound="left", style="Nuevo.TMenubutton"
        )

        button_sub_menu = tk.Menu(
            menu_button,
            tearoff=False,
            relief=tk.SOLID,
            font=("Montserrat", 12),
            borderwidth=20,
        )
        button_sub_menu.add_command(label="  Tokens")
        button_sub_menu.add_command(label="  Errores")
        button_sub_menu.add_command(label="  Arbol de Derivación")

        menu_button["menu"] = button_sub_menu
        btn_1 = ttk.Button(
            panel_superior,
            text=" Abrir",
            compound="left",
            width=7,
        )
        btn_1.grid_configure(padx=0)
        # btn_1.configure(foreground="#50dfea")

        panel_superior.columnconfigure((0, 1, 2, 3), uniform="a", pad=5)
        panel_superior.rowconfigure((0), uniform="a")

        btn_1.grid(row=0, column=0, columnspan=1)
        menu_button.grid(row=0, column=1, columnspan=1)

    def crear_medio(self):
        panel_medio = tk.Frame()
        panel_medio.pack(padx=20, pady=10, fill="both", expand=True)
        panel_medio.configure(bg="#080b0f")
        panel_medio.columnconfigure(0, weight=2, pad=700)
        panel_medio.columnconfigure(1, weight=1, minsize=320)
        panel_medio.rowconfigure(0, weight=1)

        panel_izq = tk.Frame(panel_medio)
        # panel_izq.configure(bg="#ff7b72")
        self.crear_panel_izq(panel_izq)

        panel_izq.grid(row=0, column=0, sticky=tk.NSEW, padx=10)

        panel_der = tk.Frame(panel_medio)
        panel_der.grid(row=0, column=1, sticky=tk.NSEW)
        self.crear_panel_der(panel_der)

    def crear_panel_izq(self, panel_izq):
        panel_izq_sup = tk.Frame(panel_izq)
        panel_izq_sup.columnconfigure(0, weight=4)
        panel_izq_sup.columnconfigure(1, weight=1)
        panel_izq_sup.rowconfigure(0, weight=1)
        panel_izq_sup.pack(fill="x", pady=0)
        panel_izq_sup.configure(bg="#34384f")
        lbl_nombre = tk.Label(
            panel_izq_sup,
            text="Nombre.bizdata",
            background="#34384f",
            font=("Montserrat SemiBold", 11),
        )

        btn_ejecutar = ttk.Button(
            panel_izq_sup,
            text="Ejecutar",
            width=7,
            style="Accent.TButton",
        )

        lbl_nombre.grid(row=0, column=0)
        btn_ejecutar.grid(row=0, column=1, sticky=tk.E)

        panel_text = tk.Frame(panel_izq)
        panel_text.pack(fill="y")
        self.text_code = tk.Text(
            panel_text,
            font=("Cascadia Code", 12),
            background="#212327",
            border=0,
            wrap=None,
        )
        self.text_code.pack(fill="both")

    def crear_panel_der(self, panel_der):
        panel_der_sup = tk.Frame(panel_der)
        # panel_der_sup.configure(bg="#ffffff")
        panel_der_sup.columnconfigure(0, weight=4)
        panel_der_sup.columnconfigure(1, weight=1)
        panel_der_sup.rowconfigure(0, weight=1)
        # panel_der_sup.configure(bg="#4effca")
        panel_der_sup.pack(fill="x", pady=0)
        lbl_nombre = tk.Label(
            panel_der_sup, text="Consola", font=("Montserrat SemiBold", 11), pady=5
        )
        lbl_nombre.pack(fill="x", expand=True)
        lbl_nombre.configure(bg="#34384f")
        panel_text = tk.Frame(panel_der)
        panel_text.pack(fill="y")
        self.text_consola = tk.Text(
            panel_text,
            font=("Cascadia Code", 12),
            background="#212327",
            border=0,
            wrap=None,
        )
        self.text_consola.pack(fill="both")

    def crear_final(self):
        panel_fin = tk.Frame()
        panel_fin.pack(padx=2, pady=3, fill="x")
        panel_fin.configure(bg="#080b0f")
        lbl_nombre = tk.Label(
            panel_fin,
            text="Proyecto 2 - 202200135",
            font=("Montserrat", 11),
            background="#080b0f",
        )
        lbl_nombre.pack()


# if __name__ == "__main__":
#     #App()
