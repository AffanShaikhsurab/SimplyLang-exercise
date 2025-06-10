from typing import Any
import lexer
import parser as Pr


class ShowNode:
    def __init__(self, body, position_var):
        self.body = body


class NumberNode:
    def __init__(self, value):
        self.value = value


class VariableNode:
    def __init__(self, varible_name, value_node):
        self.variable_name = varible_name
        self.value_node = value_node


class VariableAccessNode:
    def __init__(self, varible_name_token):
        self.variable_name = varible_name_token


class UniaryOperatorNode:
    def __init__(self, op_token, node):
        self.token = op_token
        self.node = node

    def __repr__(self) -> str:
        return f"({self.token} {self.node})"


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
            if token.type in (lexer.TT_ADD, lexer.TT_MINUS):
                result.register_advance()
                self.advance()
                factor = result.register(self.factor())
                if result.error:
                    return result
                return result.success(UniaryOperatorNode(token, factor))

            elif token.type in (lexer.TT_GT, lexer.TT_LT):

                result.register_advance()
                self.advance()
                factor = result.register(self.factor())
                if result.error:
                    return result
                return result.success(UniaryOperatorNode(token, factor))
            if token.type == lexer.TT_STRING:
                result.register_advance()
                self.advance()
                return result.success(token)
            elif token.type in (lexer.TT_INT, lexer.TT_DOUBLE):
                result.register_advance()
                self.advance()
                return result.success(NumberNode(token))
            elif token.type == lexer.TT_IDENTIFIER:
                result.register_advance()
                self.advance()
                return result.success(VariableAccessNode(token))
        return None

    def bin_operation(self, function, ops):
        res = ParserResult()
        left = res.register(function())
        if res.error:
            return res
        while self.current_token is not None and self.current_token.type in ops:
            token = self.current_token
            res.register_advance()
            self.advance()
            right = res.register(function())
            if res.error:
                return res
            left = BinaryOperationNode(left, token, right)
        return res.success(left)

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

        if (
            self.current_token.type == lexer.TT_KEYWORD
            and self.current_token.value == "show"
        ):
            position_var = self.current_token

            res.register_advance()
            self.advance()
            if self.current_token.type != lexer.TT_LP:
                return res.failure("Expected '('")
            res.register_advance()
            self.advance()

            body = []

            while self.current_token.type != lexer.TT_RP:

                data = None
                if self.current_token.type == lexer.TT_STRING:
                    res.register_advance()
                    self.advance()
                    is_string = False
                    if self.current_token.type != lexer.TT_IDENTIFIER:
                        return res.failure("Expected identifier")
                    variable = self.current_token.value
                    self.advance()
                    data = variable
                    body.append(data)

                if self.current_token.type == lexer.TT_IDENTIFIER:
                    expr = res.register(self.expr(True))
                    if res.error:
                        return res.error
                    data = expr
                    body.append(data)

                if (
                    self.current_token.type != lexer.TT_RP
                    and self.current_token.type != lexer.TT_COMMA
                ):
                    return res.failure("Expected ','")

                if self.current_token.type != lexer.TT_RP:
                    self.advance()

                if self.current_token.type == lexer.TT_NEWLINE:
                    return res.failure("Expected ')'")
            res.register_advance()
            self.advance()
            return res.success(ShowNode(body, position_var))

        return self.bin_operation(
            self.term,
            (
                lexer.TT_ADD,
                lexer.TT_MINUS,
                lexer.TT_LT,
                lexer.TT_GT,
            ),
        )


def print_ast(node, indent=""):
    """
    Recursively print the AST in a hierarchical, readable format.

    Args:
    node: The current AST node
    indent: The current indentation level (string of spaces)
    """
    # Print the current node's type and any relevant attributes
    node_type = type(node).__name__
    print(f"{indent}{node_type}", end="")

    if hasattr(node, "value"):
        print(f": {node.value}", end="")
    elif hasattr(node, "token"):
        print(f": {node.token.type} '{node.token.value}'", end="")
    elif hasattr(node, "variable_name"):
        print(f": {node.variable_name}", end="")
    elif hasattr(node, "function_name"):
        print(f": {node.function_name}", end="")
    elif hasattr(node, "class_name"):
        print(f": {node.class_name}", end="")

    print()  # New line

    # Recursively print child nodes
    new_indent = indent + "  "
    if hasattr(node, "statements"):
        for stmt in node.statements:
            print_ast(stmt, new_indent)
    elif hasattr(node, "body"):
        for item in node.body:
            print_ast(item, new_indent)
    elif hasattr(node, "left"):
        print_ast(node.left, new_indent)
        print_ast(node.right, new_indent)
    elif hasattr(node, "condition_expr"):
        print(f"{new_indent}Condition:")
        print_ast(node.condition_expr, new_indent + "  ")
        print(f"{new_indent}Then:")
        for stmt in node.then_expr:
            print_ast(stmt, new_indent + "  ")
        if hasattr(node, "otherwise_expr") and node.otherwise_expr:
            print(f"{new_indent}Otherwise:")
            for stmt in node.otherwise_expr:
                print_ast(stmt, new_indent + "  ")
    elif hasattr(node, "value_node"):
        print_ast(node.value_node, new_indent)


def run(filename) -> tuple[ParserResult | None, Any]:
    tokens, error = lexer.generate(filename)
    if error == None:
        parser = Pr.Parser(tokens)
        ast: ParserResult | None = parser.parse()
        if ast is None:
            print("Error: Invalid syntax")
            return None, "Invalid syntax"
        else:
            print("AST:")
            print_ast(ast.node)
            return ast.node, ast.error
    else:
        return None, error
