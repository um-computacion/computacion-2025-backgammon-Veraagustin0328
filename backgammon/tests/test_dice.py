import random
import inspect
import pytest
<<<<<<< HEAD
from backgammon.core.dice import Dice
=======
from backgammon.backgammon.core.dice import Dice
>>>>>>> origin/main


def test_dice_deterministic_with_seed():
    rng = random.Random(1234)
    d = Dice(rng=rng)
    r1 = d.roll()

    rng = random.Random(1234)
    d2 = Dice(rng=rng)
    r2 = d2.roll()

    assert r1 == r2
    assert 1 <= r1[0] <= 6 and 1 <= r1[1] <= 6


def test_dice_stores_last_roll_and_getter_setter():
    d = Dice(rng=random.Random(7))
    result = d.roll()
    assert d.get_ultima_tirada() == result

    d.set_ultima_tirada((6, 6))
    assert d.get_ultima_tirada() == (6, 6)

    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))


def test_attributes_have_double_underscores_and_camelcase_name():
    # Clase con CamelCase
    assert Dice.__name__ == "Dice" and "_" not in Dice.__name__

    # Atributos internos con doble guion bajo
    d = Dice()
    for attr in d.__dict__.keys():
        assert attr.startswith("__") and attr.endswith("__"), f"Atributo inválido: {attr}"


def test_has_getters_and_setters_required():
    # La clase debe tener getters y setters
    members = dict(inspect.getmembers(Dice))
    for name in ("get_rng", "set_rng", "get_ultima_tirada", "set_ultima_tirada"):
        assert name in members and inspect.isfunction(members[name]), f"Falta {name}"

#nuevo tests

def test_is_double_true_false():
    d = Dice.from_seed(1)
    d.set_ultima_tirada((4, 4))
    assert d.is_double()
    d.set_ultima_tirada((3, 5))
    assert not d.is_double()


def test_moves_from_roll_double_and_normal():
    d = Dice()
    d.set_ultima_tirada((2, 2))
    assert d.moves_from_roll() == [2, 2, 2, 2]
    d.set_ultima_tirada((1, 3))
    assert d.moves_from_roll() == [1, 3]


def test_repr_str_and_validation():
    d = Dice()
    d.set_ultima_tirada((6, 2))
    assert "Dice" in repr(d)
    assert "Tirada actual" in str(d)

    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))


#nuevo tests

import random
import inspect
import pytest
<<<<<<< HEAD
from backgammon.core.dice import Dice

=======
from backgammon.backgammon.core.dice import Dice
>>>>>>> origin/main


def test_dice_deterministic_with_seed():
    rng = random.Random(1234)
    d = Dice(rng=rng)
    r1 = d.roll()

    rng = random.Random(1234)
    d2 = Dice(rng=rng)
    r2 = d2.roll()

    assert r1 == r2
    assert 1 <= r1[0] <= 6 and 1 <= r1[1] <= 6


def test_dice_stores_last_roll_and_getter_setter():
    d = Dice(rng=random.Random(7))
    result = d.roll()
    assert d.get_ultima_tirada() == result

    d.set_ultima_tirada((6, 6))
    assert d.get_ultima_tirada() == (6, 6)

    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))


def test_attributes_have_double_underscores_and_camelcase_name():
    assert Dice.__name__ == "Dice" and "_" not in Dice.__name__
    d = Dice()
    for attr in d.__dict__.keys():
        assert attr.startswith("__") and attr.endswith("__"), f"Atributo inválido: {attr}"


def test_has_getters_and_setters_required():
    members = dict(inspect.getmembers(Dice))
    for name in ("get_rng", "set_rng", "get_ultima_tirada", "set_ultima_tirada"):
        assert name in members and inspect.isfunction(members[name]), f"Falta {name}"


def test_is_double_true_false():
    d = Dice.from_seed(1)
    d.set_ultima_tirada((4, 4))
    assert d.is_double()
    d.set_ultima_tirada((3, 5))
    assert not d.is_double()


def test_moves_from_roll_double_and_normal():
    d = Dice()
    d.set_ultima_tirada((2, 2))
    assert d.moves_from_roll() == [2, 2, 2, 2]
    d.set_ultima_tirada((1, 3))
    assert d.moves_from_roll() == [1, 3]


def test_repr_str_and_validation():
    d = Dice()
    d.set_ultima_tirada((6, 2))
    assert "Dice" in repr(d)
    assert "Tirada actual" in str(d)

    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))


def test_dice_inicializacion_default():
    """Test de inicialización sin parámetros"""
    d = Dice()
    assert d.get_ultima_tirada() == (0, 0)
    assert isinstance(d.get_rng(), random.Random)


def test_dice_inicializacion_con_rng():
    """Test de inicialización con RNG personalizado"""
    rng = random.Random(42)
    d = Dice(rng=rng)
    assert d.get_rng() == rng


def test_dice_from_seed():
    """Test del método from_seed"""
    d = Dice.from_seed(123)
    assert isinstance(d, Dice)
    # Verificar que las tiradas son reproducibles
    d1 = Dice.from_seed(123)
    d2 = Dice.from_seed(123)
    assert d1.roll() == d2.roll()


def test_dice_roll():
    """Test del método roll"""
    d = Dice()
    resultado = d.roll()
    
    # Verificar que devuelve tupla de 2 elementos
    assert isinstance(resultado, tuple)
    assert len(resultado) == 2
    
    # Verificar que los valores están entre 1 y 6
    d1, d2 = resultado
    assert 1 <= d1 <= 6
    assert 1 <= d2 <= 6
    
    # Verificar que se guarda en ultima_tirada
    assert d.get_ultima_tirada() == resultado


def test_dice_roll_actualiza_ultima_tirada():
    """Test que roll actualiza la última tirada"""
    d = Dice.from_seed(100)
    primera = d.roll()
    segunda = d.roll()
    
    # La última tirada debe ser la segunda
    assert d.get_ultima_tirada() == segunda
    assert primera != segunda or True  # Pueden ser iguales por azar


def test_dice_is_double_true():
    """Test de is_double cuando hay dobles"""
    d = Dice()
    d.set_ultima_tirada((3, 3))
    assert d.is_double() is True
    
    d.set_ultima_tirada((6, 6))
    assert d.is_double() is True


def test_dice_is_double_false():
    """Test de is_double cuando NO hay dobles"""
    d = Dice()
    d.set_ultima_tirada((1, 2))
    assert d.is_double() is False
    
    d.set_ultima_tirada((5, 3))
    assert d.is_double() is False


def test_dice_moves_from_roll_normal():
    """Test de moves_from_roll con tirada normal (no dobles)"""
    d = Dice()
    d.set_ultima_tirada((2, 5))
    moves = d.moves_from_roll()
    
    assert moves == [2, 5]
    assert len(moves) == 2


def test_dice_moves_from_roll_dobles():
    """Test de moves_from_roll con dobles"""
    d = Dice()
    d.set_ultima_tirada((4, 4))
    moves = d.moves_from_roll()
    
    assert moves == [4, 4, 4, 4]
    assert len(moves) == 4


def test_dice_get_set_rng():
    """Test de getters y setters de RNG"""
    d = Dice()
    rng_original = d.get_rng()
    
    nuevo_rng = random.Random(999)
    d.set_rng(nuevo_rng)
    
    assert d.get_rng() == nuevo_rng
    assert d.get_rng() != rng_original


def test_dice_get_ultima_tirada():
    """Test del getter de ultima_tirada"""
    d = Dice()
    d.set_ultima_tirada((1, 6))
    
    tirada = d.get_ultima_tirada()
    assert tirada == (1, 6)
    assert isinstance(tirada, tuple)


def test_dice_set_ultima_tirada_tupla_valida():
    """Test de set_ultima_tirada con tupla válida"""
    d = Dice()
    d.set_ultima_tirada((3, 5))
    assert d.get_ultima_tirada() == (3, 5)


def test_dice_set_ultima_tirada_lista_valida():
    """Test de set_ultima_tirada con lista válida (se convierte a tupla)"""
    d = Dice()
    d.set_ultima_tirada([2, 4])
    assert d.get_ultima_tirada() == (2, 4)


def test_dice_set_ultima_tirada_invalida_fuera_rango():
    """Test de set_ultima_tirada con valores fuera de rango"""
    d = Dice()
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((0, 5))  # 0 es inválido
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((3, 7))  # 7 es inválido
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((-1, 3))  # Negativo


def test_dice_set_ultima_tirada_invalida_tipo():
    """Test de set_ultima_tirada con tipos inválidos"""
    d = Dice()
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((1.5, 3))  # Float no válido
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada(("1", "2"))  # Strings no válidos


def test_dice_set_ultima_tirada_invalida_longitud():
    """Test de set_ultima_tirada con longitud incorrecta"""
    d = Dice()
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((1,))  # Solo 1 elemento
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada((1, 2, 3))  # 3 elementos


def test_dice_set_ultima_tirada_invalida_no_tupla_ni_lista():
    """Test de set_ultima_tirada con tipo completamente inválido"""
    d = Dice()
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada("12")  # String
    
    with pytest.raises(ValueError, match="Tirada inválida"):
        d.set_ultima_tirada(12)  # Int


def test_dice_repr():
    """Test del método __repr__"""
    d = Dice()
    d.set_ultima_tirada((4, 5))
    
    repr_str = repr(d)
    assert "Dice" in repr_str
    assert "4" in repr_str
    assert "5" in repr_str


def test_dice_str():
    """Test del método __str__"""
    d = Dice()
    d.set_ultima_tirada((2, 6))
    
    str_repr = str(d)
    assert "Tirada actual" in str_repr
    assert "2" in str_repr
    assert "6" in str_repr


def test_dice_valores_limite():
    """Test con valores en los límites (1 y 6)"""
    d = Dice()
    
    # Valor mínimo
    d.set_ultima_tirada((1, 1))
    assert d.get_ultima_tirada() == (1, 1)
    assert d.is_double() is True
    
    # Valor máximo
    d.set_ultima_tirada((6, 6))
    assert d.get_ultima_tirada() == (6, 6)
    assert d.is_double() is True


def test_dice_reproducibilidad_con_seed():
    """Test que la semilla produce tiradas reproducibles"""
    d1 = Dice.from_seed(555)
    d2 = Dice.from_seed(555)
    
    tiradas1 = [d1.roll() for _ in range(5)]
    tiradas2 = [d2.roll() for _ in range(5)]
    
    assert tiradas1 == tiradas2


def test_dice_roll_multiples_veces():
    """Test de múltiples rolls consecutivos"""
    d = Dice.from_seed(777)
    
    for _ in range(10):
        resultado = d.roll()
        assert len(resultado) == 2
        assert all(1 <= val <= 6 for val in resultado)
        assert d.get_ultima_tirada() == resultado


def test_dice_moves_from_roll_todos_dobles():
    """Test de moves_from_roll con todos los posibles dobles"""
    d = Dice()
    
    for i in range(1, 7):
        d.set_ultima_tirada((i, i))
        moves = d.moves_from_roll()
        assert moves == [i, i, i, i]
        assert len(moves) == 4
        
        
def test_dice_is_double_false_y_true():
    d = Dice.from_seed(3)
    d.set_ultima_tirada((4, 5))
    assert not d.is_double()
    d.set_ultima_tirada((6, 6))
    assert d.is_double()

def test_dice_moves_from_roll_con_doble_y_normal():
    d = Dice()
    d.set_ultima_tirada((2, 2))
    assert d.moves_from_roll() == [2, 2, 2, 2]
    d.set_ultima_tirada((1, 3))
    assert d.moves_from_roll() == [1, 3]

def test_dice_set_ultima_tirada_lista_y_valor_invalido():
    d = Dice()
    # aceptar lista
    d.set_ultima_tirada([5, 2])
    assert d.get_ultima_tirada() == (5, 2)
    # rechazar tupla inválida
    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 8))

def test_dice_repr_y_str_contienen_info_correcta():
    d = Dice()
    d.set_ultima_tirada((6, 2))
    s = str(d)
    r = repr(d)
    assert "6" in s and "2" in s
    assert "Dice(" in r and ")" in r

def test_dice_cambia_y_recupera_rng():
    d = Dice()
    nuevo_rng = random.Random(99)
    d.set_rng(nuevo_rng)
    assert d.get_rng() == nuevo_rng