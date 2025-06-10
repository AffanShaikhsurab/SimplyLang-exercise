import parser as Parser
import lexer as Lexer


class Interpreter:
    def __init__(self):
        pass

    def visitNumberNode(self, node):
        return node.value    def visitBinaryOperationNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

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


print(run("simply.txt"))
