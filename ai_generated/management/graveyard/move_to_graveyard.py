#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""
RP Graveyard Refactoring Script

This script moves code blocks marked with #GRAVEYARD START and #GRAVEYARD END
from r.py to libs/graveyard.py, with proper dependency qualification.

Usage:
    /opt/homebrew/opt/python@3.10/bin/python3.10 move_to_graveyard.py

The script will:
1. Find all #GRAVEYARD START/END pairs in r.py
2. Extract the code blocks between markers
3. Apply qualify_imports to handle rp dependencies  
4. Remove blocks from r.py
5. Append processed blocks to libs/graveyard.py
6. Add graveyard import to r.py if needed
"""

import os
import re
import sys
import ast

# Add the rp directory to path so we can import rp
rp_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rp_path)

import rp

def find_graveyard_blocks(content):
    """Find all code blocks marked with #GRAVEYARD START/END pairs.
    
    Returns:
        List of tuples: (start_line, end_line, block_content)
    """
    lines = content.split('\n')
    blocks = []
    start_line = None
    
    for i, line in enumerate(lines):
        if '#GRAVEYARD START' in line:
            if start_line is not None:
                raise ValueError(f"Found nested GRAVEYARD START at line {i+1}, previous START at line {start_line+1}")
            start_line = i
        elif '#GRAVEYARD END' in line:
            if start_line is None:
                raise ValueError(f"Found GRAVEYARD END at line {i+1} without matching START")
            
            # Extract the block content (excluding the markers)
            block_lines = lines[start_line+1:i]
            block_content = '\n'.join(block_lines)
            
            blocks.append((start_line, i, block_content))
            start_line = None
    
    if start_line is not None:
        raise ValueError(f"Found GRAVEYARD START at line {start_line+1} without matching END")
    
    return blocks

def process_block_for_graveyard(block_content):
    """Process a code block for the graveyard by adding rp import and qualifying dependencies.
    
    Args:
        block_content: Raw code block extracted from r.py
        
    Returns:
        Processed code block ready for graveyard.py
    """
    # Step 1: Add star import at top (this is the key step you specified)
    code_with_star_import = "from rp.r import *\n\n" + block_content
    
    # Step 2: Use qualify_imports to convert "from rp.r import *" to qualified calls
    try:
        qualified_code = rp.qualify_imports(code_with_star_import, 'rp.r')
        print("✓ Successfully applied qualify_imports to process rp.r dependencies")
        return qualified_code
    except Exception as e:
        print(f"ERROR: qualify_imports failed ({e}) - this indicates a bug in the process")
        print(f"Block content that failed:\n{code_with_star_import[:200]}...")
        raise e  # Don't continue with manual processing - this should always work

def remove_blocks_from_content(content, blocks):
    """Remove graveyard blocks from the original content.
    
    Args:
        content: Original file content
        blocks: List of (start_line, end_line, block_content) tuples
        
    Returns:
        Content with marked blocks removed
    """
    lines = content.split('\n')
    
    # Sort blocks by line number in reverse order to remove from bottom to top
    # This prevents line number shifts from affecting subsequent removals
    sorted_blocks = sorted(blocks, key=lambda x: x[0], reverse=True)
    
    for start_line, end_line, _ in sorted_blocks:
        # Remove lines from start_line to end_line (inclusive, including markers)
        del lines[start_line:end_line+1]
    
    return '\n'.join(lines)

def add_graveyard_import_to_rpy(content):
    """Add graveyard import to r.py if not already present.
    
    Args:
        content: r.py content
        
    Returns:
        Content with graveyard import added if needed
    """
    graveyard_import = "from rp.libs.graveyard import *"
    
    if graveyard_import in content:
        print("Graveyard import already present in r.py")
        return content
    
    # Find a good place to add the import - after other rp imports
    lines = content.split('\n')
    
    # Look for existing rp imports or just add after the initial imports
    insert_line = 0
    for i, line in enumerate(lines):
        if line.startswith('import rp') or line.startswith('from rp'):
            insert_line = i + 1
        elif line.startswith('import ') and 'rp' not in line:
            # Found other imports, but let's keep looking for rp imports
            if insert_line == 0:
                insert_line = i + 1
    
    # Insert the import
    lines.insert(insert_line, graveyard_import)
    print(f"Added graveyard import at line {insert_line + 1}")
    
    return '\n'.join(lines)

def extract_exported_names(code):
    """Extract all function and variable names that should be in __all__.
    
    Args:
        code: Python code as string
        
    Returns:
        List of names (functions, variables, classes) to export
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # If there's a syntax error, return empty list
        return []
    
    names = []
    # Only get top-level definitions (not nested ones)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            # Handle variable assignments at module level only
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Filter out common temporary variables and single letters
                    var_name = target.id
                    if (len(var_name) > 1 or var_name.startswith('_')) and var_name not in ['os', 'sys', 'ast', 're']:
                        names.append(var_name)
    
    return names

def generate_all_list(graveyard_content):
    """Generate __all__ list from graveyard content.
    
    Args:
        graveyard_content: Full content of graveyard.py
        
    Returns:
        String representation of __all__ list
    """
    # Extract all names from the graveyard content
    all_names = set()
    
    # Split content into blocks and extract names from each
    blocks = graveyard_content.split('# Block ')
    for block in blocks[1:]:  # Skip header
        # Find the actual code part (after the separator line)
        lines = block.split('\n')
        code_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('# ----'):
                code_start = i + 1
                break
        
        if code_start > 0:
            block_code = '\n'.join(lines[code_start:])
            names = extract_exported_names(block_code)
            all_names.update(names)
    
    # Sort names for consistent output, with private names (_) at end
    public_names = sorted([name for name in all_names if not name.startswith('_')])
    private_names = sorted([name for name in all_names if name.startswith('_')])
    all_names_sorted = public_names + private_names
    
    # Generate the __all__ string
    if not all_names_sorted:
        return "__all__ = []"
    
    all_str = "__all__ = [\n"
    for name in all_names_sorted:
        all_str += f"    '{name}',\n"
    all_str += "]"
    
    return all_str

def update_graveyard_all_list(graveyard_path):
    """Update the __all__ list in graveyard.py based on current content.
    
    Args:
        graveyard_path: Path to graveyard.py
    """
    with open(graveyard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new __all__ list
    new_all_list = generate_all_list(content)
    
    # Find where to insert/replace __all__
    lines = content.split('\n')
    all_start = None
    all_end = None
    
    # Look for existing __all__ definition
    for i, line in enumerate(lines):
        if line.strip().startswith('__all__'):
            all_start = i
            # Find the end of the __all__ definition
            bracket_count = line.count('[') - line.count(']')
            if bracket_count == 0:
                all_end = i
            else:
                j = i + 1
                while j < len(lines) and bracket_count > 0:
                    bracket_count += lines[j].count('[') - lines[j].count(']')
                    j += 1
                all_end = j - 1
            break
    
    if all_start is not None:
        # Replace existing __all__
        new_lines = lines[:all_start] + new_all_list.split('\n') + lines[all_end+1:]
    else:
        # Insert __all__ after the comment about automatic generation
        insert_point = None
        for i, line in enumerate(lines):
            if "automatically generated" in line.lower():
                insert_point = i + 1
                break
        
        if insert_point is not None:
            new_lines = lines[:insert_point] + [''] + new_all_list.split('\n') + [''] + lines[insert_point:]
        else:
            # Fallback: insert after docstring
            insert_point = 0
            for i, line in enumerate(lines):
                if '"""' in line:
                    insert_point = i + 1
                    break
            new_lines = lines[:insert_point] + [''] + new_all_list.split('\n') + [''] + lines[insert_point:]
    
    # Write back to file
    with open(graveyard_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✓ Updated __all__ list in graveyard.py with {len(new_all_list.split(','))} exported names")

def append_to_graveyard(graveyard_path, blocks):
    """Append processed blocks to graveyard.py.
    
    Args:
        graveyard_path: Path to graveyard.py
        blocks: List of processed code blocks
    """
    with open(graveyard_path, 'a', encoding='utf-8') as f:
        f.write('\n\n')
        f.write('# ' + '='*70 + '\n')
        f.write('# Code blocks moved from r.py\n')
        f.write('# ' + '='*70 + '\n')
        
        for i, (start_line, end_line, processed_block) in enumerate(blocks):
            f.write(f'\n\n# Block {i+1} - Originally from r.py lines {start_line+1}-{end_line+1}\n')
            f.write('# ' + '-'*60 + '\n\n')
            f.write(processed_block)
            f.write('\n')

def main():
    """Main refactoring function."""
    rpy_path = os.path.join(rp_path, 'r.py')
    graveyard_path = os.path.join(rp_path, 'libs', 'graveyard.py')
    
    if not os.path.exists(rpy_path):
        print(f"Error: r.py not found at {rpy_path}")
        return 1
    
    if not os.path.exists(graveyard_path):
        print(f"Error: graveyard.py not found at {graveyard_path}")
        return 1
    
    # Read r.py content
    print(f"Reading {rpy_path}...")
    with open(rpy_path, 'r', encoding='utf-8') as f:
        rpy_content = f.read()
    
    # Find graveyard blocks
    print("Searching for GRAVEYARD markers...")
    try:
        blocks = find_graveyard_blocks(rpy_content)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    if not blocks:
        print("No GRAVEYARD blocks found in r.py")
        return 0
    
    print(f"Found {len(blocks)} graveyard blocks:")
    for i, (start, end, content) in enumerate(blocks):
        lines_count = len(content.split('\n'))
        print(f"  Block {i+1}: lines {start+1}-{end+1} ({lines_count} lines of content)")
    
    # Process each block for graveyard
    print("Processing blocks for graveyard...")
    processed_blocks = []
    for start, end, content in blocks:
        processed_content = process_block_for_graveyard(content)
        processed_blocks.append((start, end, processed_content))
    
    # Remove blocks from r.py
    print("Removing blocks from r.py...")
    updated_rpy_content = remove_blocks_from_content(rpy_content, blocks)
    
    # Add graveyard import to r.py
    print("Checking graveyard import in r.py...")
    updated_rpy_content = add_graveyard_import_to_rpy(updated_rpy_content)
    
    # Write updated r.py
    print(f"Writing updated r.py...")
    with open(rpy_path, 'w', encoding='utf-8') as f:
        f.write(updated_rpy_content)
    
    # Append to graveyard
    print(f"Appending blocks to graveyard.py...")
    append_to_graveyard(graveyard_path, processed_blocks)
    
    # Update __all__ list to include all functions (including private ones)
    print("Updating __all__ list to export all functions including private ones...")
    update_graveyard_all_list(graveyard_path)
    
    print(f"✓ Successfully moved {len(blocks)} blocks to graveyard!")
    print(f"✓ Updated r.py with graveyard import")
    print(f"✓ Updated __all__ list to export private functions")
    print(f"✓ All functions remain accessible via graveyard import")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())