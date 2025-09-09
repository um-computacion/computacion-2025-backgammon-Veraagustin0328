# backgammon/backgammon/core/game.py
from .board import Board

class Game:
    
    def __init__(self, players=("WHITE", "BLACK")):
        self.__board = Board()
        self.__players = list(players)
        self.__current = self.__players[0]

    def get_board(self):
        return self.__board

    def set_board(self, b):
        self.__board = b

    def get_players(self):
        return self.__players

    def set_players(self, ps):
        self.__players = ps

    def get_current(self):
        return self.__current

    def set_current(self, p):
        self.__current = p

    def is_over(self):
        return False

