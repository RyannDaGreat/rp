"""Span-based selection utilities."""
from typing import List, Tuple, Optional, Set

Span = Tuple[int, int]


def get_word_spans(code: str) -> Set[Span]:
    """Spans for words/identifiers."""
    spans, i = set(), 0
    while i < len(code):
        if code[i].isalnum() or code[i] == '_':
            start = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1
            spans.add((start, i))
        else:
            i += 1
    return spans


def get_string_content_spans(code: str) -> Set[Span]:
    """Spans for string contents (without quotes)."""
    spans, i = set(), 0
    while i < len(code):
        if code[i] in '"\'':
            q = code[i]
            if code[i:i+3] == q * 3:  # Triple quote
                j = i + 3
                while j + 2 < len(code) and code[j:j+3] != q * 3:
                    j += 1
                if j + 2 < len(code) and j > i + 3:
                    spans.add((i + 3, j))
                i = j + 3 if j + 2 < len(code) else j
            else:  # Single quote
                j = i + 1
                while j < len(code) and code[j] != q and code[j] != '\n':
                    j += 2 if code[j] == '\\' and j + 1 < len(code) else 1
                if j < len(code) and code[j] == q and j > i + 1:
                    spans.add((i + 1, j))
                i = j + 1 if j < len(code) and code[j] == q else j
        else:
            i += 1
    return spans


def get_bracket_spans(code: str) -> Set[Span]:
    """Spans for bracket contents and brackets+contents."""
    spans = set()
    for op, cl in [('(', ')'), ('[', ']'), ('{', '}')]:
        i = 0
        while i < len(code):
            if code[i] == op:
                depth, j = 1, i + 1
                while j < len(code) and depth > 0:
                    depth += (code[j] == op) - (code[j] == cl)
                    j += 1
                if depth == 0:
                    if j - 1 > i + 1:
                        spans.add((i + 1, j - 1))
                    spans.add((i, j))
            i += 1
    return spans


def get_line_spans(code: str) -> Set[Span]:
    """Spans for each non-empty line (with and without leading indent)."""
    spans, offset = set(), 0
    for line in code.split('\n'):
        if line.strip():
            spans.add((offset, offset + len(line)))  # Full line with indent
            indent = len(line) - len(line.lstrip())
            if indent:
                spans.add((offset + indent, offset + len(line)))  # Without indent
        offset += len(line) + 1
    return spans


def get_comment_block_spans(code: str) -> Set[Span]:
    """Spans for contiguous comment blocks."""
    spans, offset, start, end = set(), 0, None, None
    for line in code.split('\n'):
        if line.strip().startswith('#'):
            if start is None:
                start = offset
            end = offset + len(line)
        elif start is not None:
            spans.add((start, end))
            indent = len(line) - len(line.lstrip()) if line.strip() else 0
            if indent and start + indent < end:
                spans.add((start + indent, end))
            start = None
        offset += len(line) + 1
    if start is not None:
        spans.add((start, end))
    return spans


def get_indent_paragraph_spans(code: str) -> Set[Span]:
    """Spans for contiguous multi-line blocks at same indent level (3+ lines)."""
    spans, offset = set(), 0
    start, start_no_indent, end, indent, line_count = None, None, None, -1, 0

    for line in code.split('\n'):
        line_end = offset + len(line)
        stripped = line.strip()

        if not stripped:
            if start is not None and line_count >= 3:  # Only 3+ lines
                spans.add((start, end))
                if start_no_indent:
                    spans.add((start_no_indent, end))
            start = None
            line_count = 0
        else:
            line_indent = len(line) - len(stripped)
            if start is None or line_indent != indent:
                if start is not None and line_count >= 3:  # Only 3+ lines
                    spans.add((start, end))
                    if start_no_indent:
                        spans.add((start_no_indent, end))
                start, start_no_indent = offset, offset + line_indent
                indent = line_indent
                line_count = 1
            else:
                line_count += 1
            end = line_end
        offset = line_end + 1

    if start is not None and line_count >= 3:  # Only 3+ lines
        spans.add((start, end))
        if start_no_indent:
            spans.add((start_no_indent, end))
    return spans


def breaks_atomic(span: Span, atomic: Set[Span]) -> bool:
    """Check if span partially overlaps any atomic span."""
    s, e = span
    for a_s, a_e in atomic:
        if not (e <= a_s or s >= a_e or (a_s <= s and e <= a_e) or (s <= a_s and a_e <= e)):
            return True
    return False


def _contained_by_ast(span: Span, ast_spans: Set[Span]) -> bool:
    """Check if span is fully contained by some AST span."""
    s, e = span
    return any(a_s <= s and e <= a_e for a_s, a_e in ast_spans)


def find_next_span(
    start: int, end: int,
    all_spans: Set[Span],
    atomic: Set[Span],
    ast_spans: Optional[Set[Span]] = None,
    code: Optional[str] = None
) -> Optional[Span]:
    """Find smallest span strictly containing [start, end)."""
    ast_spans = ast_spans or set()
    size = end - start

    # If selection starts with whitespace, also consider its non-whitespace start
    content_start = start
    if code and start < end:
        while content_start < end and code[content_start] in ' \t':
            content_start += 1

    def contains(sp: Span) -> bool:
        """Check if span contains current selection (allowing whitespace prefix)."""
        if sp[1] - sp[0] <= size:
            return False
        # Normal containment
        if sp[0] <= start and end <= sp[1]:
            return True
        # Allow if span contains content (after whitespace)
        if content_start > start and sp[0] <= content_start and end <= sp[1]:
            return True
        return False

    # Get containing candidates, sorted by size
    cands = sorted(
        [sp for sp in all_spans if contains(sp)],
        key=lambda x: (x[1] - x[0], x[0])
    ) if start != end else sorted(
        [sp for sp in all_spans if sp[0] <= start < sp[1]],
        key=lambda x: (x[1] - x[0], x[0])
    )

    # Filter: AST spans always ok, synthetics must be contained by some AST span
    cands = [sp for sp in cands if sp in ast_spans or _contained_by_ast(sp, ast_spans)]

    # Return first non-breaking span
    return next((sp for sp in cands if not breaks_atomic(sp, atomic)), None)


def contract(history: List[Span]) -> Optional[Tuple[int, int, List[Span]]]:
    """Contract selection by popping history."""
    return (*history[-1], history[:-1]) if history else None
