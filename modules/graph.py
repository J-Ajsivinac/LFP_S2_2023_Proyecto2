import graphviz


class Graph:
    def __init__(self, datos):
        self.datos = datos
        self.dot = graphviz.Digraph(filename="AST", format="png", strict=True)
        self.dot.attr("node", shape="box", style="filled", color="lightgrey")
        self.i = 0
        self.contador_n = 0
        self.stack = []
        # self.raiz = None
        print(self.datos)
        self.graficar_AST(self.datos)
        self.dot.format = "svg"
        self.dot.render("resultados/test", view=True)

    def graficar_AST(self, datos: list, raiz=None, nivel=0):
        # if nivel > 0 and len()
        cabeza = raiz
        for i, elemento in enumerate(datos):
            if (
                elemento == "inicio"
                or elemento == "otro comando"
                or elemento == "comando"
            ):
                # self.stack.append(nivel)
                self.dot.node(f"{nivel}_{self.contador_n}", str(elemento))
                cabeza = f"{nivel}_{self.contador_n}"
                if raiz is not None and nivel > 0:
                    self.dot.edge(raiz, f"{nivel}_{self.contador_n}")
                # raiz = f"{nivel}_{self.contador_n}"
                nivel += 1
                self.contador_n += 1
            elif isinstance(elemento, list):
                # print("  " * nivel + "[")
                self.stack.append(nivel)
                nivel += 1
                # self.raiz = f"{nivel}_{no_nodo}"
                self.graficar_AST(elemento, cabeza, nivel)
                nivel = self.stack.pop()
                # print("  " * nivel + "]")
            else:
                # print("  " * nivel + str(elemento))
                self.dot.node(f"{nivel}_{self.contador_n}", str(elemento))
                if raiz and nivel > 0:
                    self.dot.edge(raiz, f"{nivel}_{self.contador_n}")
                if (i + 1) < len(datos) and isinstance(datos[i + 1], list):
                    cabeza = f"{nivel}_{self.contador_n}"
                self.contador_n += 1
                # print(nivel, str(elemento))

    def recursivo(self, datos: list):
        for i, dato in enumerate(datos):
            if isinstance(datos, list):
                self.recursivo(datos[i:])
                return datos[i:]
            self.dot.node(str(self.i), str(dato))
            self.i += 1
