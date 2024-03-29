from modules.aLexico import AnalizadorLexico
from modules.Tipo import TipoToken
from modules.Abstract.error import Error
from modules.control import Control
import copy


class AnalizadorSintactico:
    def __init__(self, lista_tokens, ctrl: Control):
        self.tokens_originales = lista_tokens
        self.lista_tokens = self.eliminar_comentario()
        self.copia = copy.deepcopy(self.lista_tokens)
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

    def eliminar_comentario(self):
        nueva_lista = []
        for value in self.tokens_originales:
            if value.tipo not in [TipoToken.COMENTARIO, TipoToken.COMENTARIO_M]:
                nueva_lista.append(value)
        return nueva_lista

    def eliminar_primero(self):
        try:
            return self.lista_tokens.pop(0)
        except Exception as _:
            if not self.es_ultimo:
                ultimo = self.copia[-1]
                if isinstance(ultimo.valor, str):
                    ultimo.columna += len(ultimo.valor)
                elif isinstance(ultimo.valor, (int, float)):
                    ultimo.columna += len(str(ultimo.valor))
                self.es_ultimo = True
                return ultimo
            return None

    def crear_error(self, datos, fila, columna, leido):
        if datos is None:
            return
        self.errores_s.append(Error("Error Sintáctico", datos, fila, columna, leido))

    def parser(self):
        if len(self.lista_tokens) > 0:
            inicio = []
            self.datos_grafica.append("INICIO")
            self.inicio(inicio)
            self.datos_grafica.append(inicio)

    def inicio(self, inicio: list):
        if len(self.lista_tokens) == 0:
            return

        while len(self.lista_tokens) != 0:
            inicio.append("COMANDO")
            comando = []
            self.comando(comando)
            inicio.append(comando)
            if len(self.lista_tokens) == 0:
                break
        # self.otro_comando(inicio)

    def comando(self, comando: list):
        actual = self.eliminar_primero()
        if actual.tipo in [TipoToken.COMENTARIO, TipoToken.COMENTARIO_M]:
            comando.append(actual.valor)
            return
        if actual.tipo in [TipoToken.R_CLAVES]:
            comando.append("ASIGNACION")
            asignacion = []
            asignacion.append(actual.valor)
            self.asignacion(asignacion)
            comando.append(asignacion)
            self.claves = list(self.diccionario.keys())
            self.size = len(self.claves)
        elif actual.tipo in [TipoToken.R_REGISTROS]:
            comando.append("ASIGNACION")
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
            comando.append("INSTRUCCIÓN")
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
                    "Se esperaba un ; ", actual.fila, actual.columna, actual.valor
                )
                if len(self.lista_tokens) > 0:
                    self.lista_tokens.insert(0, actual)
        else:
            self.crear_error(
                "Se esperaba una palabra reservada | clave  | registro",
                actual.fila,
                actual.columna,
                actual.valor,
            )

    def otro_comando(self, inicio: list):
        if len(self.lista_tokens) > 0:
            inicio.append("OTRO COMANDO")
            otro_comando = []
            otro_comando.append("INICIO")
            inicio_2 = []
            self.inicio(inicio_2)
            otro_comando.append(inicio_2)
            inicio.append(otro_comando)

    def asignacion(self, asignacion: list):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            asignacion.append(actual.valor)
            asignacion.append("declaracion_c")
            declaracion_c = []
            self.declaracion_c(declaracion_c=declaracion_c)
            asignacion.append(declaracion_c)
        else:
            self.crear_error(
                "Se esperaba un = ", actual.fila, actual.columna, actual.valor
            )
            self.declaracion_c(actual=actual)

    def declaracion_c(self, actual=None, declaracion_c: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            if declaracion_c is not None:
                declaracion_c.append(actual.valor)
                declaracion_c.append("ELEMENTOS")
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
                    "Se esperaba un ]", actual.fila, actual.columna, actual.valor
                )
        else:
            self.crear_error(
                "Se esperaba un [", actual.fila, actual.columna, actual.valor
            )
            self.elementos(actual)

    def elementos(self, actual=None, elementos: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.STRING:
            if elementos is not None:
                elementos.append("VALOR")
                variable = []
                variable.append(actual.valor)
                elementos.append(variable)
            valor_key = actual.valor.replace('"', "")
            if len(valor_key.strip()) != 0:
                self.diccionario[actual.valor] = []
            else:
                self.crear_error(
                    "La clave no puede ser vacia",
                    actual.fila,
                    actual.columna,
                    actual.valor,
                )
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA or (
                len(self.lista_tokens) == 0 and actual.tipo != TipoToken.COMA
            ):
                self.lista_tokens.insert(0, actual)
                return
            if actual.tipo == TipoToken.COMA:
                if elementos is not None:
                    elementos.append(actual.valor)
                    elementos.append("ELEMENTOS")
                elementos1 = []
                self.elementos(elementos=elementos1)
                if elementos is not None:
                    elementos.append(elementos1)
            else:
                self.crear_error(
                    "Se esperaba una ,", actual.fila, actual.columna, actual.valor
                )
                if len(self.lista_tokens) > 0:
                    self.elementos(actual)

        else:
            if actual.tipo in [
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
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                    actual.valor,
                )
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
            respuesta = self.instruccion_1(instruccion=instruccion)
        elif valor.tipo in [TipoToken.R_DATOS, TipoToken.R_CONTEO]:
            respuesta = self.instruccion_0(instruccion=instruccion)
        elif valor.tipo in [TipoToken.R_CONTARSI]:
            respuesta, respuesta2 = self.instruccion_2(instruccion=instruccion)
        return respuesta, respuesta2

    def instruccion_0(self, instruccion: list = None):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            instruccion.append(actual.valor)
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                instruccion.append(actual.valor)
            else:
                self.crear_error(
                    "Se esperaba un )", actual.fila, actual.columna, actual.valor
                )
        else:
            self.crear_error(
                "Se esperaba un (", actual.fila, actual.columna, actual.valor
            )
            if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un )", actual.fila, actual.columna, actual.valor
                )
        return "exito"

    def instruccion_1(self, instruccion: list = None):
        valor = None
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.PARENTESIS_APERTURA:
            fila_comando = actual.fila
            columna_comando = actual.columna
            if instruccion is not None:
                instruccion.append(actual.valor)
            actual = self.eliminar_primero()
            if actual.tipo == TipoToken.STRING:
                a = []
                if instruccion is not None:
                    instruccion.append("A")
                    a.append(actual.valor)
                    instruccion.append(a)

                valor = actual.valor
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    if instruccion is not None:
                        instruccion.append(actual.valor)
                else:
                    self.crear_error(
                        "Se esperaba un )", actual.fila, actual.columna, actual.valor
                    )
            else:
                fila = actual.fila if actual.fila == fila_comando else fila_comando
                columna = (
                    actual.columna
                    if actual.columna == columna_comando
                    else columna_comando + 1
                )
                self.crear_error(
                    "Se esperaba una cadena de texto", fila, columna, actual.valor
                )
                if actual.tipo in self.salidas_asig or actual.tipo in self.reservadas:
                    self.lista_tokens.insert(0, actual)
                    return None

                if len(self.lista_tokens) == 0:
                    return
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )", actual.fila, actual.columna, actual.valor
                    )
        else:
            self.crear_error(
                "Se esperaba un (", actual.fila, actual.columna, actual.valor
            )
            if actual.tipo == TipoToken.STRING:
                actual = self.eliminar_primero()
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )", actual.fila, actual.columna, actual.valor
                    )
            else:
                if len(self.lista_tokens) == 0:
                    return
                self.crear_error(
                    "Se esperaba una cadena de texto",
                    actual.fila,
                    actual.columna,
                    actual.valor,
                )
                actual = self.eliminar_primero()
                if actual is None:
                    return
                if actual.tipo == TipoToken.PARENTESIS_CERRADURA:
                    pass
                else:
                    self.crear_error(
                        "Se esperaba un )", actual.fila, actual.columna, actual.valor
                    )
        return valor

    def instruccion_2(self, instruccion: list = None):
        valor1 = None
        valor2 = None
        parametros = None
        elemento_parametro = None
        actual = self.eliminar_primero()
        parentesis = False
        if actual.tipo != TipoToken.PARENTESIS_APERTURA:
            self.crear_error(
                "Se esperaba un (", actual.fila, actual.columna, actual.valor
            )
            parentesis = True
        else:
            if instruccion is not None:
                instruccion.append(actual.valor)
                instruccion.append("PARAMETROS")
                parametros = []
        if not parentesis:
            actual = self.eliminar_primero()
        string = False
        if actual.tipo == TipoToken.STRING:
            if parametros is not None:
                a = []
                parametros.append("A")
                a.append(actual.valor)
                parametros.append(a)
            valor1 = actual.valor
        else:
            self.crear_error(
                "Se esperaba una cadena de texto",
                actual.fila,
                actual.columna,
                actual.valor,
            )
            string = True
        if not string:
            actual = self.eliminar_primero()
        coma = False
        if actual.tipo != TipoToken.COMA:
            self.crear_error(
                "Se esperaba una ,", actual.fila, actual.columna, actual.valor
            )
            coma = True
        else:
            if parametros is not None:
                parametros.append(actual.valor)
        if not coma:
            actual = self.eliminar_primero()
        entero = False
        if (
            actual.tipo == TipoToken.ENTERO
            or actual.tipo == TipoToken.STRING
            or actual.tipo == TipoToken.REAL
        ):
            if parametros is not None:
                parametros.append("ELEMENTO PARAMETRO")
            elemento_parametro = []
            elemento_parametro.append(actual.valor)
            valor2 = actual.valor
        else:
            self.crear_error(
                "Se esperaba un entero | cadena de texto | decimal",
                actual.fila,
                actual.columna,
                actual.valor,
            )
            entero = True
        if not entero:
            actual = self.eliminar_primero()
        if actual.tipo != TipoToken.PARENTESIS_CERRADURA:
            self.crear_error(
                "Se esperaba un )", actual.fila, actual.columna, actual.valor
            )
        else:
            if instruccion is not None:
                if parametros is not None:
                    parametros.append(elemento_parametro)
                if instruccion is not None:
                    instruccion.append(parametros)
                    instruccion.append(actual.valor)
        return valor1, valor2

    def registros(self, asignacion: list):
        actual = self.eliminar_primero()
        if actual.tipo == TipoToken.IGUAL:
            if asignacion is not None:
                asignacion.append(actual.valor)
                asignacion.append("DECLARACION_R")
            declaracion_r = []
            self.declaracion_r(declaracion_r=declaracion_r)
            if asignacion is not None:
                asignacion.append(declaracion_r)
        else:
            self.crear_error(
                "Se esperaba un =", actual.fila, actual.columna, actual.valor
            )
            self.declaracion_r(actual)

    def declaracion_r(self, actual=None, declaracion_r: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo == TipoToken.CORCHETE_APERTURA:
            if declaracion_r is not None:
                declaracion_r.append(actual.valor)
                declaracion_r.append("ARREGLOS")
            arreglos = []
            self.arreglos(arreglos=arreglos)
            if declaracion_r is not None:
                declaracion_r.append(arreglos)
            actual = self.eliminar_primero()
            if actual is None:
                return
            if actual.tipo == TipoToken.LLAVE_APERTURA:
                self.arreglos(actual)
                actual = self.eliminar_primero()
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                if declaracion_r is not None:
                    declaracion_r.append(actual.valor)
            else:
                self.crear_error(
                    "Se esperaba un ]", actual.fila, actual.columna, actual.valor
                )
        else:
            self.crear_error(
                "Se esperaba un [", actual.fila, actual.columna, actual.valor
            )
            self.arreglos()
            actual = self.eliminar_primero()
            if actual is None:
                return
            if actual.tipo == TipoToken.CORCHETE_CERRADURA:
                pass
            else:
                self.crear_error(
                    "Se esperaba un }", actual.fila, actual.columna, actual.valor
                )

    def arreglos(self, actual=None, arreglos: list = None):
        if actual is None:
            if len(self.lista_tokens) > 0:
                actual = self.eliminar_primero()

        if actual is None:
            actual = self.eliminar_primero()
            self.crear_error(
                "Se esperaba un {", actual.fila, actual.columna, actual.valor
            )
            return

        if actual.tipo == TipoToken.LLAVE_APERTURA:
            self.size_list += 1
            if arreglos is not None:
                arreglos.append(actual.valor)
                arreglos.append("ELEMENTOS_R")
            elementos_r = []
            self.elementos_r(elementos_r=elementos_r)
            if arreglos is not None:
                arreglos.append(elementos_r)
            actual = self.eliminar_primero()
            if actual is None:
                self.crear_error(
                    "Se esperaba un }",
                    self.copia[-1].fila,
                    self.copia[-1].columna,
                    actual.valor,
                )
                return
            if actual.tipo == TipoToken.LLAVE_CERRADURA:
                self.contador = 0
                if arreglos is not None:
                    arreglos.append(actual.valor)
            else:
                self.crear_error(
                    "Se esperaba un }", actual.fila, actual.columna, actual.valor
                )
                if actual.tipo in self.reservadas or actual.tipo in self.reservadas:
                    self.lista_tokens.insert(0, actual)
                    return
                self.arreglos(actual)
            if (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.LLAVE_APERTURA
            ):
                if arreglos is not None:
                    arreglos.append("ARREGLOS")
                arreglos1 = []
                self.arreglos(arreglos=arreglos1)
                if arreglos is not None:
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
                "Se esperaba un {", actual.fila, actual.columna, actual.valor
            )
            self.size_list += 1
            self.elementos_r(actual)
            actual = self.eliminar_primero()
            if actual.tipo in self.salidas_asig or actual.tipo in self.reservadas:
                self.lista_tokens.insert(0, actual)
                return

            if actual.tipo == TipoToken.LLAVE_CERRADURA:
                self.contador = 0
                actual = self.eliminar_primero()
                if arreglos is not None:
                    arreglos.append(actual.valor)
                if actual.tipo == TipoToken.LLAVE_APERTURA:
                    self.lista_tokens.insert(0, actual)
                return
            else:
                self.crear_error(
                    "Se esperaba un }", actual.fila, actual.columna, actual.valor
                )
                if actual.tipo in self.salidas_asig or actual.tipo in self.reservadas:
                    self.lista_tokens.insert(0, actual)
                    return
                self.contador = 0
                self.arreglos(actual)
            if (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.LLAVE_APERTURA
            ):
                self.contador = 0
                self.arreglos()
            elif (
                len(self.lista_tokens) > 0
                and self.lista_tokens[0].tipo == TipoToken.CORCHETE_CERRADURA
            ):
                return
            else:
                if len(self.lista_tokens) > 0:
                    self.contador = 0
                    self.arreglos()

    def elementos_r(self, actual=None, elementos_r: list = None):
        if actual is None:
            actual = self.eliminar_primero()
        if actual.tipo in [TipoToken.STRING, TipoToken.ENTERO, TipoToken.REAL]:
            valor = actual.valor
            # if actual.tipo in [TipoToken.STRING]:
            #     valor = valor.replace('"', "")
            elemento_r = []
            if elementos_r is not None:
                elementos_r.append("ELEMENTO_R")
                elemento_r.append(valor)
                elementos_r.append(elemento_r)
            if self.contador < self.size:
                self.diccionario[self.claves[self.contador]].append(valor)
                self.contador += 1
            actual = self.eliminar_primero()
            if actual is None:
                return
            if (
                actual.tipo in [TipoToken.LLAVE_CERRADURA, TipoToken.LLAVE_APERTURA]
                or actual.tipo in self.salidas_asig
                or actual.tipo in self.reservadas
            ):
                if self.contador < self.size:
                    faltantes = self.size - self.contador
                    self.crear_error(
                        f"Falta {faltantes} valores en el arreglo",
                        actual.fila,
                        actual.columna - 1,
                        actual.valor,
                    )
                    for key in self.claves:
                        if len(self.diccionario[key]) == self.size_list:
                            self.diccionario[key].pop()
                    self.size_list -= 1
                self.lista_tokens.insert(0, actual)
                return
            if actual.tipo == TipoToken.COMA:
                if elementos_r is not None:
                    elementos_r.append(actual.valor)
                    elementos_r.append("ELEMENTOS_R")
                elementos_r1 = []
                self.elementos_r(elementos_r=elementos_r1)
                if elementos_r is not None:
                    elementos_r.append(elementos_r1)
            else:
                self.crear_error(
                    "se esperaba una ,", actual.fila, actual.columna, actual.valor
                )
                self.elementos_r(actual)

        else:
            self.crear_error(
                "Se esperaba un Entero | Decimal | Cadena de texto",
                actual.fila,
                actual.columna,
                actual.valor,
            )
            if actual.tipo in [
                TipoToken.LLAVE_APERTURA,
                TipoToken.LLAVE_CERRADURA,
                TipoToken.R_CLAVES,
                TipoToken.R_REGISTROS,
                TipoToken.COMENTARIO_M,
                TipoToken.COMENTARIO,
            ]:
                if self.contador < self.size:
                    faltantes = self.size - self.contador
                    self.crear_error(
                        f"Falta {faltantes} valores en el arreglo",
                        actual.fila,
                        actual.columna - 1,
                        actual.valor,
                    )
                    for key in self.claves:
                        if len(self.diccionario[key]) == self.size_list:
                            self.diccionario[key].pop()
                    self.size_list -= 1
                self.lista_tokens.insert(0, actual)
                return
            else:
                if len(self.lista_tokens) > 0:
                    if len(self.lista_tokens) > 0 and self.lista_tokens[0].tipo in [
                        TipoToken.COMA
                    ]:
                        actual = self.eliminar_primero()
                        self.elementos_r(actual)
                    else:
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
