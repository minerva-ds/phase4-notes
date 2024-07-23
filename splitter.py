import json

# Function to split markdown into markdown and code cells
def split_markdown(markdown_content):
    lines = markdown_content.split('\n')
    new_cells = []
    current_markdown = []
    current_code = []
    in_code_block = False

    for line in lines:
        if line.startswith("```python"):
            if current_markdown:
                new_cells.append({"cell_type": "markdown", "source": "\n".join(current_markdown), "metadata": {}})
                current_markdown = []
            in_code_block = True
            current_code.append(line)  # include the starting ```python line
        elif line.startswith("```") and in_code_block:
            current_code.append(line)  # include the ending ``` line
            in_code_block = False
            new_cells.append({"cell_type": "code", "source": "\n".join(current_code), "metadata": {}, "outputs": [], "execution_count": None})
            current_code = []
        elif in_code_block:
            current_code.append(line)
        else:
            current_markdown.append(line)
    
    if current_markdown:
        new_cells.append({"cell_type": "markdown", "source": "\n".join(current_markdown), "metadata": {}})
    
    return new_cells

# Read the original notebook
with open('notes.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

new_cells = []
for cell in notebook['cells']:
    if cell['cell_type'] == 'markdown':
        new_cells.extend(split_markdown("".join(cell['source'])))
    else:
        new_cells.append(cell)

# Create new notebook content
new_notebook = {
    "cells": new_cells,
    "metadata": notebook['metadata'],
    "nbformat": notebook['nbformat'],
    "nbformat_minor": notebook['nbformat_minor']
}

# Write to the new notebook
with open('split_notes.ipynb', 'w', encoding='utf-8') as f:
    json.dump(new_notebook, f, indent=2)

print("New notebook created as 'split_notes.ipynb'")
