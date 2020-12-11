# https://adventofcode.com/2020/day/11

import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'


DIRECTION_TO_OFFSET = {
    'N': (-1, 0),
    'NE': (-1, 1),
    'E': (0, 1),
    'SE': (1, 1),
    'S': (1, 0),
    'SW': (1, -1),
    'W': (0, -1),
    'NW': (-1, -1),
}


def read_seats(path: Path) -> List[str]:
    with open(path) as seating_file:
        return [line.rstrip() for line in seating_file]


def count_adjacent_occupied_seats(seating, row, column):
    height = len(seating)
    width = len(seating[0])
    return sum(
        seating[i][j] == OCCUPIED
        for i in range(max(row - 1, 0), min(row + 2, height))
        for j in range(max(column - 1, 0), min(column + 2, width))
        if (i, j) != (row, column)
    )


def generate_coordinates(start, direction: str, width, height):
    i, j = start
    delta_i, delta_j = DIRECTION_TO_OFFSET[direction]
    while True:
        i += delta_i
        j += delta_j
        if i < 0 or i >= height or j < 0 or j >= width:
            return
        yield i, j


def is_occupied_in_direction(seating, start, direction, width, height):
    for i, j in generate_coordinates(start, direction, width, height):
        if seating[i][j] == OCCUPIED:
            return True
        if seating[i][j] == EMPTY:
            return False
    return False


def count_far_occupied_seats(seating, row, column):
    height = len(seating)
    width = len(seating[0])
    return sum(
        is_occupied_in_direction(seating, (row, column), direction, width, height)
        for direction in DIRECTION_TO_OFFSET
    )


def next_generation(seating, count_occupied_around, max_occupied_around):
    changed = 0
    new_seating = []
    for i, row in enumerate(seating):
        new_seating.append([])
        for j, tile in enumerate(row):
            new_tile = tile
            occupied_around = count_occupied_around(seating, i, j)
            if tile == EMPTY and occupied_around == 0:
                new_tile = OCCUPIED
                changed += 1
            elif tile == OCCUPIED and occupied_around >= max_occupied_around:
                new_tile = EMPTY
                changed += 1
            new_seating[-1].append(new_tile)
    return new_seating, changed


def stable_occupied_count(dataset, count_occupied_around, max_occupied_around):
    seats = read_seats(dataset)
    while True:
        seats, changed = next_generation(seats, count_occupied_around, max_occupied_around)
        if changed == 0:
            break
    return sum(
        seat == OCCUPIED
        for row in seats
        for seat in row
    )


def part1(dataset: Path):
    print(stable_occupied_count(dataset, count_adjacent_occupied_seats, max_occupied_around=4))


def part2(dataset: Path):
    print(stable_occupied_count(dataset, count_far_occupied_seats, max_occupied_around=5))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
