import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar
import subprocess
import os
import ast

def run_code(file_path):
    """Run the Python code from the selected file."""
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error executing the code: {str(e)}"

def summarize_code(file_path):
    """Summarize the selected Python code and generate an explanation."""
    with open(file_path, 'r') as file:
        code = file.read()

    # Basic summary based on function definitions and classes
    tree = ast.parse(code)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]

    summary = []
    explanation = []

    # Summary of functions
    if functions:
        summary.append(f"Functions found: {', '.join([func.name for func in functions])}")
        explanation.append("The code defines the following functions:")
        for func in functions:
            # Summarizing the function purpose
            func_details = f"- {func.name}: This function is likely a {func.name} calculation. "
            func_details += "It accepts the input parameter(s) and returns the result of the calculation."

            # Describe the parameters (if available) and return value
            if func.args.args:
                parameters = [arg.arg for arg in func.args.args]
                func_details += f"The function takes the parameters: {', '.join(parameters)}."
            explanation.append(func_details)

            # Detailed description of function logic
            explanation.append(f"  Function {func.name} performs the following steps:")
            for node in func.body:
                if isinstance(node, ast.If):
                    explanation.append("  - Contains conditional checks (if statements).")
                elif isinstance(node, ast.For):
                    explanation.append("  - Contains a loop (for loop).")
                elif isinstance(node, ast.Return):
                    explanation.append("  - Returns a result.")
                elif isinstance(node, ast.Assign):
                    explanation.append(f"  - Assigns values to variables, e.g., {ast.dump(node)}.")
                elif isinstance(node, ast.Expr):
                    explanation.append(f"  - Contains an expression: {ast.dump(node)}.")

    # Summary of classes
    if classes:
        summary.append(f"Classes found: {', '.join([cls.name for cls in classes])}")
        explanation.append("The code defines the following classes:")
        for cls in classes:
            explanation.append(f"- {cls.name}: This class represents {cls.name} related tasks or functionality.")

    # Code flow description
    explanation.append("\nMain Program Flow:")
    explanation.append("1. The code likely defines the structure and flow of a program with classes and functions.")
    explanation.append("2. It handles tasks like processing data, user input, and performing operations.")
    explanation.append("3. The execution starts with function calls or entry points defined in the script.")
    
    # If no functions or classes were found, it's likely procedural code
    if not functions and not classes:
        summary.append("No functions or classes were found.")
        explanation.append("The code seems to be procedural in nature and doesn't have any classes or functions defined.")

    return "\n".join(summary), "\n".join(explanation)

def analyze_code():
    """Analyze the selected Python code and display the output."""
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if not file_path:
        return

    # Run code and display the output
    output = run_code(file_path)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

    # Summarize the code
    summary, explanation = summarize_code(file_path)

    # Display summary and explanation
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)

    explanation_text.delete(1.0, tk.END)
    explanation_text.insert(tk.END, explanation)

def exit_app():
    """Exit the application."""
    root.quit()

# Set up the main window
root = tk.Tk()
root.title("Python Code Analyzer")
root.geometry("800x600")
root.configure(bg='#2e3d4f')

# Add a title label with a specific font style
title_label = tk.Label(root, text="Python Code Analyzer", font=("Helvetica", 24, "bold"), fg="white", bg="#2e3d4f")
title_label.pack(pady=20)

# Analyze button
analyze_button = tk.Button(root, text="Analyze Code", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=analyze_code)
analyze_button.pack(pady=10)

# Output area with a scrollbar
output_frame = tk.Frame(root)
output_frame.pack(pady=20)

output_scroll = Scrollbar(output_frame, orient="vertical")
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

output_text = Text(output_frame, wrap=tk.WORD, height=10, width=80, font=("Courier New", 12))
output_text.pack(side=tk.LEFT, fill=tk.BOTH)
output_scroll.config(command=output_text.yview)
output_text.config(yscrollcommand=output_scroll.set)

# Summary area
summary_label = tk.Label(root, text="Code Summary", font=("Helvetica", 16), fg="white", bg="#2e3d4f")
summary_label.pack(pady=10)

summary_text = Text(root, wrap=tk.WORD, height=8, width=80, font=("Courier New", 12))
summary_text.pack(pady=10)

# Explanation area
explanation_label = tk.Label(root, text="Code Explanation", font=("Helvetica", 16), fg="white", bg="#2e3d4f")
explanation_label.pack(pady=10)

explanation_text = Text(root, wrap=tk.WORD, height=10, width=80, font=("Courier New", 12))
explanation_text.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), bg="#f44336", fg="white", command=exit_app)
exit_button.pack(pady=20)

# Run the main loop
root.mainloop()