<h1 align="center">Manual de Usuario</h1>

<div align="center">
🙍‍♂️ Joab Israel Ajsivinac Ajsivinac 🆔 202200135
</div>
<div align="center">
📕 Lenguajes Formales y de Programación
</div>
<div align="center"> 🏛 Universidad San Carlos de Guatemala</div>
<div align="center"> 📆 Segundo Semestre 2023</div>

<!-- Tabla de Contenidos -->
## 📋 Tabla de Contenidos

<!-- - [📋 Tabla de Contenidos](#-tabla-de-contenidos) -->
- [📋 Tabla de Contenidos](#-tabla-de-contenidos)
- [📖 Descripción](#-descripción)
- [⚒ Requerimientos](#-requerimientos)
- [🗂 Recursos](#-recursos)
- [📟 Instalación](#-instalación)
- [⚡ Inicio Rápido](#-inicio-rápido)
- [💻 Interfaz de Usuario y Funcionalidades](#-interfaz-de-usuario-y-funcionalidades)
  - [Parte superior](#parte-superior)
  - [Tipos de errores](#tipos-de-errores)
  - [Parte inferior](#parte-inferior)


<!-- Requerimientos -->
## 📖 Descripción
El programa es un analizador léxico y sintáctico con interfaz gráfica de archivos con extesnión bizdata, el cual contiene una sintaxis de codigo especifica, la cual tiene la capacidad de imprimir datos mediante una consola dentro del programa dependiendo de la instrucción utilizada en el cuadro de texto donde se debe agregar el codigo.

El programa cuenta con 3 opciones principales, que son: abrir, ejecutar y reportes, los reportes que genera son 4, 3 que se derivan del analisis del codigo y 1 reporte que esta completamente basado en lo que el ususario agregue como un registro.

## ⚒ Requerimientos
<ul>
  <li>Windows 8 o Superior</li>
  <li>macOS Catalina o Superior</li>
  <li>Linux: Ubuntu, Debian, CentOS, Fedora, etc.</li>
  <li>Python 3.10.8 o Superior</li>
  <li>Tkinter 8.6 o superior</li>
  <li>Graphviz 0.20 o superior</li>
  <li>Pillow 10.0.1 o Superior</li>
  <li>sv_ttk</li>
  <br>
  <li>Fuentes</li>
  <ul>
  <li>Montserrat </li>
  <li>Cascadia Code</li></ul>
  
</ul>

## 🗂 Recursos
<ul>
  <li><a href="https://www.python.org/downloads/">Python 3.10.8 o Superior</a></li>
  <li>pip install tkinter</li>
  <li><a href="https://pypi.org/project/graphviz/">Graphviz 0.20 o superior</a></li>
  <li><a href="https://pypi.org/project/Pillow/">Pillow 10.0.1 o Superior</a></li>
  <li>pip install sv-ttk</li>
  <br>
  <li>Fuentes</li>
  <ul>
  <li><a href="https://fonts.google.com/specimen/Montserrat">Montserrat </a></li>
  <li><a href="https://github.com/microsoft/cascadia-code">Cascadia Code</a></li>
  </ul>
  
</ul>

## 📟 Instalación
Descargue el código o bien clone el repositorio en una carpeta.

Si se opta por la clonación se hace con la siguiente linea de código en terminal (Antes de ejecutar el codigo asegurese de estar en la carpeta donde lo quiere descargar)

```bash
git clone https://github.com/J-Ajsivinac/LFP_S2_2023_Proyecto2_202200135
```

## ⚡ Inicio Rápido
Una vez con la carpeta del proyecto y teniendo los recursos, dirijase a donde está al archivo `main.py` y ejecutelo de la siguiente forma

```bash
python main.py
```

Luego se le abrirá la ventana principal

## 💻 Interfaz de Usuario y Funcionalidades
Al ejecutar la aplicación se desplegará la siguiente ventana, la cual es la principal:
![Captura 1](https://i.imgur.com/7IUQk3y.png)

La ventana principal esta dividida en dos partes principales:

### Parte superior
En la parte superior se tienen 2 botones

El primer botón es el que se encarga de abrir archivos con extensión bizdata
donde se Despliega una ventana donde se puede elegir un archivo que tenga el formato bizdata
![Captura 3](https://i.imgur.com/8j2IFtK.png)

Con el botón de reportes podra elegir entre 3 reportes, a generar, los reportes de errores y tokens se generarán en formato Html, y la gráfica de derivación se generá en formato svg

![Captura 4](https://i.imgur.com/2hrobz1.png)

Los reportes html tienen la siguiente apariencia:

![Captura 5](https://i.imgur.com/9fxS9K4.png)

Dependiendo del tipo de reporte la información cambiará.

El reporte del arbol se verá de la siguiente forma:

![Captura 6](https://i.imgur.com/felVhwb.png)

### Tipos de errores
Los errores mostrados en los reportes se dividen en 2, errores léxicos y sintácticos, Los errores léxicos son caracteres que no esperaba el sistema, por lo que se muestra el caracter leido la fila y la columna donde se encuentra el caracter

Para los errores sintácticos, se puede tener los siguientes errores:


| Error                                                                   | Descripción                                                                                |
| :---------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| Se esperaba una palabra reservada \| clave \| comentario\|  registro \| | Significa que se esperaba una de las siguientes palabras:                                  |
| Se esperaba un Entero \| Decimal\|  Cadena de texto                     | Significa que esperaba un numero entero, un numero con decimal o una cadena entre comillas |
| Se esperaba un ;                                                        | significa que falta un punto y coma                                                        |
| Se esperaba un =                                                        | significa que falta un signo igual                                                         |
| Se esperaba un ]                                                        | significa que falta un corchete de cerradura                                               |
| Se esperaba un [                                                        | Lo que significa que falta un corchete de apertura                                         |
| La clave no puede ser vacia                                             | Una clave no puede ser un valor vació                                                      |
| Se esperaba una ,                                                       | Lo que significa que falta una coma                                                        |
| Se esperaba una cadena de texto                                         | Significa que se esperaba una cadena entre comillas dobles                                 |
| Se esperaba un )                                                        | Lo que significa que falta un paréntesis de cerradura                                      |
| Se esperaba un (                                                        | Lo que significa que falta un paréntesis de apertura                                       |
| Se esperaba un }                                                        | Significa que falta una llave de cerradura                                                 |
| Se esperaba un {                                                        | Significa que falta una llave de apertura                                                  |
| Falta n valores en el arreglo                                           | Significa que un registro no esta completo, lo que hace que no se registre                 |



### Parte inferior
La parte inferior esta dividida en 2 columnas, de la siguiente manera:

La primera columna donde se puede visualiza el nombre del archivo actual junto con su extención (Al inicio el nombre es Nuevo Documento.json) a si como el botón para ejecutar y el lugar donde se debe agregar el texto a analizar.

La segunda columna es donde se podrá visualizar las acciones escritas anteriormente.

![Captura 7](https://i.imgur.com/7IUQk3y.png)

El codigo de entrada puede reconocer las siguientes instrucciones y definir lo siguiente:

>Comentario de una linea, se define de la siguiente manera
>```java
># Comentario
>```

>Comentario de una linea
>```java
>'''
>    COMENTARIO MULTILINEA
>'''
>```

>Definición de claves
>```java
> claves = ["clave_1","clave_2","clave_n"]
>```

>Definición de registros
>```java
> registros = [
>   {1, "Barbacoa", 10.50, 20.00, 6}
>]
>```


> **Definición de instrucciones**
>
> Las instrucciones disponibles son:
> * imprimir: Imprime por consola el valor dado por la cadena.
>
> ```java
> imprimir(cadena);
>```
>
> * imprimirln: imprime por consola el valor dado por la cadena, finalizando con un salto de linea.
> ```java
> imprimirln(cadena);
>```
> * datos: Imprime por consola los registros leídos.
> ```java
> datos();
>```
> * conteo: Imprime por consola la cantidad de registros en el arreglo de registros.
> ```java
> conteo();
>```
> * promedio: Imprime por consola el promedio del campo dado.
> ```java
> promedio();
>```
> * contarsi:Imprime por consola la cantidad de registros en la que el campo dado sea igual al valor dado.
> ```java
> contarsi(“campo”, valor);
>```
> * sumar:Imprime en consola la suma todos los valores del campo dado.
> ```java
> sumar(“campo”);
>```
> * max: Encuentra el valor máximo del campo dado
> ```java
> max(“campo”);
>```
> * min: Encuentra el valor mínimo del campo dado
> ```java
> min(“campo”);
>```
> exportar Reporte:Genera un archivo html con una tabla en donde se encuentren los registros leídos y con el título como parámetro.
> ```java
> exportarReporte(“titulo”);
>```
