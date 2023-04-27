from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import (
    KrecikFunctionRedeclarationError,
    KrecikUsageOfBuiltinFunctionNameError,
)
from interpreter.function_mapper import FunctionMapper
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.logicki import Logicki
from interpreter.variable_stack import VariableStack


class Listener(KrecikListener):
    def __init__(self, function_mapper: FunctionMapper, variable_stack: VariableStack) -> None:
        self.function_mapper = function_mapper
        self.variable_stack = variable_stack

    def exitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext) -> None:
        self.function_mapper.declared_function_map.clear()

    def enterFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        name = ctx.VARIABLE_NAME().symbol.text
        if self.function_mapper.build_in_function_map.get(name) is not None:
            raise KrecikUsageOfBuiltinFunctionNameError(name=name)
        if self.function_mapper.declared_function_map.get(name) is not None:
            raise KrecikFunctionRedeclarationError(name=name)
        self.function_mapper.declared_function_map.update({name: (ctx, [], None)})

        self.variable_stack.append_frame(name)
        self.variable_stack.append_subframe()

    def exitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        self.variable_stack.pop_frame()

    # Otwieramy stack
    def enterBody(self, ctx: KrecikParser.BodyContext) -> None:
        if not isinstance(ctx.parentCtx, KrecikParser.Function_declarationContext):
            self.variable_stack.append_subframe()

    # Zamykamy stack
    def exitBody(self, ctx: KrecikParser.BodyContext) -> None:
        self.variable_stack.pop_subframe()

    def enterDeclaration(self, ctx: KrecikParser.DeclarationContext) -> None:
        var_name = ctx.VARIABLE_NAME()
        var_type_ctx: KrecikParser.Var_typeContext = ctx.var_type()

        var_type: type[Cislo] | type[Cely] | type[Logicki]
        if var_type_ctx.Cislo():
            var_type = Cislo
        elif var_type_ctx.Cely():
            var_type = Cely
        elif var_type_ctx.Logicki():
            var_type = Logicki
        else:
            raise NotImplementedError("Unknown var type")
        self.variable_stack.declare_variable(var_type, var_name)
