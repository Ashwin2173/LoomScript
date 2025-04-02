from lang import constants

from lang.utils.tokenUtils import Token, TokenIterator
from lang.utils.parserUtils import (Program,
                                    Statement,
                                    Expression,
                                    Identifier,
                                    IntLiteral,
                                    StringLiteral,
                                    UnaryExpression,
                                    ReturnStatement,
                                    BinaryExpression,
                                    FunctionDeclaration,
                                    ExpressionStatement,
                                    Trace)

from lang.exception import LoomSyntaxError


class Parse:
    def __init__(self, tokens: TokenIterator) -> None:
        self.tokens = tokens
        self.stack_trace: list[Trace] = [Trace("global", 1)]

    def parse(self) -> Program:
        program = Program()
        program.body = self.parse_statements()
        return program

    def parse_statements(self) -> list[Statement]:
        statements: list[Statement] = list()
        while self.tokens.has_token():
            tokens = self.tokens.get()
            if tokens.is_of_type(constants.KW_FN):
                if len(self.stack_trace) != 1:
                    raise LoomSyntaxError("function declaration inside another method or sub-block is not allowed")
                statements.append(self.parse_function())
            elif tokens.is_of_type(constants.CLOSE_BRACE):
                self.stack_trace.pop()
                return statements
            elif tokens.is_of_type(constants.KW_RET):
                statements.append(self.parse_return())
            else:
                statements.append(self.parse_expression())
                self.tokens.expect_consume(1, constants.SEMICOLON)
        return statements

    def parse_return(self) -> Statement:
        token = self.tokens.get()
        self.tokens.expect_consume(1, constants.KW_RET)
        return_statement = ReturnStatement(self.parse_expression(), token.get_line())
        self.tokens.expect_consume(1, constants.SEMICOLON)
        return return_statement

    def parse_function(self) -> Statement:
        name: Token = self.tokens.move_expect(1, constants.ID)
        self.stack_trace.append(Trace(name.get_raw(), name.get_line()))     # adding to the stack trace
        self.tokens.move_expect(1, constants.OPEN_PARAM)
        self.tokens.move()
        params: list[Identifier] = self.parse_params()
        self.tokens.expect_consume(1, constants.CLOSE_PARAM)
        self.tokens.expect_consume(1, constants.OPEN_BRACE)
        body: list[Statement] = self.parse_statements()
        self.tokens.expect_consume(1, constants.CLOSE_BRACE)
        return FunctionDeclaration(name.get_raw(), params, body, name.get_line())

    def parse_params(self) -> list[Identifier]:
        name_set = set()
        params: list[Identifier] = list()
        if self.tokens.has_token() and self.tokens.get().is_of_type(constants.CLOSE_PARAM):     # no arg functions
            return params
        while self.tokens.has_token():
            token = self.tokens.expect_consume(1, constants.ID)
            name = token.get_raw()
            if name in name_set:    # todo: make it scoped by add it to stack_trace
                raise LoomSyntaxError(f"re-usage of argument name '{name}'")
            else:
                name_set.add(name)
            params.append(Identifier(token.get_raw(), token.get_line()))
            if self.tokens.get().is_of_type(constants.CLOSE_PARAM):
                break
            self.tokens.expect_consume(1, constants.COMMA)
        return params

    def parse_expression(self) -> ExpressionStatement:
        expression = self.equality()
        return ExpressionStatement(expression, expression.line)

    def equality(self) -> Expression:
        left_expression: Expression = self.comparison()
        while self.tokens.has_token() and self.tokens.get().is_of_type(constants.DOUBLE_EQUAL, constants.NOT_EQUAL):
            self.tokens.move()
            operator: Token = self.tokens.get()
            right_expression: Expression = self.comparison()
            left_expression = BinaryExpression(
                left_expression,
                operator.get_type(),
                right_expression,
                operator.get_line())
        return left_expression

    def comparison(self) -> Expression:
        left_expression: Expression = self.term()
        while self.tokens.has_token() and self.tokens.get().is_of_type(constants.LESSER, constants.GREATER,
                                                                       constants.LESSER_EQUAL, constants.GREATER_EQUAL):
            operator: Token = self.tokens.get()
            self.tokens.move()
            right_expression: Expression = self.term()
            left_expression = BinaryExpression(
                left_expression,
                operator.get_type(),
                right_expression,
                operator.get_line())
        return left_expression

    def term(self) -> Expression:
        left_expression: Expression = self.factor()
        while self.tokens.has_token() and self.tokens.get().is_of_type(constants.PLUS, constants.MINUS):
            operator: Token = self.tokens.get()
            self.tokens.move()
            right_expression: Expression = self.factor()
            left_expression = BinaryExpression(
                left_expression,
                operator.get_type(),
                right_expression,
                operator.get_line())
        return left_expression

    def factor(self) -> Expression:
        left_expression: Expression = self.unary()
        while self.tokens.has_token() and self.tokens.get().is_of_type(constants.STAR, constants.SLASH):
            operator: Token = self.tokens.get()
            self.tokens.move()
            right_expression: Expression = self.unary()
            left_expression = BinaryExpression(
                left_expression,
                operator.get_type(),
                right_expression,
                operator.get_line())
        return left_expression

    def unary(self) -> Expression:
        if self.tokens.has_token():
            token = self.tokens.get()
            if token.is_of_type(constants.NOT, constants.MINUS):
                right_expression: Expression = self.unary()
                return UnaryExpression(token.get_type(), right_expression, token.get_line())
        return self.primary()

    def primary(self) -> Expression:
        if not self.tokens.has_token():
            raise LoomSyntaxError("Invalid expression", self.tokens.get(-1).get_line())
        token = self.tokens.get()
        if token.is_of_type(constants.INT_LITERAL):
            value: int = int(token.get_raw())
            self.tokens.move()
            return IntLiteral(value, token.get_line())
        elif token.is_of_type(constants.STRING_LITERAL):
            value: str = token.get_raw()
            self.tokens.move()
            return StringLiteral(value, token.get_line())
        elif token.is_of_type(constants.ID):
            name: str = token.get_raw()
            self.tokens.move()
            return Identifier(name, token.get_line())
        raise LoomSyntaxError(f"Invalid literal '{self.tokens.get().get_raw()}'")
