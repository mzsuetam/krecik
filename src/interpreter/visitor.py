from types import NoneType
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
    KrecikNullValueUsageError,
    KrecikFunctionRedeclarationError,
    KrecikUsageOfBuiltinFunctionNameError,
    KrecikMissingEntryPointError,
    KrecikFunctionUndeclaredError,
    IncorrectArgumentsNumberError,
    KrecikWrongFunctionReturnTypeError,
    KrecikMissingFunctionReturnError,
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
        self.visit(ctx.functions_declarations_list())

        entry_point_name = "ahoj"
        entry_point_type = "nedostatek"
        entry_point = self.function_mapper.declared_function_map.get(entry_point_name)
        if entry_point is None or len(entry_point[1]) > 0:
            raise KrecikMissingEntryPointError(name=f"{entry_point_type} {entry_point_name}()")
        ep_ctx, ep_arg_types, ep_return_type = entry_point

        self.variable_stack.append_frame(entry_point_name)
        self.variable_stack.append_subframe()
        self.visit(ep_ctx.body())
        self.variable_stack.pop_frame()

    def visitFunctions_declarations_list(
        self, ctx: KrecikParser.Functions_declarations_listContext
    ) -> Any:
        function_ctx: KrecikParser.Function_declarationContext = ctx.function_declaration()
        name = function_ctx.VARIABLE_NAME().symbol.text
        if self.function_mapper.build_in_function_map.get(name) is not None:
            raise KrecikUsageOfBuiltinFunctionNameError(name=name)
        if self.function_mapper.declared_function_map.get(name) is not None:
            raise KrecikFunctionRedeclarationError(name=name)

        arg_types = []
        arg_list_ctx: KrecikParser.Declaration_arg_listContext = function_ctx.declaration_arg_list()
        while arg_list_ctx is not None:
            arg_ctx: KrecikParser.DeclarationContext = arg_list_ctx.declaration()
            arg_list_ctx = arg_list_ctx.declaration_arg_list()
            arg_types.append(self.visit(arg_ctx.var_type()))

        return_type = self.visit(function_ctx.return_var_type())
        function = (function_ctx, arg_types, return_type)
        self.function_mapper.declared_function_map.update({name: function})

        if declaration_list := ctx.functions_declarations_list():
            self.visit(declaration_list)

    @handle_exception
    def visitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> Any:
        pass

    @handle_exception
    def visitBody(self, ctx: KrecikParser.BodyContext) -> KrecikType | None:
        if not isinstance(ctx.parentCtx, KrecikParser.Function_declarationContext):
            self.variable_stack.append_subframe()

        item_list: list[KrecikParser.Body_itemContext] = []
        item_list_ctx: KrecikParser.Body_items_listContext = ctx.body_items_list()
        while item_list_ctx is not None:
            item_ctx: KrecikParser.Body_itemContext = item_list_ctx.body_item()
            item_list_ctx = item_list_ctx.body_items_list()
            item_list.append(item_ctx)

        return_value = None
        for child_ctx in item_list:
            return_value = self.visit(child_ctx)
            if self.function_mapper.is_returning():
                self.variable_stack.pop_subframe()
                return return_value
        return None

    def visitBody_item(self, ctx: KrecikParser.Body_itemContext) -> KrecikType | None:
        if cond_expr := ctx.conditional_instruction():
            expr = self.visit(cond_expr)
            return_value = None
            if expr.value:
                return_value = self.visit(ctx.body()[0])
            elif len(ctx.body()) > 1:
                return_value = self.visit(ctx.body()[1])
            return return_value
        if body_line := ctx.body_line():
            val = self.visit(body_line)
            return val
        raise NotImplementedError("Unknown body item.")

    def visitBody_line(self, ctx: KrecikParser.Body_lineContext) -> KrecikType | None:
        child_ctx = ctx.children[0]
        return_value = self.visit(child_ctx)
        return return_value

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
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
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
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise KrecikNullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            # print(left, right, symbol)
            match symbol:
                case "*":
                    return left * right
                case "/":
                    return left / right
        raise KrecikIncompatibleTypes(
            operand_type=symbol, type_1=left.type_name, type_2=right.type_name
        )

    def visitPrimary_operator(self, ctx: KrecikParser.Primary_operatorContext) -> str:
        return ctx.getText()

    @handle_exception
    def visitExpressionSecondaryOperator(
        self, ctx: KrecikParser.ExpressionSecondaryOperatorContext
    ) -> KrecikType:
        left = self.visit(ctx.expression(0))
        symbol = self.visit(ctx.secondary_operator())
        right = self.visit(ctx.expression(1))
        if left is None:
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise KrecikNullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            match symbol:
                case "+":
                    return left + right
                case "-":
                    return left - right
        raise KrecikIncompatibleTypes(
            operand_type=symbol, type_1=left.type_name, type_2=right.type_name
        )

    def visitSecondary_operator(self, ctx: KrecikParser.Secondary_operatorContext) -> str:
        return ctx.getText()

    @handle_exception
    def visitExpressionComparisonOperator(
        self, ctx: KrecikParser.ExpressionComparisonOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        symbol = self.visit(ctx.comparison_operator())
        right = self.visit(ctx.expression(1))
        if left is None:
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise KrecikNullValueUsageError(operand_number=1, operation=ctx.getText())
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
            operand_type=symbol, type_1=left.type_name, type_2=right.type_name
        )

    def visitComparison_operator(self, ctx: KrecikParser.Comparison_operatorContext) -> str:
        return ctx.getText()

    @handle_exception
    def visitExpressionLogicalAndOperator(
        self, ctx: KrecikParser.ExpressionLogicalAndOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None:
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise KrecikNullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            return left and right
        raise KrecikIncompatibleTypes(
            operand_type="oba", type_1=left.type_name, type_2=right.type_name
        )

    @handle_exception
    def visitExpressionLogicalOrOperator(
        self, ctx: KrecikParser.ExpressionLogicalOrOperatorContext
    ) -> Logicki:
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None:
            raise KrecikNullValueUsageError(operand_number=0, operation=ctx.getText())
        if right is None:
            raise KrecikNullValueUsageError(operand_number=1, operation=ctx.getText())
        if type(left) is type(right):
            return left or right
        raise KrecikIncompatibleTypes(
            operand_type="nebo", type_1=left.type_name, type_2=right.type_name
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
            var = self.variable_stack.get_var(name)
            if var.value is None:
                raise KrecikVariableUnassignedError(name=name)
            return var
        raise NotImplementedError("Unknown product.")

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
    def visitFunction_call(self, ctx: KrecikParser.Function_callContext) -> KrecikType | None:
        name = ctx.VARIABLE_NAME().symbol.text
        arguments: list[KrecikType] = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        if name == "print" and self._debug:
            values = [f"[print line {ctx.start.line}] {argument.value}" for argument in arguments]
            print(", ".join(values))
            return KRECIK_TRUE

        builtin = self.function_mapper.build_in_function_map.get(name)
        declared = self.function_mapper.declared_function_map.get(name)
        if builtin is None and declared is None:
            raise KrecikFunctionUndeclaredError(name=name)
        if builtin is not None:
            return self.function_mapper.callBuiltin(name, arguments)
        if declared is None:
            raise KrecikFunctionUndeclaredError(name=name)

        f_ctx: KrecikParser.Function_declarationContext
        f_arg_types: list[Type[KrecikType]]
        f_return_type: KrecikType | None
        f_ctx, f_arg_types, f_return_type = declared
        try:
            self.function_mapper.validate_args(arguments, f_arg_types)
        except IncorrectArgumentsNumberError as exc:
            exc.attrs.update({"function_name": name})
            raise exc

        self.variable_stack.append_frame(name)
        self.variable_stack.append_subframe()
        self.visit(f_ctx.declaration_arg_list())

        arg_names: list[str] = []
        arg_list_ctx: KrecikParser.Declaration_arg_listContext = f_ctx.declaration_arg_list()
        while arg_list_ctx is not None:
            arg_ctx: KrecikParser.DeclarationContext = arg_list_ctx.declaration()
            arg_list_ctx = arg_list_ctx.declaration_arg_list()
            arg_names.append(arg_ctx.VARIABLE_NAME().symbol.text)
        arg: KrecikType
        for name, arg in zip(arg_names, arguments):
            var = self.variable_stack.get_var(name)
            var.value = arg.value
        return_value = self.visit(f_ctx.body())
        if self.function_mapper.is_returning():
            self.function_mapper.reset_returning()
        elif f_return_type is not None:
            raise KrecikMissingFunctionReturnError(expected=f_return_type.type_name)
        self.variable_stack.pop_frame()
        return return_value

    def visitVratit(self, ctx: KrecikParser.VratitContext) -> KrecikType | None:
        self.function_mapper.init_returning()
        expr = ctx.expression()
        return_value = self.visit(expr) if expr else None
        f_name = self.variable_stack.get_curr_function_name()
        function = self.function_mapper.declared_function_map.get(f_name)
        if not function:
            raise KrecikFunctionUndeclaredError(name=f_name)
        exp_type = function[2]
        got_type = type(return_value)
        if exp_type != got_type:
            got_type_str = "nedostatek" if got_type is NoneType else got_type.type_name
            exp_type_str = "nedostatek" if exp_type is None else exp_type.type_name
            raise KrecikWrongFunctionReturnTypeError(expected=exp_type_str, got=got_type_str)

        return return_value

    @handle_exception
    def visitDeclaration(self, ctx: KrecikParser.DeclarationContext) -> KrecikType:
        var_type = self.visit(ctx.var_type())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self.variable_stack.declare_variable(var_type, name)
        return var

    def visitReturn_var_type(self, ctx: KrecikParser.Return_var_typeContext) -> Type | None:
        if ctx.Cislo():
            return Cislo
        if ctx.Cely():
            return Cely
        if ctx.Logicki():
            return Logicki
        if ctx.Nedostatek():
            return None
        raise NotImplementedError("Unknown return type")

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
        expr: KrecikType = self.visit(ctx.expression())
        var: KrecikType = self.visit(ctx.variable())
        if not expr:
            e_name = ctx.getText().split("=")[1]
            raise KrecikVariableValueUnassignableError(expr=e_name)
        if var.type_name != expr.type_name:
            raise KrecikVariableAssignedTypeError(
                name=ctx.getText().split("=")[0], type=var.type_name, val_type=expr.type_name
            )
        var.value = expr.value

    @handle_exception
    def visitVariable(self, ctx: KrecikParser.VariableContext) -> KrecikType:
        if ctx.declaration():
            return self.visit(ctx.children[0])
        if ctx.VARIABLE_NAME():
            return self.variable_stack.get_var(ctx.VARIABLE_NAME().symbol.text)
        raise NotImplementedError("Unknown variable type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = KrecikSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)

    @handle_exception
    def visitConditional_instruction(
        self, ctx: KrecikParser.Conditional_instructionContext
    ) -> KrecikType:
        return self.visit(ctx.expression())
