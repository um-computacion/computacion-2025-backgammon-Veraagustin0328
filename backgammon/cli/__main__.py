import argparse
import sys

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback sin colores
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

from backgammon.core.dice import Dice
from backgammon.core.board import Board, BoardWithSetup
from backgammon.core.player import Player


def print_header(text):
    """Imprime un header colorido."""
    if HAS_COLOR:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{text:^50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*50}{Style.RESET_ALL}\n")
    else:
        print(f"\n{'='*50}")
        print(f"{text:^50}")
        print(f"{'='*50}\n")


def cmd_roll(_args):
    """Tira los dados y muestra el resultado con colores."""
    print_header("TIRANDO DADOS")
    
    d = Dice()
    vals = d.roll()
    
    is_double = vals[0] == vals[1] if len(vals) == 2 else False
    
    if is_double:
        print(f"{Fore.YELLOW}{Style.BRIGHT}¡DOBLES!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Dados: [{vals[0]}] [{vals[1]}] [{vals[0]}] [{vals[1]}]{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Podés mover 4 veces con el valor {vals[0]}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Dados: [{vals[0]}] [{vals[1]}]{Style.RESET_ALL}")
        print(f"Podés mover con {vals[0]} o {vals[1]}")


def cmd_board(_args):
    """Muestra el tablero con ASCII art mejorado."""
    print_header("TABLERO DE BACKGAMMON")
    
    b = Board()
    
    # Crear visualización del tablero
    print("┌─────────────────────────────────────────────────────────────┐")
    
    # Top half (puntos 13-24)
    top_nums = "│ " + "  ".join([f"{i:2d}" for i in range(13, 19)]) + " │ BAR │ " + "  ".join([f"{i:2d}" for i in range(19, 25)]) + " │"
    print(top_nums)
    
    # Fichas superiores (simplificado - muestra cantidad)
    top_checkers = []
    for i in range(12, 24):
        count = len(b.points[i]) if i < len(b.points) else 0
        if count == 0:
            top_checkers.append(" -- ")
        elif count < 10:
            top_checkers.append(f" {Fore.WHITE}●{count}{Style.RESET_ALL} " if count > 0 else " -- ")
        else:
            top_checkers.append(f"{Fore.WHITE}{count:2d}{Style.RESET_ALL} ")
    
    line1 = "│ " + "  ".join(top_checkers[:6]) + " │     │ " + "  ".join(top_checkers[6:]) + " │"
    print(line1)
    
    # Línea divisoria
    print("├─────────────────────────────────────────────────────────────┤")
    
    # Bottom half (puntos 12-1)
    bottom_checkers = []
    for i in range(11, -1, -1):
        count = len(b.points[i]) if i < len(b.points) else 0
        if count == 0:
            bottom_checkers.append(" -- ")
        elif count < 10:
            bottom_checkers.append(f" {Fore.RED}○{count}{Style.RESET_ALL} " if count > 0 else " -- ")
        else:
            bottom_checkers.append(f"{Fore.RED}{count:2d}{Style.RESET_ALL} ")
    
    line2 = "│ " + "  ".join(bottom_checkers[:6]) + " │ OFF │ " + "  ".join(bottom_checkers[6:]) + " │"
    print(line2)
    
    bottom_nums = "│ " + "  ".join([f"{i:2d}" for i in range(12, 6, -1)]) + " │     │ " + "  ".join([f"{i:2d}" for i in range(6, 0, -1)]) + " │"
    print(bottom_nums)
    
    print("└─────────────────────────────────────────────────────────────┘")
    
    # Info adicional
    print(f"\n{Fore.CYAN}Estado:{Style.RESET_ALL}")
    
    # Bar
    bar_white = len([c for c in getattr(b, 'bar', []) if hasattr(c, 'color') and c.color == 'blanco'])
    bar_black = len([c for c in getattr(b, 'bar', []) if hasattr(c, 'color') and c.color == 'negro'])
    
    print(f"  {Fore.YELLOW}Bar:{Style.RESET_ALL} Blancas: {bar_white}, Negras: {bar_black}")
    
    # Off
    off_white = 0
    off_black = 0
    if hasattr(b, 'off'):
        off_white = b.off.get('blanco', 0)
        off_black = b.off.get('negro', 0)
    
    print(f"  {Fore.GREEN}Off (Bear Off):{Style.RESET_ALL} Blancas: {off_white}, Negras: {off_black}")


def cmd_info(_args):
    """Muestra información sobre el juego."""
    print_header("INFORMACION DE BACKGAMMON")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}Objetivo:{Style.RESET_ALL}")
    print("  Mover todas tus fichas al 'home board' y sacarlas del tablero (bear off).")
    print("  El primer jugador en sacar las 15 fichas gana.\n")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}Comandos disponibles:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}roll{Style.RESET_ALL}  - Tirar los dados")
    print(f"  {Fore.GREEN}board{Style.RESET_ALL} - Mostrar el tablero")
    print(f"  {Fore.GREEN}info{Style.RESET_ALL}  - Mostrar esta información")
    print(f"  {Fore.GREEN}play{Style.RESET_ALL}  - Jugar una partida interactiva (próximamente)")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Reglas básicas:{Style.RESET_ALL}")
    print("  • Cada jugador tiene 15 fichas (blancas o negras)")
    print("  • Las blancas se mueven de 1→24, las negras de 24→1")
    print("  • Si sacás dobles, movés 4 veces ese número")
    print("  • Podés capturar fichas solitarias del oponente")
    print("  • Las fichas capturadas van a la 'barra' y deben re-entrar")


def cmd_play(_args):
    """Comando para jugar (placeholder por ahora)."""
    print_header("MODO JUEGO")
    print(f"{Fore.YELLOW}Este comando está en desarrollo.{Style.RESET_ALL}")
    print("Por ahora podés usar:")
    print(f"  • {Fore.GREEN}roll{Style.RESET_ALL} para tirar dados")
    print(f"  • {Fore.GREEN}board{Style.RESET_ALL} para ver el tablero")
    print(f"\n{Fore.CYAN}Próximamente: partida interactiva completa!{Style.RESET_ALL}")


def cmd_setup(_args):
    """Muestra el tablero con la posición inicial estándar."""
    print_header("TABLERO - POSICION INICIAL")
    
    # Crear tablero con setup
    b = BoardWithSetup()
    p1 = Player("Blancas", color="blanco")
    p2 = Player("Negras", color="negro")
    
    b.setup_initial_position(p1, p2)
    
    # Mostrar tablero con ASCII art
    print("┌─────────────────────────────────────────────────────────────┐")
    
    # Top half (puntos 13-24)
    top_nums = "│ " + "  ".join([f"{i:2d}" for i in range(13, 19)]) + " │ BAR │ " + "  ".join([f"{i:2d}" for i in range(19, 25)]) + " │"
    print(top_nums)
    
    # Fichas superiores (puntos 13-24)
    top_checkers = []
    for i in range(13, 25):
        count = b.point_count(i)
        if count == 0:
            top_checkers.append(" -- ")
        else:
            top_checker = b.get_top_checker(i)
            if hasattr(top_checker, 'get_color'):
                color = top_checker.get_color()
                symbol = f"{Fore.WHITE}●{Style.RESET_ALL}" if color == "blanco" else f"{Fore.RED}○{Style.RESET_ALL}"
            else:
                symbol = "●"
            
            if count < 10:
                top_checkers.append(f" {symbol}{count} ")
            else:
                top_checkers.append(f"{symbol}{count:2d}")
    
    line1 = "│ " + "  ".join(top_checkers[:6]) + " │     │ " + "  ".join(top_checkers[6:]) + " │"
    print(line1)
    
    # Línea divisoria
    print("├─────────────────────────────────────────────────────────────┤")
    
    # Bottom half (puntos 12-1)
    bottom_checkers = []
    for i in range(12, 0, -1):
        count = b.point_count(i)
        if count == 0:
            bottom_checkers.append(" -- ")
        else:
            bottom_checker = b.get_top_checker(i)
            if hasattr(bottom_checker, 'get_color'):
                color = bottom_checker.get_color()
                symbol = f"{Fore.WHITE}●{Style.RESET_ALL}" if color == "blanco" else f"{Fore.RED}○{Style.RESET_ALL}"
            else:
                symbol = "○"
            
            if count < 10:
                bottom_checkers.append(f" {symbol}{count} ")
            else:
                bottom_checkers.append(f"{symbol}{count:2d}")
    
    line2 = "│ " + "  ".join(bottom_checkers[:6]) + " │ OFF │ " + "  ".join(bottom_checkers[6:]) + " │"
    print(line2)
    
    bottom_nums = "│ " + "  ".join([f"{i:2d}" for i in range(12, 6, -1)]) + " │     │ " + "  ".join([f"{i:2d}" for i in range(6, 0, -1)]) + " │"
    print(bottom_nums)
    
    print("└─────────────────────────────────────────────────────────────┘")
    
    print(f"\n{Fore.GREEN}Posición inicial estándar del Backgammon{Style.RESET_ALL}")
    print(f"  • Blancas: {Fore.WHITE}●{Style.RESET_ALL} (mueven de 1→24)")
    print(f"  • Negras: {Fore.RED}○{Style.RESET_ALL} (mueven de 24→1)")


def cmd_simulate(_args):
    """Simula una tirada de dados y muestra posibles movimientos."""
    print_header("SIMULACION DE TIRADA")
    
    d = Dice()
    vals = d.roll()
    
    is_double = vals[0] == vals[1]
    
    print(f"{Fore.CYAN}Dados:{Style.RESET_ALL} [{vals[0]}] [{vals[1]}]")
    
    if is_double:
        print(f"{Fore.YELLOW}¡DOBLES!{Style.RESET_ALL} Podés mover 4 veces con el valor {vals[0]}")
        moves = [vals[0]] * 4
    else:
        print(f"Movimientos posibles: {vals[0]} o {vals[1]}")
        moves = list(vals)
    
    print(f"\n{Fore.CYAN}Ejemplos de movimientos:{Style.RESET_ALL}")
    
    if is_double:
        print(f"  • Mover una ficha del punto X al punto X+{vals[0]} (4 veces)")
        print(f"  • Mover 4 fichas diferentes, cada una {vals[0]} espacios")
        print(f"  • Combinar: 2 fichas {vals[0]} espacios, 2 veces")
    else:
        print(f"  • Mover una ficha {vals[0]} espacios desde el punto X")
        print(f"  • Mover otra ficha {vals[1]} espacios desde el punto Y")
        print(f"  • O mover la misma ficha {vals[0]}+{vals[1]}={vals[0]+vals[1]} espacios totales")
    
    print(f"\n{Fore.GREEN}Tip:{Style.RESET_ALL} Siempre debés usar todos los movimientos disponibles si es posible.")


def cmd_stats(_args):
    """Muestra estadísticas y reglas del tablero."""
    print_header("ESTADISTICAS Y REGLAS")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}Estructura del tablero:{Style.RESET_ALL}")
    print(f"  • {Fore.GREEN}24 puntos{Style.RESET_ALL} numerados del 1 al 24")
    print(f"  • {Fore.YELLOW}Barra (BAR){Style.RESET_ALL} - donde van las fichas capturadas")
    print(f"  • {Fore.MAGENTA}Bear Off (OFF){Style.RESET_ALL} - donde se sacan las fichas del juego")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Cada jugador:{Style.RESET_ALL}")
    print(f"  • Tiene {Fore.GREEN}15 fichas{Style.RESET_ALL}")
    print(f"  • Blancas: mueven de {Fore.WHITE}1→24{Style.RESET_ALL}")
    print(f"  • Negras: mueven de {Fore.RED}24→1{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Home Board:{Style.RESET_ALL}")
    print(f"  • Blancas: puntos {Fore.WHITE}19-24{Style.RESET_ALL}")
    print(f"  • Negras: puntos {Fore.RED}1-6{Style.RESET_ALL}")
    print(f"  • Solo podés hacer bear off cuando todas tus fichas estén en tu home board")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Reglas de captura:{Style.RESET_ALL}")
    print(f"  • Podés capturar una ficha {Fore.YELLOW}solitaria{Style.RESET_ALL} del oponente")
    print(f"  • La ficha capturada va a la {Fore.YELLOW}barra{Style.RESET_ALL}")
    print(f"  • Debe re-entrar al tablero antes de mover otras fichas")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Objetivo:{Style.RESET_ALL}")
    print(f"  • Llevar las 15 fichas a tu home board")
    print(f"  • Sacarlas del tablero (bear off)")
    print(f"  • {Fore.GREEN}¡El primero en sacar las 15 fichas gana!{Style.RESET_ALL}")


def main():
    """Función principal de la CLI."""
    parser = argparse.ArgumentParser(
        prog="backgammon",
        description=f"{Fore.CYAN}CLI de Backgammon{Style.RESET_ALL} - Juego de mesa clásico",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  backgammon roll          Tirar los dados
  backgammon board         Ver el tablero
  backgammon info          Ver información del juego
  backgammon play          Jugar una partida (en desarrollo)
        """
    )
    
    sub = parser.add_subparsers(dest="cmd", title="Comandos disponibles")
    
    # Comando roll
    p_roll = sub.add_parser("roll", help="Tirar los dados")
    p_roll.set_defaults(func=cmd_roll)
    
    # Comando board
    p_board = sub.add_parser("board", help="Mostrar tablero con ASCII art")
    p_board.set_defaults(func=cmd_board)
    
    # Comando info
    p_info = sub.add_parser("info", help="Mostrar información del juego")
    p_info.set_defaults(func=cmd_info)
    
    # Comando play
    p_play = sub.add_parser("play", help="Jugar una partida interactiva")
    p_play.set_defaults(func=cmd_play)
    
    # Comando setup
    p_setup = sub.add_parser("setup", help="Mostrar tablero con posición inicial")
    p_setup.set_defaults(func=cmd_setup)
    
    # Comando simulate
    p_simulate = sub.add_parser("simulate", help="Simular una tirada y mostrar movimientos")
    p_simulate.set_defaults(func=cmd_simulate)
    
    # Comando stats
    p_stats = sub.add_parser("stats", help="Mostrar estadísticas y reglas del juego")
    p_stats.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
