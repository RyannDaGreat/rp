"""
Pure functional AST-based smart selection for Python code.

This module provides pure functions for expanding and contracting text selections
based on Python's Abstract Syntax Tree structure.

Architecture:
    1. Core AST extraction (get_pure_ast_spans) - No synthetic spans
    2. Composable rules that augment/modify expansions:
       - Bracket rule (add_bracket_spans) - Adds granular bracket selection
       - Line rule (apply_line_expansion_rule) - Ensures full line before multi-line
    3. Main expansion logic (expand_selection) - Composes everything

This makes rules independent, testable, and easy to enable/disable.
"""
from typing import List, Tuple, Optional
import ast


# ============================================================================
# Core AST Spans (no synthetic rules)
# ============================================================================

def get_pure_ast_spans(code: str) -> List[Tuple[int, int]]:
    """
    Get AST node spans only (no synthetic spans).

    Pure AST extraction with no additional rules applied.

    Args:
        code: Python source code

    Returns:
        List of (start, end) position tuples from AST nodes only

    >>> code = "x = 5"
    >>> spans = get_pure_ast_spans(code)
    >>> len(spans) > 0
    True
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    spans = []

    def visit_node(node):
        if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
            lines = code.split('\n')
            start_offset = sum(len(line) + 1 for line in lines[:node.lineno - 1]) + node.col_offset

            if hasattr(node, 'end_lineno') and hasattr(node, 'end_col_offset'):
                end_offset = sum(len(line) + 1 for line in lines[:node.end_lineno - 1]) + node.end_col_offset
            else:
                end_offset = start_offset + 1

            spans.append((start_offset, end_offset))

        for child in ast.iter_child_nodes(node):
            visit_node(child)

    visit_node(tree)
    return spans


# ============================================================================
# Bracket/Paren Rule (Composable)
# ============================================================================

def add_bracket_spans(code: str, spans: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Add synthetic spans for bracket/paren contents.

    This is a composable rule that adds granular selection for:
    - Content inside brackets: "bar" in "foo[bar]"
    - Brackets + content: "[bar]" in "foo[bar]"

    Args:
        code: Source code
        spans: Existing spans to augment

    Returns:
        Original spans plus bracket-related synthetic spans

    >>> code = "foo[bar]"
    >>> base_spans = [(0, 8), (0, 3), (4, 7)]  # foo[bar], foo, bar
    >>> result = add_bracket_spans(code, base_spans)
    >>> len(result) > len(base_spans)
    True
    """
    new_spans = list(spans)  # Copy to avoid mutation

    bracket_pairs = {'(': ')', '[': ']', '{': '}'}
    for open_char, close_char in bracket_pairs.items():
        i = 0
        while i < len(code):
            if code[i] == open_char:
                depth = 1
                j = i + 1
                while j < len(code) and depth > 0:
                    if code[j] == open_char:
                        depth += 1
                    elif code[j] == close_char:
                        depth -= 1
                    j += 1

                if depth == 0:
                    # Add span for content inside brackets (excluding brackets)
                    inner_start = i + 1
                    inner_end = j - 1
                    if inner_start < inner_end:
                        new_spans.append((inner_start, inner_end))
                    # Add span for brackets + content
                    new_spans.append((i, j))
            i += 1

    return new_spans


def get_ast_spans(code: str) -> List[Tuple[int, int]]:
    """
    Get all AST spans with bracket rule applied.

    This composes pure AST spans with bracket rules.

    Args:
        code: Python source code

    Returns:
        List of (start, end) position tuples

    >>> code = "x = foo[bar]"
    >>> spans = get_ast_spans(code)
    >>> len(spans) > 0
    True
    """
    base_spans = get_pure_ast_spans(code)
    return add_bracket_spans(code, base_spans)


# ============================================================================
# Line Expansion Rule (Composable)
# ============================================================================

def count_lines_in_span(code: str, start: int, end: int) -> int:
    """
    Count number of lines spanned by [start, end).

    Args:
        code: Source code
        start: Start position
        end: End position

    Returns:
        Number of lines (minimum 1)

    >>> count_lines_in_span("hello\\nworld", 0, 5)
    1
    >>> count_lines_in_span("hello\\nworld", 0, 11)
    2
    >>> count_lines_in_span("a\\nb\\nc", 0, 5)
    3
    """
    if start >= end:
        return 1
    return code[start:end].count('\n') + 1


def spans_complete_lines(code: str, start: int, end: int) -> bool:
    """
    Check if selection spans complete lines (from line start to line end).

    Args:
        code: Source code
        start: Start position
        end: End position

    Returns:
        True if selection covers complete lines

    >>> spans_complete_lines("hello\\nworld", 0, 11)
    True
    >>> spans_complete_lines("  hello", 2, 7)
    False
    >>> spans_complete_lines("  hello", 0, 7)
    True
    """
    if start >= end:
        return False

    # Check if start is at beginning of line
    starts_at_line_start = (start == 0) or (code[start - 1] == '\n')

    # Check if end is at end of line
    ends_at_line_end = (end >= len(code)) or (code[end] == '\n')

    return starts_at_line_start and ends_at_line_end


def get_full_lines_span(code: str, start: int, end: int) -> Tuple[int, int]:
    """
    Expand selection to cover complete lines.

    Args:
        code: Source code
        start: Current start position
        end: Current end position

    Returns:
        (new_start, new_end) covering complete lines

    >>> get_full_lines_span("hello\\nworld\\nfoo", 6, 11)
    (6, 11)
    >>> get_full_lines_span("  hello", 2, 7)
    (0, 7)
    """
    # Find start of first line
    new_start = start
    while new_start > 0 and code[new_start - 1] != '\n':
        new_start -= 1

    # Find end of last line
    new_end = end
    while new_end < len(code) and code[new_end] != '\n':
        new_end += 1

    return (new_start, new_end)


def apply_line_expansion_rule(
    code: str,
    current_start: int,
    current_end: int,
    new_start: int,
    new_end: int
) -> Optional[Tuple[int, int]]:
    """
    Apply line expansion rule: when expanding from N lines to >N lines,
    must first select complete lines.

    This is a composable rule that can intercept expansions.

    Args:
        code: Source code
        current_start: Current selection start
        current_end: Current selection end
        new_start: Proposed next selection start
        new_end: Proposed next selection end

    Returns:
        Modified (start, end) if rule applies, or None to use original next selection

    >>> code = "  print()\\nother()"
    >>> # Expanding from 'print()' to multiple lines
    >>> result = apply_line_expansion_rule(code, 2, 9, 0, 17)
    >>> result  # Should return full line first
    (0, 9)
    """
    current_lines = count_lines_in_span(code, current_start, current_end)
    new_lines = count_lines_in_span(code, new_start, new_end)

    # If expanding to more lines AND current selection doesn't span complete lines,
    # insert intermediate step to select complete lines first
    if new_lines > current_lines and not spans_complete_lines(code, current_start, current_end):
        full_line_start, full_line_end = get_full_lines_span(code, current_start, current_end)

        # Only insert intermediate step if it's actually different from current selection
        if (full_line_start, full_line_end) != (current_start, current_end):
            return (full_line_start, full_line_end)

    # Rule doesn't apply - return None to indicate no modification
    return None


def find_new_larger_span(spans: List[Tuple[int, int]], start: int, end: int) -> Optional[Tuple[int, int]]:
    """
    Find the next larger span that contains [start, end).

    Args:
        spans: List of (start, end) tuples
        start: Current selection start
        end: Current selection end

    Returns:
        (new_start, new_end) or None if no larger span exists

    >>> spans = [(0, 3), (0, 10), (0, 20)]
    >>> find_new_larger_span(spans, 0, 3)
    (0, 10)
    >>> find_new_larger_span(spans, 0, 20)
    """
    # Find all spans that contain current selection
    if start == end:
        candidates = [(s, e) for s, e in spans if s <= start <= e]
    else:
        candidates = [(s, e) for s, e in spans if s <= start and end <= e]

    # Remove duplicates and sort by size
    candidates = sorted(set(candidates), key=lambda x: x[1] - x[0])

    if start == end:
        return candidates[0] if candidates else None

    # Find next larger
    current_size = end - start
    for s, e in candidates:
        if (e - s) > current_size:
            return (s, e)

    return None


def expand_selection(
    code: str,
    start: int,
    end: int,
    history: List[Tuple[int, int]]
) -> Optional[Tuple[int, int, List[Tuple[int, int]]]]:
    """
    Expand selection to next larger AST node.

    Composes AST spans with bracket rule and line expansion rule.

    Pure function: takes immutable inputs, returns new data, no side effects.

    Args:
        code: Source code
        start: Current selection start position
        end: Current selection end position
        history: List of previous selections (oldest first)

    Returns:
        (new_start, new_end, new_history) tuple, or None if can't expand

    >>> code = "x = 5"
    >>> result = expand_selection(code, 0, 1, [])
    >>> result is not None
    True
    """
    # Get spans (already has bracket rule applied via get_ast_spans)
    spans = get_ast_spans(code)
    if not spans:
        return None

    # Find next larger span
    result = find_new_larger_span(spans, start, end)
    if result is None:
        return None

    new_start, new_end = result

    #TODO: Only apply this rule IF the selection we would get with line expansion is a SUBSET of what we would get if we expanded again ignoring this rule 
    # # Apply line expansion rule (may modify the expansion)
    # line_rule_result = apply_line_expansion_rule(code, start, end, new_start, new_end)
    # if line_rule_result is not None:
    #     # Line rule intercepts - use its result
    #     new_start, new_end = line_rule_result
    # else:
    #     # No interception - use original next span
    #     new_start, new_end = new_start, new_end

    # Return with updated history
    new_history = history + [(start, end)]
    return (new_start, new_end, new_history)


def contract_selection(
    code: str,
    start: int,
    end: int,
    history: List[Tuple[int, int]]
) -> Optional[Tuple[int, int, List[Tuple[int, int]]]]:
    """
    Contract selection to previous state from history.

    Pure function: takes immutable inputs, returns new data, no side effects.

    Args:
        code: Source code (unused but kept for symmetry with expand_selection)
        start: Current selection start position
        end: Current selection end position
        history: List of previous selections (oldest first)

    Returns:
        (new_start, new_end, new_history) tuple, or None if history is empty

    >>> history = [(0, 1), (0, 5)]
    >>> result = contract_selection("x = 5", 0, 10, history)
    >>> result
    (0, 5, [(0, 1)])
    """
    if not history:
        return None

    # Pop last item from history
    new_history = history[:-1]
    prev_start, prev_end = history[-1]

    return (prev_start, prev_end, new_history)


# if __name__ == "__main__":
#     # Simple test
#     test_code = "result = foo[bar]"
#     print(f"Test code: {repr(test_code)}")
#     print("\nExpanding from middle of 'bar':")
#     start, end = 14, 14  # Middle of 'bar'
#     history = []
#     for i in range(6):
#         result = expand_selection(test_code, start, end, history)
#         if result:
#             start, end, history = result
#             print(f"  {i+1}. [{start}:{end}] = {repr(test_code[start:end])}")
#         else:
#             print(f"  {i+1}. Can't expand further")
#             break
#     print("\nContracting back:")
#     while True:
#         result = contract_selection(test_code, start, end, history)
#         if result:
#             start, end, history = result
#             if start == end:
#                 print(f"  → cursor at {start}")
#             else:
#                 print(f"  → [{start}:{end}] = {repr(test_code[start:end])}")
#         else:
#             print(f"  → no more history")
#             break
