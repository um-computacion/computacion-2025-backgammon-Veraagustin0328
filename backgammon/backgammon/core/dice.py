import random

class Dice:
    'Maneja las tiradas de los dos dados.'

    def __init__(self, rng=None):
        'Arranca los dados con un generador aleatorio (o fijo para testear).'
        self.__rng = rng or random.Random()
        self.__ultima_tirada = (0, 0)

    def roll(self):
        'Tira los dos dados y devuelve el resultado como (d1, d2).'
        a = self.__rng.randint(1, 6)
        b = self.__rng.randint(1, 6)
        self.__ultima_tirada = (a, b)
        return self.__ultima_tirada

    def moves_from_roll(self):
        'Devuelve los movimientos posibles, si es doble se repite 4 veces.'
        d1, d2 = self.__ultima_tirada
        return [d1, d2, d1, d2] if d1 == d2 else [d1, d2]

    def get_rng(self):
        'Devuelve el generador aleatorio que se usa.'
        return self.__rng

    def set_rng(self, rng):
        'Cambia el generador aleatorio.'
        self.__rng = rng

    def get_ultima_tirada(self):
        'Devuelve la última tirada de los dados.'
        return self.__ultima_tirada

    def set_ultima_tirada(self, tirada):
        'Permite setear una tirada a mano (valida que sea correcta).'
        if (not isinstance(tirada, tuple) or len(tirada) != 2
            or any(not isinstance(x, int) or x < 1 or x > 6 for x in tirada)):
            raise ValueError("Tirada inválida: debe ser (d1, d2) con valores de 1 a 6")
        self.__ultima_tirada = tirada

