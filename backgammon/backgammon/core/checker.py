class Checker:
    def __init__(self, color):
        self.__color__ = color

    def get_color(self):
        return self.__color__

    def set_color(self, c):
        self.__color__ = c
