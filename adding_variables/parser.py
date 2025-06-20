from typing import Any
import lexer
import parser as Pr


class ShowNode:
    def __init__(self, body, position_var):
        self.body = body


class NumberNode:
    def __init__(self, value, position_var):
        self.value = value


class VariableNode:
    def __init__(self, varible_name, value_node):
        self.variable_name = varible_name
        self.value_node = value_node


class BinaryOperationNode:
    def __init__(self, left, op, right):
        self.left = left
        self.operator = op
        self.right = right


class StatementsNode:
    def __init__(self, statements):
        self.statements = statements


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


class Parser:
    def __init__(self, tokens: list[lexer.Token]):
        self.tokens: list[lexer.Token] = tokens
        self.current_token: lexer.Token | None = None
        self.index: int = -1
        self.variables: list[str] = []
        self.advance()

    def advance(self):
        self.index += 1
        self.current_token = (
            self.tokens[self.index] if self.index < len(self.tokens) else None
        )

    def parse(self):
        res = ParserResult()
        statements = []

        while self.current_token != None and self.current_token.type != lexer.TT_EOF:
            if self.current_token.type == lexer.TT_NEWLINE:
                res.register_advance()
                self.advance()
                continue

            stmt = res.register(self.expr())
            if res.error:
                return res
            statements.append(stmt)

            if self.current_token != None and self.current_token.type not in (
                lexer.TT_NEWLINE,
                lexer.TT_EOF,
            ):
                return None
        return res.success(StatementsNode(statements))

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
        if self.current_token is None:
            return res.failure("Expected an expression")

        if not seen and self.current_token.type == lexer.TT_IDENTIFIER:
            # Store the variable name token
            variable_token = self.current_token

            res.register_advance()
            self.advance()

            # Check if next token is 'is' keyword
            if (
                self.current_token.type != lexer.TT_KEYWORD
                and self.current_token.value != "is"
            ):
                return res.failure("Expected 'is' keyword after identifier")

            res.register_advance()
            self.advance()

            # Handle the expression (either a direct value or a complex expression)
            if self.current_token.type in (
                lexer.TT_STRING,
                lexer.TT_NUMBER,
            ):
                print(f"Variable created: {variable_token.value} ")
                # Direct value assignment
                expression = self.current_token
                res.register_advance()
                self.advance()

                # Store variable in our tracking list
                if expression.value is not None:
                    self.variables.append(str(variable_token.value))
                print(f"Variable created: {variable_token.value} = {expression.value}")

                return res.success(VariableNode(variable_token, expression))
            else:
                # Complex expression
                expression = res.register(self.expr(True))
                if res.error:
                    return res
                # Store variable in our tracking list
                if variable_token.value is not None:
                    self.variables.append(str(variable_token.value))
                print(
                    f"Variable created: {variable_token.value} with complex expression"
                )

                return res.success(VariableNode(variable_token, expression))

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


def run(filename) -> tuple[ParserResult | None, Any]:
    tokens, error = lexer.generate(filename)
    if error == None:
        parser = Pr.Parser(tokens)
        ast: ParserResult | None = parser.parse()
        if ast is None:
            print("Error: Invalid syntax")
            return None, "Invalid syntax"
        else:
            print("AST:", ast.node)
            return ast.node, ast.error
    else:
        return None, error
