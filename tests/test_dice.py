import pytest
from  backgammon.core.dice import Dice 

def test_roll_returns_two_values_between_1_and_6():
    dice = Dice(seed=123)  
    result = dice.roll()
    assert all(1 <= value <= 6 for value in result)
    assert len(result) in (2, 4) 

def test_roll_with_seed_reproducible():
    dice1 = Dice(seed=42)
    dice2 = Dice(seed=42)
    assert dice1.roll() == dice2.roll()

def test_roll_returns_four_when_doubles():
    dice = Dice(seed=42)
    for _ in range(100):  # probamos varias tiradas
        result = dice.roll()
        if len(result) == 4:
            assert all(v == result[0] for v in result)
            return
    pytest.skip("No salieron dobles en 100 tiradas con esta semilla")