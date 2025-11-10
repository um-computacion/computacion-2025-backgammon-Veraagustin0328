from __future__ import annotations
import random
from typing import Tuple, List, Optional


class Dice:
    """
    Clase que representa dos dados de seis caras
    """

    def __init__(self, rng: Optional[random.Random] = None) -> None:
        # Atributos internos con doble underscore (encapsulación)
        self.__rng__ = rng or random.Random()
        self.__ultima_tirada__: Tuple[int, int] = (0, 0)

    @classmethod
    def from_seed(cls, seed: int) -> "Dice":
        """Crea un dado con una semilla fija para obtener tiradas reproducibles"""
        rng = random.Random(seed)
        return cls(rng)

    def roll(self) -> Tuple[int, int]:
        """Tira los dos dados, guarda la tirada y devuelve una tupla (d1, d2)"""
        d1 = self.__rng__.randint(1, 6)
        d2 = self.__rng__.randint(1, 6)
        self.__ultima_tirada__ = (d1, d2)
        return (d1, d2)

    def is_double(self) -> bool:
        """Devuelve True si ambos dados son iguales"""
        d1, d2 = self.__ultima_tirada__
        return d1 == d2

    def moves_from_roll(self) -> List[int]:
        """
        Devuelve una lista con los movimientos posibles según la tirada
        Si es doble, repite cuatro veces; si no, solo dos valores
        """
        d1, d2 = self.__ultima_tirada__
        return [d1, d2, d1, d2] if d1 == d2 else [d1, d2]

    def get_rng(self) -> random.Random:
        """Devuelve el generador aleatorio actual"""
        return self.__rng__

    def set_rng(self, rng: random.Random) -> None:
        """Permite cambiar el generador aleatorio"""
        self.__rng__ = rng

    def get_ultima_tirada(self) -> Tuple[int, int]:
        """Devuelve la última tirada como tupla (d1, d2)"""
        return self.__ultima_tirada__

    def set_ultima_tirada(self, tirada) -> None:
        """
        Acepta (d1, d2) o [d1, d2] y valida que sean enteros entre 1 y 6
        """
        if isinstance(tirada, list):
            tirada = tuple(tirada)
        if (
            not isinstance(tirada, tuple)
            or len(tirada) != 2
            or any(not isinstance(x, int) or x < 1 or x > 6 for x in tirada)
        ):
            raise ValueError("Tirada inválida: debe ser (d1, d2) con valores entre 1 y 6")
        self.__ultima_tirada__ = tirada

    def __repr__(self) -> str:
        d1, d2 = self.__ultima_tirada__
        return f"Dice({d1}, {d2})"

    def __str__(self) -> str:
        d1, d2 = self.__ultima_tirada__
        return f"Tirada actual: {d1} y {d2}"
