import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from lexer import lexer
from parser import Parser
from interpreter import Interpreter

# Shared memory for variables
memory = {}
memory_displayed = False  # To track if memory is currently shown


def run_code():
    """
    Execute the DSL code entered by the user and display the output.
    """
    code = text_input.get("1.0", tk.END).strip()  # Get code from input area
    output_box.delete("1.0", tk.END)  # Clear previous output

    try:
        # Step 1: Tokenize the code
        tokens = lexer(code)

        # Step 2: Parse tokens into AST
        parser = Parser(tokens)
        ast = parser.parse()

        # Step 3: Interpret the AST with shared memory
        interpreter = Interpreter(memory=memory)
        import io
        import sys
        # Capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        interpreter.interpret(ast)
        sys.stdout = sys.__stdout__

        # Display the output in the output box
        output_box.insert(tk.END, captured_output.getvalue())

    except Exception as e:
        # Display error messages in the output box
        output_box.insert(tk.END, f"ERROR: {e}")


def toggle_memory():
    """
    Toggle the display of memory in the output box.
    """
    global memory_displayed

    if memory_displayed:
        # Hide memory
        output_box.delete("1.0", tk.END)
        memory_button.config(text="Show Memory")
        memory_displayed = False
    else:
        # Show memory
        output_box.delete("1.0", tk.END)
        if memory:
            for var, value in memory.items():
                output_box.insert(tk.END, f"{var}: {value}\n")
        else:
            output_box.insert(tk.END, "Memory is empty.\n")
        memory_button.config(text="Hide Memory")
        memory_displayed = True


def export_results():
    """
    Export the code and results to a .txt file.
    """
    code = text_input.get("1.0", tk.END).strip()
    results = output_box.get("1.0", tk.END).strip()

    if not code or not results:
        output_box.insert(tk.END, "Nothing to export!\n")
        return

    file = asksaveasfile(defaultextension=".txt", 
                         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        file.write(f"{code}\n\nResult = {results}")
        file.close()
        output_box.insert(tk.END, "Results exported successfully!\n")


def show_help():
    """
    Show a pop-up window with help information.
    """
    help_window = tk.Toplevel(root)
    help_window.title("Help - DSL Functions and Examples")
    help_window.geometry("600x400")

    help_text = tk.Text(help_window, wrap="word", font=("Courier New", 10), padx=10, pady=10)
    help_text.pack(expand=True, fill="both")

    help_content = """
    === OPERATORS ===
    +   Addition
    -   Subtraction
    *   Multiplication
    /   Division
    **  Exponentiation (Power)

    === FUNCTIONS ===
    sin(x)       Sine of x (in radians)
    cos(x)       Cosine of x (in radians)
    tan(x)       Tangent of x (in radians)
    sqrt(x)      Square root of x
    log(x)       Natural logarithm of x
    pow(x, y)    x raised to the power of y
    ceil(x)      Ceiling of x
    floor(x)     Floor of x

    === CONSTANTS ===
    PI           3.141592653589793
    E            2.718281828459045

    === EXAMPLES ===
    1. Basic Arithmetic:
        set A to 5;
        set B to 10;
        set C to A + B;
        show C;

    2. Functions:
        set Angle to PI / 2;
        set Result to sin(Angle);
        show Result;

    3. Multi-Argument Function:
        set Power to pow(2, 3);
        show Power;

    4. Using Parentheses:
        set A to (5 + 10) * 2;
        show A;

    === NOTES ===
    - All numbers are treated as floating-point.
    - Variables must start with an uppercase letter.
    """
    help_text.insert("1.0", help_content)
    help_text.configure(state="disabled")


# Create the main application window
root = tk.Tk()
root.title("DSL Interpreter")
root.geometry("600x500")  # Set default size

# Apply a modern theme
style = ttk.Style()
style.theme_use("clam")

# Top Frame for Input
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill="x", padx=10, pady=5)

input_label = ttk.Label(input_frame, text="Enter DSL Code:")
input_label.pack(anchor="w")

text_input = scrolledtext.ScrolledText(input_frame, width=70, height=10, font=("Courier New", 10))
text_input.pack(fill="x", pady=5)

# Button Frame
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill="x", padx=10, pady=5)

run_button = ttk.Button(button_frame, text="Run", command=run_code)
run_button.pack(side="left", padx=5)

memory_button = ttk.Button(button_frame, text="Show Memory", command=toggle_memory)
memory_button.pack(side="left", padx=5)

export_button = ttk.Button(button_frame, text="Export Results", command=export_results)
export_button.pack(side="left", padx=5)

help_button = ttk.Button(button_frame, text="Help", command=show_help)
help_button.pack(side="left", padx=5)

clear_input_button = ttk.Button(button_frame, text="Clear Input", command=lambda: text_input.delete("1.0", tk.END))
clear_input_button.pack(side="left", padx=5)

clear_output_button = ttk.Button(button_frame, text="Clear Output", command=lambda: output_box.delete("1.0", tk.END))
clear_output_button.pack(side="left", padx=5)

# Bottom Frame for Output
output_frame = ttk.Frame(root, padding="10")
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_label = ttk.Label(output_frame, text="Output:")
output_label.pack(anchor="w")

output_box = scrolledtext.ScrolledText(output_frame, width=70, height=10, font=("Courier New", 10), state="normal")
output_box.pack(fill="both", expand=True, pady=5)

# Start the Tkinter event loop
root.mainloop()
