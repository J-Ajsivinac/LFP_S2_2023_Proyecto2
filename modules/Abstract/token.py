from modules.Abstract.abstract import Expresion


class Token(Expresion):
    def __init__(self, tipo, valor, fila, columna):
        super().__init__(tipo, valor, fila, columna)
