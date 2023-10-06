from abc import ABC, abstractmethod


class Expresion(ABC):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
