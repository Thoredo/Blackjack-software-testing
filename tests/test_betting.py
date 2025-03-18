import sys
import os
import pytest
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game_ui import GameUi
from betting import BettingLogic
from enums import GameState
from main import Game


@pytest.fixture
def setup_betting_logic():
    pygame.init()

    game = Game()

    game_ui = GameUi(game)
    game_ui.chip_rects = []
    game_ui.create_chip_rects()

    betting_logic = BettingLogic(game, game_ui.chip_rects)

    return game, betting_logic


@pytest.mark.parametrize(
    "click_position, expected_bet",
    [
        ((20, 680), 1),
        ((110, 680), 5),
        ((200, 680), 10),
        ((20, 770), 25),
        ((110, 770), 50),
        ((200, 770), 100),
    ],
)
def test_chip_click_adds_correct_bet_amount(
    setup_betting_logic, click_position, expected_bet
):
    game, betting_logic = setup_betting_logic

    betting_logic.check_chip_clicked(click_position)

    assert game.current_phase == GameState.BETTING
    assert game.player_bet == expected_bet


@pytest.mark.parametrize(
    "current_game_state, expected_bet",
    [
        (GameState.BUSTED, 0),
        (GameState.BLACKJACK, 0),
        (GameState.BETTING, 1),
        (GameState.PLAYERS_HAND, 0),
        (GameState.DEALERS_HAND, 0),
        (GameState.DRAW, 0),
        (GameState.DEALER_BLACKJACK, 0),
        (GameState.DEALER_BUSTED, 0),
        (GameState.PLAYER_WON, 0),
        (GameState.DEALER_WON, 0),
    ],
)
def test_only_bet_in_betting_phase(
    setup_betting_logic, current_game_state, expected_bet
):
    game, betting_logic = setup_betting_logic
    game.current_phase = current_game_state

    betting_logic.check_chip_clicked((20, 680))

    assert game.current_phase == current_game_state
    assert game.player_bet == expected_bet


def test_no_bet_above_credit_balance(setup_betting_logic):
    game, betting_logic = setup_betting_logic

    game.player_credits = 10
    game.player_bet = 0

    # raise bet by 1
    betting_logic.check_chip_clicked((20, 680))
    assert game.player_bet == 1
    # raise bet by 10
    betting_logic.check_chip_clicked((200, 680))
    assert game.player_bet == 1
    # raise bet by 1
    betting_logic.check_chip_clicked((20, 680))
    assert game.player_bet == 2
