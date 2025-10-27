from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseBoard(ABC):
    """
    Interfaz base para tableros de Backgammon (OCP).
    
    Permite extender con nuevos tipos de tableros sin modificar el código existente.
    """

    @abstractmethod
    def initialize_points(self) -> List[list]:
        """Devuelve la estructura inicial de puntos del tablero."""
        raise NotImplementedError

    @abstractmethod
    def get_points(self) -> List[list]:
        """Devuelve los puntos del tablero."""
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """Reinicia el tablero a su estado inicial."""
        raise NotImplementedError


class BarManager:
    """
    SRP: Gestiona únicamente las operaciones de la barra.
    """

    def __init__(self) -> None:
        self.__bar: Dict[str, int] = {"blanco": 0, "negro": 0}

    def add_to_bar(self, color: str) -> None:
        """Agrega una ficha del color dado a la barra."""
        if color not in ["blanco", "negro"]:
            raise ValueError(f"Color inválido: {color}")
        self.__bar[color] += 1

    def remove_from_bar(self, color: str) -> bool:
        """
        Quita una ficha del color dado de la barra.
        
        Returns:
            True si se removió exitosamente, False si no había fichas.
        """
        if color not in ["blanco", "negro"]:
            raise ValueError(f"Color inválido: {color}")
        
        if self.__bar[color] > 0:
            self.__bar[color] -= 1
            return True
        return False

    def get_count(self, color: str) -> int:
        """Retorna la cantidad de fichas del color en la barra."""
        if color not in ["blanco", "negro"]:
            raise ValueError(f"Color inválido: {color}")
        return self.__bar[color]

    def has_checkers(self, color: str) -> bool:
        """Verifica si hay fichas del color en la barra."""
        return self.get_count(color) > 0

    def get_state(self) -> Dict[str, int]:
        """Retorna una copia del estado de la barra."""
        return self.__bar.copy()

    def reset(self) -> None:
        """Reinicia la barra a estado vacío."""
        self.__bar = {"blanco": 0, "negro": 0}


class BearOffManager:
    """
    SRP: Gestiona únicamente las operaciones de bear off.
    """

    def __init__(self) -> None:
        self.__off: Dict[str, int] = {"blanco": 0, "negro": 0}

    def bear_off(self, color: str) -> None:
        """Saca una ficha del color dado del tablero."""
        if color not in ["blanco", "negro"]:
            raise ValueError(f"Color inválido: {color}")
        self.__off[color] += 1

    def get_count(self, color: str) -> int:
        """Retorna la cantidad de fichas del color fuera del juego."""
        if color not in ["blanco", "negro"]:
            raise ValueError(f"Color inválido: {color}")
        return self.__off[color]

    def has_won(self, color: str) -> bool:
        """Verifica si el jugador del color ganó (15 fichas fuera)."""
        return self.get_count(color) == 15

    def get_state(self) -> Dict[str, int]:
        """Retorna una copia del estado de bear off."""
        return self.__off.copy()

    def reset(self) -> None:
        """Reinicia el bear off a estado vacío."""
        self.__off = {"blanco": 0, "negro": 0}




class Board(BaseBoard):
    """
    Tablero estándar de Backgammon con 24 puntos + barra + bear off.
    """

    def __init__(self) -> None:
        """Inicializa el tablero con sus componentes."""
        self.__points: List[list] = self.initialize_points()
        self.__bar_manager = BarManager()
        self.__bear_off_manager = BearOffManager()


    def initialize_points(self) -> List[list]:
        """
        Inicializa 24 puntos vacíos.
        
        Para tablero con posición inicial, heredar y override este método.
        """
        return [[] for _ in range(24)]

    def get_points(self) -> List[list]:
        """Retorna una copia de los puntos del tablero."""
        return [point.copy() for point in self.__points]

    def reset(self) -> None:
        """Reinicia el tablero a su estado inicial."""
        self.__points = self.initialize_points()
        self.__bar_manager.reset()
        self.__bear_off_manager.reset()


    def point_count(self, position: int) -> int:
        """
        Retorna la cantidad de fichas en una posición (1-24).
        
        Args:
            position: Posición del tablero (1-24)
            
        Returns:
            Cantidad de fichas en esa posición
            
        Raises:
            ValueError: Si la posición está fuera del rango válido
        """
        self._validate_position(position)
        return len(self.__points[position - 1])

    def colocar_ficha(self, player: Any, position: int) -> None:
        """
        Coloca una ficha del jugador en la posición indicada.
        
        Args:
            player: Objeto jugador/ficha a colocar
            position: Posición donde colocar (1-24)
            
        Raises:
            ValueError: Si la posición es inválida
        """
        self._validate_position(position)
        self.__points[position - 1].append(player)

    def quitar_ficha(self, position: int) -> Optional[Any]:
        """
        Quita la última ficha de la posición indicada.
        
        Args:
            position: Posición de donde quitar (1-24)
            
        Returns:
            La ficha removida, o None si no había fichas
            
        Raises:
            ValueError: Si la posición es inválida
        """
        self._validate_position(position)
        idx = position - 1
        
        if len(self.__points[idx]) == 0:
            return None
        
        return self.__points[idx].pop()

    def mover_ficha(self, from_pos: int, to_pos: int) -> Optional[Any]:
        """
        Mueve una ficha de una posición a otra.
        
        Args:
            from_pos: Posición origen (1-24)
            to_pos: Posición destino (1-24)
            
        Returns:
            Ficha capturada si hubo captura, None en caso contrario
            
        Raises:
            ValueError: Si las posiciones son inválidas o no hay fichas en origen
        """
        self._validate_position(from_pos)
        self._validate_position(to_pos)
        
        idx_from = from_pos - 1
        idx_to = to_pos - 1
        
        if len(self.__points[idx_from]) == 0:
            raise ValueError(f"No hay fichas en la posición {from_pos}")
        
        # Quitar ficha de origen
        ficha = self.__points[idx_from].pop()
        
        # Verificar si hay captura (ficha solitaria del oponente)
        captured = None
        if len(self.__points[idx_to]) == 1:
            opponent_checker = self.__points[idx_to][0]
            # Verificar que sea del oponente (si las fichas tienen color)
            if hasattr(ficha, 'get_color') and hasattr(opponent_checker, 'get_color'):
                if ficha.get_color() != opponent_checker.get_color():
                    captured = self.__points[idx_to].pop()
                    # Agregar a la barra
                    self.__bar_manager.add_to_bar(captured.get_color())
        
        # Colocar ficha en destino
        self.__points[idx_to].append(ficha)
        
        return captured

    def get_top_checker(self, position: int) -> Optional[Any]:
        """
        Retorna la ficha superior de una posición sin removerla.
        
        Args:
            position: Posición a consultar (1-24)
            
        Returns:
            La ficha superior, o None si está vacío
        """
        self._validate_position(position)
        idx = position - 1
        
        if len(self.__points[idx]) == 0:
            return None
        
        return self.__points[idx][-1]



    def add_to_bar(self, color: str) -> None:
        """Agrega una ficha del color a la barra."""
        self.__bar_manager.add_to_bar(color)

    def remove_from_bar(self, color: str) -> bool:
        """Remueve una ficha del color de la barra."""
        return self.__bar_manager.remove_from_bar(color)

    def get_bar_count(self, color: str) -> int:
        """Retorna cantidad de fichas del color en la barra."""
        return self.__bar_manager.get_count(color)

    def has_checkers_on_bar(self, color: str) -> bool:
        """Verifica si hay fichas del color en la barra."""
        return self.__bar_manager.has_checkers(color)

 

    def bear_off_checker(self, color: str) -> None:
        """Saca una ficha del color del tablero."""
        self.__bear_off_manager.bear_off(color)

    def get_bear_off_count(self, color: str) -> int:
        """Retorna cantidad de fichas del color fuera del juego."""
        return self.__bear_off_manager.get_count(color)

    def has_won(self, color: str) -> bool:
        """Verifica si el jugador del color ganó."""
        return self.__bear_off_manager.has_won(color)

  

    def get_estado(self) -> List[Any]:
        """
        Retorna el estado del tablero con índices 1-24.
        
        Returns:
            Lista donde el índice 0 es None y del 1-24 tiene el nombre 
            del último checker en cada punto (o None si está vacío)
        """
        estado = [None]
        for punto in self.__points:
            if len(punto) == 0:
                estado.append(None)
            else:
                if hasattr(punto[-1], 'get_nombre'):
                    estado.append(punto[-1].get_nombre())
                else:
                    estado.append(str(punto[-1]))
        return estado

    def get_full_state(self) -> Dict[str, Any]:
        """
        Retorna el estado completo del tablero.
        
        Returns:
            Diccionario con points, bar y off
        """
        return {
            "points": self.get_points(),
            "bar": self.__bar_manager.get_state(),
            "off": self.__bear_off_manager.get_state()
        }



    @property
    def points(self) -> List[list]:
        """Property para acceso directo a los puntos."""
        return self.__points

    @property
    def bar(self) -> Dict[str, int]:
        """Property para acceso al estado de la barra."""
        return self.__bar_manager.get_state()

    @property
    def off(self) -> Dict[str, int]:
        """Property para acceso al estado de bear off."""
        return self.__bear_off_manager.get_state()

   

    def _validate_position(self, position: int) -> None:
        """
        Valida que una posición esté en el rango válido (1-24).
        
        Args:
            position: Posición a validar
            
        Raises:
            ValueError: Si la posición está fuera del rango
        """
        if not (1 <= position <= 24):
            raise ValueError(f"La posición debe estar entre 1 y 24, recibido: {position}")



    def __repr__(self) -> str:
        """Representación string del tablero."""
        total_checkers = sum(len(point) for point in self.__points)
        return (f"Board(points=24, checkers={total_checkers}, "
                f"bar={self.bar}, off={self.off})")

    def __str__(self) -> str:
        """String legible del tablero."""
        lines = ["=== BOARD STATE ==="]
        for i, point in enumerate(self.__points, start=1):
            lines.append(f"Point {i:2d}: {len(point)} checkers")
        lines.append(f"Bar: {self.bar}")
        lines.append(f"Off: {self.off}")
        return "\n".join(lines)




class BoardWithSetup(Board):
    """
    OCP: Extensión de Board que incluye posición inicial estándar.
    
    No modifica Board, solo extiende su comportamiento.
    """

    def initialize_points(self) -> List[list]:
        """
        Inicializa con la posición estándar de Backgammon.
        
        Nota: Requiere objetos Checker o similar para las fichas.
        Por ahora retorna estructura vacía y se debe llamar a setup_initial_position.
        """
        return [[] for _ in range(24)]

    def setup_initial_position(self, player_white: Any, player_black: Any) -> None:
        """
        Configura la posición inicial estándar del juego.
        
        Args:
            player_white: Jugador/Checker blanco
            player_black: Jugador/Checker negro
        """
        # Limpiar tablero
        self.reset()
        
        # Posición inicial estándar (fichas blancas)
        # 2 fichas en punto 1
        for _ in range(2):
            self.colocar_ficha(player_white, 1)
        
        # 5 fichas en punto 12
        for _ in range(5):
            self.colocar_ficha(player_white, 12)
        
        # 3 fichas en punto 17
        for _ in range(3):
            self.colocar_ficha(player_white, 17)
        
        # 5 fichas en punto 19
        for _ in range(5):
            self.colocar_ficha(player_white, 19)
        
        # Posición inicial estándar (fichas negras - espejo)
        # 2 fichas en punto 24
        for _ in range(2):
            self.colocar_ficha(player_black, 24)
        
        # 5 fichas en punto 13
        for _ in range(5):
            self.colocar_ficha(player_black, 13)
        
        # 3 fichas en punto 8
        for _ in range(3):
            self.colocar_ficha(player_black, 8)
        
        # 5 fichas en punto 6
        for _ in range(5):
            self.colocar_ficha(player_black, 6)