from modules.aLexico import AnalizadorLexico
from modules.Tipo import TipoToken
from modules.Abstract.error import Error
import copy


class AnalizadorSintactico:
    def __init__(self, lista_tokens):
        self.lista_tokens = lista_tokens
        self.copia = copy.deepcopy(lista_tokens)
        self.errores_s = []
        self.es_ultimo = False

    def eliminar_primero(self):
        try:
            return self.lista_tokens.pop(0)
        except Exception as _:
            ultimo = self.copia[-1]
            if not self.es_ultimo:
                ultimo.columna += len(ultimo.valor)
                self.es_ultimo = True
            else:
                ultimo.columna += 1
            return ultimo
            # return None

    def crear_error(self, datos, fila, columna):
        if datos is None:
            return
        self.errores_s.append(Error("Error Sintáctico", datos, fila, columna))

    def parser(self):
        while self.lista_tokens:
            actual = self.eliminar_primero()

            if actual.tipo in [TipoToken.COMENTARIO, TipoToken.COMENTARIO_M]:
                continue
            if actual.tipo in [TipoToken.R_CLAVES]:
                self.asignacion()
            elif actual.tipo in [TipoToken.R_REGISTROS]:
                self.registros()
            elif actual.tipo in [
                TipoToken.R_CONTARSI,
                TipoToken.R_EXPORTAR,
                TipoToken.R_CONTEO,
                TipoToken.R_DATOS,
                TipoToken.R_IMPRIMIR,
                TipoToken.R_IMPRIMIRLN,
                TipoToken.R_MAX,
                TipoToken.R_MIN,
                TipoToken.R_SUMAR,
                TipoToken.R_PROMEDIO,
            ]:
                self.instruccion(actual)
                actual = self.eliminar_primero()
                if actual and actual.tipo == TipoToken.PUNTO_COMA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un ; ",
                        actual.fila,
                        actual.columna,
                    )
                    if len(self.lista_tokens) > 0:
                        self.lista_tokens.insert(0, actual)
            else:
                self.crear_error(
                    "Se esperaba una palabra reservada | clave | comentario | registro",
                    actual.fila,
                    actual.columna,
                )

    def asignacion(self):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            self.declaracion_c()
        else:
            self.crear_error(
                "Se esperaba un = ",
                actual.fila,
                actual.columna,
            )
            self.declaracion_c(actual)

    def declaracion_c(self, actual=None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            self.elementos()
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un ]",
                    actual.fila,
                    actual.columna,
                )
        else:
            self.crear_error(
                "Se esperaba un [",
                actual.fila,
                actual.columna,
            )
            self.elementos(actual)

    def elementos(self, actual=None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.STRING:
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA or (
                len(self.lista_tokens) == 0 and actual.tipo != TipoToken.COMA
            ):
                self.lista_tokens.insert(0, actual)
                return
            if actual.tipo == TipoToken.COMA:
                self.elementos()
            else:
                self.crear_error(
                    "Se esperaba una ,",
                    actual.fila,
                    actual.columna,
                )
                if len(self.lista_tokens) > 0:
                    self.elementos(actual)

        else:
            self.crear_error(
                "Se esperaba una cadena de texto",
                actual.fila,
                actual.columna,
            )
            if actual.tipo not in [
                TipoToken.CORCHETE_CERRADURA,
                TipoToken.R_CLAVES,
                TipoToken.R_REGISTROS,
                TipoToken.COMENTARIO_M,
                TipoToken.COMENTARIO,
            ]:
                return
            else:
                self.elementos()

    def parametros(self):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.COMA:
            actual = self.eliminar_primero()
            if actual == TipoToken.STRING:
                pass
            else:
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                )
        else:
            self.crear_error(
                "Se esperaba una ,",
                actual.fila,
                actual.columna,
            )

    def instruccion(self, valor):
        if valor.tipo in [
            TipoToken.R_IMPRIMIR,
            TipoToken.R_IMPRIMIRLN,
            TipoToken.R_PROMEDIO,
            TipoToken.R_SUMAR,
            TipoToken.R_MAX,
            TipoToken.R_MIN,
            TipoToken.R_EXPORTAR,
        ]:
            self.instruccion_1()
        elif valor.tipo in [TipoToken.R_DATOS, TipoToken.R_CONTEO]:
            self.instruccion_0()
        elif valor.tipo in [TipoToken.R_CONTARSI]:
            self.instruccion_2()
            # if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
            #     pass
            # else:
            #     self.crear_error(
            #         "Se esperaba una )",
            #         actual.fila,
            #         actual.columna,
            #     )

    def instruccion_0(self):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un )",
                    actual.fila,
                    actual.columna,
                )
        else:
            self.crear_error(
                "Se esperaba un (",
                actual.fila,
                actual.columna,
            )
            if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un )",
                    actual.fila,
                    actual.columna,
                )

    def instruccion_1(self):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.STRING:
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )",
                        actual.fila,
                        actual.columna,
                    )
            else:
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                )
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )",
                        actual.fila,
                        actual.columna,
                    )
        else:
            self.crear_error(
                "Se esperaba un (",
                actual.fila,
                actual.columna,
            )
            if actual.tipo == TipoToken.STRING:
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )",
                        actual.fila,
                        actual.columna,
                    )
            else:
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                )
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )",
                        actual.fila,
                        actual.columna,
                    )

    def instruccion_2(self):
        actual = self.eliminar_primero()
        parentesis = False
        if actual.tipo != TipoToken.PARENTESIS_APERTURA:
            self.crear_error(
                "Se esperaba un (",
                actual.fila,
                actual.columna,
            )
            parentesis = True
        if not parentesis:
            actual = self.eliminar_primero()
        string = False
        if actual.tipo != TipoToken.STRING:
            self.crear_error(
                "Se esperaba una cadena de texto",
                actual.fila,
                actual.columna,
            )
            string = True
        if not string:
            actual = self.eliminar_primero()
        coma = False
        if actual.tipo != TipoToken.COMA:
            self.crear_error(
                "Se esperaba una ,",
                actual.fila,
                actual.columna,
            )
            coma = True
        if not coma:
            actual = self.eliminar_primero()
        entero = False
        if actual.tipo != TipoToken.ENTERO:
            self.crear_error(
                "Se esperaba un entero",
                actual.fila,
                actual.columna,
            )
            entero = True
        if not entero:
            actual = self.eliminar_primero()
        if actual.tipo != TipoToken.PARENTESIS_CERRADURA:
            self.crear_error(
                "Se esperaba un )",
                actual.fila,
                actual.columna,
            )

    def registros(self):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            self.declaracion_r()
        else:
            self.crear_error(
                "Se esperaba un =",
                actual.fila,
                actual.columna,
            )
            self.declaracion_r(actual)

    def declaracion_r(self, actual=None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            self.arreglos()
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un ]",
                    actual.fila,
                    actual.columna,
                )
        else:
            self.crear_error(
                "Se esperaba un [",
                actual.fila,
                actual.columna,
            )
            self.arreglos()
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un }",
                    actual.fila,
                    actual.columna,
                )

    def arreglos(self, actual=None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.LLAVE_APERTURA:
            self.elementos_r()

            if (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.LLAVE_APERTURA
            ):
                self.arreglos()
            elif (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.CORCHETE_CERRADURA
            ):
                return
            else:
                if len(self.lista_tokens) > 0:
                    self.arreglos()
            #     self.crear_error(
            #         "Se esperaba un {",
            #         self.lista_tokens[0].fila,
            #         self.lista_tokens[0].columna,
            #     )
            #     self.arreglos()
        else:
            self.crear_error(
                "Se esperaba un {",
                actual.fila,
                actual.columna,
            )
            self.elementos_r(actual)
            if (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.LLAVE_APERTURA
            ):
                self.arreglos()
            elif (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.CORCHETE_CERRADURA
            ):
                return
            else:
                # self.crear_error(actual)
                if len(self.lista_tokens) > 0:
                    self.arreglos()

    def elementos_r(self, actual=None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo in [TipoToken.STRING, TipoToken.ENTERO, TipoToken.REAL]:
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.COMA:
                self.elementos_r()

            elif actual.tipo == TipoToken.LLAVE_CERRADURA:
                return
            else:
                self.crear_error(
                    "Se esperaba un }",
                    actual.fila,
                    actual.columna,
                )
                self.lista_tokens.insert(0, actual)
        else:
            self.crear_error(
                "Se esperaba un Entero | Decimal | Cadena de texto",
                actual.fila,
                actual.columna,
            )
            if actual.tipo not in [
                TipoToken.LLAVE_CERRADURA,
                TipoToken.R_CLAVES,
                TipoToken.R_REGISTROS,
                TipoToken.COMENTARIO_M,
                TipoToken.COMENTARIO,
            ]:
                return
            else:
                self.elementos_r()

    def imprimir(self):
        for _, dato in enumerate(self.errores_s):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
