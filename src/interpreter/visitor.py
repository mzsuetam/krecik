from typing import Any

from antlr4.tree.Tree import ErrorNodeImpl  # type: ignore

from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.decorators import handle_exception
from interpreter.exceptions import KrecikSyntaxError
from interpreter.function_mapper import FunctionMapper
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class Visitor(KrecikVisitor):
    def __init__(self, function_mapper: FunctionMapper) -> None:
        self.function_mapper = function_mapper

    @handle_exception
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> Any:
        name = str(ctx.VARIABLE_NAME())
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        return self.function_mapper.call(str(name), arguments)

    @handle_exception
    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visit(ctx.children[0])]
        if ctx.expressions_list():
            expr_list += self.visit(ctx.expressions_list())
        return expr_list

    @handle_exception
    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        '''
        '(' SP* expression SP* ')'
        | unary_operator SP* expression
        | expression SP* binary_operator SP* expression
        | function_call
        | VARIABLE_NAME
        | literal
        '''
        if ctx.function_call():
            krecik_literal = self.visitChildren(ctx)
            return krecik_literal
        if ctx.literal():
            krecik_literal = self.visit(ctx.children[0])
            return krecik_literal
        if ctx.unary_operator():
            match ctx.children[0]:
                case '+':
                    return self.visit(ctx.children[1])
                case '-':
                    return -self.visit(ctx.children[1])
                case 'Ne':
                    return not self.visit(ctx.children[1])
        if ctx.children[0].getText() == '(':
            return self.visit(ctx.children[1])
        if ctx.binary_operator():
            first_expression = self.visit(ctx.children[0])
            second_expression = self.visit(ctx.children[2])
            if not (first_expression.type_name == "cely" and second_expression.type_name == "cely" ) and not (first_expression.type_name == "cislo" and second_expression.type_name == "cislo"):
                raise TypeError("Wrong expression type")
            operator = ctx.children[1].getText()
            match operator:
                case '+':
                    return first_expression + second_expression
                case '-':
                    return first_expression.value - second_expression.value
                case '*':
                    return first_expression * second_expression
                case '/':
                    return first_expression / second_expression
                case 'mensi':
                    return first_expression < second_expression
                case 'wetsi':
                    return first_expression > second_expression
            raise NotImplementedError(operator)

    def visitLiteral(self, ctx: KrecikParser.LiteralContext) -> KrecikType:
        value = ctx.getText()
        if ctx.BOOLEAN_VAL():
            return Logicki(value)
        if ctx.FLOAT_VAL():
            return Cislo(value)
        if ctx.INT_VAL():
            return Cely(value)
        raise NotImplementedError("Unknown literal type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)
        raise exc
