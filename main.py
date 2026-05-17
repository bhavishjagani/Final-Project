import pygame
import sys
 
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y,
    COLOR_BACKGROUND,
    FONT_MEDIUM,
)
from game import Game
from renderer import Renderer, Button
 
 
def main():
    pygame.init()
    screen   = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess")
    frame_clock = pygame.time.Clock()
    renderer    = Renderer(screen)
 
    time_options   = [1, 3, 5]
    selected_time  = 3
    button_center_y = WINDOW_HEIGHT // 2 - 80
 
    time_buttons = [
        Button(
            WINDOW_WIDTH // 2 - 170 + index * 116,
            button_center_y,
            100, 46,
            f"{minutes} min",
        )
        for index, minutes in enumerate(time_options)
    ]
    start_button = Button(
        WINDOW_WIDTH // 2 - 110,
        button_center_y + 80,
        220, 54,
        "START GAME",
        FONT_MEDIUM,
        is_accent=True,
    )
    all_buttons     = time_buttons + [start_button]
    application_state = "menu"
    active_game       = None
    promote_hitboxes  = []
 
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in all_buttons:
            button.update_hover((mouse_x, mouse_y))
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if application_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button, minutes in zip(time_buttons, time_options):
                        if button.is_clicked((mouse_x, mouse_y)):
                            selected_time = minutes
                    if start_button.is_clicked((mouse_x, mouse_y)):
                        active_game = Game(selected_time)
                        active_game.clock.switch("w")
                        application_state = "game"
 
            elif application_state == "game":
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_r
                ):
                    application_state = "menu"
                    active_game       = None
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if active_game.promote_sq:
                        for (hit_x, hit_y, hit_w, hit_h, piece_type) in promote_hitboxes:
                            if (
                                hit_x <= mouse_x <= hit_x + hit_w
                                and hit_y <= mouse_y <= hit_y + hit_h
                            ):
                                active_game.apply_promotion(piece_type)
                        continue
 
                    panel_x     = BOARD_OFFSET_X + 8 * SQUARE_SIZE + 28
                    panel_width = WINDOW_WIDTH - panel_x - 18
                    clock_mid_y = BOARD_OFFSET_Y + 96 + (SQUARE_SIZE * 8 - 192) // 2
                    clock_rect  = pygame.Rect(panel_x, clock_mid_y, panel_width, 52)
 
                    if clock_rect.collidepoint(mouse_x, mouse_y):
                        active_game.press_clock()
                        continue
 
                    board_rel_x = mouse_x - BOARD_OFFSET_X
                    board_rel_y = mouse_y - BOARD_OFFSET_Y
                    clicked_col = board_rel_x // SQUARE_SIZE
                    clicked_row = board_rel_y // SQUARE_SIZE
 
                    if (
                        0 <= clicked_row < 8
                        and 0 <= clicked_col < 8
                    ):
                        active_game.click_square(clicked_row, clicked_col)
 
        if application_state == "menu":
            renderer.draw_menu(selected_time, time_options, all_buttons)
 
        elif application_state == "game" and active_game:
            active_game.tick()
            screen.fill(COLOR_BACKGROUND)
            renderer.draw_board(active_game)
            renderer.draw_panel(active_game)
 
            if active_game.promote_sq:
                promote_hitboxes = renderer.draw_promote_menu(active_game)
            elif active_game.status == "w_win":
                subtext = "Checkmate" if active_game.clock.remaining["b"] > 0 else "On time"
                renderer.draw_overlay("White Wins", subtext)
            elif active_game.status == "b_win":
                subtext = "Checkmate" if active_game.clock.remaining["w"] > 0 else "On time"
                renderer.draw_overlay("Black Wins", subtext)
            elif active_game.status == "draw":
                renderer.draw_overlay("Draw", "Stalemate or insufficient material")
 
            pygame.display.flip()
 
        frame_clock.tick(60)
 
 
main()