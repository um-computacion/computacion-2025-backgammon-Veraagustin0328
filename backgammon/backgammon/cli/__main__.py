import argparse
from backgammon.core.dice import Dice
from backgammon.core.board import Board


def cmd_roll(_args):
    """Tira los dados y muestra el resultado."""
    d = Dice()
    vals = d.roll()
    label = " (doble)" if d.is_double() else ""
    print(f"Dados: {vals}{label}")


def cmd_board(_args):
    """Muestra un tablero vacío (vista simple)."""
    b = Board()
    lines = []
    for i, p in enumerate(b.points, start=1):
        lines.append(f"{i:02d}: {len(p)} fichas")
    print("\n".join(lines))
    print(f"Bar: {b.bar} | Off: {b.off}")


def main():
    parser = argparse.ArgumentParser(prog="backgammon", description="CLI mínima de Backgammon")
    sub = parser.add_subparsers(dest="cmd")

    p_roll = sub.add_parser("roll", help="tirar los dados")
    p_roll.set_defaults(func=cmd_roll)

    p_board = sub.add_parser("board", help="mostrar tablero vacío")
    p_board.set_defaults(func=cmd_board)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
