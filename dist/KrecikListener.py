# Generated from Krecik.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .KrecikParser import KrecikParser
else:
    from KrecikParser import KrecikParser

# This class defines a complete listener for a parse tree produced by KrecikParser.
class KrecikListener(ParseTreeListener):

    # Enter a parse tree produced by KrecikParser#primary_expression.
    def enterPrimary_expression(self, ctx:KrecikParser.Primary_expressionContext):
        pass

    # Exit a parse tree produced by KrecikParser#primary_expression.
    def exitPrimary_expression(self, ctx:KrecikParser.Primary_expressionContext):
        pass


    # Enter a parse tree produced by KrecikParser#functions_declarations_list.
    def enterFunctions_declarations_list(self, ctx:KrecikParser.Functions_declarations_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#functions_declarations_list.
    def exitFunctions_declarations_list(self, ctx:KrecikParser.Functions_declarations_listContext):
        pass


    # Enter a parse tree produced by KrecikParser#function_declaration.
    def enterFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by KrecikParser#function_declaration.
    def exitFunction_declaration(self, ctx:KrecikParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by KrecikParser#declaration_arg_list.
    def enterDeclaration_arg_list(self, ctx:KrecikParser.Declaration_arg_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#declaration_arg_list.
    def exitDeclaration_arg_list(self, ctx:KrecikParser.Declaration_arg_listContext):
        pass


    # Enter a parse tree produced by KrecikParser#body.
    def enterBody(self, ctx:KrecikParser.BodyContext):
        pass

    # Exit a parse tree produced by KrecikParser#body.
    def exitBody(self, ctx:KrecikParser.BodyContext):
        pass


    # Enter a parse tree produced by KrecikParser#body_items_list.
    def enterBody_items_list(self, ctx:KrecikParser.Body_items_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_items_list.
    def exitBody_items_list(self, ctx:KrecikParser.Body_items_listContext):
        pass


    # Enter a parse tree produced by KrecikParser#body_item.
    def enterBody_item(self, ctx:KrecikParser.Body_itemContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_item.
    def exitBody_item(self, ctx:KrecikParser.Body_itemContext):
        pass


    # Enter a parse tree produced by KrecikParser#body_line.
    def enterBody_line(self, ctx:KrecikParser.Body_lineContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_line.
    def exitBody_line(self, ctx:KrecikParser.Body_lineContext):
        pass


    # Enter a parse tree produced by KrecikParser#expression.
    def enterExpression(self, ctx:KrecikParser.ExpressionContext):
        pass

    # Exit a parse tree produced by KrecikParser#expression.
    def exitExpression(self, ctx:KrecikParser.ExpressionContext):
        pass


    # Enter a parse tree produced by KrecikParser#function_call.
    def enterFunction_call(self, ctx:KrecikParser.Function_callContext):
        pass

    # Exit a parse tree produced by KrecikParser#function_call.
    def exitFunction_call(self, ctx:KrecikParser.Function_callContext):
        pass


    # Enter a parse tree produced by KrecikParser#expressions_list.
    def enterExpressions_list(self, ctx:KrecikParser.Expressions_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#expressions_list.
    def exitExpressions_list(self, ctx:KrecikParser.Expressions_listContext):
        pass


    # Enter a parse tree produced by KrecikParser#vratit.
    def enterVratit(self, ctx:KrecikParser.VratitContext):
        pass

    # Exit a parse tree produced by KrecikParser#vratit.
    def exitVratit(self, ctx:KrecikParser.VratitContext):
        pass


    # Enter a parse tree produced by KrecikParser#conditional_instruction.
    def enterConditional_instruction(self, ctx:KrecikParser.Conditional_instructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#conditional_instruction.
    def exitConditional_instruction(self, ctx:KrecikParser.Conditional_instructionContext):
        pass


    # Enter a parse tree produced by KrecikParser#loop_instruction.
    def enterLoop_instruction(self, ctx:KrecikParser.Loop_instructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#loop_instruction.
    def exitLoop_instruction(self, ctx:KrecikParser.Loop_instructionContext):
        pass


    # Enter a parse tree produced by KrecikParser#instruction.
    def enterInstruction(self, ctx:KrecikParser.InstructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#instruction.
    def exitInstruction(self, ctx:KrecikParser.InstructionContext):
        pass


    # Enter a parse tree produced by KrecikParser#unary_operator.
    def enterUnary_operator(self, ctx:KrecikParser.Unary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#unary_operator.
    def exitUnary_operator(self, ctx:KrecikParser.Unary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#binary_operator.
    def enterBinary_operator(self, ctx:KrecikParser.Binary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#binary_operator.
    def exitBinary_operator(self, ctx:KrecikParser.Binary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#numeric_unary_operator.
    def enterNumeric_unary_operator(self, ctx:KrecikParser.Numeric_unary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#numeric_unary_operator.
    def exitNumeric_unary_operator(self, ctx:KrecikParser.Numeric_unary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#numeric_binary_operator.
    def enterNumeric_binary_operator(self, ctx:KrecikParser.Numeric_binary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#numeric_binary_operator.
    def exitNumeric_binary_operator(self, ctx:KrecikParser.Numeric_binary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#boolean_unary_operator.
    def enterBoolean_unary_operator(self, ctx:KrecikParser.Boolean_unary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#boolean_unary_operator.
    def exitBoolean_unary_operator(self, ctx:KrecikParser.Boolean_unary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#boolean_binary_operator.
    def enterBoolean_binary_operator(self, ctx:KrecikParser.Boolean_binary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#boolean_binary_operator.
    def exitBoolean_binary_operator(self, ctx:KrecikParser.Boolean_binary_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#comparison_operator.
    def enterComparison_operator(self, ctx:KrecikParser.Comparison_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#comparison_operator.
    def exitComparison_operator(self, ctx:KrecikParser.Comparison_operatorContext):
        pass


    # Enter a parse tree produced by KrecikParser#return_var_type.
    def enterReturn_var_type(self, ctx:KrecikParser.Return_var_typeContext):
        pass

    # Exit a parse tree produced by KrecikParser#return_var_type.
    def exitReturn_var_type(self, ctx:KrecikParser.Return_var_typeContext):
        pass


    # Enter a parse tree produced by KrecikParser#var_type.
    def enterVar_type(self, ctx:KrecikParser.Var_typeContext):
        pass

    # Exit a parse tree produced by KrecikParser#var_type.
    def exitVar_type(self, ctx:KrecikParser.Var_typeContext):
        pass


    # Enter a parse tree produced by KrecikParser#declaration.
    def enterDeclaration(self, ctx:KrecikParser.DeclarationContext):
        pass

    # Exit a parse tree produced by KrecikParser#declaration.
    def exitDeclaration(self, ctx:KrecikParser.DeclarationContext):
        pass


    # Enter a parse tree produced by KrecikParser#literal.
    def enterLiteral(self, ctx:KrecikParser.LiteralContext):
        pass

    # Exit a parse tree produced by KrecikParser#literal.
    def exitLiteral(self, ctx:KrecikParser.LiteralContext):
        pass


    # Enter a parse tree produced by KrecikParser#assignment.
    def enterAssignment(self, ctx:KrecikParser.AssignmentContext):
        pass

    # Exit a parse tree produced by KrecikParser#assignment.
    def exitAssignment(self, ctx:KrecikParser.AssignmentContext):
        pass


    # Enter a parse tree produced by KrecikParser#variable.
    def enterVariable(self, ctx:KrecikParser.VariableContext):
        pass

    # Exit a parse tree produced by KrecikParser#variable.
    def exitVariable(self, ctx:KrecikParser.VariableContext):
        pass



del KrecikParser