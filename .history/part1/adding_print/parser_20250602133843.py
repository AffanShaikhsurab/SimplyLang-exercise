from typing import Any
import lexer


class ShowNode:
    def __init__(self, body, position_var):
        self.body = body


class NumberNode:
    def __init__(self, value, position_var):
        self.value = value


class BinaryOperationNode:
    def __init__(self, left, op, right):
        self.left = left
        self.operator = op
        self.right = right


class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advance(self):
        self.advance_count += 1

    def register(self, res):
        if res != None:
            try:
                self.advance_count += res.advance_count
                if res.error:
                    self.error = res.error
                return res.node
            except:
                return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
            return self


class Praser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.variables = []
        self.advance()

    def advance(self):
        self.index += 1
        self.current_token = (
            self.tokens[self.index] if self.index < len(self.tokens) else None
        )

    def parse(self):
        res = ParserResult()
        expr = res.register(self.expr())
        if res.error:
            return res
        return res.success(expr)

    def factor(self):
        result = ParserResult()
        token = self.current_token

        if token != None:
            if token.type == lexer.TT_STRING:
                result.register_advance()
                self.advance()
                return result.success(token)

        return None

    def term(self):
        return (
            self.factor()
        )  # Simplified since we only need to handle strings    def skip_newlines(self, res):
        # Helper method to skip over newlines

    def expr(self, seen=False):
        res = ParserResult()

        # Check if we have a show statement
        if (
            self.current_token is not None
            and self.current_token.type == lexer.TT_KEYWORD
            and self.current_token.value == "show"
        ):
            position_var = self.current_token

            res.register_advance()
            self.advance()

            # Make sure there's an opening parenthesis
            if (
                self.current_token is not None
                and self.current_token.type != lexer.TT_LP
            ):
                return res.failure("Expected '('")

            res.register_advance()
            self.advance()

            body = []

            # Process everything inside the parentheses
            while (
                self.current_token is not None
                and self.current_token.type != lexer.TT_RP
            ):
                # For now, we only handle string literals in our show statement
                if self.current_token.type == lexer.TT_STRING:
                    string_value = self.current_token.value
                    body.append(string_value)
                    res.register_advance()
                    self.advance()

                # Check for closing parenthesis
                if (
                    self.current_token is not None
                    and self.current_token.type == lexer.TT_RP
                ):
                    break

                # Error if we encounter unexpected token
                if self.current_token is None:
                    return res.failure("Expected ')'")

            # Consume the closing parenthesis
            if self.current_token is None:
                return res.failure("Expected ')'")

            res.register_advance()
            self.advance()

            return res.success(ShowNode(body, position_var))

        return res.failure("Invalid syntax")


def run(filename):
    tokens, error = lexer.generate(filename)
    if error == None:
        parser = Praser(tokens)
        ast = parser.parse()
        return ast.node, ast.error
    else:
        return None, error


