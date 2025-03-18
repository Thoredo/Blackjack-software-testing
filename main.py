import pygame
from game_ui import GameUi
from betting import BettingLogic
from gamecontroller import GameController
from enums import GameState


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1600
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_credits = 5000
        self.player_bet = 0
        self.player_score = 0
        self.dealer_score = 0
        self.current_phase = GameState.BETTING

        self.background_image = pygame.image.load("img/background.jpg")
        self.background_scaled = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height)
        )

        self.game_ui = GameUi(self)
        self.betting_logic = BettingLogic(self, self.game_ui.chip_rects)
        self.game_controller = GameController(self, self.game_ui.button_rects)

    def close_game(self):
        self.running = False

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.close_game()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    self.betting_logic.check_chip_clicked(mouse_position)
                    self.game_controller.check_buttons_clicked(mouse_position)
                    self.game_ui.draw()
                    self.game_controller.draw()

                pygame.display.flip()
                self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()
