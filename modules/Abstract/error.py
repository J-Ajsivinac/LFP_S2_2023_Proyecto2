from modules.Abstract.abstract import Expresion


class Error(Expresion):
    def __init__(self, tipo, valor, fila, columna, leido=None):
        super().__init__(tipo, valor, fila, columna)
        self.leido = leido
