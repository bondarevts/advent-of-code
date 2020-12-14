# https://adventofcode.com/2020/day/14
import re
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_program(path: Path):
    memory_set_pattern = re.compile(r'mem\[(\d+)] = (\d+)')
    with open(path) as program_file:
        for line in program_file:
            if line.startswith('mask'):
                yield 'mask', line[7:-1]  # remove "mask = " and "\n"
            else:
                address, value = memory_set_pattern.match(line).groups()
                yield 'mem', int(address), int(value)


def apply_mask(value, mask):
    return (value | int(mask.replace('X', '0'), base=2)) & int(mask.replace('X', '1'), base=2)


def mask_updates_value(data, mask, address, value):
    assert mask is not None
    data[address] = apply_mask(value, mask)


def run_program(dataset, update_data):
    data = {}
    mask = None
    for command, *args in read_program(dataset):
        if command == 'mask':
            mask = args[0]
        else:
            address, value = args
            update_data(data, mask, address, value)
    print(sum(data.values()))


def generate_addresses(address, mask):
    address_mask = [
        address_bit if mask_bit == '0' else mask_bit
        for address_bit, mask_bit in zip(f'{address:036b}', mask)
    ]
    floating_positions = [i for i, value in enumerate(address_mask) if value == 'X']
    for values in product('01', repeat=len(floating_positions)):
        for i, value in zip(floating_positions, values):
            address_mask[i] = value
        yield int(''.join(address_mask), base=2)


def mask_updates_address(data, mask, initial_address, value):
    assert mask is not None
    for address in generate_addresses(initial_address, mask):
        data[address] = value


def part1(dataset: Path):
    run_program(dataset, mask_updates_value)


def part2(dataset: Path):
    run_program(dataset, mask_updates_address)


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
