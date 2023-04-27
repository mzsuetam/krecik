from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikException, KrecikVariableRedeclarationError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki
from interpreter.variable_stack import VariableStack


class Listener(KrecikListener):
    def __init__(self, variable_stack: VariableStack) -> None:
        self.variable_stack = variable_stack

    def enterFunction_declaration(self, ctx: KrecikParser.Function_declarationContext) -> None:
        self.variable_stack.append_frame(ctx.VARIABLE_NAME())
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
        if var_type_ctx.Cislo():
            var_type = Cislo
        elif var_type_ctx.Cely():
            var_type = Cely
        elif var_type_ctx.Logicki():
            var_type = Logicki
        else:
            raise NotImplementedError("Unknown var type")
        self.variable_stack.declare_variable(var_type, var_name)
