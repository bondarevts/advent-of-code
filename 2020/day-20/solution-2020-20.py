# https://adventofcode.com/2020/day/20
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from operator import attrgetter
from pathlib import Path
from typing import Generic
from typing import TypeVar

import numpy as np
import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'

TILES_NUMBER = 144
TILE_SIZE = 10

T = TypeVar("T")


MONSTER = '''\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''


def monster_mask():
    return np.asarray([
        list(map(int, line.replace('#', '1').replace(' ', '0')))
        for line in MONSTER.splitlines()
    ], dtype=int)


@dataclass
class Sides(Generic[T]):
    top: T
    right: T
    bottom: T
    left: T

    @property
    def all(self):
        return self.top, self.right, self.bottom, self.left


class Tile:
    def __init__(self, tile_id, values):
        self.id = tile_id
        self.tile = values
        self.sides = Sides(
            *map(to_number, Sides(
                top=self.tile[0, :],
                right=self.tile[:, -1],
                bottom=self.tile[-1, ::-1],
                left=self.tile[::-1, 0],
            ).all)
        )

    def flip(self):
        new_id = self.id[:-1] if self.id.endswith('r') else self.id + 'r'
        return Tile(new_id, np.fliplr(self.tile))

    def rotate(self):
        return Tile(self.id, np.rot90(self.tile))

    def __repr__(self):
        return self.id


def read_tile(lines):
    header = next(lines)
    assert header.startswith('Tile')
    tile_id = header[5:-1]
    tile = [list(map(int, next(lines).replace('#', '1').replace('.', '0'))) for _ in range(TILE_SIZE)]
    next(lines)
    return Tile(tile_id, np.asarray(tile, dtype=int))


def read_tiles(path: Path, number):
    lines = iter(path.read_text().splitlines())
    tiles = {}
    for _ in range(number):
        tile = read_tile(lines)
        tiles[tile.id] = tile
    return tiles


def to_number(array):
    return (array * 2 ** np.arange(array.size)[::-1]).sum()


def build_border_to_tiles(tiles):
    d = defaultdict(list)
    for tile in tiles.values():
        for border in tile.sides.all:
            d[border].append(tile)
        flipped = tile.flip()
        for border in flipped.sides.all:
            d[border].append(flipped)
    return d


def corner_tiles(graph):
    return (
        v
        for v, edges in graph.items()
        if len(edges) == 2 and not v.endswith('r')
    )


def make_graph(tiles):
    inner_edges = defaultdict(list)
    for tile in tiles.values():
        for side in tile.sides.all:
            inner_edges[side].append(tile)
        flipped = tile.flip()
        for side in flipped.sides.all:
            inner_edges[side].append(flipped)

    graph = defaultdict(dict)
    for edge, related_tiles in inner_edges.items():
        if len(related_tiles) != 2:
            continue
        tile1, tile2 = related_tiles
        graph[tile1.flip().id][reverse_side(edge)] = tile2
        graph[tile2.flip().id][reverse_side(edge)] = tile1
    return graph


def find_corner_tile(graph, tiles):
    corner_id = next(corner_tiles(graph))
    tile = tiles[corner_id]
    for _ in range(4):
        if tile.sides.top not in graph[tile.id] and tile.sides.left not in graph[tile.id]:
            return tile
        tile = tile.rotate()
    assert False


def part1(dataset: Path):
    tiles = read_tiles(dataset, TILES_NUMBER)
    graph = make_graph(tiles)
    print(math.prod(map(int, corner_tiles(graph))))


def rotate_for_top(tile, top):
    return rotate_for(tile, attrgetter('top'), top)


def rotate_for_left(tile, left):
    return rotate_for(tile, attrgetter('left'), left)


def rotate_for(tile, getter, value):
    total_rotations = 0
    while getter(tile.sides) != value and total_rotations < 4:
        total_rotations += 1
        tile = tile.rotate()
    return tile if total_rotations <= 3 else None


def reverse_side(value: int) -> int:
    return int(f'{value:0{TILE_SIZE}b}'[::-1], base=2)


def build_tile_matrix(graph, tiles, side):
    corner = find_corner_tile(graph, tiles)
    tile_matrix = [[None] * side for _ in range(side)]
    tile_matrix[0][0] = corner
    for i in range(side):
        if i != 0:
            top_tile = tile_matrix[i - 1][0]
            edge = reverse_side(top_tile.sides.bottom)
            bottom_tile = rotate_for_top(graph[top_tile.id][top_tile.sides.bottom], edge)
            tile_matrix[i][0] = bottom_tile
        for j in range(1, side):
            left_tile = tile_matrix[i][j - 1]
            edge = reverse_side(left_tile.sides.right)
            right_tile = rotate_for_left(graph[left_tile.id][left_tile.sides.right], edge)
            tile_matrix[i][j] = right_tile
    return tile_matrix


def make_picture(graph, tiles):
    side = int(math.sqrt(len(graph) // 2))
    tile_matrix = build_tile_matrix(graph, tiles, side)
    inner_tile_size = TILE_SIZE - 2  # no borders
    full_image = np.zeros((side * (TILE_SIZE - 2),) * 2, dtype=int)
    for i, row in enumerate(tile_matrix):
        image_i = inner_tile_size * i
        for j, tile in enumerate(row):
            image_j = inner_tile_size * j
            if i != 0:
                assert np.array_equal(tile.tile[0, :], tile_matrix[i-1][j].tile[-1, :])
            if j != 0:
                assert np.array_equal(tile.tile[:, 0], tile_matrix[i][j - 1].tile[:, -1])
            full_image[image_i:image_i + inner_tile_size, image_j: image_j + inner_tile_size] = tile.tile[1:-1, 1:-1]
    return full_image


def find_monsters(picture):
    mask = monster_mask()
    mask_threshold = mask.sum()
    mask_height, mask_width = mask.shape
    pic_height, pic_width = picture.shape
    positions = []
    for _ in range(4):
        for i, j in product(range(pic_height - mask_height + 1), range(pic_width - mask_width + 1)):
            pic_tile = picture[i:i+mask_height, j:j+mask_width]
            assert pic_tile.shape == mask.shape
            if (pic_tile * mask).sum() == mask_threshold:
                positions.append((i, j))
        if positions:
            return positions
        picture = np.rot90(picture)
    return []


def part2(dataset: Path):
    tiles = read_tiles(dataset, TILES_NUMBER)
    graph = make_graph(tiles)
    picture = make_picture(graph, tiles)
    positions = find_monsters(picture)
    if not positions:
        positions = find_monsters(np.fliplr(picture))
    print(picture.sum() - len(positions) * monster_mask().sum())


def test_corners():
    assert {'1951', '3079', '2971', '1171'} == set(corner_tiles(make_graph(read_tiles(ROOT / 'test-dataset-1.txt', 9))))


def test_graph():
    tiles = read_tiles(ROOT / 'test-dataset-1.txt', 9)
    graph = make_graph(tiles)
    build_tile_matrix(graph, tiles, 3)


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
