import parser as Pr
import lexer as Lexer


class Interpreter:
    def __init__(self):
        pass

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

    def visitShowNode(self, node):
        # Simply print each item in the body list (string literals)
        for statement in node.body:
            print(statement, end=" ")
        print()  # Add a newline at the end
        return None


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
