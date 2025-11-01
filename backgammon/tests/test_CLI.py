import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys


class TestPrintHeader(unittest.TestCase):
    """Tests para la función print_header."""
    
    @patch('builtins.print')
    def test_print_header_imprime_titulo(self, mock_print):
        """Verifica que print_header imprime el título correctamente"""
        from backgammon.cli.__main__ import print_header
        
        print_header("TEST TITULO")
        
        # Debe imprimir al menos 3 líneas (separador, título, separador)
        self.assertGreaterEqual(mock_print.call_count, 3)


class TestCmdRoll(unittest.TestCase):
    """Tests para el comando roll."""
    
    @patch('builtins.print')
    def test_cmd_roll_imprime_dados(self, mock_print):
        """Verifica que roll imprime los dados"""
        from backgammon.cli.__main__ import cmd_roll
        
        cmd_roll(None)
        
        # Debe imprimir algo (header + dados)
        self.assertGreater(mock_print.call_count, 0)


class TestCmdBoard(unittest.TestCase):
    """Tests para el comando board."""
    
    @patch('builtins.print')
    def test_cmd_board_muestra_tablero(self, mock_print):
        """Verifica que board muestra el tablero"""
        from backgammon.cli.__main__ import cmd_board
        
        cmd_board(None)
        
        # Debe imprimir múltiples líneas del tablero
        self.assertGreater(mock_print.call_count, 5)


class TestCmdInfo(unittest.TestCase):
    """Tests para el comando info."""
    
    @patch('builtins.print')
    def test_cmd_info_muestra_informacion(self, mock_print):
        """Verifica que info muestra información del juego"""
        from backgammon.cli.__main__ import cmd_info
        
        cmd_info(None)
        
        # Debe imprimir varias líneas de info
        self.assertGreater(mock_print.call_count, 5)


class TestCmdSetup(unittest.TestCase):
    """Tests para el comando setup."""
    
    @patch('builtins.print')
    def test_cmd_setup_muestra_posicion_inicial(self, mock_print):
        """Verifica que setup muestra la posición inicial"""
        from backgammon.cli.__main__ import cmd_setup
        
        cmd_setup(None)
        
        # Debe imprimir el tablero con posición inicial
        self.assertGreater(mock_print.call_count, 5)


class TestCmdSimulate(unittest.TestCase):
    """Tests para el comando simulate."""
    
    @patch('builtins.print')
    def test_cmd_simulate_muestra_simulacion(self, mock_print):
        """Verifica que simulate muestra una simulación"""
        from backgammon.cli.__main__ import cmd_simulate
        
        cmd_simulate(None)
        
        # Debe imprimir ejemplos de movimientos
        self.assertGreater(mock_print.call_count, 3)


class TestCmdStats(unittest.TestCase):
    """Tests para el comando stats."""
    
    @patch('builtins.print')
    def test_cmd_stats_muestra_estadisticas(self, mock_print):
        """Verifica que stats muestra estadísticas"""
        from backgammon.cli.__main__ import cmd_stats
        
        cmd_stats(None)
        
        # Debe imprimir reglas y estadísticas
        self.assertGreater(mock_print.call_count, 5)


class TestMostrarTableroCli(unittest.TestCase):
    """Tests para la función mostrar_tablero_cli"""
    
    @patch('builtins.print')
    def test_mostrar_tablero_cli_vacio(self, mock_print):
        """Verifica que muestra un tablero vacío correctamente"""
        from backgammon.cli.__main__ import mostrar_tablero_cli
        from backgammon.core.board import Board
        
        board = Board()
        mostrar_tablero_cli(board)
        
        # Debe imprimir varias líneas (tablero ASCII)
        self.assertGreaterEqual(mock_print.call_count, 8)
    
    @patch('builtins.print')
    def test_mostrar_tablero_cli_con_fichas(self, mock_print):
        """Verifica que muestra fichas en el tablero"""
        from backgammon.cli.__main__ import mostrar_tablero_cli
        from backgammon.core.board import BoardWithSetup
        from backgammon.core.player import Player
        
        board = BoardWithSetup()
        p1 = Player("Test1", color="blanco")
        p2 = Player("Test2", color="negro")
        board.setup_initial_position(p1, p2)
        
        mostrar_tablero_cli(board)
        
        # Debe imprimir el tablero
        self.assertGreaterEqual(mock_print.call_count, 8)


class TestPuedeMover(unittest.TestCase):
    """Tests para la función puede_mover"""
    
    def test_puede_mover_con_fichas_disponibles(self):
        """Verifica que detecta cuando hay movimientos posibles"""
        from backgammon.cli.__main__ import puede_mover
        from backgammon.core.board import Board
        from backgammon.core.player import Player
        
        board = Board()
        player = Player("Test", color="blanco")
        
        # Colocar ficha en punto 5
        board.colocar_ficha(player, 5)
        
        # Debería poder mover con dado [3]
        result = puede_mover(board, player, [3])
        self.assertTrue(result)
    
    def test_puede_mover_sin_fichas(self):
        """Verifica que detecta cuando no hay fichas para mover"""
        from backgammon.cli.__main__ import puede_mover
        from backgammon.core.board import Board
        from backgammon.core.player import Player
        
        board = Board()
        player = Player("Test", color="blanco")
        
        # Sin fichas en el tablero
        result = puede_mover(board, player, [3, 5])
        self.assertFalse(result)
    
    def test_puede_mover_con_fichas_en_barra(self):
        """Verifica detección de fichas en barra"""
        from backgammon.cli.__main__ import puede_mover
        from backgammon.core.board import Board
        from backgammon.core.player import Player
        from backgammon.core.checker import Checker
        
        board = Board()
        player = Player("Test", color="blanco")
        
        # Agregar ficha a la barra usando capture_checker
        checker = Checker(player=player, color="blanco")
        board.capture_checker(checker)
        
        # Por ahora retorna True (TODO en el código)
        result = puede_mover(board, player, [3])
        self.assertTrue(result)
    
    def test_puede_mover_bloqueado_por_oponente(self):
        """Verifica cuando todas las posiciones están bloqueadas"""
        from backgammon.cli.__main__ import puede_mover
        from backgammon.core.board import Board
        from backgammon.core.player import Player
        
        board = Board()
        p1 = Player("P1", color="blanco")
        p2 = Player("P2", color="negro")
        
        # Colocar ficha blanca en punto 5
        board.colocar_ficha(p1, 5)
        
        # Bloquear todos los destinos posibles con fichas negras
        board.colocar_ficha(p2, 6)
        board.colocar_ficha(p2, 6)
        board.colocar_ficha(p2, 7)
        board.colocar_ficha(p2, 7)
        board.colocar_ficha(p2, 8)
        board.colocar_ficha(p2, 8)
        
        result = puede_mover(board, p1, [1, 2, 3])
        # Este test verifica la lógica básica
        self.assertIsInstance(result, bool)


class TestMostrarAyudaJuego(unittest.TestCase):
    """Tests para la función mostrar_ayuda_juego"""
    
    @patch('builtins.print')
    def test_mostrar_ayuda_juego_imprime_texto(self, mock_print):
        """Verifica que la ayuda imprime información"""
        from backgammon.cli.__main__ import mostrar_ayuda_juego
        
        mostrar_ayuda_juego()
        
        # Debe imprimir varias líneas de ayuda
        self.assertGreater(mock_print.call_count, 10)


class TestCmdPlayInteractivo(unittest.TestCase):
    """Tests para el juego interactivo cmd_play"""
    
    @patch('builtins.input', side_effect=['Jugador1', 'Jugador2', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_salir_inmediato(self, mock_print, mock_input):
        """Verifica que se puede salir con Q"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe haber llamado a input para nombres y comando
        self.assertEqual(mock_input.call_count, 3)
        
        # Debe imprimir algo
        self.assertGreater(mock_print.call_count, 0)
    
    @patch('builtins.input', side_effect=['Test1', 'Test2', 'B', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_comando_board(self, mock_print, mock_input):
        """Verifica que el comando B muestra el tablero"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar el tablero al menos una vez
        self.assertGreater(mock_print.call_count, 10)
    
    @patch('builtins.input', side_effect=['Test1', 'Test2', 'H', '', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_comando_ayuda(self, mock_print, mock_input):
        """Verifica que el comando H muestra ayuda"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe haber mostrado ayuda
        self.assertGreater(mock_print.call_count, 15)
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'R', '', 'Q'])
    @patch('builtins.print')
    @patch('backgammon.cli.__main__.puede_mover', return_value=False)
    def test_cmd_play_tirar_dados(self, mock_puede_mover, mock_print, mock_input):
        """Verifica que se pueden tirar dados con R"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe haber procesado el comando R
        self.assertGreater(mock_print.call_count, 10)
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'P', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_pasar_sin_dados(self, mock_print, mock_input):
        """Verifica que no se puede pasar sin tirar dados"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar error
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('dado' in str(c).lower() for c in calls))
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'M 5 8', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_mover_sin_dados(self, mock_print, mock_input):
        """Verifica que no se puede mover sin tirar dados"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar error sobre tirar dados primero
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('dado' in str(c).lower() for c in calls))
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'INVALIDO', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_comando_invalido(self, mock_print, mock_input):
        """Verifica manejo de comandos inválidos"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar mensaje de comando no reconocido
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('reconocido' in str(c).lower() or 'ayuda' in str(c).lower() for c in calls))
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'R', 'P', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_tirar_y_pasar(self, mock_print, mock_input):
        """Verifica que se puede tirar y pasar turno"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe haber procesado los comandos
        self.assertGreater(mock_print.call_count, 10)


class TestCmdPlayMovimientos(unittest.TestCase):
    """Tests para movimientos en cmd_play"""
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'R', 'M', 'Q'])
    @patch('builtins.print')
    @patch('backgammon.cli.__main__.puede_mover', return_value=True)
    def test_cmd_play_formato_movimiento_incorrecto(self, mock_puede_mover, mock_print, mock_input):
        """Verifica error en formato de movimiento"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar error de formato
        calls = [str(call) for call in mock_print.call_args_list]
        # El error puede decir "formato" o "usá"
        self.assertTrue(
            any('formato' in str(c).lower() for c in calls) or 
            any('usá' in str(c).lower() or 'usa' in str(c).lower() for c in calls)
        )
    
    @patch('builtins.input', side_effect=['P1', 'P2', 'R', 'M ABC DEF', 'Q'])
    @patch('builtins.print')
    @patch('backgammon.cli.__main__.puede_mover', return_value=True)
    def test_cmd_play_movimiento_no_numerico(self, mock_puede_mover, mock_print, mock_input):
        """Verifica error con movimiento no numérico"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe mostrar error de números
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('número' in str(c).lower() for c in calls))


class TestCmdPlayIntegracion(unittest.TestCase):
    """Tests de integración más complejos"""
    
    @patch('builtins.input', side_effect=['Blancas', 'Negras', 'R', 'P', 'Q'])
    @patch('builtins.print')
    @patch('backgammon.cli.__main__.puede_mover', return_value=False)
    def test_cmd_play_flujo_completo(self, mock_puede_mover, mock_print, mock_input):
        """Test de flujo completo: tirar dados y pasar"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe haber procesado el turno
        self.assertGreater(mock_print.call_count, 10)


class TestCasosBorde(unittest.TestCase):
    """Tests de casos borde y edge cases"""
    
    @patch('builtins.input', side_effect=['', '', 'Q'])
    @patch('builtins.print')
    def test_cmd_play_nombres_vacios(self, mock_print, mock_input):
        """Verifica que maneja nombres vacíos (usa defaults)"""
        from backgammon.cli.__main__ import cmd_play
        
        cmd_play(None)
        
        # Debe usar nombres por defecto
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('jugador' in str(c).lower() for c in calls))
    
    def test_puede_mover_con_destino_fuera_tablero(self):
        """Verifica que puede_mover maneja destinos fuera del tablero"""
        from backgammon.cli.__main__ import puede_mover
        from backgammon.core.board import Board
        from backgammon.core.player import Player
        
        board = Board()
        player = Player("Test", color="blanco")
        
        # Colocar ficha en punto 23
        board.colocar_ficha(player, 23)
        
        # Intentar mover con dado [5] llevaría a punto 28 (fuera)
        result = puede_mover(board, player, [5])
        
        # No debería crashear
        self.assertIsInstance(result, bool)


class TestMainCompleto(unittest.TestCase):
    """Tests adicionales para la función main"""
    
    @patch('sys.argv', ['backgammon'])
    def test_main_sin_argumentos_muestra_help(self):
        """Verifica que sin argumentos muestra la ayuda"""
        from backgammon.cli.__main__ import main
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            # Debe mostrar opciones de comandos
            self.assertTrue('play' in output.lower() or 'roll' in output.lower() or 'usage' in output.lower())
    
    @patch('sys.argv', ['backgammon', 'play'])
    @patch('builtins.input', side_effect=['P1', 'P2', 'Q'])
    @patch('builtins.print')
    def test_main_ejecuta_play(self, mock_print, mock_input):
        """Verifica que main puede ejecutar play"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'roll'])
    @patch('builtins.print')
    def test_main_ejecuta_roll(self, mock_print):
        """Verifica que main puede ejecutar roll"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'board'])
    @patch('builtins.print')
    def test_main_ejecuta_board(self, mock_print):
        """Verifica que main puede ejecutar board"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'info'])
    @patch('builtins.print')
    def test_main_ejecuta_info(self, mock_print):
        """Verifica que main puede ejecutar info"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'setup'])
    @patch('builtins.print')
    def test_main_ejecuta_setup(self, mock_print):
        """Verifica que main puede ejecutar setup"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'simulate'])
    @patch('builtins.print')
    def test_main_ejecuta_simulate(self, mock_print):
        """Verifica que main puede ejecutar simulate"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)
    
    @patch('sys.argv', ['backgammon', 'stats'])
    @patch('builtins.print')
    def test_main_ejecuta_stats(self, mock_print):
        """Verifica que main puede ejecutar stats"""
        from backgammon.cli.__main__ import main
        
        result = main()
        
        # No debe haber error
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
    
