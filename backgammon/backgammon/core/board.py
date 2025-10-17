from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseBoard(ABC):
    """Base para tableros de Backgammon (OCP)."""

    @abstractmethod
    def initialize_points(self) -> List[list]:
        """Devuelve la estructura inicial de 24 puntos."""
        raise NotImplementedError


class Board(BaseBoard):
    """
    Tablero estándar: 24 puntos + bar + off.
    Aplica principios SOLID:
    - SRP: Solo maneja el estado del tablero
    - OCP: Extensible mediante herencia de BaseBoard
    - LSP: Puede ser sustituida por otras implementaciones de BaseBoard
    - DIP: No depende de implementaciones concretas
    """

    def __init__(self) -> None:
        # Atributos privados con __
        self.__points: List[list] = self.initialize_points()
        self.__bar: Dict[str, int] = {"blanco": 0, "negro": 0}
        self.__off: Dict[str, int] = {"blanco": 0, "negro": 0}

    def initialize_points(self) -> List[list]:
        """
        Por ahora tablero vacío. Si luego quiero arrancar con fichas 
        puestas, lo cambio acá o armamos otra clase que herede
        """
        return [[] for _ in range(24)]

    def get_points(self) -> List[list]:
        """Devuelve los puntos del tablero"""
        return self.__points

    def get_bar(self) -> Dict[str, int]:
        """Devuelve el bar (fichas capturadas)"""
        return self.__bar.copy()

    def get_off(self) -> Dict[str, int]:
        """Devuelve las fichas fuera del tablero"""
        return self.__off.copy()

    def get_estado(self) -> List[Any]:
        estado = [None]  # Cambiar [[]] por [None]
        for punto in self.__points:
            if len(punto) == 0:
                estado.append(None)  # Cambiar [] por None
            else:
                estado.append(punto[-1].get_nombre())
        return estado
    
    def point_count(self, index: int) -> int:
        """Me da cuántas fichas hay en el punto 1..24. Simple"""
        i = index - 1
        if not (0 <= i < 24):
            raise IndexError("El punto debe estar entre 1 y 24.")
        return len(self.__points[i])

    def colocar_ficha(self, player: Any, posicion: int) -> None:
        """
        Coloca una ficha del jugador en la posición indicada (1-24).
        
        Args:
            player: Jugador que coloca la ficha
            posicion: Posición donde colocar (1-24)
            
        Raises:
            ValueError: Si la posición es inválida
        """
        if not (1 <= posicion <= 24):
            raise ValueError("La posición debe estar entre 1 y 24")
        idx = posicion - 1
        self.__points[idx].append(player)

    def quitar_ficha(self, posicion: int) -> Optional[Any]:
        """
        Quita una ficha de la posición indicada (1-24).
        
        Args:
            posicion: Posición de donde quitar la ficha (1-24)
            
        Returns:
            El jugador dueño de la ficha removida, o None si no había fichas
            
        Raises:
            ValueError: Si la posición es inválida
        """
        if not (1 <= posicion <= 24):
            raise ValueError("La posición debe estar entre 1 y 24")
        idx = posicion - 1
        if len(self.__points[idx]) == 0:
            return None
        return self.__points[idx].pop()

    def mover_ficha(self, desde: int, hasta: int) -> None:
        """
        Mueve una ficha desde una posición a otra.
        
        Args:
            desde: Posición origen (1-24)
            hasta: Posición destino (1-24)
            
        Raises:
            ValueError: Si las posiciones son inválidas o no hay ficha para mover
        """
        if not (1 <= desde <= 24):
            raise ValueError("La posición 'desde' debe estar entre 1 y 24")
        if not (1 <= hasta <= 24):
            raise ValueError("La posición 'hasta' debe estar entre 1 y 24")
        idx_desde = desde - 1
        if len(self.__points[idx_desde]) == 0:
            raise ValueError(f"No hay fichas en la posición {desde}")
        ficha = self.__points[idx_desde].pop()
        idx_hasta = hasta - 1
        self.__points[idx_hasta].append(ficha)

    def reset(self) -> None:
        """Reinicia el tablero a su estado inicial"""
        self.__points = self.initialize_points()
        self.__bar = {"blanco": 0, "negro": 0}
        self.__off = {"blanco": 0, "negro": 0}

    @property
    def points(self) -> List[list]:
        """Property para acceso a los puntos (compatibilidad)"""
        return self.__points

    @property
    def bar(self) -> Dict[str, int]:
        """Property para acceso al bar (compatibilidad)"""
        return self.__bar

    @property
    def off(self) -> Dict[str, int]:
        """Property para acceso a off (compatibilidad)"""
        return self.__off

    def __repr__(self) -> str:
        return f"Board(points={len(self.__points)}, bar={self.__bar}, off={self.__off})"