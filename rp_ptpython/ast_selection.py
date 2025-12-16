"""
AST-based smart selection for Python code.

Fallback for when tree-sitter is not available. Only works with valid syntax.
"""
from typing import List, Tuple, Optional, Set
import ast

from .selection_utils import (
    get_word_spans,
    get_string_content_spans,
    get_bracket_spans,
    get_line_spans,
    get_indent_paragraph_spans,
    get_comment_block_spans,
    find_next_span,
    contract,
)


def get_ast_spans(code: str) -> Set[Tuple[int, int]]:
    """Get spans from Python AST nodes."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return set()

    spans = set()
    lines = code.split('\n')

    def offset(lineno: int, col: int) -> int:
        return sum(len(line) + 1 for line in lines[:lineno - 1]) + col

    def visit(node):
        if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
            start = offset(node.lineno, node.col_offset)
            if hasattr(node, 'end_lineno') and hasattr(node, 'end_col_offset'):
                end = offset(node.end_lineno, node.end_col_offset)
            else:
                end = start + 1
            spans.add((start, end))
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return spans


def get_synthetic_spans(code: str) -> Set[Tuple[int, int]]:
    """Get all synthetic (non-AST) spans."""
    spans = set()
    spans |= get_word_spans(code)
    spans |= get_string_content_spans(code)
    spans |= get_bracket_spans(code)
    spans |= get_line_spans(code)
    spans |= get_indent_paragraph_spans(code)
    spans |= get_comment_block_spans(code)
    return spans


def expand_selection(
    code: str,
    start: int,
    end: int,
    history: List[Tuple[int, int]]
) -> Optional[Tuple[int, int, List[Tuple[int, int]]]]:
    """Expand selection to next span."""
    ast_spans = get_ast_spans(code)
    synthetic = get_synthetic_spans(code)
    all_spans = ast_spans | synthetic
    # For AST fallback, use all AST spans as atomic (stricter validation)
    result = find_next_span(start, end, all_spans, ast_spans, code=code)
    if result:
        return (result[0], result[1], history + [(start, end)])
    return None


def contract_selection(
    code: str,
    start: int,
    end: int,
    history: List[Tuple[int, int]]
) -> Optional[Tuple[int, int, List[Tuple[int, int]]]]:
    """Contract selection by popping history."""
    return contract(history)
