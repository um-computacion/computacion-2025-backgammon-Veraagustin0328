from .board import Board

class Game:
    'Juego de backgammon, maneja el tablero y a los jugadores.'

    def __init__(self, players=("WHITE", "BLACK")):
        'Crea el tablero y arranca el juego con dos jugadores.'
        self.__board = Board()
        self.__players = list(players)
        self.__current = self.__players[0]

    def get_board(self):
        'Devuelve el tablero del juego.'
        return self.__board

    def set_board(self, b):
        'Cambia el tablero por otro.'
        self.__board = b

    def get_players(self):
        'Devuelve la lista de jugadores.'
        return self.__players

    def set_players(self, ps):
        'Actualiza los jugadores por los que le paso.'
        self.__players = ps

    def get_current(self):
        'Devuelve quién juega ahora.'
        return self.__current

    def set_current(self, p):
        'Cambia quién está jugando.'
        self.__current = p

    def is_over(self):
        'Por ahora siempre dice que no terminó, después se completará.'
        return False

