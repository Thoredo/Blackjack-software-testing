import sys
import os
import pytest
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import Game
from game_ui import GameUi
from gamecontroller import GameController
from enums import GameState


@pytest.fixture
def setup_game():
    pygame.init()

    game = Game()

    game_ui = GameUi(game)
    game_ui.button_rects = []
    game_ui.create_button_rects()

    game_controller = GameController(game, game_ui.button_rects)

    return game, game_controller


def test_deal_button_only_works_when_bet_above_zero(setup_game):
    game, game_controller = setup_game

    # Test if hands stay empty and gamestates stays betting when player bet = 0
    assert game.player_bet == 0
    game_controller.deal_cards()
    assert game.current_phase == GameState.BETTING
    assert len(game_controller.player_cards) == 0
    assert len(game_controller.dealer_cards) == 0

    # Test if hands get 2 cards and gamestates switches to players hand when bet is > 0
    game.player_bet = 1
    game_controller.deal_cards()
    assert game.current_phase != GameState.BETTING
    assert len(game_controller.player_cards) == 2
    assert len(game_controller.dealer_cards) == 2


@pytest.mark.parametrize(
    "current_game_state, expected_hand_size",
    [
        (GameState.BUSTED, 0),
        (GameState.BLACKJACK, 0),
        (GameState.PLAYERS_HAND, 0),
        (GameState.DEALERS_HAND, 0),
        (GameState.DRAW, 0),
        (GameState.DEALER_BLACKJACK, 0),
        (GameState.DEALER_BUSTED, 0),
        (GameState.PLAYER_WON, 0),
        (GameState.DEALER_WON, 0),
    ],
)
def test_deal_button_does_not_work_in_non_betting_states(
    setup_game, current_game_state, expected_hand_size
):
    game, game_controller = setup_game

    game.player_bet = 1
    game.current_phase = current_game_state
    game_controller.deal_cards()
    assert game.current_phase == current_game_state
    assert len(game_controller.player_cards) == expected_hand_size
    assert len(game_controller.dealer_cards) == expected_hand_size


def test_hit_button_raises_player_cards_by_one(setup_game):
    game, game_controller = setup_game

    game.player_bet = 1
    game_controller._deal_initial_cards()

    assert len(game_controller.player_cards) == 2

    game_controller.handle_hit()

    assert len(game_controller.player_cards) == 3


@pytest.mark.parametrize(
    "current_game_state",
    [
        GameState.BUSTED,
        GameState.BLACKJACK,
        GameState.BETTING,
        GameState.DEALERS_HAND,
        GameState.DRAW,
        GameState.DEALER_BLACKJACK,
        GameState.DEALER_BUSTED,
        GameState.PLAYER_WON,
        GameState.DEALER_WON,
    ],
)
def test_hit_button_does_not_work_in_non_players_hand_states(
    setup_game, current_game_state
):
    game, game_controller = setup_game

    game.current_phase = current_game_state
    initial_hand_size = len(game_controller.player_cards)

    game_controller.handle_hit()

    assert game.current_phase == current_game_state
    assert len(game_controller.player_cards) == initial_hand_size


def test_stand_button_changes_game_state_from_players_hand(setup_game):
    game, game_controller = setup_game

    possible_game_states = [
        GameState.DEALER_BUSTED,
        GameState.DEALER_WON,
        GameState.DRAW,
        GameState.PLAYER_WON,
    ]

    game.player_bet = 1
    game_controller._deal_initial_cards()

    assert game.current_phase == GameState.PLAYERS_HAND

    game_controller.handle_stand()

    assert game.current_phase in possible_game_states


@pytest.mark.parametrize(
    "current_game_state",
    [
        GameState.BUSTED,
        GameState.BLACKJACK,
        GameState.BETTING,
        GameState.DEALERS_HAND,
        GameState.DRAW,
        GameState.DEALER_BLACKJACK,
        GameState.DEALER_BUSTED,
        GameState.PLAYER_WON,
        GameState.DEALER_WON,
    ],
)
def test_stand_button_does_not_work_in_non_players_hand_states(
    setup_game, current_game_state
):
    game, game_controller = setup_game

    game.current_phase = current_game_state

    game_controller.handle_stand()

    assert game.current_phase == current_game_state


def test_reset_button_not_in_button_rects_during_betting_or_players_hand(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.BETTING
    assert (
        any(rect for rect in game_controller.button_rects if rect[1] == "reset")
        is False
    )

    game.current_phase = GameState.PLAYERS_HAND
    assert (
        any(rect for rect in game_controller.button_rects if rect[1] == "reset")
        is False
    )


def test_reset_game_sets_player_bet_to_zero(setup_game):
    game, game_controller = setup_game

    game.player_bet = 50
    game_controller.reset_game()

    assert game.player_bet == 0


def test_reset_game_sets_player_score_to_zero(setup_game):
    game, game_controller = setup_game

    game.player_score = 50
    game_controller.reset_game()

    assert game.player_score == 0


def test_reset_game_sets_dealer_score_to_zero(setup_game):
    game, game_controller = setup_game

    game.dealer_score = 50
    game_controller.reset_game()

    assert game.dealer_score == 0


def test_reset_game_clears_player_cards(setup_game):
    game, game_controller = setup_game

    game_controller._deal_initial_cards()
    assert len(game_controller.player_cards) > 0

    game_controller.reset_game()

    assert len(game_controller.player_cards) == 0


def test_reset_game_clears_dealer_cards(setup_game):
    game, game_controller = setup_game

    game_controller._deal_initial_cards()
    assert len(game_controller.dealer_cards) > 0

    game_controller.reset_game()

    assert len(game_controller.dealer_cards) == 0


def test_credits_decrease_if_player_has_lower_score_than_dealer(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 15
    game_controller.dealer_total_score = 20

    game_controller.handle_stand()

    credit_difference = initial_credits - game.player_bet

    assert game.current_phase == GameState.DEALER_WON
    assert game.player_credits < initial_credits
    assert credit_difference == initial_credits - game.player_credits


def test_credits_decrease_if_player_is_busted(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()

    # To prevent inconsistencies with aces i made the score and aces_change
    # extra high so when the players cards contain an ace this test doesnt fail.
    game.player_score = 41
    game_controller.aces_changed = 10

    game_controller.handle_hit()

    credit_difference = initial_credits - game.player_bet

    assert game.current_phase == GameState.BUSTED
    assert game.player_credits < initial_credits
    assert credit_difference == initial_credits - game.player_credits


def test_credits_decrease_if_dealer_blackjack(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 15
    game_controller.dealer_total_score = 21

    game_controller._handle_special_cases()

    credit_difference = initial_credits - game.player_bet

    assert game.current_phase == GameState.DEALER_BLACKJACK
    assert game.player_credits < initial_credits
    assert credit_difference == initial_credits - game.player_credits


def test_credits_increase_if_player_has_higher_score_than_dealer(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 20
    game_controller.dealer_total_score = 19

    game_controller.handle_stand()

    credit_difference = initial_credits - game.player_bet

    assert game.current_phase == GameState.PLAYER_WON
    assert game.player_credits > initial_credits
    assert credit_difference == game.player_credits - initial_credits


def test_credits_increase_if_dealer_is_busted(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 15
    game_controller.dealer_total_score = 25

    game_controller.handle_stand()

    credit_difference = initial_credits - game.player_bet

    assert game.current_phase == GameState.DEALER_BUSTED
    assert game.player_credits > initial_credits
    assert credit_difference == game.player_credits - initial_credits


def test_credits_increase_if_player_has_blackjack(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 21
    game_controller.dealer_total_score = 17

    game_controller._handle_special_cases()

    credit_difference = game.player_bet * 1.5

    assert game.current_phase == GameState.BLACKJACK
    assert game.player_credits > initial_credits
    assert credit_difference == game.player_credits - initial_credits


def test_credits_stay_same_if_player_and_dealer_have_same_score(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 17
    game_controller.dealer_total_score = 17

    game_controller.handle_stand()

    assert game.current_phase == GameState.DRAW
    assert game.player_credits == initial_credits


def test_credits_stay_same_if_player_and_dealer_both_have_blackjack(setup_game):
    game, game_controller = setup_game

    initial_credits = 100
    game.player_credits = initial_credits
    game.player_bet = 50

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 21
    game_controller.dealer_total_score = 21

    game_controller._handle_special_cases()

    assert game.current_phase == GameState.DRAW
    assert game.player_credits == initial_credits


def test_face_down_card_dealer_gets_shown_when_player_has_blackjack(setup_game):
    game, game_controller = setup_game

    game_controller._deal_initial_cards()
    game.player_score = 21
    game_controller.dealer_total_score = 18
    game_controller._handle_special_cases()

    assert game.current_phase == GameState.BLACKJACK
    assert game_controller.dealer_cards[1][0] == "back_dark"


def test_face_down_card_dealer_gets_shown_when_player_gets_busted(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()

    # To prevent inconsistencies with aces i made the score and aces_change
    # extra high so when the players cards contain an ace this test doesnt fail.
    game.player_score = 41
    game_controller.aces_changed = 10

    game_controller.handle_hit()

    assert game.current_phase == GameState.BUSTED
    assert game_controller.dealer_cards[1][0] == "back_dark"


def test_face_down_card_dealer_gets_shown_when_dealer_gets_blackjack(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 15
    game_controller.dealer_total_score = 21

    game_controller._handle_special_cases()

    assert (
        game.current_phase == GameState.DEALER_BLACKJACK
        or game.current_phase == GameState.DRAW
    )
    assert game_controller.dealer_cards[1][0] != "back_dark"


def test_face_down_card_dealer_gets_shown_when_player_ends_his_turn(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()

    game_controller.handle_stand()

    assert game.current_phase != GameState.PLAYERS_HAND
    assert game_controller.dealer_cards[1][0] != "back_dark"


def test_score_above_twenty_one_makes_game_state_busted(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()

    # To prevent inconsistencies with aces i made the score and aces_change
    # extra high so when the players cards contain an ace this test doesnt fail.
    game.player_score = 41
    game_controller.aces_changed = 10

    game_controller.handle_hit()

    assert game.current_phase == GameState.BUSTED


def test_score_of_twenty_one_during_dealing_makes_game_state_blackjack(setup_game):
    game, game_controller = setup_game

    game_controller._deal_initial_cards()
    game.player_score = 21
    game_controller.dealer_total_score = 18
    game_controller._handle_special_cases()

    assert game.current_phase == GameState.BLACKJACK


def test_when_only_dealer_begins_with_twenty_one_game_state_becomes_dealer_blackjack(
    setup_game,
):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 15
    game_controller.dealer_total_score = 21

    game_controller._handle_special_cases()

    assert game.current_phase == GameState.DEALER_BLACKJACK


def test_when_both_begin_with_twenty_one_game_state_becomes_draw(setup_game):
    game, game_controller = setup_game

    game.current_phase = GameState.PLAYERS_HAND
    game_controller._deal_initial_cards()
    game.player_score = 21
    game_controller.dealer_total_score = 21

    game_controller._handle_special_cases()

    assert game.current_phase == GameState.DRAW
