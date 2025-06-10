import parser as Pr
import lexer as Lexer


class Bool:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def isEquall(self, other):
        if isinstance(other, Bool):
            return (
                Bool(self.value == other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Can't compare bool with {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def isNotEquall(self, other):
        if isinstance(other, Bool):
            return (
                Bool(self.value != other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Can't compare bool with {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def and_with(self, other):
        if isinstance(other, Bool):
            return (
                Bool(self.value and other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Can't perform AND with {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def or_with(self, other):
        if isinstance(other, Bool):
            return (
                Bool(self.value or other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Can't perform OR with {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )


class InterpreterResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value + other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def minus(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value - other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def isLT(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value < other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def isEquall(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value == other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f" Cant compare Number with {type(other).__name__} ",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def isNotEquall(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value != other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def isGT(self, other):
        """
        This function is used to evaluate if the value of the current Number
        instance is greater than the value of the other Number instance.

        Parameters
        ----------
        other : Number
            The other Number instance to compare with.

        Returns
        -------
        Number, Error
            A Number instance with the result of the comparison and an Error
            instance if an error occurred during the comparison.

        """
        if isinstance(other, Number):
            # Create a new Number instance with the result of the comparison.
            # The value of the new Number instance is a boolean indicating if
            # the value of the current Number instance is greater than the value
            # of the other Number instance.
            comparison_result = Number(self.value > other.value)

            # Set the context of the new Number instance to the same context as
            # the current Number instance.
            comparison_result.set_context(self.context)

            # Set the position of the new Number instance to be the same as the
            # position of the current Number instance.
            comparison_result.set_pos(self.pos_start, other.pos_end)

            # Return the new Number instance and None (no error occurred).
            return comparison_result, None

    def mul(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value * other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Lexer.IllegalOperationError(
                    "Divide by zero", self.pos_start, other.pos_end, self.context
                )
            return (
                Number(self.value / other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )

    def mod(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Lexer.IllegalOperationError(
                    "Modulo by zero", self.pos_start, other.pos_end, self.context
                )
            return (
                Number(self.value % other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Cannot perform modulo with Number and {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def pow(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value**other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Cannot perform power operation with Number and {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def floor_div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Lexer.IllegalOperationError(
                    "Floor division by zero",
                    self.pos_start,
                    other.pos_end,
                    self.context,
                )
            return (
                Number(self.value // other.value)
                .set_context(self.context)
                .set_pos(self.pos_start, other.pos_end),
                None,
            )
        else:
            return None, Lexer.IllegalOperationError(
                f"Cannot perform floor division with Number and {type(other).__name__}",
                self.pos_start,
                self.pos_end,
                self.context,
            )

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return str(self.value)


class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.function_list = []

    def visitNumberNode(self, node):
        return node.value

    def visitBinaryOperationNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left is None or right is None:
            return None
        if node.operator.type == Lexer.TT_PLUS:
            return left + right
        elif node.operator.type == Lexer.TT_MINUS:
            return left - right
        elif node.operator.type == Lexer.TT_MUL:
            return left * right
        elif node.operator.type == Lexer.TT_DIV:
            return left / right

    def visit_TillNode(self, node):
        res = InterpreterResult()
        condition = res.register(self.visit(node.condition_expr))
        if res.error:
            return res
        while condition.value is True:  # Assuming 0 is false, any other value is true
            for expr in node.body:
                value = res.register(self.visit(expr))
                if res.error:
                    return res
            condition = res.register(self.visit(node.condition_expr))
        value = None
        return res.success(value)

    def visit_RepeatNode(self, node):
        res = InterpreterResult()
        for i in range(node.range):
            for expr in node.body:
                value = res.register(self.visit(expr))
                if res.error:
                    return res
        return res.success(value)  # type: ignore

    def visit(
        self,
        node,
    ):

        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_FunctionNode(
        self,
        node,
    ):
        res = InterpreterResult()
        self.function_list.append(node)
        return res.success(None)

    def visit_NumberNode(
        self,
        node,
    ):
        return InterpreterResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FunctionCallNode(
        self, node: Pr.FunctionCallNode, context, symbol_table: List[SymbolTable]
    ):
        res = InterpreterResult()
        function = []
        function_symbol_table = SymbolTable()
        function_symbol_table.set("NULL", Number(0))
        for func in self.function_list:
            if func.function_name.value == node.function_name:
                function = func.body
                if func.variables != None:
                    if len(node.parameters) != len(func.variables):
                        return InterpreterResult().failure(
                            Lex.InvalidSyntaxError(
                                f"'Invalid number of parameters are passed in function {node.function_name}'",
                                node.pos_start,
                                node.pos_end,
                            )
                        )
                    for i in range(len(node.parameters)):
                        value = self.getVariable(node.parameters[i], symbol_table)
                        if value:
                            function_symbol_table.set(func.variables[i], value)
                        else:
                            function_symbol_table.set(
                                func.variables[i], node.parameters[i]
                            )

        has_return = False
        return_value = None

        for expr in function:
            value = res.register(
                self.visit(expr, context, symbol_table + [function_symbol_table])
            )
            if res.error:
                return res

        # If no return statement was found, return None
        if not has_return:
            return res.success(None)

        return res.success(result)

    def visit_StatementsNode(
        self,
        node,
    ):
        res = InterpreterResult()
        value = None
        for statement in node.statements:
            value = res.register(
                self.visit(
                    statement,
                )
            )
            if res.error:
                return res
        return res.success(value)

    def visit_VariableNode(
        self,
        node: Pr.VariableNode,
    ):
        res = InterpreterResult()
        var_name = node.variable_name.value
        value = res.register(
            self.visit(
                node.value_node,
            )
        )
        if res.error:
            return res
        self.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_ShowNode(self, node):
        for statement in node.body:
            # Directly print supported data types
            if isinstance(statement, (int, str, bool, float)):
                print(str(statement).strip(), end=" ")
            elif isinstance(statement, Pr.VariableAccessNode):
                # Retrieve variable value
                value = self.symbol_table.get(statement.variable_name.value)
                if value is None:  # Check for undefined variable
                    return InterpreterResult().failure(
                        Lexer.InvalidSyntaxError(
                            f"'{statement.variable_name.value}' is not defined",
                            node.pos_start,
                            node.pos_end,
                        )
                    )
                # Print list values
                if isinstance(value, list):
                    print(" ".join(map(str, value)), end=" ")
                else:
                    print(value, end=" ")
            else:
                # Visit the statement and handle result
                result = self.visit(
                    statement,
                )
                if result and result.value is not None:  # Avoid printing None
                    if isinstance(result.value, Bool):
                        print(str(result.value.value).strip(), end=" ")
                    else:
                        print(result.value, end=" ")
        print()  # Ensure newline after printing all statements
        return InterpreterResult().success("success")

    def visit_VariableAccessNode(
        self,
        node,
    ):
        variable_name = node.variable_name.value
        value = self.symbol_table.get(variable_name)

        if not value:
            return InterpreterResult().failure(
                Lexer.InvalidSyntaxError(
                    f"'{variable_name}' is not defined", node.pos_start, node.pos_end
                )
            )
        try:
            value = value.copy().set_pos(node.pos_start, node.pos_end)
        except:
            value = value
        return InterpreterResult().success(value)

    def visit_BinaryOperationNode(self, node):
        res = InterpreterResult()
        left = res.register(
            self.visit(
                node.left,
            )
        )
        if res.error:
            return res
        right = res.register(self.visit(node.right))
        if res.error:
            return res

        result = None
        error = None

        if isinstance(left, Bool) or isinstance(right, Bool):
            # Convert both operands to Bool if needed
            if not isinstance(left, Bool):
                left = Bool(bool(left.value if isinstance(left, Number) else left))
            if not isinstance(right, Bool):
                right = Bool(bool(right.value if isinstance(right, Number) else right))

            if node.token.type == Lexer.TT_EQUAL:
                result, error = left.isEquall(right)
            elif node.token.type == Lexer.TT_NOT_EQUAL:
                result, error = left.isNotEquall(right)
            else:
                return res.failure(
                    Lexer.InvalidSyntaxError(
                        f"Invalid operator '{node.token.value}' for boolean values",
                        node.token.start,
                        node.token.end,
                    )
                )
        else:
            if not isinstance(left, Number):
                left = Number(left)
            if not isinstance(right, Number):
                right = Number(right)

            if node.token.type == Lexer.TT_ADD:
                result, error = left.add(right)  # type: ignore
            elif node.token.type == Lexer.TT_MINUS:
                result, error = left.minus(right)  # type: ignore
            elif node.token.type == Lexer.TT_MUL:
                result, error = left.mul(right)  # type: ignore
            elif node.token.type == Lexer.TT_DIV:
                result, error = left.div(right)  # type: ignore
            elif node.token.type == Lexer.TT_LT:
                result, error = left.isLT(right)  # type: ignore
            elif node.token.type == Lexer.TT_GT:
                result, error = left.isGT(right)  # type: ignore
            elif node.token.type == Lexer.TT_EQUAL:
                result, error = left.isEquall(right)
            elif node.token.type == Lexer.TT_NOT_EQUAL:
                result, error = left.isNotEquall(right)  # type: ignore
            else:
                return res.failure(
                    Lexer.InvalidSyntaxError(
                        f"Invalid operator '{node.token.value}'",
                        node.token.start,
                        node.token.end,
                    )
                )

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))  # type: ignore


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        value = self.symbols.get(name)
        if value == None:
            return None
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


def run(filename):

    interpreter = Interpreter()
    ast, error = Pr.run(filename)
    if ast is None:
        return None, "Parser returned None"
    if error is None:
        result = interpreter.visit(ast)
        return result, error
    else:
        return None, error


result, error = run("simply.txt")

if error is not None:
    print("Error:", error)
