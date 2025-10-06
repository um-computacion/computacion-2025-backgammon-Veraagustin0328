from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


class BaseBoard(ABC):
    """Base para tableros de Backgammon (OCP)."""

    @abstractmethod
    def initialize_points(self) -> List[list]:
        """Devuelve la estructura inicial de 24 puntos."""
        raise NotImplementedError


class Board(BaseBoard):
    """Tablero estándar: 24 puntos + bar + off."""

    def __init__(self) -> None:
        # Acá no me caliento con cómo se inicializa, delego al método.
        self.points: List[list] = self.initialize_points()
        self.bar: Dict[str, int] = {"blanco": 0, "negro": 0}
        self.off: Dict[str, int] = {"blanco": 0, "negro": 0}

    def initialize_points(self) -> List[list]:
        # Por ahora tablero vacío. Si mañana querés arrancar con fichas puestas, lo cambiás acá
        # o armás otra clase que herede y listo.
        return [[] for _ in range(24)]

    def point_count(self, index: int) -> int:
        # Dame cuántas fichas hay en el punto 1..24. Simple y sin drama.
        i = index - 1
        if not (0 <= i < 24):
            raise IndexError("El punto debe estar entre 1 y 24.")
        return len(self.points[i])

    def __repr__(self) -> str:
        return f"Board(points={len(self.points)}, bar={self.bar}, off={self.off})"


