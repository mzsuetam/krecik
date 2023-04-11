from enum import Enum, auto


class TileType(Enum):
    GRASS = "_"
    ROCKS = "X"
    MOUND = "O"
    TOMATO = "T"
    MUSHROOM = "M"


class Terrain(Enum):
    GRASS = auto()
    ROCKS = auto()
    MOUND = auto()


class Gatherable(Enum):
    TOMATO = auto()
    MUSHROOM = auto()
