import os


class Imagenes:
    _ruta = os.path.dirname(os.path.abspath(__file__))
    BTN_PLAY = os.path.join(_ruta, "play.png").replace("\\", "\\\\")
    BTN_OPEN = os.path.join(_ruta, "open.png").replace("\\", "\\\\")
    BTN_REPORT = os.path.join(_ruta, "report.png").replace("\\", "\\\\")
