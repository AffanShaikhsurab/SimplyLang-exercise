from typing import Any
import lexer
import parser as Pr


class ShowNode:
    def __init__(self, body, position_var):
        self.body = body
        self.pos_start = position_var.start
        self.pos_end = position_var.end
class ReturnExprNode:
    def __init__(self, token, pos_token):
        self.token = token
        self.pos_start = pos_token.start
        self.pos_end = pos_token.end

class ReturnNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.start
        self.pos_end = self.token.end
        
class VariableFunctionNode:
    def __init__(self, varible_name, value_node):
        self.variable_name = varible_name
        self.value_node = value_node

        self.pos_start = self.variable_name.start
        self.pos_end = self.variable_name.end


class RepeatNode:
    def __init__(self, variable, body):
        self.range = variable.value
        self.body = body
        self.pos_start = variable.start
        self.pos_end = self.body[len(self.body) - 1].pos_end


class FunctionNode:
    def __init__(self, name, body, variables=None):
        self.function_name = name
        self.body = body
        self.variables = variables
        self.pos_start = self.body[0].pos_start
        self.pos_end = self.body[len(self.body) - 1].pos_end

    def __repr__(self) -> str:
        return f"({self.body})"


class TillNode:
    def __init__(self, condition_expr, body):
        self.condition_expr = condition_expr
        self.body = body
        # Handle position attributes safely
        self.pos_start = getattr(
            self.condition_expr,
            "pos_start",
            getattr(self.condition_expr, "start", None),
        )
        if self.body and hasattr(self.body[-1], "pos_end"):
            self.pos_end = self.body[-1].pos_end
        elif self.body and hasattr(self.body[-1], "end"):
            self.pos_end = self.body[-1].end
        else:
            self.pos_end = getattr(
                self.condition_expr,
                "pos_end",
                getattr(self.condition_expr, "end", None),
            )

    def __repr__(self) -> str:
        return f"(till {self.condition_expr} do {self.body})"


class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.start
        self.pos_end = self.token.end

    def __repr__(self) -> str:
        return f"{self.token}"


class VariableNode:
    def __init__(self, varible_name, value_node):
        self.variable_name = varible_name
        self.value_node = value_node
        self.pos_start = self.variable_name.start
        # Handle different types of value_node (token vs node)
        if hasattr(value_node, "end"):
            self.pos_end = value_node.end
        elif hasattr(value_node, "pos_end"):
            self.pos_end = value_node.pos_end
        else:
            self.pos_end = self.variable_name.end


class VariableAccessNode:
    def __init__(self, varible_name_token):
        self.variable_name = varible_name_token
        self.pos_start = self.variable_name.start
        self.pos_end = self.variable_name.end


class UniaryOperatorNode:
    def __init__(self, op_token, node):
        self.token = op_token
        self.node = node

    def __repr__(self) -> str:
        return f"({self.token} {self.node})"


class FunctionCallNode:
    def __init__(self, function_name, function, parameters):
        self.function_name = function_name
        self.parameters = parameters
        self.pos_start = function.start
        self.pos_end = function.end

    def __repr__(self) -> str:
        return f"({self.function_name})"


class BinaryOperationNode:
    def __init__(self, left, op, right):

        self.left = left
        self.token = op
        self.right = right
        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end

    def __repr__(self) -> str:
        return f"({self.left} {self.token.value} {self.right})"


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


class Error:
    def __init__(self, error_msg, error_type, start, end):
        self.msg = error_msg
        self.type = error_type
        self.start = start
        self.end = end

    def print(self) -> str:
        result = f"{self.type}: {self.msg}\n"
        result += f"File {self.start.filename}, line {self.start.line + 1}, column {self.start.column + 1}\n"
        result += f"{self.start.text.splitlines()[self.start.line]}\n"
        result += " " * self.start.column + "^"
        return result


class IllegalCharError(Error):
    def __init__(self, error_msg, start, end):
        super().__init__(error_msg, "Illegal character", start, end)


class IllegalOperationError(Error):
    def __init__(self, error_msg, start, end, context=None):
        super().__init__(error_msg, "Runtime Error", start, end)
        self.context = context

    def print(self) -> str:
        result = self.generate_traceback()
        result += f"{self.type}: {self.msg}\n"
        result += f"{self.start.text.splitlines()[self.start.line]}\n"
        result += " " * self.start.column + "^"
        return result

    def generate_traceback(self):
        result = ""
        pos = self.start
        context = self.context
        while context:
            result += (
                f"File {pos.filename}, line {pos.line + 1}, in  {context.display_name}\n"
                + result
            )
            pos = context.parent_entry_pos
            context = context.parent
        return "Traceback (most recent call last): \n" + result


class InvalidSyntaxError(Error):
    def __init__(self, error_msg, start, end):
        super().__init__(error_msg, "Illegal syntax", start, end)


class Parser:
    def __init__(self, tokens: list[lexer.Token]):
        self.tokens: list[lexer.Token] = tokens
        self.current_token: lexer.Token | None = None
        self.index: int = -1
        self.functionNames = []
        self.is_class = False
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
                self.advance()
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
        temp = self.current_token
        if not seen and self.current_token.type == lexer.TT_IDENTIFIER:
            # Store the variable name token
            variable_token = self.current_token

            res.register_advance()
            self.advance()
            if self.current_token.type == lexer.TT_LP:

                parameters = []
                if temp.value not in self.functionNames:
                    return res.failure(
                        lexer.InvalidSyntaxError(
                            f"Function Name {temp.value} not defined",
                            temp.start,
                            temp.end,
                        )
                    )
                self.advance()
                while self.current_token.type != lexer.TT_RP:
                    if self.current_token.type == lexer.TT_NEWLINE:
                        res.failure(
                            lexer.InvalidSyntaxError("Expected )", temp.start, temp.end)
                        )
                    if self.current_token.type == lexer.TT_IDENTIFIER:
                        if self.current_token.value not in self.variables:
                            return res.failure(
                                lexer.InvalidSyntaxError(
                                    f"Variable  Name {temp.value} not defined",
                                    temp.start,
                                    temp.end,
                                )
                            )

                    parameters.append(self.current_token.value)

                    self.advance()

                    self.skip_commas(res)

                self.advance()
                res.register_advance()

                return res.success(FunctionCallNode(temp.value, temp, parameters))

            if self.current_token.value == "takes":
                self.advance()
                variables = []

                while self.current_token.value != "does":
                    if self.current_token.type != lexer.TT_IDENTIFIER:
                        return res.failure(
                            lexer.InvalidSyntaxError(
                                f"Expected Identifier not {self.current_token.type}",
                                self.current_token.start,
                                self.current_token.end,
                            )
                        )
                    variable = self.current_token.value
                    variables.append(variable)
                    self.variables.append(variable)

                    self.advance()

                    if self.current_token.type == lexer.TT_COMMA:
                        self.advance()

                if self.current_token.value == "does":
                    if temp.value in self.functionNames:
                        return res.failure(
                            lexer.InvalidSyntaxError(
                                f"Function Name {temp.value} already defined",
                                self.current_token.start,
                                self.current_token.end,
                            )
                        )
                    name = temp
                    res.register_advance()
                    self.advance()
                    then_expr = []
                    while self.current_token.type != lexer.TT_STOP:
                        self.skip_newlines(res)
                        expr = res.register(self.expr())
                        if res.error:
                            return res
                        then_expr.append(expr)
                        self.skip_newlines(res)
                    res.register_advance()  # Consume the STOP token
                    self.advance()

                    self.functionNames.append(name.value)
                    return res.success(FunctionNode(name, then_expr, variables))

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
                # Direct value assignment
                expression = self.current_token
                res.register_advance()
                self.advance()

                # Store variable in our tracking list
                if expression.value is not None:
                    self.variables.append(str(variable_token.value))

                return res.success(VariableNode(variable_token, expression))
            else:
                # Complex expression
                expression = res.register(self.expr(True))
                if res.error:
                    return res
                # Store variable in our tracking list
                if variable_token.value is not None:
                    self.variables.append(str(variable_token.value))

                return res.success(VariableNode(variable_token, expression))

        if (
            self.current_token.type == lexer.TT_KEYWORD
            and self.current_token.value == "till"
        ):
            res.register_advance()
            self.advance()

            condition_expression = res.register(self.expr(True))
            if res.error:
                return res

            if not self.current_token.matches(lexer.TT_KEYWORD, "do"):
                return res.failure(
                    lexer.InvalidSyntaxError(
                        "Expected 'do'",
                        self.current_token.start,
                        self.current_token.end,
                    )
                )

            res.register_advance()
            self.advance()

            self.skip_newlines(res)

            then_expr = []
            while self.current_token.type != lexer.TT_EOF:
                if self.current_token.value == ".":
                    break

                stmt = res.register(self.expr(False))
                if res.error:
                    return res
                then_expr.append(stmt)

                self.skip_newlines(res)

            if (
                self.current_token.type != lexer.TT_STOP
                or self.current_token.value != "."
            ):
                return res.failure(
                    lexer.InvalidSyntaxError(
                        "Expected '.'", self.current_token.start, self.current_token.end
                    )
                )

            res.register_advance()
            self.advance()

            return res.success(TillNode(condition_expression, then_expr))
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
                    data = self.current_token.value
                    res.register_advance()
                    self.advance()
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

        if self.current_token.type == lexer.TT_IDENTIFIER:
            variable = temp
            function_name = self.current_token
            if self.tokens[self.index + 1].type == lexer.TT_LP:
                self.advance()
                parameters = []

                if function_name.value not in self.functionNames:
                    return res.failure(
                        lexer.InvalidSyntaxError(
                            f"-- Function Name {function_name.value} not defined",
                            function_name.start,
                            function_name.end,
                        )
                    )
                self.advance()
                while self.current_token.type != lexer.TT_RP:
                    if self.current_token.type == lexer.TT_NEWLINE:
                        res.failure(
                            lexer.InvalidSyntaxError(
                                "Expected )", function_name.start, function_name.end
                            )
                        )

                    if self.current_token.type == lexer.TT_IDENTIFIER:
                        if self.current_token.value not in self.variables:
                            return res.failure(
                                lexer.InvalidSyntaxError(
                                    f"Variable Name {function_name.value} not defined",
                                    function_name.start,
                                    function_name.end,
                                )
                            )

                    parameters.append(self.current_token.value)

                    self.advance()

                    self.skip_commas(res)

                self.advance()
                res.register_advance()

                self.variables.append(variable.value)  # type: ignore
                if self.is_class == True:
                    self.is_class = False
                    return res.success(
                        FunctionCallNode(function_name.value, function_name, parameters)
                    )
                else:
                    return res.success(
                        VariableFunctionNode(
                            variable,
                            FunctionCallNode(
                                function_name.value, function_name, parameters
                            ),
                        )
                    )
        if (
            self.current_token.type == lexer.TT_KEYWORD
            and self.current_token.value == "return"
        ):
            self.advance()
            if self.current_token.type not in (
                lexer.TT_IDENTIFIER,
                lexer.TT_BOOL,
                lexer.TT_INT,
                lexer.TT_DOUBLE,
                lexer.TT_STRING,
            ):
                return res.failure(
                    lexer.InvalidSyntaxError(
                        "Unexpected Identifier",
                        self.current_token.start,
                        self.current_token.end,
                    )
                )
            pos_token = self.current_token
            if self.tokens[self.index + 1].type == lexer.TT_NEWLINE:
                value = self.current_token
                res.register_advance()
                self.advance()
                return res.success(ReturnNode(value))
            else:
                value = res.register(self.expr())
                if res.error:
                    return res
                res.register_advance()
                self.advance()
                return res.success(ReturnExprNode(value, pos_token))
        if (
            self.current_token.type == lexer.TT_KEYWORD
            and self.current_token.value == "repeat"
        ):
            print("Found repeat")
            res.register_advance()
            self.advance()

            variable = self.current_token
            res.register_advance()
            self.advance()

            if not self.current_token.matches(lexer.TT_KEYWORD, "times"):
                return res.failure(
                    lexer.InvalidSyntaxError(
                        "Expected 'times'",
                        self.current_token.start,
                        self.current_token.end,
                    )
                )

            res.register_advance()
            self.advance()

            self.skip_newlines(res)

            then_expr = []
            while self.current_token.type != lexer.TT_EOF:
                if self.current_token.value == ".":
                    break

                stmt = res.register(self.expr())
                if res.error:
                    return res
                then_expr.append(stmt)
                print(f"Adding statement: {stmt}")
                self.skip_newlines(res)

            if (
                self.current_token.type != lexer.TT_STOP
                or self.current_token.value != "."
            ):
                return res.failure(
                    lexer.InvalidSyntaxError(
                        "Expected '.'", self.current_token.start, self.current_token.end
                    )
                )

            res.register_advance()
            self.advance()

            return res.success(RepeatNode(variable, then_expr))
        return self.bin_operation(
            self.term,
            (
                lexer.TT_ADD,
                lexer.TT_MINUS,
                lexer.TT_LT,
                lexer.TT_GT,
            ),
        )

    def skip_newlines(self, res=ParserResult()):
        while (
            self.current_token != None and self.current_token.type == lexer.TT_NEWLINE
        ):
            res.register_advance()
            self.advance()

    def skip_commas(self, res):
        while self.current_token != None and self.current_token.type == lexer.TT_COMMA:
            res.register_advance()
            self.advance()


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


def run(filename):

    tokens, error = lexer.generate(filename)
    if error == None:
        parser = Parser(tokens)
        ast: ParserResult | None = parser.parse()
        if ast is None:
            return None, "Invalid syntax"
        print_ast(ast.node)

        return ast.node, ast.error
    else:
        return None, error.print()
