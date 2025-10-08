import pytest
from backgammon.core.player import Player

def test_player_inicializacion():
    jugador = Player("Agus")
    assert jugador.get_nombre() == "Agus"
    assert jugador.get_fichas() == 15
    assert jugador.get_puntos() == 0

def test_player_modifica_puntos():
    jugador = Player("Agus")
    jugador.sumar_puntos(5)
    assert jugador.get_puntos() == 5

def test_player_perder_ficha_ok():
    jugador = Player("Agus")
    jugador.perder_ficha()
    assert jugador.get_fichas() == 14

def test_player_perder_ficha_sin_fichas():
    jugador = Player("Agus")
    jugador.set_fichas(0)
    with pytest.raises(ValueError):
        jugador.perder_ficha()

