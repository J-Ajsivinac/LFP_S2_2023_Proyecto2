class Reporte:
    def crear_reporte_tokens(self, tokens: list, ruta):
        html = """
        <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="report/css/style.css">
                <title>Tokens</title>
            </head>

            <body>
                <main>
                    <div class="contenedor">
                        <div class="titulo">
                            <h2>Reporte de Tokens</h2>
                        </div>
                    <div class="contenido">
                        <table>
                            <tr>
                                <th>Lexema</th>
                                <th>Fila</th>
                                <th>Columna</th>
                                <th>Tipo</th>
                            </tr>
        """
        for token in tokens:
            html += f"""
                <tr>
                    <td>{token.valor}</td>
                    <td>{token.fila}</td>
                    <td>{token.columna}</td>
                    <td>{token.tipo}</td>
                </tr>
            """
        html += """
                        </table>
                    </div>
                </div>
            </main>
        </body>
        </html>
        """
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)

    def crear_reporte_errores(self, e_lexicos: list, e_sintacticos: list, ruta):
        html = """
        <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="report/css/style.css">
                <title>Tokens</title>
            </head>

            <body>
                <main>
                    <div class="contenedor">
                        <div class="titulo">
                            <h2>Errores Léxicos</h2>
                        </div>
                    <div class="contenido-error">
                        <table>
                            <tr>
                                <th>Descripción</th>
                                <th>Fila</th>
                                <th>Columna</th>
                            </tr>
        """
        for error in e_lexicos:
            html += f"""
                <tr>
                    <td>{error.valor}</td>
                    <td>{error.fila}</td>
                    <td>{error.columna}</td>
                </tr>
            """
        html += """
                        </table>
                    </div>
                    <div class="titulo">
                        <h2>Errores Sintácticos</h2>
                    </div>
                    <div class="contenido-error">
                        <table>
                            <tr>
                                <th>Descripción</th>
                                <th>Fila</th>
                                <th>Columna</th>
                            </tr>
        """
        for error in e_sintacticos:
            html += f"""
                <tr>
                    <td>{error.valor}</td>
                    <td>{error.fila}</td>
                    <td>{error.columna}</td>
                </tr>
            """
        html += """
                        </table>
                    </div>
                </div>
                </div>
            </main>
        </body>
        </html>
        """
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)

    def crear_reporte_datos(self, datos: dict, titulo, ruta):
        titulo = titulo.replace('"', "")
        keys = list(datos.keys())
        html = f"""
        <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="report/css/style.css">
                <title>Tokens</title>
            </head>

            <body>
                <main>
                    <div class="contenedor">
                        <div class="titulo">
                            <h2>{titulo}s</h2>
                        </div>
                    <div class="contenido-reporte">
                        <table>
                            <tr>
            """
        ancho = 100 / len(keys)
        for key in keys:
            html += f"""
            <th style="width: {ancho}%;">{key.replace('"',"")}</th>              
            """
        html += "</tr>"
        # encabezados = "\t".join(datos.keys()) + "\n"
        size = len(next(iter(datos.values())))
        for i in range(size):
            html += "<tr>"
            for encabezado in datos.keys():
                html += f"""
                    <td>{datos[encabezado][i]}</td>
                """
            html += "</tr>"

        html += """
                        </table>
                    </div>
                </div>
            </main>
        </body>
        </html>
        """

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
