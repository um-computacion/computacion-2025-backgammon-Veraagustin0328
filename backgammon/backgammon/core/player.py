class Player:
    def __init__(self, nombre: str):
        self.__nombre__ = str(nombre)
        self.__fichas__ = 15
        self.__puntos__ = 0

    
    def get_nombre(self):
        return self.__nombre__

    def set_nombre(self, n: str):
        self.__nombre__ = str(n)

    def get_fichas(self):
        return self.__fichas__

    def set_fichas(self, cantidad: int):
        self.__fichas__ = int(cantidad)

    def get_puntos(self):
        return self.__puntos__

    def set_puntos(self, n: int):
        self.__puntos__ = int(n)

    
    def sumar_puntos(self, n: int):
        self.__puntos__ += int(n)

    def perder_ficha(self):
        if self.__fichas__ > 0:
            self.__fichas__ -= 1
        else:
            raise ValueError("El jugador no tiene fichas para perder.")
