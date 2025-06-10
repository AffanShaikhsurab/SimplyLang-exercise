import parser as Parser
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
        if isinstance(node, Parser.NumberNode):
            return self.visitNumberNode(node)
        elif isinstance(node, Parser.BinaryOperationNode):
            return self.visitBinaryOperationNode(node)
        elif isinstance(node, Parser.ShowNode):
            return self.visitShowNode(node)

    def visitShowNode(self, node):
        # Simply print each item in the body list (string literals)
        for statement in node.body:
            print(statement, end=" ")
        print()  # Add a newline at the end
        return None
    
    def visit_VariableNode(
        self, node: Parser.VariableNode, context, symbol_table: List[SymbolTable]
    ):
        var_name = node.variable_name.value
        value = res.register(self.visit(node.value_node, context, symbol_table))
        if res.error:
            return res
        self.setVariable(var_name, value, symbol_table)
        return res.success(value)


def run(filename):

    interpreter = Interpreter()
    tokens, error = Lexer.generate(filename)
    if error == None:
        parser = Parser.Praser(tokens)
        ast = parser.parse()
        if ast.error == None:
            result = interpreter.visit(ast.node)
            return result, ast.error
        else:
            return None, ast.error
    else:
        return None, error


run("simply.txt")
