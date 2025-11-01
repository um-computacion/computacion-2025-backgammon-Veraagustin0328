from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
"""
Módulo que define el tablero de Backgammon.
"""


if TYPE_CHECKING:
    from .player import Player
    from .checker import Checker


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    """

    def __init__(self) -> None:
        """
        Inicializa un tablero vacío con 24 puntos.
        Puntos numerados del 1 al 24.
        """
        # 25 elementos: índice 0 no se usa, puntos 1-24
        self.points: List[List[Checker]] = [[] for _ in range(25)]
        self.bar: List[Checker] = []  # Fichas capturadas
        self.off: dict[str, int] = {"blanco": 0, "negro": 0}  # Fichas sacadas

    def colocar_ficha(self, player: Player, point: int) -> None:
        """
        Coloca una ficha del jugador en un punto específico.
        
        Args:
            player: Jugador dueño de la ficha
            point: Número del punto (1-24)
        
        Raises:
            ValueError: Si el punto está fuera del rango válido
        """
        if not (1 <= point <= 24):
            raise ValueError(f"Punto {point} fuera de rango (1-24)")
        
        from .checker import Checker
        checker = Checker(player=player, color=player.get_color())
        self.points[point].append(checker)

    def mover_ficha(self, origin: int, dest: int) -> None:
        """
        Mueve una ficha de un punto a otro.
        Si hay una ficha solitaria del oponente en el destino, la captura automáticamente.
        
        Args:
            origin: Punto de origen (1-24)
            dest: Punto de destino (1-24)
        
        Raises:
            ValueError: Si el movimiento es inválido
        """
        if not (1 <= origin <= 24 and 1 <= dest <= 24):
            raise ValueError("Puntos fuera de rango")
        
        if not self.points[origin]:
            raise ValueError(f"No hay fichas en el punto {origin}")
        
        # Sacar ficha del origen
        checker = self.points[origin].pop()
        
        # Verificar si hay captura (1 ficha solitaria del oponente)
        if self.point_count(dest) == 1:
            dest_checker = self.get_top_checker(dest)
            if dest_checker and dest_checker.get_color() != checker.get_color():
                # Capturar: sacar la ficha del oponente y ponerla en bar
                captured = self.points[dest].pop()
                self.bar.append(captured)
        
        # Colocar la ficha en el destino
        self.points[dest].append(checker)

    def point_count(self, point: int) -> int:
        """
        Cuenta las fichas en un punto.
        
        Args:
            point: Número del punto (1-24)
        
        Returns:
            Cantidad de fichas en el punto
        """
        if not (1 <= point <= 24):
            return 0
        return len(self.points[point])

    def get_top_checker(self, point: int) -> Optional[Checker]:
        """
        Obtiene la ficha superior de un punto.
        
        Args:
            point: Número del punto (1-24)
        
        Returns:
            La ficha superior o None si el punto está vacío
        """
        if not (1 <= point <= 24):
            return None
        
        if not self.points[point]:
            return None
        
        return self.points[point][-1]

    def get_bar_count(self, color: str) -> int:
        """
        Cuenta las fichas de un color en la barra.
        
        Args:
            color: Color de las fichas ('blanco' o 'negro')
        
        Returns:
            Cantidad de fichas en la barra
        """
        return sum(1 for c in self.bar if c.get_color() == color)

    def get_off_count(self, color: str) -> int:
        """
        Obtiene la cantidad de fichas sacadas del tablero.
        
        Args:
            color: Color de las fichas ('blanco' o 'negro')
        
        Returns:
            Cantidad de fichas sacadas
        """
        return self.off.get(color, 0)

    def is_empty(self, point: int) -> bool:
        """
        Verifica si un punto está vacío.
        
        Args:
            point: Número del punto (1-24)
        
        Returns:
            True si el punto está vacío
        """
        if not (1 <= point <= 24):
            return True
        return len(self.points[point]) == 0

    def get_point_color(self, point: int) -> Optional[str]:
        """
        Obtiene el color de las fichas en un punto.
        
        Args:
            point: Número del punto (1-24)
        
        Returns:
            Color de las fichas o None si está vacío
        """
        if self.is_empty(point):
            return None
        
        top = self.get_top_checker(point)
        return top.get_color() if top else None

    def can_place_checker(self, point: int, color: str) -> bool:
        """
        Verifica si se puede colocar una ficha en un punto.
        
        Args:
            point: Número del punto (1-24)
            color: Color de la ficha a colocar
        
        Returns:
            True si se puede colocar
        """
        if not (1 <= point <= 24):
            return False
        
        if self.is_empty(point):
            return True
        
        point_color = self.get_point_color(point)
        if point_color == color:
            return True
        
        # Solo se puede capturar si hay una sola ficha del oponente
        return self.point_count(point) == 1

    def capture_checker(self, checker: Checker) -> None:
        """
        Captura una ficha y la coloca en la barra.
        
        Args:
            checker: Ficha a capturar
        """
        self.bar.append(checker)

    def remove_from_bar(self, color: str) -> Optional[Checker]:
        """
        Saca una ficha de la barra.
        
        Args:
            color: Color de la ficha a sacar
        
        Returns:
            La ficha sacada o None si no hay fichas de ese color
        """
        for i, checker in enumerate(self.bar):
            if checker.get_color() == color:
                return self.bar.pop(i)
        return None

    def bear_off(self, color: str) -> None:
        """
        Saca una ficha del tablero (bear off).
        
        Args:
            color: Color de la ficha a sacar
        """
        self.off[color] = self.off.get(color, 0) + 1

    def bear_off_checker(self, color: str) -> None:
        """
        Saca una ficha del tablero (bear off).
        Alias de bear_off para compatibilidad con tests.
        
        Args:
            color: Color de la ficha a sacar
        """
        self.bear_off(color)

    def has_won(self, color: str) -> bool:
        """
        Verifica si un jugador ganó (sacó todas sus 15 fichas).
        
        Args:
            color: Color del jugador
        
        Returns:
            True si tiene 15 fichas fuera del tablero
        """
        return self.get_off_count(color) >= 15

    def get_all_checkers(self, color: str) -> List[tuple[int, int]]:
        """
        Obtiene todas las posiciones de fichas de un color.
        
        Args:
            color: Color de las fichas
        
        Returns:
            Lista de tuplas (punto, cantidad)
        """
        positions = []
        for point in range(1, 25):
            if self.get_point_color(point) == color:
                positions.append((point, self.point_count(point)))
        return positions

    def is_in_home_board(self, point: int, color: str) -> bool:
        """
        Verifica si un punto está en el home board del jugador.
        
        Args:
            point: Número del punto
            color: Color del jugador
        
        Returns:
            True si el punto está en el home board
        """
        if color == "blanco":
            return 19 <= point <= 24
        else:
            return 1 <= point <= 6

    def all_in_home_board(self, color: str) -> bool:
        """
        Verifica si todas las fichas de un color están en su home board.
        
        Args:
            color: Color del jugador
        
        Returns:
            True si todas las fichas están en home board
        """
        if color == "blanco":
            home_range = range(19, 25)
        else:
            home_range = range(1, 7)
        
        # Verificar que no haya fichas fuera del home board
        for point in range(1, 25):
            if point not in home_range:
                if self.get_point_color(point) == color:
                    return False
        
        # Verificar que no haya fichas en la barra
        if self.get_bar_count(color) > 0:
            return False
        
        return True

    def clear(self) -> None:
        """Limpia el tablero completamente."""
        self.points = [[] for _ in range(25)]
        self.bar = []
        self.off = {"blanco": 0, "negro": 0}

    def __str__(self) -> str:
        """Representación en string del tablero."""
        lines = []
        lines.append("=== TABLERO DE BACKGAMMON ===")
        
        # Mostrar puntos 13-24
        top_line = "Arriba (13-24): "
        for point in range(13, 25):
            count = self.point_count(point)
            color = self.get_point_color(point)
            if count > 0:
                symbol = "●" if color == "blanco" else "○"
                top_line += f"[{point}:{symbol}{count}] "
        lines.append(top_line)
        
        # Barra y off
        lines.append(f"Bar: Blancas={self.get_bar_count('blanco')}, Negras={self.get_bar_count('negro')}")
        lines.append(f"Off: Blancas={self.off.get('blanco', 0)}, Negras={self.off.get('negro', 0)}")
        
        # Mostrar puntos 12-1
        bottom_line = "Abajo (12-1):  "
        for point in range(12, 0, -1):
            count = self.point_count(point)
            color = self.get_point_color(point)
            if count > 0:
                symbol = "●" if color == "blanco" else "○"
                bottom_line += f"[{point}:{symbol}{count}] "
        lines.append(bottom_line)
        
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Representación técnica del tablero."""
        return f"Board(points={len([p for p in self.points if p])}, bar={len(self.bar)}, off={self.off})"


class BoardWithSetup(Board):
    """
    Tablero con posición inicial estándar de Backgammon.
    """

    def setup_initial_position(self, player1: Player, player2: Player) -> None:
        """
        Configura la posición inicial estándar del Backgammon.
        
        Posición inicial estándar (vista desde el lado de las blancas):
        - Punto 1:  2 fichas BLANCAS
        - Punto 6:  5 fichas NEGRAS
        - Punto 8:  3 fichas NEGRAS
        - Punto 12: 5 fichas BLANCAS
        - Punto 13: 5 fichas NEGRAS
        - Punto 17: 3 fichas BLANCAS
        - Punto 19: 5 fichas BLANCAS
        - Punto 24: 2 fichas NEGRAS
        
        Args:
            player1: Jugador con fichas blancas
            player2: Jugador con fichas negras
        """
        # Limpiar tablero
        self.clear()
        
        # Fichas BLANCAS (player1)
        # Punto 1: 2 blancas
        for _ in range(2):
            self.colocar_ficha(player1, 1)
        
        # Punto 12: 5 blancas
        for _ in range(5):
            self.colocar_ficha(player1, 12)
        
        # Punto 17: 3 blancas
        for _ in range(3):
            self.colocar_ficha(player1, 17)
        
        # Punto 19: 5 blancas
        for _ in range(5):
            self.colocar_ficha(player1, 19)
        
        # Fichas NEGRAS (player2)
        # Punto 24: 2 negras
        for _ in range(2):
            self.colocar_ficha(player2, 24)
        
        # Punto 13: 5 negras
        for _ in range(5):
            self.colocar_ficha(player2, 13)
        
        # Punto 8: 3 negras
        for _ in range(3):
            self.colocar_ficha(player2, 8)
        
        # Punto 6: 5 negras
        for _ in range(5):
            self.colocar_ficha(player2, 6)