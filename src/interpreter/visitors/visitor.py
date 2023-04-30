from typing import Any, Type

from antlr4.tree.Tree import ErrorNodeImpl

from antlr.KrecikParser import KrecikParser
from interpreter.decorators import handle_exception
from interpreter.exceptions import (
    KrecikSyntaxError,
    KrecikVariableAssignedTypeError,
    KrecikVariableUnassignedError,
    KrecikVariableValueUnassignableError,
)
from interpreter.function_mapper import FunctionMapper
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_TRUE, Logicki
from interpreter.variable_stack import VariableStack
from interpreter.visitors.expressions_visitor import ExpressionsVisitor


class Visitor(ExpressionsVisitor):
    def __init__(
        self,
        function_mapper: FunctionMapper,
        variable_stack: VariableStack,
        debug: bool = False,
    ) -> None:
        self.function_mapper = function_mapper
        self.variable_stack = variable_stack
        self._debug = debug

    # PRIMARY EXPRESSION
    @handle_exception
    def visitPrimary_expression(
        self,
        ctx: KrecikParser.Primary_expressionContext,
    ) -> None:
        return self.visitChildren(ctx)

    # FUNCTIONS
    @handle_exception
    def visitFunction_declaration(
        self,
        ctx: KrecikParser.Function_declarationContext,
    ) -> Any:
        name = str(ctx.VARIABLE_NAME())
        self.variable_stack.enter_function(str(name))
        return_value = self.visitChildren(ctx)
        self.variable_stack.exit_function()
        return return_value

    @handle_exception
    def visitBody(
        self,
        ctx: KrecikParser.BodyContext,
    ) -> Any:
        self.variable_stack.enter_stack()
        val = self.visitChildren(ctx)
        self.variable_stack.exit_stack()
        return val

    def visitBody_item(
        self,
        ctx: KrecikParser.Body_itemContext,
    ) -> None:
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
    def visitFunction_call(
        self,
        ctx: KrecikParser.Function_callContext,
    ) -> KrecikType:
        name = ctx.VARIABLE_NAME().symbol.text
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        if name == "print" and self._debug:
            values = [f"[print line {ctx.start.line}] {argument.value}" for argument in arguments]
            print(", ".join(values))
            return KRECIK_TRUE
        self.variable_stack.enter_function(name)
        return_value = self.function_mapper.call(name, arguments)
        self.variable_stack.exit_function()
        return return_value

    # EXPRESSIONS
    @handle_exception
    def visitAtom(
        self,
        ctx: KrecikParser.AtomContext,
    ) -> KrecikType | None:
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

    # INSTRUCTIONS
    @handle_exception
    def visitConditional_instruction(
        self,
        ctx: KrecikParser.Conditional_instructionContext,
    ) -> KrecikType:
        return self.visit(ctx.expression())

    # VARIABLES AND TYPES
    def visitVar_type(self, ctx: KrecikParser.Var_typeContext) -> Type[KrecikType]:
        if ctx.Cislo():
            return Cislo
        if ctx.Cely():
            return Cely
        if ctx.Logicki():
            return Logicki
        raise NotImplementedError("Unknown var type")

    @handle_exception
    def visitDeclaration(
        self,
        ctx: KrecikParser.DeclarationContext,
    ) -> KrecikType:
        var_type = self.visit(ctx.var_type())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self.variable_stack.declare(var_type, name)
        return var

    @handle_exception
    def visitLiteral(
        self,
        ctx: KrecikParser.LiteralContext,
    ) -> KrecikType:
        value = ctx.getText()
        if ctx.BOOLEAN_VAL():
            return Logicki(value)
        if ctx.FLOAT_VAL():
            return Cislo(value)
        if ctx.INT_VAL():
            return Cely(value)
        raise NotImplementedError("Unknown literal type")

    @handle_exception
    def visitAssignment(
        self,
        ctx: KrecikParser.AssignmentContext,
    ) -> None:
        expr: KrecikType = self.visit(ctx.expression())
        if expr is None:
            expr_str = ctx.expression().getText()
            raise KrecikVariableValueUnassignableError(expr=expr_str)

        var: KrecikType = self.visit(ctx.variable())
        if type(var) is not type(expr):
            var_str = ctx.variable().getText().split(" ")
            if len(var_str) > 1:
                var_str = var_str[1]
            else:
                var_str = var_str[0]
            raise KrecikVariableAssignedTypeError(
                val_type=expr.type_name,
                name=var_str,
                type=var.type_name,
            )

        var.value = expr.value

    @handle_exception
    def visitVariable(
        self,
        ctx: KrecikParser.VariableContext,
    ) -> KrecikType:
        if declaration_ctx := ctx.declaration():
            return self.visit(declaration_ctx)
        if var_name_ctx := ctx.VARIABLE_NAME():
            var_name = var_name_ctx.symbol.text
            return self.variable_stack.get_var_value(var_name)
        raise NotImplementedError("Unknown variable type")

    def visitErrorNode(
        self,
        error_node: ErrorNodeImpl,
    ) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)
