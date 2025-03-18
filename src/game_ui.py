import pygame


class GameUi:
    def __init__(self, game):
        self.display = game.screen
        self.game = game
        self.box_width = 156
        self.box_height = 215
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.chip_rects = []
        self.button_rects = []
        self.player_card_boxes = []
        self.dealer_card_boxes = []

        self.create_chip_rects()
        self.create_button_rects()

        self.add_initial_card_boxes()
        self.draw()

    def draw(self):
        self.game.screen.blit(self.game.background_scaled, (0, 0))

        for box in self.dealer_card_boxes:
            self.draw_card_box(box[0], box[1])

        for box in self.player_card_boxes:
            self.draw_card_box(box[0], box[1])

        self.draw_chips()
        self.draw_buttons()
        self.draw_scores_and_bet()

    def add_initial_card_boxes(self):
        self.dealer_card_boxes.append((595, 95))
        self.dealer_card_boxes.append((755, 95))
        self.player_card_boxes.append((595, 550))
        self.player_card_boxes.append((755, 550))

    def draw_card_box(self, x, y):
        self.card_box = pygame.draw.rect(
            self.display,
            "red",
            (x, y, self.box_width, self.box_height),
            5,
            15,
        )

    def draw_chips(self):
        self.one_chip = pygame.image.load("img/chips/one_chip.png")
        self.one_chip = self.scale_chip(self.one_chip)
        self.display.blit(self.one_chip, (20, 680))

        self.five_chip = pygame.image.load("img/chips/five_chip.png")
        self.five_chip = self.scale_chip(self.five_chip)
        self.display.blit(self.five_chip, (110, 680))

        self.ten_chip = pygame.image.load("img/chips/ten_chip.png")
        self.ten_chip = self.scale_chip(self.ten_chip)
        self.display.blit(self.ten_chip, (200, 680))

        self.twentyfive_chip = pygame.image.load("img/chips/twentyfive_chip.png")
        self.twentyfive_chip = self.scale_chip(self.twentyfive_chip)
        self.display.blit(self.twentyfive_chip, (20, 770))

        self.fifty_chip = pygame.image.load("img/chips/fifty_chip.png")
        self.fifty_chip = self.scale_chip(self.fifty_chip)
        self.display.blit(self.fifty_chip, (110, 770))

        self.onehundred_chip = pygame.image.load("img/chips/onehundred_chip.png")
        self.onehundred_chip = self.scale_chip(self.onehundred_chip)
        self.display.blit(self.onehundred_chip, (200, 770))

    def create_chip_rects(self):
        self.one_chip_rect = pygame.Rect(20, 680, 80, 80)
        self.chip_rects.append((self.one_chip_rect, 1))

        self.five_chip_rect = pygame.Rect(110, 680, 80, 80)
        self.chip_rects.append((self.five_chip_rect, 5))

        self.ten_chip_rect = pygame.Rect(200, 680, 80, 80)
        self.chip_rects.append((self.ten_chip_rect, 10))

        self.twentyfive_chip_rect = pygame.Rect(20, 770, 80, 80)
        self.chip_rects.append((self.twentyfive_chip_rect, 25))

        self.fifty_chip_rect = pygame.Rect(110, 770, 80, 80)
        self.chip_rects.append((self.fifty_chip_rect, 50))

        self.onehundred_chip_rect = pygame.Rect(200, 770, 80, 80)
        self.chip_rects.append((self.onehundred_chip_rect, 100))

    def scale_chip(self, chip):
        return pygame.transform.scale(chip, (80, 80))

    def draw_buttons(self):
        pygame.draw.rect(self.display, "#FFD700", (500, 800, 150, 50), border_radius=15)
        self.display.blit(self.font.render("Deal", True, (0, 0, 0)), (540, 800))
        pygame.draw.rect(self.display, "#FFD700", (700, 800, 150, 50), border_radius=15)
        self.display.blit(self.font.render("Hit", True, (0, 0, 0)), (755, 800))
        pygame.draw.rect(self.display, "#FFD700", (900, 800, 150, 50), border_radius=15)
        self.display.blit(self.font.render("Stand", True, (0, 0, 0)), (930, 800))

    def create_button_rects(self):
        self.deal_button_rect = pygame.Rect(500, 800, 150, 50)
        self.button_rects.append((self.deal_button_rect, "deal"))
        self.hit_button_rect = pygame.Rect(700, 800, 150, 50)
        self.button_rects.append((self.hit_button_rect, "hit"))
        self.stand_button_rect = pygame.Rect(900, 800, 150, 50)
        self.button_rects.append((self.stand_button_rect, "stand"))

    def draw_scores_and_bet(self):
        self.display.blit(
            self.font.render(f"Credits: {self.game.player_credits}", True, "white"),
            (20, 20),
        )
        self.display.blit(
            self.font.render(f"Current Bet: {self.game.player_bet}", True, "white"),
            (250, 20),
        )
        self.display.blit(
            self.font.render(f"Dealer Score: {self.game.dealer_score}", True, "white"),
            (630, 40),
        )
        self.display.blit(
            self.font.render(f"Player Score: {self.game.player_score}", True, "white"),
            (630, 490),
        )
