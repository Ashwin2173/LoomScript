from lang import constants
from lang.exception import LoomSyntaxError
from lang.utils.tokenUtils import Token, is_valid_identifier_beginner, is_valid_identifier_char


class Lexer:
    def __init__(self, program: str) -> None:
        self.index = -1
        self.line = 1
        self.program = program + "\n"
        self.tokens: list[Token] = list()
        self.length = len(program)

    def tokenize(self) -> list[Token]:
        while not self.__is_eof():
            char = self.__next()
            if char.isspace():
                self.__skip_space()
            elif char == r'\n':
                self.line += 1
            elif is_valid_identifier_beginner(char):
                word = self.__tokenize_word()
                self.__make_token(word, constants.find_word_type(word))
            elif char.isnumeric():
                integer = self.__tokenize_number()
                if self.__peek() == '.':  # checking if the current integer is a float
                    self.__next()
                    decimal = self.__tokenize_number()
                    self.__make_token(integer + "." + decimal, constants.FLOAT_LITERAL)
                    continue
                self.__make_token(integer, constants.INT_LITERAL)
            elif char == '"' or char == "'":
                self.__make_token(self.__tokenize_string(), constants.STRING_LITERAL)
            elif char == '.':
                self.__make_token(self.__tokenize_string(), constants.DOT)
            elif char == '(':
                self.__make_token('(', constants.OPEN_PARAM)
            elif char == ')':
                self.__make_token(')', constants.CLOSE_PARAM)
            elif char == '{':
                self.__make_token('{', constants.OPEN_BRACE)
            elif char == '}':
                self.__make_token('}', constants.CLOSE_BRACE)
            elif char == ';':
                self.__make_token(';', constants.SEMICOLON)
            elif char == ',':
                self.__make_token(',', constants.COMMA)
            elif char == '+':
                self.__make_token('+', constants.PLUS)
            elif char == '-':
                self.__make_token('-', constants.MINUS)
            elif char == '*':
                self.__make_token('*', constants.STAR)
            elif char == '/':
                self.__make_token('/', constants.SLASH)
            elif char == '!':
                if self.__peek(1) == '=':
                    self.__next()
                    self.__make_token('!=', constants.NOT_EQUAL)
                else:
                    self.__make_token('!', constants.NOT)
            elif char == '=':
                if self.__peek(1) == '=':
                    self.__make_token('==', constants.DOUBLE_EQUAL)
                    self.__next()
                else:
                    self.__make_token('=', constants.EQUAL)
            elif char == '>':
                if self.__peek(1) == '=':
                    self.__make_token('>=', constants.GREATER_EQUAL)
                    self.__next()
                else:
                    self.__make_token('>', constants.GREATER)
            elif char == '<':
                if self.__peek(1) == '=':
                    self.__next()
                    self.__make_token('<=', constants.LESSER_EQUAL)
                else:
                    self.__make_token('<', constants.LESSER)
            else:
                raise LoomSyntaxError(f"Invalid character '{char}'", self.line)
        return self.tokens

    def __tokenize_string(self) -> str:
        start_index = self.index
        while not self.__is_eof() and self.__next() != self.program[start_index]:
            if self.__peek() == '\n':
                self.line += 1
        return self.program[start_index + 1: self.index]

    def __tokenize_number(self) -> str:
        start_index = self.index
        while not self.__is_eof() and self.__next().isnumeric():
            continue
        number = self.program[start_index: self.index]
        self.__step_back()
        return number

    def __tokenize_word(self) -> str:
        start_index = self.index
        while not self.__is_eof() and is_valid_identifier_char(self.__next()):
            if self.__peek() == '\n':
                self.line += 1
        word = self.program[start_index: self.index]
        self.index -= 1
        return word

    def __skip_space(self) -> None:
        while not self.__is_eof():
            if not self.__next().isspace():
                self.__step_back()
                return

    def __make_token(self, raw: str, token_type: int) -> None:
        self.tokens.append(Token(raw, token_type, self.line))

    def __next(self) -> str:
        self.index += 1
        return self.program[self.index]

    def __peek(self, offset: int = 1) -> str | None:
        if self.index + offset >= self.length - 1:
            return None
        return self.program[self.index + offset]

    def __step_back(self, offset: int = 1) -> None:
        if self.index - offset >= 0:
            self.index -= offset
        else:
            self.index = 0

    def __is_eof(self) -> bool:
        return not (self.index < self.length)
