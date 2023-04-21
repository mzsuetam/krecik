# Generated from C:/Users/Tomasz/Documents/GitHub/krecik/src/antlr\Krecik.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .KrecikParser import KrecikParser
else:
    from KrecikParser import KrecikParser

# This class defines a complete generic visitor for a parse tree produced by KrecikParser.

class KrecikVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by KrecikParser#primary_expression.
    def visitPrimary_expression(self, ctx:KrecikParser.Primary_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#functions_declarations_list.
    def visitFunctions_declarations_list(self, ctx:KrecikParser.Functions_declarations_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#function_declaration.
    def visitFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#declaration_arg_list.
    def visitDeclaration_arg_list(self, ctx:KrecikParser.Declaration_arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#body.
    def visitBody(self, ctx:KrecikParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#body_items_list.
    def visitBody_items_list(self, ctx:KrecikParser.Body_items_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#body_item.
    def visitBody_item(self, ctx:KrecikParser.Body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#body_line.
    def visitBody_line(self, ctx:KrecikParser.Body_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#expression.
    def visitExpression(self, ctx:KrecikParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#product.
    def visitProduct(self, ctx:KrecikParser.ProductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#function_call.
    def visitFunction_call(self, ctx:KrecikParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#expressions_list.
    def visitExpressions_list(self, ctx:KrecikParser.Expressions_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#vratit.
    def visitVratit(self, ctx:KrecikParser.VratitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#conditional_instruction.
    def visitConditional_instruction(self, ctx:KrecikParser.Conditional_instructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#else_instruction.
    def visitElse_instruction(self, ctx:KrecikParser.Else_instructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#loop_instruction.
    def visitLoop_instruction(self, ctx:KrecikParser.Loop_instructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#unary_operator.
    def visitUnary_operator(self, ctx:KrecikParser.Unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#binary_operator.
    def visitBinary_operator(self, ctx:KrecikParser.Binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#numeric_unary_operator.
    def visitNumeric_unary_operator(self, ctx:KrecikParser.Numeric_unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#numeric_binary_operator.
    def visitNumeric_binary_operator(self, ctx:KrecikParser.Numeric_binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#boolean_unary_operator.
    def visitBoolean_unary_operator(self, ctx:KrecikParser.Boolean_unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#boolean_binary_operator.
    def visitBoolean_binary_operator(self, ctx:KrecikParser.Boolean_binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#comparison_operator.
    def visitComparison_operator(self, ctx:KrecikParser.Comparison_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#return_var_type.
    def visitReturn_var_type(self, ctx:KrecikParser.Return_var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#var_type.
    def visitVar_type(self, ctx:KrecikParser.Var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#declaration.
    def visitDeclaration(self, ctx:KrecikParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#literal.
    def visitLiteral(self, ctx:KrecikParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#assignment.
    def visitAssignment(self, ctx:KrecikParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KrecikParser#variable.
    def visitVariable(self, ctx:KrecikParser.VariableContext):
        return self.visitChildren(ctx)



del KrecikParser