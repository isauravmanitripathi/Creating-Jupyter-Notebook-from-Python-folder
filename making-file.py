"""
This script processes Python source files within a specified directory and its subdirectories,
creating a Jupyter notebook that compiles the content from these files. It is particularly
effective for assembling the contents of multiple Python files into a single notebook for
review or documentation purposes.

Main functions and features:
- Traverses the specified directory and its subdirectories to locate Python files.
- Extracts the content from each Python file.
- Removes single-line and multi-line comments and docstrings from the extracted content for clarity.
- Assembles the cleaned content into a Jupyter notebook, with each file's content in a separate cell.
- Prompts user interaction to confirm processing of each directory.
- Creates a notebook file in the specified directory with the compiled content.
"""

import os
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

def create_notebook_from_python_files(folder_path):
    """
    Creates a Jupyter notebook from Python files in the given folder and subfolders.
    """
    nb = nbf.v4.new_notebook()
    code_cell_count = 0  # Counter for code cells

    for root, dirs, files in os.walk(folder_path):
        enter_folder = input(f"Do you want to enter the folder {root}? (yes/no): ")
        if enter_folder.lower() != 'yes':
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                with open(file_path, 'r') as f:
                    content = f.read()
                content_without_comments = remove_comments_and_docstrings(content)

                if content_without_comments:
                    print(f"Processing content from {file}")
                    markdown_cell = nbf.v4.new_markdown_cell(f"# {file}\n\nPath: {file_path}")
                    nb['cells'].append(markdown_cell)

                    code_cell = nbf.v4.new_code_cell(content_without_comments)
                    nb['cells'].append(code_cell)
                    code_cell_count += 1
                else:
                    print(f"No content found in {file}")

    print(f"Total number of code cells created: {code_cell_count}")
    return nb

# Ask the user to enter the path to the folder
folder_path = input("Enter the path to your folder: ")
nb = create_notebook_from_python_files(folder_path)
nbf.write(nb, os.path.join(folder_path, 'extracted_content.ipynb'))
