from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, ClassVar


@dataclass(slots=True)
class Checker:
    """
    Ficha del tablero.

    position:
        - None  -> sin ubicar (o desconocido)
        - -1    -> en la barra (BAR)
        -  0    -> fuera del tablero (OFF / borne off)
        - 1..24 -> punto del tablero
    """
    BAR: ClassVar[int] = -1
    OFF: ClassVar[int] = 0
    MIN_POINT: ClassVar[int] = 1
    MAX_POINT: ClassVar[int] = 24

    color: str = field(default="blanco")
    position: Optional[int] = field(default=None)

   

    def set_position(self, pos: Optional[int]) -> None:
        """Setea la posición con validación de rango """
        if pos is None:
            self.position = None
            return
        if pos in (self.BAR, self.OFF):
            self.position = pos
            return
        if not (self.MIN_POINT <= pos <= self.MAX_POINT):
            raise ValueError(f"Punto inválido: {pos}. Debe ser {self.MIN_POINT}..{self.MAX_POINT}, "
                             f"o BAR({self.BAR})/OFF({self.OFF})/None")
        self.position = pos

    def move_to(self, target_point: int) -> None:
        """Mueve la ficha a un punto específico (valida rango) """
        self.set_position(target_point)

    

    def is_on_bar(self) -> bool:
        return self.position == self.BAR

    def is_borne_off(self) -> bool:
        return self.position == self.OFF

    def is_on_board(self) -> bool:
        return isinstance(self.position, int) and self.MIN_POINT <= self.position <= self.MAX_POINT

   

    def to_dict(self) -> Dict[str, Any]:
        return {"color": self.color, "position": self.position}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Checker":
        c = cls(color=str(data.get("color", "blanco")), position=None)
        c.set_position(data.get("position"))
        return c

 

    def __repr__(self) -> str:
        return f"Checker(color={self.color!r}, position={self.position!r})"

