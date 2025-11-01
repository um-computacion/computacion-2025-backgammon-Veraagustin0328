# Backgammon - Proyecto Computación 2025

Agustin Vera

## ¿De qué va este proyecto?

Este es un juego de Backgammon completo hecho en Python para la materia Computación 2025. Tiene dos formas de jugar:

1. **CLI (Terminal)**: Comandos simples desde la consola
2. **Pygame (Interfaz gráfica)**: Juego visual con clicks del mouse

## Requisitos

- Python 3.10 o más nuevo
- pip para instalar las librerías

## Instalación

1. Clonar el repo:
```bash
git clone https://github.com/tu-usuario/backgammon.git
cd backgammon
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

Si te falta alguna librería específica:
```bash
pip install pygame colorama pytest pytest-cov
```

## ¿Cómo jugar?

### Desde la terminal (CLI)

El CLI tiene varios comandos que podés usar:
```bash
# Ver el tablero vacío
python -m backgammon.cli board

# Tirar los dados
python -m backgammon.cli roll

# Ver la posición inicial del juego
python -m backgammon.cli setup

# Ver las reglas e info del juego
python -m backgammon.cli info

# Simular una tirada con ejemplos
python -m backgammon.cli simulate

# Ver estadísticas y más reglas
python -m backgammon.cli stats
```

### Con interfaz gráfica (Pygame)

Para jugar con la interfaz visual:
```bash
python -m backgammon.pygame_ui.main
```

**Cómo jugar:**
- Presioná `ESPACIO` o hacé click en "Roll Dice" para tirar los dados
- Click en una ficha para seleccionarla (se pone amarilla)
- Click en el destino para moverla
- `ESC` para salir

## Testing

Para correr todos los tests:
```bash
pytest
```

Para ver cuánto código está cubierto por tests:
```bash
pytest --cov=backgammon --cov-report=term-missing
```

El proyecto tiene más del 90% de cobertura en el código core (la lógica principal del juego).

Los tests están en `backgammon/tests/` y podés correr tests específicos:
```bash
# Solo tests de Player
pytest backgammon/tests/test_player.py

# Solo tests de Board
pytest backgammon/tests/test_board.py
```

## Estructura del proyecto
```
backgammon/
├── backgammon/
│   ├── core/              # Lógica del juego (Game, Board, Player, etc.)
│   │   ├── game.py        # Coordina la partida
│   │   ├── board.py       # Tablero y movimientos
│   │   ├── player.py      # Jugadores
│   │   ├── dice.py        # Dados
│   │   └── checker.py     # Fichas
│   ├── cli/               # Interfaz de terminal
│   │   └── __main__.py    # Comandos del CLI
│   ├── pygame_ui/         # Interfaz gráfica
│   │   └── main.py        # Juego visual
│   ├── tests/             # Tests unitarios
│   └── assets/            # Imágenes y recursos
├── requirements.txt       # Librerías necesarias
├── pytest.ini            # Config de tests
├── .coveragerc           # Config de cobertura
├── CHANGELOG.md          # Historial de cambios
└── JUSTIFICACION.md      # Decisiones de diseño
```

## Tecnologías usadas

- **Python 3.11**: Lenguaje principal
- **Pygame**: Para la interfaz gráfica
- **pytest**: Para correr los tests
- **pytest-cov**: Para medir la cobertura de código
- **colorama**: Para colores bonitos en la terminal
- **GitHub Actions**: Para CI/CD (tests automáticos en cada commit)

## Estado actual del proyecto

 **Completo:**
- Lógica del juego (core) funcionando 100%
- CLI con múltiples comandos
- Interfaz gráfica con Pygame
- Tests con >90% de cobertura
- CI/CD configurado
- Documentación completa



## Reglas de Backgammon

Si no conocés el juego, acá hay un link para jugar online y aprender:
https://www.ludoteka.com/clasika/backgammon-es.html

### Resumen rápido:
- Cada jugador tiene 15 fichas (blancas o negras)
- Las blancas se mueven de 1→24, las negras de 24→1
- Tirás dos dados y movés tus fichas esa cantidad de espacios
- Si sacás dobles, movés 4 veces
- Podés capturar fichas solitarias del oponente
- Ganás cuando sacás todas tus fichas del tablero

## Documentación adicional

- **JUSTIFICACION.md**: Explicación completa del diseño y las decisiones tomadas
- **CHANGELOG.md**: Historial de cambios del proyecto
- **prompts-*.md**: Prompts usados con IA durante el desarrollo

## Links útiles

- [Documentación de Pygame](https://www.pygame.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

