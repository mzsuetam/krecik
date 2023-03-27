from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from board.board import Board
from interpreter.function_mapper import FunctionMapper
from window.window import Window


class Visitor(KrecikVisitor):
    """
    Visitor is controller that performs game logic in Board and presents results in Window.
    """
    
    def __init__(self, board: Board, window: Window) -> None:
        self.board = board
        self.window = window
        self.function_mapper = FunctionMapper()
    
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        # for child in ctx.children:
        #     print(child)
        return self.visitChildren(ctx)
    
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext):
        name = ctx.VARIABLE_NAME()
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        function = self.function_mapper.get(str(name))
        return function(self.board, self.window, *arguments)

    def visitExpressions_list(
        self,
        ctx: KrecikParser.Expressions_listContext,
    ):
        expr_list = [self.visit(ctx.children[0])]
        if ctx.expressions_list():
            expr_list += self.visit(ctx.expressions_list())
        return expr_list

    def visitExpression(self, ctx: KrecikParser.ExpressionContext):
        if ctx.function_call():
            value = self.visitChildren(ctx)
            print("func:", ctx.getText())
            return value
        if ctx.literal():
            value = self.visit(ctx.children[0])
            print("lit:", value)
            return value
        return 0
    
    def visitLiteral(self, ctx: KrecikParser.LiteralContext):
        value = ctx.getText()
        if ctx.BOOLEAN_VAL():
            return bool(value)
        if ctx.FLOAT_VAL():
            return float(value)
        if ctx.INT_VAL():
            return int(value)
