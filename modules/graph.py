import graphviz


class Graph:
    def __init__(self, datos):
        self.datos = datos
        self.dot = graphviz.Digraph(filename="AST", format="png", strict=True)
        self.dot.attr("node", shape="box", style="filled", color="lightgrey")
        self.i = 0
        self.contador_n = 0
        self.stack = []
        print(self.datos)
        self.graficar_AST(self.datos)

    def graficar_AST(self, datos: list, raiz=None, nivel=0):
        cabeza = raiz
        for i, elemento in enumerate(datos):
            if (
                elemento == "inicio"
                or elemento == "otro comando"
                or elemento == "comando"
            ):
                self.stack.append(nivel)
                self.dot.node(f"{nivel}_{self.contador_n}", str(elemento))
                cabeza = f"{nivel}_{self.contador_n}"
                if raiz is not None and nivel > 0:
                    self.dot.edge(raiz, f"{nivel}_{self.contador_n}")
                nivel += 1
                self.contador_n += 1
            elif isinstance(elemento, list):
                self.stack.append(nivel)
                nivel += 1
                self.graficar_AST(elemento, cabeza, nivel)
                nivel = self.stack.pop()
            else:
                self.dot.node(f"{nivel}_{self.contador_n}", str(elemento))
                if raiz and nivel > 0:
                    self.dot.edge(raiz, f"{nivel}_{self.contador_n}")
                if (i + 1) < len(datos) and isinstance(datos[i + 1], list):
                    cabeza = f"{nivel}_{self.contador_n}"
                self.contador_n += 1

    def generar(self):
        self.dot.format = "svg"
        self.dot.render("resultados/test", view=True)
