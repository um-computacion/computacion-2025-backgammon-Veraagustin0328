from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar


@dataclass(slots=True)
class Player:
    """ Jugador de Backgammon """

    # Colores permitidos “típicos”
    ALLOWED_COLORS: ClassVar[set[str]] = {"blanco", "negro"}

    name: str = field(default="Jugador")
    color: str = field(default="blanco")

    def __post_init__(self) -> None:
        # Validación, si el color no está en el set, hay un ValueError.
        if self.color not in self.ALLOWED_COLORS:
            raise ValueError(
                f"Color inválido: {self.color!r}. Permitidos: {sorted(self.ALLOWED_COLORS)}"
            )
        # Sino existe un nombre, se pone default
        if not str(self.name).strip():
            self.name = "Jugador"

    def rename(self, new_name: str) -> None:
        """ Cambia el nombre del jugador """
        if not str(new_name).strip():
            raise ValueError("El nombre no puede ser vacío.")
        self.name = new_name

    def recolor(self, new_color: str) -> None:
        """Permite cambiar el color si está permitido """
        if new_color not in self.ALLOWED_COLORS:
            raise ValueError(
                f"Color inválido: {new_color!r}. Permitidos: {sorted(self.ALLOWED_COLORS)}"
            )
        self.color = new_color

    def to_dict(self) -> Dict[str, Any]:
        """Serializa a dict (útil si después queremos guardar estado) """
        return {"name": self.name, "color": self.color}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        """Crea un Player desde un dict. Ideal para tests rápidos."""
        return cls(name=str(data.get("name", "Jugador")), color=str(data.get("color", "blanco")))

    def clone(self) -> "Player":
        """Devuelve una copia (para no tocar el original sin querer) """
        return Player(self.name, self.color)

    def __str__(self) -> str:  # print(player)
        return f"{self.name} ({self.color})"

    def __repr__(self) -> str:  # debug más explícito
        return f"Player(name={self.name!r}, color={self.color!r})"

    def __hash__(self) -> int:
        # Lo hacemos hasheable por si queremos usarlo en sets/dicts (p. ej., puntajes)
        return hash((self.name, self.color))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.color == other.color
