import random


class Cards:
    def __init__(self):
        # fmt: off
        self.possible_cards = {
            "clubs_2": 2, "clubs_3": 3, "clubs_4": 4, "clubs_5": 5,
            "clubs_6": 6, "clubs_7": 7, "clubs_8": 8, "clubs_9": 9,
            "clubs_10": 10, "clubs_J": 10, "clubs_Q": 10,
            "clubs_K": 10, "clubs_A": 11,
            "diamonds_2": 2, "diamonds_3": 3, "diamonds_4": 4, "diamonds_5": 5,
            "diamonds_6": 6, "diamonds_7": 7, "diamonds_8": 8, "diamonds_9": 9,
            "diamonds_10": 10, "diamonds_J": 10, "diamonds_Q": 10,
            "diamonds_K": 10, "diamonds_A": 11,
            "hearts_2": 2, "hearts_3": 3, "hearts_4": 4, "hearts_5": 5,
            "hearts_6": 6, "hearts_7": 7, "hearts_8": 8, "hearts_9": 9,
            "hearts_10": 10, "hearts_J": 10, "hearts_Q": 10,
            "hearts_K": 10, "hearts_A": 11,
            "spades_2": 2, "spades_3": 3, "spades_4": 4, "spades_5": 5,
            "spades_6": 6, "spades_7": 7, "spades_8": 8, "spades_9": 9,
            "spades_10": 10, "spades_J": 10, "spades_Q": 10,
            "spades_K": 10, "spades_A": 11,
        }
        # fmt: on

    def select_card(self):
        return random.choice(list(self.possible_cards.items()))
