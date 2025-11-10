"""
Implementación SOLID de Board siguiendo SRP.

Separa las responsabilidades de Board en:
- BoardPoints: Gestión de puntos 1-24
- BarManager: Gestión de la barra (fichas capturadas)
- BearOffManager: Gestión de bear off (fichas sacadas)
- CaptureRules: Lógica de captura de fichas
- BoardValidator: Validaciones de colocación

BoardFacade coordina estos componentes siguiendo el patrón Facade.
"""

from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player
    from .checker import Checker

from .board import Board, BoardWithSetup


class BoardPoints:
    """
    SRP: Responsabilidad única de gestionar los 24 puntos del tablero.
    
    Maneja solo el estado de los puntos (fichas en cada posición).
    """
    
    def __init__(self):
        # 25 elementos: índice 0 no se usa, puntos 1-24
        self.__points: List[List] = [[] for _ in range(25)]
    
    def get_points(self) -> List[List]:
        """Getter de todos los puntos."""
        return self.__points
    
    def get_point(self, point: int) -> List:
        """
        Getter de un punto específico.
        
        Args:
            point: Número del punto (1-24)
            
        Returns:
            Lista de fichas en ese punto
        """
        if not (1 <= point <= 24):
            return []
        return self.__points[point]
    
    def add_checker_to_point(self, point: int, checker) -> None:
        """
        Agrega una ficha a un punto.
        
        Args:
            point: Número del punto (1-24)
            checker: Ficha a agregar
        """
        if not (1 <= point <= 24):
            raise ValueError(f"Punto {point} fuera de rango (1-24)")
        self.__points[point].append(checker)
    
    def remove_checker_from_point(self, point: int):
        """
        Remueve y retorna la ficha superior de un punto.
        
        Args:
            point: Número del punto (1-24)
            
        Returns:
            La ficha removida
        """
        if not (1 <= point <= 24):
            raise ValueError(f"Punto {point} fuera de rango (1-24)")
        
        if not self.__points[point]:
            raise ValueError(f"No hay fichas en el punto {point}")
        
        return self.__points[point].pop()
    
    def point_count(self, point: int) -> int:
        """
        Cuenta las fichas en un punto.
        
        Args:
            point: Número del punto (1-24)
            
        Returns:
            Cantidad de fichas
        """
        if not (1 <= point <= 24):
            return 0
        return len(self.__points[point])
    
    def get_top_checker(self, point: int):
        """
        Obtiene la ficha superior de un punto sin removerla.
        
        Args:
            point: Número del punto (1-24)
            
        Returns:
            La ficha superior o None
        """
        if not (1 <= point <= 24):
            return None
        
        if not self.__points[point]:
            return None
        
        return self.__points[point][-1]
    
    def clear(self) -> None:
        """Limpia todos los puntos."""
        self.__points = [[] for _ in range(25)]


class BarManager:
    """
    SRP: Responsabilidad única de gestionar la barra.
    
    Maneja las fichas capturadas que deben re-entrar al tablero.
    """
    
    def __init__(self):
        self.__bar: List = []
    
    def get_bar(self) -> List:
        """Getter de la barra."""
        return self.__bar
    
    def add_to_bar(self, checker) -> None:
        """
        Agrega una ficha a la barra.
        
        Args:
            checker: Ficha capturada
        """
        self.__bar.append(checker)
    
    def remove_from_bar(self, color: str):
        """
        Remueve una ficha de la barra por color.
        
        Args:
            color: Color de la ficha a remover
            
        Returns:
            La ficha removida o None
        """
        for i, checker in enumerate(self.__bar):
            if checker.get_color() == color:
                return self.__bar.pop(i)
        return None
    
    def get_bar_count(self, color: str) -> int:
        """
        Cuenta las fichas de un color en la barra.
        
        Args:
            color: Color de las fichas
            
        Returns:
            Cantidad de fichas
        """
        return sum(1 for c in self.__bar if c.get_color() == color)
    
    def clear(self) -> None:
        """Limpia la barra."""
        self.__bar = []


class BearOffManager:
    """
    SRP: Responsabilidad única de gestionar bear off.
    
    Maneja las fichas que han sido sacadas del tablero.
    """
    
    def __init__(self):
        self.__off: dict = {"blanco": 0, "negro": 0}
    
    def get_off_dict(self) -> dict:
        """Getter del diccionario de bear off."""
        return self.__off
    
    def get_off_count(self, color: str) -> int:
        """
        Obtiene la cantidad de fichas sacadas de un color.
        
        Args:
            color: Color de las fichas
            
        Returns:
            Cantidad de fichas sacadas
        """
        return self.__off.get(color, 0)
    
    def bear_off_checker(self, color: str) -> None:
        """
        Saca una ficha del tablero (bear off).
        
        Args:
            color: Color de la ficha
        """
        self.__off[color] = self.__off.get(color, 0) + 1
    
    def has_won(self, color: str) -> bool:
        """
        Verifica si un jugador ganó (15 fichas sacadas).
        
        Args:
            color: Color del jugador
            
        Returns:
            True si tiene 15 fichas fuera
        """
        return self.get_off_count(color) >= 15
    
    def clear(self) -> None:
        """Reinicia bear off."""
        self.__off = {"blanco": 0, "negro": 0}


class CaptureRules:
    """
    SRP: Responsabilidad única de implementar reglas de captura.
    
    Determina cuándo y cómo capturar fichas del oponente.
    """
    
    def __init__(self, points: BoardPoints, bar: BarManager):
        self.__points = points
        self.__bar = bar
    
    def get_points(self) -> BoardPoints:
        """Getter de BoardPoints."""
        return self.__points
    
    def set_points(self, points: BoardPoints) -> None:
        """Setter de BoardPoints."""
        self.__points = points
    
    def get_bar(self) -> BarManager:
        """Getter de BarManager."""
        return self.__bar
    
    def set_bar(self, bar: BarManager) -> None:
        """Setter de BarManager."""
        self.__bar = bar
    
    def should_capture(self, dest: int, moving_checker) -> bool:
        """
        Determina si se debe capturar una ficha en el destino.
        
        Args:
            dest: Punto de destino
            moving_checker: Ficha que se está moviendo
            
        Returns:
            True si debe capturar
        """
        # Solo captura si hay exactamente 1 ficha del oponente
        if self.__points.point_count(dest) != 1:
            return False
        
        dest_checker = self.__points.get_top_checker(dest)
        if not dest_checker:
            return False
        
        # Captura solo si es del color opuesto
        return dest_checker.get_color() != moving_checker.get_color()
    
    def execute_capture(self, dest: int) -> None:
        """
        Ejecuta la captura de una ficha.
        
        Args:
            dest: Punto donde está la ficha a capturar
        """
        captured = self.__points.remove_checker_from_point(dest)
        self.__bar.add_to_bar(captured)


class BoardValidator:
    """
    SRP: Responsabilidad única de validar operaciones en el tablero.
    
    Verifica si se pueden colocar fichas en posiciones específicas.
    """
    
    def __init__(self, points: BoardPoints):
        self.__points = points
    
    def get_points(self) -> BoardPoints:
        """Getter de BoardPoints."""
        return self.__points
    
    def set_points(self, points: BoardPoints) -> None:
        """Setter de BoardPoints."""
        self.__points = points
    
    def can_place_checker(self, point: int, color: str) -> bool:
        """
        Verifica si se puede colocar una ficha en un punto.
        
        Args:
            point: Número del punto
            color: Color de la ficha
            
        Returns:
            True si se puede colocar
        """
        if not (1 <= point <= 24):
            return False
        
        # Punto vacío: siempre se puede
        if self.__points.point_count(point) == 0:
            return True
        
        top = self.__points.get_top_checker(point)
        if not top:
            return True
        
        point_color = top.get_color()
        
        # Mismo color: siempre se puede
        if point_color == color:
            return True
        
        # Color diferente: solo si hay 1 ficha (captura)
        return self.__points.point_count(point) == 1
    
    def is_empty(self, point: int) -> bool:
        """
        Verifica si un punto está vacío.
        
        Args:
            point: Número del punto
            
        Returns:
            True si está vacío
        """
        return self.__points.point_count(point) == 0
    
    def get_point_color(self, point: int) -> Optional[str]:
        """
        Obtiene el color de las fichas en un punto.
        
        Args:
            point: Número del punto
            
        Returns:
            Color o None si está vacío
        """
        if self.is_empty(point):
            return None
        
        top = self.__points.get_top_checker(point)
        return top.get_color() if top else None


class BoardFacade:
    """
    Facade Pattern: Coordina los componentes de Board siguiendo SOLID.
    
    Componentes:
    - BoardPoints: Gestiona puntos 1-24
    - BarManager: Gestiona la barra
    - BearOffManager: Gestiona bear off
    - CaptureRules: Implementa reglas de captura
    - BoardValidator: Valida operaciones
    
    Esta clase mantiene compatibilidad con la interfaz de Board original,
    pero internamente delega responsabilidades a componentes especializados.
    
    DIP: Acepta inyección de dependencias para los componentes.
    """
    
    def __init__(
        self,
        points: Optional[BoardPoints] = None,
        bar: Optional[BarManager] = None,
        bear_off: Optional[BearOffManager] = None,
        capture_rules: Optional[CaptureRules] = None,
        validator: Optional[BoardValidator] = None
    ):
        """
        Inicializa el tablero con inyección de dependencias (DIP).
        
        Args:
            points: Componente de puntos (si es None, crea uno)
            bar: Componente de barra (si es None, crea uno)
            bear_off: Componente de bear off (si es None, crea uno)
            capture_rules: Componente de reglas de captura (si es None, crea uno)
            validator: Componente de validación (si es None, crea uno)
        """
        # Inyección de dependencias (DIP)
        self.__points = points or BoardPoints()
        self.__bar = bar or BarManager()
        self.__bear_off = bear_off or BearOffManager()
        self.__capture_rules = capture_rules or CaptureRules(self.__points, self.__bar)
        self.__validator = validator or BoardValidator(self.__points)
        
        # Guardar referencia a Board original para compatibilidad
        self.__original_board = Board()
    
    # ========== Getters y Setters de componentes ==========
    
    def get_points_component(self) -> BoardPoints:
        """Getter del componente de puntos."""
        return self.__points
    
    def set_points_component(self, points: BoardPoints) -> None:
        """Setter del componente de puntos."""
        self.__points = points
        self.__capture_rules.set_points(points)
        self.__validator.set_points(points)
    
    def get_bar_component(self) -> BarManager:
        """Getter del componente de barra."""
        return self.__bar
    
    def set_bar_component(self, bar: BarManager) -> None:
        """Setter del componente de barra."""
        self.__bar = bar
        self.__capture_rules.set_bar(bar)
    
    def get_bear_off_component(self) -> BearOffManager:
        """Getter del componente de bear off."""
        return self.__bear_off
    
    def set_bear_off_component(self, bear_off: BearOffManager) -> None:
        """Setter del componente de bear off."""
        self.__bear_off = bear_off
    
    def get_capture_rules(self) -> CaptureRules:
        """Getter del componente de reglas de captura."""
        return self.__capture_rules
    
    def set_capture_rules(self, capture_rules: CaptureRules) -> None:
        """Setter del componente de reglas de captura."""
        self.__capture_rules = capture_rules
    
    def get_validator(self) -> BoardValidator:
        """Getter del componente de validación."""
        return self.__validator
    
    def set_validator(self, validator: BoardValidator) -> None:
        """Setter del componente de validación."""
        self.__validator = validator
    
    # ========== Delegación a BoardPoints ==========
    
    @property
    def points(self) -> List[List]:
        """Property para acceso a los puntos (compatibilidad)."""
        return self.__points.get_points()
    
    def point_count(self, point: int) -> int:
        """Cuenta las fichas en un punto."""
        return self.__points.point_count(point)
    
    def get_top_checker(self, point: int):
        """Obtiene la ficha superior de un punto."""
        return self.__points.get_top_checker(point)
    
    def colocar_ficha(self, player, point: int) -> None:
        """
        Coloca una ficha del jugador en un punto.
        
        Args:
            player: Jugador dueño de la ficha
            point: Número del punto (1-24)
        """
        from .checker import Checker
        checker = Checker(player=player, color=player.get_color())
        self.__points.add_checker_to_point(point, checker)
        
        # Sincronizar con Board original
        self.__original_board.colocar_ficha(player, point)
    
    # ========== Delegación a BarManager ==========
    
    @property
    def bar(self) -> List:
        """Property para acceso a la barra (compatibilidad)."""
        return self.__bar.get_bar()
    
    def get_bar_count(self, color: str) -> int:
        """Cuenta las fichas de un color en la barra."""
        return self.__bar.get_bar_count(color)
    
    def capture_checker(self, checker) -> None:
        """Captura una ficha y la coloca en la barra."""
        self.__bar.add_to_bar(checker)
    
    def remove_from_bar(self, color: str):
        """Saca una ficha de la barra."""
        return self.__bar.remove_from_bar(color)
    
    # ========== Delegación a BearOffManager ==========
    
    @property
    def off(self) -> dict:
        """Property para acceso a bear off (compatibilidad)."""
        return self.__bear_off.get_off_dict()
    
    def get_off_count(self, color: str) -> int:
        """Obtiene la cantidad de fichas sacadas."""
        return self.__bear_off.get_off_count(color)
    
    def bear_off(self, color: str) -> None:
        """Saca una ficha del tablero (bear off)."""
        self.__bear_off.bear_off_checker(color)
    
    def bear_off_checker(self, color: str) -> None:
        """Alias de bear_off para compatibilidad."""
        self.bear_off(color)
    
    def has_won(self, color: str) -> bool:
        """Verifica si un jugador ganó."""
        return self.__bear_off.has_won(color)
    
    # ========== Delegación a BoardValidator ==========
    
    def is_empty(self, point: int) -> bool:
        """Verifica si un punto está vacío."""
        return self.__validator.is_empty(point)
    
    def get_point_color(self, point: int) -> Optional[str]:
        """Obtiene el color de las fichas en un punto."""
        return self.__validator.get_point_color(point)
    
    def can_place_checker(self, point: int, color: str) -> bool:
        """Verifica si se puede colocar una ficha."""
        return self.__validator.can_place_checker(point, color)
    
    # ========== Operaciones con captura ==========
    
    def mover_ficha(self, origin: int, dest: int) -> None:
        """
        Mueve una ficha de un punto a otro con captura automática.
        
        Args:
            origin: Punto de origen (1-24)
            dest: Punto de destino (1-24)
        """
        if not (1 <= origin <= 24 and 1 <= dest <= 24):
            raise ValueError("Puntos fuera de rango")
        
        # Remover ficha del origen
        checker = self.__points.remove_checker_from_point(origin)
        
        # Verificar si hay captura
        if self.__capture_rules.should_capture(dest, checker):
            self.__capture_rules.execute_capture(dest)
        
        # Colocar la ficha en el destino
        self.__points.add_checker_to_point(dest, checker)
    
    # ========== Métodos de análisis ==========
    
    def is_in_home_board(self, point: int, color: str) -> bool:
        """
        Verifica si un punto está en el home board.
        
        Args:
            point: Número del punto
            color: Color del jugador
            
        Returns:
            True si está en home board
        """
        if color == "blanco":
            return 19 <= point <= 24
        else:
            return 1 <= point <= 6
    
    def all_in_home_board(self, color: str) -> bool:
        """
        Verifica si todas las fichas están en home board.
        
        Args:
            color: Color del jugador
            
        Returns:
            True si todas están en home
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
    
    def get_all_checkers(self, color: str) -> List[Tuple[int, int]]:
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
    
    # ========== Limpieza y reinicio ==========
    
    def clear(self) -> None:
        """Limpia el tablero completamente."""
        self.__points.clear()
        self.__bar.clear()
        self.__bear_off.clear()
    
    # ========== Representación ==========
    
    def __str__(self) -> str:
        """Representación en string del tablero."""
        lines = []
        lines.append("=== TABLERO DE BACKGAMMON (SOLID) ===")
        
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
        lines.append(f"Off: Blancas={self.get_off_count('blanco')}, Negras={self.get_off_count('negro')}")
        
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
        active_points = len([p for p in self.__points.get_points() if p])
        return f"BoardFacade(points={active_points}, bar={len(self.bar)}, off={self.off}, SOLID=True)"


class BoardWithSetupFacade(BoardFacade):
    """
    Tablero con posición inicial usando Strategy Pattern.
    
    OCP: Extensible sin modificar BoardFacade.
    LSP: Sustituible por BoardFacade.
    """
    
    def setup_initial_position(self, player1, player2) -> None:
        """
        Configura la posición inicial estándar del Backgammon.
        
        Usa el patrón Strategy para aplicar diferentes configuraciones iniciales.
        
        Args:
            player1: Jugador con fichas blancas
            player2: Jugador con fichas negras
        """
        # Limpiar tablero
        self.clear()
        
        # Fichas BLANCAS (player1)
        for _ in range(2):
            self.colocar_ficha(player1, 1)
        
        for _ in range(5):
            self.colocar_ficha(player1, 12)
        
        for _ in range(3):
            self.colocar_ficha(player1, 17)
        
        for _ in range(5):
            self.colocar_ficha(player1, 19)
        
        # Fichas NEGRAS (player2)
        for _ in range(2):
            self.colocar_ficha(player2, 24)
        
        for _ in range(5):
            self.colocar_ficha(player2, 13)
        
        for _ in range(3):
            self.colocar_ficha(player2, 8)
        
        for _ in range(5):
            self.colocar_ficha(player2, 6)