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


def test_player_reset_fichas_y_puntos():
    jugador = Player("Josias")
    jugador.sumar_puntos(4)
    jugador.set_fichas(5)
    jugador.reset()
    assert jugador.get_fichas() == 15
    assert jugador.get_puntos() == 0


def test_player_repr_y_str():
    jugador = Player("Valentina")
    repr_str = repr(jugador)
    assert "Valentina" in repr_str
    assert str(jugador).startswith("Valentina")


def test_player_comparacion_igualdad():
    jugador1 = Player("Agustin")
    jugador2 = Player("Agustin")
    jugador3 = Player("Franco")
    assert jugador1 == jugador2
    assert jugador1 != jugador3


def test_player_serializacion_dict():
    jugador = Player("Camila")
    d = jugador.to_dict()
    assert "nombre" in d and "fichas" in d and "puntos" in d
    j2 = Player.from_dict(d)
    assert j2.get_nombre() == jugador.get_nombre()


def test_player_set_fichas_negativas():
    jugador = Player("Josias")
    with pytest.raises(ValueError):
        jugador.set_fichas(-1)


def test_player_sumar_puntos_y_perder_ficha_funciona():
    p = Player("Agus")
    p.sumar_puntos(10)
    assert p.get_puntos() == 10
    p.perder_ficha()
    assert p.get_fichas() == 14


def test_player_perder_ficha_error_si_no_hay():
    p = Player("Franco")
    p.set_fichas(0)
    with pytest.raises(ValueError):
        p.perder_ficha()


def test_player_reset_vuelve_a_estado_inicial():
    p = Player("Cami")
    p.set_fichas(5)
    p.sumar_puntos(12)
    p.reset()
    assert p.get_fichas() == 15
    assert p.get_puntos() == 0


def test_player_to_from_dict_reconstruye_correctamente():
    p = Player("Valen")
    p.set_fichas(10)
    p.sumar_puntos(7)
    data = p.to_dict()
    nuevo = Player.from_dict(data)
    assert nuevo.get_nombre() == "Valen"
    assert nuevo.get_fichas() == 10
    assert nuevo.get_puntos() == 7


def test_player_eq_y_hash_basados_en_nombre():
    p1 = Player("Lucas")
    p2 = Player("Lucas")
    p3 = Player("Jose")
    assert p1 == p2
    assert p1 != p3
    assert hash(p1) == hash(p2)
