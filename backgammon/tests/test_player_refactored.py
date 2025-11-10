import pytest
from backgammon.core.player_refactored import (
    PlayerIdentity,
    PlayerInventory,
    PlayerScore,
    PlayerFacade
)


class TestPlayerIdentity:
    """Tests para PlayerIdentity (SRP: solo identidad)"""
    
    def test_inicializacion_basica(self):
        identity = PlayerIdentity("Agus", "blanco")
        assert identity.get_nombre() == "Agus"
        assert identity.get_color() == "blanco"
    
    def test_nombre_vacio_usa_default(self):
        identity = PlayerIdentity("", "blanco")
        assert identity.get_nombre() == "Jugador"
    
    def test_color_invalido_usa_default(self):
        identity = PlayerIdentity("Test", "rojo")
        assert identity.get_color() == "blanco"
    
    def test_set_nombre_valido(self):
        identity = PlayerIdentity("Test", "blanco")
        identity.set_nombre("Nuevo")
        assert identity.get_nombre() == "Nuevo"
    
    def test_set_nombre_vacio_lanza_error(self):
        identity = PlayerIdentity("Test", "blanco")
        with pytest.raises(ValueError):
            identity.set_nombre("")
    
    def test_set_color_valido(self):
        identity = PlayerIdentity("Test", "blanco")
        identity.set_color("negro")
        assert identity.get_color() == "negro"
    
    def test_set_color_invalido_lanza_error(self):
        identity = PlayerIdentity("Test", "blanco")
        with pytest.raises(ValueError):
            identity.set_color("rojo")


class TestPlayerInventory:
    """Tests para PlayerInventory (SRP: solo fichas)"""
    
    def test_inicializacion_default(self):
        inventory = PlayerInventory()
        assert inventory.get_fichas() == 15
    
    def test_inicializacion_custom(self):
        inventory = PlayerInventory(10)
        assert inventory.get_fichas() == 10
    
    def test_set_fichas_valido(self):
        inventory = PlayerInventory()
        inventory.set_fichas(10)
        assert inventory.get_fichas() == 10
    
    def test_set_fichas_negativo_lanza_error(self):
        inventory = PlayerInventory()
        with pytest.raises(ValueError):
            inventory.set_fichas(-1)
    
    def test_perder_ficha(self):
        inventory = PlayerInventory()
        inventory.perder_ficha()
        assert inventory.get_fichas() == 14
    
    def test_perder_ficha_sin_fichas_lanza_error(self):
        inventory = PlayerInventory(0)
        with pytest.raises(ValueError):
            inventory.perder_ficha()
    
    def test_reset(self):
        inventory = PlayerInventory()
        inventory.set_fichas(5)
        inventory.reset()
        assert inventory.get_fichas() == 15


class TestPlayerScore:
    """Tests para PlayerScore (SRP: solo puntuación)"""
    
    def test_inicializacion_default(self):
        score = PlayerScore()
        assert score.get_puntos() == 0
    
    def test_inicializacion_custom(self):
        score = PlayerScore(10)
        assert score.get_puntos() == 10
    
    def test_set_puntos(self):
        score = PlayerScore()
        score.set_puntos(5)
        assert score.get_puntos() == 5
    
    def test_sumar_puntos(self):
        score = PlayerScore()
        score.sumar_puntos(3)
        score.sumar_puntos(2)
        assert score.get_puntos() == 5
    
    def test_reset(self):
        score = PlayerScore()
        score.sumar_puntos(10)
        score.reset()
        assert score.get_puntos() == 0


class TestPlayerRefactored:
    """Tests para PlayerRefactored (Facade Pattern)"""
    
    def test_inicializacion_basica(self):
        player = PlayerFacade("Agus", "blanco")
        assert player.get_nombre() == "Agus"
        assert player.get_color() == "blanco"
        assert player.get_fichas() == 15
        assert player.get_puntos() == 0
    
    def test_delegacion_a_identity(self):
        player = PlayerFacade("Test", "blanco")
        player.set_nombre("Nuevo")
        assert player.get_nombre() == "Nuevo"
        
        player.set_color("negro")
        assert player.get_color() == "negro"
    
    def test_delegacion_a_inventory(self):
        player = PlayerFacade("Test", "blanco")
        player.set_fichas(10)
        assert player.get_fichas() == 10
        
        player.perder_ficha()
        assert player.get_fichas() == 9
    
    def test_delegacion_a_score(self):
        player = PlayerFacade("Test", "blanco")
        player.sumar_puntos(5)
        assert player.get_puntos() == 5
    
    def test_reset_completo(self):
        player = PlayerFacade("Test", "blanco")
        player.set_fichas(5)
        player.sumar_puntos(10)
        
        player.reset()
        
        assert player.get_fichas() == 15
        assert player.get_puntos() == 0
    
    def test_to_dict(self):
        player = PlayerFacade("Test", "negro")
        player.set_fichas(12)
        player.sumar_puntos(7)
        
        data = player.to_dict()
        
        assert data["nombre"] == "Test"
        assert data["color"] == "negro"
        assert data["fichas"] == 12
        assert data["puntos"] == 7
    
    def test_from_dict(self):
        data = {
            "nombre": "FromDict",
            "color": "blanco",
            "fichas": 10,
            "puntos": 5
        }
        
        player = PlayerFacade.from_dict(data)
        
        assert player.get_nombre() == "FromDict"
        assert player.get_color() == "blanco"
        assert player.get_fichas() == 10
        assert player.get_puntos() == 5
    
    def test_str_representation(self):
        player = PlayerFacade("Test", "blanco")
        assert "Test" in str(player)
        assert "blanco" in str(player)
    
    def test_repr_representation(self):
        player = PlayerFacade("Test", "negro")
        repr_str = repr(player)
        assert "PlayerFacade" in repr_str
        assert "SOLID=True" in repr_str
    
    def test_eq_con_mismo_nombre(self):
        p1 = PlayerFacade("Test", "blanco")
        p2 = PlayerFacade("Test", "negro")
        assert p1 == p2
    
    def test_eq_con_diferente_nombre(self):
        p1 = PlayerFacade("Test1", "blanco")
        p2 = PlayerFacade("Test2", "blanco")
        assert p1 != p2
    
    def test_hash(self):
        p1 = PlayerFacade("Test", "blanco")
        p2 = PlayerFacade("Test", "negro")
        assert hash(p1) == hash(p2)
    
    def test_inyeccion_dependencias_identity(self):
        """Test DIP: inyección de componente Identity"""
        custom_identity = PlayerIdentity("Custom", "negro")
        player = PlayerFacade("Test", "blanco", identity=custom_identity)
        
        assert player.get_nombre() == "Custom"
        assert player.get_color() == "negro"
    
    def test_inyeccion_dependencias_inventory(self):
        """Test DIP: inyección de componente Inventory"""
        custom_inventory = PlayerInventory(5)
        player = PlayerFacade("Test", "blanco", inventory=custom_inventory)
        
        assert player.get_fichas() == 5
    
    def test_inyeccion_dependencias_score(self):
        """Test DIP: inyección de componente Score"""
        custom_score = PlayerScore(10)
        player = PlayerFacade("Test", "blanco", score=custom_score)
        
        assert player.get_puntos() == 10
    
    def test_getters_componentes(self):
        """Test de getters de componentes SOLID"""
        player = PlayerFacade("Test", "blanco")
        
        assert isinstance(player.get_identity(), PlayerIdentity)
        assert isinstance(player.get_inventory(), PlayerInventory)
        assert isinstance(player.get_score_component(), PlayerScore)
    
    def test_setters_componentes(self):
        """Test de setters de componentes SOLID"""
        player = PlayerFacade("Test", "blanco")
        
        new_identity = PlayerIdentity("New", "negro")
        player.set_identity(new_identity)
        assert player.get_nombre() == "New"
        
        new_inventory = PlayerInventory(8)
        player.set_inventory(new_inventory)
        assert player.get_fichas() == 8
        
        new_score = PlayerScore(15)
        player.set_score_component(new_score)
        assert player.get_puntos() == 15