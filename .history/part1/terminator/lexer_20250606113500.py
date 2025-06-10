import string

# Token types
TT_KEYWORD = "KEYWORD"
TT_STRING = "STRING"
TT_LP = "LP"  # Left parentheses
TT_RP = "RP"  # Right parentheses
TT_EOF = "EOF"
TT_COMMA = "COMMA"
TT_NEWLINE = "NEWLINE"
TT_ADD = "ADD"
TT_COMMA = "COMMA"
TT_GT = "GT"
TT_LT = "LT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT
TT_DIV = "DIV"
TT_INT = "INT"
TT_DOUBLE = "DOUBLE"
TT_NUMBER = "NUMBER"
TT_IDENTIFIER = "IDENTIFIER"
# Constants
LETTERS = string.ascii_letters
DIGITS = "0123456789"
LETTER_DIGITS = LETTERS + DIGITS

# Keywords
KEYWORDS = {
    "show": TT_KEYWORD,
    "is": TT_KEYWORD,
}


class Token:
    def __init__(self, type, value=None, start=None, end=None):
        self.type = type
        self.value = value

    def matches(self, type, value):
        return self.type == type and self.value == value

    def __repr__(self) -> str:
        return f"{self.value , self.type}"


class Position:
    def __init__(self, index, line, col, filename, text):
        self.index = index
        self.line = line
        self.col = col
        self.filename = filename
        self.text = text

    def copy(self):
        return Position(self.index, self.line, self.col, self.filename, self.text)


class Lex:
    def __init__(self, text, filename):
        self.text = text
        self.pos = Position(0, 1, 0, filename, text)
        self.current = None
        self.tokens = []
        self.filename = filename
        self.iterate()

    def iterate(self):
        self.pos.index += 1
        self.pos.col += 1
        self.current = (
            self.text[self.pos.index - 1] if self.pos.index <= len(self.text) else None
        )

    def create_token(self):
        while self.current is not None:
            if self.current in " \t":
                self.iterate()
            elif self.current == "\n":
                self.tokens.append(Token(TT_NEWLINE, "\n", start=self.pos))
                self.iterate()
            elif self.current == "(":
                self.tokens.append(Token(TT_LP, "(", start=self.pos))
                self.iterate()
            elif self.current == ")":
                self.tokens.append(Token(TT_RP, ")", start=self.pos))
                self.iterate()
            elif self.current == ",":
                self.tokens.append(Token(TT_COMMA, ",", start=self.pos))
                self.iterate()
            elif self.current == "+":
                self.tokens.append(Token(TT_PLUS, "+", start=self.pos))
                self.iterate()
            elif self.current == "-":
                self.tokens.append(Token(TT_MINUS, "-", start=self.pos))
                self.iterate()
            elif self.current == "*":
                self.tokens.append(Token(TT_MUL, "*", start=self.pos))
                self.iterate()
            elif self.current == "/":
                self.tokens.append(Token(TT_DIV, "/", start=self.pos))
                self.iterate()
            elif self.current in DIGITS:
                self.tokens.append(self.create_number())
            elif self.current == '"':
                self.tokens.append(self.create_string())
            elif self.current in LETTERS:
                self.tokens.append(self.make_identifier())
            elif self.current == ".":
                # Handle the dot at the end of statements
                self.iterate()
            else:
                # Skip any other characters for now
                self.iterate()

        self.tokens.append(Token(TT_EOF, TT_EOF, start=self.pos))
        return self.tokens, None

    def create_string(self):

        string = ""
        pos_start = self.pos.copy()

        # Skip the opening quote
        self.iterate()

        while self.current is not None and self.current != '"':
            string += self.current
            self.iterate()

        # Skip the closing quote
        if self.current == '"':
            self.iterate()

        return Token(TT_STRING, string, pos_start, self.pos)

    def create_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current is not None and (
            self.current.isdigit() or self.current == "."
        ):
            if self.current == ".":
                dot_count += 1
                if dot_count > 1:
                    break
            num_str += self.current
            self.iterate()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_DOUBLE, float(num_str))

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current is not None and (self.current in LETTER_DIGITS + "_"):
            id_str += self.current
            self.iterate()

        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str, pos_start, self.pos)
        else:
            return Token(TT_IDENTIFIER, id_str, pos_start, self.pos)

    def make_number(self):
        num_str = ""
        pos_start = self.pos.copy()
        dot_count = 0

        while self.current is not None and (self.current in DIGITS + "."):
            if self.current == ".":
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.current
            self.iterate()

        if dot_count == 0:
            return Token(TT_NUMBER, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_NUMBER, float(num_str), pos_start, self.pos)


def generate(filename):
    with open(filename) as f:
        text = f.read()
    lexer = Lex(text, filename)
    tokens, error = lexer.create_token()
    print(f"Tokens: {tokens}")
    return tokens, error
