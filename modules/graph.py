import graphviz


class Graph:
    def __init__(self, datos):
        self.datos = datos
        self.dot = graphviz.Digraph(filename="AST", format="png", strict=True)
        self.dot.attr("node", shape="box", style="filled", color="lightgrey")
        self.i = 0
        self.contador_n = 0
        self.graficar_AST(self.datos)

    def graficar_AST(self, datos: list, nivel=0):
        for elemento in datos:
            if isinstance(elemento, list):
                print(" ")
                self.graficar_AST(elemento, nivel + 1)
            elif elemento == "otro comando":
                print(" ")
                nivel += 1
                print("  " * nivel + str(elemento), end=" ")
            else:
                print("  " * nivel + str(elemento), end=" ")
                # print(nivel, str(elemento))

    def recursivo(self, datos: list):
        for i, dato in enumerate(datos):
            if isinstance(datos, list):
                self.recursivo(datos[i:])
                return datos[i:]
            else:
                self.dot.node(str(self.i), str(dato))
                self.i += 1
