from antlr4 import CommonTokenStream, InputStream

from antlr.KrecikLexer import KrecikLexer
from antlr.KrecikParser import KrecikParser
from board.board import Board
from board.tile import TileType
from visitor import Visitor


if __name__ == "__main__":

    with open("../inputs/simple.krecik", "r") as file:
        data = InputStream(file.read())

    # lexer
    lexer = KrecikLexer(data)
    stream = CommonTokenStream(lexer)
    # parser
    parser = KrecikParser(stream)
    tree = parser.primary_expression()

    matrix = [
        [TileType.GRASS, TileType.GRASS],
        [TileType.GRASS, TileType.GRASS],
    ]
    board = Board(matrix)
    # evaluator
    visitor = Visitor(board)
    output = visitor.visit(tree)
    print(output)
