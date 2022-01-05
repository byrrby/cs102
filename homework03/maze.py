from copy import deepcopy
from random import choice, randint, seed
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:

    if grid[coord[0]][coord[1]] != " ":
        grid[coord[0]][coord[1]] = " "
    elif coord[1] + 1 < len(grid[0]) - 1:
        grid[coord[0]][coord[1] + 1] = " "
    elif coord[0] - 1 > 1:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    grid[beginning[0]][beginning[1]] = "X"
    grid[ending[0]][ending[1]] = "X"

    for y_coordinate_curr in range(1, rows, 2):
        for x_coordinate_curr in range(1, cols, 2):
            direction = randint(0, 1)
            if direction == 1:
                if y_coordinate_curr != 1:
                    grid[y_coordinate_curr - 1][x_coordinate_curr] = " "
                else:
                    if x_coordinate_curr != cols - 2:
                        grid[y_coordinate_curr][x_coordinate_curr + 1] = " "
            else:
                if y_coordinate_curr != 1:
                    grid[y_coordinate_curr - 1][x_coordinate_curr] = " "
                else:
                    if x_coordinate_curr != cols - 2:
                        grid[y_coordinate_curr][x_coordinate_curr + 1] = " "

    if random_exit:
        beginning = (0, randint(0, rows - 1))
        ending = (randint(0, rows - 1), 0)
    else:
        beginning = (0, rows - 1)
        ending = (cols - 1, 0)

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:

    ans = []
    rows = len(grid) - 1
    columns = len(grid[0]) - 1

    for j in range(rows):
        if grid[j][0] == "X":
            ans.append((j, 0))
    for i in range(columns):
        if grid[0][i] == "X":
            ans.append((0, i))

    if len(ans) != 2:
        for j in range(rows):
            if grid[j][columns] == "X":
                ans.append((j, columns))
        for i in range(columns):
            if grid[rows][i] == "X":
                ans.append((rows, i))
    if len(ans) > 1:
        if ans[1][1] < ans[0][1]:
            ans[0], ans[1] = ans[1], ans[0]
        if ans[1][0] < ans[0][0]:
            ans[0], ans[1] = ans[1], ans[0]

    return ans


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k:
                if grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
            elif grid[i][j] == k and grid[i][j] == 1:
                if i == 0:
                    grid[i + 1][j] = k + 1
                if j == 0:
                    grid[i][j + 1] = k + 1
                if i == len(grid) - 1:
                    grid[i - 1][j] = k + 1
                if j == len(grid[0]) - 1:
                    grid[i][j - 1] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coordinate: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:

    path_way = [exit_coordinate]
    x = exit_coordinate[0]
    y = exit_coordinate[1]
    shortest = grid[x][y]
    k = int(shortest)
    while k > 1:
        if x != len(grid) - 1 and grid[x + 1][y] == k - 1:
            x += 1
            path_way.append((x, y))
        if y != len(grid[0]) - 1 and grid[x][y + 1] == k - 1:
            y += 1
            path_way.append((x, y))
        if x != 0 and grid[x - 1][y] == k - 1:
            x -= 1
            path_way.append((x, y))
        if y != 0 and grid[x][y - 1] == k - 1:
            y -= 1
            path_way.append((x, y))
        k -= 1
    return path_way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    if (
        coord == (0, 0)
        or coord == (len(grid) - 1, len(grid[0]) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (0, len(grid[0]) - 1)
    ):
        return True
    elif coord[0] == 0:
        if grid[1][coord[1]] != " ":
            return True
    elif coord[0] == len(grid) - 1:
        if grid[len(grid) - 2][coord[1]] != " ":
            return True
    elif coord[1] == 0:
        if grid[coord[0]][1] != " ":
            return True
    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][len(grid[0]) - 2] != " ":
            return True
    return False


def solve_maze(grid: List[List[Union[str, int]]]) -> Optional[List[Tuple[int, int]]]:
    exits = get_exits(grid)
    if len(exits) == 1:
        return None

    for i in exits:
        if encircled_exit(grid, i):
            return None
    beginning = exits[0]
    ending = exits[1]
    grid[beginning[0]][beginning[1]] = 1
    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == " ":
                grid[row][col] = 0

    grid[ending[0]][ending[1]] = 0

    k = 1

    if beginning[0] != 0:
        if grid[beginning[0] - 1][beginning[1]] == 0:
            grid[beginning[0] - 1][beginning[1]] = k + 1
    if beginning[0] != len(grid) - 1:
        if grid[beginning[0] + 1][beginning[1]] == 0:
            grid[beginning[0] + 1][beginning[1]] = k + 1
    if beginning[1] != 0:
        if grid[beginning[0]][beginning[1] - 1] == 0:
            grid[beginning[0]][beginning[1] - 1] = k + 1
    if beginning[1] != len(grid[0]) - 1:
        if grid[beginning[0]][beginning[1] + 1] == 0:
            grid[beginning[0]][beginning[1] + 1] = k + 1
    while grid[ending[0]][ending[1]] == 0:
        k += 1
        make_step(grid, k)
    return shortest_path(grid, ending)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
