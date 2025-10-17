from __future__ import annotations
from typing import List, Dict, Any, Optional
from backgammon.backgammon.core.player import Player
from backgammon.backgammon.core.board import Board
from backgammon.backgammon.core.dice import Dice


class Game:
    """
    Clase principal del juego de Backgammon.
    Aplica principios SOLID:
    - SRP: gestiona flujo del juego.
    - OCP/DIP: permite inyectar Board y Dice.
    - LSP: compatible con subclases de Player/Dice.
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
            self.__players[1].get_nombre(): 0,
        }

    # ---------- GETTERS ----------
    def get_players(self) -> List[Player]:
        return self.__players

    def get_board(self) -> Board:
        return self.__board

    def get_dice(self) -> Dice:
        return self.__dice

    def get_current_player(self) -> Player:
        return self.__players[self.__current_index]

    def get_history(self) -> List[Dict[str, Any]]:
        return self.__roll_history

    def get_score(self) -> Dict[str, int]:
        return self.__score

    def get_current_index(self) -> int:
        """Devuelve el índice del jugador actual (0 o 1)."""
        return self.__current_index

    # ---------- PROPERTIES ----------
    @property
    def current_player(self) -> Player:
        """Permite acceder como g.current_player"""
        return self.get_current_player()

    # ---------- LÓGICA PRINCIPAL ----------
    def roll_dice(self) -> tuple[int, int]:
        result = self.__dice.roll()
        self.__roll_history.append(
            {"player": self.get_current_player().get_nombre(), "roll": result}
        )
        return result

    def roll(self) -> list[int]:
        r = self.roll_dice()
        return [r[0], r[1]]

    def change_turn(self) -> None:
        """Cambia el turno al otro jugador."""
        self.__current_index = 1 - self.__current_index

    # Alias para compatibilidad con tests
    def next_turn(self) -> None:
        """Alias de change_turn()."""
        self.change_turn()

    def add_points(self, player: Player, puntos: int) -> None:
        nombre = player.get_nombre()
        if nombre not in self.__score:
            raise ValueError(f"Jugador '{nombre}' no pertenece a la partida.")
        self.__score[nombre] += int(puntos)

    # Alias de add_points
    def add_score(self, player: Player, puntos: int) -> None:
        """Alias para compatibilidad con tests."""
        self.add_points(player, puntos)

    # ---------- SERIALIZACIÓN ----------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "players": [p.to_dict() for p in self.__players],
            "current_index": self.__current_index,
            "score": self.__score,
            "history": self.__roll_history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Game:
        players_data = data.get("players", [])
        if len(players_data) < 2:
            raise ValueError("Se requieren al menos dos jugadores en los datos.")
        p1 = Player.from_dict(players_data[0])
        p2 = Player.from_dict(players_data[1])

        g = cls(p1, p2)
        g.__current_index = data.get("current_index", 0)
        g.__score = data.get("score", g.__score)
        g.__roll_history = data.get("history", [])
        return g

    # ---------- REPRESENTACIONES ----------
    def __repr__(self) -> str:
        return f"Game({self.__players[0]}, {self.__players[1]}, turno={self.__current_index})"

    def __str__(self) -> str:
        jugador = self.get_current_player().get_nombre()
        return f"Turno de {jugador}. Marcador: {self.__score}"
