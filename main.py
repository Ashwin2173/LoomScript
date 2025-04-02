import sys

from lang.tokenizer import Lexer
from lang.utils.tokenUtils import Token, TokenIterator

from lang.parser import Parse


def print_usage(should_exit: bool) -> None:
    print("USAGE:")
    print("lscript <name>.ls")
    if should_exit:
        exit(1)


def main(args: list[str]) -> None:
    if len(args) < 2:
        print_usage(should_exit=True)

    program_path = args[1]
    raw_program = load_raw_program(program_path)
    parse(tokenize(raw_program))


def load_raw_program(program_path: str) -> str:
    try:
        with open(program_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Error : file not found")
        exit(1)
    except Exception as err:
        print("Internal Error: Unhandled Exception during loading the file")
        print(f"Error Message: {err}")
        exit(1)


def tokenize(raw_program: str) -> list[Token]:
    lexer = Lexer(raw_program)
    return lexer.tokenize()


def parse(tokens: list[Token]) -> None:
    tokens_iterator = TokenIterator(tokens)
    parser = Parse(tokens_iterator)
    tree = parser.parse()
    print(tree)


if __name__ == "__main__":
    main(sys.argv)
