
import random

class Dice:
    def __init__(self, rng=None):
        self.__rng__ = rng or random.Random()
        self.__ultima_tirada__ = (0, 0)

    def get_ultima_tirada(self):
        return self.__ultima_tirada__

    def set_rng(self, rng):
        self.__rng__ = rng

    def roll(self):
        a = self.__rng__.randint(1, 6)
        b = self.__rng__.randint(1, 6)
        self.__ultima_tirada__ = (a, b)
        return self.__ultima_tirada__
