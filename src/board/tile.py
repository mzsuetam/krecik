from board.enums import Gatherable, Terrain, TileType
from board.inventory_mixin import InventoryMixin


class Tile(InventoryMixin):
    BLOCKING_TERRAIN = {Terrain.ROCKS}

    VALUE_TO_TERRAIN_AND_GATHERABLE_MAP = {
        TileType.GRASS: (Terrain.GRASS, None),
        TileType.ROCKS: (Terrain.ROCKS, None),
        TileType.MOUND: (Terrain.MOUND, None),
        TileType.TOMATO: (Terrain.GRASS, Gatherable.TOMATO),
        TileType.MUSHROOM: (Terrain.GRASS, Gatherable.MUSHROOM),
    }

    def __init__(self, tile_type: TileType) -> None:
        terrain, gatherable = Tile.VALUE_TO_TERRAIN_AND_GATHERABLE_MAP.get(
            tile_type,
            (Terrain.GRASS, None),
        )
        self.terrain: Terrain = terrain
        super().__init__()
        if gatherable is not None:
            self.append_gatherable(gatherable)

    def can_step_on(self) -> bool:
        return self.terrain not in self.BLOCKING_TERRAIN

    def is_terrain(self, terrain: Terrain) -> bool:
        return self.terrain == terrain

    def change_terrain(self, terrain: Terrain) -> None:
        self.terrain = terrain

    def __repr__(self) -> str:
        return f"<Tile: {self.terrain}, {self.inventory}>"
