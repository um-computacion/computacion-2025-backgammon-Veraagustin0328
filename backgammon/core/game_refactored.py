from __future__ import annotations
from typing import Optional, List
from .game import Game
from .player import Player
from .board import Board
from .dice import Dice


class MoveValidator:
    """
    SRP: Responsabilidad única de validar movimientos.
    
    Extrae la lógica de validación que antes estaba en Game.is_valid_move()
    """
    
    def __init__(self, board: Board, current_player: Player):
        self.__board = board
        self.__current_player = current_player
    
    def get_board(self) -> Board:
        """Getter del tablero."""
        return self.__board
    
    def set_board(self, board: Board) -> None:
        """Setter del tablero."""
        self.__board = board
    
    def get_current_player(self) -> Player:
        """Getter del jugador actual."""
        return self.__current_player
    
    def set_current_player(self, player: Player) -> None:
        """Setter del jugador actual."""
        self.__current_player = player
    
    def is_valid_move(self, origin: int, dest: int, dice_value: int) -> bool:
        """
        Verifica si un movimiento es válido según las reglas de Backgammon.
        
        Args:
            origin: Punto de origen (1-24)
            dest: Punto de destino (1-24)
            dice_value: Valor del dado a usar
        
        Returns:
            True si el movimiento es válido, False en caso contrario
        """
        # Verificar que el punto origen tenga fichas
        if self.__board.point_count(origin) == 0:
            return False
        
        # Verificar que la ficha del origen sea del jugador actual
        top_checker = self.__board.get_top_checker(origin)
        if top_checker is None:
            return False
        
        if top_checker.get_color() != self.__current_player.get_color():
            return False
        
        # Verificar que la distancia coincida con el dado
        current_color = self.__current_player.get_color()
        if current_color == "blanco":
            distance = dest - origin
        else:
            distance = origin - dest
        
        if distance != dice_value:
            return False
        
        # Verificar que el destino sea válido (dentro del tablero)
        if dest < 1 or dest > 24:
            return False
        
        # Verificar que el destino no esté bloqueado
        dest_count = self.__board.point_count(dest)
        
        # Si el destino está vacío, el movimiento es válido
        if dest_count == 0:
            return True
        
        # Si hay fichas en el destino, verificar las reglas de Backgammon
        dest_checker = self.__board.get_top_checker(dest)
        
        if dest_checker is None:
            return True
        
        if dest_checker.get_color() == current_color:
            # Destino tiene fichas propias, se puede mover
            return True
        else:
            # Destino tiene fichas del oponente
            # Solo es válido si hay exactamente 1 (se puede capturar)
            return dest_count == 1


class TurnManager:
    """
    SRP: Responsabilidad única de gestionar turnos entre jugadores.
    
    Maneja el cambio de turno y seguimiento del jugador actual.
    """
    
    def __init__(self, players: List[Player]):
        self.__players = players
        self.__current_index = 0
    
    def get_players(self) -> List[Player]:
        """Getter de la lista de jugadores."""
        return self.__players
    
    def set_players(self, players: List[Player]) -> None:
        """Setter de la lista de jugadores."""
        self.__players = players
    
    def get_current_index(self) -> int:
        """Getter del índice del jugador actual."""
        return self.__current_index
    
    def set_current_index(self, index: int) -> None:
        """Setter del índice del turno actual."""
        if not (0 <= index < len(self.__players)):
            raise IndexError("Índice de jugador fuera de rango")
        self.__current_index = index
    
    def get_current_player(self) -> Player:
        """Retorna el jugador que tiene el turno actual."""
        return self.__players[self.__current_index]
    
    def next_turn(self) -> Player:
        """Avanza al siguiente jugador y lo retorna."""
        self.__current_index = (self.__current_index + 1) % len(self.__players)
        return self.get_current_player()


class VictoryChecker:
    """
    SRP: Responsabilidad única de verificar condiciones de victoria.
    
    Determina si el juego ha terminado y quién es el ganador.
    """
    
    def __init__(self, board: Board, players: List[Player]):
        self.__board = board
        self.__players = players
    
    def get_board(self) -> Board:
        """Getter del tablero."""
        return self.__board
    
    def set_board(self, board: Board) -> None:
        """Setter del tablero."""
        self.__board = board
    
    def get_players(self) -> List[Player]:
        """Getter de la lista de jugadores."""
        return self.__players
    
    def set_players(self, players: List[Player]) -> None:
        """Setter de la lista de jugadores."""
        self.__players = players
    
    def is_game_over(self) -> bool:
        """
        Verifica si el juego ha terminado.
        El juego termina cuando un jugador sacó todas sus fichas (bear off completo).
        
        Returns:
            True si el juego terminó
        """
        for player in self.__players:
            if self.__board.has_won(player.get_color()):
                return True
        return False
    
    def get_winner(self) -> Optional[Player]:
        """
        Obtiene el ganador del juego.
        
        Returns:
            El jugador ganador, o None si no hay ganador aún
        """
        for player in self.__players:
            if self.__board.has_won(player.get_color()):
                return player
        return None


class GameFacade:
    """
    Facade Pattern: Proporciona una interfaz simplificada siguiendo SOLID.
    
    Esta clase coordina las responsabilidades separadas:
    - MoveValidator: valida movimientos
    - TurnManager: gestiona turnos
    - VictoryChecker: verifica victoria
    
    Internamente usa la clase Game original para mantener compatibilidad,
    pero expone una interfaz que respeta los principios SOLID.
    
    DIP (Dependency Inversion): Acepta dependencias inyectadas en el constructor.
    """
    
    def __init__(
        self,
        player1: Player,
        player2: Player,
        board: Optional[Board] = None,
        dice: Optional[Dice] = None,
        validator: Optional[MoveValidator] = None,
        turn_manager: Optional[TurnManager] = None,
        victory_checker: Optional[VictoryChecker] = None
    ):
        """
        Inicializa el juego con inyección de dependencias (DIP).
        
        Args:
            player1: Primer jugador
            player2: Segundo jugador
            board: Tablero (si es None, crea uno nuevo)
            dice: Dados (si es None, crea unos nuevos)
            validator: Validador de movimientos (si es None, crea uno)
            turn_manager: Gestor de turnos (si es None, crea uno)
            victory_checker: Verificador de victoria (si es None, crea uno)
        """
        # Usar Game original internamente para no romper funcionalidad existente
        self.__game = Game(player1, player2, board=board, dice=dice)
        
        # Inyección de dependencias (DIP)
        self.__validator = validator or MoveValidator(
            self.__game.get_board(),
            self.__game.get_current_player()
        )
        
        self.__turn_manager = turn_manager or TurnManager(
            self.__game.get_players()
        )
        
        self.__victory_checker = victory_checker or VictoryChecker(
            self.__game.get_board(),
            self.__game.get_players()
        )
    
    # ========== Getters y Setters de componentes SOLID ==========
    
    def get_validator(self) -> MoveValidator:
        """Getter del validador de movimientos."""
        return self.__validator
    
    def set_validator(self, validator: MoveValidator) -> None:
        """Setter del validador de movimientos."""
        self.__validator = validator
    
    def get_turn_manager(self) -> TurnManager:
        """Getter del gestor de turnos."""
        return self.__turn_manager
    
    def set_turn_manager(self, turn_manager: TurnManager) -> None:
        """Setter del gestor de turnos."""
        self.__turn_manager = turn_manager
    
    def get_victory_checker(self) -> VictoryChecker:
        """Getter del verificador de victoria."""
        return self.__victory_checker
    
    def set_victory_checker(self, victory_checker: VictoryChecker) -> None:
        """Setter del verificador de victoria."""
        self.__victory_checker = victory_checker
    
    # ========== Delegación a componentes SOLID ==========
    
    def is_valid_move(self, origin: int, dest: int, dice_value: int) -> bool:
        """Usa el validador SOLID para verificar movimientos."""
        # Actualizar validador con jugador actual
        self.__validator.set_current_player(self.get_current_player())
        return self.__validator.is_valid_move(origin, dest, dice_value)
    
    def next_turn(self) -> Player:
        """Usa el gestor de turnos SOLID."""
        # Sincronizar con Game interno
        result = self.__turn_manager.next_turn()
        self.__game.set_current_index(self.__turn_manager.get_current_index())
        return result
    
    def is_game_over(self) -> bool:
        """Usa el verificador de victoria SOLID."""
        return self.__victory_checker.is_game_over()
    
    def get_winner(self) -> Optional[Player]:
        """Usa el verificador de victoria SOLID."""
        return self.__victory_checker.get_winner()
    
    # ========== Delegación directa a Game original ==========
    # (Mantiene compatibilidad con código existente)
    
    def get_board(self) -> Board:
        """Retorna el tablero."""
        return self.__game.get_board()
    
    def get_dice(self) -> Dice:
        """Retorna los dados."""
        return self.__game.get_dice()
    
    def get_players(self) -> List[Player]:
        """Retorna la lista de jugadores."""
        return self.__game.get_players()
    
    def get_current_player(self) -> Player:
        """Retorna el jugador actual."""
        # Sincronizar índices
        game_index = self.__game.get_current_index()
        if game_index != self.__turn_manager.get_current_index():
            self.__turn_manager.set_current_index(game_index)
        return self.__turn_manager.get_current_player()
    
    def get_current_index(self) -> int:
        """Retorna el índice del jugador actual."""
        return self.__turn_manager.get_current_index()
    
    def roll(self) -> List[int]:
        """Tira los dados."""
        return self.__game.roll()
    
    def move(self, origin: int, dest: int) -> None:
        """Ejecuta un movimiento."""
        self.__game.move(origin, dest)
    
    def get_score(self) -> dict:
        """Retorna el marcador."""
        return self.__game.get_score()
    
    def add_score(self, player: Player, points: int = 1) -> None:
        """Suma puntos al marcador."""
        self.__game.add_score(player, points)
    
    def add_points(self, player: Player, points: int = 1) -> None:
        """Alias de add_score."""
        self.__game.add_points(player, points)
    
    def get_history(self) -> List[dict]:
        """Retorna el historial de tiradas."""
        return self.__game.get_history()
    
    def get_roll_history(self) -> List[dict]:
        """Retorna el historial de tiradas."""
        return self.__game.get_roll_history()
    
    def last_roll(self) -> Optional[List[int]]:
        """Retorna la última tirada."""
        return self.__game.last_roll()
    
    def reset(self) -> None:
        """Reinicia el juego."""
        self.__game.reset()
        self.__turn_manager.set_current_index(0)
    
    def swap_players(self) -> None:
        """Intercambia el orden de jugadores."""
        self.__game.swap_players()
        self.__turn_manager.set_players(self.__game.get_players())
        self.__turn_manager.set_current_index(0)
    
    def set_board(self, board: Board) -> None:
        """Establece un nuevo tablero."""
        self.__game.set_board(board)
        self.__validator.set_board(board)
        self.__victory_checker.set_board(board)
    
    def set_dice(self, dice: Dice) -> None:
        """Establece nuevos dados."""
        self.__game.set_dice(dice)
    
    def set_current_index(self, idx: int) -> None:
        """Establece el índice del turno."""
        self.__game.set_current_index(idx)
        self.__turn_manager.set_current_index(idx)
    
    def can_bear_off(self, player: Player) -> bool:
        """Verifica si puede hacer bear off."""
        return self.__game.can_bear_off(player)
    
    def is_home_board_loaded(self, player: Player) -> bool:
        """Verifica si todas las fichas están en home board."""
        return self.__game.is_home_board_loaded(player)
    
    # ========== Properties para compatibilidad ==========
    
    @property
    def players(self) -> List[Player]:
        """Property para acceso a jugadores."""
        return self.__game.players
    
    @property
    def board(self) -> Board:
        """Property para acceso al tablero."""
        return self.__game.board
    
    @property
    def dice(self) -> Dice:
        """Property para acceso a los dados."""
        return self.__game.dice
    
    @property
    def current_player(self) -> Player:
        """Property para acceso al jugador actual."""
        return self.get_current_player()
    
    def change_turn(self) -> None:
        """Alias de next_turn para compatibilidad."""
        self.next_turn()
    
    # ========== Representación ==========
    
    def __repr__(self) -> str:
        return f"GameFacade(current={self.get_current_player()!r}, SOLID=True)"
    
    def __str__(self) -> str:
        current = self.get_current_player().get_nombre()
        scores = ", ".join([f"{k}: {v}" for k, v in self.get_score().items()])
        return f"[SOLID] Turno de {current} | Marcador: {scores}"