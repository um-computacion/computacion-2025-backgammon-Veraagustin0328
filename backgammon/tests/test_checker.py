import pytest
from backgammon.core.checker import Checker
from backgammon.core.player import Player



def test_checker_inicializacion():
    p = Player("Agus")
    c = Checker(p)
    assert c.get_player() == p


def test_checker_repr_y_color():
    p = Player("Josias")
    c = Checker(p)
    assert str(p.get_nombre()) in repr(c)

import pytest
from backgammon.core.checker import Checker
from backgammon.core.player import Player


def test_checker_inicializacion():
    p = Player("Agus")
    c = Checker(p)
    assert c.get_player() == p


def test_checker_repr_y_color():
    p = Player("Josias")
    c = Checker(p)
    assert str(p.get_nombre()) in repr(c)


def test_checker_con_color_custom():
    """Test de inicialización con color específico"""
    p = Player("Test")
    c = Checker(p, color="negro")
    assert c.get_color() == "negro"


def test_checker_con_posicion_inicial():
    """Test de inicialización con posición"""
    p = Player("Test")
    c = Checker(p, position=5)
    assert c.get_position() == 5


def test_checker_set_color():
    """Test del setter de color"""
    p = Player("Test")
    c = Checker(p, color="blanco")
    c.set_color("negro")
    assert c.get_color() == "negro"


def test_checker_move_to():
    """Test del método move_to"""
    p = Player("Test")
    c = Checker(p, position=1)
    c.move_to(10)
    assert c.get_position() == 10


def test_checker_move_to_bar():
    """Test de mover a la barra"""
    p = Player("Test")
    c = Checker(p, position=5)
    c.move_to_bar()
    assert c.is_on_bar()
    assert c.get_position() == Checker.BAR


def test_checker_move_to_off():
    """Test de mover fuera del tablero"""
    p = Player("Test")
    c = Checker(p, position=20)
    c.move_to_off()
    assert c.is_borne_off()
    assert c.get_position() == Checker.OFF


def test_checker_is_on_board():
    """Test de verificación si está en el tablero"""
    p = Player("Test")
    c = Checker(p, position=15)
    assert c.is_on_board()
    
    c.move_to_bar()
    assert not c.is_on_board()
    
    c.move_to_off()
    assert not c.is_on_board()


def test_checker_set_position_none():
    """Test de setear posición a None"""
    p = Player("Test")
    c = Checker(p, position=5)
    c.set_position(None)
    assert c.get_position() is None


def test_checker_set_position_invalida():
    """Test de posición inválida debe lanzar ValueError"""
    p = Player("Test")
    c = Checker(p)
    
    with pytest.raises(ValueError):
        c.set_position(25)  # Fuera de rango
    
    with pytest.raises(ValueError):
        c.set_position(-5)  # Número negativo inválido


def test_checker_to_dict():
    """Test de serialización a diccionario"""
    p = Player("TestPlayer")
    c = Checker(p, color="negro", position=10)
    d = c.to_dict()
    
    assert d["player"] == "TestPlayer"
    assert d["color"] == "negro"
    assert d["position"] == 10


def test_checker_from_dict():
    """Test de deserialización desde diccionario"""
    p = Player("PlayerTest")
    data = {
        "color": "blanco",
        "position": 7
    }
    c = Checker.from_dict(data, p)
    
    assert c.get_player() == p
    assert c.get_color() == "blanco"
    assert c.get_position() == 7


def test_checker_str():
    """Test del método __str__"""
    p = Player("Juan")
    c = Checker(p, color="negro", position=12)
    s = str(c)
    
    assert "Juan" in s
    assert "negro" in s
    assert "12" in s


def test_checker_eq():
    """Test de comparación entre fichas"""
    p1 = Player("Player1")
    p2 = Player("Player2")
    
    c1 = Checker(p1, color="blanco")
    c2 = Checker(p1, color="blanco")
    c3 = Checker(p2, color="blanco")
    c4 = Checker(p1, color="negro")
    
    # Mismas fichas (mismo jugador y color)
    assert c1 == c2
    
    # Diferente jugador
    assert c1 != c3
    
    # Diferente color
    assert c1 != c4
    
    # Comparar con no-Checker
    assert c1 != "not a checker"
    assert c1 != None
    
    
    
def test_checker_inicializacion():
    p = Player("Agus")
    c = Checker(p)
    assert c.get_player() == p


def test_checker_repr_y_color():
    """Test de representación y color"""
    p = Player("Josias")
    c = Checker(p)
    assert str(p.get_nombre()) in repr(c)


# ========== TESTS ADICIONALES PARA 100% DE COBERTURA ==========

def test_checker_inicializacion_completa():
    """Test de inicialización con todos los parámetros"""
    p = Player("TestPlayer")
    c = Checker(p, color="negro", position=10)
    
    assert c.get_player() == p
    assert c.get_color() == "negro"
    assert c.get_position() == 10


def test_checker_inicializacion_sin_posicion():
    """Test de inicialización sin posición (None por defecto)"""
    p = Player("Test")
    c = Checker(p, color="blanco")
    
    assert c.get_position() is None
    assert c.get_color() == "blanco"


def test_checker_inicializacion_color_default():
    """Test que el color por defecto es 'blanco'"""
    p = Player("Test")
    c = Checker(p)
    
    assert c.get_color() == "blanco"


def test_checker_get_player():
    """Test del getter de player"""
    p1 = Player("Jugador1")
    p2 = Player("Jugador2")
    
    c1 = Checker(p1)
    c2 = Checker(p2)
    
    assert c1.get_player() == p1
    assert c2.get_player() == p2
    assert c1.get_player() != c2.get_player()


def test_checker_get_color():
    """Test del getter de color"""
    p = Player("Test")
    c1 = Checker(p, color="blanco")
    c2 = Checker(p, color="negro")
    
    assert c1.get_color() == "blanco"
    assert c2.get_color() == "negro"


def test_checker_get_position():
    """Test del getter de position"""
    p = Player("Test")
    c = Checker(p, position=15)
    
    assert c.get_position() == 15


def test_checker_get_position_none():
    """Test del getter cuando position es None"""
    p = Player("Test")
    c = Checker(p)
    
    assert c.get_position() is None


def test_checker_set_position_valida():
    """Test de set_position con valores válidos"""
    p = Player("Test")
    c = Checker(p)
    
    # Probar todos los puntos válidos
    for i in range(1, 25):
        c.set_position(i)
        assert c.get_position() == i


def test_checker_set_position_none():
    """Test de set_position a None"""
    p = Player("Test")
    c = Checker(p, position=10)
    
    c.set_position(None)
    assert c.get_position() is None


def test_checker_set_position_bar():
    """Test de set_position a BAR (-1)"""
    p = Player("Test")
    c = Checker(p, position=5)
    
    c.set_position(Checker.BAR)
    assert c.get_position() == Checker.BAR
    assert c.get_position() == -1


def test_checker_set_position_off():
    """Test de set_position a OFF (0)"""
    p = Player("Test")
    c = Checker(p, position=20)
    
    c.set_position(Checker.OFF)
    assert c.get_position() == Checker.OFF
    assert c.get_position() == 0


def test_checker_set_position_invalida_mayor():
    """Test de set_position con valor mayor a 24"""
    p = Player("Test")
    c = Checker(p)
    
    with pytest.raises(ValueError, match="Punto inválido"):
        c.set_position(25)
    
    with pytest.raises(ValueError, match="Punto inválido"):
        c.set_position(100)


def test_checker_set_position_invalida_menor():
    """Test de set_position con valor menor a -1"""
    p = Player("Test")
    c = Checker(p)
    
    with pytest.raises(ValueError, match="Punto inválido"):
        c.set_position(-2)
    
    with pytest.raises(ValueError, match="Punto inválido"):
        c.set_position(-10)


def test_checker_set_color():
    """Test del setter de color"""
    p = Player("Test")
    c = Checker(p, color="blanco")
    
    c.set_color("negro")
    assert c.get_color() == "negro"
    
    c.set_color("blanco")
    assert c.get_color() == "blanco"


def test_checker_set_color_conversion_string():
    """Test que set_color convierte a string"""
    p = Player("Test")
    c = Checker(p)
    
    c.set_color(123)  # Convertirá a "123"
    assert c.get_color() == "123"


def test_checker_move_to():
    """Test del método move_to con posiciones válidas"""
    p = Player("Test")
    c = Checker(p, position=1)
    
    c.move_to(10)
    assert c.get_position() == 10
    
    c.move_to(24)
    assert c.get_position() == 24
    
    c.move_to(1)
    assert c.get_position() == 1


def test_checker_move_to_invalida():
    """Test de move_to con posición inválida"""
    p = Player("Test")
    c = Checker(p, position=5)
    
    with pytest.raises(ValueError):
        c.move_to(30)


def test_checker_move_to_bar():
    """Test del método move_to_bar"""
    p = Player("Test")
    c = Checker(p, position=15)
    
    c.move_to_bar()
    assert c.get_position() == Checker.BAR
    assert c.is_on_bar()


def test_checker_move_to_off():
    """Test del método move_to_off"""
    p = Player("Test")
    c = Checker(p, position=22)
    
    c.move_to_off()
    assert c.get_position() == Checker.OFF
    assert c.is_borne_off()


def test_checker_is_on_bar_true():
    """Test de is_on_bar cuando está en la barra"""
    p = Player("Test")
    c = Checker(p, position=Checker.BAR)
    
    assert c.is_on_bar() is True


def test_checker_is_on_bar_false():
    """Test de is_on_bar cuando NO está en la barra"""
    p = Player("Test")
    c = Checker(p, position=10)
    
    assert c.is_on_bar() is False


def test_checker_is_borne_off_true():
    """Test de is_borne_off cuando está fuera"""
    p = Player("Test")
    c = Checker(p, position=Checker.OFF)
    
    assert c.is_borne_off() is True


def test_checker_is_borne_off_false():
    """Test de is_borne_off cuando NO está fuera"""
    p = Player("Test")
    c = Checker(p, position=15)
    
    assert c.is_borne_off() is False


def test_checker_is_on_board_true():
    """Test de is_on_board cuando está en el tablero"""
    p = Player("Test")
    
    for pos in range(1, 25):
        c = Checker(p, position=pos)
        assert c.is_on_board() is True


def test_checker_is_on_board_false_bar():
    """Test de is_on_board cuando está en BAR"""
    p = Player("Test")
    c = Checker(p, position=Checker.BAR)
    
    assert c.is_on_board() is False


def test_checker_is_on_board_false_off():
    """Test de is_on_board cuando está OFF"""
    p = Player("Test")
    c = Checker(p, position=Checker.OFF)
    
    assert c.is_on_board() is False


def test_checker_is_on_board_false_none():
    """Test de is_on_board cuando position es None"""
    p = Player("Test")
    c = Checker(p)
    
    assert c.is_on_board() is False


def test_checker_to_dict():
    """Test de serialización a diccionario"""
    p = Player("TestPlayer")
    c = Checker(p, color="negro", position=12)
    
    d = c.to_dict()
    
    assert d["player"] == "TestPlayer"
    assert d["color"] == "negro"
    assert d["position"] == 12


def test_checker_to_dict_sin_posicion():
    """Test de to_dict cuando position es None"""
    p = Player("Player1")
    c = Checker(p, color="blanco")
    
    d = c.to_dict()
    
    assert d["player"] == "Player1"
    assert d["color"] == "blanco"
    assert d["position"] is None


def test_checker_to_dict_en_bar():
    """Test de to_dict cuando está en BAR"""
    p = Player("Player2")
    c = Checker(p, color="negro", position=Checker.BAR)
    
    d = c.to_dict()
    
    assert d["position"] == -1


def test_checker_from_dict():
    """Test de deserialización desde diccionario"""
    p = Player("PlayerTest")
    data = {
        "color": "negro",
        "position": 18
    }
    
    c = Checker.from_dict(data, p)
    
    assert c.get_player() == p
    assert c.get_color() == "negro"
    assert c.get_position() == 18


def test_checker_from_dict_sin_posicion():
    """Test de from_dict sin position en los datos"""
    p = Player("Player")
    data = {
        "color": "blanco"
    }
    
    c = Checker.from_dict(data, p)
    
    assert c.get_player() == p
    assert c.get_color() == "blanco"
    assert c.get_position() is None


def test_checker_from_dict_color_default():
    """Test de from_dict sin color (usa default)"""
    p = Player("Player")
    data = {
        "position": 5
    }
    
    c = Checker.from_dict(data, p)
    
    assert c.get_color() == "blanco"
    assert c.get_position() == 5


def test_checker_from_dict_posicion_bar():
    """Test de from_dict con posición BAR"""
    p = Player("Player")
    data = {
        "color": "negro",
        "position": -1
    }
    
    c = Checker.from_dict(data, p)
    
    assert c.is_on_bar()


def test_checker_repr():
    """Test del método __repr__"""
    p = Player("RepPlayer")
    c = Checker(p, color="blanco", position=7)
    
    repr_str = repr(c)
    
    assert "Checker" in repr_str
    assert "RepPlayer" in repr_str
    assert "blanco" in repr_str
    assert "7" in repr_str


def test_checker_repr_sin_posicion():
    """Test de __repr__ sin posición"""
    p = Player("Player")
    c = Checker(p)
    
    repr_str = repr(c)
    
    assert "Checker" in repr_str
    assert "Player" in repr_str
    assert "None" in repr_str


def test_checker_str():
    """Test del método __str__"""
    p = Player("StrPlayer")
    c = Checker(p, color="negro", position=15)
    
    str_repr = str(c)
    
    assert "Ficha" in str_repr
    assert "StrPlayer" in str_repr
    assert "negro" in str_repr
    assert "15" in str_repr


def test_checker_str_posicion_none():
    """Test de __str__ con posición None"""
    p = Player("Player")
    c = Checker(p, color="blanco")
    
    str_repr = str(c)
    
    assert "Player" in str_repr
    assert "blanco" in str_repr
    assert "None" in str_repr


def test_checker_eq_iguales():
    """Test de __eq__ con fichas iguales"""
    p = Player("Player1")
    c1 = Checker(p, color="blanco", position=5)
    c2 = Checker(p, color="blanco", position=10)  # Distinta posición
    
    # Son iguales si tienen mismo jugador y color
    assert c1 == c2


def test_checker_eq_diferente_jugador():
    """Test de __eq__ con diferente jugador"""
    p1 = Player("Player1")
    p2 = Player("Player2")
    
    c1 = Checker(p1, color="blanco")
    c2 = Checker(p2, color="blanco")
    
    assert c1 != c2


def test_checker_eq_diferente_color():
    """Test de __eq__ con diferente color"""
    p = Player("Player")
    
    c1 = Checker(p, color="blanco")
    c2 = Checker(p, color="negro")
    
    assert c1 != c2


def test_checker_eq_con_no_checker():
    """Test de __eq__ comparando con objetos que no son Checker"""
    p = Player("Player")
    c = Checker(p)
    
    assert c != "not a checker"
    assert c != 123
    assert c != None
    assert c != []
    assert c != {}


def test_checker_constantes_clase():
    """Test de las constantes de clase"""
    assert Checker.BAR == -1
    assert Checker.OFF == 0
    assert Checker.MIN_POINT == 1
    assert Checker.MAX_POINT == 24


def test_checker_movimientos_completos():
    """Test de una secuencia completa de movimientos"""
    p = Player("Player")
    c = Checker(p, position=1)
    
    # Mover por el tablero
    c.move_to(5)
    assert c.is_on_board()
    
    # Mover a la barra
    c.move_to_bar()
    assert c.is_on_bar()
    assert not c.is_on_board()
    assert not c.is_borne_off()
    
    # Volver al tablero
    c.move_to(20)
    assert c.is_on_board()
    
    # Sacar del tablero
    c.move_to_off()
    assert c.is_borne_off()
    assert not c.is_on_board()
    assert not c.is_on_bar()


def test_checker_todas_posiciones_validas():
    """Test verificando todas las posiciones válidas del tablero"""
    p = Player("Test")
    c = Checker(p)
    
    # Probar todos los puntos del 1 al 24
    for i in range(1, 25):
        c.set_position(i)
        assert c.get_position() == i
        assert c.is_on_board()
        assert not c.is_on_bar()
        assert not c.is_borne_off()


def test_checker_color_conversion():
    """Test que el color se convierte a string en __init__"""
    p = Player("Test")
    
    # Color como número
    c = Checker(p, color=42)
    assert c.get_color() == "42"
    
    # Color vacío
    c2 = Checker(p, color="")
    assert c2.get_color() == ""

