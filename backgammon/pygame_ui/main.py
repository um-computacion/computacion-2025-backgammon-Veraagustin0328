import sys
import pygame
from backgammon.core.game import Game
from backgammon.core.board import BoardWithSetup
from backgammon.core.player import Player
from backgammon.core.dice import Dice


"""
Interfaz gráfica de Backgammon con Pygame.
VERSIÓN FINAL con colores y layout correctos
"""



#Config visual 

WIDTH, HEIGHT = 1300, 700  # MÁS ANCHO
MARGIN_X, MARGIN_Y = 60, 40  # MÁS MARGEN
BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE_COLOR = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
RED = (200, 20, 20)
TEXT_COLOR = (25, 25, 25)

MAX_VISIBLE_STACK = 5


def point_index_to_display(point):
    """
    Convierte punto 1-24 (backgammon) a:
    - row: 'top' o 'bottom'  
    - col_vis: 0-11 (columna visual)
    
    Layout:
    Top:    13 14 15 16 17 18 | BAR | 19 20 21 22 23 24
    Bottom: 12 11 10  9  8  7 | BAR |  6  5  4  3  2  1
    """
    if 13 <= point <= 24:
        col_vis = point - 13
        return 'top', col_vis
    else:
        col_vis = 12 - point
        return 'bottom', col_vis


def draw_triangle(surface, board_rect, col_vis, row, color):
    """Dibuja un triángulo LARGO (42% de altura)"""
    tri_width = board_rect.width / 12.0
    x0 = board_rect.left + col_vis * tri_width
    x1 = x0 + tri_width
    x_mid = (x0 + x1) / 2.0
    
    if row == 'top':
        tip_y = board_rect.top + board_rect.height * 0.42
        pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
    else:
        tip_y = board_rect.bottom - board_rect.height * 0.42
        pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
    
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.polygon(surface, LINE_COLOR, pts, 1)


def draw_checker(surface, center, color_name, radius, label=None, font=None):
    """Dibuja una ficha con el color correcto"""
    if color_name == "blanco":
        checker_color = WHITE
        text_color = LINE_COLOR
    else:  # "negro"
        checker_color = RED
        text_color = WHITE
    
    pygame.draw.circle(surface, checker_color, (int(center[0]), int(center[1])), radius)
    pygame.draw.circle(surface, LINE_COLOR, (int(center[0]), int(center[1])), radius, 2)
    
    if label and font:
        txt = font.render(str(label), True, text_color)
        rect = txt.get_rect(center=(int(center[0]), int(center[1])))
        surface.blit(txt, rect)


def render_board(surface, game, font):
    """Dibuja el tablero y devuelve hitmap"""
    surface.fill(BG_COLOR)
    
    # Marco del tablero - MÁS ESPACIO
    board_rect = pygame.Rect(
        MARGIN_X,
        MARGIN_Y + 30,
        WIDTH - 2 * MARGIN_X - 220,
        HEIGHT - 2 * MARGIN_Y - 60
    )
    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE_COLOR, board_rect, 2, border_radius=12)
    
    # Dibujar 24 triángulos
    for col_vis in range(12):
        color_top = TRI_A if col_vis % 2 == 0 else TRI_B
        draw_triangle(surface, board_rect, col_vis, 'top', color_top)
        
        color_bottom = TRI_B if col_vis % 2 == 0 else TRI_A
        draw_triangle(surface, board_rect, col_vis, 'bottom', color_bottom)
    
    # Línea divisoria central
    mid_y = board_rect.centery
    pygame.draw.line(surface, LINE_COLOR, 
                     (board_rect.left, mid_y), 
                     (board_rect.right, mid_y), 2)
    
    # Parámetros para fichas
    tri_width = board_rect.width / 12.0
    radius = int(tri_width * 0.38)
    radius = max(14, min(radius, 24))
    vgap = 3
    step = radius * 2 + vgap
    
    # Etiquetas de puntos - Top: 13-24
    for col_vis in range(12):
        point_num = 13 + col_vis
        x = int(board_rect.left + col_vis * tri_width + tri_width / 2)
        y = board_rect.top - 14
        img = font.render(str(point_num), True, TEXT_COLOR)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
    
    # Etiquetas de puntos - Bottom: 12-1
    for col_vis in range(12):
        point_num = 12 - col_vis
        x = int(board_rect.left + col_vis * tri_width + tri_width / 2)
        y = board_rect.bottom + 14
        img = font.render(str(point_num), True, TEXT_COLOR)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
    
    # Hitmap para clicks
    hitmap = {i: [] for i in range(1, 25)}
    
    # Dibujar fichas del tablero
    board = game.get_board()
    
    for point in range(1, 25):
        count = board.point_count(point)
        if count == 0:
            continue
        
        top_checker = board.get_top_checker(point)
        if not top_checker:
            continue
        
        color = top_checker.get_color()
        row, col_vis = point_index_to_display(point)
        cx = int(board_rect.left + col_vis * tri_width + tri_width / 2)
        
        visibles = min(count, MAX_VISIBLE_STACK)
        extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0
        
        if row == 'top':
            start_y = int(board_rect.top + radius + 8)
            for i in range(visibles):
                cy = start_y + i * step
                label = extras if (extras and i == visibles - 1) else None
                draw_checker(surface, (cx, cy), color, radius, label, font)
                hitmap[point].append((cx, cy, radius))
        else:
            start_y = int(board_rect.bottom - radius - 8)
            for i in range(visibles):
                cy = start_y - i * step
                label = extras if (extras and i == visibles - 1) else None
                draw_checker(surface, (cx, cy), color, radius, label, font)
                hitmap[point].append((cx, cy, radius))
    
    # Dibujar barra
    bar_x = board_rect.right + 30
    
    white_bar = board.get_bar_count("blanco")
    if white_bar > 0:
        for i in range(min(white_bar, 3)):
            cy = mid_y - 60 + i * (radius * 2 + 2)
            label = white_bar if i == 2 and white_bar > 3 else None
            draw_checker(surface, (bar_x, cy), "blanco", radius, label, font)
    
    black_bar = board.get_bar_count("negro")
    if black_bar > 0:
        for i in range(min(black_bar, 3)):
            cy = mid_y + 60 - i * (radius * 2 + 2)
            label = black_bar if i == 2 and black_bar > 3 else None
            draw_checker(surface, (bar_x, cy), "negro", radius, label, font)
    
    # Bear off
    info_x = board_rect.right + 80
    
    white_off = board.get_off_count("blanco")
    off_text = font.render(f"White: {white_off}", True, TEXT_COLOR)
    surface.blit(off_text, (info_x, board_rect.top + 20))
    
    black_off = board.get_off_count("negro")
    off_text = font.render(f"Black: {black_off}", True, TEXT_COLOR)
    surface.blit(off_text, (info_x, board_rect.bottom - 40))
    
    return hitmap


def hit_test(hitmap, pos):
    """Detecta click en ficha"""
    mx, my = pos
    for point, circles in hitmap.items():
        for (cx, cy, r) in circles:
            dx, dy = mx - cx, my - cy
            if dx*dx + dy*dy <= r*r:
                return point
    return None


def draw_dice(surface, dice_values, x, y, font):
    """Dibuja los dados"""
    if not dice_values:
        return
    
    dice_size = 35
    spacing = 45
    
    for i, value in enumerate(dice_values):
        dice_x = x + i * spacing
        dice_rect = pygame.Rect(dice_x, y, dice_size, dice_size)
        
        pygame.draw.rect(surface, WHITE, dice_rect, border_radius=5)
        pygame.draw.rect(surface, LINE_COLOR, dice_rect, 2, border_radius=5)
        
        text = font.render(str(value), True, LINE_COLOR)
        text_rect = text.get_rect(center=dice_rect.center)
        surface.blit(text, text_rect)


def draw_game_info(surface, game, font, dice_values, message):
    """Dibuja info del juego"""
    info_x = WIDTH - 200
    info_y = 150
    
    current = game.get_current_player()
    color_name = "Blancas" if current.get_color() == "blanco" else "Negras"
    text = font.render(f"Turno:", True, TEXT_COLOR)
    surface.blit(text, (info_x, info_y))
    
    text2 = font.render(color_name, True, TEXT_COLOR)
    surface.blit(text2, (info_x, info_y + 25))
    
    # Botón Roll Dice
    button_rect = pygame.Rect(info_x, info_y + 60, 140, 45)
    pygame.draw.rect(surface, TRI_A, button_rect, border_radius=8)
    pygame.draw.rect(surface, LINE_COLOR, button_rect, 2, border_radius=8)
    
    btn_text = font.render("Roll Dice", True, TEXT_COLOR)
    btn_rect = btn_text.get_rect(center=button_rect.center)
    surface.blit(btn_text, btn_rect)
    
    # Dados
    if dice_values:
        draw_dice(surface, dice_values, info_x, info_y + 120, font)
    
    # Mensaje
    if message:
        msg_font = pygame.font.SysFont(None, 18)
        msg_text = msg_font.render(message, True, TEXT_COLOR)
        surface.blit(msg_text, (MARGIN_X, HEIGHT - 35))
    
    return button_rect


def main():
    """Main loop"""
    pygame.init()
    pygame.display.set_caption("Backgammon (Pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    
    # Crear juego
    p1 = Player("Blancas", color="blanco")
    p2 = Player("Negras", color="negro")
    board = BoardWithSetup()
    board.setup_initial_position(p1, p2)
    dice = Dice()
    
    game = Game(p1, p2, board=board, dice=dice)
    
    dice_values = []
    available_moves = []
    selected_point = None
    message = "Presioná ESPACIO o 'Roll Dice' para empezar"
    hitmap = {}
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not dice_values:
                        dice_values = game.roll()
                        available_moves = dice_values.copy()
                        selected_point = None
                        message = f"Dados: {dice_values}. Hacé click en una ficha"
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_rect = pygame.Rect(WIDTH - 200, 210, 140, 45)
                
                if button_rect.collidepoint(event.pos):
                    if not dice_values:
                        dice_values = game.roll()
                        available_moves = dice_values.copy()
                        selected_point = None
                        message = f"Dados: {dice_values}"
                    else:
                        message = "Terminá de mover primero"
                
                else:
                    clicked_point = hit_test(hitmap, event.pos)
                    
                    if clicked_point and dice_values:
                        current_player = game.get_current_player()
                        board = game.get_board()
                        
                        if selected_point is None:
                            if board.point_count(clicked_point) > 0:
                                top = board.get_top_checker(clicked_point)
                                if top and top.get_color() == current_player.get_color():
                                    selected_point = clicked_point
                                    message = f"Punto {clicked_point} seleccionado"
                                else:
                                    message = "Esa no es tu ficha"
                            else:
                                message = "Punto vacío"
                        
                        else:
                            if current_player.get_color() == "blanco":
                                distance = clicked_point - selected_point
                            else:
                                distance = selected_point - clicked_point
                            
                            if distance in available_moves:
                                try:
                                    board.mover_ficha(selected_point, clicked_point)
                                    available_moves.remove(distance)
                                    message = f"Moviste {selected_point} → {clicked_point}"
                                    selected_point = None
                                    
                                    if not available_moves:
                                        game.next_turn()
                                        dice_values = []
                                        message = f"Turno de {game.get_current_player().get_nombre()}"
                                
                                except Exception:
                                    message = f"Movimiento inválido"
                                    selected_point = None
                            else:
                                message = f"Distancia {distance} no disponible"
                                selected_point = None
        
        # RENDER
        hitmap = render_board(screen, game, font)
        draw_game_info(screen, game, font, available_moves, message)
        
        # Highlight punto seleccionado
        if selected_point:
            board_rect = pygame.Rect(MARGIN_X, MARGIN_Y + 30, WIDTH - 2*MARGIN_X - 220, HEIGHT - 2*MARGIN_Y - 60)
            row, col_vis = point_index_to_display(selected_point)
            tri_width = board_rect.width / 12.0
            x = board_rect.left + col_vis * tri_width
            
            if row == 'top':
                y = board_rect.top
                h = board_rect.height * 0.42
            else:
                y = board_rect.bottom - board_rect.height * 0.42
                h = board_rect.height * 0.42
            
            highlight = pygame.Rect(x, y, tri_width, h)
            pygame.draw.rect(screen, (255, 255, 0), highlight, 3)
        
        # Instrucciones
        inst_font = pygame.font.SysFont(None, 18)
        inst = inst_font.render("ESPACIO = tirar dados | Click = seleccionar/mover | ESC = salir", True, TEXT_COLOR)
        screen.blit(inst, (MARGIN_X, 15))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()