import os


class Imagenes:
    _ruta = os.path.dirname(os.path.abspath(__file__))
    BTN_PLAY = os.path.join(_ruta, "play.png").replace("\\", "\\\\")
