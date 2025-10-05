import random

class Dice:
    'Maneja las tiradas de dos dados de 6 caras.'

    def __init__(self, rng=None):
        'Usa un RNG inyectable para poder testear.'
        self.__rng = rng or random.Random()
        self.__ultima_tirada = (0, 0)

    def roll(self):
        'Tira los dados y guarda la última tirada.'
        a = self.__rng.randint(1, 6)
        b = self.__rng.randint(1, 6)
        self.__ultima_tirada = (a, b)
        return self.__ultima_tirada

    def moves_from_roll(self):
        'Devuelve [d1, d2] o [d, d, d, d] si es doble.'
        d1, d2 = self.__ultima_tirada
        return [d1, d2, d1, d2] if d1 == d2 else [d1, d2]

    def get_rng(self):
        'Devuelve el generador aleatorio actual.'
        return self.__rng

    def set_rng(self, rng):
        'Cambia el generador aleatorio.'
        self.__rng = rng

    def get_ultima_tirada(self):
        'Devuelve la última tirada guardada.'
        return self.__ultima_tirada

    def set_ultima_tirada(self, tirada):
        'Setea manualmente la última tirada validando el formato.'
        if (not isinstance(tirada, tuple) or len(tirada) != 2
            or any(not isinstance(x, int) or x < 1 or x > 6 for x in tirada)):
            raise ValueError("Tirada inválida: debe ser (d1, d2) con valores de 1 a 6")
        self.__ultima_tirada = tirada
