import tkinter as tk


class Control:
    def __init__(self, consola: tk.Text):
        self.matriz = {}
        self.consola = consola

    def cargar_claves(self, i_d):
        self.matriz[i_d] = []

    def cargar_valores(self, i_d, valor):
        self.matriz[i_d].append(valor)

    def imprimir(self, valor):
        self.consola.insert("end", valor)

    def imprimirln(self, valor):
        self.consola.insert("end", "\n" + valor)

    def conteo(self):
        valor = len(next(iter(self.matriz.values())))
        self.consola.insert("end", "\n" + str(valor))

    def promedio(self, valor):
        valores = self.matriz[valor]
        promedio = sum(valores) / len(valores)
        self.consola.insert("end", "\n" + str(promedio))

    def contarsi(self, i_d, valor):
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if v == valor:
                contador += 1

        self.consola.insert("end", "\n" + str(contador))

    def datos(self):
        size = len(next(iter(self.matriz.values())))
        encabezados = "\t".join(self.matriz.keys()) + "\n"
        self.consola.insert("end", "\n" + encabezados.replace('"', ""))

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
        valores = self.matriz[i_d]
        contador = 0
        for v in valores:
            if isinstance(v, (int, float)):
                contador += v
        self.consola.insert("end", "\n" + str(contador))

    def get_max(self, i_d):
        valores = self.matriz[i_d]
        maximo = max(valores)
        self.consola.insert("end", "\n" + str(maximo))

    def get_min(self, i_d):
        valores = self.matriz[i_d]
        minimo = min(valores)
        self.consola.insert("end", "\n" + str(minimo))

    def exportar(self, nombre):
        self.consola.insert("end", "\n" + f"exportando {nombre}")
