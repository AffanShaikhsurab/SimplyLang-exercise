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
            return self.visit_ShowNode(node)
        elif isinstance(node, Pr.StatementsNode):
            return self.visit_StatementsNode(node)
        elif isinstance(node, Pr.VariableNode):
            return self.visit_VariableNode(node)
        elif isinstance(node, Pr.VariableAccessNode):
            return self.visit_VariableAccessNode(node)

    def visit_StatementsNode(
        self,
        node,
    ):
        value = None
        for statement in node.statements:
            value = self.visit(
                statement,
            )
        return value
    def visit_TillNode(self, node, context, symbol_table: List[SymbolTable]):
        condition = res.register(self.visit(node.condition_expr, context, symbol_table))
        if res.error:
            return res
        while condition.value != 0:  # Assuming 0 is false, any other value is true
            for expr in node.body:
                value = res.register(self.visit(expr, context, symbol_table))
                if res.error:
                    return res
            condition = res.register(
                self.visit(node.condition_expr, context, symbol_table)
            )
        value = None
        return res.success(value)
    
    def visit_VariableNode(self, node: Pr.VariableNode):
        var_name = node.variable_name
        print(f"Visiting variable node: {node.value_node}")
        value = self.visit(node.value_node)
        if value is None:
            return None
        print(f"Setting variable '{var_name.value}' to {value}")
        self.symbol_table.set(var_name.value, value)
        return value

    def visit_ShowNode(
        self,
        node,
    ):
        for statement in node.body:
            # Directly print supported data types
            if isinstance(statement, (int, str, bool, float)):
                print(str(statement).strip(), end=" ")
            elif isinstance(statement, Pr.VariableAccessNode):
                # Retrieve variable value
                value = self.symbol_table.get(statement.variable_name.value)
                if value is None:  # Check for undefined variable
                    print(
                        f"Undefined variable: {statement.variable_name.value}", end=" "
                    )
                    continue

                # Print list values
                if isinstance(value, list):
                    print(" ".join(map(str, value)), end=" ")
                else:
                    print("final output: ", end="")
                    print(value.value, end=" ")
            else:
                # Visit the statement and handle result
                result = self.visit(statement)
                if result and result.value is not None:  # Avoid printing None
                    if isinstance(result.value, bool):
                        print(str(result.value).strip(), end=" ")
                    else:
                        print(result.value, end=" ")
        print()  # Ensure newline after printing all statements
        return None

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

    def get(self, name):
        value = self.symbols.get(name)
        if value == None:
            return None
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
