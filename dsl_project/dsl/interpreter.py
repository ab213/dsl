import math
from nodes import NumberNode, VariableNode, BinaryOperationNode, AssignmentNode, PrintNode, FunctionNode

class Interpreter:
    def __init__(self, memory=None):
        """
        Initializes the interpreter with a memory (variable storage).
        If no memory is provided, it creates an empty dictionary for variables.
        """
        self.variables = memory if memory is not None else {}

    def interpret(self, nodes):
        """
        Executes a list of AST nodes by evaluating each node in sequence.
        
        Args:
            nodes (list): A list of AST nodes to interpret.
        """
        for node in nodes:
            self.evaluate(node)  # Evaluate each node

    def evaluate(self, node):
        """
        Evaluates a single AST node and performs the appropriate operation.
        
        Args:
            node: The AST node to evaluate.

        Returns:
            The result of the evaluation, if applicable.
        """
        if isinstance(node, NumberNode):
            # Return the numerical value stored in the node
            return node.value

        elif isinstance(node, VariableNode):
            # Fetch the value of the variable from memory
            if node.name in self.variables:
                return self.variables[node.name]
            elif node.name == "PI":  # Handle the constant π
                return math.pi
            elif node.name == "E":  # Handle the constant e
                return math.e
            else:
                raise ValueError(f"Undefined variable: {node.name}")

        elif isinstance(node, BinaryOperationNode):
            # Perform the binary operation based on the operator
            left = self.evaluate(node.left)  # Evaluate the left operand
            right = self.evaluate(node.right)  # Evaluate the right operand
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                if right == 0:
                    raise ValueError("Division by zero is not allowed")
                return left / right
            elif node.operator == '**':
                return left ** right

        elif isinstance(node, FunctionNode):
            # Evaluate function calls (e.g., sin, cos, sqrt)
            arguments = [self.evaluate(arg) for arg in node.arguments]  # Evaluate all arguments
            if hasattr(math, node.function_name):  # Check if the function exists in the math module
                return getattr(math, node.function_name)(*arguments)  # Call the math function
            else:
                raise ValueError(f"Unsupported function: {node.function_name}")

        elif isinstance(node, AssignmentNode):
            # Assign a value to a variable
            value = self.evaluate(node.value)  # Evaluate the expression on the right-hand side
            self.variables[node.variable] = value  # Store the result in memory

        elif isinstance(node, PrintNode):
            # Print the value of a variable
            if node.variable in self.variables:
                print(self.variables[node.variable])  # Print the variable's value
            else:
                raise ValueError(f"Undefined variable: {node.variable}")
