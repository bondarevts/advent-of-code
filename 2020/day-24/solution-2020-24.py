# https://adventofcode.com/{{ year }}/day/{{ day }}
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_directions(path: Path):
    direction_pattern = re.compile(r'(w|nw|ne|e|se|sw)')
    for line in path.read_text().splitlines():
        position = 0
        directions = []
        while match := direction_pattern.match(line, position):
            directions.append(match.group())
            position = match.span()[1]
        yield directions


def apply_move(coordinate, move):
    x, y = coordinate
    if move == 'w':
        x -= 1
    elif move == 'nw':
        y += 1
    elif move == 'ne':
        x += 1
        y += 1
    elif move == 'e':
        x += 1
    elif move == 'se':
        y -= 1
    else:
        assert move == 'sw'
        x -= 1
        y -= 1
    return x, y


def black_tiles_positions(dataset):
    black_tiles = set()
    for moves in read_directions(dataset):
        coordinate = (0, 0)
        for move in moves:
            coordinate = apply_move(coordinate, move)
        if coordinate in black_tiles:
            black_tiles.remove(coordinate)
        else:
            black_tiles.add(coordinate)
    return black_tiles


def part1(dataset: Path):
    print(len(black_tiles_positions(dataset)))


def neighbors(coordinate):
    x, y = coordinate
    return [
        (x - 1, y),
        (x, y + 1),
        (x + 1, y + 1),
        (x + 1, y),
        (x, y - 1),
        (x - 1, y - 1),
    ]


def black_neighbors_number(black_tiles, coordinate):
    return sum(
        neighbor in black_tiles
        for neighbor in neighbors(coordinate)
    )


def part2(dataset: Path):
    tiles = black_tiles_positions(dataset)
    for _ in range(100):
        to_visit = tiles | {
            coordinate
            for tile in tiles
            for coordinate in neighbors(tile)
        }
        new_tiles = set()
        for coordinate in to_visit:
            black_around = black_neighbors_number(tiles, coordinate)
            if coordinate in tiles and (0 < black_around <= 2):
                new_tiles.add(coordinate)
            elif coordinate not in tiles and black_around == 2:
                new_tiles.add(coordinate)
        tiles = new_tiles
    print(len(tiles))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
