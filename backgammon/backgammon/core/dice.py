# backgammon/backgammon/core/dice.py
import random

class Dice:
    """Lógica de tiradas de dos dados de 6 caras."""
    def __init__(self, rng=None):
        self.__rng__ = rng or random.Random()
        self.__ultima_tirada__ = (0, 0)

    def get_rng(self):
        return self.__rng__

    def set_rng(self, rng):
        self.__rng__ = rng

    def get_ultima_tirada(self):
        return self.__ultima_tirada__

    def set_ultima_tirada(self, tirada):
        if (not isinstance(tirada, tuple) or len(tirada) != 2
            or any(not isinstance(x, int) or x < 1 or x > 6 for x in tirada)):
            raise ValueError("Tirada inválida: debe ser (d1, d2) con valores de 1 a 6")
        self.__ultima_tirada__ = tirada

    def roll(self):
        a = self.__rng__.randint(1, 6)
        b = self.__rng__.randint(1, 6)
        self.__ultima_tirada__ = (a, b)
        return self.__ultima_tirada__


