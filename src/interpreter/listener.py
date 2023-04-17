from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikException, KrecikVariableRedeclarationError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki
from interpreter.variable_stack import VariableStack


class Listener(KrecikListener):

    variable_stack: VariableStack = None

    current_func: str | None = None
    current_stack: int | None = None

    def __init__(self, variable_stack: VariableStack) -> None:
        self.variable_stack = variable_stack

    # Otwieramy top level dict
    def enterFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        func_name = ctx.VARIABLE_NAME().__str__()
        if self.variable_stack.stack.get(func_name):
            raise KrecikVariableRedeclarationError(name=func_name)
        self.variable_stack.stack.update({func_name: []})
        self.current_func = func_name
        self.variable_stack.stack.get(self.current_func).append({}) # obligatory because of arg list
        self.current_stack = 0

    # Zamykamy top level dict
    def exitFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        self.current_func = None

    # Otwieramy stack
    def enterBody(self, ctx:KrecikParser.BodyContext):
        if len(self.variable_stack.stack.get(self.current_func)) > 0:
            self.variable_stack.stack.get(self.current_func).append({})
            self.current_stack += 1

    # Zamykamy stack
    def exitBody(self, ctx:KrecikParser.BodyContext):
        self.current_stack -= 1
        pass

    def enterDeclaration(self, ctx: KrecikParser.DeclarationContext):
        var_type, var_name = ctx.getText().split(' ')
        var: KrecikType | None = None

        if var_type == Cely.type_name:
            var = Cely(None, var_name)
        if var_type == Cislo.type_name:
            var = Cislo(None, var_name)
        if var_type == Logicki.type_name:
            var = Logicki(None, var_name)
        if not var:
            raise KrecikException()

        # tylko ten sam stack, bo niżej możemy miec 'stare zmienne'
        if self.variable_stack.stack.get(self.current_func)[self.current_stack].get(var_name):
            raise KrecikVariableRedeclarationError(var_name=var_name, func_name=self.current_func)

        self.variable_stack.stack.get(self.current_func)[self.current_stack].update({var_name: var})
