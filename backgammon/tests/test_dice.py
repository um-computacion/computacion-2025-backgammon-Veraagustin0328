import random
import inspect
import pytest
from backgammon.backgammon.core.dice import Dice


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
