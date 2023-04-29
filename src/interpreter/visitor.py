from typing import Any, Type

from antlr4.tree.Tree import ErrorNodeImpl

from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.decorators import handle_exception
from interpreter.exceptions import (
    KrecikVariableUnassignedError,
    KrecikVariableValueUnassignableError,
    KrecikVariableAssignedTypeError,
    KrecikSyntaxError,
    KrecikIncompatibleTypes,
    NullValueUsageError,
)
from interpreter.function_mapper import FunctionMapper

from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_TRUE, Logicki
from interpreter.variable_stack import VariableStack


class Visitor(KrecikVisitor):
    def __init__(
        self,
        function_mapper: FunctionMapper,
        variable_stack: VariableStack,
        debug: bool = False,
    ) -> None:
        self.function_mapper = function_mapper
        self.variable_stack = variable_stack
        self._debug = debug

    @handle_exception
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext) -> None:
        return self.visitChildren(ctx)

    @handle_exception
    def visitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> Any:
        name = str(ctx.VARIABLE_NAME())
        self.variable_stack.enter_function(str(name))
        return_value = self.visitChildren(ctx)
        self.variable_stack.exit_function()
        return return_value

    @handle_exception
    def visitBody(self, ctx: KrecikParser.BodyContext) -> Any:
        self.variable_stack.enter_stack()
        val = self.visitChildren(ctx)
        self.variable_stack.exit_stack()
        return val

    def visitBody_item(self, ctx: KrecikParser.Body_itemContext) -> None:
        if cond_expr := ctx.conditional_instruction():
            logicki = self.visit(cond_expr)
            if logicki.value:
                self.visit(ctx.body()[0])
            elif len(ctx.body()) > 1:
                self.visit(ctx.body()[1])
            return
        if body_line := ctx.body_line():
            self.visitChildren(body_line)
            return
        raise NotImplementedError("Unknown body item.")

    @handle_exception
    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visit(ctx.expression())]
        if rest := ctx.expressions_list():
            expr_list += self.visit(rest)
        return expr_list

    @handle_exception
    def visitExpressionUnaryOperator(
        self, ctx: KrecikParser.ExpressionUnaryOperatorContext
    ) -> KrecikType:
        symbol = self.visit(ctx.secondary_operator())
        expression = self.visit(ctx.expression())
        if expression is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        match symbol:
            case "+":
                return expression
            case "-":
                return -expression
            case "ne":
                return ~expression
        raise NotImplementedError("Bad symbol: ", symbol)

    @handle_exception
    def visitExpressionPrimaryOperator(
        self, ctx: KrecikParser.ExpressionPrimaryOperatorContext
    ) -> KrecikType:
        left = self.visit(ctx.expression(0))
        symbol = self.visit(ctx.primary_operator())
        right = self.visit(ctx.expression(1))
        if left is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise NullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            # print(left, right, symbol)
            match symbol:
                case "*":
                    return left * right
                case "/":
                    return left / right
        raise KrecikIncompatibleTypes(
            operand_type=symbol,
            type_1=left.type_name,
            type_2=right.type_name,
        )

    def visitPrimary_operator(self, ctx: KrecikParser.Primary_operatorContext) -> str:
        return ctx.children[0].symbol.text

    @handle_exception
    def visitExpressionSecondaryOperator(
        self, ctx: KrecikParser.ExpressionSecondaryOperatorContext
    ) -> KrecikType:
        left = self.visit(ctx.expression(0))
        symbol = self.visit(ctx.secondary_operator())
        right = self.visit(ctx.expression(1))
        if left is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise NullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            match symbol:
                case "+":
                    return left + right
                case "-":
                    return left - right
        raise KrecikIncompatibleTypes(
            operand_type=symbol,
            type_1=left.type_name,
            type_2=right.type_name,
        )

    def visitSecondary_operator(self, ctx: KrecikParser.Secondary_operatorContext) -> str:
        return ctx.children[0].symbol.text

    @handle_exception
    def visitExpressionComparisonOperator(
        self, ctx: KrecikParser.ExpressionComparisonOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        symbol = self.visit(ctx.comparison_operator())
        right = self.visit(ctx.expression(1))
        if left is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise NullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            # print(left, right, symbol)
            match symbol:
                case "mensi":
                    return left < right
                case "wetsi":
                    return left > right
                case "je":
                    return left == right
                case "neje":
                    return left != right
        raise KrecikIncompatibleTypes(
            operand_type=symbol,
            type_1=left.type_name,
            type_2=right.type_name,
        )

    def visitComparison_operator(self, ctx: KrecikParser.Comparison_operatorContext) -> str:
        return ctx.children[0].symbol.text

    @handle_exception
    def visitExpressionLogicalAndOperator(
        self, ctx: KrecikParser.ExpressionLogicalAndOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise NullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            return left and right
        raise KrecikIncompatibleTypes(
            operand_type="oba",
            type_1=left.type_name,
            type_2=right.type_name,
        )

    @handle_exception
    def visitExpressionLogicalOrOperator(
        self, ctx: KrecikParser.ExpressionLogicalOrOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None:
            raise NullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise NullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            return left or right
        raise KrecikIncompatibleTypes(
            operand_type="nebo",
            type_1=left.type_name,
            type_2=right.type_name,
        )

    @handle_exception
    def visitParenthesisedExpression(
        self, ctx: KrecikParser.ParenthesisedExpressionContext
    ) -> KrecikType | None:
        return self.visit(ctx.expression())

    @handle_exception
    def visitAtomExpression(self, ctx: KrecikParser.AtomExpressionContext) -> KrecikType | None:
        return self.visit(ctx.atom())

    @handle_exception
    def visitAtom(self, ctx: KrecikParser.AtomContext) -> KrecikType | None:
        if func_call := ctx.function_call():
            return self.visit(func_call)
        if literal := ctx.literal():
            return self.visit(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self.variable_stack.get_var_value(name)
            if var.value is None:
                raise KrecikVariableUnassignedError(name=name)
            return var
        raise NotImplementedError("Unknown product.")

    @handle_exception
    def visitLiteral(self, ctx: KrecikParser.LiteralContext) -> KrecikType:
        value = ctx.children[0].symbol.text
        if ctx.BOOLEAN_VAL():
            return Logicki(value)
        if ctx.FLOAT_VAL():
            return Cislo(value)
        if ctx.INT_VAL():
            return Cely(value)
        raise NotImplementedError("Unknown literal type")

    @handle_exception
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> KrecikType:
        name = ctx.VARIABLE_NAME().symbol.text
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        if name == "print" and self._debug:
            values = [str(argument) for argument in arguments]
            print(f"[print line {ctx.start.line}]", ", ".join(values))
            return KRECIK_TRUE
        self.variable_stack.enter_function(name)
        return_value = self.function_mapper.call(name, arguments)
        self.variable_stack.exit_function()
        return return_value

    @handle_exception
    def visitDeclaration(self, ctx: KrecikParser.DeclarationContext) -> KrecikType:
        var_type = self.visit(ctx.var_type())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self.variable_stack.declare(var_type, name)
        return var

    def visitVar_type(self, ctx: KrecikParser.Var_typeContext) -> Type[KrecikType]:
        if ctx.Cislo():
            return Cislo
        if ctx.Cely():
            return Cely
        if ctx.Logicki():
            return Logicki
        raise NotImplementedError("Unknown var type")

    @handle_exception
    def visitAssignment(self, ctx: KrecikParser.AssignmentContext) -> None:
        var: KrecikType = self.visit(ctx.variable())
        expr: KrecikType = self.visit(ctx.expression())
        if not expr:
            expr_text = ctx.getText().split("=")[1]
            raise KrecikVariableValueUnassignableError(expr=expr_text)
        if var.type_name != expr.type_name:
            var_name = ctx.getText().split("=")[0]
            raise KrecikVariableAssignedTypeError(
                name=var_name,
                type=var.type_name,
                val_type=expr.type_name,
            )
        var.value = expr.value

    @handle_exception
    def visitVariable(self, ctx: KrecikParser.VariableContext) -> KrecikType:
        if ctx.declaration():
            return self.visit(ctx.children[0])
        if ctx.VARIABLE_NAME():
            return self.variable_stack.get_var_value(str(ctx.VARIABLE_NAME()))
        raise NotImplementedError("Unknown variable type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)

    @handle_exception
    def visitConditional_instruction(
        self, ctx: KrecikParser.Conditional_instructionContext
    ) -> KrecikType:
        return self.visit(ctx.expression())
