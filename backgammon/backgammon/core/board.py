class Board:
    """Tablero del backgammon, donde se ponen las fichas."""

    def __init__(self, puntos=24):
        """Arranca el tablero con 24 puntos, más la barra y las fichas que salieron."""
        self.__puntos = puntos
        self.__bar = {"WHITE": 0, "BLACK": 0}
        self.__borne_off = {"WHITE": 0, "BLACK": 0}

    def get_puntos(self):
        """Devuelve la cantidad de puntos que tiene el tablero (24)."""
        return self.__puntos

    def set_puntos(self, n):
        """Cambia la cantidad de puntos (aunque siempre deberían ser 24)."""
        self.__puntos = int(n)

    def get_bar(self):
        """Devuelve la barra (fichas comidas que esperan para volver a entrar)."""
        return self.__bar

    def set_bar(self, bar):
        """Cambia la barra por lo que le paso."""
        self.__bar = bar

    def get_borne_off(self):
        """Devuelve cuántas fichas ya salieron del tablero."""
        return self.__borne_off

    def set_borne_off(self, bo):
        """Actualiza la cantidad de fichas que ya salieron."""
        self.__borne_off = bo

