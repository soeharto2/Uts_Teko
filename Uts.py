import re


# AST NODE


class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, value):
        self.value = value

class Var(AST):
    def __init__(self, name):
        self.name = name

class ParserError(Exception):
    pass



# MINI COMPILER


class MiniCompiler:
    def __init__(self, source, env):

        # TUGAS 1
        # tambahkan simbol ^
        self._tokens = iter(
            re.findall(
                r'[a-zA-Z_]\w*|\d+(?:\.\d+)?|[\^+*/()\-]',
                source
            ) + ['?']
        )

        self._current = None
        self._env = env
        self._temp_count = 0
        self.advance()

    def advance(self):
        try:
            self._current = next(self._tokens)
        except StopIteration:
            self._current = None

    def expect(self, expected):
        if self._current != expected and not (
            expected == "ID" and self._current.isalnum()
        ):
            raise ParserError(
                f"Expected {expected}, found {self._current}"
            )

        token = self._current
        self.advance()
        return token

    def factor(self):
        token = self._current

        if token is not None and token.replace('.', '', 1).isdigit():
            self.advance()
            return Num(float(token) if '.' in token else int(token))

        elif token and token.isalpha():

            # ANALISIS SEMANTIK
            if token not in self._env:
                raise ParserError(
                    f"Semantic Error: Undefined variable '{token}'"
                )

            self.advance()
            return Var(token)

        elif token == '(':
            self.advance()

            node = self.expr()

            self.expect(')')
            return node

        raise ParserError(f"Unexpected token: {token}")

  
    # TUGAS 2
    
    def power(self):

        node = self.factor()

        while self._current == '^':
            op = self._current
            self.advance()

            node = BinOp(
                left=node,
                op=op,
                right=self.factor()
            )

        return node

    
    # TUGAS 3
    
    def term(self):

        # sekarang term memakai power()
        node = self.power()

        while self._current in ('*', '/'):
            op = self._current
            self.advance()

            node = BinOp(
                left=node,
                op=op,
                right=self.power()
            )

        return node

    def expr(self):

        node = self.term()

        while self._current in ('+', '-'):
            op = self._current
            self.advance()

            node = BinOp(
                left=node,
                op=op,
                right=self.term()
            )

        return node

    
    # TAC GENERATOR
    
    def generate_tac(self, node):

        if isinstance(node, Num):
            return str(node.value)

        if isinstance(node, Var):
            return node.name

        left_val = self.generate_tac(node.left)
        right_val = self.generate_tac(node.right)

        self._temp_count += 1
        temp_name = f"t{self._temp_count}"

        print(f"{temp_name} = {left_val} {node.op} {right_val}")

        return temp_name



# UJI COBA


source_code = "a ^ 2 + b * c"
symbol_table = {
    'a': 5,
    'b': 10,
    'c': 2
}

try:

    print(f"Input: {source_code}")

    compiler = MiniCompiler(
        source_code,
        symbol_table
    )

    ast_root = compiler.expr()

    print("\n--- Output Three Address Code (TAC) ---")

    compiler.generate_tac(ast_root)

except Exception as e:
    print(f"Error: {e}")
