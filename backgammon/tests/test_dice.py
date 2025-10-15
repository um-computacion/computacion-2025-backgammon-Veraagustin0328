from backgammon.core.dice import Dice
import random
import inspect

def test_dice_roll_in_range():
    d = Dice()
    a, b = d.roll()
    assert 1 <= a <= 6
    assert 1 <= b <= 6

def test_dice_deterministic_with_seed():
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    d1 = Dice(rng=rng1)
    d2 = Dice(rng=rng2)
    assert d1.roll() == d2.roll()

def test_dice_stores_last_roll_and_getter_setter():
    d = Dice(rng=random.Random(7))
    result = d.roll()
    assert d.get_ultima_tirada() == result
    d.set_ultima_tirada((6, 6))
    assert d.get_ultima_tirada() == (6, 6)

def test_attributes_have_double_underscores_and_camelcase_name():
    
    assert Dice.__name__ == "Dice" and "_" not in Dice.__name__
    
    d = Dice()
    for attr in d.__dict__.keys():
        assert attr.startswith("__") and attr.endswith("__"), f"Atributo inválido: {attr}"

def test_has_getters_and_setters_required():
    
    members = dict(inspect.getmembers(Dice))
    for name in ("get_rng", "set_rng", "get_ultima_tirada", "set_ultima_tirada"):
        assert name in members and inspect.isfunction(members[name]), f"Falta {name}"



import pytest
from backgammon.backgammon.core.dice import Dice

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

    # Prueba de validación en set_ultima_tirada
    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))
