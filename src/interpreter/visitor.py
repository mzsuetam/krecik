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
)
from interpreter.function_mapper import FunctionMapper

from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki
from interpreter.variable_stack import VariableStack


class Visitor(KrecikVisitor):
    """
    Visitor is controller that performs game logic in Board and presents results in Window.
    """

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
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext) -> Any:
        return_value = self.visitChildren(ctx)
        return return_value

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

    @handle_exception
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> Any:
        name = ctx.VARIABLE_NAME().symbol.text
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        self.variable_stack.enter_function(name)
        return_value = self.function_mapper.call(name, arguments)
        self.variable_stack.exit_function()
        return return_value

    @handle_exception
    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visit(ctx.expression())]
        if rest := ctx.expressions_list():
            expr_list += self.visit(rest)
        return expr_list

    @handle_exception
    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        if product := ctx.product():
            symbol = self.visit(ctx.children[1])
            product = self.visit(ctx.product(0))
            prod_val = product.value
            expression = self.visit(ctx.expression(0))
            exp_val = expression.value
            if isinstance(product, Cislo) and isinstance(expression, Cislo):
                match symbol:
                    case '+':
                        return Cislo(prod_val + exp_val)
                    case '-':
                        return Cislo(prod_val + exp_val)
            if isinstance(product, Cely) and isinstance(expression, Cely):
                match symbol:
                    case '+':
                        return Cely(prod_val + exp_val)
                    case '-':
                        return Cely(prod_val + exp_val)
    @handle_exception
    def visitProduct(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        if func_call := ctx.function_call():
            return self.visit(func_call)
        if literal := ctx.literal():
            return self.visit(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self.variable_stack.get_var_value(name)
            if var.value is None:
                raise KrecikVariableUnassignedError(name=var.name)
            return var
        if ctx.children[0].getText() == "(":
            return self.visit(ctx.expression(0))
        if unary_operator := ctx.unary_operator():
            symbol = self.visit(unary_operator)
            expression = self.visit(ctx.product(0))
            exp_val = expression.value
            if isinstance(expression, Cislo):
                match symbol:
                    case "+":
                        return Cislo(exp_val)
                    case "-":
                        return Cislo(-exp_val)
                    case "ne":
                        return Logicki(not exp_val)
            if isinstance(expression, Cely):
                match symbol:
                    case "+":
                        return Cely(exp_val)
                    case "-":
                        return Cely(-exp_val)
                    case "ne":
                        return Logicki(not exp_val)

    '''
    @handle_exception
    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        if func_call := ctx.function_call():
            return self.visit(func_call)
        if literal := ctx.literal():
            return self.visit(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self.variable_stack.get_var_value(name)
            if var.value is None:
                raise KrecikVariableUnassignedError(name=var.name)
            return var
        if unary_operator := ctx.unary_operator():
            symbol = self.visit(unary_operator)
            expression = self.visit(ctx.expression(0))
            exp_val = expression.value
            if isinstance(expression, Cislo):
                match symbol:
                    case "+":
                        return Cislo(exp_val)
                    case "-":
                        return Cislo(-exp_val)
                    case "ne":
                        return Logicki(not exp_val)
            if isinstance(expression, Cely):
                match symbol:
                    case "+":
                        return Cely(exp_val)
                    case "-":
                        return Cely(-exp_val)
                    case "ne":
                        return Logicki(not exp_val)
        if ctx.children[0].getText() == "(":
            return self.visit(ctx.expression(0))
        if binary_operator := ctx.binary_operator():
            symbol = self.visit(binary_operator)
            first_expression = self.visit(ctx.expression(0))
            second_expression = self.visit(ctx.expression(1))
            first_value = first_expression.value
            second_value = second_expression.value
            if isinstance(first_expression, Cislo) and isinstance(second_expression, Cislo):
                match symbol:
                    case "+":
                        return Cislo(first_value + second_value)
                    case "-":
                        return Cislo(first_value - second_value)
                    case "*":
                        return Cislo(first_value * second_value)
                    case "/":
                        return Cislo(first_value / second_value)
                    case "mensi":
                        return Logicki(first_value < second_value)
                    case "wetsi":
                        return Logicki(first_value > second_value)
            if isinstance(first_expression, Cely) and isinstance(second_expression, Cely):
                match symbol:
                    case "+":
                        return Cely(first_value + second_value)
                    case "-":
                        return Cely(first_value - second_value)
                    case "*":
                        return Cely(first_value * second_value)
                    case "/":
                        return Cely(first_value / second_value)
                    case "mensi":
                        return Logicki(first_value < second_value)
                    case "wetsi":
                        return Logicki(first_value > second_value)
            if isinstance(first_expression, Logicki) and isinstance(second_expression, Logicki):
                match symbol:
                    case "nebo":
                        return Logicki(first_value or second_value)
                    case "oba":
                        return Logicki(first_value and second_value)
                    case "je":
                        return Logicki(first_value == second_value)
                    case "neje":
                        return Logicki(first_value != second_value)
            raise KrecikIncompatibleTypes()
        raise NotImplementedError("Unknown expression type")
    '''
    def visitUnary_operator(self, ctx: KrecikParser.Unary_operatorContext) -> str:
        return ctx.getText()

    def visitBinary_operator(self, ctx: KrecikParser.Binary_operatorContext) -> str:
        return ctx.getText()

    @handle_exception
    def visitLiteral(self, ctx: KrecikParser.LiteralContext) -> KrecikType:
        value = ctx.getText()
        if ctx.BOOLEAN_VAL():
            return Logicki(value)
        if ctx.FLOAT_VAL():
            return Cislo(value)
        if ctx.INT_VAL():
            return Cely(value)
        raise NotImplementedError("Unknown literal type")

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
            e_name = ctx.getText().split(" = ")[1]
            raise KrecikVariableValueUnassignableError(expr=e_name)
        if var.type_name != expr.type_name:
            raise KrecikVariableAssignedTypeError(
                name=var.name, type=var.type_name, val_type=expr.type_name
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

    @handle_exception
    def visitInstruction(self, ctx: KrecikParser.InstructionContext) -> bool:
        if cond_expr := ctx.conditional_instruction():
            logicki = self.visit(cond_expr)
            flag = logicki.value
            return flag
        raise NotImplementedError("Unknown instruction.")

    @handle_exception
    def visitBody_item(self, ctx: KrecikParser.Body_itemContext) -> None:
        if instruction := ctx.instruction():
            if self.visit(instruction):
                self.visit(ctx.body())
            return
        if body_line := ctx.body_line():
            self.visitChildren(body_line)
            return
        raise NotImplementedError("Unknown body item.")
