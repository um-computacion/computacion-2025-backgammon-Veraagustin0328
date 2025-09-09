class Board:
    def __init__(self, puntos=24):
        self.__puntos__ = puntos

    def get_puntos(self):
        return self.__puntos__

    def set_puntos(self, n):
        self.__puntos__ = int(n)
