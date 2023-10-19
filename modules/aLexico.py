from modules.Abstract.token import Token
from modules.Abstract.error import Error
from modules.Tipo import TipoToken
import re


class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 1
        self.fila = 1
        self.columna = 1
        self.abierto = False
        self.patrones = [
            (re.compile(r"claves", re.I), TipoToken.R_CLAVES),
            (re.compile(r"registros", re.I), TipoToken.R_REGISTROS),
            (re.compile(r"imprimir", re.I), TipoToken.R_IMPRIMIR),
            (re.compile(r"imprimirln", re.I), TipoToken.R_IMPRIMIRLN),
            (re.compile(r"conteo", re.I), TipoToken.R_CONTEO),
            (re.compile(r"promedio", re.I), TipoToken.R_PROMEDIO),
            (re.compile(r"contarsi", re.I), TipoToken.R_CONTARSI),
            (re.compile(r"datos", re.I), TipoToken.R_DATOS),
            (re.compile(r"sumar", re.I), TipoToken.R_SUMAR),
            (re.compile(r"max", re.I), TipoToken.R_MAX),
            (re.compile(r"min", re.I), TipoToken.R_MIN),
            (re.compile(r"exportarreporte", re.I), TipoToken.R_EXPORTAR),
        ]
        self.buffer = ""
        self.es_decimal = False
        self.com_abierto = False
        self.comentario_1 = False

    def analizar(self, cadena):
        self.estado = 1

        while cadena:
            cadena, _ = self.limpiar(cadena)
            if len(cadena) == 0:
                break
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
            elif self.estado == 18:
                cadena = self.x1_8(cadena)

    def limpiar(self, cadena):
        puntero = 0
        if self.com_abierto:
            return cadena, 0
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

    def crear_error(self, valor, fila, columna, error=False):
        self.errores.append(Error("Error Léxico", valor, fila, columna))
        if error:
            valor = valor.split("\n")[-1]
            self.columna += len(valor)
            return
        self.columna += len(valor)

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
            self.agregar_token(TipoToken.LLAVE_APERTURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "}":
            self.agregar_token(TipoToken.LLAVE_CERRADURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "[":
            self.agregar_token(TipoToken.CORCHETE_APERTURA, char)
            self.estado = 1
            cadena = cadena[1:]
        elif char == "]":
            self.agregar_token(TipoToken.CORCHETE_CERRADURA, char)
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
        elif char in ['"']:
            self.buffer += char
            cadena = cadena[1:]
            self.com_abierto = True
            self.estado = 8
        elif char == "'":
            self.buffer += char
            cadena = cadena[1:]
            self.com_abierto = True
            self.estado = 18
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
        elif char in ['"', "\n", "\t", " ", ",", "}", "{", "=", "(", ")"]:
            token_type = None
            for pat, tipo in self.patrones:
                if re.fullmatch(pat, self.buffer):
                    # if pat == self.buffer:
                    token_type = tipo
                    break
            if token_type:
                self.agregar_token(token_type, self.buffer)
                self.estado = 1
                self.buffer = ""
            else:
                self.agregar_token(TipoToken.TEXT, self.buffer)
                self.estado = 1
                self.buffer = ""
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            cadena = self.x_3(cadena)
            # self.estado = 1
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
        elif char in ['"', "\n", "\t", " ", ",", "}", ")"]:
            try:
                self.agregar_token(TipoToken.ENTERO, int(self.buffer))
                self.estado = 1
                self.buffer = ""
            except Exception as _:
                self.estado = 1
                self.buffer = ""
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
                self.agregar_token(TipoToken.REAL, float(self.buffer))
                self.buffer = ""
            except Exception as _:
                self.buffer = ""
                self.estado = 1
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
            self.com_abierto = False
        else:
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_9(cadena)
        # else:
        #     self.columna += 1
        #     self.crear_error(char, self.fila, self.columna)
        #     cadena = cadena[1:]
        #     self.buffer = ""
        #     self.estado = 1
        return cadena

    def x1_8(self, cadena):
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x1_11(cadena)
            self.com_abierto = False
        else:
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x1_9(cadena)
        # else:
        #     valor = self.buffer + char
        #     self.crear_error(valor, self.fila, self.columna)
        #     cadena = cadena[1:]
        #     self.estado = 1
        return cadena

    def x_9(self, cadena):
        if cadena is None or len(cadena) == 0:
            self.crear_error('"', self.fila, self.columna)
            self.estado = 1
            return None
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.agregar_token(TipoToken.STRING, self.buffer)
            self.com_abierto = False
            self.buffer = ""
        else:
            if char == "\n":
                self.fila += 1
                self.columna = 1
                self.crear_error('falta de cierre "', self.fila, self.columna)
                self.estado = 1
                return cadena
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_9(cadena)

        return cadena

    def x1_9(self, cadena):
        if cadena is None or len(cadena) == 0:
            self.crear_error('"', self.fila, self.columna)
            self.estado = 1
            return None
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            self.agregar_token(TipoToken.STRING, self.buffer)
            self.buffer = ""
            self.com_abierto = False
        else:
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_9(cadena)

        return cadena

    def x_11(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_12(cadena)
        else:
            self.crear_error(self.buffer, self.fila, self.columna)
            self.com_abierto = False
            self.estado = 1
            self.buffer = ""
        return cadena

    def x1_11(self, cadena):
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x1_12(cadena)
        else:
            self.crear_error(self.buffer, self.fila, self.columna)
            self.com_abierto = False
            self.estado = 1
            self.buffer = ""
        return cadena

    def x_12(self, cadena):
        if cadena is None or len(cadena) == 0:
            self.crear_error('No hay cierre de "', self.fila, self.columna)
            self.estado = 1
            return None
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_13(cadena)
        else:
            if char == "\n":
                self.fila += 1
                self.columna = 1
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x_12(cadena)
        return cadena

    def x1_12(self, cadena):
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x1_13(cadena)
        else:
            if char == "\n":
                self.columna = 1
                self.fila += 1
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.x1_12(cadena)
        return cadena

    def x_13(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x_14(cadena)
        else:
            self.crear_error(self.buffer, self.fila, self.columna, True)
            self.com_abierto = False
            self.estado = 1
            self.buffer = ""
        return cadena

    def x1_13(self, cadena):
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            cadena = self.x1_14(cadena)
        else:
            self.crear_error(self.buffer, self.fila, self.columna)
            self.com_abierto = False
            self.estado = 1
            self.buffer = ""
        return cadena

    def x_14(self, cadena):
        char = cadena[0]
        if char == '"':
            self.buffer += char
            cadena = cadena[1:]
            self.agregar_token(TipoToken.COMENTARIO_M, self.buffer)
            self.buffer = ""
        else:
            self.crear_error(self.buffer, self.fila, self.columna)
            self.com_abierto = False
            self.estado = 1
            self.buffer = ""
        return cadena

    def x1_14(self, cadena):
        char = cadena[0]
        if char == "'":
            self.buffer += char
            cadena = cadena[1:]
            self.agregar_token(TipoToken.COMENTARIO_M, self.buffer)
            self.buffer = ""
        else:
            self.com_abierto = False
            self.crear_error(char, self.fila, self.columna)
            self.estado = 1
            self.buffer = ""
        return cadena

    def regresar_tokens(self):
        return self.tokens

    def imprimir(self):
        for _, dato in enumerate(self.tokens):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
        print("----")
        for _, dato in enumerate(self.errores):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
