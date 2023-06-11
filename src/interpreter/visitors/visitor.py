from typing import Any

from antlr4.tree.Tree import ErrorNodeImpl

from antlr.KrecikParser import KrecikParser
from interpreter.decorators import handle_exception
from interpreter.exceptions import (
    KrecikSyntaxError,
    KrecikVariableAssignedTypeError,
    KrecikVariableUnassignedError,
    KrecikVariableValueUnassignableError,
    ConditionTypeError,
    IncorrectArgumentsNumberError,
    KrecikMissingFunctionReturnError,
    KrecikMissingEntryPointError,
    KrecikUsageOfBuiltinFunctionNameError,
    KrecikWrongFunctionReturnTypeError,
    NotDefinedFunctionError,
)
from interpreter.function_mappers.builtin_function_mapper import (
    BuiltinFunctionMapper,
)
from interpreter.builtin_function_names import BuiltinFunctionName
from interpreter.function_mappers.declared_function_mapper import DeclaredFunctionMapper
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_TRUE, Logicki
from interpreter.krecik_types.nedostatek import Nedostatek, KRECIK_NONE
from interpreter.utils import validate_args
from interpreter.variable_stack import VariableStack
from interpreter.visitors.expressions_visitor import ExpressionsVisitor


class Visitor(ExpressionsVisitor):
    def __init__(
        self,
        builtin_function_mapper: BuiltinFunctionMapper,
        declared_function_mapper: DeclaredFunctionMapper,
        variable_stack: VariableStack,
        allow_prints: bool = False,
    ) -> None:
        self.builtin_function_mapper = builtin_function_mapper
        self.declared_function_mapper = declared_function_mapper
        self.variable_stack = variable_stack
        self._allow_prints = allow_prints

    # PRIMARY EXPRESSION
    @handle_exception
    def visitPrimary_expression(
        self,
        ctx: KrecikParser.Primary_expressionContext,
    ) -> None:
        function_declaration_ctx_list = self.visitFunctions_declarations_list(
            ctx.functions_declarations_list()
        )
        for function_declaration_ctx in function_declaration_ctx_list:
            self.visitFunction_declaration(function_declaration_ctx)

        main_return_type, main_name = "nedostatek", "ahoj"
        main_func = self.declared_function_mapper.get_function(main_name)
        if len(main_func.arg_types) > 0:
            raise KrecikMissingEntryPointError(name=f"{main_return_type} {main_name}()")

        self.variable_stack.append_frame(main_name)
        self.variable_stack.append_subframe()
        self.visitBody(main_func.context.body())
        self.variable_stack.pop_frame()

    # FUNCTIONS
    def visitFunctions_declarations_list(
        self, ctx: KrecikParser.Functions_declarations_listContext
    ) -> Any:
        func_declr_list: list[KrecikParser.Function_declarationContext] = []
        func_declr_list_ctx: KrecikParser.Functions_declarations_listContext = ctx
        while func_declr_list_ctx is not None:
            func_declr_ctx: KrecikParser.Function_declarationContext = (
                func_declr_list_ctx.function_declaration()
            )
            func_declr_list_ctx = func_declr_list_ctx.functions_declarations_list()
            func_declr_list.append(func_declr_ctx)
        return func_declr_list

    @handle_exception
    def visitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        """
        Use only for function declaration. Not for function call.
        """
        name = ctx.VARIABLE_NAME().symbol.text
        try:
            BuiltinFunctionName[name]
        except KeyError:
            arg_types = []
            arg_list_ctx: KrecikParser.Declaration_arg_listContext = ctx.declaration_arg_list()
            if arg_list_ctx:
                arg_types = [
                    self.visitVar_type(a_ctx.var_type())
                    for a_ctx in self.visitDeclaration_arg_list(arg_list_ctx)
                ]

            return_type = self.visitReturn_var_type(ctx.return_var_type())
            self.declared_function_mapper.declare_function(name, ctx, arg_types, return_type)
            return None

        raise KrecikUsageOfBuiltinFunctionNameError(name=name)

    @handle_exception
    def visitDeclaration_arg_list(
        self, ctx: KrecikParser.Declaration_arg_listContext
    ) -> list[KrecikParser.DeclarationContext]:
        arg_ctx_list: list[KrecikParser.DeclarationContext] = []
        arg_list_ctx: KrecikParser.Declaration_arg_listContext = ctx
        while arg_list_ctx is not None:
            arg_ctx: KrecikParser.DeclarationContext = arg_list_ctx.declaration()
            arg_list_ctx = arg_list_ctx.declaration_arg_list()
            arg_ctx_list.append(arg_ctx)
        return arg_ctx_list

    @handle_exception
    def visitBody(self, ctx: KrecikParser.BodyContext) -> KrecikType:
        if not isinstance(ctx.parentCtx, KrecikParser.Function_declarationContext):
            self.variable_stack.append_subframe()

        body_item_ctx_list: list[KrecikParser.Body_itemContext] = self.visitBody_items_list(
            ctx.body_items_list()
        )
        for child_ctx in body_item_ctx_list:
            return_value = self.visitBody_item(child_ctx)
            if self.declared_function_mapper.is_returning():
                self.variable_stack.pop_subframe()
                return return_value
        self.variable_stack.pop_subframe()
        return KRECIK_NONE

    def visitBody_items_list(
        self, ctx: KrecikParser.Body_items_listContext
    ) -> list[KrecikParser.Body_itemContext]:
        item_list: list[KrecikParser.Body_itemContext] = []
        item_list_ctx: KrecikParser.Body_items_listContext = ctx
        while item_list_ctx is not None:
            item_ctx: KrecikParser.Body_itemContext = item_list_ctx.body_item()
            item_list_ctx = item_list_ctx.body_items_list()
            item_list.append(item_ctx)
        return item_list

    @handle_exception
    def visitBody_item(self, ctx: KrecikParser.Body_itemContext) -> KrecikType:
        if cond_instr_ctx := ctx.conditional_instruction():
            return self.visitConditional_instruction(cond_instr_ctx)
        if loop_instr_ctx := ctx.loop_instruction():
            return self.visitLoop_instruction(loop_instr_ctx)
        if body_line := ctx.body_line():
            val = self.visitBody_line(body_line)
            return val
        raise NotImplementedError("Unknown body item.")

    @handle_exception
    def visitBody_line(self, ctx: KrecikParser.Body_lineContext) -> KrecikType:
        child_ctx = ctx.children[0]
        return_value = self.visit(child_ctx)
        return return_value

    @handle_exception
    def visitFunction_call(
        self,
        ctx: KrecikParser.Function_callContext,
    ) -> KrecikType:
        a_name = ctx.VARIABLE_NAME().symbol.text
        arguments: list[KrecikType] = []
        if ctx.expressions_list():
            arguments = self.visitExpressions_list(ctx.expressions_list())
        if a_name == "print" and self._allow_prints:
            values = [f"[print line {ctx.start.line}] {argument.value}" for argument in arguments]
            print(", ".join(values))
            return KRECIK_TRUE

        try:
            val = self.builtin_function_mapper.call(a_name, arguments)
            return val
        except NotDefinedFunctionError:
            declared_function = self.declared_function_mapper.get_function(a_name)

        try:
            validate_args(arguments, declared_function.arg_types)
        except IncorrectArgumentsNumberError as exc:
            exc.attrs.update({"function_name": a_name})
            raise exc

        self.variable_stack.append_frame(a_name)
        self.variable_stack.append_subframe()
        arg_list_ctx = declared_function.context.declaration_arg_list()
        self.visitDeclaration_arg_list(arg_list_ctx)

        arg_names = []
        if arg_list_ctx:
            arg_names = [
                a_ctx.VARIABLE_NAME().symbol.text
                for a_ctx in self.visitDeclaration_arg_list(arg_list_ctx)
            ]
        arg: KrecikType
        for a_name, a_type, arg in zip(arg_names, declared_function.arg_types, arguments):
            var = self.variable_stack.declare_variable(a_type, a_name)
            var.value = arg.value
        return_value = self.visitBody(declared_function.context.body())
        if self.declared_function_mapper.is_returning():
            self.declared_function_mapper.reset_returning()
        elif declared_function.return_type != KRECIK_NONE:
            raise KrecikMissingFunctionReturnError(expected=declared_function.return_type.type_name)
        self.variable_stack.pop_frame()
        return return_value

    @handle_exception
    def visitReturn(self, ctx: KrecikParser.ReturnContext) -> KrecikType:
        self.declared_function_mapper.init_returning()
        return_value = self.visitExpression(e_ctx) if (e_ctx := ctx.expression()) else KRECIK_NONE
        function_name = self.variable_stack.get_curr_function_name()
        function = self.declared_function_mapper.get_function(function_name)
        if not isinstance(return_value, function.return_type):
            got_type_str = return_value.type_name
            exp_type_str = function.return_type.type_name
            raise KrecikWrongFunctionReturnTypeError(expected=exp_type_str, got=got_type_str)
        return return_value

    # EXPRESSIONS
    @handle_exception
    def visitAtom(
        self,
        ctx: KrecikParser.AtomContext,
    ) -> KrecikType:
        if func_call := ctx.function_call():
            return self.visitFunction_call(func_call)
        if literal := ctx.literal():
            return self.visitLiteral(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self.variable_stack.get_var(name)
            if var.value is None:
                raise KrecikVariableUnassignedError(name=name)
            return var
        raise NotImplementedError("Unknown product.")

    # INSTRUCTIONS
    @handle_exception
    def visitConditional_instruction(
        self,
        ctx: KrecikParser.Conditional_instructionContext,
    ) -> None:
        expression_ctx = ctx.expression()
        if self.check_condition(expression_ctx):
            val = self.visitBody(ctx.body(0))
            if self.declared_function_mapper.is_returning():
                return val
        elif ctx.Jiny():
            val = self.visitBody(ctx.body(1))
            if self.declared_function_mapper.is_returning():
                return val

    @handle_exception
    def visitLoop_instruction(
        self,
        ctx: KrecikParser.Loop_instructionContext,
    ) -> None:
        expression_ctx = ctx.expression()
        body_ctx = ctx.body()
        while self.check_condition(expression_ctx):
            val = self.visitBody(body_ctx)
            if self.declared_function_mapper.is_returning():
                return val

    def check_condition(self, condition_ctx: KrecikParser.ExpressionContext) -> bool:
        condition_value: KrecikType = self.visitExpression(condition_ctx)
        if not isinstance(condition_value, Logicki):
            raise ConditionTypeError(type=condition_value.type_name)
        if condition_value != KRECIK_TRUE:
            return False
        return True

    # VARIABLES AND TYPES

    def visitReturn_var_type(self, ctx: KrecikParser.Return_var_typeContext) -> type[KrecikType]:
        if ctx.Cislo():
            return Cislo
        if ctx.Cely():
            return Cely
        if ctx.Logicki():
            return Logicki
        if ctx.Nedostatek():
            return Nedostatek
        raise NotImplementedError("Unknown return type")

    def visitVar_type(self, ctx: KrecikParser.Var_typeContext) -> type[KrecikType]:
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
        var_type = self.visitVar_type(ctx.var_type())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self.variable_stack.declare_variable(var_type, name)
        return var

    @handle_exception
    def visitLiteral(
        self,
        ctx: KrecikParser.LiteralContext,
    ) -> KrecikType:
        value = ctx.children[0].symbol.text
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
        expr: KrecikType = self.visitExpression(ctx.expression())
        if expr is None:
            expr_str = ctx.expression().getText()
            raise KrecikVariableValueUnassignableError(expr=expr_str)

        var: KrecikType = self.visitVariable(ctx.variable())
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
            return self.visitDeclaration(declaration_ctx)
        if var_name_ctx := ctx.VARIABLE_NAME():
            var_name = var_name_ctx.symbol.text
            return self.variable_stack.get_var(var_name)
        raise NotImplementedError("Unknown variable type")

    def visitErrorNode(
        self,
        error_node: ErrorNodeImpl,
    ) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)
