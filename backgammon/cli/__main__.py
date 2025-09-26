import argparse

# Importa core desde el paquete plano si existe; si no, desde backgammon/backgammon
try:
    from backgammon.core.dice import Dice
    from backgammon.core.board import Board
except Exception:
    from backgammon.backgammon.core.dice import Dice
    from backgammon.backgammon.core.board import Board


def _is_double(dice, values):
    # Si el core tiene is_double(), usarlo
    if hasattr(dice, "is_double") and callable(getattr(dice, "is_double")):
        try:
            return bool(dice.is_double())
        except Exception:
            pass
    # Si no, calcularlo a mano
    if isinstance(values, (list, tuple)) and len(values) == 2:
        return values[0] == values[1]
    return False


def _get_points(board):
    # Intentar varios nombres comunes
    for name in ("points", "board", "spaces", "puntos"):
        if hasattr(board, name):
            return getattr(board, name)
    # Fallback: 24 puntos vacíos
    return [[] for _ in range(24)]


def _count_checkers_at(point):
    # Si el punto es una lista de fichas
    try:
        return len(point)
    except Exception:
        # si es int u otra cosa
        if isinstance(point, int):
            return point
        return 0


def _get_map(board, names, default):
    for n in names:
        if hasattr(board, n):
            return getattr(board, n)
    return default


def cmd_roll(_args):
    d = Dice()
    vals = d.roll() if hasattr(d, "roll") else []
    label = " (doble)" if _is_double(d, vals) else ""
    print(f"Dados: {list(vals)}{label}")


def cmd_board(_args):
    b = Board()
    pts = _get_points(b)
    # Si pts no tiene 24 elementos, rellenar/recortar para mostrar 24 posiciones
    if not isinstance(pts, (list, tuple)):
        pts = [[] for _ in range(24)]
    else:
        pts = list(pts)[:24] + ([[]] * max(0, 24 - len(pts)))

    lines = [f"{i:02d}: {_count_checkers_at(p)} fichas" for i, p in enumerate(pts, start=1)]
    print("\n".join(lines))

    bar = _get_map(b, ("bar", "barra"), {"blanco": 0, "negro": 0})
    off = _get_map(b, ("off", "bear_off", "borne_off", "fuera"), {"blanco": 0, "negro": 0})
    print(f"Bar: {bar} | Off: {off}")


def main():
    parser = argparse.ArgumentParser(prog="backgammon", description="CLI mínima de Backgammon (tolerante al core)")
    sub = parser.add_subparsers(dest="cmd")

    p_roll = sub.add_parser("roll", help="tirar los dados")
    p_roll.set_defaults(func=cmd_roll)

    p_board = sub.add_parser("board", help="mostrar tablero")
    p_board.set_defaults(func=cmd_board)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
