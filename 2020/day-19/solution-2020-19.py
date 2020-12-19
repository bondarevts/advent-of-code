# https://adventofcode.com/2020/day/19

import sys
from pathlib import Path
from typing import Optional

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


class Letter:
    def __init__(self, value):
        self.value = value

    def match(self, rules, string, start) -> Optional[int]:
        if start >= len(string):
            return None
        if string[start:start+1] == self.value:
            return start + 1
        return None


class Sequence:
    def __init__(self, rule_ids):
        self.rule_ids = rule_ids

    def match(self, rules, string, start) -> Optional[int]:
        position = start
        for rule_id in self.rule_ids:
            position = rules[rule_id].match(rules, string, position)
            if position is None:
                return None
        return position


class Choice:
    def __init__(self, choices):
        self.choices = choices

    def match(self, rules, string, start) -> Optional[int]:
        for choice in self.choices:
            position = choice.match(rules, string, start)
            if position is not None:
                return position
        return None


def test_letter():
    assert Letter('a').match({}, 'ab', start=0) == 1
    assert Letter('a').match({}, 'ab', start=1) is None


def test_sequence():
    rules = {
        '1': Letter('a'),
        '2': Letter('b'),
    }
    assert Sequence(list('12')).match(rules, 'abc', start=0) == 2
    assert Sequence(list('21')).match(rules, 'abc', start=0) is None


def parse_rule(description):
    if '"' in description:
        return Letter(description[1])
    if '|' in description:
        sub_rules = description.split(' | ')
        assert len(sub_rules) == 2
        first, second = sub_rules
        return Choice([Sequence(first.split()), Sequence(second.split())])
    return Sequence(description.split())


def parse_dataset(path: Path):
    lines = iter(path.read_text().splitlines())
    rules = {}
    for line in lines:
        if not line:
            break
        number, _, description = line.partition(': ')
        rules[number] = parse_rule(description)

    return rules, list(lines)


def part1(dataset: Path):
    rules, messages = parse_dataset(dataset)
    print(sum(
        rules['0'].match(rules, message, start=0) == len(message)
        for message in messages
    ))


def matches_rule_0(rules, string):
    # 0: 8 11
    # 8: 42+
    # 11: 42+ 31+  (same number)
    # 0: 42+ 31+ (#42 > #31)

    blocks = [string[i:i+8] for i in range(0, len(string), 8)]  # 8 is a size of match for #42 and #31

    matches42 = 0
    for block in blocks:
        if rules['42'].match(rules, block, 0) != len(block):
            break
        matches42 += 1

    matches31 = 0
    for block in reversed(blocks):
        if rules['31'].match(rules, block, 0) != len(block):
            break
        matches31 += 1
    return matches42 + matches31 >= len(blocks) and matches42 > matches31 > 0


def part2(dataset: Path):
    rules, messages = parse_dataset(dataset)
    rules.pop('8')
    rules.pop('11')
    print(sum(matches_rule_0(rules, message) for message in messages))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
