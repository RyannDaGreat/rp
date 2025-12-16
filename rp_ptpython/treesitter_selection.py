"""
Tree-sitter based smart selection for Python code.

Uses tree-sitter for robust parsing that handles broken/incomplete syntax.
Synthetic spans are only used when they don't skip AST nodes.
"""
from typing import List, Tuple, Optional, Set
import tree_sitter
import tree_sitter_python

from .selection_utils import (
    get_word_spans,
    get_string_content_spans,
    get_bracket_spans,
    get_line_spans,
    get_indent_paragraph_spans,
    get_comment_block_spans,
    find_next_span,
    breaks_atomic,
    contract,
)

_parser = None


def _get_parser():
    global _parser
    if _parser is None:
        lang = tree_sitter.Language(tree_sitter_python.language())
        _parser = tree_sitter.Parser(lang)
    return _parser


# Node types that are "atomic" - cannot be split by synthetic spans
ATOMIC_NODE_TYPES = {
    'string', 'string_start', 'string_content', 'string_end',
    'integer', 'float', 'true', 'false', 'none',
    'identifier', 'attribute',
}


def get_ast_spans_and_atomic(code: str) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    Get spans for all tree-sitter nodes, plus identify atomic spans.

    Returns:
        (all_spans, atomic_spans) - atomic spans are nodes that can't be split
    """
    tree = _get_parser().parse(bytes(code, 'utf8'))
    all_spans = set()
    atomic_spans = set()

    def visit(node):
        span = (node.start_byte, node.end_byte)
        all_spans.add(span)

        # Track atomic nodes
        if node.type in ATOMIC_NODE_TYPES:
            atomic_spans.add(span)

        # For block nodes, also add span including preceding comment siblings
        for i, child in enumerate(node.children):
            if child.type == 'block':
                start = child.start_byte
                for j in range(i - 1, -1, -1):
                    sib = node.children[j]
                    if sib.type == 'comment':
                        start = sib.start_byte
                    elif sib.type == ':':
                        continue
                    else:
                        break
                if start < child.start_byte:
                    all_spans.add((start, child.end_byte))

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return all_spans, atomic_spans


def get_ast_spans(code: str) -> Set[Tuple[int, int]]:
    """Get spans for all tree-sitter nodes, plus block+comment spans."""
    all_spans, _ = get_ast_spans_and_atomic(code)
    return all_spans


def get_statement_group_spans(code: str) -> Set[Tuple[int, int]]:
    """
    Get spans for consecutive statements NOT separated by blank lines.

    Uses tree-sitter to find statement-level children of block nodes,
    then groups consecutive ones together.
    """
    tree = _get_parser().parse(bytes(code, 'utf8'))
    spans = set()

    # Build line info for blank line detection
    lines = code.split('\n')
    line_starts = []
    offset = 0
    for line in lines:
        line_starts.append((offset, line))
        offset += len(line) + 1

    def is_blank_between(pos1: int, pos2: int) -> bool:
        """Check if there's a blank line between two positions."""
        for start, line in line_starts:
            if pos1 <= start < pos2:
                if not line.strip():
                    return True
        return False

    def visit(node):
        # Look for block nodes with multiple statement children
        if node.type == 'block':
            statements = [c for c in node.children if 'statement' in c.type or c.type == 'expression_statement']
            if len(statements) > 1:
                # Group consecutive statements not separated by blank lines
                group_start = None
                group_end = None
                for stmt in statements:
                    if group_start is None:
                        group_start = stmt.start_byte
                        group_end = stmt.end_byte
                    elif not is_blank_between(group_end, stmt.start_byte):
                        # Continue the group
                        group_end = stmt.end_byte
                    else:
                        # Blank line found - save current group and start new
                        if group_end > group_start:
                            spans.add((group_start, group_end))
                        group_start = stmt.start_byte
                        group_end = stmt.end_byte
                # Save final group
                if group_start is not None and group_end > group_start:
                    spans.add((group_start, group_end))

        for child in node.children:
            visit(child)

    visit(tree.root_node)
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
    spans |= get_statement_group_spans(code)
    return spans


def get_all_spans(code: str) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    Get all candidate spans and atomic spans for selection.

    Returns (all_spans, atomic_spans) where:
    - all_spans: union of AST spans + synthetic spans
    - atomic_spans: spans that can't be split (strings, identifiers)
    """
    ast_spans, atomic_spans = get_ast_spans_and_atomic(code)
    synthetic_spans = get_synthetic_spans(code)
    return ast_spans | synthetic_spans, atomic_spans


def expand_selection(
    code: str,
    start: int,
    end: int,
    history: List[Tuple[int, int]]
) -> Optional[Tuple[int, int, List[Tuple[int, int]]]]:
    """Expand selection to next span."""
    ast_spans, atomic_spans = get_ast_spans_and_atomic(code)
    synthetic_spans = get_synthetic_spans(code)
    all_spans = ast_spans | synthetic_spans
    result = find_next_span(start, end, all_spans, atomic_spans, ast_spans, code)
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
