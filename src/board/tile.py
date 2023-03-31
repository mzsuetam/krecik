from enum import Enum


class TileType(Enum):
    GRASS = 0
    ROCKS = 1
    MOUND = 2
    TOMATO = 3
    MUSHROOM = 4


class Terrain(Enum):
    GRASS = 0
    ROCKS = 1
    MOUND = 2


class Gatherable(Enum):
    TOMATO = 0
    MUSHROOM = 1


class Tile:

    VALUE_TO_TERRAIN_AND_GATHERABLE_MAP = {
        TileType.GRASS: (Terrain.GRASS, None),
        TileType.ROCKS: (Terrain.ROCKS, None),
        TileType.MOUND: (Terrain.MOUND, None),
        TileType.TOMATO: (Terrain.GRASS, Gatherable.TOMATO),
        TileType.MUSHROOM: (Terrain.GRASS, Gatherable.MUSHROOM),
    }

    def __init__(self, tile_type: TileType) -> None:
        self.terrain, self.gatherable = Tile.VALUE_TO_TERRAIN_AND_GATHERABLE_MAP.get(
            tile_type,
            (Terrain.GRASS, None),
        )

    def pick(self) -> Gatherable:
        gatherable = self.gatherable
        self.gatherable = None
        return gatherable

    def can_step_on(self) -> bool:
        return self.terrain != Terrain.ROCKS

    def is_grass(self) -> bool:
        return self.terrain == Terrain.GRASS

    def is_rocks(self) -> bool:
        return self.terrain == Terrain.ROCKS

    def is_mound(self) -> bool:
        return self.terrain == Terrain.MOUND

    def is_tomato(self) -> bool:
        return self.gatherable == Gatherable.TOMATO

    def is_mushroom(self) -> bool:
        return self.gatherable == Gatherable.MUSHROOM

    def __repr__(self) -> str:
        return f"<Tile: {self.terrain}, {self.gatherable}>"
