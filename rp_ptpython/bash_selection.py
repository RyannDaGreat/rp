"""
Tree-sitter based smart selection for Bash code.

Uses tree-sitter-bash for robust parsing that handles incomplete syntax.
"""
from typing import List, Tuple, Optional, Set
import tree_sitter
import tree_sitter_bash

from .selection_utils import (
    get_word_spans,
    get_bracket_spans,
    get_line_spans,
    get_indent_paragraph_spans,
    find_next_span,
    contract,
)

_parser = None


def _get_parser():
    global _parser
    if _parser is None:
        lang = tree_sitter.Language(tree_sitter_bash.language())
        _parser = tree_sitter.Parser(lang)
    return _parser


# Node types that are "atomic" - cannot be split by synthetic spans
ATOMIC_NODE_TYPES = {
    'word', 'string', 'raw_string', 'ansii_c_string', 'heredoc_body',
    'number', 'variable_name', 'special_variable_name',
    'simple_expansion', 'expansion',
}


def get_bash_string_content_spans(code: str) -> Set[Tuple[int, int]]:
    """Spans for string contents (without quotes) in bash."""
    spans, i = set(), 0
    while i < len(code):
        if code[i] == '"':
            # Double quote - find matching
            j = i + 1
            while j < len(code) and code[j] != '"':
                if code[j] == '\\' and j + 1 < len(code):
                    j += 2
                else:
                    j += 1
            if j < len(code) and j > i + 1:
                spans.add((i + 1, j))
            i = j + 1 if j < len(code) else j
        elif code[i] == "'":
            # Single quote - literal, no escapes
            j = i + 1
            while j < len(code) and code[j] != "'":
                j += 1
            if j < len(code) and j > i + 1:
                spans.add((i + 1, j))
            i = j + 1 if j < len(code) else j
        elif code[i] == '$' and i + 1 < len(code) and code[i + 1] == "'":
            # $'...' ANSI-C quoting
            j = i + 2
            while j < len(code) and code[j] != "'":
                if code[j] == '\\' and j + 1 < len(code):
                    j += 2
                else:
                    j += 1
            if j < len(code) and j > i + 2:
                spans.add((i + 2, j))
            i = j + 1 if j < len(code) else j
        else:
            i += 1
    return spans


def get_bash_comment_block_spans(code: str) -> Set[Tuple[int, int]]:
    """Spans for contiguous comment blocks."""
    spans, offset, start, end = set(), 0, None, None
    for line in code.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#') and not stripped.startswith('#!'):
            if start is None:
                start = offset
            end = offset + len(line)
        elif start is not None:
            spans.add((start, end))
            start = None
        offset += len(line) + 1
    if start is not None:
        spans.add((start, end))
    return spans


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

        if node.type in ATOMIC_NODE_TYPES:
            atomic_spans.add(span)

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return all_spans, atomic_spans


def get_ast_spans(code: str) -> Set[Tuple[int, int]]:
    """Get spans for all tree-sitter nodes."""
    all_spans, _ = get_ast_spans_and_atomic(code)
    return all_spans


def get_pipe_sequence_spans(code: str) -> Set[Tuple[int, int]]:
    """Get spans for individual commands in a pipeline."""
    tree = _get_parser().parse(bytes(code, 'utf8'))
    spans = set()

    def visit(node):
        # For pipelines, add each command as a span
        if node.type == 'pipeline':
            for child in node.children:
                if child.type not in ('|', '|&'):
                    spans.add((child.start_byte, child.end_byte))

        # For command lists (&&, ||, ;)
        if node.type == 'list':
            for child in node.children:
                if child.type not in ('&&', '||', ';'):
                    spans.add((child.start_byte, child.end_byte))

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return spans


def get_synthetic_spans(code: str) -> Set[Tuple[int, int]]:
    """Get all synthetic (non-AST) spans for bash."""
    spans = set()
    spans |= get_word_spans(code)
    spans |= get_bash_string_content_spans(code)
    spans |= get_bracket_spans(code)
    spans |= get_line_spans(code)
    spans |= get_indent_paragraph_spans(code)
    spans |= get_bash_comment_block_spans(code)
    spans |= get_pipe_sequence_spans(code)
    return spans


def get_all_spans(code: str) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    Get all candidate spans and atomic spans for selection.

    Returns (all_spans, atomic_spans)
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
