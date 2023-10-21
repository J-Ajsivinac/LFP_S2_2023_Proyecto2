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
            self.consola.insert("end", "0 \n")
            return
        valor = len(next(iter(self.matriz.values())))
        self.consola.insert("end", str(valor) + "\n")

    def promedio(self, valor):
        if not valor in self.matriz or len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        valores = self.matriz[valor]
        try:
            promedio = sum(valores) / len(valores)
            self.consola.insert("end", str(promedio) + "\n")
        except Exception as _:
            self.consola.insert("end", "Los valores no son numeros" + "\n")

    def contarsi(self, i_d, valor):
        if not i_d in self.matriz or len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if v == valor:
                contador += 1

        self.consola.insert("end", str(contador) + "\n")

    def imprimir_encabezado(self):
        largo = 0
        largo_retornar = []
        for i, value in enumerate(self.matriz):
            largo = 0
            largo += len(str(value))
            largo += 4
            largo_retornar.append(largo)
            # print(largo)
            if i == 0:
                self.consola.insert("end", "╔")
            self.consola.insert("end", "=" * largo)
            if i != len(self.matriz) - 1:
                self.consola.insert("end", "╦")
            if i == len(self.matriz) - 1:
                self.consola.insert("end", "╗" + "\n")

        for i, value in enumerate(self.matriz):
            valor = value.replace('"', "")
            largo = 0
            largo += len(str(value))
            largo += 4
            # print(largo)
            if i == 0:
                self.consola.insert("end", "║")
            self.consola.insert("end", f"%-{largo}s" % f" {valor}")
            if i != len(self.matriz) - 1:
                self.consola.insert("end", "║")
            if i == len(self.matriz) - 1:
                self.consola.insert("end", "║" + "\n")

        for i, value in enumerate(self.matriz):
            largo = 0
            largo += len(str(value))
            largo += 4
            # print(largo)
            if i == 0:
                self.consola.insert("end", "╠")
            self.consola.insert("end", "=" * largo)
            if i != len(self.matriz) - 1:
                self.consola.insert("end", "╬")
            if i == len(self.matriz) - 1:
                self.consola.insert("end", "╣" + "\n")
        return largo_retornar

    def imprimir_cuerpo(self, largo_total: list):
        llaves = list(self.matriz.keys())
        size = len(next(iter(self.matriz.values())))

        for i in range(size):
            for j, _ in enumerate(llaves):
                if j == 0:
                    self.consola.insert("end", "║")
                largo = largo_total[j]
                self.consola.insert(
                    "end", f"%-{largo}s" % f" {self.matriz[llaves[j]][i]}"
                )
                if j == len(self.matriz) - 1:
                    self.consola.insert("end", "║" + "\n")
                else:
                    self.consola.insert("end", "║")

        for i, value in enumerate(self.matriz):
            largo = 0
            largo += len(str(value))
            largo += 4
            # print(largo)
            if i == 0:
                self.consola.insert("end", "╚")
            self.consola.insert("end", "=" * largo)
            if i != len(self.matriz) - 1:
                self.consola.insert("end", "╩")
            if i == len(self.matriz) - 1:
                self.consola.insert("end", "╝" + "\n")

    def datos(self):
        if len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        largo = self.imprimir_encabezado()
        self.imprimir_cuerpo(largo)
        # self.consola.insert("end", "╗" + "\n")

    def sumar(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if isinstance(v, (int, float)):
                contador += v
        self.consola.insert("end", str(contador) + "\n")

    def get_max(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        valores = self.matriz[i_d]
        if len(valores) == 0:
            self.consola.insert("end", "0 \n")
            return
        maximo = max(valores)
        self.consola.insert("end", str(maximo) + "\n")

    def get_min(self, i_d):
        if not i_d in self.matriz or len(self.matriz) == 0:
            self.consola.insert("end", "0 \n")
            return
        valores = self.matriz[i_d]
        if len(valores) == 0:
            self.consola.insert("end", "0 \n")
            return
        minimo = min(valores)
        self.consola.insert("end", str(minimo) + "\n")

    def exportar(self, nombre):
        if len(self.matriz) == 0:
            self.consola.insert("end", "No hay datos registrados \n")
            return
        nombre = nombre.replace('"', "")
        ruta_archivo = os.path.join(self.ruta, "reporte_datos.html").replace(
            "\\", "\\\\"
        )
        rep = Reporte()
        rep.crear_reporte_datos(self.matriz, nombre, ruta_archivo)
        self.consola.insert("end", "Reporte generado con éxito \n")
