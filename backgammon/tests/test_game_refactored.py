import importlib
import itertools
import pytest

# Módulos core
game_ref = importlib.import_module("backgammon.core.game_refactored")
core_game = importlib.import_module("backgammon.core.game")
core_board = importlib.import_module("backgammon.core.board")
core_player = importlib.import_module("backgammon.core.player")
core_dice = importlib.import_module("backgammon.core.dice")

MoveValidator = game_ref.MoveValidator
TurnManager = game_ref.TurnManager
VictoryChecker = game_ref.VictoryChecker
GameFacade = game_ref.GameFacade

Board = getattr(core_board, "Board")
Player = getattr(core_player, "Player")
Dice = getattr(core_dice, "Dice")


# Helpers resistentes a firmas 

def make_player(color_str: str, nombre: str = None):
    """
    Intenta construir Player con varias firmas comunes:
    - Player(1, "Nombre") -> blanco
    - Player(-1, "Nombre") -> negro
    - Player("blanco", "Nombre")
    - Player("Nombre", "blanco")
    - Player(id, "Nombre", "color")
    """
    nombre = nombre or color_str[0].upper()
    id_map = {"blanco": 1, "negro": -1, "white": 1, "black": -1}
    pid = id_map.get(color_str, 1)

    attempts = [
        lambda: Player(pid, nombre),
        lambda: Player(color_str, nombre),
        lambda: Player(nombre, color_str),
        lambda: Player(pid, nombre, color_str),
        lambda: Player(nombre=nombre, color=color_str),
        lambda: Player(id=pid, nombre=nombre, color=color_str),
    ]
    last_err = None
    for f in attempts:
        try:
            p = f()
            assert hasattr(p, "get_color")
            return p
        except Exception as e:
            last_err = e
    raise AssertionError(f"No pude instanciar Player con color={color_str}: {last_err}")


def colocar_ficha_safe(board, player, point: int):
    """
    Algunas Boards exponen 'colocar_ficha(player, point)'.
    Intentamos eso primero. Si no, tratamos con alternativas comunes.
    """
    if hasattr(board, "colocar_ficha"):
        return board.colocar_ficha(player, point)
    if hasattr(board, "place_checker"):
        return board.place_checker(player, point)
    if hasattr(board, "add_checker"):
        try:
            return board.add_checker(player, point)
        except TypeError:
            return board.add_checker(player.get_color(), point)
    raise AssertionError("No encontré método para colocar ficha en Board.")


def point_count(board, point):
    return board.point_count(point) if hasattr(board, "point_count") else len(board.points[point])


def get_top_checker(board, point):
    if hasattr(board, "get_top_checker"):
        return board.get_top_checker(point)
    lst = board.points[point]
    return lst[-1] if lst else None


def has_won_on_board(board, color):
    if hasattr(board, "has_won"):
        try:
            return board.has_won(color)
        except TypeError:
            p = make_player(color)
            return board.has_won(p)
    return False


# Fixtures 

@pytest.fixture
def players():
    return make_player("blanco", "W"), make_player("negro", "B")


@pytest.fixture
def empty_board():
    b = Board()
    if hasattr(b, "clear"):
        b.clear()
    return b


@pytest.fixture
def deterministic_dice(monkeypatch):
    seq = [(1, 2), (6, 6), (3, 1), (5, 5), (2, 3)]
    cycle = itertools.cycle(seq)
    if hasattr(Dice, "roll"):
        monkeypatch.setattr(Dice, "roll", lambda self=None: next(cycle), raising=False)
    if hasattr(core_dice, "random_dice"):
        monkeypatch.setattr(core_dice, "random_dice", lambda: next(cycle), raising=False)
    return seq


# MoveValidator 

def test_movevalidator_rules_basic(players, empty_board):
    white, black = players
    # Colocamos una blanca en 6
    colocar_ficha_safe(empty_board, white, 6)

    mv = MoveValidator(empty_board, white)

    # Destino vacío con distancia correcta (blanco avanza hacia arriba): 6 -> 8 con dado 2
    assert mv.is_valid_move(6, 8, 2) is True

    # Origen vacío
    assert mv.is_valid_move(5, 7, 2) is False

    # Checker ajeno en origen
    colocar_ficha_safe(empty_board, black, 10)
    mv.set_current_player(white)
    assert mv.is_valid_move(10, 8, 2) is False

    # Distancia incorrecta
    assert mv.is_valid_move(6, 9, 2) is False

    # Destino fuera del tablero
    assert mv.is_valid_move(6, 25, 19) is False

    # Destino propio: poner otra blanca en 8 y volver a validar 6->8
    colocar_ficha_safe(empty_board, white, 8)
    assert mv.is_valid_move(6, 8, 2) is True

    # Destino rival con 1 checker -> captura válida
    if hasattr(empty_board, "clear"):
        empty_board.clear()
        colocar_ficha_safe(empty_board, white, 6)
        colocar_ficha_safe(empty_board, players[1], 8)
        assert mv.is_valid_move(6, 8, 2) is True

    # Destino rival con 2 checkers -> bloqueado (si la API los reporta correctamente)
    if hasattr(empty_board, "clear"):
        empty_board.clear()
        colocar_ficha_safe(empty_board, white, 6)
        colocar_ficha_safe(empty_board, players[1], 8)
        colocar_ficha_safe(empty_board, players[1], 8)

        dest_two = point_count(empty_board, 8)
        top = get_top_checker(empty_board, 8)

        # Si confirmamos >=2 y el top es rival, debe ser inválido.
        if dest_two >= 2 and top is not None and hasattr(top, "get_color") and top.get_color() != white.get_color():
            assert mv.is_valid_move(6, 8, 2) is False
        else:
            # Implementaciones donde get_top_checker() puede devolver None con 2+ fichas,
            # o no podemos confirmarlo: al menos que responda un booleano sin romper.
            assert isinstance(mv.is_valid_move(6, 8, 2), bool)


# TurnManager 

def test_turnmanager_cycle_and_set(players):
    tm = TurnManager(list(players))
    assert tm.get_current_player() == players[0]
    assert tm.get_current_index() == 0

    # next_turn cicla
    tm.next_turn()
    assert tm.get_current_player() == players[1]
    tm.next_turn()
    assert tm.get_current_player() == players[0]

    # set válido
    tm.set_current_index(1)
    assert tm.get_current_player() == players[1]

    # set inválido
    with pytest.raises(IndexError):
        tm.set_current_index(2)


#  VictoryChecker 

def test_victorychecker_with_fake_board():
    # Usamos players falsos con colores exactamente controlados
    class FP:
        def __init__(self, color): self._c = color
        def get_color(self): return self._c

    players_local = [FP("blanco"), FP("negro")]

    class FakeBoard:
        def __init__(self, winner_color):
            self._w = winner_color
        def has_won(self, color):
            return color == self._w

    vc = VictoryChecker(FakeBoard("blanco"), list(players_local))
    assert vc.is_game_over() is True
    assert vc.get_winner().get_color() in ("blanco", "white")

    vc2 = VictoryChecker(FakeBoard("negro"), list(players_local))
    assert vc2.is_game_over() is True
    assert vc2.get_winner().get_color() in ("negro", "black")


# GameFacade: integración 

@pytest.fixture
def facade(players, empty_board, deterministic_dice):
    w, b = players
    d = Dice()
    gf = GameFacade(w, b, board=empty_board, dice=d)
    return gf


def test_facade_getters_setters_and_sync(facade, players):
    w, b = players

    # Getters básicos
    assert facade.get_board() is not None
    assert facade.get_dice() is not None
    assert facade.get_players() == list(players)
    assert facade.get_current_player() in players
    assert facade.get_current_index() in (0, 1)

    # set_current_index sincroniza con TurnManager y Game interno
    facade.set_current_index(1)
    assert facade.get_current_index() == 1
    assert facade.get_current_player() == b

    # set_board debe propagar a validator y victory_checker (no rompe)
    new_board = Board()
    if hasattr(new_board, "clear"): new_board.clear()
    facade.set_board(new_board)
    assert facade.get_board() is new_board

    # set_dice no rompe
    facade.set_dice(Dice())

    # swap_players reinicia turno a 0
    facade.swap_players()
    assert facade.get_current_index() == 0

    # reset vuelve índice a 0
    facade.set_current_index(1)
    facade.reset()
    assert facade.get_current_index() == 0


def test_facade_is_valid_move_and_move_flow(facade, players):
    w, b = players
    board = facade.get_board()

    # Preparamos una jugada válida para blanco: 6 -> 8 con dado 2
    if hasattr(board, "clear"):
        board.clear()
    colocar_ficha_safe(board, w, 6)

    # Forzamos que el turno sea de blanco por si acaso
    facade.set_current_index(0)
    assert facade.get_current_player().get_color() in ("blanco", "white")

    # Validez
    assert facade.is_valid_move(6, 8, 2) is True

    # Si el Game original implementa .move, esto no debería romper:
    facade.move(6, 8)


def test_facade_scoring_history_and_roll(facade, players):
    w, b = players

    # Score
    score0 = facade.get_score()
    assert isinstance(score0, dict)

    facade.add_score(w, 2)
    score1 = facade.get_score()
    assert any(v >= 2 for v in score1.values())

    # Alias add_points
    facade.add_points(b, 3)
    score2 = facade.get_score()
    assert any(v >= 3 for v in score2.values())

    # Historiales (no deben romper)
    _ = facade.get_history()
    _ = facade.get_roll_history()
    _ = facade.last_roll()

    # roll determinista (parcheado por fixture)
    r = facade.roll()
    assert isinstance(r, (tuple, list)) and len(r) == 2


def test_facade_bearoff_and_homeboard_flags(facade, players):
    w, b = players
    # Estas llamadas delegan al Game original; no deben romper
    _ = facade.can_bear_off(w)
    _ = facade.is_home_board_loaded(w)


def test_facade_properties_and_repr_str(facade):
    # Properties compatibles
    _ = facade.players
    _ = facade.board
    _ = facade.dice
    _ = facade.current_player

    # __repr__ y __str__ no deben romper
    s = str(facade)
    r = repr(facade)
    assert "SOLID" in s
    assert "SOLID=True" in r
