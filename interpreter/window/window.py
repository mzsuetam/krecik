from pathlib import Path
from tkinter import Tk, Label
from tkinter.constants import W
import time
from PIL import ImageTk, Image
import sys

from interpreter.board.board import Board
from interpreter.board.krecik import Position, Rotation


class Window:

    def __init__(self, board: Board, wait_time: float = 0.5) -> None:
        self._wait_time = wait_time  # wait time [s]

        min_field_size = 100  # in px
        max_field_size = 1000  # in px
        largest_dimension = max(board.width, board.height)
        self._field_size = (
            min_field_size
            if largest_dimension * min_field_size < max_field_size
            else max_field_size // largest_dimension
        )  # in px

        # ----------------------------- tkinter - window --------------------- #
        self._root = Tk()
        self._root.title("Krecik")
        # self.__root.geometry("1200x800")
        self._root.resizable(width=False, height=False)

        # ----------------------------- tkinter - images --------------------- #
        self._images = self._init_images()

        # ----------------------------- tkinter - fields --------------------- #
        for row_index, row in enumerate(board.matrix):
            for col_index, tile in enumerate(row):
                label = Label(self._root, image=self._images["dirt"], bd=0)
                label.grid(row=row_index, column=col_index, sticky=W)

        # ---------------------------- tkinter - log label ------------------- #
        self._cmd_label = Label(self._root, text="Starting...", font="none 12 bold")
        self._cmd_label.grid(
            row=board.height + 1,
            column=0,
            columnspan=board.width,
            sticky=W,
        )

        # ----------------------------- tkinter - objects -------------------- #
        # @FIXME: implement object loading

        # ------------------------ tkinter - objects - krecik ---------------- #
        self._krecik_label = Label(self._root, image="", bd=0, bg='black')
        self._command_label_text: str = ""
        self._krecik_position: Position | None = None
        self._krecik_rotation: Rotation | None = None
        self.update_krecik_position(board.krecik.position)
        self.update_krecik_rotation(board.krecik.rotation)
        # # l4.grid_forget() # usuwanie

        # -------------------------- tkinter - window cont. ------------------ #
        # self.__root.mainloop()
        # self.__root.update_idletasks()
        self._root.update()
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ------------------------------------------------------------------------ #
    #                              tkinter funny stuff                         #
    # ------------------------------------------------------------------------ #
    def _on_closing(self) -> None:
        # @FIXME: closing window by x button generates exception
        self._root.destroy()
        sys.exit()

    # ------------------------------------------------------------------------ #
    #                                    assets                                #
    # ------------------------------------------------------------------------ #
    def _init_images(self) -> dict[str, ImageTk]:
        current_parent_path = Path(__file__).parent.resolve()
        return {
            "dirt": ImageTk.PhotoImage(
                Image.open(current_parent_path / "assets" / "dirt.png")
                .resize(
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

    # ------------------------------------------------------------------------ #
    #                                    krecik                                #
    # ------------------------------------------------------------------------ #
    def refresh(self, board: Board) -> None:
        self.update_krecik_position(board.krecik.position)
        self.update_krecik_rotation(board.krecik.rotation)
        self.update_command_label_text()
        time.sleep(self._wait_time)
        self._root.update()

    def update_krecik_position(self, new_position: Position) -> None:
        if new_position == self._krecik_position:
            return
        self._krecik_position = new_position
        self._command_label_text = f"Krecik moves to {new_position.row}, {new_position.col}"
        self._krecik_label.grid(
            row=new_position.row,
            column=new_position.col,
            sticky=W,
        )

    def update_krecik_rotation(self, new_rotation: Rotation) -> None:
        if new_rotation == self._krecik_rotation:
            return
        self._krecik_rotation = new_rotation
        self._command_label_text = f"Krecik rotate to face {new_rotation.name}"
        if new_rotation == Rotation.N:
            self._krecik_label.config(image=self._images["krecik_idle_N"])
        elif new_rotation == Rotation.E:
            self._krecik_label.config(image=self._images["krecik_idle_E"])
        elif new_rotation == Rotation.S:
            self._krecik_label.config(image=self._images["krecik_idle_S"])
        elif new_rotation == Rotation.W:
            self._krecik_label.config(image=self._images["krecik_idle_W"])

    def update_command_label_text(self) -> None:
        new_text = (
            f"Position: ({self._krecik_position.row}, {self._krecik_position.col}), "
            f"Rotation: {self._krecik_rotation.name}, "
            f"{self._command_label_text}"
        )
        self._cmd_label.config(text=new_text)
