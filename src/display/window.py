from pathlib import Path
from tkinter import Tk, Label
from tkinter.constants import W

from PIL import ImageTk, Image
import sys

from PIL.ImageTk import PhotoImage

from board.board import Board
from board.krecik import Rotation
from board.enums import Gatherable, Terrain
from display.base_display import BaseDisplay


class Window(BaseDisplay):
    ROTATION_TO_IMAGE_NAME_MAP = {
        Rotation.N: "krecik_idle_N",
        Rotation.E: "krecik_idle_E",
        Rotation.S: "krecik_idle_S",
        Rotation.W: "krecik_idle_W",
    }

    TERRAIN_TO_IMAGE_NAME_MAP = {
        Terrain.GRASS: "dirt",
        Terrain.ROCKS: "rock",
        Terrain.MOUND: "mound",
    }

    GATHERABLE_TO_IMAGE_NAME_MAP = {
        Gatherable.TOMATO: "tomato",
        Gatherable.MUSHROOM: "mushroom",
    }

    MIN_FIELD_SIZE = 100  # in px
    MAX_FIELD_SIZE = 1000  # in px

    def __init__(self, board: Board) -> None:
        super().__init__(board)
        largest_dimension = max(board.width, board.height)
        self._field_size = (
            Window.MIN_FIELD_SIZE
            if largest_dimension * Window.MIN_FIELD_SIZE < Window.MAX_FIELD_SIZE
            else Window.MAX_FIELD_SIZE // largest_dimension
        )

        self._root = self._init_root()
        self._images = self._init_images()
        self._tiles = self._init_tiles()
        self._cmd_label = self._init_cmd_label()

        # @FIXME: implement object loading

        self._krecik_label = Label(self._root, image="", bd=0, bg="black")
        self.update_krecik_position()
        self.update_krecik_rotation()
        # # l4.grid_forget() # usuwanie

        # self.__root.mainloop()
        # self.__root.update_idletasks()
        self._root.update()
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _init_images(self) -> dict[str, PhotoImage]:
        current_parent_path = Path(__file__).parent.resolve()
        return {
            "dirt": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "dirtv2.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "rock": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "kamykv3.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "mound": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "kopiecv3.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "tomato": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "pomidorv3.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "mushroom": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "muchomorv3.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "krecik_idle_W": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecikv3_W.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "krecik_idle_N": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecikv3_N.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "krecik_idle_E": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecikv3_E.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
            "krecik_idle_S": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecikv3_S.png").resize(
                    (self._field_size, self._field_size), Image.ANTIALIAS
                )
            ),
        }

    @staticmethod
    def _init_root() -> Tk:
        root = Tk()
        root.title("Krecik")
        # self.__root.geometry("1200x800")
        root.resizable(width=False, height=False)
        return root

    def _init_tiles(self) -> list[list[Label]]:
        tiles_matrix = []
        for row_index, row in enumerate(self.board.matrix):
            tiles_row = []
            for col_index, tile in enumerate(row):
                terrain_image_name = Window.TERRAIN_TO_IMAGE_NAME_MAP[tile.terrain]
                terrain_image = self._images[terrain_image_name]
                label = Label(self._root, image=terrain_image, bd=0)
                label.grid(row=row_index, column=col_index, sticky=W)
                tiles_row.append(label)
            tiles_matrix.append(tiles_row)
        return tiles_matrix

    def _init_cmd_label(self) -> Label:
        cmd_label = Label(self._root, text="Starting...", font="none 12 bold")
        cmd_label.grid(
            row=self.board.height + 1,
            column=0,
            columnspan=self.board.width,
            sticky=W,
        )
        return cmd_label

    def _on_closing(self) -> None:
        # @FIXME: closing window by x button generates exception
        self._root.destroy()
        sys.exit()

    def update_krecik_position(self) -> None:
        pos = self.board.krecik.position
        self._krecik_label.grid(
            row=pos.row,
            column=pos.col,
            sticky=W,
        )
        command_label_text = f"krecik moves to {pos}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_krecik_rotation(self) -> None:
        rot = self.board.krecik.rotation
        image_name = Window.ROTATION_TO_IMAGE_NAME_MAP.get(rot)
        if image_name is None:
            raise NotImplementedError()
        image = self._images.get(image_name)
        if image is None:
            raise NotImplementedError()
        self._krecik_label.config(image=image)
        command_label_text = f"krecik face {rot}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_make_mound(self) -> None:
        pos = self.board.krecik.position
        mound_image = self._images["mound"]
        label: Label = self._tiles[pos.row][pos.col]
        label.configure(image=mound_image)
        command_label_text = f"krecik makes mound at {self.board.krecik.position}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_remove_mound(self) -> None:
        pos = self.board.krecik.position
        dirt_image = self._images["dirt"]
        label: Label = self._tiles[pos.row][pos.col]
        label.configure(image=dirt_image)
        command_label_text = f"krecik removes mound at {self.board.krecik.position}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_hide(self) -> None:
        mound_image = self._images["mound"]
        self._krecik_label.config(image=mound_image)
        command_label_text = f"krecik hides in mound at {self.board.krecik.position}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_get_out(self) -> None:
        rot = self.board.krecik.rotation
        image_name = Window.ROTATION_TO_IMAGE_NAME_MAP.get(rot)
        if image_name is None:
            raise NotImplementedError()
        image = self._images.get(image_name)
        if image is None:
            raise NotImplementedError()
        self._krecik_label.config(image=image)
        command_label_text = f"krecik gets out from mound at {self.board.krecik.position}"
        self.update_command_label_text(command_label_text)
        self.update()

    def update_command_label_text(self, command_label_text: str) -> None:
        self._cmd_label.config(text=command_label_text)

    def update(self) -> None:
        self._root.update()
