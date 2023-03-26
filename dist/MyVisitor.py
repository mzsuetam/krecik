import sys
from antlr4 import *
from KrecikLexer import KrecikLexer
from KrecikParser import KrecikParser
from KrecikVisitor import KrecikVisitor
from KrecikWindow import Board


class MyVisitor(KrecikVisitor):
    
    actions_list = []
    
    def __init__(self, _board : Board):
        self.board = _board
    
    def visitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        # for child in ctx.children:
        #     print(child)
        return self.visitChildren(ctx)
        
    # def visitFunctions_declarations_list(self, ctx:KrecikParser.Functions_declarations_listContext):
    #     return self.visitChildren(ctx)

    # def visitFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
    #     return self.visitChildren(ctx)
    
    # def visitBody(self, ctx:KrecikParser.BodyContext):
    #     return self.visitChildren(ctx)
	

    def visitFunction_call(self, ctx:KrecikParser.Function_callContext):
        fun_name = ctx.children[2]
        # print(fun_name)
        # value = ctx.getText()
        # for child in ctx.children:
        #     print(child)
            # pass
            
        return self.visitChildren(ctx)
    
    def visitFunction_call(self, ctx:KrecikParser.Function_callContext):
        name = ctx.VARIABLE_NAME()
        arguments = []
        if ctx.expressions_list():
            arguments = self.visit(ctx.expressions_list())
        print(arguments)
        if name == "do_predu":
            self.board.getKrecik().moveForward()
        
        return 

    def visitExpressions_list(self, ctx:KrecikParser.Expressions_listContext):
        list = [ self.visit(ctx.children[0]) ]
        if ctx.expressions_list():
            list += self.visit(ctx.expressions_list())
        return list

    def visitExpression(self, ctx:KrecikParser.ExpressionContext):
        if ctx.function_call():
            value = self.visitChildren(ctx)
            print("func:", ctx.getText())
            return value
        if ctx.literal():
            value = self.visit(ctx.children[0])
            print("lit:", value)
            return value
        return 0
    
    def visitLiteral(self, ctx:KrecikParser.LiteralContext):
        value = ctx.getText()
        if ctx.BOOLEAN_VAL() :
            return bool(value)
        if ctx.FLOAT_VAL() :
            return float(value)
        if ctx.INT_VAL() :
            return int(value)

if __name__ == "__main__":

    data = None  # InputStream(input(">>> "))
    with open("inputs/simple.krecik", "r") as file:
         data = InputStream(file.read())

    # lexer
    lexer = KrecikLexer(data)
    stream = CommonTokenStream(lexer)
    # parser
    parser = KrecikParser(stream)
    tree = parser.primary_expression()
    # evaluator
    visitor = MyVisitor()
    output = visitor.visit(tree)
    # print(output)
