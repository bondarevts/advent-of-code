# https://adventofcode.com/{{ year }}/day/{{ day }}

import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_numbers(path: Path):
    return [int(v) for v in path.read_text().strip().split(',')]


def get_sequence_at(start_sequence, position):
    last_positions = {v: i for i, v in enumerate(start_sequence[:-1])}
    last_value = start_sequence[-1]
    for i in range(len(start_sequence), position):
        if last_value not in last_positions:
            new_last_value = 0
        else:
            new_last_value = i - last_positions[last_value] - 1
        last_positions[last_value] = i - 1
        last_value = new_last_value
    return last_value


def part1(dataset: Path):
    print(get_sequence_at(read_numbers(dataset), 2020))


def part2(dataset: Path):
    print(get_sequence_at(read_numbers(dataset), 30_000_000))


def test():
    assert get_sequence_at([0, 3, 6], 2020) == 436
    assert get_sequence_at([1, 3, 2], 2020) == 1
    assert get_sequence_at([2, 1, 3], 2020) == 10
    assert get_sequence_at([1, 2, 3], 2020) == 27
    assert get_sequence_at([2, 3, 1], 2020) == 78
    assert get_sequence_at([3, 2, 1], 2020) == 438
    assert get_sequence_at([3, 1, 2], 2020) == 1836

    assert get_sequence_at([0, 3, 6], 30_000_000) == 175594
    assert get_sequence_at([1, 3, 2], 30_000_000) == 2578
    assert get_sequence_at([2, 1, 3], 30_000_000) == 3544142
    assert get_sequence_at([1, 2, 3], 30_000_000) == 261214
    assert get_sequence_at([2, 3, 1], 30_000_000) == 6895259
    assert get_sequence_at([3, 2, 1], 30_000_000) == 18
    assert get_sequence_at([3, 1, 2], 30_000_000) == 362


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        test()


if __name__ == '__main__':
    main()
