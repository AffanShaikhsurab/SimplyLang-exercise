import os
from typing import List
import parser as Pr
import lexer as Lexer


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


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


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
        if isinstance(other, Number):
            comparison_result = Number(self.value > other.value)
            comparison_result.set_context(self.context)
            comparison_result.set_pos(self.pos_start, other.pos_end)
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

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return str(self.value)


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


class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.function_list = []

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node):
        return InterpreterResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BoolNode(self, node):
        return InterpreterResult().success(
            Bool(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VariableAccessNode(self, node):
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

    def visit_VariableNode(self, node: Pr.VariableNode):
        res = InterpreterResult()
        var_name = node.variable_name.value
        value = res.register(self.visit(node.value_node))
        if res.error:
            return res
        self.symbol_table.set(var_name, value)
        return res.success(value)

    # Array-related visit methods
    def visit_ArrayNode(self, node):
        res = InterpreterResult()
        var_name = node.variable_name.value
        value = node.value_node
        if res.error:
            return res
        self.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_ArrayVariable(self, node: Pr.ArrayVariable):
        res = InterpreterResult()
        array_var_name = node.variable.value
        index = node.index.value

        expression_value = None
        if hasattr(node.expression, 'token'):
            expression_value = node.expression.token.value
        else:
            expression_value = res.register(self.visit(node.expression))
            if res.error:
                return res

        value = self.symbol_table.get(array_var_name)
        if not value:
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not defined", node.pos_start, node.pos_end
                )
            )
        if not isinstance(value, list):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not an array", node.pos_start, node.pos_end
                )
            )
        if index < 0 or index >= len(value):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"Index out of range", node.pos_start, node.pos_end
                )
            )

        value[index] = expression_value
        self.symbol_table.set(array_var_name, value)
        return res.success(value)

    def visit_ArrayAccessNode(self, node: Pr.ArrayAccessNode):
        res = InterpreterResult()

        array_name = node.access_variable
        target_var = node.variable_name.value
        index = node.value_node.value

        array = self.symbol_table.get(array_name)
        if not array:
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_name}' is not defined", node.pos_start, node.pos_end
                )
            )

        if not isinstance(array, list):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_name}' is not an array", node.pos_start, node.pos_end
                )
            )

        if index < 0 or index >= len(array):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"Index {index} out of bounds for array '{array_name}'",
                    node.pos_start,
                    node.pos_end,
                )
            )

        value = array[index]
        self.symbol_table.set(target_var, Number(value))
        return res.success(Number(value))

    def visit_ArrayArrangeNode(self, node: Pr.ArrayArrangeNode):
        res = InterpreterResult()
        var_name = node.variable_name.value
        array_var = node.array
        is_ascending = node.type

        if hasattr(array_var, 'value'):
            array_var_name = array_var.value
        else:
            array_var_name = array_var

        array = self.symbol_table.get(array_var_name)

        if not array:
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not defined", node.pos_start, node.pos_end
                )
            )
        if not isinstance(array, list):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not an array", node.pos_start, node.pos_end
                )
            )
        
        sorted_array = array.copy()
        if is_ascending:
            sorted_array.sort()
        else:
            sorted_array.sort(reverse=True)
        
        self.symbol_table.set(var_name, sorted_array)
        return res.success(sorted_array)

    def visit_ArrayLengthNode(self, node: Pr.ArrayLengthNode):
        res = InterpreterResult()

        variable = node.variable.value
        array_var = node.expression

        if hasattr(array_var, 'value'):
            array_var_name = array_var.value
        else:
            array_var_name = array_var

        array = self.symbol_table.get(array_var_name)
        if not array:
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not defined", node.pos_start, node.pos_end
                )
            )
        if not isinstance(array, list):
            return res.failure(
                Lexer.InvalidSyntaxError(
                    f"'{array_var_name}' is not an array", node.pos_start, node.pos_end
                )
            )

        length = len(array)
        self.symbol_table.set(variable, length)
        return res.success(length)

    def visit_StatementsNode(self, node):
        res = InterpreterResult()
        value = None
        for statement in node.statements:
            value = res.register(self.visit(statement))
            if res.error:
                return res
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
                result = self.visit(statement)
                if result and result.value is not None:  # Avoid printing None
                    if isinstance(result.value, Bool):
                        print(str(result.value.value).strip(), end=" ")
                    else:
                        print(result.value, end=" ")
        print()  # Ensure newline after printing all statements
        return InterpreterResult().success("success")

    def visit_FunctionNode(self, node):
        res = InterpreterResult()
        self.function_list.append(node)
        return res.success(None)

    def visit_FunctionCallNode(self, node: Pr.FunctionCallNode):
        res = InterpreterResult()
        function = []
        for func in self.function_list:
            if func.function_name.value == node.function_name:
                function = func.body
                if func.variables != None:
                    if len(node.parameters) != len(func.variables):
                        return InterpreterResult().failure(
                            Lexer.InvalidSyntaxError(
                                f"'Invalid number of parameters are passed in function {node.function_name}'",
                                node.pos_start,
                                node.pos_end,
                            )
                        )
                    for i in range(len(node.parameters)):
                        value = self.symbol_table.get(node.parameters[i])
                        if value:
                            self.symbol_table.set(func.variables[i], value)
                        else:
                            self.symbol_table.set(func.variables[i], node.parameters[i])
        value = None
        for expr in function:
            value = res.register(self.visit(expr))
            if res.error:
                return res

        return res.success(value)

    def visit_TillNode(self, node):
        res = InterpreterResult()
        condition = res.register(self.visit(node.condition_expr))
        if res.error:
            return res
        while condition.value != 0:  # Assuming 0 is false, any other value is true
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
        return res.success(value)

    def visit_BinaryOperationNode(self, node):
        res = InterpreterResult()
        left = res.register(self.visit(node.left))
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
                result, error = left.add(right)
            elif node.token.type == Lexer.TT_MINUS:
                result, error = left.minus(right)
            elif node.token.type == Lexer.TT_MUL:
                result, error = left.mul(right)
            elif node.token.type == Lexer.TT_DIV:
                result, error = left.div(right)
            elif node.token.type == Lexer.TT_LT:
                result, error = left.isLT(right)
            elif node.token.type == Lexer.TT_GT:
                result, error = left.isGT(right)
            elif node.token.type == Lexer.TT_EQUAL:
                result, error = left.isEquall(right)
            elif node.token.type == Lexer.TT_NOT_EQUAL:
                result, error = left.isNotEquall(right)
            elif node.token.type == Lexer.TT_MOD:
                result, error = left.mod(right)
            elif node.token.type == Lexer.TT_POW:
                result, error = left.pow(right)
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
            return res.success(result.set_pos(node.pos_start, node.pos_end))


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


# Test execution
if __name__ == "__main__":
    result, error = run("simply.txt")
    if error is not None:
        print("Error:", error)
