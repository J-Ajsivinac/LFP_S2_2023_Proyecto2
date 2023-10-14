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
