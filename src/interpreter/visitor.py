from typing import Any

from antlr4 import ParserRuleContext  # type: ignore

from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.exceptions import KrecikException
from interpreter.function_mapper import FunctionMapper

from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class Visitor(KrecikVisitor):
    """
    Visitor is controller that performs game logic in Board and presents results in Window.
    """
    
    def __init__(self, function_mapper: FunctionMapper) -> None:
        self.function_mapper = function_mapper
    
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        # for child in ctx.children:
        #     print(child)
        return self.visitChildren(ctx)
    
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> Any:
        name = str(ctx.VARIABLE_NAME())
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        try:
            return self.function_mapper.call(str(name), arguments)
        except KrecikException as exc:
            self.inject_context_to_exc(exc, ctx)

    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visit(ctx.children[0])]
        if ctx.expressions_list():
            expr_list += self.visit(ctx.expressions_list())
        return expr_list

    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        if ctx.function_call():
            krecik_literal = self.visitChildren(ctx)
            return krecik_literal
        if ctx.literal():
            krecik_literal = self.visit(ctx.children[0])
            return krecik_literal
        raise RuntimeError("Unknown expression type")

    def visitLiteral(self, ctx: KrecikParser.LiteralContext) -> KrecikType:
        value = ctx.getText()
        if ctx.BOOLEAN_VAL():
            return Logicki(value)
        if ctx.FLOAT_VAL():
            return Cislo(value)
        if ctx.INT_VAL():
            return Cely(value)
        raise RuntimeError("Unknown literal type")

    @staticmethod
    def inject_context_to_exc(exc: KrecikException, ctx: ParserRuleContext) -> None:
        exc.start_line = ctx.start.line
        exc.stop_line = ctx.stop.line
        exc.start_column = ctx.start.column
        exc.stop_column = ctx.stop.column
        raise exc
