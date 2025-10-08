class Player:
    'Representa un jugador del backgammon.'

    def __init__(self, name, color):
        'Crea un jugador con nombre y color (WHITE o BLACK).'
        self.__name = name
        self.__color = color

    def get_name(self):
        'Devuelve el nombre del jugador.'
        return self.__name

    def set_name(self, name):
        'Cambia el nombre del jugador.'
        self.__name = name

    def get_color(self):
        'Devuelve el color del jugador.'
        return self.__color

    def set_color(self, color):
        'Cambia el color del jugador.'
        self.__color = color

