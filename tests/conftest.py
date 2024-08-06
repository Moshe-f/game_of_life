from unittest.mock import patch

import pytest

import game_of_life.game as game


@pytest.fixture
def game_grid(scope="function"):
    return game.create_grid()


@pytest.fixture
def mock_update():
    with patch("pygame.display.update") as mock:
        yield mock


@pytest.fixture
def mock_rect():
    with patch("pygame.draw.rect") as mock:
        yield mock


@pytest.fixture
def mock_changing_cell_status():
    with patch("game_of_life.game.changing_cell_status", side_effect=game.changing_cell_status) as mock:
        yield mock


@pytest.fixture
def mock_update_grid():
    with patch("game_of_life.game.update_grid", side_effect=game.update_grid) as mock:
        yield mock


@pytest.fixture
def mock_draw():
    with patch("game_of_life.game.draw", side_effect=game.draw) as mock:
        yield mock


@pytest.fixture
def mock_random_game_generation():
    with patch("game_of_life.game.random_game_generation") as mock:
        mock.return_value = (game.create_grid(), 0)
        yield mock
