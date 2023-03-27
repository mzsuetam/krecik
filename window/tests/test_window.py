from board.board import Board
from board.tile import TileType
from window.window import Window


def test_simple_program_scenario() -> None:
    matrix = [[TileType.GRASS] * 16] * 10
    board = Board(matrix)
    window = Window(board, wait_time=.2)

    commands = [
        board.krecik_move,
        board.krecik_move,
        board.krecik.turn_left,
        board.krecik_move,
        board.krecik_move,
        board.krecik_move,
        board.krecik.turn_right,
        board.krecik.turn_right,
        board.krecik.turn_right,
        board.krecik.turn_right,
        board.krecik.turn_right,
    ]

    for command in commands:
        command()
        window.update_krecik_position(board.krecik)
        window.update_krecik_rotation(board.krecik)
        window.refresh()
