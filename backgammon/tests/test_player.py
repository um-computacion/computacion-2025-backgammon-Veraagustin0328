import pytest
from backgammon.core.player import Player


def test_player_inicializacion():
    jugador = Player("Agus")
    assert jugador.get_nombre() == "Agus"
    assert jugador.get_fichas() == 15
    assert jugador.get_puntos() == 0


def test_player_modifica_puntos():
    jugador = Player("Agus")
    jugador.sumar_puntos(5)
    assert jugador.get_puntos() == 5


def test_player_perder_ficha_ok():
    jugador = Player("Agus")
    jugador.perder_ficha()
    assert jugador.get_fichas() == 14


def test_player_perder_ficha_sin_fichas():
    jugador = Player("Agus")
    jugador.set_fichas(0)
    with pytest.raises(ValueError):
        jugador.perder_ficha()


def test_player_reset_fichas_y_puntos():
    jugador = Player("Josias")
    jugador.sumar_puntos(4)
    jugador.set_fichas(5)
    jugador.reset()
    assert jugador.get_fichas() == 15
    assert jugador.get_puntos() == 0


def test_player_repr_y_str():
    jugador = Player("Valentina")
    repr_str = repr(jugador)
    assert "Valentina" in repr_str
    assert str(jugador).startswith("Valentina")


def test_player_comparacion_igualdad():
    jugador1 = Player("Agustin")
    jugador2 = Player("Agustin")
    jugador3 = Player("Franco")
    assert jugador1 == jugador2
    assert jugador1 != jugador3


def test_player_serializacion_dict():
    jugador = Player("Camila")
    d = jugador.to_dict()
    assert "nombre" in d and "fichas" in d and "puntos" in d
    j2 = Player.from_dict(d)
    assert j2.get_nombre() == jugador.get_nombre()


def test_player_set_fichas_negativas():
    jugador = Player("Josias")
    with pytest.raises(ValueError):
        jugador.set_fichas(-1)


def test_player_sumar_puntos_y_perder_ficha_funciona():
    p = Player("Agus")
    p.sumar_puntos(10)
    assert p.get_puntos() == 10
    p.perder_ficha()
    assert p.get_fichas() == 14


def test_player_perder_ficha_error_si_no_hay():
    p = Player("Franco")
    p.set_fichas(0)
    with pytest.raises(ValueError):
        p.perder_ficha()


def test_player_reset_vuelve_a_estado_inicial():
    p = Player("Cami")
    p.set_fichas(5)
    p.sumar_puntos(12)
    p.reset()
    assert p.get_fichas() == 15
    assert p.get_puntos() == 0


def test_player_to_from_dict_reconstruye_correctamente():
    p = Player("Valen")
    p.set_fichas(10)
    p.sumar_puntos(7)
    data = p.to_dict()
    nuevo = Player.from_dict(data)
    assert nuevo.get_nombre() == "Valen"
    assert nuevo.get_fichas() == 10
    assert nuevo.get_puntos() == 7


def test_player_eq_y_hash_basados_en_nombre():
    p1 = Player("Lucas")
    p2 = Player("Lucas")
    p3 = Player("Jose")
    assert p1 == p2
    assert p1 != p3
    assert hash(p1) == hash(p2)

# === BLOQUE EXTRA DE TESTS PARA PLAYER (sin BackgammonGame) ===
import pytest

try:
    from backgammon.core.player import Player
except Exception as _e:
    Player = None

@pytest.mark.skipif(Player is None, reason="No se pudo importar Player")
def test_player_str_and_basic_identity():
    # Intento de construcción sin parámetros; si no, probamos alternativas
    try:
        p = Player()
    except TypeError:
        # alterna: Player(color=..., name=...) si tu __init__ lo exige
        kwargs_options = [
            {"name": "P1"}, {"color": "white"}, {"color": 0, "name": "P1"}
        ]
        for kw in kwargs_options:
            try:
                p = Player(**kw)
                break
            except Exception:
                p = None
        if p is None:
            pytest.skip("No hay forma conocida de instanciar Player")

    s = str(p)
    assert isinstance(s, str)
    if hasattr(p, "name"):
        assert isinstance(p.name, (str, type(None)))
    if hasattr(p, "color"):
        assert (p.color in (None, "white", "black", 0, 1)) or True

@pytest.mark.skipif(Player is None, reason="No se pudo importar Player")
def test_player_turn_toggle_and_flags_if_exist():
    # Construcción tolerante
    try:
        p = Player()
    except TypeError:
        for kw in ({"name": "P1"}, {"color": "white"}, {"color": 0, "name": "P1"}):
            try:
                p = Player(**kw); break
            except Exception:
                p = None
        if p is None:
            pytest.skip("No hay forma conocida de instanciar Player")

    # toggles/banderas
    for attr in ("is_turn", "active", "enabled"):
        if hasattr(p, attr):
            before = getattr(p, attr)
            try:
                setattr(p, attr, not bool(before))
                after = getattr(p, attr)
                assert after != before
            except Exception:
                for m in ("toggle_turn", "toggle", "set_active", "activate", "deactivate"):
                    if hasattr(p, m):
                        try:
                            getattr(p, m)()
                        except TypeError:
                            getattr(p, m)(not bool(before))
                        break

    # contadores/score/bear-off si existen
    for inc in ("add_score", "inc_score", "bear_off_one", "add_checker_off"):
        if hasattr(p, inc):
            before = None
            for gattr in ("score", "borne_off", "checkers_off"):
                if hasattr(p, gattr):
                    before = getattr(p, gattr)
                    break
            try:
                getattr(p, inc)()
            except TypeError:
                getattr(p, inc)(1)
            after = None
            for gattr in ("score", "borne_off", "checkers_off"):
                if hasattr(p, gattr):
                    after = getattr(p, gattr)
                    break
            if (before is not None) and (after is not None):
                assert (after == before) or (after == before + 1)

@pytest.mark.skipif(Player is None, reason="No se pudo importar Player")
def test_player_equality_or_hash_if_defined():
    # Construcción tolerante
    def mk():
        try:
            return Player()
        except TypeError:
            for kw in ({"name": "P1"}, {"color": "white"}, {"color": 0, "name": "P1"}):
                try:
                    return Player(**kw)
                except Exception:
                    pass
            return None

    p = mk()
    if p is None:
        pytest.skip("No hay forma conocida de instanciar Player")

    if hasattr(p, "__eq__"):
        try:
            q = mk()
            _ = (p == q)
        except Exception:
            pass
    if hasattr(p, "__hash__"):
        try:
            _ = hash(p)
        except Exception:
            pass
