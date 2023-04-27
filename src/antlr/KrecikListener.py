# Generated from src/antlr/Krecik.g4 by ANTLR 4.12.0
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .KrecikParser import KrecikParser
else:
    from KrecikParser import KrecikParser


# This class defines a complete listener for a parse tree produced by KrecikParser.
class KrecikListener(ParseTreeListener):
    # Enter a parse tree produced by KrecikParser#primary_expression.
    def enterPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        pass

    # Exit a parse tree produced by KrecikParser#primary_expression.
    def exitPrimary_expression(self, ctx: KrecikParser.Primary_expressionContext):
        pass

    # Enter a parse tree produced by KrecikParser#functions_declarations_list.
    def enterFunctions_declarations_list(
        self, ctx: KrecikParser.Functions_declarations_listContext
    ):
        pass

    # Exit a parse tree produced by KrecikParser#functions_declarations_list.
    def exitFunctions_declarations_list(self, ctx: KrecikParser.Functions_declarations_listContext):
        pass

    # Enter a parse tree produced by KrecikParser#function_declaration.
    def enterFunction_declaration(self, ctx: KrecikParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by KrecikParser#function_declaration.
    def exitFunction_declaration(self, ctx: KrecikParser.Function_declarationContext):
        pass

    # Enter a parse tree produced by KrecikParser#declaration_arg_list.
    def enterDeclaration_arg_list(self, ctx: KrecikParser.Declaration_arg_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#declaration_arg_list.
    def exitDeclaration_arg_list(self, ctx: KrecikParser.Declaration_arg_listContext):
        pass

    # Enter a parse tree produced by KrecikParser#body.
    def enterBody(self, ctx: KrecikParser.BodyContext):
        pass

    # Exit a parse tree produced by KrecikParser#body.
    def exitBody(self, ctx: KrecikParser.BodyContext):
        pass

    # Enter a parse tree produced by KrecikParser#body_items_list.
    def enterBody_items_list(self, ctx: KrecikParser.Body_items_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_items_list.
    def exitBody_items_list(self, ctx: KrecikParser.Body_items_listContext):
        pass

    # Enter a parse tree produced by KrecikParser#body_item.
    def enterBody_item(self, ctx: KrecikParser.Body_itemContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_item.
    def exitBody_item(self, ctx: KrecikParser.Body_itemContext):
        pass

    # Enter a parse tree produced by KrecikParser#body_line.
    def enterBody_line(self, ctx: KrecikParser.Body_lineContext):
        pass

    # Exit a parse tree produced by KrecikParser#body_line.
    def exitBody_line(self, ctx: KrecikParser.Body_lineContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionComparisonOperator.
    def enterExpressionComparisonOperator(
        self, ctx: KrecikParser.ExpressionComparisonOperatorContext
    ):
        pass

    # Exit a parse tree produced by KrecikParser#expressionComparisonOperator.
    def exitExpressionComparisonOperator(
        self, ctx: KrecikParser.ExpressionComparisonOperatorContext
    ):
        pass

    # Enter a parse tree produced by KrecikParser#atomExpression.
    def enterAtomExpression(self, ctx: KrecikParser.AtomExpressionContext):
        pass

    # Exit a parse tree produced by KrecikParser#atomExpression.
    def exitAtomExpression(self, ctx: KrecikParser.AtomExpressionContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionPrimaryOperator.
    def enterExpressionPrimaryOperator(self, ctx: KrecikParser.ExpressionPrimaryOperatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#expressionPrimaryOperator.
    def exitExpressionPrimaryOperator(self, ctx: KrecikParser.ExpressionPrimaryOperatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionSecondaryOperator.
    def enterExpressionSecondaryOperator(
        self, ctx: KrecikParser.ExpressionSecondaryOperatorContext
    ):
        pass

    # Exit a parse tree produced by KrecikParser#expressionSecondaryOperator.
    def exitExpressionSecondaryOperator(self, ctx: KrecikParser.ExpressionSecondaryOperatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionUnaryOperator.
    def enterExpressionUnaryOperator(self, ctx: KrecikParser.ExpressionUnaryOperatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#expressionUnaryOperator.
    def exitExpressionUnaryOperator(self, ctx: KrecikParser.ExpressionUnaryOperatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionLogicalOrOperator.
    def enterExpressionLogicalOrOperator(
        self, ctx: KrecikParser.ExpressionLogicalOrOperatorContext
    ):
        pass

    # Exit a parse tree produced by KrecikParser#expressionLogicalOrOperator.
    def exitExpressionLogicalOrOperator(self, ctx: KrecikParser.ExpressionLogicalOrOperatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressionLogicalAndOperator.
    def enterExpressionLogicalAndOperator(
        self, ctx: KrecikParser.ExpressionLogicalAndOperatorContext
    ):
        pass

    # Exit a parse tree produced by KrecikParser#expressionLogicalAndOperator.
    def exitExpressionLogicalAndOperator(
        self, ctx: KrecikParser.ExpressionLogicalAndOperatorContext
    ):
        pass

    # Enter a parse tree produced by KrecikParser#parenthesisedExpression.
    def enterParenthesisedExpression(self, ctx: KrecikParser.ParenthesisedExpressionContext):
        pass

    # Exit a parse tree produced by KrecikParser#parenthesisedExpression.
    def exitParenthesisedExpression(self, ctx: KrecikParser.ParenthesisedExpressionContext):
        pass

    # Enter a parse tree produced by KrecikParser#primary_operator.
    def enterPrimary_operator(self, ctx: KrecikParser.Primary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#primary_operator.
    def exitPrimary_operator(self, ctx: KrecikParser.Primary_operatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#secondary_operator.
    def enterSecondary_operator(self, ctx: KrecikParser.Secondary_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#secondary_operator.
    def exitSecondary_operator(self, ctx: KrecikParser.Secondary_operatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#comparison_operator.
    def enterComparison_operator(self, ctx: KrecikParser.Comparison_operatorContext):
        pass

    # Exit a parse tree produced by KrecikParser#comparison_operator.
    def exitComparison_operator(self, ctx: KrecikParser.Comparison_operatorContext):
        pass

    # Enter a parse tree produced by KrecikParser#atom.
    def enterAtom(self, ctx: KrecikParser.AtomContext):
        pass

    # Exit a parse tree produced by KrecikParser#atom.
    def exitAtom(self, ctx: KrecikParser.AtomContext):
        pass

    # Enter a parse tree produced by KrecikParser#function_call.
    def enterFunction_call(self, ctx: KrecikParser.Function_callContext):
        pass

    # Exit a parse tree produced by KrecikParser#function_call.
    def exitFunction_call(self, ctx: KrecikParser.Function_callContext):
        pass

    # Enter a parse tree produced by KrecikParser#expressions_list.
    def enterExpressions_list(self, ctx: KrecikParser.Expressions_listContext):
        pass

    # Exit a parse tree produced by KrecikParser#expressions_list.
    def exitExpressions_list(self, ctx: KrecikParser.Expressions_listContext):
        pass

    # Enter a parse tree produced by KrecikParser#vratit.
    def enterVratit(self, ctx: KrecikParser.VratitContext):
        pass

    # Exit a parse tree produced by KrecikParser#vratit.
    def exitVratit(self, ctx: KrecikParser.VratitContext):
        pass

    # Enter a parse tree produced by KrecikParser#conditional_instruction.
    def enterConditional_instruction(self, ctx: KrecikParser.Conditional_instructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#conditional_instruction.
    def exitConditional_instruction(self, ctx: KrecikParser.Conditional_instructionContext):
        pass

    # Enter a parse tree produced by KrecikParser#else_instruction.
    def enterElse_instruction(self, ctx: KrecikParser.Else_instructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#else_instruction.
    def exitElse_instruction(self, ctx: KrecikParser.Else_instructionContext):
        pass

    # Enter a parse tree produced by KrecikParser#loop_instruction.
    def enterLoop_instruction(self, ctx: KrecikParser.Loop_instructionContext):
        pass

    # Exit a parse tree produced by KrecikParser#loop_instruction.
    def exitLoop_instruction(self, ctx: KrecikParser.Loop_instructionContext):
        pass

    # Enter a parse tree produced by KrecikParser#return_var_type.
    def enterReturn_var_type(self, ctx: KrecikParser.Return_var_typeContext):
        pass

    # Exit a parse tree produced by KrecikParser#return_var_type.
    def exitReturn_var_type(self, ctx: KrecikParser.Return_var_typeContext):
        pass

    # Enter a parse tree produced by KrecikParser#var_type.
    def enterVar_type(self, ctx: KrecikParser.Var_typeContext):
        pass

    # Exit a parse tree produced by KrecikParser#var_type.
    def exitVar_type(self, ctx: KrecikParser.Var_typeContext):
        pass

    # Enter a parse tree produced by KrecikParser#declaration.
    def enterDeclaration(self, ctx: KrecikParser.DeclarationContext):
        pass

    # Exit a parse tree produced by KrecikParser#declaration.
    def exitDeclaration(self, ctx: KrecikParser.DeclarationContext):
        pass

    # Enter a parse tree produced by KrecikParser#literal.
    def enterLiteral(self, ctx: KrecikParser.LiteralContext):
        pass

    # Exit a parse tree produced by KrecikParser#literal.
    def exitLiteral(self, ctx: KrecikParser.LiteralContext):
        pass

    # Enter a parse tree produced by KrecikParser#assignment.
    def enterAssignment(self, ctx: KrecikParser.AssignmentContext):
        pass

    # Exit a parse tree produced by KrecikParser#assignment.
    def exitAssignment(self, ctx: KrecikParser.AssignmentContext):
        pass

    # Enter a parse tree produced by KrecikParser#variable.
    def enterVariable(self, ctx: KrecikParser.VariableContext):
        pass

    # Exit a parse tree produced by KrecikParser#variable.
    def exitVariable(self, ctx: KrecikParser.VariableContext):
        pass


del KrecikParser
