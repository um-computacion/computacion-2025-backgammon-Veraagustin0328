import pytest
<<<<<<< HEAD
from backgammon.core.board import Board, BoardWithSetup, BarManager, BearOffManager
from backgammon.core.player import Player


class TestBoardInicializacion:
    """Tests de inicialización del tablero."""
    
    def test_board_inicializacion_basica(self):
        """Verifica que el tablero se inicializa correctamente."""
        b = Board()
        assert isinstance(b.get_estado(), list)
        assert len(b.get_estado()) == 25  # 0 + 24 posiciones
    
    def test_board_inicializa_24_puntos(self):
        """Verifica que se crean 24 puntos."""
        b = Board()
        points = b.get_points()
        assert len(points) == 24
    
    def test_board_puntos_inicialmente_vacios(self):
        """Verifica que todos los puntos inician vacíos."""
        b = Board()
        for i in range(1, 25):
            assert b.point_count(i) == 0
    
    def test_board_bar_inicialmente_vacio(self):
        """Verifica que la barra inicia vacía."""
        b = Board()
        assert b.get_bar_count("blanco") == 0
        assert b.get_bar_count("negro") == 0
    
    def test_board_off_inicialmente_vacio(self):
        """Verifica que bear off inicia vacío."""
        b = Board()
        assert b.get_bear_off_count("blanco") == 0
        assert b.get_bear_off_count("negro") == 0


class TestBoardOperacionesBasicas:
    """Tests de colocar, quitar y mover fichas."""
    
    def test_colocar_ficha(self):
        """Verifica que se puede colocar una ficha."""
        b = Board()
        p = Player("Agus", color="blanco")
        b.colocar_ficha(p, 1)
        assert b.point_count(1) == 1
    
    def test_colocar_multiples_fichas(self):
        """Verifica que se pueden colocar múltiples fichas."""
        b = Board()
        p = Player("Agus", color="blanco")
        b.colocar_ficha(p, 5)
        b.colocar_ficha(p, 5)
        b.colocar_ficha(p, 5)
        assert b.point_count(5) == 3
    
    def test_quitar_ficha(self):
        """Verifica que se puede quitar una ficha."""
        b = Board()
        p = Player("Agus", color="blanco")
        b.colocar_ficha(p, 1)
        removed = b.quitar_ficha(1)
        assert removed == p
        assert b.point_count(1) == 0
    
    def test_quitar_ficha_de_posicion_vacia(self):
        """Verifica que quitar de posición vacía retorna None."""
        b = Board()
        removed = b.quitar_ficha(5)
        assert removed is None
    
    def test_mover_ficha_valida(self):
        """Verifica movimiento válido de ficha."""
        b = Board()
        p = Player("Agus", color="blanco")
        b.colocar_ficha(p, 1)
        b.mover_ficha(1, 3)
        assert b.point_count(1) == 0
        assert b.point_count(3) == 1
    
    def test_mover_ficha_sin_origen(self):
        """Verifica que mover sin ficha en origen lanza error."""
        b = Board()
        with pytest.raises(ValueError, match="No hay fichas"):
            b.mover_ficha(5, 10)
    
    def test_get_top_checker(self):
        """Verifica que retorna la ficha superior."""
        b = Board()
        p1 = Player("P1", color="blanco")
        p2 = Player("P2", color="negro")
        b.colocar_ficha(p1, 5)
        b.colocar_ficha(p2, 5)
        
        top = b.get_top_checker(5)
        assert top == p2
    
    def test_get_top_checker_posicion_vacia(self):
        """Verifica que posición vacía retorna None."""
        b = Board()
        assert b.get_top_checker(5) is None


class TestBoardValidaciones:
    """Tests de validaciones de posiciones."""
    
    def test_colocar_posicion_invalida_menor(self):
        """Verifica que posición < 1 lanza error."""
        b = Board()
        p = Player("Test", color="blanco")
        with pytest.raises(ValueError, match="debe estar entre 1 y 24"):
            b.colocar_ficha(p, 0)
    
    def test_colocar_posicion_invalida_mayor(self):
        """Verifica que posición > 24 lanza error."""
        b = Board()
        p = Player("Test", color="blanco")
        with pytest.raises(ValueError, match="debe estar entre 1 y 24"):
            b.colocar_ficha(p, 25)
    
    def test_quitar_posicion_invalida(self):
        """Verifica validación en quitar."""
        b = Board()
        with pytest.raises(ValueError):
            b.quitar_ficha(0)
        with pytest.raises(ValueError):
            b.quitar_ficha(25)
    
    def test_mover_origen_invalido(self):
        """Verifica que origen inválido lanza error."""
        b = Board()
        with pytest.raises(ValueError):
            b.mover_ficha(0, 5)
    
    def test_mover_destino_invalido(self):
        """Verifica que destino inválido lanza error."""
        b = Board()
        p = Player("Test", color="blanco")
        b.colocar_ficha(p, 5)
        with pytest.raises(ValueError):
            b.mover_ficha(5, 25)
    
    def test_point_count_posicion_invalida(self):
        """Verifica validación en point_count."""
        b = Board()
        with pytest.raises(ValueError):
            b.point_count(0)
        with pytest.raises(ValueError):
            b.point_count(30)


class TestBoardCaptura:
    """Tests de captura de fichas."""
    
    def test_captura_ficha_solitaria(self):
        """Verifica que se captura ficha solitaria del oponente."""
        b = Board()
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        
        b.colocar_ficha(p1, 1)
        b.colocar_ficha(p2, 5)
        
        captured = b.mover_ficha(1, 5)
        
        assert captured == p2
        assert b.get_bar_count("negro") == 1
        assert b.point_count(5) == 1
    
    def test_no_captura_si_multiples_fichas(self):
        """Verifica que no captura si hay 2+ fichas."""
        b = Board()
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        
        b.colocar_ficha(p1, 1)
        b.colocar_ficha(p2, 5)
        b.colocar_ficha(p2, 5)
        
        captured = b.mover_ficha(1, 5)
        
        assert captured is None
        assert b.get_bar_count("negro") == 0
        assert b.point_count(5) == 3
    
    def test_no_captura_ficha_propia(self):
        """Verifica que no captura ficha del mismo color."""
        b = Board()
        p1 = Player("Blanco", color="blanco")
        
        b.colocar_ficha(p1, 1)
        b.colocar_ficha(p1, 5)
        
        captured = b.mover_ficha(1, 5)
        
        assert captured is None
        assert b.point_count(5) == 2




class TestBarManager:
    """Tests del BarManager."""
    
    def test_add_to_bar(self):
        """Verifica agregar ficha a la barra."""
        b = Board()
        b.add_to_bar("blanco")
        assert b.get_bar_count("blanco") == 1
    
    def test_add_multiple_to_bar(self):
        """Verifica agregar múltiples fichas."""
        b = Board()
        b.add_to_bar("negro")
        b.add_to_bar("negro")
        b.add_to_bar("negro")
        assert b.get_bar_count("negro") == 3
    
    def test_remove_from_bar(self):
        """Verifica remover ficha de la barra."""
        b = Board()
        b.add_to_bar("blanco")
        success = b.remove_from_bar("blanco")
        assert success is True
        assert b.get_bar_count("blanco") == 0
    
    def test_remove_from_empty_bar(self):
        """Verifica que remover de barra vacía retorna False."""
        b = Board()
        success = b.remove_from_bar("blanco")
        assert success is False
    
    def test_has_checkers_on_bar(self):
        """Verifica detección de fichas en barra."""
        b = Board()
        assert not b.has_checkers_on_bar("blanco")
        
        b.add_to_bar("blanco")
        assert b.has_checkers_on_bar("blanco")
    
    def test_bar_color_invalido(self):
        """Verifica que color inválido lanza error."""
        b = Board()
        with pytest.raises(ValueError, match="Color inválido"):
            b.add_to_bar("rojo")
        with pytest.raises(ValueError):
            b.remove_from_bar("azul")


class TestBearOffManager:
    """Tests del BearOffManager."""
    
    def test_bear_off_checker(self):
        """Verifica sacar ficha del tablero."""
        b = Board()
        b.bear_off_checker("blanco")
        assert b.get_bear_off_count("blanco") == 1
    
    def test_bear_off_multiple(self):
        """Verifica sacar múltiples fichas."""
        b = Board()
        for _ in range(5):
            b.bear_off_checker("negro")
        assert b.get_bear_off_count("negro") == 5
    
    def test_has_won_con_15_fichas(self):
        """Verifica victoria con 15 fichas fuera."""
        b = Board()
        for _ in range(15):
            b.bear_off_checker("blanco")
        assert b.has_won("blanco")
    
    def test_has_won_con_14_fichas(self):
        """Verifica que 14 fichas no es victoria."""
        b = Board()
        for _ in range(14):
            b.bear_off_checker("blanco")
        assert not b.has_won("blanco")
    
    def test_bear_off_color_invalido(self):
        """Verifica que color inválido lanza error."""
        b = Board()
        with pytest.raises(ValueError, match="Color inválido"):
            b.bear_off_checker("verde")
    

class TestBoardEstado:
    """Tests de consultas de estado."""
    
    def test_get_estado_estructura(self):
        """Verifica estructura del estado."""
        b = Board()
        estado = b.get_estado()
        assert len(estado) == 25
        assert estado[0] is None
    
    def test_get_estado_con_fichas(self):
        """Verifica estado con fichas."""
        b = Board()
        p = Player("Test", color="blanco")
        b.colocar_ficha(p, 5)
        estado = b.get_estado()
        assert estado[5] == "Test"
    
    def test_get_full_state(self):
        """Verifica estado completo."""
        b = Board()
        state = b.get_full_state()
        
        assert "points" in state
        assert "bar" in state
        assert "off" in state
        assert len(state["points"]) == 24
    
    def test_get_points_retorna_copia(self):
        """Verifica que get_points retorna copia."""
        b = Board()
        points1 = b.get_points()
        points2 = b.get_points()
        assert points1 is not points2


class TestBoardProperties:
    """Tests de properties para compatibilidad."""
    
    def test_property_points(self):
        """Verifica property points."""
        b = Board()
        assert len(b.points) == 24
    
    def test_property_bar(self):
        """Verifica property bar."""
        b = Board()
        b.add_to_bar("blanco")
        assert b.bar["blanco"] == 1
    
    def test_property_off(self):
        """Verifica property off."""
        b = Board()
        b.bear_off_checker("negro")
        assert b.off["negro"] == 1

class TestBoardReset:
    """Tests de reinicio del tablero."""
    
    def test_reset_limpia_puntos(self):
        """Verifica que reset limpia los puntos."""
        b = Board()
        p = Player("Test", color="blanco")
        
        for i in range(1, 25):
            b.colocar_ficha(p, i)
        
        b.reset()
        
        for i in range(1, 25):
            assert b.point_count(i) == 0
    
    def test_reset_limpia_barra(self):
        """Verifica que reset limpia la barra."""
        b = Board()
        b.add_to_bar("blanco")
        b.add_to_bar("negro")
        
        b.reset()
        
        assert b.get_bar_count("blanco") == 0
        assert b.get_bar_count("negro") == 0
    
    def test_reset_limpia_bear_off(self):
        """Verifica que reset limpia bear off."""
        b = Board()
        b.bear_off_checker("blanco")
        b.bear_off_checker("negro")
        
        b.reset()
        
        assert b.get_bear_off_count("blanco") == 0
        assert b.get_bear_off_count("negro") == 0


class TestBoardRepresentacion:
    """Tests de __repr__ y __str__."""
    
    def test_repr_contiene_board(self):
        """Verifica que __repr__ contiene 'Board'."""
        b = Board()
        assert "Board" in repr(b)
    
    def test_repr_contiene_info_relevante(self):
        """Verifica que __repr__ tiene info útil."""
        b = Board()
        repr_str = repr(b)
        assert "bar" in repr_str
        assert "off" in repr_str
    
    def test_str_readable(self):
        """Verifica que __str__ es legible."""
        b = Board()
        str_repr = str(b)
        assert "BOARD STATE" in str_repr


class TestBoardWithSetup:
    """Tests de tablero con posición inicial."""
    
    def test_setup_initial_position(self):
        """Verifica configuración de posición inicial."""
        b = BoardWithSetup()
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        
        b.setup_initial_position(p1, p2)
        
        # Verificar fichas blancas
        assert b.point_count(1) == 2
        assert b.point_count(12) == 5
        assert b.point_count(17) == 3
        assert b.point_count(19) == 5
        
        # Verificar fichas negras
        assert b.point_count(24) == 2
        assert b.point_count(13) == 5
        assert b.point_count(8) == 3
        assert b.point_count(6) == 5
    
    def test_setup_limpia_antes(self):
        """Verifica que setup limpia el tablero antes."""
        b = BoardWithSetup()
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        
        # Agregar fichas random
        b.colocar_ficha(p1, 10)
        b.add_to_bar("blanco")
        
        # Setup
        b.setup_initial_position(p1, p2)
        
        # Verificar que se limpió
        assert b.point_count(10) == 0
        assert b.get_bar_count("blanco") == 0


class TestBoardIntegracion:
    """Tests de integración con flujos completos."""
    
    def test_flujo_completo_movimiento_y_captura(self):
        """Test de flujo: colocar, mover, capturar."""
        b = Board()
        p1 = Player("Blanco", color="blanco")
        p2 = Player("Negro", color="negro")
        
        # Colocar fichas
        b.colocar_ficha(p1, 1)
        b.colocar_ficha(p2, 3)
        
        # Mover y capturar
        captured = b.mover_ficha(1, 3)
        
        # Verificaciones
        assert captured == p2
        assert b.point_count(1) == 0
        assert b.point_count(3) == 1
        assert b.get_bar_count("negro") == 1
    
    def test_flujo_completo_bear_off(self):
        """Test de flujo completo hasta bear off."""
        b = Board()
        p = Player("Test", color="blanco")
        
        # Simular fichas en posición para bear off
        for _ in range(15):
            b.bear_off_checker("blanco")
        
        # Verificar victoria
        assert b.has_won("blanco")
        assert b.get_bear_off_count("blanco") == 15
=======
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
>>>>>>> origin/main
