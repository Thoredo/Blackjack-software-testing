from cards import Cards
from enums import GameState


class BettingLogic:
    def __init__(self, game, chip_rects):
        self.display = game.screen
        self.game = game
        self.chip_rects = chip_rects
        self.cards = Cards()

    def check_chip_clicked(self, mouse_position):
        for rect in self.chip_rects:
            if rect[0].collidepoint(mouse_position):
                if self.game.current_phase == GameState.BETTING:
                    bet_value = rect[1]
                    self.game.player_bet += bet_value
                    self.enough_credits_validation(bet_value)
                    self.cards.select_card()

    def enough_credits_validation(self, bet_value):
        if self.game.player_bet > self.game.player_credits:
            self.game.player_bet -= bet_value
