from board.enums import Gatherable


class InventoryMixin:
    def __init__(self, inventory_limit: int | None = 1) -> None:
        """inventory_limit = None means no limit"""
        self.inventory: list[Gatherable] = []
        self.inventory_limit = inventory_limit

    def append_gatherable(self, gatherable: Gatherable) -> bool:
        if self.can_append_gatherable():
            self.inventory.append(gatherable)
            return True
        return False

    def can_append_gatherable(self) -> bool:
        if self.inventory_limit is None:
            return True
        return len(self.inventory) < self.inventory_limit

    def pop_gatherable(self) -> Gatherable | None:
        if self.inventory:
            return self.inventory.pop()
        return None

    def has_gatherable(self, gatherable: Gatherable) -> bool:
        return gatherable in self.inventory

    def transfer_to(self, obj_with_inventory: "InventoryMixin") -> bool:
        if obj_with_inventory.can_append_gatherable():
            if gatherable := self.pop_gatherable():
                obj_with_inventory.inventory.append(gatherable)
                return True
        return False
