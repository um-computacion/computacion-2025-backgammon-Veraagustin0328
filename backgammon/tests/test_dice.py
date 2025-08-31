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
