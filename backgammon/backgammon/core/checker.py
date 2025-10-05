class Checker:
    'Representa las fichas de los jugadores.'

    def __init__(self):
        'Arranca con 15 fichas blancas y 15 negras.'
        self.__count_white = 15
        self.__count_black = 15

    def get_count_white(self):
        'Devuelve cuántas fichas blancas hay.'
        return self.__count_white

    def set_count_white(self, n):
        'Cambia la cantidad de fichas blancas.'
        self.__count_white = n

    def get_count_black(self):
        'Devuelve cuántas fichas negras hay.'
        return self.__count_black

    def set_count_black(self, n):
        'Cambia la cantidad de fichas negras.'
        self.__count_black = n
