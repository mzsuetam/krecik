from antlr4 import ParserRuleContext
from antlr4.tree.Tree import ParseTree, TerminalNodeImpl

from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.decorators import handle_exception
from interpreter.exceptions import KrecikNullValueUsageError
from interpreter.krecik_types.krecik_type import KrecikType


class ExpressionsVisitor(KrecikVisitor):
    # EXPRESSIONS
    @handle_exception
    def visitExpressions_list(self, ctx: KrecikParser.Expressions_listContext) -> list[KrecikType]:
        expr_list = [self.visitExpression(ctx.expression())]
        if rest := ctx.expressions_list():
            expr_list += self.visitExpressions_list(rest)
        return expr_list

    @handle_exception
    def visitExpression(self, ctx: KrecikParser.ExpressionContext) -> KrecikType:
        children = list(filter(self.is_not_empty_terminal, ctx.children))
        match children:
            case [atom_ctx]:
                return self.visitAtom(atom_ctx)

            case [bool_unary, expr] if ctx.boolean_unary_operator():
                return self.handle_boolean_unary_operator(bool_unary, expr)

            case [num_unary, expr] if ctx.numeric_unary_operator():
                return self.handle_numeric_unary_operator(num_unary, expr)

            case [left, mult_op, right] if ctx.multiplication_operator():
                return self.handle_multiplication_operator(left, mult_op, right)

            case [left, add_op, right] if ctx.addition_operator():
                return self.handle_addition_operator(left, add_op, right)

            case [left, comp_op, right] if ctx.comparison_operator():
                return self.handle_comparison_operator(left, comp_op, right)

            case [left, and_op, right] if ctx.and_operator():
                return self.handle_and_operator(left, and_op, right)

            case [left, or_op, right] if ctx.or_operator():
                return self.handle_or_operator(left, or_op, right)

            case [parentheses_start, expr, parentheses_end] if (
                parentheses_start.symbol.text == "(" and parentheses_end.symbol.text == ")"
            ):
                return self.visitExpression(expr)

        raise NotImplementedError(f"Unknown expression type. {ctx.getText()}")

    @staticmethod
    def is_not_empty_terminal(node: ParseTree) -> bool:
        if not isinstance(node, TerminalNodeImpl):
            return True
        if node.symbol.text != " ":
            return True
        return False

    def handle_boolean_unary_operator(
        self,
        boolean_unary_op_ctx: KrecikParser.Boolean_unary_operatorContext,
        expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        expression = self.get_operand(expr_ctx, boolean_unary_op_ctx)
        match self.visitBoolean_unary_operator(boolean_unary_op_ctx):
            case "ne":
                return ~expression
        raise NotImplementedError(
            f"Unknown boolean unary operator: {boolean_unary_op_ctx.getText()}",
        )

    def handle_numeric_unary_operator(
        self,
        numeric_unary_op_ctx: KrecikParser.Numeric_unary_operatorContext,
        expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        expression = self.get_operand(expr_ctx, numeric_unary_op_ctx)
        match self.visitNumeric_unary_operator(numeric_unary_op_ctx):
            case "+":
                return +expression
            case "-":
                return -expression
        raise NotImplementedError(
            f"Unknown numeric unary operator: {numeric_unary_op_ctx.getText()}",
        )

    def handle_multiplication_operator(
        self,
        left_expr_ctx: KrecikParser.ExpressionContext,
        mult_op_ctx: KrecikParser.Multiplication_operatorContext,
        right_expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        left = self.get_operand(left_expr_ctx, mult_op_ctx)
        right = self.get_operand(right_expr_ctx, mult_op_ctx)
        match self.visitMultiplication_operator(mult_op_ctx):
            case "*":
                return left * right
            case "/":
                return left / right
        raise NotImplementedError(
            f"Unknown multiplication operator: {mult_op_ctx.getText()}",
        )

    def handle_addition_operator(
        self,
        left_expr_ctx: KrecikParser.ExpressionContext,
        add_op_ctx: KrecikParser.Addition_operatorContext,
        right_expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        left = self.get_operand(left_expr_ctx, add_op_ctx)
        right = self.get_operand(right_expr_ctx, add_op_ctx)
        match self.visitAddition_operator(add_op_ctx):
            case "+":
                return left + right
            case "-":
                return left - right
        raise NotImplementedError(f"Unknown addition operator: {add_op_ctx.getText()}")

    def handle_comparison_operator(
        self,
        left_expr_ctx: KrecikParser.ExpressionContext,
        comp_op_ctx: KrecikParser.Comparison_operatorContext,
        right_expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        left = self.get_operand(left_expr_ctx, comp_op_ctx)
        right = self.get_operand(right_expr_ctx, comp_op_ctx)
        match self.visitComparison_operator(comp_op_ctx):
            case "mensi":
                return left < right
            case "wetsi":
                return left > right
            case "je":
                return left.is_equal(right)
            case "neje":
                return left.is_not_equal(right)
        raise NotImplementedError(
            f"Unknown comparison operator: {comp_op_ctx.getText()}",
        )

    def handle_and_operator(
        self,
        left_expr_ctx: KrecikParser.ExpressionContext,
        and_op_ctx: KrecikParser.And_operatorContext,
        right_expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        left = self.get_operand(left_expr_ctx, and_op_ctx)
        right = self.get_operand(right_expr_ctx, and_op_ctx)
        return left and right

    def handle_or_operator(
        self,
        left_expr_ctx: KrecikParser.ExpressionContext,
        or_op_ctx: KrecikParser.Or_operatorContext,
        right_expr_ctx: KrecikParser.ExpressionContext,
    ) -> KrecikType:
        left = self.get_operand(left_expr_ctx, or_op_ctx)
        right = self.get_operand(right_expr_ctx, or_op_ctx)
        return left or right

    def get_operand(
        self,
        operand_ctx: KrecikParser.ExpressionContext,
        operator_ctx: ParserRuleContext,
    ) -> KrecikType:
        expression = self.visitExpression(operand_ctx)
        if expression is None:
            raise KrecikNullValueUsageError(
                operand=operand_ctx.getText(),
                operation=operator_ctx.getText(),
            )
        return expression

    def visitBoolean_unary_operator(self, ctx: KrecikParser.Boolean_unary_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitNumeric_unary_operator(self, ctx: KrecikParser.Boolean_unary_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitMultiplication_operator(self, ctx: KrecikParser.Multiplication_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitAddition_operator(self, ctx: KrecikParser.Addition_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitComparison_operator(self, ctx: KrecikParser.Comparison_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitAnd_operator(self, ctx: KrecikParser.And_operatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitOr_operator(self, ctx: KrecikParser.Or_operatorContext) -> str:
        return ctx.children[0].symbol.text
