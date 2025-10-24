import pytest
from backgammon.core.game import Game
from backgammon.core.player import Player
from backgammon.core.dice import Dice


def test_game_roll_turn_and_score():
    """Test que verifica el roll de dados, turnos y puntaje"""
    # Player solo acepta 1 argumento (nombre), no color
    g = Game(Player("A"), Player("B"), dice=Dice.from_seed(123))
    
    # Verificar que roll devuelve una lista de 2 elementos
    v1 = g.roll()
    assert isinstance(v1, list) and len(v1) == 2
    
    # Guardar jugador actual y sumarle puntos
    cur = g.current_player
    g.add_score(cur, 2)
    
    # Verificar que el puntaje se guardó correctamente usando get_nombre()
    s = g.get_score()
    assert s[cur.get_nombre()] == 2
    
    # Cambiar turno y verificar que es otro jugador
    g.next_turn()
    assert g.current_player.get_nombre() != cur.get_nombre()


def test_game_to_from_dict():
    """Test de serialización y deserialización del juego"""
    # Crear juego con dos jugadores
    g = Game(Player("A"), Player("B"))
    
    # Serializar a diccionario
    d = g.to_dict()
    
    # Deserializar desde diccionario
    g2 = Game.from_dict(d)
    
    # Verificar que el jugador actual se mantuvo
    assert g2.current_player.get_nombre() == g.current_player.get_nombre()


def test_game_inicializacion_basica():
    """Test de inicialización básica del juego"""
    p1 = Player("Agus")
    p2 = Player("Franco")
    g = Game(p1, p2)
    
    # Verificar que el jugador actual es uno de los dos jugadores
    assert g.current_player in (p1, p2)
    
    # Verificar que los jugadores están en la lista
    assert p1 in g.get_players()
    assert p2 in g.get_players()
    
    # Verificar que el índice inicial es válido
    assert g.get_current_index() in (0, 1)


def test_game_cambio_turno():
    """Test del cambio de turno entre jugadores"""
    p1 = Player("Agus")
    p2 = Player("Franco")
    g = Game(p1, p2)
    
    # Guardar jugador actual
    actual = g.current_player
    
    # Cambiar turno
    g.next_turn()
    
    # Verificar que el jugador cambió
    assert g.current_player != actual
    
    # Verificar que es el otro jugador
    if actual == p1:
        assert g.current_player == p2
    else:
        assert g.current_player == p1
        
        
def test_game_roll_devuelve_lista_y_historial_aumenta():
    g = Game(Player("A"), Player("B"), dice=Dice.from_seed(123))
    h0 = len(g.get_history())
    r = g.roll()
    assert isinstance(r, list) and len(r) == 2 and all(1 <= x <= 6 for x in r)
    assert len(g.get_history()) == h0 + 1


def test_game_change_turn_varias_veces_vuelve_al_inicial():
    p1, p2 = Player("A"), Player("B")
    g = Game(p1, p2)
    inicial = g.get_current_player()
    g.change_turn()
    g.change_turn()
    assert g.get_current_player() == inicial


def test_game_add_points_valido_e_invalido():
    p1, p2 = Player("A"), Player("B")
    g = Game(p1, p2)
    g.add_points(p1, 7)
    assert g.get_score()[p1.get_nombre()] == 7
    # jugador no perteneciente al juego
    p3 = Player("C")
    with pytest.raises(ValueError):
        g.add_points(p3, 1)


def test_game_to_from_dict_redondeo_completo():
    p1, p2 = Player("A"), Player("B")
    g = Game(p1, p2, dice=Dice.from_seed(5))
    g.roll()                # genera historial
    g.add_points(p1, 3)
    d = g.to_dict()
    g2 = Game.from_dict(d)
    # mismos jugadores en score
    assert set(g2.get_score().keys()) == set(g.get_score().keys())
    # puntajes trasladados
    assert g2.get_score()[p1.get_nombre()] == 3
    # turno y tamaño de historial preservados
    assert len(g2.get_history()) == len(g.get_history())


import pytest
from backgammon.backgammon.core.game import Game
from backgammon.backgammon.core.player import Player
from backgammon.backgammon.core.dice import Dice


def test_game_repr_y_str_mencionan_jugador_y_marcador():
    g = Game(Player("A"), Player("B"))
    s = str(g)
    r = repr(g)
    assert "Turno de" in s and "Marcador" in s
    # en repr debería aparecer Game( y los dos jugadores
    assert "Game(" in r and "A" in r and "B" in r


def test_game_next_turn_alias_y_current_index():
    p1, p2 = Player("A"), Player("B")
    g = Game(p1, p2)
    idx0 = g.get_current_index()
    g.next_turn()  # alias de change_turn
    idx1 = g.get_current_index()
    assert idx1 in (0, 1) and idx1 != idx0
    # y la property debe “seguir” el índice
    assert g.current_player == g.get_players()[idx1]


def test_game_add_points_rechaza_jugador_ajeno():
    p1, p2, p3 = Player("A"), Player("B"), Player("C")  # p3 NO está en el juego
    g = Game(p1, p2)
    with pytest.raises(ValueError):
        g.add_score(p3, 5)  # usa alias para cubrir ambas rutas


def test_game_to_from_dict_con_historial_y_score():
    p1, p2 = Player("A"), Player("B")
    g = Game(p1, p2, dice=Dice.from_seed(7))
    # generamos historial y sumamos puntos
    g.roll()  # agrega un item al history
    g.add_score(p1, 3)

    d = g.to_dict()
    g2 = Game.from_dict(d)

    # se preserva índice, history y score
    assert g2.get_current_index() == g.get_current_index()
    assert isinstance(g2.get_history(), list) and len(g2.get_history()) >= 1
    s1, s2 = g.get_score(), g2.get_score()
    assert s2.get("A", 0) == s1.get("A", 0) and s2.get("B", 0) == s1.get("B", 0)
