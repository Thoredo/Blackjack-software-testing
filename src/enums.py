from enum import Enum


class GameState(Enum):
    BUSTED = "Busted"
    BLACKJACK = "Blackjack"
    BETTING = "Betting"
    PLAYERS_HAND = "Players Hand"
    DEALERS_HAND = "Dealers Hand"
    DRAW = "Draw"
    DEALER_BLACKJACK = "Dealer Blackjack"
    DEALER_BUSTED = "Dealer Busted"
    PLAYER_WON = "You Win"
    DEALER_WON = "Dealer Wins"
