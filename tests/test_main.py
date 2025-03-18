import sys
import os
import pytest
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import Game
from enums import GameState


@pytest.fixture
def setup_game():
    pygame.init()

    game = Game()

    return game


def test_player_credits(setup_game):
    game = setup_game

    assert game.player_credits == 5000


def test_player_bet(setup_game):
    game = setup_game

    assert game.player_bet == 0


def test_player_score(setup_game):
    game = setup_game

    assert game.player_score == 0


def test_dealer_score(setup_game):
    game = setup_game

    assert game.dealer_score == 0


def test_game_state(setup_game):
    game = setup_game

    assert game.current_phase == GameState.BETTING
