from __future__ import annotations
from typing import List, Optional, Dict, Any

from .player import Player
from .board import Board
from .dice import Dice


class Game:
    """
    Orquesta una partida entre dos jugadores
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        board: Optional[Board] = None,
        dice: Optional[Dice] = None,
    ) -> None:
        self.__players: List[Player] = [player1, player2]
        self.__board: Board = board if board is not None else Board()
        self.__dice: Dice = dice if dice is not None else Dice()
        self.__current_index: int = 0
        self.__roll_history: List[Dict[str, Any]] = []
        self.__score: Dict[str, int] = {
            self.__players[0].get_nombre(): 0, 
            self.__players[1].get_nombre(): 0
        }

    def get_players(self) -> List[Player]:
        """Devuelve la lista de jugadores"""
        return self.__players

    def get_board(self) -> Board:
        """Devuelve el tablero actual"""
        return self.__board

    def get_dice(self) -> Dice:
        """Devuelve los dados actuales"""
        return self.__dice

    def get_current_index(self) -> int:
        """Devuelve el índice del jugador actual"""
        return self.__current_index

    def get_roll_history(self) -> List[Dict[str, Any]]:
        """Devuelve el historial de tiradas"""
        return self.__roll_history.copy()

    @property
    def players(self) -> List[Player]:
        """Property para acceso a jugadores (compatibilidad)"""
        return self.__players

    @property
    def board(self) -> Board:
        """Property para acceso al tablero (compatibilidad)"""
        return self.__board

    @property
    def dice(self) -> Dice:
        """Property para acceso a los dados (compatibilidad)"""
        return self.__dice

    @property
    def current_player(self) -> Player:
        """Devuelve el jugador que tiene el turno"""
        return self.__players[self.__current_index]

    def next_turn(self) -> Player:
        """Pasa el turno al siguiente jugador y lo devuelve"""
        self.__current_index = (self.__current_index + 1) % len(self.__players)
        return self.current_player

    def set_current_index(self, idx: int) -> None:
        """Fuerza el índice de turno (para tests o reinicio ordenado)"""
        if not (0 <= idx < len(self.__players)):
            raise IndexError("Índice de jugador fuera de rango")
        self.__current_index = idx

    def roll(self) -> List[int]:
        """
        Tira los dados del juego y devuelve los valores.
        También registra la tirada en un historial minimalista
        """
        values = list(self.__dice.roll())
        self.__roll_history.append({
            "player": self.current_player.get_nombre(), 
            "values": values.copy()
        })
        return values

    def last_roll(self) -> Optional[List[int]]:
        """Devuelve la última tirada (si es que hubo)"""
        if not self.__roll_history:
            return None
        return list(self.__roll_history[-1]["values"])

    def add_score(self, player: Player, points: int = 1) -> None:
        """Suma puntos al marcador. Sencillo, para mostrar algo de estado acumulado"""
        nombre = player.get_nombre()
        self.__score.setdefault(nombre, 0)
        self.__score[nombre] += int(points)

    def get_score(self) -> Dict[str, int]:
        """Devuelve una copia del marcador"""
        return dict(self.__score)

    def reset(self) -> None:
        """Reinicia tablero, limpia historial y vuelve turno al primer jugador"""
        self.__board = Board()
        self.__roll_history.clear()
        self.set_current_index(0)

    def swap_players(self) -> None:
        """Intercambia el orden de los jugadores (por si queremos que empiece el otro)"""
        self.__players[0], self.__players[1] = self.__players[1], self.__players[0]
        nombre0 = self.__players[0].get_nombre()
        nombre1 = self.__players[1].get_nombre()
        self.__score = {
            nombre0: self.__score.get(nombre0, 0),
            nombre1: self.__score.get(nombre1, 0)
        }
        self.set_current_index(0)

    def set_board(self, board: Board) -> None:
        """Reemplaza el board actual por otro (validación básica)"""
        if not isinstance(board, Board):
            raise TypeError("board debe ser instancia de Board")
        self.__board = board

    def set_dice(self, dice: Dice) -> None:
        """Reemplaza los dados actuales por otros"""
        if not isinstance(dice, Dice):
            raise TypeError("dice debe ser instancia de Dice")
        self.__dice = dice

    def set_players(self, p1: Player, p2: Player) -> None:
        """Permite configurar jugadores de nuevo (por ejemplo, renombrados)"""
        if not isinstance(p1, Player) or not isinstance(p2, Player):
            raise TypeError("p1 y p2 deben ser Player")
        self.__players = [p1, p2]
        nombre1 = p1.get_nombre()
        nombre2 = p2.get_nombre()
        self.__score = {
            nombre1: self.__score.get(nombre1, 0), 
            nombre2: self.__score.get(nombre2, 0)
        }
        self.set_current_index(0)

    def to_dict(self) -> Dict[str, Any]:
        """Estado mínimo serializable (no pretende ser formato final del juego)"""
        return {
            "players": [p.to_dict() for p in self.__players],
            "current_index": self.__current_index,
            "score": dict(self.__score),
            "last_roll": self.last_roll(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Game":
        """Reconstrucción mínima; tablero nuevo y dados default (simple)"""
        pdata = data.get("players", [{"nombre": "A"}, {"nombre": "B"}])
        p1 = Player.from_dict(pdata[0])
        p2 = Player.from_dict(pdata[1])
        game = cls(p1, p2, board=None, dice=None)
        idx = int(data.get("current_index", 0))
        game.set_current_index(idx if idx in (0, 1) else 0)
        score = data.get("score", {})
        nombre1 = p1.get_nombre()
        nombre2 = p2.get_nombre()
        game._Game__score = {
            nombre1: int(score.get(nombre1, 0)), 
            nombre2: int(score.get(nombre2, 0))
        }
        return game

    def __repr__(self) -> str:
        return (
            f"Game(current={self.current_player!r}, "
            f"board=Board(...), "
            f"score={self.__score})"
        )
