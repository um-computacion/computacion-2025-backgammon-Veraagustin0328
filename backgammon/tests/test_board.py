import pytest
from backgammon.backgammon.core.board import Board
from backgammon.backgammon.core.player import Player


def test_board_inicializacion():
    b = Board()
    assert isinstance(b.get_estado(), list)
    assert len(b.get_estado()) > 0


def test_board_colocar_y_quitar_ficha():
    b = Board()
    p = Player("Agus")
    b.colocar_ficha(p, 1)
    assert b.get_estado()[1] == p.get_nombre()
    b.quitar_ficha(1)
    assert b.get_estado()[1] is None


def test_board_mover_ficha_valida():
    b = Board()
    p = Player("Agus")
    b.colocar_ficha(p, 1)
    b.mover_ficha(1, 3)
    assert b.get_estado()[3] == p.get_nombre()
    assert b.get_estado()[1] is None


def test_board_mover_ficha_invalida():
    b = Board()
    with pytest.raises(ValueError):
        b.mover_ficha(5, 1)



def test_board_posicion_invalida_en_colocar():
    b = Board()
    p = Player("Agus")
    with pytest.raises(ValueError):
        b.colocar_ficha(p, 0)      # inválida
    with pytest.raises(ValueError):
        b.colocar_ficha(p, 25)     # inválida


def test_board_posicion_invalida_en_mover():
    b = Board()
    p = Player("Agus")
    # origen inválido
    with pytest.raises(ValueError):
        b.mover_ficha(0, 2)
    # destino inválido
    b.colocar_ficha(p, 1)
    with pytest.raises(ValueError):
        b.mover_ficha(1, 25)


def test_board_mover_sin_ficha_en_origen():
    b = Board()
    with pytest.raises(ValueError):
        b.mover_ficha(3, 4)  # no hay nada en 3


def test_board_quitar_y_estado_vacio():
    b = Board()
    p = Player("Agus")
    b.colocar_ficha(p, 2)
    b.quitar_ficha(2)
    estado = b.get_estado()[2]
    # soporte para ambas implementaciones: string o lista
    if isinstance(estado, list):
        assert len(estado) == 0
    else:
        assert estado is None


def test_board_repr_tiene_board():
    b = Board()
    assert "Board" in repr(b)
