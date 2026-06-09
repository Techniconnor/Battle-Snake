import pygame

from constants import *
from game import Game
from rendering import *

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battle Snake")

clock = pygame.time.Clock()

game = Game()
show_menu = True

running = True

# =========================
# MAIN LOOP
# =========================
while running:

    # -------------------
    # EVENTS
    # -------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if show_menu:
                if event.key == pygame.K_1:
                    game.mode = MODE_PLAYER_VS_ENEMY
                    game.reset_match()
                    show_menu = False
                elif event.key == pygame.K_2:
                    game.mode = MODE_PLAYER_VS_PLAYER
                    game.reset_match()
                    show_menu = False
                elif event.key == pygame.K_3:
                    game.mode = MODE_COMPUTER_VS_COMPUTER
                    game.reset_match()
                    show_menu = False
                continue

            # -------------------
            # RESTART / NEXT ROUND
            # -------------------
            if event.key == pygame.K_r and (game.game_over or game.match_over):
                game.next_round()

            # -------------------
            # RETURN TO MENU AFTER MATCH
            # -------------------
            elif game.match_over and event.key == pygame.K_m:
                game.reset_match()
                show_menu = True

            # -------------------
            # INPUT ONLY DURING ACTIVE ROUND
            # -------------------
            if not game.game_over and not game.match_over and game.mode != MODE_COMPUTER_VS_COMPUTER:
                if event.key == pygame.K_w:
                    game.change_direction(UP)
                elif event.key == pygame.K_s:
                    game.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    game.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    game.change_direction(RIGHT)
                elif event.key == pygame.K_UP:
                    if game.mode == MODE_PLAYER_VS_PLAYER:
                        game.change_direction(UP, enemy=True)
                    else:
                        game.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    if game.mode == MODE_PLAYER_VS_PLAYER:
                        game.change_direction(DOWN, enemy=True)
                    else:
                        game.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    if game.mode == MODE_PLAYER_VS_PLAYER:
                        game.change_direction(LEFT, enemy=True)
                    else:
                        game.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    if game.mode == MODE_PLAYER_VS_PLAYER:
                        game.change_direction(RIGHT, enemy=True)
                    else:
                        game.change_direction(RIGHT)

    # -------------------
    # UPDATE GAME
    # -------------------
    if not show_menu and not game.game_over and not game.match_over:
        game.update()

    # -------------------
    # DRAW
    # -------------------
    screen.fill((0, 0, 0))

    if show_menu:
        draw_main_menu(screen)
    else:
        draw_snake(screen, game.snake)
        draw_enemy(screen, game.enemy)
        draw_food(screen, game.food)

        # -------------------
        # UI OVERLAYS
        # -------------------
        if game.match_over:
            draw_match_over(screen, game)

        elif game.game_over:
            draw_game_over(screen, game)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()