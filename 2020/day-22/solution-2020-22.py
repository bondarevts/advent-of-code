# https://adventofcode.com/{{ year }}/day/{{ day }}

import sys
from collections import deque
from itertools import islice
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_player(lines):
    player = deque()
    next(lines)
    for line in lines:
        if not line:
            break
        player.append(int(line))
    return player


def read_decks(path: Path):
    lines = iter(path.read_text().splitlines())
    return read_player(lines), read_player(lines)


def get_winning_deck(p1, p2):
    while p1 and p2:
        v1 = p1.popleft()
        v2 = p2.popleft()
        if v1 > v2:
            p1.extend((v1, v2))
        else:
            p2.extend((v2, v1))
    return p1 if p1 else p2


def deck_score(deck):
    return sum(value * score for score, value in enumerate(reversed(deck), start=1))


def part1(dataset: Path):
    p1, p2 = read_decks(dataset)
    winner = get_winning_deck(p1, p2)
    print(deck_score(winner))


def test_winning_deck():
    p1 = deque([9, 2, 6, 3, 1])
    p2 = deque([5, 8, 4, 7, 10])
    expected_final_deck = [3, 2, 10, 6, 8, 5, 9, 4, 7, 1]
    final_deck = get_winning_deck(p1, p2)
    assert list(final_deck) == expected_final_deck
    assert deck_score(final_deck) == 306


def get_winning_recursive_deck(p1, p2):
    played_combinations = set()
    while p1 and p2:
        combination = tuple(p1), tuple(p2)
        if combination in played_combinations:
            return 1, p1
        else:
            played_combinations.add(combination)
        v1 = p1.popleft()
        v2 = p2.popleft()
        if len(p1) >= v1 and len(p2) >= v2:
            winner, _ = get_winning_recursive_deck(
                deque(islice(p1, 0, v1)),
                deque(islice(p2, 0, v2))
            )
            if winner == 1:
                p1.extend((v1, v2))
            else:
                p2.extend((v2, v1))
        elif v1 > v2:
            p1.extend((v1, v2))
        else:
            p2.extend((v2, v1))
    return (1, p1) if p1 else (2, p2)


def part2(dataset: Path):
    p1, p2 = read_decks(dataset)
    _, deck = get_winning_recursive_deck(p1, p2)
    print(deck_score(deck))


def test_recursive_game():
    p1 = deque([9, 2, 6, 3, 1])
    p2 = deque([5, 8, 4, 7, 10])
    _, deck = get_winning_recursive_deck(p1, p2)
    assert deck_score(deck) == 291


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
