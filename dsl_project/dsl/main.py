from lexer import lexer
from parser import Parser
from interpreter import Interpreter

def normalize_output(output, precision=10):
    """
    Normalize numerical outputs to remove differences between integers and floats,
    and round floats to a given precision.
    """
    try:
        # Try converting to a float, then round to the specified precision
        num = float(output)
        rounded = round(num, precision)
        return str(int(rounded)) if rounded.is_integer() else str(rounded)
    except ValueError:
        # If conversion fails, return original output (non-numeric)
        return output

def run_test_case(code, expected_output):
    """
    Runs a single test case by processing the DSL code and comparing the output.
    """
    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Capture interpreter output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        sys.stdout = sys.__stdout__
        actual_output = captured_output.getvalue().strip()
        
        # Normalize both expected and actual outputs
        normalized_expected = "\n".join(map(normalize_output, expected_output.split("\n")))
        normalized_actual = "\n".join(map(normalize_output, actual_output.split("\n")))
        
        assert normalized_actual == normalized_expected, f"Test Failed!\nCode:\n{code}\nExpected:\n{normalized_expected}\nGot:\n{normalized_actual}"
        print(f"Test Passed!\nCode:\n{code}\nOutput:\n{actual_output}\n")
    except Exception as e:
        print(f"Test Failed with Exception!\nCode:\n{code}\nException:\n{str(e)}\n")


def main():
    # Test Case 1: Simple variable assignment and print
    run_test_case("""
    set A to 5;
    show A;
    """, "5")

    # Test Case 2: Arithmetic operations
    run_test_case("""
    set A to 5;
    set B to 10;
    set C to A + B;
    show C;
    """, "15")

    # Test Case 3: Nested arithmetic operations with precedence
    run_test_case("""
    set A to 10;
    set B to 5;
    set C to (A + B) * 2;
    show C;
    """, "30")

    # Test Case 4: Exponentiation
    run_test_case("""
    set A to 2;
    set B to A ** 3;
    show B;
    """, "8.0")

    # Test Case 5: Mathematical functions (sin, sqrt)
    run_test_case("""
    set Angle to 3.14159;
    set Result to sin(Angle);
    show Result;
    """, "2.6535897933527304e-06")

    run_test_case("""
    set Root to sqrt(16);
    show Root;
    """, "4.0")

    # Test Case 6: Multi-argument function (pow)
    run_test_case("""
    set Power to pow(2, 3);
    show Power;
    """, "8.0")

    # Test Case 7: Using constants (PI and E)
    run_test_case("""
    set Circumference to 2 * PI * 10;
    show Circumference;
    """, "62.83185307179586")

    run_test_case("""
    set Exponential to E ** 2;
    show Exponential;
    """, "7.38905609893065")  # Adjust precision

    # Test Case 8: Variable reassignment
    run_test_case("""
    set A to 10;
    set A to 20;
    show A;
    """, "20")

    # Test Case 9: Error handling for undefined variable
    run_test_case("""
    show UndefinedVariable;
    """, "Test Failed with Exception!\nCode:\nshow UndefinedVariable;\nException:\nUndefined variable: UndefinedVariable\n")

    # Test Case 10: Error handling for invalid function
    run_test_case("""
    set Result to invalid_function(5);
    show Result;
    """, "Test Failed with Exception!\nCode:\nset Result to invalid_function(5);\nException:\nUnsupported function: invalid_function\n")


if __name__ == "__main__":
    main()
