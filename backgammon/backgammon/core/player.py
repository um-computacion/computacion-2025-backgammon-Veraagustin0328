from __future__ import annotations
from typing import Dict, Any


class Player:
    """
    Representa a un jugador de Backgammon

    """

    FICHAS_INICIALES = 15
    PUNTOS_INICIALES = 0

    def __init__(self, nombre: str) -> None:
        self._nombre = str(nombre)
        self._fichas = self.FICHAS_INICIALES
        self._puntos = self.PUNTOS_INICIALES


    def get_nombre(self) -> str:
        return self._nombre

    def get_fichas(self) -> int:
        return self._fichas

    def get_puntos(self) -> int:
        return self._puntos


    def set_fichas(self, cantidad: int) -> None:
        """
        Setea fichas de forma directa, validando que no sea negativo
        
        """
        if int(cantidad) < 0:
            raise ValueError("La cantidad de fichas no puede ser negativa ")
        self._fichas = int(cantidad)

    def sumar_puntos(self, puntos: int) -> None:
        """Suma puntos (permite valores negativos si alguna regla lo requiere) """
        self._puntos += int(puntos)

    def perder_ficha(self) -> None:
        """
        Resta una ficha. Si no hay, lanza ValueError 
        """
        if self._fichas <= 0:
            raise ValueError("No hay fichas para perder ")
        self._fichas -= 1


    def reset(self) -> None:
        """Vuelve a estado inicial: fichas=15, puntos=0 """
        self._fichas = self.FICHAS_INICIALES
        self._puntos = self.PUNTOS_INICIALES

    def to_dict(self) -> Dict[str, Any]:
        """ Serialización simple (útil para asserts y debugging) """
        return {
            "nombre": self._nombre,
            "fichas": self._fichas,
            "puntos": self._puntos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        
        nombre = str(data.get("nombre", "Jugador"))
        p = cls(nombre)
        # Aplicamos si vienen; validamos fichas con el setter
        if "fichas" in data:
            p.set_fichas(int(data["fichas"]))
        if "puntos" in data:
            p._puntos = int(data["puntos"])
        return p


    def __repr__(self) -> str:
        return f"Player(nombre={self._nombre!r}, fichas={self._fichas}, puntos={self._puntos})"

    def __str__(self) -> str:
        return f"{self._nombre} (fichas={self._fichas}, puntos={self._puntos})"

    def __eq__(self, other: object) -> bool:
        
        if not isinstance(other, Player):
            return False
        return self._nombre == other._nombre

    def __hash__(self) -> int:
        return hash(self._nombre)
