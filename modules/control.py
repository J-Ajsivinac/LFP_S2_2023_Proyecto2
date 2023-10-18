import tkinter as tk
from modules.reporte import Reporte
import os


class Control:
    def __init__(self, consola: tk.Text, ruta):
        self.matriz = {}
        self.consola = consola
        self.ruta = ruta

    def reiniciar(self):
        self.matriz = {}

    def cargar_claves(self, i_d):
        self.matriz[i_d] = []

    def cargar_valores(self, i_d, valor):
        self.matriz[i_d].append(valor)

    def imprimir(self, valor):
        self.consola.insert("end", valor)

    def imprimirln(self, valor):
        self.consola.insert("end", valor + "\n")

    def conteo(self):
        if len(self.matriz) == 0:
            return
        valor = len(next(iter(self.matriz.values())))
        self.consola.insert("end", str(valor) + "\n")

    def promedio(self, valor):
        if not valor in self.matriz or len(self.matriz) == 0:
            return
        valores = self.matriz[valor]
        promedio = sum(valores) / len(valores)
        self.consola.insert("end", str(promedio) + "\n")

    def contarsi(self, i_d, valor):
        if not i_d in self.matriz or len(self.matriz) == 0:
            return
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if v == valor:
                contador += 1

        self.consola.insert("end", str(contador) + "\n")

    def datos(self):
        if len(self.matriz) == 0:
            return
        size = len(next(iter(self.matriz.values())))
        encabezados = "\t".join(self.matriz.keys()) + "\n"
        self.consola.insert("end", encabezados.replace('"', "") + "\n")

        for i in range(size):
            fila = (
                "\t".join(
                    [
                        str(self.matriz[encabezado][i])
                        for encabezado in self.matriz.keys()
                    ]
                )
                + "\n"
            )
            self.consola.insert("end", fila)

    def sumar(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            return
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if isinstance(v, (int, float)):
                contador += v
        self.consola.insert("end", str(contador) + "\n")

    def get_max(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            return
        valores = self.matriz[i_d]
        maximo = max(valores)
        self.consola.insert("end", str(maximo) + "\n")

    def get_min(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            return
        valores = self.matriz[i_d]
        minimo = min(valores)
        self.consola.insert("end", str(minimo) + "\n")

    def exportar(self, nombre):
        if len(self.matriz) == 0:
            return
        nombre = nombre.replace('"', "")
        ruta_archivo = os.path.join(self.ruta, "reporte_datos.html").replace(
            "\\", "\\\\"
        )
        rep = Reporte()
        rep.crear_reporte_datos(self.matriz, nombre, ruta_archivo)
