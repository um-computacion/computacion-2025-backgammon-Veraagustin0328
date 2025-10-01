# backgammon/backgammon/core/dice.py
# backgammon/backgammon/core/dice.py
import random

class Dice:
    def __init__(self, rng=None):
        self.__rng = rng or random.Random()
        self.__ultima_tirada = (0, 0)

    def get_rng(self):
        return self.__rng

    def set_rng(self, rng):
        self.__rng = rng

    def get_ultima_tirada(self):
        return self.__ultima_tirada

    def set_ultima_tirada(self, tirada):
        if (not isinstance(tirada, tuple) or len(tirada) != 2
            or any(not isinstance(x, int) or x < 1 or x > 6 for x in tirada)):
            raise ValueError("Tirada inválida: debe ser (d1, d2) con valores de 1 a 6")
        self.__ultima_tirada = tirada

    def roll(self):
        a = self.__rng.randint(1, 6)
        b = self.__rng.randint(1, 6)
        self.__ultima_tirada = (a, b)
        return self.__ultima_tirada

    def moves_from_roll(self):
        d1, d2 = self.__ultima_tirada
        return [d1, d2, d1, d2] if d1 == d2 else [d1, d2]


