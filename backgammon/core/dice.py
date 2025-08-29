import random

class Dice:
    
    
    """ Clase para poder crear dados de 6 caras """

    
    def __init__(self, seed: int | None = None) -> None:
        self.__seed__ = seed
        self.__rng__ = random.Random(seed)

    def roll(self) -> list[int]:
        """ Tiramos los dados.
        - Si son diferentes: devuelve [d1, d2]
        - Si son dobles: devuelve [d, d, d, d] """
       
        d1 = self.__rng__.randint(1, 6)
        d2 = self.__rng__.randint(1, 6)
        if d1 == d2:
            return [d1, d1, d1, d1]
        return [d1, d2]
    
    
    
   