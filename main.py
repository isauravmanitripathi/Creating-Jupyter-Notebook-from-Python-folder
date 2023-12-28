"""
This script is designed to process Python source files in a specified directory (and its subdirectories),
extracting functions and classes from these files. It then assembles these extracted code snippets
into a Jupyter notebook. The script removes comments and docstrings from the extracted code for clarity.
It's useful for consolidating and reviewing code from multiple files in a single notebook,
especially for documentation or educational purposes.

Key features:
- Traverses a specified directory and its subdirectories.
- Extracts functions and classes from Python files using AST (Abstract Syntax Tree) parsing.
- Removes comments and docstrings from the extracted code.
- Compiles the extracted code into a Jupyter notebook, with each snippet in a separate cell.
- Allows user interaction to choose which directories to process.
"""
import os
import ast
import nbformat as nbf
import re

def remove_comments_and_docstrings(source_code):
    """
    Removes single-line and multi-line comments and docstrings from the source code.
    """
    # Remove single-line comments
    source_code = re.sub(r'#.*$', '', source_code, flags=re.MULTILINE)

    # Remove multi-line string literals used as comments or docstrings
    def replacer(match):
        return '' if match.group(0).startswith(('"""', "'''")) else match.group(0)

    pattern = r'(""".*?"""|\'\'\'.*?\'\'\')|(\".*?\"|\'.*?\')'
    source_code = re.sub(pattern, replacer, source_code, flags=re.DOTALL)

    return source_code

def extract_functions_and_classes_from_file(file_path):
    """
    Extracts functions and classes from a given Python file using AST.
    This function opens the file, reads its content, and then parses it using AST.
    It returns a list of functions and classes, excluding comments and docstrings.
    """
    with open(file_path, 'r') as file:
        node = ast.parse(file.read())

    functions_and_classes = []

    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            code = ast.unparse(item)
            code_without_comments = remove_comments_and_docstrings(code)
            functions_and_classes.append(code_without_comments)

    return functions_and_classes

def create_notebook_from_python_files(folder_path):
    """
    Creates a Jupyter notebook from Python files in the given folder and subfolders.
    This function walks through the folder structure, asking the user whether to process each folder.
    It then extracts functions and classes from each Python file and adds them to the notebook.
    """
    nb = nbf.v4.new_notebook()
    code_cell_count = 0  # Counter for code cells

    for root, dirs, files in os.walk(folder_path):
        # Ask whether to enter the folder
        enter_folder = input(f"Do you want to enter the folder {root}? (yes/no): ")
        if enter_folder.lower() != 'yes':
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                contents = extract_functions_and_classes_from_file(file_path)
                if contents:
                    print(f"Extracted {len(contents)} functions/classes from {file}")
                    markdown_cell = nbf.v4.new_markdown_cell(f"# Functions and Classes from {file}")
                    nb['cells'].append(markdown_cell)
                    for content in contents:
                        code_cell = nbf.v4.new_code_cell(content)
                        nb['cells'].append(code_cell)
                        code_cell_count += 1  # Increment code cell counter
                else:
                    print(f"No functions or classes found in {file}")

    print(f"Total number of code cells created: {code_cell_count}")
    return nb

# Ask the user to enter the path to the folder
folder_path = input("Enter the path to your folder: ")
nb = create_notebook_from_python_files(folder_path)
nbf.write(nb, os.path.join(folder_path, 'extracted_functions_and_classes.ipynb'))
