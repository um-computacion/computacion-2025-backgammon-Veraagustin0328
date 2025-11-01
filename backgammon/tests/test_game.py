import pytest
from backgammon.core.game import Game
from backgammon.core.board import Board
from backgammon.core.player import Player
from backgammon.core.dice import Dice

"""
Tests para la clase Game.
"""

class TestGameInicializacion:
    """Tests de inicialización del juego."""
    
    def test_game_inicializa_con_dos_jugadores(self):
        """Verifica que el juego se inicializa con 2 jugadores."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_current_player() == p1
        assert g.get_players()[0] == p1
        assert g.get_players()[1] == p2
    
    def test_game_inicializa_con_tablero(self):
        """Verifica que el juego tiene un tablero."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_board() is not None
        assert isinstance(g.get_board(), Board)
    
    def test_game_inicializa_con_dados(self):
        """Verifica que el juego tiene dados."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_dice() is not None
        assert isinstance(g.get_dice(), Dice)


class TestGameTurnos:
    """Tests de cambio de turnos."""
    
    def test_next_turn_cambia_jugador(self):
        """Verifica que next_turn cambia al siguiente jugador."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_current_player() == p1
        g.next_turn()
        assert g.get_current_player() == p2
        g.next_turn()
        assert g.get_current_player() == p1
    
    def test_get_current_player_index(self):
        """Verifica que get_current_player retorna el jugador correcto."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        current = g.get_current_player()
        assert current in [p1, p2]


class TestGameDados:
    """Tests de tirada de dados."""
    
    def test_roll_retorna_valores(self):
        """Verifica que roll retorna valores de dados."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        vals = g.roll()
        assert isinstance(vals, list)
        assert len(vals) in [2, 4]  # 2 normales o 4 si dobles
        assert all(1 <= v <= 6 for v in vals)


class TestGameVictoria:
    """Tests de condiciones de victoria."""
    
    def test_is_game_over_inicialmente_false(self):
        """Verifica que el juego no termina al inicio."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.is_game_over() is False
    
    def test_get_winner_sin_ganador(self):
        """Verifica que no hay ganador al inicio."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_winner() is None


class TestGameValidaciones:
    """Tests de validaciones de movimientos."""
    
    def test_is_valid_move_punto_origen_invalido(self):
        """Verifica que rechaza punto origen inválido."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        g = Game(p1, p2, board=board)
        
        # Punto sin fichas
        assert g.is_valid_move(1, 3, 2) is False
    
    def test_is_valid_move_punto_origen_con_ficha_oponente(self):
        """Verifica que rechaza mover ficha del oponente."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Colocar ficha del jugador 2 en punto 1
        board.colocar_ficha(p2, 1)
        
        g = Game(p1, p2, board=board)
        
        # Jugador 1 intenta mover ficha del jugador 2
        assert g.is_valid_move(1, 3, 2) is False
    
    def test_is_valid_move_valido(self):
        """Verifica movimiento válido."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Colocar ficha del jugador actual
        board.colocar_ficha(p1, 1)
        
        g = Game(p1, p2, board=board)
        
        # Movimiento válido: de 1 a 3 con dado de 2
        assert g.is_valid_move(1, 3, 2) is True
    
    def test_is_valid_move_distancia_incorrecta(self):
        """Verifica que rechaza distancia incorrecta."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        board.colocar_ficha(p1, 1)
        
        g = Game(p1, p2, board=board)
        
        # Movimiento inválido: distancia no coincide con dado
        assert g.is_valid_move(1, 5, 2) is False


class TestGameHomeBoard:
    """Tests de home board."""
    
    def test_is_home_board_loaded_blanco_sin_fichas(self):
        """Verifica que detecta cuando no hay fichas en home."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        g = Game(p1, p2, board=board)
        
        assert g.is_home_board_loaded(p1) is False
    
    def test_is_home_board_loaded_blanco_con_fichas(self):
        """Verifica que detecta fichas en home board."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Colocar todas las fichas en home board (19-24)
        for i in range(19, 25):
            board.colocar_ficha(p1, i)
        
        g = Game(p1, p2, board=board)
        
        assert g.is_home_board_loaded(p1) is True
    
    def test_is_home_board_loaded_negro_sin_fichas(self):
        """Verifica home board para jugador negro."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        g = Game(p1, p2, board=board)
        
        assert g.is_home_board_loaded(p2) is False
    
    def test_is_home_board_loaded_negro_con_fichas(self):
        """Verifica que detecta fichas negras en home board."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Colocar todas las fichas en home board negro (1-6)
        for i in range(1, 7):
            board.colocar_ficha(p2, i)
        
        g = Game(p1, p2, board=board)
        
        assert g.is_home_board_loaded(p2) is True


class TestGameBearOff:
    """Tests de bear off."""
    
    def test_can_bear_off_sin_fichas_en_home(self):
        """Verifica que no puede hacer bear off sin fichas en home."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Fichas fuera del home board
        board.colocar_ficha(p1, 1)
        
        g = Game(p1, p2, board=board)
        
        assert g.can_bear_off(p1) is False
    
    def test_can_bear_off_con_fichas_en_home(self):
        """Verifica que puede hacer bear off con todas en home."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        # Todas las fichas en home board
        for i in range(19, 25):
            board.colocar_ficha(p1, i)
        
        g = Game(p1, p2, board=board)
        
        assert g.can_bear_off(p1) is True


class TestGameMove:
    """Tests del método move."""
    
    def test_move_simple_valido(self):
        """Verifica movimiento simple válido."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        board.colocar_ficha(p1, 1)
        
        g = Game(p1, p2, board=board)
        
        # Mover de 1 a 3
        g.move(1, 3)
        
        assert board.point_count(1) == 0
        assert board.point_count(3) == 1
    
    def test_move_captura_ficha(self):
        """Verifica que move mueve la ficha correctamente."""
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        board = Board()
        
        board.colocar_ficha(p1, 1)
        
        g = Game(p1, p2, board=board)
        
        # Mover ficha
        g.move(1, 3)
        
        assert board.point_count(1) == 0
        assert board.point_count(3) == 1


class TestGameGetters:
    """Tests de métodos getter."""
    
    def test_get_board_retorna_board(self):
        """Verifica que get_board retorna el tablero."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert isinstance(g.get_board(), Board)
    
    def test_get_dice_retorna_dice(self):
        """Verifica que get_dice retorna los dados."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert isinstance(g.get_dice(), Dice)
    
    def test_get_players_retorna_lista(self):
        """Verifica que get_players retorna lista de jugadores."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        players = g.get_players()
        assert isinstance(players, list)
        assert len(players) == 2
        assert p1 in players
        assert p2 in players
        
class TestGameScore:
    """Tests de scoring."""
    
    def test_add_score_agrega_puntos(self):
        """Verifica que add_score suma puntos correctamente."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.add_score(p1, 5)
        score = g.get_score()
        
        assert score["Jugador1"] == 5
        assert score["Jugador2"] == 0
    
    def test_add_score_acumula_puntos(self):
        """Verifica que add_score acumula puntos."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.add_score(p1, 3)
        g.add_score(p1, 2)
        score = g.get_score()
        
        assert score["Jugador1"] == 5
    
    def test_add_points_funciona(self):
        """Verifica que add_points (alias) funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.add_points(p1, 10)
        score = g.get_score()
        
        assert score["Jugador1"] == 10
    
    def test_add_score_jugador_invalido(self):
        """Verifica que rechaza jugador que no está en la partida."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        p3 = Player("Jugador3", color="blanco")
        g = Game(p1, p2)
        
        with pytest.raises(ValueError):
            g.add_score(p3, 5)


class TestGameReset:
    """Tests del método reset."""
    
    def test_reset_limpia_historial(self):
        """Verifica que reset limpia el historial."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.roll()
        g.roll()
        assert len(g.get_history()) == 2
        
        g.reset()
        assert len(g.get_history()) == 0
    
    def test_reset_vuelve_turno_inicial(self):
        """Verifica que reset vuelve al jugador 1."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.next_turn()
        assert g.get_current_player() == p2
        
        g.reset()
        assert g.get_current_player() == p1


class TestGameSwapPlayers:
    """Tests del método swap_players."""
    
    def test_swap_players_intercambia_orden(self):
        """Verifica que swap_players cambia el orden."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_players()[0] == p1
        assert g.get_players()[1] == p2
        
        g.swap_players()
        
        assert g.get_players()[0] == p2
        assert g.get_players()[1] == p1
    
    def test_swap_players_resetea_turno(self):
        """Verifica que swap_players vuelve al turno inicial."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.next_turn()
        assert g.get_current_player() == p2
        
        g.swap_players()
        assert g.get_current_player() == p2  # Ahora p2 está primero


class TestGameSetters:
    """Tests de métodos set."""
    
    def test_set_board_cambia_tablero(self):
        """Verifica que set_board reemplaza el tablero."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        nuevo_board = Board()
        g.set_board(nuevo_board)
        
        assert g.get_board() == nuevo_board
    
    def test_set_board_rechaza_tipo_invalido(self):
        """Verifica que set_board valida el tipo."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        with pytest.raises(TypeError):
            g.set_board("no es un board")
    
    def test_set_dice_cambia_dados(self):
        """Verifica que set_dice reemplaza los dados."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        nuevos_dados = Dice()
        g.set_dice(nuevos_dados)
        
        assert g.get_dice() == nuevos_dados
    
    def test_set_dice_rechaza_tipo_invalido(self):
        """Verifica que set_dice valida el tipo."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        with pytest.raises(TypeError):
            g.set_dice("no son dados")
    
    def test_set_players_cambia_jugadores(self):
        """Verifica que set_players reemplaza jugadores."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        p3 = Player("Jugador3", color="blanco")
        p4 = Player("Jugador4", color="negro")
        
        g.set_players(p3, p4)
        
        assert p3 in g.get_players()
        assert p4 in g.get_players()
    
    def test_set_current_index_cambia_turno(self):
        """Verifica que set_current_index funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        g.set_current_index(1)
        assert g.get_current_player() == p2
    
    def test_set_current_index_rechaza_invalido(self):
        """Verifica que set_current_index valida el rango."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        with pytest.raises(IndexError):
            g.set_current_index(5)


class TestGameSerialization:
    """Tests de serialización."""
    
    def test_to_dict_retorna_dict(self):
        """Verifica que to_dict retorna un diccionario."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        data = g.to_dict()
        
        assert isinstance(data, dict)
        assert "players" in data
        assert "current_index" in data
        assert "score" in data
    
    def test_from_dict_reconstruye_game(self):
        """Verifica que from_dict reconstruye el juego."""
        data = {
            "players": [
                {"nombre": "Test1", "color": "blanco"},
                {"nombre": "Test2", "color": "negro"}
            ],
            "current_index": 0,
            "score": {"Test1": 5, "Test2": 3}
        }
        
        g = Game.from_dict(data)
        
        assert len(g.get_players()) == 2
        assert g.get_players()[0].get_nombre() == "Test1"
        assert g.get_players()[1].get_nombre() == "Test2"


class TestGameProperties:
    """Tests de properties."""
    
    def test_property_players(self):
        """Verifica que la property players funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.players == g.get_players()
    
    def test_property_board(self):
        """Verifica que la property board funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.board == g.get_board()
    
    def test_property_dice(self):
        """Verifica que la property dice funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.dice == g.get_dice()
    
    def test_property_current_player(self):
        """Verifica que la property current_player funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.current_player == g.get_current_player()


class TestGameMiscellaneous:
    """Tests misceláneos."""
    
    def test_last_roll_inicialmente_none(self):
        """Verifica que last_roll es None al inicio."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.last_roll() is None
    
    def test_last_roll_despues_de_tirar(self):
        """Verifica que last_roll retorna la última tirada."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        vals = g.roll()
        last = g.last_roll()
        
        assert last == vals
    
    def test_change_turn_funciona(self):
        """Verifica que change_turn (alias) funciona."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        assert g.get_current_player() == p1
        g.change_turn()
        assert g.get_current_player() == p2
    
    def test_str_representation(self):
        """Verifica que __str__ retorna string legible."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        s = str(g)
        assert isinstance(s, str)
        assert "Jugador1" in s
    
    def test_repr_representation(self):
        """Verifica que __repr__ retorna representación."""
        p1 = Player("Jugador1", color="blanco")
        p2 = Player("Jugador2", color="negro")
        g = Game(p1, p2)
        
        r = repr(g)
        assert isinstance(r, str)
        assert "Game" in r
    