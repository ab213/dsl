# Node classes for representing different components of an abstract syntax tree (AST).

class NumberNode:
    def __init__(self, value):
        self.value = value  # Stores the numerical value of the node

    def __repr__(self):
        return f"NumberNode({self.value})"  # Provides a clear string representation for debugging


class VariableNode:
    def __init__(self, name):
        self.name = name  # Holds the variable's name as a string

    def __repr__(self):
        return f"VariableNode({self.name})"  # Makes it easy to identify variable nodes during debugging


class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left  # Left operand
        self.operator = operator  # Operator (+, -, *, /, etc.)
        self.right = right  # Right operand

    def __repr__(self):
        return f"BinaryOperationNode({self.left}, {self.operator}, {self.right})"
        # A readable format to inspect binary operations in the AST


class AssignmentNode:
    def __init__(self, variable, value):
        self.variable = variable  # Variable being assigned
        self.value = value  # Value being assigned to the variable

    def __repr__(self):
        return f"AssignmentNode({self.variable}, {self.value})"
        # Represents assignments like `x = 5`


class PrintNode:
    def __init__(self, variable):
        self.variable = variable  # The variable or value to be printed

    def __repr__(self):
        return f"PrintNode({self.variable})"
        # Captures print instructions in the AST


class FunctionNode:
    def __init__(self, function_name, arguments):
        self.function_name = function_name  # Name of the function (e.g., sin, cos)
        self.arguments = arguments  # A list of arguments for functions that accept multiple inputs

    def __repr__(self):
        return f"FunctionNode({self.function_name}, {self.arguments})"
        # Represents function calls like `sin(x)` or `log(x, base)`
