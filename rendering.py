import pygame
from constants import *


def _direction(a, b):
    #Return the grid direction vector from point a to point b.
    return (b[0] - a[0], b[1] - a[1])


def _draw_segment(screen, segment, fill_color, prev_segment=None, next_segment=None):
    #Draw a snake body segment using dots and path connectors.

    #Each body segment is represented by a small center dot plus
    #connection bars toward the previous and next segments in the snake.
    #Edges that are not connected to the path are outlined with a darker border.

    x, y = segment
    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    # Compute the center point for the dot and connector bars.
    center_x = rect.centerx
    center_y = rect.centery

    # Determine which directions this segment connects to on the snake path.
    connected = set()
    for neighbor in (prev_segment, next_segment):
        if neighbor is None:
            continue
        connected.add(_direction(segment, neighbor))

    dot_radius = max(3, CELL_SIZE // 6)
    connector_thickness = max(4, CELL_SIZE // 5)

    # Draw the central dot for the segment.
    pygame.draw.circle(screen, fill_color, (center_x, center_y), dot_radius)

    # Draw path connectors only where the body is actually connected.
    if (-1, 0) in connected:
        pygame.draw.rect(
            screen,
            fill_color,
            pygame.Rect(rect.left, center_y - connector_thickness // 2, center_x - rect.left, connector_thickness)
        )
    if (1, 0) in connected:
        pygame.draw.rect(
            screen,
            fill_color,
            pygame.Rect(center_x, center_y - connector_thickness // 2, rect.right - center_x, connector_thickness)
        )
    if (0, -1) in connected:
        pygame.draw.rect(
            screen,
            fill_color,
            pygame.Rect(center_x - connector_thickness // 2, rect.top, connector_thickness, center_y - rect.top)
        )
    if (0, 1) in connected:
        pygame.draw.rect(
            screen,
            fill_color,
            pygame.Rect(center_x - connector_thickness // 2, center_y, connector_thickness, rect.bottom - center_y)
        )

    # Draw an outer border on any exposed edges.
    border_color = tuple(max(0, value - 20) for value in fill_color)
    border_width = 2

    if (-1, 0) not in connected:
        pygame.draw.rect(screen, border_color, pygame.Rect(rect.left, rect.top, border_width, rect.height))
    if (1, 0) not in connected:
        pygame.draw.rect(screen, border_color, pygame.Rect(rect.right - border_width, rect.top, border_width, rect.height))
    if (0, -1) not in connected:
        pygame.draw.rect(screen, border_color, pygame.Rect(rect.left, rect.top, rect.width, border_width))
    if (0, 1) not in connected:
        pygame.draw.rect(screen, border_color, pygame.Rect(rect.left, rect.bottom - border_width, rect.width, border_width))


# =========================
# DRAW SNAKE
# =========================

def draw_snake(screen, snake):
    #Draw the player snake on the screen.

    #The head is drawn as a solid block for instant recognition.
    #The rest of the body uses the dot-and-connector style.

    for i, segment in enumerate(snake):
        prev_segment = snake[i - 1] if i > 0 else None
        next_segment = snake[i + 1] if i + 1 < len(snake) else None

        if i == 0:
            x, y = segment
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (0, 200, 0), rect)
        else:
            _draw_segment(screen, segment, (0, 120, 0), prev_segment, next_segment)


# =========================
# DRAW COMPUTER
# =========================

def draw_enemy(screen, enemy, head_color=(200, 0, 0), body_color=(120, 0, 0)):
    #Draw the computer-controlled snake.

    #The enemy/computer head is drawn as a solid block, while the body
    #shares the same connector-based visualization as the player snake.

    for i, segment in enumerate(enemy):
        prev_segment = enemy[i - 1] if i > 0 else None
        next_segment = enemy[i + 1] if i + 1 < len(enemy) else None

        if i == 0:
            x, y = segment
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, head_color, rect)
        else:
            _draw_segment(screen, segment, body_color, prev_segment, next_segment)


# =========================
# DRAW FOOD
# =========================

def draw_food(screen, food):
    #Draw the food item as a small circle in the grid cell.
    x, y = food

    center_x = x * CELL_SIZE + CELL_SIZE // 2
    center_y = y * CELL_SIZE + CELL_SIZE // 2

    radius = CELL_SIZE // 2 - 2

    pygame.draw.circle(
        screen,
        (255, 200, 0),
        (center_x, center_y),
        radius
    )


def draw_main_menu(screen):
    #Render the main menu text and controls on the screen.
    title_font = pygame.font.SysFont(None, 72)
    subtitle_font = pygame.font.SysFont(None, 32)
    body_font = pygame.font.SysFont(None, 24)

    title_text = title_font.render("BATTLE SNAKE", True, (255, 255, 255))
    mode1_text = subtitle_font.render("Press 1 for Player vs Computer", True, (200, 200, 200))
    mode2_text = subtitle_font.render("Press 2 for Player vs Player", True, (200, 200, 200))
    mode3_text = subtitle_font.render("Press 3 for Computer vs Computer", True, (200, 200, 200))
    controls_text = body_font.render("WASD for player 1. Arrows for player 2.", True, (180, 180, 180))
    match_text = body_font.render("Best of 5 rounds — survive, grow, and defeat the computer.", True, (180, 180, 180))

    screen.blit(
        title_text,
        (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100)
    )
    screen.blit(
        mode1_text,
        (WINDOW_WIDTH // 2 - mode1_text.get_width() // 2, 200)
    )
    screen.blit(
        mode2_text,
        (WINDOW_WIDTH // 2 - mode2_text.get_width() // 2, 250)
    )
    screen.blit(
        mode3_text,
        (WINDOW_WIDTH // 2 - mode3_text.get_width() // 2, 300)
    )
    screen.blit(
        controls_text,
        (WINDOW_WIDTH // 2 - controls_text.get_width() // 2, 350)
    )
    screen.blit(
        match_text,
        (WINDOW_WIDTH // 2 - match_text.get_width() // 2, 380)
    )


def draw_game_over(screen, game):
    #Render the round result overlay when a round finishes.
    font = pygame.font.SysFont(None, 48)
    small = pygame.font.SysFont(None, 28)

    if game.mode == MODE_PLAYER_VS_PLAYER:
        player_label = "PLAYER 1"
        enemy_label = "PLAYER 2"
    elif game.mode == MODE_COMPUTER_VS_COMPUTER:
        player_label = "COMPUTER 1"
        enemy_label = "COMPUTER 2"
    else:
        player_label = "PLAYER"
        enemy_label = "COMPUTER"

    # Round result text depends on the scores.
    if game.player_score > game.enemy_score:
        result_text = f"{player_label} WINS ROUND"
        color = (0, 255, 0)
    elif game.enemy_score > game.player_score:
        result_text = f"{enemy_label} WINS ROUND"
        color = (255, 0, 0)
    else:
        result_text = "ROUND DRAW"
        color = (200, 200, 200)

    main_text = font.render(result_text, True, color)
    sub_text = small.render("Press R for next round", True, (200, 200, 200))

    screen.blit(
        main_text,
        (WINDOW_WIDTH // 2 - main_text.get_width() // 2, 200)
    )
    screen.blit(
        sub_text,
        (WINDOW_WIDTH // 2 - sub_text.get_width() // 2, 260)
    )

    # Display score and round standings in the top-left corner.
    score_text = small.render(
        f"{player_label}: {game.player_score} | {enemy_label}: {game.enemy_score}",
        True,
        (255, 255, 255)
    )
    screen.blit(score_text, (20, 20))

    rounds_text = small.render(
        f"Rounds - {player_label}: {game.player_rounds} | {enemy_label}: {game.enemy_rounds}",
        True,
        (180, 180, 180)
    )
    screen.blit(rounds_text, (20, 50))


# =========================
# MATCH OVER
# =========================

def draw_match_over(screen, game):
    #Render the match result overlay when the full match ends.
    font = pygame.font.SysFont(None, 64)
    small = pygame.font.SysFont(None, 32)

    if game.mode == MODE_PLAYER_VS_PLAYER:
        player_label = "PLAYER 1"
        enemy_label = "PLAYER 2"
    elif game.mode == MODE_COMPUTER_VS_COMPUTER:
        player_label = "COMPUTER 1"
        enemy_label = "COMPUTER 2"
    else:
        player_label = "PLAYER"
        enemy_label = "COMPUTER"

    if game.player_rounds > game.enemy_rounds:
        text = f"{player_label}"
        color = (0, 255, 0)
    elif game.enemy_rounds > game.player_rounds:
        text = f"{enemy_label}"
        color = (255, 0, 0)
    else:
        text = "MATCH DRAW"
        color = (200, 200, 200)

    main_text = font.render(text, True, color)
    win_text = small.render("WINS MATCH!", True, color)
    sub_text_1 = small.render("Press R to restart match", True, (200, 200, 200))
    sub_text_2 = small.render("Press M to return to menu", True, (200, 200, 200))

    rounds_text = small.render(
        f"Rounds - {player_label}: {game.player_rounds} | {enemy_label}: {game.enemy_rounds}",
        True,
        (255, 255, 255)
    )

    screen.blit(main_text, (WINDOW_WIDTH // 2 - main_text.get_width() // 2, 180))
    if text != "MATCH DRAW":
        screen.blit(win_text, (WINDOW_WIDTH // 2 - win_text.get_width() // 2, 220))
    screen.blit(sub_text_1, (WINDOW_WIDTH // 2 - sub_text_1.get_width() // 2, 280))
    screen.blit(sub_text_2, (WINDOW_WIDTH // 2 - sub_text_2.get_width() // 2, 320))
    screen.blit(rounds_text, (WINDOW_WIDTH // 2 - rounds_text.get_width() // 2, 370))


    