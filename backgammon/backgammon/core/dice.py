from __future__ import annotations
import random
from typing import Callable, List

class Dice:
    """ solo maneja tiradas/estado.
     podés inyectar la función randint para tests (o usar from_seed) """

    def __init__(self, randint: Callable[[int, int], int] | None = None) -> None:
        # Si no me pasan nada, uso el randint de random. Si me pasan uno, joya para testear.
        self._randint = randint or random.randint
        # Arranco con algo simple para no dejarlo vacío.
        self.values: List[int] = [1, 1]

    @classmethod
    def from_seed(cls, seed: int) -> "Dice":
        # Con esto puedo testear siempre lo mismo: RNG con semilla fija.
        rng = random.Random(seed)
        return cls(randint=rng.randint)

    def roll(self) -> List[int]:
        # Tiro dos veces, guardo, y devuelvo. Listo, sin vueltas.
        self.values = [self._randint(1, 6), self._randint(1, 6)]
        return self.values

    def is_double(self) -> bool:
        # Si los dos números son iguales, es doble. Fin.
        return self.values[0] == self.values[1]

    def __repr__(self) -> str:
        return f"Dice({self.values[0]}, {self.values[1]})"
