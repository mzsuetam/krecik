from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from interpreter.builtin_function_names import BuiltinFunctionName
from interpreter.decorators import handle_exception
from interpreter.exceptions import (
    KrecikUsageOfBuiltinFunctionNameError,
)
from interpreter.function_mappers.declared_function_mapper import DeclaredFunctionMapper
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki
from interpreter.krecik_types.nedostatek import Nedostatek
from interpreter.variable_stack import VariableStack


class Listener(KrecikListener):
    def __init__(
        self,
        declared_function_mapper: DeclaredFunctionMapper,
        variable_stack: VariableStack,
    ) -> None:
        self.declared_function_mapper = declared_function_mapper
        self.variable_stack = variable_stack

    @handle_exception
    def exitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext) -> None:
        self.declared_function_mapper.clear()

    @handle_exception
    def enterFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        name = ctx.VARIABLE_NAME().symbol.text
        try:
            BuiltinFunctionName[name]
        except KeyError:
            self.declared_function_mapper.declare_function(name, ctx, [], Nedostatek)
            self.variable_stack.append_frame(name)
            self.variable_stack.append_subframe()
            return None

        raise KrecikUsageOfBuiltinFunctionNameError(name=name)

    @handle_exception
    def exitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        self.variable_stack.pop_frame()

    @handle_exception
    def enterBody(self, ctx: KrecikParser.BodyContext) -> None:
        if not isinstance(ctx.parentCtx, KrecikParser.Function_declarationContext):
            self.variable_stack.append_subframe()

    @handle_exception
    def exitBody(self, ctx: KrecikParser.BodyContext) -> None:
        self.variable_stack.pop_subframe()

    @handle_exception
    def enterDeclaration(self, ctx: KrecikParser.DeclarationContext) -> None:
        var_name = ctx.VARIABLE_NAME().symbol.text
        var_type_ctx: KrecikParser.Var_typeContext = ctx.var_type()
        var_type: type[KrecikType]

        if var_type_ctx.Cislo():
            var_type = Cislo
        elif var_type_ctx.Cely():
            var_type = Cely
        elif var_type_ctx.Logicki():
            var_type = Logicki
        else:
            raise NotImplementedError("Unknown var type")

        self.variable_stack.declare_variable(var_type, var_name)
