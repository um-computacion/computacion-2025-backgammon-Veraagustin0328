from __future__ import annotations
from typing import Optional, Dict, Any


class Checker:
    """
    Ficha del tablero.
    
    Aplica principios SOLID:
    - SRP: Solo maneja el estado y posición de una ficha
    - OCP: Puede extenderse mediante herencia
    - LSP: Puede ser sustituida por subclases
    
    position:
        - None  -> sin ubicar (o desconocido)
        - -1    -> en la barra (BAR)
        -  0    -> fuera del tablero (OFF / borne off)
        - 1..24 -> punto del tablero
    """
    BAR: int = -1
    OFF: int = 0
    MIN_POINT: int = 1
    MAX_POINT: int = 24

    def __init__(self, player: Any, color: str = "blanco", position: Optional[int] = None) -> None:
        """
        Inicializa una ficha.
        
        Args:
            player: Jugador dueño de la ficha
            color: Color de la ficha (blanco/negro)
            position: Posición inicial (None por defecto)
        """
        self.__player: Any = player
        self.__color: str = str(color)
        self.__position: Optional[int] = None
        if position is not None:
            self.set_position(position)

    def get_player(self) -> Any:
        """Devuelve el jugador dueño de la ficha"""
        return self.__player

    def get_color(self) -> str:
        """Devuelve el color de la ficha"""
        return self.__color

    def get_position(self) -> Optional[int]:
        """Devuelve la posición actual de la ficha"""
        return self.__position

    def set_position(self, pos: Optional[int]) -> None:
        """
        Setea la posición con validación de rango.
        
        Args:
            pos: Nueva posición (None, BAR, OFF, o 1-24)
            
        Raises:
            ValueError: Si la posición es inválida
        """
        if pos is None:
            self.__position = None
            return
        if pos in (self.BAR, self.OFF):
            self.__position = pos
            return
        if not (self.MIN_POINT <= pos <= self.MAX_POINT):
            raise ValueError(
                f"Punto inválido: {pos}. Debe ser {self.MIN_POINT}..{self.MAX_POINT}, "
                f"o BAR({self.BAR})/OFF({self.OFF})/None"
            )
        self.__position = pos

    def set_color(self, color: str) -> None:
        """Establece el color de la ficha"""
        self.__color = str(color)

    def move_to(self, target_point: int) -> None:
        """
        Mueve la ficha a un punto específico (valida rango).
        
        Args:
            target_point: Punto destino
        """
        self.set_position(target_point)

    def move_to_bar(self) -> None:
        """Mueve la ficha a la barra"""
        self.set_position(self.BAR)

    def move_to_off(self) -> None:
        """Mueve la ficha fuera del tablero (borne off)"""
        self.set_position(self.OFF)

    def is_on_bar(self) -> bool:
        """Verifica si la ficha está en la barra"""
        return self.__position == self.BAR

    def is_borne_off(self) -> bool:
        """Verifica si la ficha está fuera del tablero"""
        return self.__position == self.OFF

    def is_on_board(self) -> bool:
        """Verifica si la ficha está en el tablero (puntos 1-24)"""
        return (
            isinstance(self.__position, int) 
            and self.MIN_POINT <= self.__position <= self.MAX_POINT
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la ficha a diccionario"""
        return {
            "player": self.__player.get_nombre() if hasattr(self.__player, 'get_nombre') else str(self.__player),
            "color": self.__color, 
            "position": self.__position
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], player: Any) -> "Checker":
        """
        Reconstruye una ficha desde un diccionario.
        
        Args:
            data: Diccionario con los datos
            player: Jugador dueño de la ficha
            
        Returns:
            Nueva instancia de Checker
        """
        c = cls(
            player=player,
            color=str(data.get("color", "blanco")), 
            position=None
        )
        pos = data.get("position")
        if pos is not None:
            c.set_position(pos)
        return c

    def __repr__(self) -> str:
        player_name = self.__player.get_nombre() if hasattr(self.__player, 'get_nombre') else str(self.__player)
        return f"Checker(player={player_name!r}, color={self.__color!r}, position={self.__position!r})"

    def __str__(self) -> str:
        player_name = self.__player.get_nombre() if hasattr(self.__player, 'get_nombre') else str(self.__player)
        return f"Ficha {self.__color} de {player_name} en posición {self.__position}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Checker):
            return False
        return self.__player == other.__player and self.__color == other.__color