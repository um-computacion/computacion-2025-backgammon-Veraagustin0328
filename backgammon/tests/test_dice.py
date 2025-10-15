from backgammon.core.dice import Dice
import random

def test_dice_deterministic_with_seed():
    rng = random.Random(1234)
    d = Dice(rng=rng)
    r1 = d.roll()

    
    rng = random.Random(1234)
    d2 = Dice(rng=rng)
    r2 = d2.roll()

    assert r1 == r2
    assert 1 <= r1[0] <= 6 and 1 <= r1[1] <= 6

def test_dice_stores_last_roll():
    d = Dice(rng=random.Random(7))
    r = d.roll()
    assert d.get_ultima_tirada() == r


from backgammon.core.dice import Dice
import random
import pytest

def test_dice_getter_setter_extras():
    d = Dice(rng=random.Random(1))
    assert d.get_rng() is not None

    d.set_ultima_tirada((6, 6))
    assert d.get_ultima_tirada() == (6, 6)

    with pytest.raises(ValueError):
        d.set_ultima_tirada((0, 7))  # inválido
