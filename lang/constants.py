ID = 0

INT_LITERAL = 1
STRING_LITERAL = 2
FLOAT_LITERAL = 3

KW_FN = 100
KW_RAW = 101
KW_RET = 102
KW_VAR = 103

SEMICOLON = 200
OPEN_PARAM = 201
CLOSE_PARAM = 202
OPEN_BRACE = 203
CLOSE_BRACE = 204
COMMA = 205
PLUS = 206
MINUS = 207
STAR = 208
SLASH = 209
NOT = 210
LESSER = 211
GREATER = 212
LESSER_EQUAL = 213
GREATER_EQUAL = 214
DOUBLE_EQUAL = 215
NOT_EQUAL = 216
EQUAL = 217


def find_word_type(raw_word: str) -> int:
    word_table = {
        "fn": KW_FN,
        "raw": KW_RAW,
        "ret": KW_RET,
        "var": KW_VAR
    }
    return word_table.get(raw_word, ID)


def get_constants_name(constants: int) -> str:
    # python enum sucks
    name_table = {
        0: "Identifier",
        1: "integer",
        2: "string",
        3: "float",
        100: "fn keyword",
        101: "raw keyword",
        102: "ret keyword",
        103: "var keyword",
        200: ";",
        201: "(",
        202: ")",
        203: "{",
        204: "}",
        205: "comma(,)",
        206: "plus(+)",
        207: "minus(-)",
        208: "star(*)",
        209: "slash(/)",
        210: "not(!)",
        211: "lesser(<)",
        212: "greater(>)",
        213: "lesser equals(<=)",
        214: "greater equals(>=)",
        215: "double equals(==)",
        216: "not equals(!=)",
        217: "equals(=)"
    }
    return name_table.get(constants, f"undefined(plz define id: {constants})")
