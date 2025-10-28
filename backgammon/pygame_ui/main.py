import sys
import pygame
from backgammon.core.game import Game
from backgammon.core.board import Board
from backgammon.core.player import Player
from backgammon.core.dice import Dice


"""
Interfaz gráfica de Backgammon con Pygame.
Adaptado para usar las clases del proyecto (Board, Game, Player, etc.)
"""


# Constantes de ventana
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 90, 43)
LIGHT_BROWN = (205, 133, 63)
DARK_BROWN = (101, 67, 33)
BEIGE = (245, 222, 179)
RED = (220, 20, 60)
CREAM = (255, 253, 208)

# Medidas del tablero
BOARD_MARGIN = 50
POINT_WIDTH = 40
POINT_HEIGHT = 200
BAR_WIDTH = 60
CHECKER_RADIUS = 18


def get_point_position(point_index):
    """
    Retorna (x, y) para dibujar el punto.
    point_index: 1-24 (numeración del backgammon)
    
    Layout estándar de Backgammon:
    Top:    13 14 15 16 17 18 | BAR | 19 20 21 22 23 24
    Bottom: 12 11 10  9  8  7 | BAR |  6  5  4  3  2  1
    """
    # Convertir a índice 0-23
    idx = point_index - 1
    
    x_start = BOARD_MARGIN
    y_top = BOARD_MARGIN
    y_bottom = HEIGHT - BOARD_MARGIN - POINT_HEIGHT
    
    # Puntos superiores (13-24)
    if 12 <= idx <= 23:
        col = idx - 12  # 0-11 para puntos 13-24
        if col < 6:  # 13-18 (izquierda)
            x = x_start + col * POINT_WIDTH
        else:  # 19-24 (derecha)
            x = x_start + col * POINT_WIDTH + BAR_WIDTH
        return (x, y_top)
    
    # Puntos inferiores (1-12)
    else:
        # Para 1-12: invertir para que vayan de 12 a 1 de izq a der
        # punto 12 -> col 0, punto 11 -> col 1, ..., punto 1 -> col 11
        col = 11 - idx
        if col >= 6:  # 12-7 (izquierda)
            x = x_start + (col - 6) * POINT_WIDTH
        else:  # 6-1 (derecha)
            x = x_start + col * POINT_WIDTH + BAR_WIDTH
        return (x, y_bottom)


def draw_board(screen):
    """Dibuja el tablero base (fondo, puntos triangulares)"""
    screen.fill(BEIGE)
    
    # Borde del tablero
    board_rect = pygame.Rect(
        BOARD_MARGIN - 10,
        BOARD_MARGIN - 10,
        12 * POINT_WIDTH + BAR_WIDTH + 20,
        2 * POINT_HEIGHT + 20
    )
    pygame.draw.rect(screen, DARK_BROWN, board_rect, 5)
    
    # Dibujar puntos (triángulos)
    for point in range(1, 25):
        x, y = get_point_position(point)
        
        # Color alternado
        color = BROWN if (point % 2 == 0) else LIGHT_BROWN
        
        # Determinar si es punto superior o inferior
        is_top = point >= 13
        
        # Dibujar triángulo
        if is_top:
            points = [
                (x, y),
                (x + POINT_WIDTH, y),
                (x + POINT_WIDTH // 2, y + POINT_HEIGHT)
            ]
        else:
            points = [
                (x, y + POINT_HEIGHT),
                (x + POINT_WIDTH, y + POINT_HEIGHT),
                (x + POINT_WIDTH // 2, y)
            ]
        
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 2)
    
    # Dibujar barra central
    bar_x = BOARD_MARGIN + 6 * POINT_WIDTH
    bar_rect = pygame.Rect(bar_x, BOARD_MARGIN, BAR_WIDTH, 2 * POINT_HEIGHT)
    pygame.draw.rect(screen, DARK_BROWN, bar_rect)
    
    # Dibujar línea divisoria central
    mid_y = HEIGHT // 2
    pygame.draw.line(screen, BLACK, 
                     (BOARD_MARGIN, mid_y), 
                     (BOARD_MARGIN + 12 * POINT_WIDTH + BAR_WIDTH, mid_y), 3)


def draw_checker(screen, x, y, color, number=None):
    """Dibuja una ficha en (x, y)"""
    checker_color = WHITE if color == "blanco" else RED
    border_color = BLACK
    
    # Círculo principal
    pygame.draw.circle(screen, checker_color, (x, y), CHECKER_RADIUS)
    pygame.draw.circle(screen, border_color, (x, y), CHECKER_RADIUS, 2)
    
    # Si hay número (para apilar 5+), dibujarlo
    if number:
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(number), True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)


def draw_checkers(screen, board):
    """Dibuja todas las fichas del tablero"""
    for point in range(1, 25):
        count = board.point_count(point)
        if count == 0:
            continue
        
        # Obtener color de la ficha superior
        top_checker = board.get_top_checker(point)
        if not top_checker:
            continue
        
        color = top_checker.get_color()
        x_base, y_base = get_point_position(point)
        
        # Determinar dirección de apilamiento
        is_top = point >= 13
        x_center = x_base + POINT_WIDTH // 2
        
        # Dibujar hasta 5 fichas apiladas
        max_display = min(count, 5)
        for i in range(max_display):
            if is_top:
                y = y_base + 15 + i * (CHECKER_RADIUS * 2 + 2)
            else:
                y = y_base + POINT_HEIGHT - 15 - i * (CHECKER_RADIUS * 2 + 2)
            
            # Si es la 5ta ficha y hay más, mostrar número
            if i == 4 and count > 5:
                draw_checker(screen, x_center, y, color, count)
            else:
                draw_checker(screen, x_center, y, color)


def draw_bar(screen, board):
    """Dibuja fichas en la barra"""
    bar_x = BOARD_MARGIN + 6 * POINT_WIDTH + BAR_WIDTH // 2
    
    # Fichas blancas
    white_count = board.get_bar_count("blanco")
    for i in range(min(white_count, 5)):
        y = HEIGHT // 2 - 100 + i * (CHECKER_RADIUS * 2 + 2)
        draw_checker(screen, bar_x, y, "blanco", 
                    white_count if i == 4 and white_count > 5 else None)
    
    # Fichas negras
    black_count = board.get_bar_count("negro")
    for i in range(min(black_count, 5)):
        y = HEIGHT // 2 + 100 - i * (CHECKER_RADIUS * 2 + 2)
        draw_checker(screen, bar_x, y, "negro",
                    black_count if i == 4 and black_count > 5 else None)


def draw_bear_off(screen, board):
    """Dibuja fichas sacadas (bear off)"""
    off_x = BOARD_MARGIN + 12 * POINT_WIDTH + BAR_WIDTH + 30
    
    # Blancas (arriba)
    white_off = board.get_bear_off_count("blanco")
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"White: {white_off}", True, BLACK)
    screen.blit(text, (off_x, BOARD_MARGIN + 50))
    
    # Negras (abajo)
    black_off = board.get_bear_off_count("negro")
    text = font.render(f"Black: {black_off}", True, BLACK)
    screen.blit(text, (off_x, HEIGHT - BOARD_MARGIN - 80))


def draw_dice(screen, dice_values, x, y):
    """Dibuja los dados"""
    if not dice_values:
        return
    
    dice_size = 40
    spacing = 50
    
    for i, value in enumerate(dice_values):
        dice_x = x + i * spacing
        dice_rect = pygame.Rect(dice_x, y, dice_size, dice_size)
        
        # Dibujar dado
        pygame.draw.rect(screen, WHITE, dice_rect)
        pygame.draw.rect(screen, BLACK, dice_rect, 2)
        
        # Dibujar número
        font = pygame.font.SysFont(None, 30)
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=dice_rect.center)
        screen.blit(text, text_rect)


def draw_info(screen, game, font):
    """Dibuja información del juego (turno, dados, etc.)"""
    info_x = BOARD_MARGIN + 12 * POINT_WIDTH + BAR_WIDTH + 30
    info_y = HEIGHT // 2 - 100
    
    # Turno actual
    current = game.get_current_player()
    text = font.render(f"Turno: {current.get_nombre()}", True, BLACK)
    screen.blit(text, (info_x, info_y))
    
    # Botón para tirar dados
    button_rect = pygame.Rect(info_x, info_y + 40, 100, 40)
    pygame.draw.rect(screen, LIGHT_BROWN, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    
    button_text = font.render("Roll Dice", True, BLACK)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    
    return button_rect


def get_clicked_point(mouse_pos):
    """Determina qué punto del tablero fue clickeado"""
    mx, my = mouse_pos
    
    for point in range(1, 25):
        x, y = get_point_position(point)
        
        # Área clickeable del punto
        point_rect = pygame.Rect(x, y, POINT_WIDTH, POINT_HEIGHT)
        
        if point_rect.collidepoint(mx, my):
            return point
    
    return None


def main():
    """Función principal del juego con Pygame"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon - Pygame UI")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    
    # Crear juego con posición simple para testing
    p1 = Player("Blancas", color="blanco")
    p2 = Player("Negras", color="negro")
    board = Board()
    dice = Dice()
    
    # Posición simple de prueba (en lugar de setup completo)
    # Blancas (mueven hacia arriba: 1→24)
    board.colocar_ficha(p1, 1)
    board.colocar_ficha(p1, 1)
    board.colocar_ficha(p1, 6)
    board.colocar_ficha(p1, 8)
    
    # Negras (mueven hacia abajo: 24→1)
    board.colocar_ficha(p2, 24)
    board.colocar_ficha(p2, 24)
    board.colocar_ficha(p2, 19)
    board.colocar_ficha(p2, 17)
    
    game = Game(p1, p2, board=board, dice=dice)
    
    dice_values = []
    available_moves = []
    selected_point = None
    message = "Tirá los dados para empezar"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Atajo: tirar dados con espacio
                    if not dice_values:
                        dice_values = game.roll()
                        available_moves = dice_values.copy()
                        selected_point = None
                        message = f"Dados: {dice_values}. Movimientos disponibles: {available_moves}"
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    # Verificar click en botón de dados
                    button_rect = pygame.Rect(
                        BOARD_MARGIN + 12 * POINT_WIDTH + BAR_WIDTH + 30,
                        HEIGHT // 2 - 60,
                        100, 40
                    )
                    
                    if button_rect.collidepoint(event.pos):
                        # Tirar dados solo si no hay movimientos pendientes
                        if not dice_values:
                            dice_values = game.roll()
                            available_moves = dice_values.copy()
                            selected_point = None
                            message = f"Dados: {dice_values}. Elegí una ficha para mover"
                        else:
                            message = "Terminá de usar los dados primero"
                    
                    else:
                        # Verificar click en punto
                        clicked_point = get_clicked_point(event.pos)
                        
                        if clicked_point and dice_values:
                            current_player = game.get_current_player()
                            board = game.get_board()
                            
                            # Si no hay punto seleccionado, seleccionar origen
                            if selected_point is None:
                                # Verificar que el punto tenga fichas del jugador actual
                                if board.point_count(clicked_point) > 0:
                                    top_checker = board.get_top_checker(clicked_point)
                                    if top_checker and top_checker.get_color() == current_player.get_color():
                                        selected_point = clicked_point
                                        message = f"Ficha seleccionada en punto {clicked_point}. Elegí destino"
                                    else:
                                        message = "Esa ficha no es tuya"
                                else:
                                    message = "Ese punto está vacío"
                            
                            # Si ya hay punto seleccionado, intentar mover
                            else:
                                # Calcular distancia del movimiento
                                if current_player.get_color() == "blanco":
                                    distance = clicked_point - selected_point
                                else:
                                    distance = selected_point - clicked_point
                                
                                # Verificar si el movimiento es válido (debe coincidir con un dado)
                                if distance in available_moves:
                                    try:
                                        # Intentar mover la ficha
                                        board.mover_ficha(selected_point, clicked_point)
                                        
                                        # Remover el dado usado
                                        available_moves.remove(distance)
                                        
                                        message = f"Moviste de {selected_point} a {clicked_point}"
                                        selected_point = None
                                        
                                        # Si no quedan dados, cambiar turno
                                        if not available_moves:
                                            game.next_turn()
                                            dice_values = []
                                            message = f"Turno de {game.get_current_player().get_nombre()}"
                                    
                                    except Exception as e:
                                        message = f"Movimiento inválido: {str(e)}"
                                        selected_point = None
                                else:
                                    message = f"Movimiento de {distance} no disponible. Disponibles: {available_moves}"
                                    selected_point = None
        
        # Renderizar
        draw_board(screen)
        draw_checkers(screen, game.get_board())
        draw_bar(screen, game.get_board())
        draw_bear_off(screen, game.get_board())
        
        if dice_values:
            draw_dice(screen, available_moves, 
                     BOARD_MARGIN + 12 * POINT_WIDTH + BAR_WIDTH + 30,
                     HEIGHT // 2)
        
        roll_button = draw_info(screen, game, font)
        
        # Highlight punto seleccionado
        if selected_point:
            x, y = get_point_position(selected_point)
            highlight_rect = pygame.Rect(x, y, POINT_WIDTH, POINT_HEIGHT)
            pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 3)
        
        # Mostrar mensaje
        msg_text = font.render(message, True, BLACK)
        screen.blit(msg_text, (BOARD_MARGIN, HEIGHT - 30))
        
        # Instrucciones
        instructions = font.render("ESPACIO = tirar dados | Click = seleccionar/mover", True, BLACK)
        screen.blit(instructions, (BOARD_MARGIN, 20))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()