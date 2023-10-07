from enum import Enum


class TipoToken(Enum):
    R_CLAVES = 1
    IGUAL = 2
    LLAVE_APERTURA = 3
    LLAVE_CERRADURA = 4
    COMILLAS = 5
    COMILLAS_TRIPLES = 6
    COMA = 7
    CORCHETE_APERTURA = 8
    CORCHETE_CERRADURA = 9
    NUMERAL = 10
    R_REGISTROS = 11
    R_IMPRIMIR = 12
    R_IMPRIMIRLN = 13
    R_CONTEO = 14
    R_PROMEDIO = 15
    R_CONTARSI = 16
    R_DATOS = 17
    R_SUMAR = 18
    R_MAX = 19
    R_MIN = 20
    R_EXPORTAR = 21
    PARENTESIS_APERTURA = 22
    PARENTESIS_CERRADURA = 23
    PUNTO_COMA = 24
    COMENTARIO = 25
    COMENTARIO_M = 26
    COMILLAS_SIMPLES = 27
    COMILLAS_SIMPLES_TR = 28
    STRING = 29
    ENTERO = 30
    REAL = 31
