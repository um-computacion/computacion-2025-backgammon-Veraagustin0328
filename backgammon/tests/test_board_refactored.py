import importlib
import pytest

# Cargamos el módulo de la implementación SOLID
br = importlib.import_module("backgammon.core.board_refactored")

# Clases a testear
BoardPoints = br.BoardPoints
BarManager = br.BarManager
BearOffManager = br.BearOffManager
CaptureRules = br.CaptureRules
BoardValidator = br.BoardValidator
BoardFacade = br.BoardFacade
BoardWithSetupFacade = br.BoardWithSetupFacade

# Utilidades para el test 

class FakePlayer:
    """Jugador mínimo para tests: sólo necesita get_color()."""
    def __init__(self, color: str, nombre: str = ""):
        self._color = color
        self.nombre = nombre or color
    def get_color(self) -> str:
        return self._color
    def __repr__(self):
        return f"FakePlayer(color={self._color})"

@pytest.fixture
def players():
    return FakePlayer("blanco", "W"), FakePlayer("negro", "B")

@pytest.fixture
def neutralize_original_board(monkeypatch):
    """
    BoardFacade.colocar_ficha llama internamente a Board().colocar_ficha().
    Para no depender de la implementación clásica, la neutralizamos.
    """
    board_mod = importlib.import_module("backgammon.core.board")

    # Si existe la clase Board y el método colocar_ficha, parcheamos a no-op.
    if hasattr(board_mod, "Board"):
        if hasattr(board_mod.Board, "colocar_ficha"):
            monkeypatch.setattr(board_mod.Board, "colocar_ficha", lambda self, player, point: None, raising=True)
    yield


#  TESTS DE COMPONENTES BÁSICOS 

def test_boardpoints_basic_ops():
    p = BoardPoints()

    # Fuera de rango
    assert p.get_point(0) == []
    assert p.get_point(25) == []
    assert p.point_count(0) == 0
    assert p.get_top_checker(0) is None

    # Operaciones válidas
    dummy_checker = object()
    p.add_checker_to_point(5, dummy_checker)
    assert p.point_count(5) == 1
    assert p.get_top_checker(5) is dummy_checker

    popped = p.remove_checker_from_point(5)
    assert popped is dummy_checker
    assert p.point_count(5) == 0

    # Errores esperables
    with pytest.raises(ValueError):
        p.add_checker_to_point(26, object())
    with pytest.raises(ValueError):
        p.remove_checker_from_point(7)  # no hay fichas

    # clear
    p.add_checker_to_point(10, object())
    p.clear()
    assert all(len(lst) == 0 for lst in p.get_points())


def test_bar_manager_ops(players):
    bar = BarManager()
    w, b = players

    # Vacía al inicio
    assert bar.get_bar() == []
    assert bar.get_bar_count("blanco") == 0

    # Agregar de ambos colores
    class Ck:
        def __init__(self, color): self._c = color
        def get_color(self): return self._c
    bar.add_to_bar(Ck("blanco"))
    bar.add_to_bar(Ck("negro"))
    bar.add_to_bar(Ck("blanco"))
    assert bar.get_bar_count("blanco") == 2
    assert bar.get_bar_count("negro") == 1

    # remove_by_color quita la primera que matchee
    ck = bar.remove_from_bar("blanco")
    assert ck is not None and ck.get_color() == "blanco"
    assert bar.get_bar_count("blanco") == 1

    # clear
    bar.clear()
    assert bar.get_bar() == []


def test_bearoff_manager_ops():
    bo = BearOffManager()
    assert bo.get_off_count("blanco") == 0
    assert bo.has_won("blanco") is False

    for _ in range(15):
        bo.bear_off_checker("blanco")
    assert bo.get_off_count("blanco") == 15
    assert bo.has_won("blanco") is True

    # reset
    bo.clear()
    assert bo.get_off_count("blanco") == 0


def test_capture_rules_should_and_execute():
    points = BoardPoints()
    bar = BarManager()

    # Creamos reglas y una mini clase Checker con color
    rules = CaptureRules(points, bar)
    class Ck:
        def __init__(self, color): self._c = color
        def get_color(self): return self._c

    # Caso 1: destino vacío => no captura
    assert rules.should_capture(6, Ck("blanco")) is False

    # Caso 2: destino con 1 checker del MISMO color => no captura
    points.add_checker_to_point(6, Ck("blanco"))
    assert rules.should_capture(6, Ck("blanco")) is False

    # Caso 3: destino con 1 checker de color opuesto => captura
    points.clear()
    points.add_checker_to_point(6, Ck("negro"))
    assert rules.should_capture(6, Ck("blanco")) is True

    # Ejecutar captura: debe mover la ficha a la barra
    rules.execute_capture(6)
    assert points.point_count(6) == 0
    assert bar.get_bar_count("negro") == 1


def test_board_validator_rules():
    points = BoardPoints()
    v = BoardValidator(points)

    # Fuera de rango
    assert v.can_place_checker(0, "blanco") is False

    # Punto vacío: se puede
    assert v.can_place_checker(5, "blanco") is True
    assert v.is_empty(5) is True
    assert v.get_point_color(5) is None

    # Mismo color, se puede apilar
    class Ck:
        def __init__(self, color): self._c = color
        def get_color(self): return self._c
    points.add_checker_to_point(5, Ck("blanco"))
    assert v.get_point_color(5) == "blanco"
    assert v.can_place_checker(5, "blanco") is True

    # Color distinto y hay 1 ficha => permitido (posible captura)
    assert v.can_place_checker(5, "negro") is True

    # Color distinto y hay 2 fichas => NO permitido
    points.add_checker_to_point(5, Ck("blanco"))
    assert points.point_count(5) == 2
    assert v.can_place_checker(5, "negro") is False


#  TESTS DE FACADE / INTEGRACIÓN 

def test_facade_colocar_mover_capturar(neutralize_original_board, players):
    white, black = players
    bf = BoardFacade()

    # Colocar dos blancas en 3 y una negra en 5
    bf.colocar_ficha(white, 3)
    bf.colocar_ficha(white, 3)
    bf.colocar_ficha(black, 5)

    assert bf.point_count(3) == 2
    assert bf.get_point_color(3) == "blanco"
    assert bf.point_count(5) == 1
    assert bf.get_point_color(5) == "negro"
    assert bf.get_bar_count("negro") == 0

    # Colocar una blanca en 4 y mover a 5 para CAPTURAR a la negra
    bf.colocar_ficha(white, 4)
    bf.mover_ficha(4, 5)
    assert bf.point_count(5) == 1
    assert bf.get_point_color(5) == "blanco"
    assert bf.get_bar_count("negro") == 1  # capturada

    # Bear off y has_won
    for _ in range(15):
        bf.bear_off("blanco")
    assert bf.get_off_count("blanco") == 15
    assert bf.has_won("blanco") is True

    # __str__ y __repr__ no deben romper
    s = str(bf)
    r = repr(bf)
    assert "TABLERO" in s.upper()
    assert "SOLID=True" in r


@pytest.mark.parametrize(
    "point,color,expected",
    [
        (19, "blanco", True),
        (24, "blanco", True),
        (18, "blanco", False),
        (1,  "negro",  True),
        (6,  "negro",  True),
        (7,  "negro",  False),
    ],
)
def test_facade_is_in_home_board(point, color, expected):
    bf = BoardFacade()
    assert bf.is_in_home_board(point, color) is expected


def test_facade_all_in_home_board_and_get_all(neutralize_original_board, players):
    white, black = players
    bf = BoardFacade()

    # Poner varias blancas fuera de home -> debe ser False
    for pt in (10, 11, 12):
        bf.colocar_ficha(white, pt)
    assert bf.all_in_home_board("blanco") is False

    # Limpiar y poner 3 blancas dentro del home (19..24) sin barra
    bf.clear()
    for pt in (19, 20, 24):
        bf.colocar_ficha(white, pt)

    assert bf.all_in_home_board("blanco") is True
    pos = bf.get_all_checkers("blanco")
    # Debe listar puntos y cantidades
    assert set(dict(pos).keys()).issubset({19, 20, 24})


def test_facade_clear_resets_everything(neutralize_original_board, players):
    w, b = players
    bf = BoardFacade()

    # Algo de estado
    bf.colocar_ficha(w, 19)
    bf.capture_checker(type("C", (), {"get_color": lambda self: "negro"})())
    bf.bear_off("blanco")
    assert bf.point_count(19) == 1
    assert bf.get_bar_count("negro") == 1
    assert bf.get_off_count("blanco") == 1

    # Limpiar
    bf.clear()
    assert all(len(lst) == 0 for lst in bf.points)
    assert bf.get_bar_count("negro") == 0
    assert bf.get_off_count("blanco") == 0


def test_board_with_setup_facade_positions(neutralize_original_board, players):
    w, b = players
    bw = BoardWithSetupFacade()
    bw.setup_initial_position(w, b)

    # Verificaciones mínimas del setup estándar:
    # Blancas: 2 en 1, 5 en 12, 3 en 17, 5 en 19  => total 15
    assert bw.point_count(1)  >= 2
    assert bw.point_count(12) >= 5
    assert bw.point_count(17) >= 3
    assert bw.point_count(19) >= 5
    # Negras: 2 en 24, 5 en 13, 3 en 8, 5 en 6   => total 15
    assert bw.point_count(24) >= 2
    assert bw.point_count(13) >= 5
    assert bw.point_count(8)  >= 3
    assert bw.point_count(6)  >= 5

    # Colores correctos en algunos puntos representativos
    assert bw.get_point_color(1) in ("blanco", None)   # puede apilarse y cambiar
    assert bw.get_point_color(24) in ("negro", None)
