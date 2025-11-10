from __future__ import annotations
from typing import Dict, Any


class Player:
    """
    Jugador de Backgammon
    """

    FICHAS_INICIALES = 15
    PUNTOS_INICIALES = 0
    ALLOWED_COLORS = {"blanco", "negro"}

    def __init__(self, nombre: str, color: str = "blanco") -> None:
        self.__nombre = str(nombre).strip() or "Jugador"
        self.__color = color if color in self.ALLOWED_COLORS else "blanco"
        self.__fichas = self.FICHAS_INICIALES
        self.__puntos = self.PUNTOS_INICIALES

    def get_nombre(self) -> str:
        return self.__nombre

    def get_color(self) -> str:
        return self.__color

    def get_fichas(self) -> int:
        return self.__fichas

    def get_puntos(self) -> int:
        return self.__puntos

    def set_fichas(self, cantidad: int) -> None:
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad de fichas no puede ser negativa")
        self.__fichas = cantidad

    def set_color(self, color: str) -> None:
        if color not in self.ALLOWED_COLORS:
            raise ValueError(f"Color inválido: {color}. Permitidos: {sorted(self.ALLOWED_COLORS)}")
        self.__color = color

    def set_nombre(self, nombre: str) -> None:
        if not str(nombre).strip():
            raise ValueError("El nombre no puede ser vacío")
        self.__nombre = nombre

    def sumar_puntos(self, puntos: int) -> None:
        self.__puntos += int(puntos)

    def perder_ficha(self) -> None:
        if self.__fichas <= 0:
            raise ValueError("No hay fichas para perder")
        self.__fichas -= 1

    def reset(self) -> None:
        self.__fichas = self.FICHAS_INICIALES
        self.__puntos = self.PUNTOS_INICIALES

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nombre": self.__nombre,
            "color": self.__color,
            "fichas": self.__fichas,
            "puntos": self.__puntos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        nombre = str(data.get("nombre", "Jugador"))
        color = str(data.get("color", "blanco"))
        p = cls(nombre=nombre, color=color if color in cls.ALLOWED_COLORS else "blanco")
        if "fichas" in data:
            p.set_fichas(int(data["fichas"]))
        if "puntos" in data:
            p.__puntos = int(data["puntos"])
        return p

    def __repr__(self) -> str:
        return (
            f"Player(nombre={self.__nombre!r}, color={self.__color!r}, "
            f"fichas={self.__fichas}, puntos={self.__puntos})"
        )

    def __str__(self) -> str:
        return f"{self.__nombre} ({self.__color})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Player) and self.__nombre == other.__nombre

    def __hash__(self) -> int:
        return hash(self.__nombre)
    