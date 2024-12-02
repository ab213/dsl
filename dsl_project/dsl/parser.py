from nodes import NumberNode, VariableNode, BinaryOperationNode, AssignmentNode, PrintNode, FunctionNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens to parse
        self.pos = 0  # Current position in the token list

    def current_token(self):
        """
        Returns the current token in the token list or None if at the end.
        """
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type):
        """
        Advances the current position if the token matches the expected type.
        Raises an error if the token type doesn't match.
        """
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
        else:
            raise ValueError(f"Expected {token_type}, got {self.current_token()}")

    def parse(self):
        """
        Parses the entire token list and returns a list of AST nodes.
        """
        nodes = []
        while self.current_token():  # Continue until no tokens are left
            nodes.append(self.statement())  # Parse individual statements
        return nodes

    def statement(self):
        """
        Parses a single statement. Handles assignments and print statements.
        """
        token = self.current_token()
        if token[0] == 'KEYWORD_SET':
            return self.assignment()  # Handle variable assignment
        elif token[0] == 'KEYWORD_SHOW':
            return self.print_statement()  # Handle print statement
        else:
            raise ValueError(f"Unexpected token {token}")

    def assignment(self):
        """
        Parses an assignment statement in the form:
        set <IDENTIFIER> to <expression>;
        """
        self.consume('KEYWORD_SET')
        variable = self.current_token()[1]  # Capture the variable name
        self.consume('IDENTIFIER')
        self.consume('KEYWORD_TO')
        value = self.expression()  # Parse the expression assigned to the variable
        self.consume('SEMICOLON')
        return AssignmentNode(variable, value)

    def print_statement(self):
        """
        Parses a print statement in the form:
        show <IDENTIFIER>;
        """
        self.consume('KEYWORD_SHOW')
        variable = self.current_token()[1]  # Capture the variable name to be printed
        self.consume('IDENTIFIER')
        self.consume('SEMICOLON')
        return PrintNode(variable)

    def expression(self):
        """
        Parses an expression, starting with the highest precedence (additive).
        """
        return self.additive()

    def additive(self):
        """
        Handles addition and subtraction in expressions.
        e.g., <multiplicative> + <multiplicative>
        """
        left = self.multiplicative()
        while self.current_token() and self.current_token()[1] in ('+', '-'):
            operator = self.current_token()[1]
            self.consume('OPERATOR')
            right = self.multiplicative()
            left = BinaryOperationNode(left, operator, right)  # Create a binary operation node
        return left

    def multiplicative(self):
        """
        Handles multiplication and division in expressions.
        e.g., <exponentiation> * <exponentiation>
        """
        left = self.exponentiation()
        while self.current_token() and self.current_token()[1] in ('*', '/'):
            operator = self.current_token()[1]
            self.consume('OPERATOR')
            right = self.exponentiation()
            left = BinaryOperationNode(left, operator, right)  # Create a binary operation node
        return left

    def exponentiation(self):
        """
        Handles exponentiation in expressions.
        e.g., <term> ** <term>
        """
        left = self.term()
        while self.current_token() and self.current_token()[1] == '**':
            operator = self.current_token()[1]
            self.consume('OPERATOR')
            right = self.term()
            left = BinaryOperationNode(left, operator, right)  # Create a binary operation node
        return left

    def term(self):
        """
        Handles terms in expressions. Terms can be numbers, variables, functions, or grouped expressions.
        """
        token = self.current_token()
        if token[0] == 'NUMBER':
            # Handle numeric literals
            self.consume('NUMBER')
            return NumberNode(float(token[1]))
        elif token[0] == 'IDENTIFIER':
            # Handle variable references
            self.consume('IDENTIFIER')
            return VariableNode(token[1])
        elif token[0] == 'FUNCTION':
            # Handle function calls like sin(x), sqrt(y)
            function_name = token[1]
            self.consume('FUNCTION')
            self.consume('LPAREN')
            arguments = []
            while True:
                arguments.append(self.expression())  # Parse each argument
                if self.current_token()[0] == 'RPAREN':  # Break on closing parenthesis
                    break
                self.consume('COMMA')  # Consume the comma between arguments
            self.consume('RPAREN')
            return FunctionNode(function_name, arguments)
        elif token[0] == 'LPAREN':
            # Handle grouped expressions (parentheses)
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            raise ValueError(f"Unexpected token {token}")
