# Game of Life.
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


import random
import re

import pygame


# pygame setup and variables
pygame.init()
WIDTH: int = 600
HIGHT: int = 700
SCREEN: pygame.Surface = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("Game Of Life")
CLOCK: pygame.time.Clock = pygame.time.Clock()
ROWS: int = 50
COLS: int = 50
LIVE_CELL: int = 1  # Live cell value
LIVE_CELL_COLOR: str = "green"
DEFAULT_CELL: int = 0
DEFAULT_CELL_COLOR: str = "white"
CELL_SIZE: int = WIDTH // ROWS
BORN: int = 3  # default
SURVIVOR: list[int] = [2, 3]  # default
FONT: pygame.font.Font = pygame.font.SysFont("comicsans", 20)


def get_neighbors(row: int, col: int):
    """Return all cell neighbors.

    Args:
        row (int): Cell row.
        col (int): Cell column.

    Returns:
        list|list[tuple[int]]: List of all neighbors.
    """
    neighbors: list | list[tuple[int]] = []

    if 0 <= row < ROWS and 0 <= col < COLS:
        if row > 0:  # up
            neighbors.append((row - 1, col))
        if row < ROWS - 1:  # down
            neighbors.append((row + 1, col))
        if col > 0:  # left
            neighbors.append((row, col - 1))
        if col < COLS - 1:  # right
            neighbors.append((row, col + 1))
        if row > 0 and col > 0:  # up left
            neighbors.append((row - 1, col - 1))
        if row > 0 and col < COLS - 1:  # up right
            neighbors.append((row - 1, col + 1))
        if row < ROWS - 1 and col > 0:  # down left
            neighbors.append((row + 1, col - 1))
        if row < ROWS - 1 and col < COLS - 1:  # down right
            neighbors.append((row + 1, col + 1))

    return neighbors


def create_grid():
    """Create game grid(50X50).

    Returns:
        list: List of 50 lists with 50 cells each.
    """
    grid: list[list[int]] = [
        [DEFAULT_CELL for _ in range(COLS)] for _ in range(ROWS)]
    return grid


def get_count_live_neighbors(grid: list[list[int]], neighbors: list[tuple[int]]):
    """Count all live neighbors.

    Args:
        grid (list[list[int]]): List of all game cells.
        neighbors (list[tuple[int]]): List of all neighbors.

    Returns:
        int: Count of live neighbors.
    """
    live_neighbors: int = 0
    for row, col in neighbors:
        if grid[row][col] == LIVE_CELL:
            live_neighbors += 1
    return live_neighbors


def changing_cell_status(grid: list[list[int]], row: int, col: int, live_cell_count: int):
    """Changing cell status to live or dead.

    Args:
        grid (list[list[int]]): List of all game cells.
        row (int): Cell row.
        col (int): Cell column.
        live_cell_count (int): Count of live neighbors.

    Returns:
        tuple: Grid and live_cell_count.
    """
    if 0 <= row < ROWS and 0 <= col < COLS:
        if grid[row][col] == DEFAULT_CELL:
            grid[row][col] = LIVE_CELL
            live_cell_count += 1
        elif grid[row][col] == LIVE_CELL:
            grid[row][col] = DEFAULT_CELL
            live_cell_count -= 1
    return grid, live_cell_count


def update_grid(grid: list[list[int]], born: int, survivor: list[int], live_cell_count: int):
    """Update the game grid.

    Args:
        grid (list[list[int]]): List of all game cells.
        born (int): The required number of neighbors to `born` a dead cell.
        survivor (list[int]):Min and max required numbers of neighbors for cell to `survive`.
        live_cell_count (int): Count of live neighbors.

    Returns:
        tuple: Grid and live_cell_count.
    """
    new_grid: list[list[int]] = create_grid()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors: list | list[tuple[int]] = get_neighbors(row, col)
            count_live_neighbors: int = get_count_live_neighbors(grid, neighbors)
            if grid[row][col] != LIVE_CELL and count_live_neighbors == born:
                new_grid[row][col] = LIVE_CELL
                live_cell_count += 1
            elif grid[row][col] == LIVE_CELL and \
                    survivor[0] <= count_live_neighbors <= survivor[1]:
                new_grid[row][col] = LIVE_CELL

            # Because in the next turn he dies
            elif grid[row][col] == LIVE_CELL:
                live_cell_count -= 1
    return new_grid, live_cell_count


def draw_game_buttons(start_game_text: str):
    """Draw game buttons.

    Args:
        start_game_text (str): text: start or stop.

    Returns:
        tuple: pygame.Rect(buttons).
    """
    SCREEN.fill("white")
    # Start game button
    start_stop: pygame.Rect = pygame.draw.rect(SCREEN, LIVE_CELL_COLOR, ((
        WIDTH - 200) / 2, 620, 200, CELL_SIZE * 4))
    start_stop_text: pygame.font.Font = FONT.render(
        start_game_text, 1, DEFAULT_CELL_COLOR)
    SCREEN.blit(start_stop_text,
                ((WIDTH - start_stop_text.get_width()) / 2, 628))
    # Random game button
    random_game_text: pygame.font.Font = FONT.render(
        "Random Game", 1, DEFAULT_CELL_COLOR)
    random_game: pygame.Rect = pygame.draw.rect(SCREEN, LIVE_CELL_COLOR, ((
        WIDTH - random_game_text.get_width()) - 30, 660, random_game_text.get_width() + 20, CELL_SIZE * 3))
    SCREEN.blit(random_game_text,
                ((WIDTH - random_game_text.get_width()) - 20, 660))
    return start_stop, random_game


def draw(grid: list[list[int]], live_cell_count: int, generations: int):
    """Draw the game(pygame).

    Args:
        grid (list[list[int]]): List of all game cells.
        live_cell_count (int): Count of live neighbors.
        generations (int): Count of game generations.
    """
    live_cell_count_text: pygame.font.Font = FONT.render(
        f"Live cells: {live_cell_count}", 1, LIVE_CELL_COLOR)
    SCREEN.blit(live_cell_count_text, (10, 600))
    generations_text: pygame.font.Font = FONT.render(
        f"Generations: {generations}", 1, LIVE_CELL_COLOR)
    SCREEN.blit(generations_text, (10, 628))

    for row_index, row in enumerate(grid):
        left: int = CELL_SIZE * row_index
        for col_index, cell_value in enumerate(row):
            top: int = CELL_SIZE * col_index
            if cell_value == LIVE_CELL:
                pygame.draw.rect(SCREEN, LIVE_CELL_COLOR,
                                 (left, top, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(SCREEN, DEFAULT_CELL_COLOR,
                                 (left, top, CELL_SIZE, CELL_SIZE))

            # border
            pygame.draw.rect(SCREEN, "gray", (left, top, CELL_SIZE, CELL_SIZE), 1)

    pygame.display.update()


def random_game_generation(grid: list[list[int]], live_cell_count: int):
    """Generate random game.

    Args:
        grid (list[list[int]]): List of all game cells.
        live_cell_count (int): Count of live neighbors.

    Returns:
        tuple: Grid and live_cell_count.
    """
    for _ in range(random.randint(20, 300)):
        index: tuple[int, int] = (random.randint(0, COLS), random.randint(0, COLS))
        grid, live_cell_count = changing_cell_status(
            grid, *index, live_cell_count)
    return grid, live_cell_count


def game(born: int, survivor: list[int]):
    """Run the game.

    Args:
        born (int): The required number of neighbors to `born` a dead cell.
        survivor (list[int]): Min and max required numbers of neighbors for cell to `survive`.
    """
    run: bool = True

    grid: list[list[int]] = create_grid()
    start_game: bool = False
    start_game_text: str = "Start"
    live_cell_count: int = 0
    generations: int = 0

    while run:
        start_stop, random_game = draw_game_buttons(start_game_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run: bool = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos: tuple[int, int] = event.pos
                if not start_game:
                    index = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
                    grid, live_cell_count = changing_cell_status(
                        grid, *index, live_cell_count)

                if pygame.Rect.collidepoint(random_game, *pos) and not start_game:
                    grid, live_cell_count = random_game_generation(
                        grid, live_cell_count)

                if pygame.Rect.collidepoint(start_stop, *pos) and not start_game:
                    start_game: bool = True
                    start_game_text: str = "Stop"
                elif pygame.Rect.collidepoint(start_stop, *pos) and start_game:
                    start_game: bool = False
                    start_game_text: str = "Start"
                
                if live_cell_count == 0:  # Stop the game if 0 cells are alive.
                    start_game: bool = False
                    start_game_text: str = "Start"

        if start_game:  # Automatic play
            generations += 1
            grid, live_cell_count = update_grid(
                grid, born, survivor,  live_cell_count)
        
        if live_cell_count == 0:  # Stop the game if 0 cells are alive.
            start_game: bool = False
            start_game_text: str = "Start"

        draw(grid, live_cell_count, generations)
        CLOCK.tick(30)

    pygame.quit()


def game_of_life(game_legality: str):
    """Sets the rules of the game according to user input.
    `B(born)number/S(survivor)two numbers`(B3/S23)

    Args:
        game_legality (str): User input.
    """
    regex: str = r"^B(\d)/S(\d)(\d)$"
    matches: list = re.findall(regex, game_legality)
    if matches:
        born: int = int(matches[0][0])
        survivor: list[int] = [int(matches[0][1]), int(matches[0][2])]
    else:
        born: int = BORN
        survivor: list[int] = SURVIVOR
    game(born, survivor)


def main():
    born: int = BORN
    survivor: list[int] = SURVIVOR
    game(born, survivor)


if __name__ == "__main__":
    main()
