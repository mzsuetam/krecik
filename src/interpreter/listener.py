from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikException, KrecikVariableRedeclarationError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class Listener(KrecikListener):

    variable_set = {} # dist of stacks of dicts {str, list[{str, KrecikType}]}
        # dict: append(), pop()

    current_func : str | None = None
    current_stack : int | None = None
    await_for_body : bool = True

    # Otwieramy top level dict
    def enterFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        func_name = ctx.VARIABLE_NAME()
        if self.variable_set.get(func_name):
            raise KrecikVariableRedeclarationError(name=func_name)
        self.variable_set.update({func_name: []})
        self.current_func = func_name
        self.variable_set.get(self.current_func).append({}) # obligatory because of arg list
        self.current_stack = 0
        self.await_for_body = True

    # Zamykamy top level dict
    def exitFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        self.current_func = None

    # Otwieramy stack
    def enterBody(self, ctx:KrecikParser.BodyContext):
        if self.await_for_body:
            self.await_for_body = False
        else:
            self.variable_set.get(self.current_func).append({})
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

        # print( self.current_func, self.current_stack, var_name)
        if self.variable_set.get(self.current_func)[self.current_stack].get(var_name):
            raise KrecikVariableRedeclarationError(var_name=var_name, func_name=self.current_func)

        self.variable_set.get(self.current_func)[self.current_stack].update({var_name: var})

    def getVariablesSet(self) -> {str, KrecikType}:
        return self.variable_set
