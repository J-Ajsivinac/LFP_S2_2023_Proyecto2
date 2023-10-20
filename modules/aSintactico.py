from modules.aLexico import AnalizadorLexico
from modules.Tipo import TipoToken
from modules.Abstract.error import Error
from modules.control import Control
import copy


class AnalizadorSintactico:
    def __init__(self, lista_tokens, ctrl: Control):
        self.lista_tokens = lista_tokens
        self.copia = copy.deepcopy(lista_tokens)
        self.errores_s = []
        self.salidas_asig = [
            TipoToken.COMENTARIO,
            TipoToken.COMENTARIO_M,
            TipoToken.R_CLAVES,
            TipoToken.R_REGISTROS,
        ]
        self.reservadas = [
            TipoToken.R_IMPRIMIR,
            TipoToken.R_IMPRIMIRLN,
            TipoToken.R_CONTEO,
            TipoToken.R_PROMEDIO,
            TipoToken.R_CONTARSI,
            TipoToken.R_DATOS,
            TipoToken.R_SUMAR,
            TipoToken.R_MAX,
            TipoToken.R_MIN,
            TipoToken.R_EXPORTAR,
        ]
        self.es_ultimo = False
        self.ctrl = ctrl
        self.diccionario = ctrl.matriz
        self.claves = None
        self.contador = 0
        self.size = 0
        self.size_list = 0
        self.datos_grafica = []

    def eliminar_primero(self):
        try:
            return self.lista_tokens.pop(0)
        except Exception as _:
            if not self.es_ultimo:
                ultimo = self.copia[-1]
                ultimo.columna += len(ultimo.valor)
                self.es_ultimo = True
                return ultimo
            return None

    def crear_error(self, datos, fila, columna):
        if datos is None:
            return
        self.errores_s.append(Error("Error Sintáctico", datos, fila, columna))

    def parser(self):
        if len(self.lista_tokens) > 0:
            inicio = []
            self.datos_grafica.append("inicio")
            self.inicio(inicio)
            self.datos_grafica.append(inicio)

    def inicio(self, inicio: list):
        if len(self.lista_tokens) == 0:
            return
        inicio.append("comando")
        comando = []
        self.comando(comando)
        inicio.append(comando)
        if len(self.lista_tokens) == 0:
            return
        # self.datos_grafica.append("<")
        # inicio.append("otro comando")
        self.otro_comando(inicio)

    def comando(self, comando: list):
        actual = self.eliminar_primero()
        if actual.tipo in [TipoToken.COMENTARIO, TipoToken.COMENTARIO_M]:
            comando.append(actual.valor)
            return
        if actual.tipo in [TipoToken.R_CLAVES]:
            comando.append("asignacion")
            asignacion = []
            asignacion.append(actual.valor)
            self.asignacion(asignacion)
            comando.append(asignacion)
            self.claves = list(self.diccionario.keys())
            self.size = len(self.claves)
        elif actual.tipo in [TipoToken.R_REGISTROS]:
            comando.append("asignacion")
            asignacion = []
            asignacion.append(actual.valor)
            self.registros(asignacion)
            comando.append(asignacion)
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
            comando.append("instruccion")
            instruccion = []
            instruccion.append(actual.valor)
            actual_valor = actual.tipo
            resp, resp2 = self.instruccion(actual, instruccion)
            comando.append(instruccion)
            actual = self.eliminar_primero()
            if actual is None:
                return
            if actual and actual.tipo == TipoToken.PUNTO_COMA:
                instruccion.append(actual.valor)
                if actual_valor == TipoToken.R_CONTARSI:
                    if resp is not None and resp2 is not None:
                        self.usar_operacion(actual_valor, resp, resp2)
                elif resp is not None:
                    self.usar_operacion(actual_valor, resp)
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

    def otro_comando(self, inicio: list):
        if len(self.lista_tokens) > 0:
            inicio.append("otro comando")
            otro_comando = []
            otro_comando.append("inicio")
            inicio_2 = []
            self.inicio(inicio_2)
            otro_comando.append(inicio_2)
            inicio.append(otro_comando)
            # self.inicio()

    def asignacion(self, asignacion: list):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            asignacion.append(actual.valor)
            # self.datos_grafica.append(f"{actual.valor}")
            # self.datos_grafica.append("<")
            asignacion.append("declaracion_c")
            declaracion_c = []
            self.declaracion_c(declaracion_c=declaracion_c)
            asignacion.append(declaracion_c)
            # self.datos_grafica.append(">")
        else:
            self.crear_error(
                "Se esperaba un = ",
                actual.fila,
                actual.columna,
            )
            self.declaracion_c(actual=actual)

    def declaracion_c(self, actual=None, declaracion_c: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            if declaracion_c is not None:
                declaracion_c.append(actual.valor)
                declaracion_c.append("Elementos")
            elementos = []
            self.elementos(elementos=elementos)
            if declaracion_c is not None:
                declaracion_c.append(elementos)
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                if declaracion_c is not None:
                    declaracion_c.append(actual.valor)
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

    def elementos(self, actual=None, elementos: list = None):
        # self.datos_grafica.append("Elementos")
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.STRING:
            # self.datos_grafica.append(f"{actual.valor}")
            # rec_elementos.append(actual.valor)
            if elementos is not None:
                elementos.append(actual.valor)
            self.diccionario[actual.valor] = []
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA or (
                len(self.lista_tokens) == 0 and actual.tipo != TipoToken.COMA
            ):
                # self.datos_grafica.append(">")
                self.lista_tokens.insert(0, actual)
                return
            if actual.tipo == TipoToken.COMA:
                # rec_elementos = []
                elementos.append(actual.valor)
                elementos.append("Elementos")
                elementos1 = []
                # self.datos_grafica.append("Elementos")
                self.elementos(elementos=elementos1)
                elementos.append(elementos1)
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
                TipoToken.LLAVE_CERRADURA,
                TipoToken.R_CLAVES,
                TipoToken.R_REGISTROS,
                TipoToken.COMENTARIO_M,
                TipoToken.COMENTARIO,
                TipoToken.CORCHETE_CERRADURA,
            ]:
                self.lista_tokens.insert(0, actual)
                return
            else:
                self.elementos()

    def instruccion(self, valor, instruccion: list):
        respuesta = None
        respuesta2 = None
        if valor.tipo in [
            TipoToken.R_IMPRIMIR,
            TipoToken.R_IMPRIMIRLN,
            TipoToken.R_PROMEDIO,
            TipoToken.R_SUMAR,
            TipoToken.R_MAX,
            TipoToken.R_MIN,
            TipoToken.R_EXPORTAR,
        ]:
            # instruccion_1 = []
            respuesta = self.instruccion_1(instruccion=instruccion)
        elif valor.tipo in [TipoToken.R_DATOS, TipoToken.R_CONTEO]:
            respuesta = self.instruccion_0(instruccion=instruccion)
        elif valor.tipo in [TipoToken.R_CONTARSI]:
            respuesta, respuesta2 = self.instruccion_2(instruccion=instruccion)
        return respuesta, respuesta2

    def instruccion_0(self, instruccion: list = None):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            # self.datos_grafica.append(actual.valor)
            instruccion.append(actual.valor)
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                instruccion.append(actual.valor)
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
        return "exito"

    def instruccion_1(self, instruccion: list = None):
        valor = None
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            # self.datos_grafica.append(actual.valor)
            instruccion.append(actual.valor)
            # instruccion_1 = []
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.STRING:
                instruccion.append(actual.valor)
                # self.datos_grafica.append(actual.valor)
                valor = actual.valor
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    instruccion.append(actual.valor)
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
                if len(self.lista_tokens) == 0:
                    return
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
                if len(self.lista_tokens) == 0:
                    return
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                )
                actual = self.eliminar_primero()
                if actual is None:
                    return
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )",
                        actual.fila,
                        actual.columna,
                    )
        return valor

    def instruccion_2(self, instruccion: list = None):
        valor1 = None
        valor2 = None
        actual = self.eliminar_primero()
        parentesis = False
        if actual.tipo != TipoToken.PARENTESIS_APERTURA:
            self.crear_error(
                "Se esperaba un (",
                actual.fila,
                actual.columna,
            )
            parentesis = True
        else:
            instruccion.append(actual.valor)
        if not parentesis:
            actual = self.eliminar_primero()
        string = False
        if actual.tipo == TipoToken.STRING:
            instruccion.append(actual.valor)
            valor1 = actual.valor
        else:
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
        else:
            instruccion.append(actual.valor)
        if not coma:
            # self.datos_grafica.append(actual.valor)
            actual = self.eliminar_primero()
        entero = False
        if (
            actual.tipo == TipoToken.ENTERO
            or actual.tipo == TipoToken.STRING
            or actual.tipo == TipoToken.REAL
        ):
            instruccion.append(actual.valor)
            valor2 = actual.valor
        else:
            self.crear_error(
                "Se esperaba un entero | cadena de text | decimal",
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
        else:
            instruccion.append(actual.valor)
        return valor1, valor2

    def registros(self, asignacion: list):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            asignacion.append(actual.valor)
            asignacion.append("declaracion_r")
            declaracion_r = []
            self.declaracion_r(declaracion_r=declaracion_r)
            asignacion.append(declaracion_r)
        else:
            self.crear_error(
                "Se esperaba un =",
                actual.fila,
                actual.columna,
            )
            self.declaracion_r(actual)

    def declaracion_r(self, actual=None, declaracion_r: list = None):
        # self.datos_grafica.append("")
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            if declaracion_r is not None:
                declaracion_r.append(actual.valor)
                declaracion_r.append("arreglos")
            arreglos = []
            self.arreglos(arreglos=arreglos)
            if declaracion_r is not None:
                declaracion_r.append(arreglos)
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                if declaracion_r is not None:
                    declaracion_r.append(actual.valor)
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
            if actual is None:
                return
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un }",
                    actual.fila,
                    actual.columna,
                )

    def arreglos(self, actual=None, arreglos: list = None):
        # self.datos_grafica.append("Arreglos")
        if actual is None:
            if len(self.lista_tokens) > 0:
                actual = self.eliminar_primero()

        if actual is None:
            actual = self.eliminar_primero()
            self.crear_error(
                "Se esperaba un {",
                actual.fila,
                actual.columna,
            )
            return

        if actual.tipo == TipoToken.LLAVE_APERTURA:
            self.size_list += 1
            if arreglos is not None:
                arreglos.append(actual.valor)
                arreglos.append("Elementos_r")
            elementos_r = []
            self.elementos_r(elementos_r=elementos_r)
            if arreglos is not None:
                arreglos.append(elementos_r)
            actual = self.eliminar_primero()

            if actual.tipo == TipoToken.LLAVE_CERRADURA:
                self.contador = 0
                if arreglos is not None:
                    arreglos.append(actual.valor)
            else:
                self.crear_error(
                    "Se esperaba un }",
                    actual.fila,
                    actual.columna,
                )
                self.arreglos(actual)
            if (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.LLAVE_APERTURA
            ):
                arreglos.append("arreglos")
                arreglos1 = []
                self.arreglos(arreglos=arreglos1)
                arreglos.append(arreglos1)
            elif (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.CORCHETE_CERRADURA
            ):
                return
            else:
                if len(self.lista_tokens) > 0:
                    self.arreglos()
        else:
            self.crear_error(
                "Se esperaba un {",
                actual.fila,
                actual.columna,
            )
            self.size_list += 1
            self.elementos_r(actual)
            if actual == TipoToken.LLAVE_CERRADURA:
                self.contador = 0
                if arreglos is not None:
                    arreglos.append(actual.valor)
            else:
                self.crear_error(
                    "Se esperaba un }",
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

    def elementos_r(self, actual=None, elementos_r: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo in [TipoToken.STRING, TipoToken.ENTERO, TipoToken.REAL]:
            valor = actual.valor
            if actual.tipo in [TipoToken.STRING]:
                valor = valor.replace('"', "")
            if elementos_r is not None:
                elementos_r.append(valor)
            if self.contador < self.size:
                self.diccionario[self.claves[self.contador]].append(valor)
                self.contador += 1
            actual = self.eliminar_primero()
            if actual is None:
                return
            if actual.tipo == TipoToken.COMA:
                elementos_r.append(actual.valor)
                elementos_r.append("Elementos_r")
                elementos_r1 = []
                self.elementos_r(elementos_r=elementos_r1)
                elementos_r.append(elementos_r1)
            elif actual.tipo == TipoToken.LLAVE_CERRADURA:
                if self.contador < self.size:
                    faltantes = self.size - self.contador
                    self.crear_error(
                        f"Falta {faltantes} valores en el arreglo",
                        actual.fila,
                        actual.columna - 1,
                    )
                    for key in self.claves:
                        if len(self.diccionario[key]) == self.size_list:
                            self.diccionario[key].pop()
                        # self.diccionario[key].pop()
                    self.size_list -= 1
                self.lista_tokens.insert(0, actual)
                return
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
                self.lista_tokens.insert(0, actual)
                return
            else:
                # self.diccionario[self.claves[self.contador]].append(None)
                # self.contador += 1
                if len(self.lista_tokens) > 0:
                    self.elementos_r()

    def usar_operacion(self, tipo, valor1=None, valor2=None):
        if tipo == TipoToken.R_IMPRIMIR:
            self.ctrl.imprimir(valor1.replace('"', ""))
        elif tipo == TipoToken.R_IMPRIMIRLN:
            self.ctrl.imprimirln(valor1.replace('"', ""))
        elif tipo == TipoToken.R_CONTEO:
            self.ctrl.conteo()
        elif tipo == TipoToken.R_PROMEDIO:
            self.ctrl.promedio(valor1)
        elif tipo == TipoToken.R_CONTARSI:
            self.ctrl.contarsi(valor1, valor2)
        elif tipo == TipoToken.R_DATOS:
            self.ctrl.datos()
        elif tipo == TipoToken.R_SUMAR:
            self.ctrl.sumar(valor1)
        elif tipo == TipoToken.R_MAX:
            self.ctrl.get_max(valor1)
        elif tipo == TipoToken.R_MIN:
            self.ctrl.get_min(valor1)
        elif tipo == TipoToken.R_EXPORTAR:
            self.ctrl.exportar(valor1)

    def imprimir(self):
        for _, dato in enumerate(self.errores_s):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            print(valor, tipo, fila, columna)
