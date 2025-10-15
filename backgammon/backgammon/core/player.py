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
        self._nombre = str(nombre).strip() or "Jugador"
        self._color = color if color in self.ALLOWED_COLORS else "blanco"
        self._fichas = self.FICHAS_INICIALES
        self._puntos = self.PUNTOS_INICIALES


    def get_nombre(self) -> str:
        return self._nombre

    def get_fichas(self) -> int:
        return self._fichas

    def get_puntos(self) -> int:
        return self._puntos

    def set_fichas(self, cantidad: int) -> None:
        """Setea fichas validando que no sea negativo"""
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad de fichas no puede ser negativa")
        self._fichas = cantidad

    def sumar_puntos(self, puntos: int) -> None:
        self._puntos += int(puntos)

    def perder_ficha(self) -> None:
        """Resta una ficha; si no hay, ValueError"""
        if self._fichas <= 0:
            raise ValueError("No hay fichas para perder.")
        self._fichas -= 1


    def reset(self) -> None:
        """Vuelve a estado inicial"""
        self._fichas = self.FICHAS_INICIALES
        self._puntos = self.PUNTOS_INICIALES


    @property
    def name(self) -> str:
        """Alias compatible"""
        return self._nombre

    @name.setter
    def name(self, new_name: str) -> None:
        self._nombre = str(new_name).strip() or "Jugador"

    @property
    def color(self) -> str:
        return self._color

    def rename(self, new_name: str) -> None:
        new_name = str(new_name).strip()
        if not new_name:
            raise ValueError("El nombre no puede ser vacío")
        self._nombre = new_name

    def recolor(self, new_color: str) -> None:
        if new_color not in self.ALLOWED_COLORS:
            raise ValueError(f"Color inválido: {new_color!r}. Permitidos: {sorted(self.ALLOWED_COLORS)}")
        self._color = new_color

    # ---------- Serialización ----------

    def to_dict(self) -> Dict[str, Any]:
        """Serializa estado para asserts/debug o persistencia simple"""
        return {
            "nombre": self._nombre,
            "color": self._color,
            "fichas": self._fichas,
            "puntos": self._puntos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        nombre = str(data.get("nombre") or data.get("name") or "Jugador")
        color = str(data.get("color", "blanco"))
        p = cls(nombre=nombre, color=color if color in cls.ALLOWED_COLORS else "blanco")
        if "fichas" in data:
            p.set_fichas(int(data["fichas"]))
        if "puntos" in data:
            p._puntos = int(data["puntos"])
        return p


    def __repr__(self) -> str:
        return f"Player(nombre={self._nombre!r}, color={self._color!r}, fichas={self._fichas}, puntos={self._puntos})"

    def __str__(self) -> str:
        return f"{self._nombre} ({self._color})"

    def __eq__(self, other: object) -> bool:
        """Igualdad por nombre"""
        if not isinstance(other, Player):
            return False
        return self._nombre == other._nombre

    def __hash__(self) -> int:
        return hash(self._nombre)

