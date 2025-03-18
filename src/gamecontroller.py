import pygame
from cards import Cards
from enums import GameState


class GameController:
    def __init__(self, game, button_rects):

        self.game = game
        self.display = game.screen
        self.button_rects = button_rects
        self.cards = Cards()
        self.player_cards = []
        self.dealer_cards = []
        self.busted_font = pygame.font.SysFont("Arial", 100, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.aces = ["clubs_A", "diamonds_A", "hearts_A", "spades_A"]
        self.ace_count = 0
        self.aces_changed = 0
        self.dealer_ace_count = 0
        self.dealer_aces_changed = 0
        self.dealer_total_score = 0
        self.dealer_card_two = ""

    def check_buttons_clicked(self, mouse_position):

        for rect in self.button_rects:
            if rect[0].collidepoint(mouse_position):
                if rect[1] == "deal":
                    self.deal_cards()
                if rect[1] == "hit":
                    self.handle_hit()
                if rect[1] == "stand":
                    self.handle_stand()
                if rect[1] == "reset":
                    self.reset_game()

    def deal_cards(self):

        if self.game.current_phase != GameState.BETTING or self.game.player_bet <= 0:
            return

        self._deal_initial_cards()
        self._handle_special_cases()

    def _deal_initial_cards(self):

        player_card_one = self.cards.select_card()
        player_card_two = self.cards.select_card()
        dealer_card_one = self.cards.select_card()
        self.dealer_card_two = self.cards.select_card()

        self.player_cards.append((player_card_one[0], (600, 555)))
        self.player_cards.append((player_card_two[0], (760, 555)))
        self.dealer_cards.append((dealer_card_one[0], (600, 100)))
        self.dealer_cards.append(("back_dark", (760, 100)))

        self._update_scores(player_card_one[1], player_card_two[1], dealer_card_one[1])

    def _update_scores(
        self, player_card_one_score, player_card_two_score, dealer_card_one_score
    ):

        self.game.player_score += player_card_one_score + player_card_two_score
        self.game.dealer_score += dealer_card_one_score
        self.dealer_total_score += dealer_card_one_score + self.dealer_card_two[1]

        self.game.current_phase = GameState.PLAYERS_HAND

    def _handle_special_cases(self):

        if self.game.player_score == 22:
            self.game.player_score = 12
            self.aces_changed = 1
        elif self.dealer_total_score == 21:
            if self.game.player_score == 21:
                self.game.current_phase = GameState.DRAW
            else:
                self.game.current_phase = GameState.DEALER_BLACKJACK
                self.game.player_credits -= self.game.player_bet
            self.game.dealer_score = self.dealer_total_score
            self.dealer_cards[1] = (self.dealer_card_two[0], (760, 100))
        elif self.game.player_score == 21:
            self.game.current_phase = GameState.BLACKJACK
            self.game.player_credits += round(self.game.player_bet * 1.5)

    def draw(self):
        self.draw_all_cards()
        if (
            self.game.current_phase != GameState.PLAYERS_HAND
            and self.game.current_phase != GameState.DEALERS_HAND
            and self.game.current_phase != GameState.BETTING
        ):
            self.draw_end_game_ui()

    def draw_all_cards(self):
        for card in self.player_cards:
            card_image = pygame.image.load(f"img/playing-cards-master/{card[0]}.png")
            card_image = pygame.transform.scale(card_image, (146, 205))
            self.display.blit(card_image, card[1])
        for card in self.dealer_cards:
            card_image = pygame.image.load(f"img/playing-cards-master/{card[0]}.png")
            card_image = pygame.transform.scale(card_image, (146, 205))
            self.display.blit(card_image, card[1])

    def handle_hit(self):
        if self.game.current_phase == GameState.PLAYERS_HAND:
            new_card = self.cards.select_card()
            x_coord_multiplier = len(self.player_cards) - 1
            x_coord = 760 + (160 * x_coord_multiplier)
            self.player_cards.append((new_card[0], (x_coord, 555)))
            self.game.player_score += new_card[1]
            self.game.game_ui.player_card_boxes.append((x_coord - 5, 550))
        if (
            self.game.player_score > 21
            and self.game.current_phase == GameState.PLAYERS_HAND
        ):
            for card in self.player_cards:
                if card[0] in self.aces:
                    self.ace_count += 1
            if self.ace_count > self.aces_changed:
                self.game.player_score -= 10
                self.aces_changed += 1
                self.ace_count = 0
            else:
                self.game.player_credits -= self.game.player_bet
                self.game.current_phase = GameState.BUSTED

    def handle_stand(self):
        if self.game.current_phase == GameState.PLAYERS_HAND:
            self.game.current_phase = GameState.DEALERS_HAND
            self.dealer_cards[1] = (self.dealer_card_two[0], (760, 100))
            self.game.dealer_score = self.dealer_total_score

            while self.game.dealer_score < 17:
                self.give_dealer_card()

            if self.game.dealer_score > 21:
                self.game.current_phase = GameState.DEALER_BUSTED
                self.game.player_credits += self.game.player_bet
            elif self.game.dealer_score > self.game.player_score:
                self.game.current_phase = GameState.DEALER_WON
                self.game.player_credits -= self.game.player_bet
            elif self.game.dealer_score == self.game.player_score:
                self.game.current_phase = GameState.DRAW
            else:
                self.game.current_phase = GameState.PLAYER_WON
                self.game.player_credits += self.game.player_bet

    def give_dealer_card(self):
        new_card = self.cards.select_card()
        x_coord_multiplier = len(self.dealer_cards) - 1
        x_coord = 760 + (160 * x_coord_multiplier)
        self.dealer_cards.append((new_card[0], (x_coord, 100)))
        self.game.dealer_score += new_card[1]
        self.game.game_ui.dealer_card_boxes.append((x_coord - 5, 95))
        if (
            self.game.dealer_score > 21
            and self.game.current_phase == GameState.DEALERS_HAND
        ):
            for card in self.dealer_cards:
                if card[0] in self.aces:
                    self.dealer_ace_count += 1
            if self.dealer_ace_count > self.dealer_aces_changed:
                self.game.dealer_score -= 10
                self.dealer_aces_changed += 1
                self.dealer_ace_count = 0
            else:
                self.game.player_credits -= self.game.player_bet
                self.game.current_phase = GameState.BUSTED

    def draw_end_game_ui(
        self,
    ):
        match self.game.current_phase:
            case GameState.BUSTED:
                text_position = (620, 310)
            case GameState.BLACKJACK:
                text_position = (560, 310)
            case GameState.DRAW:
                text_position = (655, 310)
            case GameState.DEALER_BLACKJACK:
                text_position = (430, 310)
            case GameState.PLAYER_WON:
                text_position = (590, 310)
            case GameState.DEALER_WON:
                text_position = (520, 310)
            case GameState.DEALER_BUSTED:
                text_position = (480, 310)
        self.display.blit(
            self.busted_font.render(self.game.current_phase.value, True, "red"),
            text_position,
        )

        pygame.draw.rect(self.display, "#FFD700", (680, 430, 150, 50), border_radius=15)
        self.display.blit(self.button_font.render("Reset", True, (0, 0, 0)), (710, 430))

        if not any(rect[1] == "reset" for rect in self.button_rects):
            self.reset_button_rect = pygame.Rect(680, 430, 150, 50)
            self.button_rects.append((self.reset_button_rect, "reset"))

    def reset_game(self):

        self.player_cards = []
        self.dealer_cards = []
        self.game.player_bet = 0
        self.game.player_score = 0
        self.game.dealer_score = 0
        self.dealer_total_score = 0
        self.game.game_ui.player_card_boxes = []
        self.game.game_ui.dealer_card_boxes = []
        self.game.game_ui.add_initial_card_boxes()
        self.game.current_phase = GameState.BETTING
        self.ace_count = 0
        self.aces_changed = 0
        self.dealer_aces_changed = 0
