from interpreter.board.board import Board
from interpreter.board.tile import TileType
from interpreter.window.window import Window


def test_simple_program_scenario() -> None:
    matrix = [[TileType.GRASS] * 16] * 10
    board = Board(matrix)
    win = Window(board, wait_time=.2)

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
        win.refresh(board)
