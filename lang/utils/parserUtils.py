class Program:
    def __init__(self) -> None:
        self.version: str = "v1"
        self.body: list[Statement] = list()


class Statement:
    def __init__(self, line: int) -> None:
        self.line = line


class Expression:
    def __init__(self, line: int) -> None:
        self.line = line


class Identifier(Expression):
    def __init__(self, name: str, line: int) -> None:
        super().__init__(line)
        self.name = name


class IntLiteral(Expression):
    def __init__(self, value: int, line: int) -> None:
        super().__init__(line)
        self.value = value


class StringLiteral(Expression):
    def __init__(self, value: str, line: int) -> None:
        super().__init__(line)
        self.value = value


class UnaryExpression(Expression):
    def __init__(self, operator: int, expression: Expression, line: int) -> None:
        super().__init__(line)
        self.operator = operator
        self.expression = expression


class BinaryExpression(Expression):
    def __init__(self, left_expression: Expression, operator: int, right_expression: Expression, line: int) -> None:
        super().__init__(line)
        self.left = left_expression
        self.operator = operator
        self.right = right_expression


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression, line) -> None:
        super().__init__(line)
        self.expression = expression


class FunctionDeclaration(Statement):
    def __init__(self, name: str, params: list[Identifier], body: list[Statement], line: int) -> None:
        super().__init__(line)
        self.name = name
        self.param = params
        self.body = body


class ReturnStatement(Statement):
    def __init__(self, expression: ExpressionStatement, line: int) -> None:
        super().__init__(line)
        self.expression = expression


class VariableDeclaration(Statement):
    def __init__(self, identifier: Identifier, init: ExpressionStatement, line: int) -> None:
        super().__init__(line)
        self.identifier = identifier
        self.init = init


class RawCodeStatement(Statement):
    def __init__(self, code: int, params: list[any], line: int) -> None:
        super().__init__(line)
        self.code = code
        self.params = params


class Trace:
    def __init__(self, block_name: str, line: int) -> None:
        self.block_name = block_name
        self.line = line
        self.variable: list[Variable] = list()


class Variable:
    def __init__(self, name: str, variable_type: int):
        self.name = name
        self.variable_type = variable_type
