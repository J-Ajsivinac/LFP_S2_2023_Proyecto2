import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from modules.lectura import cargar_json
from modules.aLexico import AnalizadorLexico
from modules.aSintactico import AnalizadorSintactico
from modules.control import Control
from modules.graph import Graph
from modules import lectura
from img.icons import Imagenes
from PIL import Image, ImageTk
import os
import copy
from modules.reporte import Reporte


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1100x668")
        self.resizable(0, 0)

        sv_ttk.set_theme("dark")
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Montserrat SemiBold", 11), border=0)
        self.style.configure("TButton1.TButton", foreground="#c2c3c4")
        self.style.configure("TLabel", font=("Montserrat SemiBold", 11))
        self.configure(bg="#080b0f")
        Contendio(self)
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
        _ruta = os.path.dirname(os.path.abspath(__file__))
        self.controlador = Control(self.text_consola, _ruta)
        self.lista_tokens = []
        self.errores_lex = []
        self.errores_sin = []
        self.info_grafica = []

    def crear_menu_superior(self):
        panel_superior = tk.Frame()
        panel_superior.pack(padx=2, pady=3, fill="x", side="top")
        panel_superior.configure(bg="#080b0f")

        style_menu = ttk.Style()
        img_o = Image.open(Imagenes.BTN_OPEN)
        img_o = img_o.resize((21, 21), Image.LANCZOS)
        self.img_open = ImageTk.PhotoImage(img_o)

        img_r = Image.open(Imagenes.BTN_REPORT)
        img_r = img_r.resize((21, 21), Image.LANCZOS)
        self.img_report = ImageTk.PhotoImage(img_r)
        # style_menu.configure("Nuevo.TButton", font=("Montserrat SemiBold", 12))
        style_menu.configure("Nuevo.TMenubutton", font=("Montserrat SemiBold", 12))
        menu_button = ttk.Menubutton(
            panel_superior,
            image=self.img_report,
            text=" Reportes",
            compound="left",
            style="Nuevo.TMenubutton",
        )

        button_sub_menu = tk.Menu(
            menu_button,
            tearoff=False,
            relief=tk.SOLID,
            font=("Montserrat", 12),
            borderwidth=20,
        )
        button_sub_menu.add_command(label="  Tokens", command=self.c_reporte_token)
        button_sub_menu.add_command(label="  Errores", command=self.c_reporte_errores)
        button_sub_menu.add_command(
            label="  Arbol de Derivación", command=self.c_reporte_grafica
        )

        menu_button["menu"] = button_sub_menu
        btn_1 = ttk.Button(
            panel_superior,
            image=self.img_open,
            text=" Abrir",
            compound="left",
            width=7,
            command=self.cargar_datos,
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
        panel_medio.columnconfigure(0, weight=2, pad=650)
        panel_medio.columnconfigure(1, weight=1, minsize=360)
        panel_medio.rowconfigure(0, weight=1)

        panel_izq = tk.Frame(panel_medio)
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
        panel_izq_sup.configure(bg="#3C3F69")
        self.lbl_nombre = tk.Label(
            panel_izq_sup,
            text="Nombre.bizdata",
            background="#3C3F69",
            font=("Montserrat SemiBold", 11),
        )
        img_1 = Image.open(Imagenes.BTN_PLAY)
        img_1 = img_1.resize((21, 21), Image.LANCZOS)
        self.img_play = ImageTk.PhotoImage(img_1)
        btn_ejecutar = ttk.Button(
            panel_izq_sup,
            image=self.img_play,
            compound="left",
            text="",
            style="Accent.TButton",
            width=2,
            command=self.analizar_datos,
        )

        self.lbl_nombre.grid(row=0, column=0)
        btn_ejecutar.grid(row=0, column=1, sticky=tk.E)

        panel_text = tk.Frame(panel_izq)

        self.hscrollbar = ttk.Scrollbar(panel_text, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(panel_text, orient=tk.VERTICAL)

        panel_text.pack(fill="y")
        self.text_code = tk.Text(
            panel_text,
            font=("Cascadia Code", 12),
            background="#212327",
            border=0,
            yscrollcommand=self.vscrollbar.set,
            xscrollcommand=self.hscrollbar.set,
            wrap="none",
            foreground="#f5f5f6",
            selectbackground="#2b313d",
        )
        self.hscrollbar.config(command=self.text_code.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.text_code.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
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
        lbl_nombre.configure(bg="#3C3F69")
        panel_text = tk.Frame(panel_der)
        panel_text.pack(fill="y")
        hscrollbar = ttk.Scrollbar(panel_text, orient=tk.HORIZONTAL)
        vscrollbar = ttk.Scrollbar(panel_text, orient=tk.VERTICAL)
        self.text_consola = tk.Text(
            panel_text,
            font=("Cascadia Code", 12),
            background="#212327",
            border=0,
            wrap="none",
            yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set,
            state="disabled",
            foreground="#bbbcc0",
        )
        hscrollbar.config(command=self.text_consola.xview)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        vscrollbar.config(command=self.text_consola.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
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

    def cargar_datos(self):
        self.archivo_actual = lectura.cargar_json(self.text_code)
        if self.archivo_actual:
            _, nombre = os.path.split(self.archivo_actual)
            self.lbl_nombre.config(text=nombre)
            # self.actualizar_contador()

    def analizar_datos(self):
        texto = self.text_code.get("1.0", "end")
        if not texto.strip():
            messagebox.showerror(message="No hay información cargada", title="Error")
            return
        analizado = AnalizadorLexico()
        analizado.analizar(texto)
        lista = analizado.regresar_tokens()
        self.lista_tokens = copy.deepcopy(analizado.tokens)
        self.errores_lex = copy.deepcopy(analizado.errores)
        # print(self.lista_tokens)
        # analizado.imprimir()
        self.text_consola.config(state="normal")
        self.controlador.reiniciar()
        contador_lineas = self.text_consola.get("1.0", "end").strip()
        if contador_lineas:
            contador_lineas = contador_lineas.count("\n") + 1
        else:
            contador_lineas = 0
        sintactico = AnalizadorSintactico(lista, self.controlador)
        sintactico.parser()
        self.errores_sin = copy.deepcopy(sintactico.errores_s)
        self.info_grafica = sintactico.datos_grafica
        contador_temp = self.text_consola.get("1.0", "end").strip()
        if contador_temp:
            contador_temp = contador_temp.count("\n") + 1
        else:
            contador_temp = 0
        if contador_temp > contador_lineas:
            self.text_consola.insert(tk.END, "\n  \n")
        self.text_consola.config(state="disabled")

    def c_reporte_token(self):
        if len(self.lista_tokens) == 0:
            messagebox.showerror(message="No hay información procesada", title="Error")
            return
        reporte = Reporte()
        _ruta = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(_ruta, "reporte_tokens.html").replace("\\", "\\\\")
        reporte.crear_reporte_tokens(self.lista_tokens, ruta_archivo)

    def c_reporte_errores(self):
        if len(self.errores_lex) == 0 and len(self.errores_sin) == 0:
            messagebox.showerror(message="No hay ningún tipo de errores", title="Error")
            return
        reporte = Reporte()
        _ruta = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(_ruta, "reporte_errores.html").replace("\\", "\\\\")
        reporte.crear_reporte_errores(self.errores_lex, self.errores_sin, ruta_archivo)

    def c_reporte_grafica(self):
        if len(self.lista_tokens) == 0:
            messagebox.showerror(message="No hay información procesada", title="Error")
            return
        # print(self.info_grafica)
        grafica = Graph(self.info_grafica)


if __name__ == "__main__":
    App()
