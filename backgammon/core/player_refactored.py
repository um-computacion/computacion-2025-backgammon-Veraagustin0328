from __future__ import annotations
from typing import Dict, Any
from .player import Player


class PlayerIdentity:
    """
    SRP: Responsabilidad única de manejar la identidad del jugador.
    
    Solo gestiona nombre y color.
    """
    
    def __init__(self, nombre: str, color: str = "blanco"):
        self.__nombre = str(nombre).strip() or "Jugador"
        self.__color = color if color in {"blanco", "negro"} else "blanco"
    
    def get_nombre(self) -> str:
        """Getter del nombre."""
        return self.__nombre
    
    def set_nombre(self, nombre: str) -> None:
        """Setter del nombre."""
        if not str(nombre).strip():
            raise ValueError("El nombre no puede ser vacío")
        self.__nombre = str(nombre).strip()
    
    def get_color(self) -> str:
        """Getter del color."""
        return self.__color
    
    def set_color(self, color: str) -> None:
        """Setter del color."""
        if color not in {"blanco", "negro"}:
            raise ValueError(f"Color inválido: {color}. Permitidos: blanco, negro")
        self.__color = color


class PlayerInventory:
    """
    SRP: Responsabilidad única de gestionar el inventario de fichas.
    
    Maneja la cantidad de fichas del jugador.
    """
    
    FICHAS_INICIALES = 15
    
    def __init__(self, fichas_iniciales: int = FICHAS_INICIALES):
        self.__fichas = fichas_iniciales
    
    def get_fichas(self) -> int:
        """Getter de la cantidad de fichas."""
        return self.__fichas
    
    def set_fichas(self, cantidad: int) -> None:
        """Setter de la cantidad de fichas."""
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad de fichas no puede ser negativa")
        self.__fichas = cantidad
    
    def perder_ficha(self) -> None:
        """Resta una ficha del inventario."""
        if self.__fichas <= 0:
            raise ValueError("No hay fichas para perder")
        self.__fichas -= 1
    
    def reset(self) -> None:
        """Reinicia el inventario al valor inicial."""
        self.__fichas = self.FICHAS_INICIALES


class PlayerScore:
    """
    SRP: Responsabilidad única de gestionar la puntuación.
    
    Maneja los puntos acumulados del jugador.
    """
    
    PUNTOS_INICIALES = 0
    
    def __init__(self, puntos_iniciales: int = PUNTOS_INICIALES):
        self.__puntos = puntos_iniciales
    
    def get_puntos(self) -> int:
        """Getter de los puntos."""
        return self.__puntos
    
    def set_puntos(self, puntos: int) -> None:
        """Setter de los puntos."""
        self.__puntos = int(puntos)
    
    def sumar_puntos(self, puntos: int) -> None:
        """Suma puntos al total."""
        self.__puntos += int(puntos)
    
    def reset(self) -> None:
        """Reinicia los puntos al valor inicial."""
        self.__puntos = self.PUNTOS_INICIALES


class PlayerFacade:
    """
    Facade Pattern: Coordina los componentes de Player siguiendo SOLID.
    
    Componentes:
    - PlayerIdentity: Maneja identidad (nombre, color)
    - PlayerInventory: Maneja fichas
    - PlayerScore: Maneja puntuación
    
    Esta clase mantiene compatibilidad con la interfaz de Player original,
    pero internamente delega responsabilidades a componentes especializados.
    
    DIP: Acepta inyección de dependencias para los componentes.
    """
    
    def __init__(
        self,
        nombre: str,
        color: str = "blanco",
        identity: PlayerIdentity = None,
        inventory: PlayerInventory = None,
        score: PlayerScore = None
    ):
        """
        Inicializa el jugador con inyección de dependencias (DIP).
        
        Args:
            nombre: Nombre del jugador
            color: Color del jugador ("blanco" o "negro")
            identity: Componente de identidad (si es None, crea uno)
            inventory: Componente de inventario (si es None, crea uno)
            score: Componente de puntuación (si es None, crea uno)
        """
        # Inyección de dependencias (DIP)
        self.__identity = identity or PlayerIdentity(nombre, color)
        self.__inventory = inventory or PlayerInventory()
        self.__score = score or PlayerScore()
        
        # Guardar referencia a Player original para compatibilidad
        self.__original_player = Player(nombre, color)
    
   
    
    def get_identity(self) -> PlayerIdentity:
        """Getter del componente de identidad."""
        return self.__identity
    
    def set_identity(self, identity: PlayerIdentity) -> None:
        """Setter del componente de identidad."""
        self.__identity = identity
    
    def get_inventory(self) -> PlayerInventory:
        """Getter del componente de inventario."""
        return self.__inventory
    
    def set_inventory(self, inventory: PlayerInventory) -> None:
        """Setter del componente de inventario."""
        self.__inventory = inventory
    
    def get_score_component(self) -> PlayerScore:
        """Getter del componente de puntuación."""
        return self.__score
    
    def set_score_component(self, score: PlayerScore) -> None:
        """Setter del componente de puntuación."""
        self.__score = score
    
    # Delegación a PlayerIdentity 
    
    def get_nombre(self) -> str:
        """Retorna el nombre del jugador."""
        return self.__identity.get_nombre()
    
    def set_nombre(self, nombre: str) -> None:
        """Establece el nombre del jugador."""
        self.__identity.set_nombre(nombre)
        self.__original_player.set_nombre(nombre)
    
    def get_color(self) -> str:
        """Retorna el color del jugador."""
        return self.__identity.get_color()
    
    def set_color(self, color: str) -> None:
        """Establece el color del jugador."""
        self.__identity.set_color(color)
        self.__original_player.set_color(color)
    
    # Delegación a PlayerInventory 
    
    def get_fichas(self) -> int:
        """Retorna la cantidad de fichas."""
        return self.__inventory.get_fichas()
    
    def set_fichas(self, cantidad: int) -> None:
        """Establece la cantidad de fichas."""
        self.__inventory.set_fichas(cantidad)
        self.__original_player.set_fichas(cantidad)
    
    def perder_ficha(self) -> None:
        """Resta una ficha del inventario."""
        self.__inventory.perder_ficha()
        self.__original_player.perder_ficha()
    
    # Delegación a PlayerScore 
    
    def get_puntos(self) -> int:
        """Retorna los puntos del jugador."""
        return self.__score.get_puntos()
    
    def sumar_puntos(self, puntos: int) -> None:
        """Suma puntos al jugador."""
        self.__score.sumar_puntos(puntos)
        self.__original_player.sumar_puntos(puntos)
    
    #  Métodos adicionales 
    
    def reset(self) -> None:
        """Reinicia fichas y puntos a valores iniciales."""
        self.__inventory.reset()
        self.__score.reset()
        self.__original_player.reset()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el jugador a diccionario."""
        return {
            "nombre": self.get_nombre(),
            "color": self.get_color(),
            "fichas": self.get_fichas(),
            "puntos": self.get_puntos(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerFacade":
        """
        Reconstruye un jugador desde un diccionario.
        
        Args:
            data: Diccionario con los datos del jugador
            
        Returns:
            Nueva instancia de PlayerFacade
        """
        nombre = str(data.get("nombre", "Jugador"))
        color = str(data.get("color", "blanco"))
        
        player = cls(nombre=nombre, color=color)
        
        if "fichas" in data:
            player.set_fichas(int(data["fichas"]))
        
        if "puntos" in data:
            player.__score.set_puntos(int(data["puntos"]))
        
        return player
    
    #  Métodos especiales 
    
    def __repr__(self) -> str:
        return (
            f"PlayerFacade(nombre={self.get_nombre()!r}, "
            f"color={self.get_color()!r}, "
            f"fichas={self.get_fichas()}, puntos={self.get_puntos()}, "
            f"SOLID=True)"
        )
    
    def __str__(self) -> str:
        return f"{self.get_nombre()} ({self.get_color()})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (PlayerFacade, Player)):
            return False
        return self.get_nombre() == (
            other.get_nombre() if hasattr(other, 'get_nombre') else str(other)
        )
    
    def __hash__(self) -> int:
        return hash(self.get_nombre())