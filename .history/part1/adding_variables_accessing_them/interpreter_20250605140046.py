import parser as Pr
import lexer as Lexer


class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()

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

    def visit(self, node):
        if isinstance(node, Pr.NumberNode):
            return self.visitNumberNode(node)
        elif isinstance(node, Pr.BinaryOperationNode):
            return self.visitBinaryOperationNode(node)
        elif isinstance(node, Pr.ShowNode):
            return self.visitShowNode(node)

    def visit_ShowNode(self, node, context, symbol_table: List[SymbolTable]):
        for statement in node.body:
            # Directly print supported data types
            if isinstance(statement, (int, str, bool, float)):
                print(str(statement).strip(), end=" ")
            elif isinstance(statement, Pr.VariableAccessNode):
                # Retrieve variable value
                value = self.getVariable(statement.variable_name.value, symbol_table)
                if value is None:  # Check for undefined variable
                    return InterpreterResult().failure(
                        Lex.InvalidSyntaxError(
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
                result = self.visit(statement, context, symbol_table)
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
            return None
        value = value
        return value


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
        print(f"Setting {name} to {value}")
        if name in self.symbols:
            raise Exception(f"Variable '{name}' already exists.")
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


def run(filename):

    interpreter = Interpreter()
    symbol_table = SymbolTable()
    ast, error = Pr.run(filename)
    if ast is None:
        return None, "Parser returned None"
    if error is None:
        result = interpreter.visit(ast)
        return result, error
    else:
        return None, error


run("simply.txt")
