from modules.Abstract.token import Token
from modules.Abstract.error import Error
from modules.Tipo import TipoToken


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 0
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
        puntero = 0
        self.estado = 0

        while cadena:
            puntero = 0
            cadena, puntero = self.limpiar(cadena)
            if self.estado == 0:
                cadena = self.s_0(cadena[puntero], cadena)
            elif self.estado == 1:
                cadena = self.s_1(cadena[puntero], cadena)
            elif self.estado == 2:
                cadena = self.s_2(cadena[puntero], cadena)
            elif self.estado == 3:
                cadena = self.s_3(cadena[puntero], cadena)
            elif self.estado == 4:
                cadena = self.s_4(cadena[puntero], cadena)
            elif self.estado == 5:
                cadena = self.s_5(cadena[0], cadena)
            elif self.estado == 6:
                cadena = self.s_6(cadena[puntero], cadena)
            elif self.estado == 7:
                cadena = self.s_7(cadena)
            elif self.estado == 8:
                cadena = self.s_8(cadena)
            elif self.estado == 9:
                cadena = self.s_9(cadena)
            elif self.estado == 10:
                cadena = self.s_10(cadena)

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
        self.estado = 0

    def agregar_token_sin_c(self, tipo, valor, col_com):
        self.tokens.append(Token(tipo, valor, self.fila, self.columna - col_com))
        # self.estado = 0

    def crear_error(self, valor, fila, columna):
        self.errores.append(Error("Error Léxico", valor, fila, columna))
        self.columna += len(self.buffer) + 1

    def s_0(self, char, cadena):
        if char == "=":
            self.agregar_token(TipoToken.IGUAL, char)
            cadena = cadena[1:]
            self.estado = 0
        elif char == "[":
            self.agregar_token(TipoToken.LLAVE_APERTURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == "]":
            self.agregar_token(TipoToken.LLAVE_CERRADURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == '"' and self.abierto:
            self.agregar_token(TipoToken.COMILLAS, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == '"':
            self.estado = 1
            cadena = cadena[1:]
        elif char.isalpha():
            self.estado = 2
        elif char.isdigit():
            self.estado = 3
        elif char == ",":
            self.agregar_token(TipoToken.COMA, char)
            cadena = cadena[1:]
        elif char == "{":
            self.agregar_token(TipoToken.CORCHETE_APERTURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == "}":
            self.agregar_token(TipoToken.CORCHETE_CERRADURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == "#":
            self.agregar_token(TipoToken.NUMERAL, char)
            self.comentario_1 = True
            self.estado = 7
            cadena = cadena[1:]
        elif char == "(":
            self.agregar_token(TipoToken.PARENTESIS_APERTURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == ")":
            self.agregar_token(TipoToken.PARENTESIS_CERRADURA, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == "'":
            self.agregar_token(TipoToken.COMILLAS_SIMPLES, char)
            self.estado = 0
            cadena = cadena[1:]
        elif char == ";":
            self.agregar_token(TipoToken.PUNTO_COMA, char)
            self.estado = 0
            cadena = cadena[1:]
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 0
        return cadena

    def s_1(self, char, cadena):
        if char == '"':
            self.estado = 4
            cadena = cadena[1:]
            self.columna += 1
        elif char.isalpha():
            self.agregar_token(TipoToken.COMILLAS, '"')
            self.abierto = not self.abierto
            # cadena = cadena[1:]
            self.estado = 5
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 0
        return cadena

    def s_2(self, char, cadena):
        if char.isalpha() or char in ["_", " "]:
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.s_2(cadena[0], cadena)
        elif char in ['"', "\n", "\t", ",", "}", "(", "="]:
            token_type = None
            for pat, tipo in self.patrones:
                if pat == self.buffer:
                    token_type = tipo
                    break

            if token_type:
                self.agregar_token(token_type, self.buffer)
                self.estado = 0
                self.buffer = ""
            else:
                self.agregar_token(TipoToken.STRING, self.buffer)
                self.estado = 0
                self.buffer = ""
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.buffer = ""
            self.estado = 0
        return cadena

    def s_3(self, char, cadena):
        self.es_decimal = False
        if char.isdigit():
            # self.columna += 1
            cadena = cadena[1:]
            self.buffer += char
            self.estado = 3
        elif char == "." and not self.es_decimal:
            self.es_decimal = True
            self.buffer += char
            self.estado = 3
            cadena = cadena[1:]
        elif char in ['"', "\n", "\t", " ", ",", "}"]:
            self.agregar_token(TipoToken.NUMERO, self.buffer)
            self.estado = 0
            self.buffer = ""
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
        return cadena

    def s_4(self, char, cadena):
        if char == '"':
            self.estado = 8
            self.columna += 1
            self.agregar_token_sin_c(TipoToken.COMILLAS_TRIPLES, '"""', 3)
            self.com_abierto = True
            cadena = cadena[1:]
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 0
        return cadena

    def s_5(self, char, cadena):
        if char != '"':
            self.estado = 5
            cadena = cadena[1:]
            self.buffer += char
        else:
            cadena = cadena[1:]
            self.estado = 0
            # self.columna += 1
            self.agregar_token(TipoToken.STRING, self.buffer)
            self.buffer = ""

        return cadena

    def s_6(self, char, cadena):
        if char == '"':
            self.estado = 8
            self.columna += 1
            self.agregar_token_sin_c(TipoToken.COMENTARIO_M, '"""', 3)
            self.com_abierto = True
            cadena = cadena[1:]
        else:
            self.crear_error(char, self.fila, self.columna)
            self.columna += 1
            cadena = cadena[1:]
            self.estado = 0
        return cadena

    def s_7(self, cadena):
        char = cadena[0]
        if char != "\n":
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.s_7(cadena)
        else:
            self.agregar_token(TipoToken.COMENTARIO, self.buffer)
            self.estado = 0
            self.comentario_1 = False
            self.buffer = ""
        # self.buffer += char
        return cadena

    def s_8(self, cadena):
        char = cadena[0]
        if char != '"':
            # self.estado = 8
            if char == "\n":
                self.fila += 1
            cadena = cadena[1:]
            self.buffer += char
            cadena = self.s_8(cadena)
        else:
            self.agregar_token(TipoToken.COMENTARIO_M, self.buffer)
            cadena = cadena[1:]
            self.estado = 9
            self.buffer = ""
            self.columna += 1
            # self.buffer = ""
        return cadena

    def s_9(self, cadena):
        char = cadena[0]
        if char == '"':
            self.estado = 10
            self.columna += 1
            # self.agregar_token_sin_c(TipoToken.COMILLAS_TRIPLES, '"""', 3)
            # self.com_abierto = False
            cadena = cadena[1:]
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 0

        return cadena

    def s_10(self, cadena):
        char = cadena[0]
        if char == '"':
            self.estado = 0
            self.columna += 1
            self.agregar_token_sin_c(TipoToken.COMILLAS_TRIPLES, '"""', 3)
            self.com_abierto = False
            cadena = cadena[1:]
        else:
            self.crear_error(char, self.fila, self.columna)
            cadena = cadena[1:]
            self.estado = 0
        return cadena

    def imprimir(self):
        for i, dato in enumerate(self.tokens):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
