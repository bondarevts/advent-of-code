# https://adventofcode.com/2020/day/17
import itertools
import sys
from dataclasses import dataclass
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


@dataclass
class Offset:
    row: int
    column: int
    level: int


class Field4D:
    EMPTY = '.'
    OCCUPIED = '#'

    def __init__(self, initial_state):
        size = 30
        self.field = np.zeros((size, size, size, size), dtype=int)
        initial_height = len(initial_state)
        initial_width = len(initial_state[0])

        for i, row in enumerate(initial_state):
            for j, value in enumerate(row):
                self.field[
                    size//2,
                    size//2,
                    (size - initial_height) // 2 + i,
                    (size - initial_width) // 2 + j
                ] = value == Field4D.OCCUPIED

    def is_alive(self, w, z, y, x):
        neighbors = self.field[max(w-1, 0):w+2, max(z-1, 0):z+2, max(y-1, 0):y+2, max(x-1, 0):x+2].sum() - self.field[w, z, y, x]
        is_active = self.field[w, z, y, x]
        if is_active:
            return 2 <= neighbors <= 3
        return neighbors == 3

    def next_iteration(self):
        new_field = np.zeros_like(self.field)
        for coord in itertools.product(*map(range, self.field.shape)):
            if self.is_alive(*coord):
                new_field[coord] = 1
        self.field = new_field


class Field3D:
    EMPTY = '.'
    OCCUPIED = '#'

    def __init__(self, initial_state):
        size = 30
        self.field = np.zeros((size, size, size), dtype=int)
        initial_height = len(initial_state)
        initial_width = len(initial_state[0])

        for i, row in enumerate(initial_state):
            for j, value in enumerate(row):
                self.field[
                    size//2,
                    (size - initial_height) // 2 + i,
                    (size - initial_width) // 2 + j
                ] = value == Field3D.OCCUPIED

    def is_alive(self, z, y, x):
        neighbors = self.field[max(z-1, 0):z+2, max(y-1, 0):y+2, max(x-1, 0):x+2].sum() - self.field[z, y, x]
        is_active = self.field[z, y, x]
        if is_active:
            return 2 <= neighbors <= 3
        return neighbors == 3

    def next_iteration(self):
        new_field = np.zeros_like(self.field)
        for z, x, y in itertools.product(*map(range, self.field.shape)):
            if self.is_alive(z, x, y):
                new_field[z, x, y] = 1
        self.field = new_field


def read_initial_field(path: Path):
    return [list(line) for line in path.read_text().splitlines()]


def part1(dataset: Path):
    field = Field3D(read_initial_field(dataset))
    for _ in range(6):
        field.next_iteration()
    print(field.field.sum())


def part2(dataset: Path):
    field = Field4D(read_initial_field(dataset))
    for _ in range(6):
        field.next_iteration()
    print(field.field.sum())


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
