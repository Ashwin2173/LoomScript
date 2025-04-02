from lang.exception import LoomSyntaxError

from lang.constants import get_constants_name


class Token:  # Token POPO
    def __init__(self, raw: str, token_type: int, line: int) -> None:
        self.raw = raw
        self.token_type = token_type
        self.line = line

    def get_raw(self) -> str:
        return self.raw

    def get_type(self) -> int:
        return self.token_type

    def get_line(self) -> int:
        return self.line

    def is_of_type(self, *token_type: int) -> bool:
        return self.token_type in token_type


class TokenIterator:
    def __init__(self, tokens: list[Token]) -> None:
        self.pointer = 0
        self.tokens = tokens
        self.length = len(tokens)

    def get(self, offset: int = 0) -> Token | None:
        if self.pointer + offset < self.length:
            return self.tokens[self.pointer + offset]
        return None

    def move(self, offset: int = 1) -> None:
        if self.pointer + offset < self.length:
            self.pointer += offset
        else:
            self.pointer = self.length

    def expect_consume(self, offset: int = 1, *expected_type: int) -> Token:
        token = self.get()
        if token.get_type() not in expected_type:
            types = list(map(get_constants_name, expected_type))
            raise LoomSyntaxError(f"expected {'or'.join(types)}, but got {token.get_raw()}", token.get_line())
        self.move(offset)
        return token

    def move_expect(self, offset: int = 1, *expected_type: int) -> Token:
        self.move(offset)
        token = self.get()
        if token is None or token.get_type() not in expected_type:
            expected_names = list(map(get_constants_name, expected_type))
            got_string = token.get_raw() if token is not None else 'nothing'
            raise LoomSyntaxError(
                f"expected {'or'.join(expected_names)}, but got {got_string}",
                token.get_line() if token is not None else None
            )
        return token

    def has_token(self) -> bool:
        return self.pointer < self.length


def is_valid_identifier_beginner(char: str) -> bool:
    return char in "abcdefghijklmnopqrstuvwxyz_"


def is_valid_identifier_char(char: str) -> bool:
    return char in "abcdefghijklmnopqrstuvwxyz_1234567890"
