from pathlib import Path
from tkinter import Tk, Label
from tkinter.constants import W
import time
from PIL import ImageTk, Image
import sys

from board.board import Board
from board.krecik import Krecik, Rotation
from board.tile import Gatherable, Terrain


class Window:

    ROTATION_TO_IMAGE_NAME_MAP = {
        Rotation.N: "krecik_idle_N",
        Rotation.E: "krecik_idle_E",
        Rotation.S: "krecik_idle_S",
        Rotation.W: "krecik_idle_W",
    }

    TERRAIN_TO_IMAGE_NAME_MAP = {
        Terrain.GRASS: "dirt",
        Terrain.ROCKS: "dirt",
        Terrain.MOUND: "dirt",
    }

    GATHERABLE_TO_IMAGE_NAME_MAP = {
        Gatherable.TOMATO: "",
        Gatherable.MUSHROOM: "",
    }

    MIN_FIELD_SIZE = 100  # in px
    MAX_FIELD_SIZE = 1000  # in px

    def __init__(self, board: Board, wait_time: float = 0.5) -> None:
        self._wait_time = wait_time  # wait time [s]
        largest_dimension = max(board.width, board.height)
        self._field_size = (
            Window.MIN_FIELD_SIZE
            if largest_dimension * Window.MIN_FIELD_SIZE < Window.MAX_FIELD_SIZE
            else Window.MAX_FIELD_SIZE // largest_dimension
        )

        self._root = self._init_root()
        self._images = self._init_images()
        self._tiles = self._init_tiles(board)
        self._cmd_label = self._init_cmd_label(board)

        # @FIXME: implement object loading

        self._krecik_label = Label(self._root, image="", bd=0, bg='black')
        self.update_krecik_position(board.krecik)
        self.update_krecik_rotation(board.krecik)
        # # l4.grid_forget() # usuwanie

        # self.__root.mainloop()
        # self.__root.update_idletasks()
        self._root.update()
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _init_images(self) -> dict[str, ImageTk]:
        current_parent_path = Path(__file__).parent.resolve()
        return {
            "dirt": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "dirt.png").resize(
                    (self._field_size, self._field_size),
                    Image.ANTIALIAS
                )
            ),
            "krecik_idle_W": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecik_W.png").resize(
                    (self._field_size, self._field_size),
                    Image.ANTIALIAS
                )
            ),
            "krecik_idle_N": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecik_N.png").resize(
                    (self._field_size, self._field_size),
                    Image.ANTIALIAS
                )
            ),
            "krecik_idle_E": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecik_E.png").resize(
                    (self._field_size, self._field_size),
                    Image.ANTIALIAS
                )
            ),
            "krecik_idle_S": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "krecik_S.png").resize(
                    (self._field_size, self._field_size),
                    Image.ANTIALIAS
                )
            )
        }

    @staticmethod
    def _init_root() -> Tk:
        root = Tk()
        root.title("Krecik")
        # self.__root.geometry("1200x800")
        root.resizable(width=False, height=False)
        return root

    def _init_tiles(self, board: Board) -> list[list[Label]]:
        tiles_matrix = []
        for row_index, row in enumerate(board.matrix):
            tiles_row = []
            for col_index, tile in enumerate(row):
                terrain_image_name = Window.TERRAIN_TO_IMAGE_NAME_MAP[tile.terrain]
                terrain_image = self._images[terrain_image_name]
                label = Label(self._root, image=terrain_image, bd=0)
                label.grid(row=row_index, column=col_index, sticky=W)
                tiles_row.append(label)
            tiles_matrix.append(tiles_row)
        return tiles_matrix

    def _init_cmd_label(self, board) -> Label:
        cmd_label = Label(self._root, text="Starting...", font="none 12 bold")
        cmd_label.grid(
            row=board.height + 1,
            column=0,
            columnspan=board.width,
            sticky=W,
        )
        return cmd_label

    def _on_closing(self) -> None:
        # @FIXME: closing window by x button generates exception
        self._root.destroy()
        sys.exit()

    def refresh(self) -> None:
        time.sleep(self._wait_time)
        self._root.update()

    def update_krecik_position(self, krecik: Krecik) -> None:
        self._krecik_label.grid(
            row=krecik.position.row,
            column=krecik.position.col,
            sticky=W,
        )
        command_label_text = f"Krecik moves to {krecik.position.row}, {krecik.position.col}"
        self.update_command_label_text(krecik, command_label_text)

    def update_krecik_rotation(self, krecik: Krecik) -> None:
        image_name = Window.ROTATION_TO_IMAGE_NAME_MAP.get(krecik.rotation)
        image = self._images.get(image_name)
        self._krecik_label.config(image=image)
        command_label_text = f"Krecik rotate to face {krecik.rotation.name}"
        self.update_command_label_text(krecik, command_label_text)

    def update_command_label_text(self, krecik: Krecik, command_label_text: str) -> None:
        new_text = (
            f"Position: ({krecik.position.row}, {krecik.position.col}), "
            f"Rotation: {krecik.rotation.name}, "
            f"{command_label_text}"
        )
        self._cmd_label.config(text=new_text)
