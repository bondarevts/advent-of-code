# https://adventofcode.com/2020/day/12
import math
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


@dataclass
class Coordinate:
    north: int
    east: int


def read_instructions(path: Path):
    with open(path) as instructions:
        for line in instructions:
            code, amount = line[0], int(line[1:])
            if code == 'R' or code == 'L':
                assert amount % 90 == 0
            yield code, amount


def part1(dataset: Path):
    ship = Coordinate(0, 0)
    direction = 0
    for code, amount in read_instructions(dataset):
        if code == 'N':
            ship.north += amount
        elif code == 'S':
            ship.north -= amount
        elif code == 'E':
            ship.east += amount
        elif code == 'W':
            ship.east -= amount
        elif code == 'F':
            ship.north += int(math.sin(math.radians(direction))) * amount
            ship.east += int(math.cos(math.radians(direction))) * amount
        elif code == 'R':
            direction -= amount
        elif code == 'L':
            direction += amount
        else:
            raise Exception()
    print(abs(ship.north) + abs(ship.east))


def part2(dataset: Path):
    ship = Coordinate(0, 0)
    waypoint = Coordinate(east=10, north=1)
    for code, amount in read_instructions(dataset):
        if code == 'N':
            waypoint.north += amount
        elif code == 'S':
            waypoint.north -= amount
        elif code == 'E':
            waypoint.east += amount
        elif code == 'W':
            waypoint.east -= amount
        elif code == 'F':
            ship.north += waypoint.north * amount
            ship.east += waypoint.east * amount
        elif code == 'R' or code == 'L':
            sign = -1 if code == 'R' else 1
            cos = int(math.cos(math.radians(sign * amount)))
            sin = int(math.sin(math.radians(sign * amount)))
            print(sin, cos)
            waypoint = Coordinate(
                north=cos * waypoint.north + sin * waypoint.east,
                east=-sin * waypoint.north + cos * waypoint.east
            )
        else:
            raise Exception()
        print(code, amount, ship, waypoint)
    print(abs(ship.north) + abs(ship.east))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
