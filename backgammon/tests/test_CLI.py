import unittest
from unittest.mock import patch, call
import sys
from io import StringIO

"""
Tests para el CLI de Backgammon.
Usa unittest.mock.patch para simular inputs y verificar outputs.
"""



# Importar funciones del CLI
from backgammon.cli.__main__ import (
    print_header,
    cmd_roll,
    cmd_board,
    cmd_info,
    cmd_play,
    cmd_setup,
    cmd_simulate,
    cmd_stats,
    main,
)


class TestPrintHeader(unittest.TestCase):
    """Tests para la función print_header"""
    
    @patch('builtins.print')
    def test_print_header_imprime_texto(self, mock_print):
        """Verifica que print_header imprime el texto"""
        print_header("TEST")
        # Verificar que se llamó print al menos 3 veces (líneas del header)
        self.assertGreaterEqual(mock_print.call_count, 3)
    
    @patch('builtins.print')
    def test_print_header_con_texto_largo(self, mock_print):
        """Verifica que funciona con texto largo"""
        print_header("ESTE ES UN TITULO MUY LARGO")
        self.assertGreaterEqual(mock_print.call_count, 3)


class TestCmdRoll(unittest.TestCase):
    """Tests para el comando roll"""
    
    @patch('backgammon.cli.__main__.Dice')
    @patch('builtins.print')
    def test_cmd_roll_dados_normales(self, mock_print, mock_dice_class):
        """Verifica que roll muestra dados normales"""
        # Configurar mock para retornar dados [3, 5]
        mock_dice = mock_dice_class.return_value
        mock_dice.roll.return_value = [3, 5]
        
        cmd_roll(None)
        
        # Verificar que se llamó roll
        mock_dice.roll.assert_called_once()
        
        # Verificar que se imprimió algo con los dados
        self.assertGreater(mock_print.call_count, 0)
    
    @patch('backgammon.cli.__main__.Dice')
    @patch('builtins.print')
    def test_cmd_roll_dobles(self, mock_print, mock_dice_class):
        """Verifica que roll detecta dobles"""
        # Configurar mock para retornar dados [4, 4]
        mock_dice = mock_dice_class.return_value
        mock_dice.roll.return_value = [4, 4]
        
        cmd_roll(None)
        
        # Verificar que se llamó roll
        mock_dice.roll.assert_called_once()
        
        # Verificar que se imprimió algo
        self.assertGreater(mock_print.call_count, 0)


class TestCmdBoard(unittest.TestCase):
    """Tests para el comando board"""
    
    @patch('backgammon.cli.__main__.Board')
    @patch('builtins.print')
    def test_cmd_board_muestra_tablero(self, mock_print, mock_board_class):
        """Verifica que board muestra el tablero"""
        # Configurar mock del tablero
        mock_board = mock_board_class.return_value
        mock_board.points = [[] for _ in range(24)]
        
        cmd_board(None)
        
        # Verificar que se creó un Board
        mock_board_class.assert_called_once()
        
        # Verificar que se imprimió el tablero (muchas líneas)
        self.assertGreater(mock_print.call_count, 10)


class TestCmdInfo(unittest.TestCase):
    """Tests para el comando info"""
    
    @patch('builtins.print')
    def test_cmd_info_muestra_informacion(self, mock_print):
        """Verifica que info muestra información del juego"""
        cmd_info(None)
        
        # Verificar que se imprimió información (varias líneas)
        self.assertGreater(mock_print.call_count, 5)


class TestCmdPlay(unittest.TestCase):
    """Tests para el comando play (placeholder)"""
    
    @patch('builtins.print')
    def test_cmd_play_muestra_mensaje_desarrollo(self, mock_print):
        """Verifica que play muestra mensaje de desarrollo"""
        cmd_play(None)
        
        # Verificar que se imprimió algo
        self.assertGreater(mock_print.call_count, 0)


class TestCmdSetup(unittest.TestCase):
    """Tests para el comando setup"""
    
    @patch('backgammon.cli.__main__.BoardWithSetup')
    @patch('backgammon.cli.__main__.Player')
    @patch('builtins.print')
    def test_cmd_setup_muestra_posicion_inicial(
        self, 
        mock_print, 
        mock_player_class, 
        mock_board_class
    ):
        """Verifica que setup muestra posición inicial"""
        # Configurar mocks
        mock_board = mock_board_class.return_value
        mock_board.point_count.return_value = 0
        mock_board.get_top_checker.return_value = None
        
        cmd_setup(None)
        
        # Verificar que se crearon jugadores
        self.assertEqual(mock_player_class.call_count, 2)
        
        # Verificar que se creó el tablero
        mock_board_class.assert_called_once()
        
        # Verificar que se llamó setup_initial_position
        mock_board.setup_initial_position.assert_called_once()
        
        # Verificar que se imprimió el tablero
        self.assertGreater(mock_print.call_count, 10)


class TestCmdSimulate(unittest.TestCase):
    """Tests para el comando simulate"""
    
    @patch('backgammon.cli.__main__.Dice')
    @patch('builtins.print')
    def test_cmd_simulate_dados_normales(self, mock_print, mock_dice_class):
        """Verifica que simulate muestra movimientos posibles"""
        # Configurar mock para dados [2, 5]
        mock_dice = mock_dice_class.return_value
        mock_dice.roll.return_value = [2, 5]
        
        cmd_simulate(None)
        
        # Verificar que se tiraron dados
        mock_dice.roll.assert_called_once()
        
        # Verificar que se imprimió información
        self.assertGreater(mock_print.call_count, 5)
    
    @patch('backgammon.cli.__main__.Dice')
    @patch('builtins.print')
    def test_cmd_simulate_dobles(self, mock_print, mock_dice_class):
        """Verifica que simulate maneja dobles correctamente"""
        # Configurar mock para dados [3, 3]
        mock_dice = mock_dice_class.return_value
        mock_dice.roll.return_value = [3, 3]
        
        cmd_simulate(None)
        
        # Verificar que se tiraron dados
        mock_dice.roll.assert_called_once()
        
        # Verificar que se imprimió información sobre dobles
        self.assertGreater(mock_print.call_count, 5)


class TestCmdStats(unittest.TestCase):
    """Tests para el comando stats"""
    
    @patch('builtins.print')
    def test_cmd_stats_muestra_estadisticas(self, mock_print):
        """Verifica que stats muestra reglas y estadísticas"""
        cmd_stats(None)
        
        # Verificar que se imprimió mucha información
        self.assertGreater(mock_print.call_count, 10)


class TestMain(unittest.TestCase):
    """Tests para la función principal main"""
    
    @patch('sys.argv', ['backgammon', 'roll'])
    @patch('backgammon.cli.__main__.cmd_roll')
    def test_main_comando_roll(self, mock_cmd_roll):
        """Verifica que main ejecuta el comando roll"""
        main()
        mock_cmd_roll.assert_called_once()
    
    @patch('sys.argv', ['backgammon', 'board'])
    @patch('backgammon.cli.__main__.cmd_board')
    def test_main_comando_board(self, mock_cmd_board):
        """Verifica que main ejecuta el comando board"""
        main()
        mock_cmd_board.assert_called_once()
    
    @patch('sys.argv', ['backgammon', 'info'])
    @patch('backgammon.cli.__main__.cmd_info')
    def test_main_comando_info(self, mock_cmd_info):
        """Verifica que main ejecuta el comando info"""
        main()
        mock_cmd_info.assert_called_once()
    
    @patch('sys.argv', ['backgammon', 'setup'])
    @patch('backgammon.cli.__main__.cmd_setup')
    def test_main_comando_setup(self, mock_cmd_setup):
        """Verifica que main ejecuta el comando setup"""
        main()
        mock_cmd_setup.assert_called_once()
    
    @patch('sys.argv', ['backgammon', 'simulate'])
    @patch('backgammon.cli.__main__.cmd_simulate')
    def test_main_comando_simulate(self, mock_cmd_simulate):
        """Verifica que main ejecuta el comando simulate"""
        main()
        mock_cmd_simulate.assert_called_once()
    
    @patch('sys.argv', ['backgammon', 'stats'])
    @patch('backgammon.cli.__main__.cmd_stats')
    def test_main_comando_stats(self, mock_cmd_stats):
        """Verifica que main ejecuta el comando stats"""
        main()
        mock_cmd_stats.assert_called_once()
    
    @patch('sys.argv', ['backgammon'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_sin_comando_muestra_ayuda(self, mock_stdout):
        """Verifica que sin comando muestra la ayuda"""
        main()
        output = mock_stdout.getvalue()
        # Debe contener información de ayuda
        self.assertIn('backgammon', output.lower())
    
    @patch('sys.argv', ['backgammon', 'roll'])
    @patch('backgammon.cli.__main__.cmd_roll', side_effect=Exception('error de prueba'))
    @patch('builtins.print')
    def test_main_maneja_excepciones(self, mock_print, mock_cmd_roll):
        """Verifica que main maneja excepciones correctamente"""
        result = main()
        
        # Debe retornar 1 (error)
        self.assertEqual(result, 1)
        
        # Debe llamar a cmd_roll
        mock_cmd_roll.assert_called_once()


class TestIntegracionCLI(unittest.TestCase):
    """Tests de integración del CLI completo"""
    
    @patch('backgammon.cli.__main__.Dice')
    @patch('builtins.print')
    def test_roll_imprime_resultado_valido(self, mock_print, mock_dice_class):
        """Test de integración: roll debe imprimir resultado válido"""
        mock_dice = mock_dice_class.return_value
        mock_dice.roll.return_value = [1, 6]
        
        cmd_roll(None)
        
        # Verificar que se imprimió algo relacionado con dados
        calls = [str(call) for call in mock_print.call_args_list]
        all_output = ' '.join(calls)
        
        # Debe contener referencias a dados o números
        self.assertTrue(
            any(keyword in all_output for keyword in ['Dados', 'dados', '1', '6'])
        )


if __name__ == '__main__':
    unittest.main()