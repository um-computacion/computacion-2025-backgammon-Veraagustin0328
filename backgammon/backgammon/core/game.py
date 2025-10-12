from __future__ import annotations
from typing import List, Optional, Dict, Any

from .player import Player
from .board import Board
from .dice import Dice


class Game:
    """
    Orquesta una partida entre dos jugadores.
    No mete reglas pesadas (golpes, bloqueos, borne-off); eso se puede hacer aparte.
    Acá coordinamos: jugadores, tablero, dados y turnos + historial simple
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        board: Optional[Board] = None,
        dice: Optional[Dice] = None,
    ) -> None:
        # Inyección de dependencias (DIP): si no me pasan, creo defaults
        self.players: List[Player] = [player1, player2]
        self.board: Board = board if board is not None else Board()
        self.dice: Dice = dice if dice is not None else Dice()

        # Turno actual: 0 o 1. Si hay más de 2 jugadores, esto igual funciona
        self._current_index: int = 0

        # Un historial para ver qué pasó
        self._roll_history: List[Dict[str, Any]] = []

        # Un marcador mínimo por si lo queremos usar (no obligatorio para backgammon estándar)
        self._score: Dict[str, int] = {self.players[0].name: 0, self.players[1].name: 0}

    

    @property
    def current_player(self) -> Player:
        """Devuelve el jugador que tiene el turno """
        return self.players[self._current_index]

    def next_turn(self) -> Player:
        """Pasa el turno al siguiente jugador y lo devuelve """
        self._current_index = (self._current_index + 1) % len(self.players)
        return self.current_player

    def set_current_index(self, idx: int) -> None:
        """Fuerza el índice de turno (para tests o reinicio ordenado) """
        if not (0 <= idx < len(self.players)):
            raise IndexError("Índice de jugador fuera de rango ")
        self._current_index = idx

    
    def roll(self) -> List[int]:
        """
        Tira los dados del juego y devuelve los valores.
        También registra la tirada en un historial minimalista
        """
        values = self.dice.roll()
        self._roll_history.append(
            {"player": self.current_player.name, "values": list(values)}  # copiamos por las dudas
        )
        return values

    def last_roll(self) -> Optional[List[int]]:
        """Devuelve la última tirada (si es que hubo) """
        if not self._roll_history:
            return None
        return list(self._roll_history[-1]["values"])

  

    def add_score(self, player: Player, points: int = 1) -> None:
        """Suma puntos al marcador. Sencillo, para mostrar algo de estado acumulado """
        self._score.setdefault(player.name, 0)
        self._score[player.name] += int(points)

    def get_score(self) -> Dict[str, int]:
        """Devuelve una copia del marcador"""
        return dict(self._score)

    

    def reset(self) -> None:
        """Reinicia tablero, limpia historial y vuelve turno al primer jugador """
        self.board = Board()
        self._roll_history.clear()
        self.set_current_index(0)

    def swap_players(self) -> None:
        """Intercambia el orden de los jugadores (por si queremos que empiece el otro) """
        self.players[0], self.players[1] = self.players[1], self.players[0]
        # Ajustamos score para que los nombres sigan matcheando
        self._score = {self.players[0].name: self._score.get(self.players[0].name, 0),
                       self.players[1].name: self._score.get(self.players[1].name, 0)}
        # Recalibramos índice (mantengo 0 como “el que arranca”)
        self.set_current_index(0)

    def set_board(self, board: Board) -> None:
        """Reemplaza el board actual por otro (validación básica) """
        if not isinstance(board, Board):
            raise TypeError("board debe ser instancia de Board")
        self.board = board

    def set_dice(self, dice: Dice) -> None:
        """Reemplaza los dados actuales por otros """
        if not isinstance(dice, Dice):
            raise TypeError("dice debe ser instancia de Dice")
        self.dice = dice

    def set_players(self, p1: Player, p2: Player) -> None:
        """Permite configurar jugadores de nuevo (por ejemplo, renombrados) """
        if not isinstance(p1, Player) or not isinstance(p2, Player):
            raise TypeError("p1 y p2 deben ser Player")
        self.players = [p1, p2]
        # Mantengo marcador por nombre:
        self._score = {p1.name: self._score.get(p1.name, 0), p2.name: self._score.get(p2.name, 0)}
        self.set_current_index(0)

    

    def to_dict(self) -> Dict[str, Any]:
        """Estado mínimo serializable (no pretende ser formato final del juego) """
        return {
            "players": [p.to_dict() for p in self.players],
            "current_index": self._current_index,
            "score": dict(self._score),
            "last_roll": self.last_roll(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Game":
        """Reconstrucción mínima; tablero nuevo y dados default (simple) """
        pdata = data.get("players", [{"name": "A", "color": "blanco"}, {"name": "B", "color": "negro"}])
        p1 = Player.from_dict(pdata[0])
        p2 = Player.from_dict(pdata[1])
        game = cls(p1, p2, board=None, dice=None)
        idx = int(data.get("current_index", 0))
        game.set_current_index(idx if idx in (0, 1) else 0)
        # score
        score = data.get("score", {})
        game._score = {p1.name: int(score.get(p1.name, 0)), p2.name: int(score.get(p2.name, 0))}
        return game

   

    def __repr__(self) -> str:
        return (
            f"Game(current={self.current_player!r}, "
            f"board=Board(points={len(self.board.points)}), "
            f"score={self._score})"
        )


