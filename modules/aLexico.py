from modules.Abstract.token import Token
from modules.Abstract.error import Error
from modules.Tipo import TipoToken


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 1
        self.fila = 1
        self.columna = 1
        self.abierto = False
        self.patrones = [
            ("claves", TipoToken.R_CLAVES),
            ("registros", TipoToken.R_REGISTROS),
            ("imprimir", TipoToken.R_IMPRIMIR),
            ("imprimirln", TipoToken.R_IMPRIMIRLN),
            ("conteo", TipoToken.R_CONTEO),
            ("promedio", TipoToken.R_PROMEDIO),
            ("contarsi", TipoToken.R_CONTARSI),
            ("datos", TipoToken.R_DATOS),
            ("sumar", TipoToken.R_SUMAR),
            ("max", TipoToken.R_MAX),
            ("min", TipoToken.R_MIN),
            ("exportarreporte", TipoToken.R_EXPORTAR),
        ]
        self.buffer = ""
        self.es_decimal = False
        self.com_abierto = False
        self.comentario_1 = False

    def analizar(self, cadena):
        self.estado = 1

        while cadena:
            cadena, _ = self.limpiar(cadena)
            if self.estado == 1:
                cadena = self.x_1(cadena)
            elif self.estado == 2:
                temp = self.x_2(cadena)
                cadena = temp
            elif self.estado == 3:
                cadena = self.x_3(cadena)
            elif self.estado == 5:
                cadena = self.x_5(cadena)
            elif self.estado == 8:
                cadena = self.x_8(cadena)
            elif self.estado == 10:
                cadena = self.x_10(cadena)

    def limpiar(self, cadena):
        puntero = 0
        while cadena and (puntero <= len(cadena) - 1):
            char = cadena[puntero]
            puntero += 1
            if char == "\t":
                self.columna += 4
                cadena = cadena[4:]
                puntero = 0
                continue
            if char == "\n":
                self.columna = 1
                self.fila += 1
                cadena = cadena[1:]
                puntero = 0
                continue
            if char == " ":
                cadena = cadena[1:]
                puntero = 0
                self.columna += 1
                continue
            break
        return cadena, 0

    def agregar_token(self, tipo, valor):
        self.tokens.append(Token(tipo, valor, self.fila, self.columna))
        self.columna += len(valor)
        self.estado = 1

    def agregar_token_sin_c(self, tipo, valor):
        self.tokens.append(Token(tipo, valor, self.fila, self.columna - len(valor)))

    def crear_error(self, valor, fila, columna):
        self.errores.append(Error("Error Léxico", valor, fila, columna))
        self.columna += len(self.buffer) + 1

    def x_1(self, cadena):
        char = cadena[0]
        if char == "=":
            self.agregar_token(TipoToken.IGUAL, char)
            cadena = cadena[1:]
            self.estado = 1
        elif char == ";":
            self.agregar_token(TipoToken.PUNTO_COMA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "(":
            self.agregar_token(TipoToken.PARENTESIS_APERTURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == ")":
            self.agregar_token(TipoToken.PARENTESIS_CERRADURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "{":
            self.agregar_token(TipoToken.CORCHETE_APERTURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "}":
            self.agregar_token(TipoToken.CORCHETE_CERRADURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "[":
            self.agregar_token(TipoToken.LLAVE_APERTURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "]":
            self.agregar_token(TipoToken.LLAVE_CERRADURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == ",":
            self.agregar_token(TipoToken.COMA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "#":
            self.buffer += char
            cadena = cadena[1:]
            self.estado = 2
        elif char in ['"', "'"]:
            self.buffer += char
            cadena = cadena[1:]
            self.estado = 8
        elif char.isalpha():
            self.estado = 3
        elif char.isdigit():
            self.estado = 5
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 1
        return cadena

    def x_2(self, cadena):
        char = cadena[0]

        if char in ["\n", "\t", "\r"]:
            self.agregar_token(TipoToken.COMENTARIO, self.buffer)
            self.estado = 1
            self.buffer = ""
        else:
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_2(cadena)
        return cadena

    def x_3(self, cadena):
        char = cadena[0]
        if char.isalpha():
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_3(cadena)
        elif char in ['"', "\n", "\t", " ", ",", "}", "{", "="]:
            token_type = None
            for pat, tipo in self.patrones:
                if pat == self.buffer:
                    token_type = tipo
                    break
            if token_type:
                self.agregar_token(token_type, self.buffer)
                self.estado = 1
                self.buffer = ""
            else:
                self.agregar_token(TipoToken.STRING, self.buffer)
                self.estado = 1
                self.buffer = ""
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            cadena = self.x_5(cadena)
        return cadena

    def x_5(self, cadena):
        char = cadena[0]
        if char.isdigit():
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_5(cadena)
        elif char == ".":
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_6(cadena)
        elif char in ['"', "\n", "\t", " ", ",", "}"]:
            try:
                self.agregar_token_sin_c(TipoToken.ENTERO, self.buffer)
                self.estado = 1
                self.buffer = ""
            except Exception as _:
                self.estado = 1
                self.buffer = ""
                print(" ")
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            cadena = self.x_5(cadena)
        return cadena

    def x_6(self, cadena):
        char = cadena[0]
        if char.isdigit():
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_7(cadena)
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            cadena = self.x_6(cadena)
        return cadena

    def x_7(self, cadena):
        char = cadena[0]
        if char.isdigit():
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_7(cadena)
        elif char in ['"', "\n", "\t", " ", ",", "}"]:
            try:
                self.agregar_token_sin_c(TipoToken.REAL, self.buffer)
                self.buffer = ""
            except Exception as _:
                self.buffer = ""
                self.estado = 1
                print(" ")
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            cadena = self.x_7(cadena)
        return cadena

    def x_8(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_11(cadena)
        elif char.isalpha():
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_9(cadena)
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 1
        return cadena

    def x_9(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.agregar_token_sin_c(TipoToken.STRING, self.buffer)
            self.buffer = ""
            self.estado = 1
        else:
            cadena = cadena[1:]
            self.buffer += char
            self.columna += 1
            cadena = self.x_9(cadena)

        return cadena

    def x_11(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            self.columna += 1
            cadena = cadena[1:]
            cadena = self.x_12(cadena)
        else:
            self.crear_error(char, self.fila, self.columna)
            self.estado = 1
            self.buffer = ""
        return cadena

    def x_12(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.columna += 1
            cadena = self.x_13(cadena)
        else:
            cadena = cadena[1:]
            self.buffer += char
            self.columna += 1
            cadena = self.x_12(cadena)
        return cadena

    def x_13(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.columna += 1
            cadena = self.x_14(cadena)
        else:
            self.crear_error(char, self.fila, self.columna)
            self.estado = 1
            self.buffer = ""
        return cadena

    def x_14(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.columna += 1
            self.agregar_token_sin_c(TipoToken.COMENTARIO_M, self.buffer)
            self.estado = 1
            self.buffer = ""
        else:
            self.crear_error(char, self.fila, self.columna)
            self.estado = 1
            self.buffer = ""
        return cadena

    def imprimir(self):
        for i, dato in enumerate(self.tokens):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
