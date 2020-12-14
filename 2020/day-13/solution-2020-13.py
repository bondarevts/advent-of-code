# https://adventofcode.com/2020/day/13
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_buses_schedule(path: Path):
    with open(path) as dataset:
        depart_time, raw_buses = dataset
    return int(depart_time), [int(bus) for bus in raw_buses.split(',') if bus.isnumeric()]


def part1(dataset: Path):
    depart_time, buses = read_buses_schedule(dataset)
    wait_time, bus_id = min((-depart_time % bus_id, bus_id) for bus_id in buses)
    print(wait_time * bus_id)


def read_buses_order(path: Path):
    with open(path) as dataset:
        _, raw_buses = dataset
    return [(int(bus), offset) for offset, bus in enumerate(raw_buses.split(',')) if bus != 'x']


def extended_gcd(a, b):
    """ returns gcd(a, b), x, y, where x * a + y * b == gcd(a, b) """
    if a == 0:
        return b, 0, 1

    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def get_multipliers(max_value, bus_id):
    multiplier = max_value // bus_id
    gcd, inverse, _ = extended_gcd(multiplier, bus_id)
    assert gcd == 1
    assert multiplier * inverse % bus_id == 1
    return multiplier, inverse


def part2(dataset: Path):
    buses_info = read_buses_order(dataset)
    max_value = math.prod(bus_id for bus_id, _ in buses_info)
    multipliers = [get_multipliers(max_value, bus_id) for bus_id, _ in buses_info]
    print(sum(
        (-bus_offset % bus_id) * m * m_inv
        for (bus_id, bus_offset), (m, m_inv) in zip(buses_info, multipliers)
    ) % max_value)  # Chinese remainder theorem


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
