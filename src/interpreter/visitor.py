from typing import Any

from antlr4 import ParserRuleContext  # type: ignore
from antlr4.tree.Tree import ErrorNodeImpl

from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.decorators import handle_exception
from interpreter.exceptions import KrecikException, KrecikVariableValueUnassignableError, \
    KrecikVariableAssignedTypeError, KrecikSyntaxError
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

    def __init__(self, function_mapper: FunctionMapper, variable_stack: VariableStack) -> None:
        self.function_mapper = function_mapper
        self.variable_stack = variable_stack

    @handle_exception
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        return_value = self.visitChildren(ctx)
        return return_value

    @handle_exception
    def visitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext):
        name = str(ctx.VARIABLE_NAME())
        self.variable_stack.enterFunction(str(name))
        ### compute children between these lines ###
        return_value = self.visitChildren(ctx)
        ############################################
        self.variable_stack.exitFunction()
        return return_value

    @handle_exception
    def visitBody(self, ctx: KrecikParser.BodyContext):
        self.variable_stack.enterStack()
        ### compute children between these lines ###
        val = self.visitChildren(ctx)
        ############################################
        self.variable_stack.exitStack()
        return val

    @handle_exception
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> Any:
        name = str(ctx.VARIABLE_NAME())
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        try:
            self.variable_stack.enterFunction(str(name))
            ### compute children between these lines ###
            return_value = self.function_mapper.call(str(name), arguments)
            ############################################
            self.variable_stack.exitFunction()
            return return_value
        except KrecikException as exc:
            self.inject_context_to_exc(exc, ctx)

    @handle_exception
    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visit(ctx.children[0])]
        if ctx.expressions_list():
            expr_list += self.visit(ctx.expressions_list())
        return expr_list

    @handle_exception
    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        if ctx.function_call():
            krecik_literal = self.visitChildren(ctx)
            return krecik_literal
        if ctx.literal():
            krecik_literal = self.visit(ctx.children[0])
            return krecik_literal
        if ctx.VARIABLE_NAME():
            var = self.variable_stack.getVarValue(ctx.getText())
            return var
        if unary_operator := ctx.unary_operator():
            match unary_operator:
                case '+':
                    return self.visit(ctx.expression())
                case '-':
                    return -self.visit(ctx.expression())
                case 'Ne':
                    return not self.visit(ctx.expression())
        if ctx.children[0].getText() == '(':
            return self.visit(ctx.expression())
        if binary_operator := ctx.binary_operator():
            first_expression = self.visit(ctx.expression(0))
            second_expression = self.visit(ctx.expression(1))
            if isinstance(first_expression, Cislo) and isinstance(second_expression, Cislo):
                binary_operator = ctx.children[1].getText()
                match binary_operator:
                    case '+':
                        return Cislo(first_expression.value + second_expression.value)
                    case '-':
                        return Cislo(first_expression.value - second_expression.value)
                    case '*':
                        return Cislo(first_expression.value * second_expression.value)
                    case '/':
                        return Cislo(first_expression.value / second_expression.value)
                    case 'mensi':
                        return Logicki(first_expression.value < second_expression.value)
                    case 'wetsi':
                        return Logicki(first_expression.value > second_expression.value)
            if isinstance(first_expression, Cely) and isinstance(second_expression, Cely):
                binary_operator = ctx.children[1].getText()
                match binary_operator:
                    case '+':
                        return Cely(first_expression.value + second_expression.value)
                    case '-':
                        return Cely(first_expression.value - second_expression.value)
                    case '*':
                        return Cely(first_expression.value * second_expression.value)
                    case '/':
                        return Cely(first_expression.value / second_expression.value)
                    case 'mensi':
                        return Logicki(first_expression.value < second_expression.value)
                    case 'wetsi':
                        return Logicki(first_expression.value > second_expression.value)
            raise NotImplementedError("Incompatible expressions' types")
        raise NotImplementedError("Unknown expression type")

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
    def visitVar_type(self, ctx: KrecikParser.Var_typeContext):
        if ctx.Cislo():
            return Cislo.type_name
        if ctx.Cely():
            return Cely.type_name
        if ctx.Logicki():
            return Logicki.type_name
        raise RuntimeError("Unknown var type")

    @handle_exception
    def visitDeclaration(self, ctx: KrecikParser.DeclarationContext):
        v_type = self.visit(ctx.var_type())
        name = str(ctx.VARIABLE_NAME())
        var = self.variable_stack.declare(v_type, name)
        if var.type_name != v_type:
            raise RuntimeError(f"Variable declared type differ ({var.type_name},{v_type})")
        return var

    @handle_exception
    def visitAssignment(self, ctx: KrecikParser.AssignmentContext):
        var: KrecikType = self.visit(ctx.variable())
        expr: KrecikType = self.visit(ctx.expression())
        if not expr:
            e_name = ctx.getText().split(' = ')[1]
            raise KrecikVariableValueUnassignableError(expr=e_name)
        if var.type_name != expr.type_name:
            raise KrecikVariableAssignedTypeError(name=var.name, type=var.type_name, val_type=expr.type_name)
        var.value = expr.value

    @handle_exception
    def visitVariable(self, ctx: KrecikParser.VariableContext):
        var = None
        if ctx.declaration():
            var = self.visit(ctx.children[0])
        if ctx.VARIABLE_NAME():
            var = self.variable_stack.getVarValue(str(ctx.VARIABLE_NAME()))
        return var

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)

    @handle_exception
    def visitConditional_instruction(self, ctx: KrecikParser.Conditional_instructionContext) -> KrecikType:
        return self.visit(ctx.expression())

    @handle_exception
    def visitInstruction(self, ctx:KrecikParser.InstructionContext) -> bool:
        if cond_expr := ctx.conditional_instruction():
            logicki = self.visit(cond_expr)
            flag = logicki.value
            return flag

    @handle_exception
    def visitBody_item(self, ctx: KrecikParser.Body_itemContext) -> None:
        if instruction := ctx.instruction():
            if self.visit(instruction):
                self.visit(ctx.body())
            return
        if body_line := ctx.body_line():
            self.visitChildren(ctx)
            return
        raise NotImplementedError("Unknown body item.")
