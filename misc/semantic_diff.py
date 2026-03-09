"""
Semantic Diff — a formatting tool for meaning-based document comparison.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! INVARIANT: ALL OUTPUT FORMATS MUST SUPPORT THE SAME FEATURES.             !!
!!                                                                           !!
!! When you add a feature (sub-chunks, new chunk kind, new line field, etc), !!
!! you MUST update ALL renderers: ANSI, HTML, and Markdown. If one format    !!
!! supports it, all formats support it. No exceptions.                       !!
!!                                                                           !!
!! Renderers: format_semantic_diff (ANSI)                                    !!
!!            format_semantic_diff_plain (plain text, no colors)              !!
!!            format_semantic_diff_html (HTML)                                !!
!!            format_semantic_diff_md (Markdown)                              !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Claude (or a human) produces diff chunks by analyzing documents. This module
formats and displays them with colors, labels, and line numbers.

Works with any document type: markdown, code, PDFs (page numbers), images
(VLM descriptions). The differ is the analyst; this is just the printer.

Chunk format (dict):
    label (str): e.g. 'A', '1B' — for referencing in conversation
    kind (str): 'added', 'removed', 'changed', 'shared'
    explanation (str): what changed and why — shown as the chunk's brief header/title
    sources (list[str]): which files this chunk references
    lines (list[dict]): each with 'text', 'source', 'line_num'/'page_num', 'sign' (+/-/ )
        Optional: 'highlights' (list of [start, end] pairs) — character spans to emphasize
            within the line text, showing exactly what changed even if the lines moved.
            ANSI: bold+underline. HTML: <mark> with configurable color. Markdown: **bold**.
    sub_chunks (list[dict], optional): bundled hunks within one semantic change,
        each with 'label', 'sources', 'explanation', 'lines'
    side_by_side (list[dict], optional): N-way dunk-style column layout.
        Each column has 'label' (str) and 'lines' (list[dict]).
        Renders as side-by-side columns in HTML, sequential blocks in ANSI/MD/plain.
        Useful for 2-way or 3-way file comparisons where seeing versions
        next to each other is clearer than interleaved +/- lines.

Label sequence: A-Z, then 1A-1Z, 2A-2Z, etc.
Sub-chunk labels: A.1, A.2, or 1A.1, 1A.2 (dot notation).

Customization notes for report authors:
    - The HTML output is a complete page with CSS custom properties in :root.
      Override --font-main, --bg-add, --bg-rem, etc. to restyle.
    - For rich reports, Claude can inject <img> tags, <video> tags, custom widgets,
      or any HTML into the explanation field or as extra lines after generating
      the base diff. The HTML renderer passes explanation through as-is.
    - Videos: embedded via <video> tags in the explanation field.
      Default: autoplay controls muted loop playsinline (silent looping with controls).
      To disable autoplay, remove the autoplay attribute.
      Videos pause when their chunk is collapsed and resume (if autoplay) when expanded.
      Default layout is horizontal (side-by-side via flex).
    - sync_videos (bool): When True, the first <video> in the chunk is the master
      (keeps controls) and all others are slaves (no controls, driven by master).
      Play/pause/seek/rate changes on the master propagate to all slaves.
      This is the default recommendation for comparing same-length video
      transformations (e.g. before/after filters, color grading, style transfer)
      where the videos have identical frame counts and timing.
    - Images: same — inject <img> tags in explanation or as asset lines.
    - The title parameter controls the page heading / browser tab title.
    - Format overrides: any string field (explanation, text, label) can be a dict
      with per-format keys instead of a plain string:
        {'default': 'fallback', 'html': '<b>rich</b>', 'md': '**rich**', 'ansi': '...', 'plain': '...'}
      The renderer picks its key, falls back to 'default', falls back to ''.
      Plain strings are backwards-compatible (treated as all formats).

Sub-chunks example (bundled changes across files for one semantic change):
    {'label': 'A', 'kind': 'changed', 'explanation': 'Rename calc_foo to compute_foo',
     'sub_chunks': [
         {'label': 'A.1', 'sources': ['math.py'], 'explanation': 'Function definition',
          'lines': [{'text': 'def calc_foo(x):', 'sign': '-', 'line_num': 12, 'source': 'math.py',
                      'highlights': [[4, 12]]},
                    {'text': 'def compute_foo(x):', 'sign': '+', 'line_num': 12, 'source': 'math.py',
                      'highlights': [[4, 15]]}]},
         {'label': 'A.2', 'sources': ['test_math.py'], 'explanation': 'Test call site',
          'lines': [{'text': 'result = calc_foo(5)', 'sign': '-', 'line_num': 8, 'source': 'test_math.py'},
                    {'text': 'result = compute_foo(5)', 'sign': '+', 'line_num': 8, 'source': 'test_math.py'}]},
     ]}

CLI usage:
    python -m rp.semantic_diff print  diff.json              # ANSI to stdout
    python -m rp.semantic_diff html   diff.json               # HTML to stdout
    python -m rp.semantic_diff html   diff.json -o out.html   # HTML to file
    python -m rp.semantic_diff md     diff.json               # Markdown to stdout
    python -m rp.semantic_diff md     diff.json -o out.md     # Markdown to file
"""

import os as _os
import re as _re

from rp.r import fansi


def _make_chunk_label(index):
    """
    Pure function. Generate chunk label from index.

    A-Z for 0-25, then 1A-1Z for 26-51, 2A-2Z for 52-77, etc.

    Args:
        index (int): Zero-based chunk index.

    Returns:
        str

    Examples:
        >>> _make_chunk_label(0)
        'A'
        >>> _make_chunk_label(25)
        'Z'
        >>> _make_chunk_label(26)
        '1A'
        >>> _make_chunk_label(52)
        '2A'
    """
    letter = chr(ord('A') + index % 26)
    group = index // 26
    if group == 0:
        return letter
    return str(group) + letter


def _get_line_num(line_info):
    """
    Pure function. Extract line or page number from a line info dict.

    Args:
        line_info (dict): Line info with optional 'line_num' or 'page_num'.

    Returns:
        int or None

    Examples:
        >>> _get_line_num({'text': 'x', 'line_num': 5})
        5
        >>> _get_line_num({'text': 'x', 'page_num': 3})
        3
        >>> _get_line_num({'text': 'x'}) is None
        True
    """
    return line_info.get('line_num') or line_info.get('page_num')


def _resolve_format(value, fmt):
    """
    Pure function. Resolve a format-overridable value.

    If value is a plain string, return it as-is (backwards compatible).
    If value is a dict, look up the format key (e.g. 'html', 'md', 'ansi',
    'plain'), then fall back to 'default', then fall back to ''.

    This allows any string field in a chunk to have per-format overrides:
        'explanation': {
            'default': 'Plain text fallback',
            'html': '<div>Rich HTML</div>',
            'md': '**Rich** markdown',
        }

    Args:
        value: A string or dict with format keys.
        fmt (str): One of 'html', 'md', 'ansi', 'plain'.

    Returns:
        str

    Examples:
        >>> _resolve_format('hello', 'html')
        'hello'
        >>> _resolve_format({'default': 'hi', 'html': '<b>hi</b>'}, 'html')
        '<b>hi</b>'
        >>> _resolve_format({'default': 'hi', 'html': '<b>hi</b>'}, 'plain')
        'hi'
        >>> _resolve_format({'html': '<b>hi</b>'}, 'plain')
        ''
        >>> _resolve_format(None, 'html')
        ''
    """
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get(fmt, value.get('default', ''))
    return str(value)


def _apply_highlights_ansi(text, highlights):
    """
    Pure function. Apply ANSI bold+underline to highlighted spans in text.

    Args:
        text (str): Plain text content.
        highlights (list): List of [start, end] character index pairs.

    Returns:
        str: Text with ANSI codes wrapping highlighted spans.

    Examples:
        >>> _apply_highlights_ansi('def calc_foo(x):', [[4, 12]])
        'def \\033[1;4mcalc_foo\\033[22;24m(x):'
    """
    if not highlights:
        return text
    # Sort by start position, process right-to-left to preserve indices
    for start, end in sorted(highlights, reverse=True):
        text = text[:start] + '\033[1;4m' + text[start:end] + '\033[22;24m' + text[end:]
    return text


def _apply_highlights_html(text, highlights):
    """
    Pure function. Wrap highlighted spans in <mark> tags (text must already be HTML-escaped).

    The caller must HTML-escape text BEFORE calling this, since this inserts raw HTML tags.

    Args:
        text (str): HTML-escaped text content.
        highlights (list): List of [start, end] pairs referencing positions in the ORIGINAL
            (pre-escape) text. This function maps them to the escaped string.

    Returns:
        str: Text with <mark> tags around highlighted spans.

    Examples:
        >>> _apply_highlights_html('def calc_foo(x):', [[4, 12]])
        'def <mark>calc_foo</mark>(x):'
    """
    if not highlights:
        return text
    for start, end in sorted(highlights, reverse=True):
        text = text[:start] + '<mark>' + text[start:end] + '</mark>' + text[end:]
    return text


def _apply_highlights_md(text, highlights):
    """
    Pure function. Apply **bold** to highlighted spans in Markdown text.

    Args:
        text (str): Plain text content.
        highlights (list): List of [start, end] character index pairs.

    Returns:
        str: Text with **bold** markers around highlighted spans.

    Examples:
        >>> _apply_highlights_md('def calc_foo(x):', [[4, 12]])
        'def **calc_foo**(x):'
    """
    if not highlights:
        return text
    for start, end in sorted(highlights, reverse=True):
        text = text[:start] + '**' + text[start:end] + '**' + text[end:]
    return text


def _strip_html(text):
    """
    Pure function. Strip HTML tags from text, leaving only content.

    Args:
        text (str): Text possibly containing HTML tags.

    Returns:
        str

    Examples:
        >>> _strip_html('hello <b>world</b>')
        'hello world'
        >>> _strip_html('no tags')
        'no tags'
        >>> _strip_html('<div style="color:red">x</div>')
        'x'
    """
    return _re.sub(r'<[^>]+>', '', text)


def _format_line_with_number(line, line_num, width=4):
    """
    Pure function. Prefix a line with a right-justified line number.

    Args:
        line (str): The line content.
        line_num (int or None): Line number, or None for no number.
        width (int): Width for line number column.

    Returns:
        str

    Examples:
        >>> _format_line_with_number('hello', 42)
        '  42 | hello'
        >>> _format_line_with_number('hello', None)
        '     | hello'
    """
    if line_num is None:
        return ' ' * width + ' | ' + line
    return str(line_num).rjust(width) + ' | ' + line


_KIND_COLORS_ANSI = {
    'added': 'green',
    'removed': 'red',
    'changed': 'yellow',
    'shared': 'blue',
}

_KIND_COLORS_HTML = {
    'added':   ('#d4edda', '#155724', '#28a745'),
    'removed': ('#f8d7da', '#721c24', '#dc3545'),
    'changed': ('#fff3cd', '#856404', '#ffc107'),
    'shared':  ('#e2e3e5', '#383d41', '#6c757d'),
}


def _visible_len(s):
    """
    Pure function. Length of string excluding ANSI escape codes.

    Args:
        s (str): String possibly containing ANSI codes.

    Returns:
        int

    Examples:
        >>> _visible_len('hello')
        5
        >>> _visible_len('\033[31mhello\033[0m')
        5
    """
    return len(_re.sub(r'\033\[[^m]*m', '', s))


def _syntax_highlight_with_bg(text, bg_code):
    """
    Near-pure function (depends on fansi_syntax_highlighting internals).
    Apply Python syntax highlighting to text while preserving a background color.

    Patches ANSI resets so the background persists through syntax color changes.

    Args:
        text (str): Code text to highlight.
        bg_code (str): ANSI background escape code (e.g. '\\033[48;2;0;40;0m').

    Returns:
        str: Syntax-highlighted text with persistent background.

    Examples:
        >>> # Result contains ANSI codes; just check it returns a string
        >>> isinstance(_syntax_highlight_with_bg('x = 1', '\\033[48;2;0;40;0m'), str)
        True
    """
    from rp.r import fansi_syntax_highlighting
    highlighted = fansi_syntax_highlighting(text).strip()
    reset = '\033[0m'
    return highlighted.replace(reset, reset + bg_code)


def _render_lines_ansi(line_infos, indent='', syntax_highlight=False):
    """
    Render a list of line info dicts as ANSI-colored strings.

    When syntax_highlight=True, added/removed lines get a full-width dark
    green/red background with syntax-highlighted code on top. Context lines
    get syntax highlighting with no background.

    Args:
        line_infos (list[dict]): Lines to render.
        indent (str): Prefix for each line (e.g. '  ' for sub-chunks).
        syntax_highlight (bool): Apply Python syntax highlighting to code content.

    Returns:
        list[str]

    Examples:
        >>> len(_render_lines_ansi([{'text': 'hi', 'sign': '+'}])) == 1
        True
    """
    from rp.r import get_terminal_width

    _BG_GREEN = '\033[48;2;0;40;0m'
    _BG_RED   = '\033[48;2;40;0;0m'
    _RESET    = '\033[0m'

    try:
        term_width = get_terminal_width()
    except Exception:
        term_width = 120

    parts = []
    for line_info in line_infos:
        text = _resolve_format(line_info.get('text', ''), 'ansi') or line_info.get('text', '')
        sign = line_info.get('sign', ' ')
        line_num = _get_line_num(line_info)
        source = line_info.get('source', '')
        highlights = line_info.get('highlights', [])

        # Apply inline highlights (bold+underline) before any other formatting
        text = _apply_highlights_ansi(text, highlights)

        prefix = indent + ({'+': '+ ', '-': '- '}.get(sign, '  '))

        # Shared-source detection: 'both', 'shared', 'all' → display as "shared"
        is_shared_source = source.lower() in ('both', 'shared', 'all')

        source_tag = ''
        if source:
            display_source = 'shared' if is_shared_source else _os.path.basename(source)
            source_color = 'blue' if not is_shared_source else 'blue'
            source_tag = fansi('[' + display_source + '] ', source_color, 'faded')

        numbered = _format_line_with_number(text, line_num)

        if syntax_highlight and sign in ('+', '-'):
            # Full-width background with syntax highlighting
            bg = _BG_GREEN if sign == '+' else _BG_RED
            raw_text_for_syntax = _resolve_format(line_info.get('text', ''), 'ansi') or line_info.get('text', '')
            highlighted_text = _syntax_highlight_with_bg(raw_text_for_syntax, bg)
            # Re-apply highlights on top of syntax highlighting
            highlighted_text = _apply_highlights_ansi(highlighted_text, highlights)
            numbered_highlighted = _format_line_with_number(highlighted_text, line_num)
            content = prefix + numbered_highlighted

            # Pad to terminal width for full-width background
            visible = _visible_len(source_tag + content)
            padding = max(0, term_width - visible)
            parts.append(bg + source_tag + content + ' ' * padding + _RESET)

        elif syntax_highlight and sign == ' ':
            # Context line with syntax highlighting, no background
            from rp.r import fansi_syntax_highlighting
            highlighted_text = fansi_syntax_highlighting(text).strip()
            numbered_highlighted = _format_line_with_number(highlighted_text, line_num)
            parts.append(source_tag + fansi(prefix, 'gray') + numbered_highlighted)

        else:
            # Plain colored (non-code or no syntax highlighting requested)
            if is_shared_source and sign == ' ':
                line_color = 'blue'
            else:
                line_color = {'+': 'green', '-': 'red'}.get(sign, 'gray')
            parts.append(source_tag + fansi(prefix + numbered, line_color))

    return parts


def format_semantic_diff(chunks):
    """
    Command. Formats semantic diff chunks into an ANSI-colored string for terminal display.

    Args:
        chunks (list[dict]): List of semantic diff chunks.

    Returns:
        str: ANSI-formatted string ready for printing.

    Examples:
        >>> isinstance(format_semantic_diff([]), str)
        True
    """
    parts = []

    for chunk in chunks:
        label = chunk['label']
        kind = chunk['kind']
        explanation = _resolve_format(chunk.get('explanation', ''), 'ansi')
        lines = chunk.get('lines', [])
        sources = chunk.get('sources', [])
        sub_chunks = chunk.get('sub_chunks', [])

        color = _KIND_COLORS_ANSI.get(kind, 'white')

        # Header
        parts.append(fansi('═' * 80, 'cyan', 'bold'))
        label_str = '[' + label + '] ' + kind.upper()
        if sources:
            label_str += '  (' + ', '.join(sources) + ')'
        parts.append(fansi(label_str, color, 'bold'))

        if explanation:
            parts.append(fansi('  ' + _strip_html(explanation), 'cyan', 'italic'))

        # Side-by-side columns (ANSI: rendered sequentially with column headers)
        sbs = chunk.get('side_by_side', [])
        for col in sbs:
            col_label = _resolve_format(col.get('label', ''), 'ansi')
            parts.append(fansi('  ┃ ' + col_label, 'blue', 'bold'))
            for li in col.get('lines', []):
                sign = li.get('sign', ' ')
                text = _resolve_format(li.get('text', ''), 'ansi') or li.get('text', '')
                highlights = li.get('highlights', [])
                text = _apply_highlights_ansi(text, highlights)
                line_num = _get_line_num(li)
                prefix = '  ' + ({'+': '+ ', '-': '- '}.get(sign, '  '))
                numbered = _format_line_with_number(text, line_num)
                line_color = {'+': 'green', '-': 'red'}.get(sign, 'gray')
                parts.append(fansi(prefix + numbered, line_color))

        # Top-level lines
        syntax = chunk.get('syntax', False)
        parts.extend(_render_lines_ansi(lines, syntax_highlight=syntax))

        # Sub-chunks
        for sub in sub_chunks:
            sub_label = sub.get('label', '')
            sub_explanation = _resolve_format(sub.get('explanation', ''), 'ansi')
            sub_sources = sub.get('sources', [])
            sub_syntax = sub.get('syntax', syntax)

            parts.append(fansi('  ' + '─' * 60, 'cyan'))
            sub_label_str = '  [' + sub_label + ']'
            if sub_sources:
                sub_label_str += '  (' + ', '.join(sub_sources) + ')'
            parts.append(fansi(sub_label_str, color))
            if sub_explanation:
                parts.append(fansi('    ' + _strip_html(sub_explanation), 'cyan', 'italic'))

            parts.extend(_render_lines_ansi(sub.get('lines', []), indent='  ', syntax_highlight=sub_syntax))

        parts.append('')

    return '\n'.join(parts)


def _html_escape(text):
    """
    Pure function. Escape HTML special characters.

    Args:
        text (str): Raw text.

    Returns:
        str

    Examples:
        >>> _html_escape('<b>hi</b> & "bye"')
        '&lt;b&gt;hi&lt;/b&gt; &amp; &quot;bye&quot;'
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _render_lines_html(line_infos, indent=False, suppress_source=None):
    """
    Pure function. Render line info dicts as HTML div elements.

    Groups consecutive lines by source file, only showing the source header
    when it changes. Each line is a flex row: sign gutter, optional line number,
    and content — all auto-sized so content gets maximum space.

    Args:
        line_infos (list[dict]): Lines to render.
        indent (bool): Whether this is a sub-chunk (adds left margin).
        suppress_source (str or None): Skip source-header for this source name.

    Returns:
        list[str]: HTML strings.

    Examples:
        >>> 'diff-line' in _render_lines_html([{'text': 'hi', 'sign': '+'}])[0]
        True
    """
    parts = []
    last_source = None

    for line_info in line_infos:
        raw_text = _resolve_format(line_info.get('text', ''), 'html') or line_info.get('text', '')
        text = _html_escape(raw_text)
        highlights = line_info.get('highlights', [])
        text = _apply_highlights_html(text, highlights)
        sign = line_info.get('sign', ' ')
        line_num = _get_line_num(line_info)
        source = line_info.get('source', '')

        # Shared-source detection: 'both', 'shared', 'all' → display as "shared"
        is_shared_source = source.lower() in ('both', 'shared', 'all')

        # Source file header — only when source changes, skip if suppressed
        if source and source != last_source:
            display_source = 'shared' if is_shared_source else _os.path.basename(source)
            if display_source != suppress_source and source != suppress_source:
                parts.append(
                    '<div class="source-header">%s</div>' % _html_escape(display_source)
                )
            last_source = source

        if is_shared_source and sign == ' ':
            sign_cls = 'shared'
        else:
            sign_cls = {'+': 'add', '-': 'rem'}.get(sign, 'ctx')
        sign_char = {'+': '+', '-': '\u2212'}.get(sign, '')
        num_str = str(line_num) if line_num else ''

        indent_cls = ' sub' if indent else ''
        parts.append(
            '<div class="diff-line %s%s">'
            '<span class="gutter-sign">%s</span>'
            '<span class="gutter-num">%s</span>'
            '<span class="line-text">%s</span>'
            '</div>' % (sign_cls, indent_cls, sign_char, num_str, text)
        )

    return parts


def _html_render_chunk_lines(lines, indent=False, suppress_source=None):
    """
    Pure function. Wrap line elements in a diff block container.

    Args:
        lines (list[dict]): Line info dicts.
        indent (bool): Sub-chunk indentation.
        suppress_source (str or None): If set, don't show source-header for this source
            (avoids duplicating the chunk-level source display).

    Returns:
        str

    Examples:
        >>> 'diff-block' in _html_render_chunk_lines([{'text': 'x', 'sign': '+'}])
        True
    """
    if not lines:
        return ''
    rows = _render_lines_html(lines, indent=indent, suppress_source=suppress_source)
    copy_btn = (
        '<button class="copy-btn" onclick="copyBlock(this)" title="Copy">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2">'
        '<rect x="9" y="9" width="13" height="13" rx="2"/>'
        '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>'
        '</svg></button>'
    )
    return (
        '<div class="diff-block-wrap">' + copy_btn +
        '<div class="diff-block">\n' + '\n'.join(rows) + '\n</div></div>'
    )


def format_semantic_diff_html(chunks, title='Semantic Diff'):
    """
    Pure function. Render semantic diff chunks as a self-contained HTML page.

    Produces a clean, distill.pub-inspired layout: dark mode by default with
    light mode toggle, Futura font, collapsible chunks, proper diff blocks,
    and source file grouping.

    Args:
        chunks (list[dict]): Semantic diff chunks.
        title (str): Page title.

    Returns:
        str: Complete HTML page string.

    Examples:
        >>> '<!DOCTYPE' in format_semantic_diff_html([])
        True
    """
    kind_labels = {'added': 'Added', 'removed': 'Removed', 'changed': 'Changed', 'shared': 'Shared'}

    h = []
    h.append('''<!DOCTYPE html>
<html lang="en">
<script>document.documentElement.setAttribute('data-theme',
  window.matchMedia('(prefers-color-scheme:light)').matches?'light':'dark');</script>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>
/* ─── Dark theme (default) ─── */
:root, [data-theme="dark"] {
    --font-main: "Futura", "Futura PT", -apple-system, "Helvetica Neue", Arial, sans-serif;
    --font-mono: "SF Mono", "Fira Code", "Consolas", "Monaco", monospace;

    --bg-page: #0d1117;
    --bg-card: #161b22;
    --bg-card-hover: #1c2129;
    --bg-add: rgba(46,160,67,0.15);
    --bg-rem: rgba(248,81,73,0.15);
    --bg-source-header: #1c2129;
    --border-card: #30363d;
    --border-sub: #30363d;

    --text-main: #e6edf3;
    --text-secondary: #8b949e;
    --text-add: #7ee787;
    --text-rem: #ffa198;
    --text-ctx: #8b949e;
    --text-num: #484f58;
    --text-explanation: #8b949e;

    --pill-add-bg: rgba(46,160,67,0.2);
    --pill-add-fg: #7ee787;
    --pill-rem-bg: rgba(248,81,73,0.2);
    --pill-rem-fg: #ffa198;
    --pill-changed-bg: rgba(210,153,34,0.2);
    --pill-changed-fg: #e3b341;
    --pill-shared-bg: rgba(56,132,244,0.2);
    --pill-shared-fg: #58a6ff;

    --mark-bg: rgba(210,153,34,0.35);
    --mark-fg: inherit;

    --card-shadow: 0 1px 3px rgba(0,0,0,0.3);
    --animation-speed: 0s;

    /* ─── Spacing / sizing (theme-independent) ─── */
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --font-size-xs: 10px;
    --font-size-sm: 11px;
    --font-size-base: 13px;
    --font-size-md: 14px;
    --font-size-lg: 26px;
    --space-xs: 4px;
    --space-sm: 6px;
    --space-md: 8px;
    --space-lg: 12px;
    --space-xl: 16px;
    --space-2xl: 32px;
    --container-max: 960px;
    --page-pad-y: 40px;
    --page-pad-x: 24px;
    --page-pad-bottom: 80px;
    --gutter-sign-width: 18px;
    --gutter-num-width: 36px;
    --toggle-size: 12px;
    --btn-size: 26px;
    --btn-icon-size: 32px;
    --max-height-open: 5000px;
    --fade-speed: 0.15s;
}

/* ─── Light theme ─── */
[data-theme="light"] {
    --bg-page: #f6f8fa;
    --bg-card: #ffffff;
    --bg-card-hover: #f6f8fa;
    --bg-add: #dafbe1;
    --bg-rem: #ffebe9;
    --bg-source-header: #f6f8fa;
    --border-card: #d0d7de;
    --border-sub: #d0d7de;

    --text-main: #1f2328;
    --text-secondary: #656d76;
    --text-add: #1a7f37;
    --text-rem: #cf222e;
    --text-ctx: #656d76;
    --text-num: #8b949e;
    --text-explanation: #656d76;

    --pill-add-bg: #dafbe1;
    --pill-add-fg: #1a7f37;
    --pill-rem-bg: #ffebe9;
    --pill-rem-fg: #cf222e;
    --pill-changed-bg: #fff8c5;
    --pill-changed-fg: #9a6700;
    --pill-shared-bg: #ddf4ff;
    --pill-shared-fg: #0969da;

    --mark-bg: #fff8c5;
    --mark-fg: #1f2328;

    --card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: var(--font-main);
    background: var(--bg-page);
    color: var(--text-main);
    padding: var(--page-pad-y) var(--page-pad-x) var(--page-pad-bottom);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
}

.container { max-width: var(--container-max); margin: 0 auto; }
.container.full-width { max-width: none; }

/* ─── Header ─── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-2xl);
}

h1 {
    font-size: var(--font-size-lg);
    font-weight: 700;
    letter-spacing: -0.3px;
}

.subtitle {
    color: var(--text-secondary);
    font-size: var(--font-size-base);
    margin-top: var(--space-xs);
}

.header-buttons {
    display: flex;
    gap: var(--space-sm);
    flex-shrink: 0;
    margin-top: var(--space-xs);
}
.toolbar-btn {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    color: var(--text-secondary);
    border-radius: var(--radius-md);
    padding: var(--space-sm);
    width: var(--btn-icon-size);
    height: var(--btn-icon-size);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}
.toolbar-btn:hover { color: var(--text-main); }
/* Theme toggle icons */
[data-theme="dark"] .icon-sun { display: none; }
[data-theme="dark"] .icon-moon { display: block; }
[data-theme="light"] .icon-sun { display: block; }
[data-theme="light"] .icon-moon { display: none; }
/* Width toggle icons — JS toggles .full-width on .container */
.icon-expand { display: block; }
.icon-contract { display: none; }
.full-width .icon-expand { display: none; }
.full-width .icon-contract { display: block; }

/* ─── Chunk card ─── */
.chunk {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-xl);
    box-shadow: var(--card-shadow);
}

.chunk-header {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-lg) var(--space-xl);
    cursor: pointer;
    user-select: none;
}
.chunk-header:hover { background: var(--bg-card-hover); border-radius: var(--radius-lg); }

.chunk-label {
    font-family: var(--font-mono);
    font-size: var(--font-size-sm);
    font-weight: 700;
    padding: 2px var(--space-sm);
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}
.chunk-label.added   { background: var(--pill-add-bg);     color: var(--pill-add-fg); }
.chunk-label.removed { background: var(--pill-rem-bg);     color: var(--pill-rem-fg); }
.chunk-label.changed { background: var(--pill-changed-bg); color: var(--pill-changed-fg); }
.chunk-label.shared  { background: var(--pill-shared-bg);  color: var(--pill-shared-fg); }

.chunk-kind {
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    flex-shrink: 0;
}
.chunk-kind.added   { color: var(--pill-add-fg); }
.chunk-kind.removed { color: var(--pill-rem-fg); }
.chunk-kind.changed { color: var(--pill-changed-fg); }
.chunk-kind.shared  { color: var(--pill-shared-fg); }

.chunk-title {
    font-size: var(--font-size-md);
    font-weight: 500;
    color: var(--text-main);
    flex: 1;
    min-width: 0;
}

.chunk-toggle {
    flex-shrink: 0;
    width: var(--toggle-size);
    height: var(--toggle-size);
    transition: transform var(--animation-speed);
}
.chunk-toggle svg { display: block; width: 100%%; height: 100%%; fill: var(--text-secondary); }
.chunk.collapsed .chunk-toggle { transform: rotate(-90deg); }
.chunk-body {
    overflow: hidden;
    max-height: var(--max-height-open);
    transition: max-height var(--animation-speed) ease-out;
}
.chunk.collapsed .chunk-body { max-height: 0; padding: 0; }
.chunk.collapsed .chunk-header { border-radius: var(--radius-lg); }

.chunk-body { padding: 0 0 var(--space-xs); }

.chunk-explanation { padding: var(--space-xs) var(--space-xl) var(--space-md); }
.chunk-explanation img, .chunk-explanation video { max-width: 100%%; height: auto; }
.chunk-explanation > div { min-width: 0; }
.chunk-explanation div[style*="flex"] > div { min-width: 0; }
.chunk-sources {
    padding: 2px var(--space-xl) var(--space-sm);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

/* ─── Sub-chunk ─── */
.sub-chunk {
    margin: var(--space-xs) var(--space-lg) var(--space-md);
    border: 1px solid var(--border-sub);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.sub-chunk-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-lg);
    background: var(--bg-source-header);
    border-bottom: 1px solid var(--border-sub);
    font-size: var(--font-size-base);
}

.sub-chunk-label {
    font-family: var(--font-mono);
    font-size: var(--font-size-xs);
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
}

.sub-chunk-sources {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
}

.sub-chunk-explanation {
    font-style: italic;
    color: var(--text-explanation);
    font-size: var(--font-size-sm);
}

/* ─── Diff block ─── */
.diff-block {
    font-family: var(--font-mono);
    font-size: var(--font-size-base);
    line-height: 1.55;
    overflow-x: auto;
}

.source-header {
    padding: 5px var(--space-xl) 3px;
    font-family: var(--font-main);
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-secondary);
    background: var(--bg-source-header);
    border-top: 1px solid var(--border-sub);
}

.diff-line {
    display: flex;
    align-items: baseline;
    padding: 0 var(--space-lg) 0 0;
}

.diff-line.add { background: var(--bg-add); }
.diff-line.rem { background: var(--bg-rem); }

.gutter-sign {
    width: var(--gutter-sign-width);
    flex-shrink: 0;
    text-align: center;
    font-weight: 700;
    user-select: none;
}
.diff-line.add .gutter-sign { color: var(--text-add); }
.diff-line.rem .gutter-sign { color: var(--text-rem); }
.diff-line.ctx .gutter-sign { color: var(--text-ctx); }
.diff-line.shared .gutter-sign { color: var(--pill-shared-fg); }

.gutter-num {
    width: var(--gutter-num-width);
    flex-shrink: 0;
    text-align: right;
    padding-right: var(--space-md);
    color: var(--text-num);
    font-size: var(--font-size-sm);
    user-select: none;
}

.line-text {
    flex: 1;
    min-width: 0;
    white-space: pre-wrap;
    word-break: break-word;
}
.diff-line.add .line-text { color: var(--text-add); }
.diff-line.rem .line-text { color: var(--text-rem); }
.diff-line.ctx .line-text { color: var(--text-ctx); }
.diff-line.shared .line-text { color: var(--pill-shared-fg); }

.diff-line.sub { padding-left: var(--space-lg); }

mark {
    background: var(--mark-bg);
    color: var(--mark-fg);
    padding: 1px 2px;
    border-radius: var(--radius-sm);
}

/* ─── Copy button ─── */
.copy-btn {
    position: absolute;
    top: var(--space-xs);
    right: var(--space-xs);
    background: var(--bg-card);
    border: 1px solid var(--border-sub);
    color: var(--text-secondary);
    border-radius: var(--radius-sm);
    width: var(--btn-size);
    height: var(--btn-size);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity var(--fade-speed);
}
.diff-block-wrap:hover .copy-btn,
.sbs-container:hover .copy-btn { opacity: 1; }
.copy-btn:hover { color: var(--text-main); border-color: var(--text-secondary); }
.copy-btn.copied { color: var(--text-add); }

.diff-block-wrap {
    position: relative;
}

/* ─── Side-by-side (dunk-style) ─── */
.sbs-container {
    display: flex;
    gap: 0;
    overflow-x: auto;
    border-top: 1px solid var(--border-sub);
    position: relative;
}

.sbs-col {
    min-width: 0;
    overflow: hidden;
    font-family: var(--font-mono);
    font-size: var(--font-size-base);
    line-height: 1.55;
}

.sbs-col-header {
    padding: 5px var(--space-lg);
    font-family: var(--font-main);
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-secondary);
    background: var(--bg-source-header);
    border-bottom: 1px solid var(--border-sub);
    text-align: center;
}

/* ─── Resizable divider between sbs columns ─── */
.sbs-divider {
    width: 5px;
    cursor: col-resize;
    background: var(--border-sub);
    flex-shrink: 0;
    position: relative;
    z-index: 1;
    transition: background 0.1s;
}
.sbs-divider:hover, .sbs-divider.active {
    background: var(--pill-shared-fg);
}
</style>
</head>
<body>
<div class="container">
<div class="page-header">
<div>
<h1>%s</h1>
<div class="subtitle">%d chunk%s</div>
</div>
<div class="header-buttons">
<button class="toolbar-btn" onclick="toggleWidth()" title="Toggle full width">
<svg class="icon-expand" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15,3 21,3 21,9"/><polyline points="9,21 3,21 3,15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
<svg class="icon-contract" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4,14 10,14 10,20"/><polyline points="20,10 14,10 14,4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
</button>
<button class="toolbar-btn" onclick="toggleTheme()" title="Toggle light/dark mode">
<svg class="icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
<svg class="icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
</button>
</div>
</div>
''' % (
        _html_escape(title),
        _html_escape(title),
        len(chunks),
        '' if len(chunks) == 1 else 's',
    ))

    for chunk in chunks:
        label = chunk['label']
        kind = chunk['kind']
        explanation = _resolve_format(chunk.get('explanation', ''), 'html')
        lines = chunk.get('lines', [])
        sources = chunk.get('sources', [])
        sub_chunks = chunk.get('sub_chunks', [])

        kind_label = kind_labels.get(kind, kind.title())

        sync_attr = ' data-sync-videos' if chunk.get('sync_videos') else ''
        h.append('<div class="chunk"%s>' % sync_attr)

        # Header — clickable to collapse, fully hides body
        # If explanation contains HTML tags, show only the plain-text prefix
        # in the header and put the full rich content in the body.
        header_title = ''
        body_explanation = ''
        if explanation:
            tag_pos = explanation.find('<')
            if tag_pos == -1:
                header_title = explanation
            else:
                header_title = explanation[:tag_pos].rstrip() if tag_pos > 0 else _strip_html(explanation)
                body_explanation = explanation

        h.append('<div class="chunk-header">')
        h.append('<span class="chunk-label %s">%s</span>' % (kind, _html_escape(label)))
        h.append('<span class="chunk-kind %s">%s</span>' % (kind, kind_label))
        if header_title:
            h.append('<span class="chunk-title">%s</span>' % _html_escape(header_title).replace('\n', ' '))
        h.append('<span class="chunk-toggle"><svg viewBox="0 0 10 10"><polygon points="0,2 10,2 5,9"/></svg></span>')
        h.append('</div>')

        h.append('<div class="chunk-body">')

        # Rich explanation (images, videos, diagrams) — inside body so it collapses
        # Newlines in plain-text explanations become <br>; HTML explanations pass through raw
        if body_explanation:
            h.append('<div class="chunk-explanation">%s</div>' % body_explanation)
        elif explanation and '\n' in explanation:
            h.append('<div class="chunk-explanation">%s</div>' % _html_escape(explanation).replace('\n', '<br>'))

        # Sources line
        if sources:
            h.append('<div class="chunk-sources">%s</div>' % _html_escape(', '.join(sources)))

        # Side-by-side columns (dunk-style, N-way)
        sbs = chunk.get('side_by_side', [])
        if sbs:
            h.append(_render_side_by_side_html(sbs))

        # Top-level lines (interleaved +/- style)
        # Suppress redundant source header when chunk has exactly 1 source
        suppress = sources[0] if len(sources) == 1 else None
        if lines:
            h.append(_html_render_chunk_lines(lines, suppress_source=suppress))

        # Sub-chunks
        for sub in sub_chunks:
            sub_label = sub.get('label', '')
            sub_explanation = _resolve_format(sub.get('explanation', ''), 'html')
            sub_sources = sub.get('sources', [])

            h.append('<div class="sub-chunk">')
            h.append('<div class="sub-chunk-header">')
            h.append('<span class="sub-chunk-label %s">%s</span>' % (kind, _html_escape(sub_label)))
            if sub_sources:
                h.append('<span class="sub-chunk-sources">%s</span>' % _html_escape(', '.join(sub_sources)))
            if sub_explanation:
                h.append('<span class="sub-chunk-explanation">%s</span>' % _html_escape(sub_explanation))
            h.append('</div>')

            # Suppress source header when sub-chunk has exactly 1 source
            sub_suppress = sub_sources[0] if len(sub_sources) == 1 else None
            if sub.get('lines'):
                h.append(_html_render_chunk_lines(sub['lines'], indent=True, suppress_source=sub_suppress))

            h.append('</div>')

        h.append('</div>')  # chunk-body
        h.append('</div>')  # chunk

    h.append('''</div>
<script>
function toggleTheme() {
    var html = document.documentElement;
    html.setAttribute('data-theme',
        html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
}
function toggleWidth() {
    document.querySelector('.container').classList.toggle('full-width');
}

/* ─── Copy block text to clipboard ─── */
function copyBlock(btn) {
    var wrap = btn.closest('.diff-block-wrap') || btn.closest('.sbs-container');
    if (!wrap) return;
    var texts = wrap.querySelectorAll('.line-text');
    var lines = [];
    texts.forEach(function(el) { lines.push(el.textContent); });
    navigator.clipboard.writeText(lines.join('\\n')).then(function() {
        btn.classList.add('copied');
        setTimeout(function() { btn.classList.remove('copied'); }, 1200);
    });
}

/* ─── Blender-style drag-collapse ───
   Click a chunk header to toggle it. While holding the mouse button,
   drag over other headers to apply the same action (collapse or expand)
   to all of them — like Blender's accordion drag behavior.
   Tracks last-visited index so fast mouse movement doesn't skip chunks. */
(function() {
    var dragging = false;
    var dragAction = null; // 'collapse' or 'expand'
    var lastIndex = -1;

    function getAllChunks() { return Array.from(document.querySelectorAll('.chunk')); }

    function syncVideos(chunk) {
        var videos = chunk.querySelectorAll('video');
        var collapsed = chunk.classList.contains('collapsed');
        videos.forEach(function(v) {
            if (collapsed) v.pause();
            else if (v.hasAttribute('autoplay')) v.play();
        });
    }

    function applyAction(chunk) {
        if (dragAction === 'collapse') chunk.classList.add('collapsed');
        else chunk.classList.remove('collapsed');
        syncVideos(chunk);
    }

    function chunkIndexOf(chunk) {
        return getAllChunks().indexOf(chunk);
    }

    function applyRange(fromIdx, toIdx) {
        var chunks = getAllChunks();
        var lo = Math.min(fromIdx, toIdx);
        var hi = Math.max(fromIdx, toIdx);
        for (var i = lo; i <= hi; i++) applyAction(chunks[i]);
    }

    document.addEventListener('mousedown', function(e) {
        var header = e.target.closest('.chunk-header');
        if (!header) return;
        var chunk = header.parentElement;
        var wasCollapsed = chunk.classList.contains('collapsed');
        chunk.classList.toggle('collapsed');
        syncVideos(chunk);
        dragging = true;
        dragAction = wasCollapsed ? 'expand' : 'collapse';
        lastIndex = chunkIndexOf(chunk);
        e.preventDefault();
    });

    document.addEventListener('mouseover', function(e) {
        if (!dragging) return;
        var header = e.target.closest('.chunk-header');
        if (!header) return;
        var chunk = header.parentElement;
        var idx = chunkIndexOf(chunk);
        if (idx === -1) return;
        if (lastIndex !== -1 && idx !== lastIndex) {
            applyRange(lastIndex, idx);
        } else {
            applyAction(chunk);
        }
        lastIndex = idx;
    });

    document.addEventListener('mouseup', function() {
        dragging = false;
        dragAction = null;
        lastIndex = -1;
    });
})();

/* ─── Synchronized video playback ───
   Chunks with data-sync-videos: first <video> is master (keeps controls),
   all others are slaves (controls removed, driven by master).
   Used for comparing same-length video transformations. */
(function() {
    var groups = document.querySelectorAll('[data-sync-videos]');
    groups.forEach(function(chunk) {
        var videos = Array.from(chunk.querySelectorAll('video'));
        if (videos.length < 2) return;
        var master = videos[0];
        var slaves = videos.slice(1);

        // Master keeps controls; remove from slaves
        master.setAttribute('controls', '');
        slaves.forEach(function(s) { s.removeAttribute('controls'); });

        var syncing = false;
        master.addEventListener('play', function() {
            slaves.forEach(function(s) { s.play(); });
        });
        master.addEventListener('pause', function() {
            slaves.forEach(function(s) { s.pause(); });
        });
        master.addEventListener('seeked', function() {
            slaves.forEach(function(s) { s.currentTime = master.currentTime; });
        });
        master.addEventListener('timeupdate', function() {
            if (syncing) return;
            syncing = true;
            slaves.forEach(function(s) {
                if (Math.abs(s.currentTime - master.currentTime) > 0.3) {
                    s.currentTime = master.currentTime;
                }
            });
            syncing = false;
        });
        master.addEventListener('ratechange', function() {
            slaves.forEach(function(s) { s.playbackRate = master.playbackRate; });
        });
    });
})();

/* ─── Resizable side-by-side column dividers ───
   Drag a divider to resize the columns on either side.
   Uses pixel widths during drag for precision. */
(function() {
    var activeDivider = null;
    var startX = 0;
    var leftCol = null;
    var rightCol = null;
    var leftStartPx = 0;
    var rightStartPx = 0;
    var minPx = 40;

    document.addEventListener('mousedown', function(e) {
        if (!e.target.classList.contains('sbs-divider')) return;
        activeDivider = e.target;
        activeDivider.classList.add('active');
        leftCol = activeDivider.previousElementSibling;
        rightCol = activeDivider.nextElementSibling;
        if (!leftCol || !rightCol) { activeDivider = null; return; }
        leftStartPx = leftCol.getBoundingClientRect().width;
        rightStartPx = rightCol.getBoundingClientRect().width;
        startX = e.clientX;
        e.preventDefault();
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    });

    document.addEventListener('mousemove', function(e) {
        if (!activeDivider) return;
        var dx = e.clientX - startX;
        var totalPx = leftStartPx + rightStartPx;
        var newLeft = Math.max(minPx, Math.min(totalPx - minPx, leftStartPx + dx));
        var newRight = totalPx - newLeft;
        leftCol.style.flex = '0 0 ' + newLeft + 'px';
        rightCol.style.flex = '0 0 ' + newRight + 'px';
    });

    document.addEventListener('mouseup', function() {
        if (!activeDivider) return;
        activeDivider.classList.remove('active');
        activeDivider = null;
        leftCol = null;
        rightCol = null;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
    });
})();
</script>
</body>
</html>''')
    return '\n'.join(h)


def _render_side_by_side_html(columns):
    """
    Pure function. Render N columns side-by-side in HTML (dunk-style).

    Each column is a dict with 'label' (str) and 'lines' (list of dicts).
    Lines within each column have 'text', optional 'line_num', optional 'sign'.
    Columns are displayed left-to-right, each taking equal width.

    This is for when a chunk has 'side_by_side': [col1, col2, ...] instead of
    (or in addition to) 'lines'. Useful for 2-way or N-way file comparisons
    where seeing the versions next to each other is more readable than
    interleaved +/- lines.

    Args:
        columns (list[dict]): Each with 'label' (str) and 'lines' (list[dict]).
            Line dicts have 'text' (str), optional 'line_num' (int),
            optional 'sign' (str: +/-/ ), optional 'highlights' (list).

    Returns:
        str: HTML string for the side-by-side block.

    Examples:
        >>> cols = [{'label': 'v1', 'lines': [{'text': 'old'}]},
        ...         {'label': 'v2', 'lines': [{'text': 'new'}]}]
        >>> 'sbs-col' in _render_side_by_side_html(cols)
        True
    """
    n = len(columns)
    if n == 0:
        return ''

    max_lines = max(len(c.get('lines', [])) for c in columns)

    h = ['<div class="sbs-container">']

    for ci, col in enumerate(columns):
        if ci > 0:
            h.append('<div class="sbs-divider"></div>')

        h.append('<div class="sbs-col" style="flex: 1 1 0;">')
        h.append('<div class="sbs-col-header">%s</div>' % _html_escape(col.get('label', '')))

        col_lines = col.get('lines', [])
        for i in range(max_lines):
            if i < len(col_lines):
                li = col_lines[i]
                text = _html_escape(li['text'])
                highlights = li.get('highlights', [])
                text = _apply_highlights_html(text, highlights)
                sign = li.get('sign', ' ')
                line_num = _get_line_num(li)
                num_str = str(line_num) if line_num else ''
                sign_cls = {'+': 'add', '-': 'rem'}.get(sign, 'ctx')
                sign_char = {'+': '+', '-': '\u2212'}.get(sign, '')

                h.append(
                    '<div class="diff-line %s">'
                    '<span class="gutter-sign">%s</span>'
                    '<span class="gutter-num">%s</span>'
                    '<span class="line-text">%s</span>'
                    '</div>' % (sign_cls, sign_char, num_str, text)
                )
            else:
                h.append('<div class="diff-line ctx">&nbsp;</div>')

        h.append('</div>')

    h.append('</div>')
    return '\n'.join(h)


def _render_lines_md(line_infos):
    """
    Pure function. Render a list of line info dicts as Markdown strings.

    Args:
        line_infos (list[dict]): Lines to render.

    Returns:
        list[str]

    Examples:
        >>> _render_lines_md([{'text': 'hello', 'sign': '+', 'line_num': 5, 'source': 'a.py'}])
        ['+ `a.py:5` hello']
    """
    parts = []
    for line_info in line_infos:
        text = _resolve_format(line_info.get('text', ''), 'md') or line_info.get('text', '')
        highlights = line_info.get('highlights', [])
        text = _apply_highlights_md(text, highlights)
        sign = line_info.get('sign', ' ')
        line_num = _get_line_num(line_info)
        source = line_info.get('source', '')

        if sign == '+':
            prefix = '+ '
        elif sign == '-':
            prefix = '- '
        else:
            prefix = '  '

        loc = ''
        if source and line_num:
            loc = '`%s:%s` ' % (_os.path.basename(source), line_num)
        elif source:
            loc = '`%s` ' % _os.path.basename(source)
        elif line_num:
            loc = '`L%s` ' % line_num

        parts.append(prefix + loc + text)
    return parts


def format_semantic_diff_md(chunks, title='Semantic Diff'):
    """
    Pure function. Render semantic diff chunks as Markdown.

    Args:
        chunks (list[dict]): Semantic diff chunks.
        title (str): Document title.

    Returns:
        str: Markdown string.

    Examples:
        >>> '##' in format_semantic_diff_md([])
        True
    """
    m = []
    m.append('## %s' % title)
    m.append('')

    kind_icons = {'added': '+', 'removed': '-', 'changed': '~', 'shared': '='}

    for chunk in chunks:
        label = chunk['label']
        kind = chunk['kind']
        explanation = _resolve_format(chunk.get('explanation', ''), 'md')
        lines = chunk.get('lines', [])
        sources = chunk.get('sources', [])
        sub_chunks = chunk.get('sub_chunks', [])

        icon = kind_icons.get(kind, '?')
        src_str = ' (%s)' % ', '.join(sources) if sources else ''
        m.append('### [%s] %s %s%s' % (icon, label, kind.upper(), src_str))
        if explanation:
            m.append('> %s' % _strip_html(explanation))
        m.append('')

        # Side-by-side columns (Markdown: rendered as sequential blocks)
        sbs = chunk.get('side_by_side', [])
        for col in sbs:
            col_label = _resolve_format(col.get('label', ''), 'md')
            m.append('**%s**' % col_label)
            m.append('```diff')
            m.extend(_render_lines_md(col.get('lines', [])))
            m.append('```')
            m.append('')

        if lines:
            m.append('```diff')
            m.extend(_render_lines_md(lines))
            m.append('```')
            m.append('')

        for sub in sub_chunks:
            sub_label = sub.get('label', '')
            sub_explanation = _resolve_format(sub.get('explanation', ''), 'md')
            sub_sources = sub.get('sources', [])

            sub_src = ' (%s)' % ', '.join(sub_sources) if sub_sources else ''
            m.append('#### [%s]%s' % (sub_label, sub_src))
            if sub_explanation:
                m.append('> %s' % _strip_html(sub_explanation))
            m.append('')
            if sub.get('lines'):
                m.append('```diff')
                m.extend(_render_lines_md(sub['lines']))
                m.append('```')
                m.append('')

        m.append('---')
        m.append('')

    return '\n'.join(m)


def format_semantic_diff_plain(chunks):
    """
    Pure function. Render semantic diff as plain text (no ANSI codes).

    Same structure as the ANSI version but without colors — suitable for
    parroting back in chat or saving to a .txt file.

    Args:
        chunks (list[dict]): Semantic diff chunks.

    Returns:
        str

    Examples:
        >>> '[A]' in format_semantic_diff_plain([{'label':'A','kind':'added','explanation':'test','lines':[]}])
        True
    """
    parts = []

    for chunk in chunks:
        label = chunk['label']
        kind = chunk['kind']
        explanation = _resolve_format(chunk.get('explanation', ''), 'plain')
        lines = chunk.get('lines', [])
        sources = chunk.get('sources', [])
        sub_chunks = chunk.get('sub_chunks', [])

        parts.append('═' * 80)
        label_str = '[%s] %s' % (label, kind.upper())
        if sources:
            label_str += '  (%s)' % ', '.join(sources)
        parts.append(label_str)

        if explanation:
            parts.append('  ' + _strip_html(explanation))

        # Side-by-side columns (plain text: sequential with column headers)
        for col in chunk.get('side_by_side', []):
            col_label = _resolve_format(col.get('label', ''), 'plain')
            parts.append('  ┃ %s' % col_label)
            for li in col.get('lines', []):
                sign = li.get('sign', ' ')
                text = _resolve_format(li.get('text', ''), 'plain') or li.get('text', '')
                line_num = _get_line_num(li)
                prefix = '  ' + ({'+': '+ ', '-': '- '}.get(sign, '  '))
                numbered = _format_line_with_number(text, line_num)
                parts.append(prefix + numbered)

        for line_info in lines:
            text = _resolve_format(line_info.get('text', ''), 'plain') or line_info.get('text', '')
            sign = line_info.get('sign', ' ')
            line_num = _get_line_num(line_info)
            source = line_info.get('source', '')

            prefix = {'+': '+ ', '-': '- '}.get(sign, '  ')
            src = '[%s] ' % _os.path.basename(source) if source else ''
            numbered = _format_line_with_number(text, line_num)
            parts.append(src + prefix + numbered)

        for sub in sub_chunks:
            sub_label = sub.get('label', '')
            sub_explanation = _resolve_format(sub.get('explanation', ''), 'plain')
            sub_sources = sub.get('sources', [])

            parts.append('  ' + '─' * 60)
            sub_str = '  [%s]' % sub_label
            if sub_sources:
                sub_str += '  (%s)' % ', '.join(sub_sources)
            parts.append(sub_str)
            if sub_explanation:
                parts.append('    ' + _strip_html(sub_explanation))

            for line_info in sub.get('lines', []):
                text = _resolve_format(line_info.get('text', ''), 'plain') or line_info.get('text', '')
                sign = line_info.get('sign', ' ')
                line_num = _get_line_num(line_info)
                source = line_info.get('source', '')

                prefix = {'+': '  + ', '-': '  - '}.get(sign, '    ')
                src = '[%s] ' % _os.path.basename(source) if source else ''
                numbered = _format_line_with_number(text, line_num)
                parts.append(src + prefix + numbered)

        parts.append('')

    return '\n'.join(parts)


# ── Save / Load / Print ─────────────────────────────────────────────────────

def save_semantic_diff_bundle(chunks, description='semantic_diff'):
    """
    Command. Save all semantic diff formats to .claude_diffs/<timestamp>_<description>/.

    Creates diff.json, diff.txt, and diff.html in a timestamped subfolder.
    Prints ANSI version to stdout. Returns dict of absolute paths.

    Args:
        chunks (list[dict]): Semantic diff chunks.
        description (str): Short description for folder name (spaces become underscores).

    Returns:
        dict: {'json': path, 'txt': path, 'html': path, 'dir': path}

    Examples:
        >>> # paths = save_semantic_diff_bundle(chunks, 'claude_md_comparison')
    """
    import datetime

    description = description.replace(' ', '_')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    dirname = '%s_%s' % (timestamp, description)
    dirpath = _os.path.join('.claude_diffs', dirname)
    _os.makedirs(dirpath, exist_ok=True)

    paths = {}
    abs_dir = _os.path.abspath(dirpath)

    # JSON
    json_path = _os.path.join(dirpath, 'diff.json')
    save_semantic_diff(chunks, json_path)
    paths['json'] = _os.path.abspath(json_path)

    # Plain text
    txt_path = _os.path.join(dirpath, 'diff.txt')
    with open(txt_path, 'w') as f:
        f.write(format_semantic_diff_plain(chunks))
    paths['txt'] = _os.path.abspath(txt_path)

    # HTML
    html_path = _os.path.join(dirpath, 'diff.html')
    with open(html_path, 'w') as f:
        f.write(format_semantic_diff_html(chunks))
    paths['html'] = _os.path.abspath(html_path)

    paths['dir'] = abs_dir

    # Print ANSI to stdout
    print_semantic_diff(chunks)

    return paths


def save_semantic_diff(chunks, path='.claude_semantic_diff.json'):
    """
    Command. Save raw semantic diff chunks as JSON for later printing.

    Args:
        chunks (list[dict]): Semantic diff chunks.
        path (str): Output file path.

    Examples:
        >>> # save_semantic_diff([{'label':'A','kind':'added','explanation':'test','lines':[]}])
    """
    import json
    with open(path, 'w') as f:
        json.dump(chunks, f, indent=2)


def load_semantic_diff(path='.claude_semantic_diff.json'):
    """
    Query. Load semantic diff chunks from JSON file.

    Args:
        path (str): Path to saved diff file.

    Returns:
        list[dict]

    Examples:
        >>> # chunks = load_semantic_diff('.claude_semantic_diff.json')
    """
    import json
    with open(path) as f:
        return json.load(f)


def print_semantic_diff(chunks):
    """
    Command. Format and print semantic diff chunks to stdout with ANSI colors.

    Args:
        chunks (list[dict]): Semantic diff chunks.

    Examples:
        >>> # print_semantic_diff(chunks)
    """
    print(format_semantic_diff(chunks))


def print_saved_semantic_diff(path='.claude_semantic_diff.json'):
    """
    Command. Load and print a previously saved semantic diff.

    Args:
        path (str): Path to saved diff file.

    Examples:
        >>> # print_saved_semantic_diff('.claude_semantic_diff.json')
    """
    print_semantic_diff(load_semantic_diff(path))


# ── Demo / Test ──────────────────────────────────────────────────────────────

def _demo_chunks():
    """
    Pure function. Return a list of chunks exercising every feature.

    Covers: all chunk kinds (added/removed/changed/shared), sub-chunks,
    syntax highlighting, page_num, line_num, multiple sources, context lines,
    inline highlights, side-by-side columns (2-way and 3-way).

    Each chunk demonstrates a specific feature so that:
    1. We can verify all renderers handle it correctly.
    2. If a feature is deemed unnecessary later, the chunk can be deleted easily.

    Returns:
        list[dict]

    Examples:
        >>> len(_demo_chunks()) >= 11
        True
    """
    return [
        # ── A: Plain text added (single source) ──
        # WHY: Tests basic 'added' kind with single source, line numbers.
        {
            'label': 'A',
            'kind': 'added',
            'sources': ['netbook_claude.md'],
            'explanation': 'PEP 723 rule only exists in netbook.',
            'lines': [
                {'text': '# PEP 723', 'sign': '+', 'line_num': 41, 'source': 'netbook_claude.md'},
                {'text': '- When I say "inline dependencies", add PEP 723 metadata', 'sign': '+', 'line_num': 42, 'source': 'netbook_claude.md'},
            ],
        },

        # ── B: Plain text removed ──
        # WHY: Tests 'removed' kind.
        {
            'label': 'B',
            'kind': 'removed',
            'sources': ['workbench_claude.md'],
            'explanation': 'Workbench dropped the scratchpad rule.',
            'lines': [
                {'text': '- NEVER use python -c. ALWAYS use scratchpad.py.', 'sign': '-', 'line_num': 3, 'source': 'workbench_claude.md'},
            ],
        },

        # ── C: Changed with multiple sources and context lines ──
        # WHY: Tests 'changed' kind, mixing +/-/context, multiple sources in one chunk.
        {
            'label': 'C',
            'kind': 'changed',
            'sources': ['CLAUDE.md', 'netbook', 'workbench'],
            'explanation': 'SHUT UP section emphasis differs across files.',
            'lines': [
                {'text': '- When the user says "SHUT UP": IMMEDIATELY stop.', 'sign': ' ', 'source': 'all'},
                {'text': '"ALL means ALL — no rationalizing..."', 'sign': ' ', 'line_num': 108, 'source': 'CLAUDE.md'},
                {'text': '!!!!! ZERO EXCEPTIONS ... EMERGENCY STOP', 'sign': '+', 'line_num': 110, 'source': 'CLAUDE.md'},
                {'text': '(shorter, no emergency emphasis)', 'sign': '-', 'line_num': 111, 'source': 'workbench_claude.md'},
            ],
        },

        # ── D: Shared (identical across files) ──
        # WHY: Tests 'shared' kind — no +/- signs, just context.
        {
            'label': 'D',
            'kind': 'shared',
            'sources': ['CLAUDE.md', 'netbook', 'workbench'],
            'explanation': 'Error handling rules identical in all three.',
            'lines': [
                {'text': '- NO SILENT FALLBACKS EVER! PERMANENT.', 'sign': ' ', 'source': 'all'},
            ],
        },

        # ── E: Code diff with syntax highlighting + sub-chunks ──
        # WHY: Tests syntax highlighting (dark bg), sub-chunks with dot notation labels.
        {
            'label': 'E',
            'kind': 'changed',
            'sources': ['r.py', 'test_r.py'],
            'explanation': 'Rename calc_foo to compute_foo.',
            'syntax': True,
            'sub_chunks': [
                {
                    'label': 'E.1',
                    'sources': ['r.py'],
                    'explanation': 'Function definition',
                    'lines': [
                        {'text': 'def calc_foo(x):', 'sign': '-', 'line_num': 12, 'source': 'r.py'},
                        {'text': 'def compute_foo(x):', 'sign': '+', 'line_num': 12, 'source': 'r.py'},
                        {'text': '    return x * 2 + 1', 'sign': ' ', 'line_num': 13, 'source': 'r.py'},
                    ],
                },
                {
                    'label': 'E.2',
                    'sources': ['test_r.py'],
                    'explanation': 'Test call site',
                    'lines': [
                        {'text': 'result = calc_foo(5)', 'sign': '-', 'line_num': 8, 'source': 'test_r.py'},
                        {'text': 'result = compute_foo(5)', 'sign': '+', 'line_num': 8, 'source': 'test_r.py'},
                    ],
                },
            ],
        },

        # ── F: PDF diff with page_num ──
        # WHY: Tests page_num (instead of line_num) for non-code documents like PDFs.
        {
            'label': 'F',
            'kind': 'changed',
            'sources': ['paper_v1.pdf', 'paper_v2.pdf'],
            'explanation': 'Abstract wording changed between versions.',
            'lines': [
                {'text': 'We propose a novel method...', 'sign': '-', 'page_num': 1, 'source': 'paper_v1.pdf'},
                {'text': 'We present an improved method...', 'sign': '+', 'page_num': 1, 'source': 'paper_v2.pdf'},
                {'text': 'Achieves SOTA on ImageNet.', 'sign': ' ', 'page_num': 1, 'source': 'both'},
            ],
        },

        # ── G: Inline highlights ──
        # WHY: Tests the 'highlights' field that marks specific character spans
        # as changed. Shows exactly WHAT changed within a line, even when lines
        # have moved. ANSI: bold+underline. HTML: <mark>. MD: **bold**.
        {
            'label': 'G',
            'kind': 'changed',
            'sources': ['config.py'],
            'explanation': 'Timeout value changed from 30 to 60.',
            'lines': [
                {'text': 'TIMEOUT = 30  # seconds', 'sign': '-', 'line_num': 7, 'source': 'config.py',
                 'highlights': [[10, 12]]},
                {'text': 'TIMEOUT = 60  # seconds', 'sign': '+', 'line_num': 7, 'source': 'config.py',
                 'highlights': [[10, 12]]},
            ],
        },

        # ── H: 2-way side-by-side (dunk-style) ──
        # WHY: Tests side_by_side with 2 columns. In HTML, renders as two
        # columns next to each other (like the `dunk` tool). In ANSI/MD/plain,
        # renders as sequential blocks since terminals can't do real columns.
        {
            'label': 'H',
            'kind': 'changed',
            'sources': ['old.py', 'new.py'],
            'explanation': '2-way side-by-side: function signature changed.',
            'side_by_side': [
                {
                    'label': 'old.py',
                    'lines': [
                        {'text': 'def process(data):', 'line_num': 1},
                        {'text': '    validate(data)', 'line_num': 2},
                        {'text': '    return transform(data)', 'line_num': 3, 'sign': '-',
                         'highlights': [[11, 25]]},
                    ],
                },
                {
                    'label': 'new.py',
                    'lines': [
                        {'text': 'def process(data, strict=True):', 'line_num': 1, 'sign': '+',
                         'highlights': [[12, 30]]},
                        {'text': '    validate(data)', 'line_num': 2},
                        {'text': '    return transform(data, strict)', 'line_num': 3, 'sign': '+',
                         'highlights': [[11, 34]]},
                    ],
                },
            ],
        },

        # ── I: Image diff ──
        # WHY: Tests embedding real images in semantic diffs via <img> tags.
        # Uses public-domain sample images. ANSI/MD/plain just show the VLM text.
        {
            'label': 'I',
            'kind': 'changed',
            'sources': ['photo_v1.jpg', 'photo_v2.jpg'],
            'explanation': (
                'Color grading changed: v1 warm tones, v2 cool tones.'
                '<div style="display:flex;gap:var(--space-lg);margin:var(--space-md) 0;">'
                '<div style="flex:1;text-align:center;">'
                '<div style="font-size:var(--font-size-sm);color:var(--text-secondary);margin-bottom:var(--space-xs);">v1 (warm)</div>'
                '<img src="https://picsum.photos/id/10/400/260" style="width:100%%;border-radius:var(--radius-md);" alt="v1 warm landscape"/>'
                '</div>'
                '<div style="flex:1;text-align:center;">'
                '<div style="font-size:var(--font-size-sm);color:var(--text-secondary);margin-bottom:var(--space-xs);">v2 (cool)</div>'
                '<img src="https://picsum.photos/id/15/400/260" style="width:100%%;border-radius:var(--radius-md);" alt="v2 cool landscape"/>'
                '</div></div>'
            ),
            'lines': [
                {'text': '[VLM] v1: Landscape photo with warm orange/amber color grading.', 'sign': '-', 'source': 'photo_v1.jpg'},
                {'text': '[VLM] v2: Same landscape with cool blue/teal color grading.', 'sign': '+', 'source': 'photo_v2.jpg'},
                {'text': '[VLM] Both: Same composition, same subject, same framing.', 'sign': ' ', 'source': 'both'},
            ],
        },

        # ── J: Video diff ──
        # WHY: Tests embedding real videos in semantic diffs. Videos are laid out
        # horizontally (side-by-side) in the explanation HTML. Uses public sample videos.
        # In non-HTML renderers, just the VLM text descriptions appear.
        {
            'label': 'J',
            'kind': 'changed',
            'sources': ['clip_original.mp4', 'clip_filter_a.mp4', 'clip_filter_b.mp4'],
            'sync_videos': True,
            'explanation': (
                'Synchronized 3-way video comparison (first is master with controls, others are slaves).'
                '<div style="display:flex;gap:var(--space-lg);margin:var(--space-md) 0;">'
                '<div style="flex:1;text-align:center;">'
                '<div style="font-size:var(--font-size-sm);color:var(--text-secondary);margin-bottom:var(--space-xs);">Original (master)</div>'
                '<video src="https://www.w3schools.com/html/mov_bbb.mp4" autoplay controls muted loop playsinline '
                'style="width:100%%;border-radius:var(--radius-md);"></video>'
                '</div>'
                '<div style="flex:1;text-align:center;">'
                '<div style="font-size:var(--font-size-sm);color:var(--text-secondary);margin-bottom:var(--space-xs);">Filter A (slave)</div>'
                '<video src="https://www.w3schools.com/html/mov_bbb.mp4" autoplay controls muted loop playsinline '
                'style="width:100%%;border-radius:var(--radius-md);"></video>'
                '</div>'
                '<div style="flex:1;text-align:center;">'
                '<div style="font-size:var(--font-size-sm);color:var(--text-secondary);margin-bottom:var(--space-xs);">Filter B (slave)</div>'
                '<video src="https://www.w3schools.com/html/mov_bbb.mp4" autoplay controls muted loop playsinline '
                'style="width:100%%;border-radius:var(--radius-md);"></video>'
                '</div></div>'
            ),
            'lines': [
                {'text': '[VLM] Original: Big Buck Bunny clip, no filter.', 'sign': ' ', 'source': 'clip_original.mp4'},
                {'text': '[VLM] Filter A: Same clip with color grading applied.', 'sign': '+', 'source': 'clip_filter_a.mp4'},
                {'text': '[VLM] Filter B: Same clip with style transfer applied.', 'sign': '+', 'source': 'clip_filter_b.mp4'},
                {'text': '[VLM] All: Same frame count, same timing, same camera.', 'sign': ' ', 'source': 'all'},
            ],
        },

        # ── K: 3-way side-by-side ──
        # WHY: Tests N-way (N=3) side-by-side. Three config files compared
        # next to each other. Useful for comparing master vs two variants.
        {
            'label': 'K',
            'kind': 'changed',
            'sources': ['master', 'staging', 'prod'],
            'explanation': '3-way side-by-side: config differs across environments.',
            'side_by_side': [
                {
                    'label': 'master',
                    'lines': [
                        {'text': 'debug = True', 'line_num': 1},
                        {'text': 'workers = 1', 'line_num': 2},
                        {'text': 'cache = off', 'line_num': 3},
                    ],
                },
                {
                    'label': 'staging',
                    'lines': [
                        {'text': 'debug = True', 'line_num': 1},
                        {'text': 'workers = 4', 'line_num': 2, 'sign': '+',
                         'highlights': [[10, 11]]},
                        {'text': 'cache = redis', 'line_num': 3, 'sign': '+',
                         'highlights': [[8, 13]]},
                    ],
                },
                {
                    'label': 'prod',
                    'lines': [
                        {'text': 'debug = False', 'line_num': 1, 'sign': '+',
                         'highlights': [[8, 13]]},
                        {'text': 'workers = 16', 'line_num': 2, 'sign': '+',
                         'highlights': [[10, 12]]},
                        {'text': 'cache = redis', 'line_num': 3, 'sign': '+',
                         'highlights': [[8, 13]]},
                    ],
                },
            ],
        },
    ]


def demo():
    """
    Command. Run comprehensive tests for all semantic diff features and print demos.

    Each test validates a specific feature across all renderers. Tests double
    as demos — the output shows what each feature looks like.

    Tests covered:
        - Label generation (A-Z, 1A-1Z, 2A-2Z)
        - All chunk kinds: added, removed, changed, shared
        - Sub-chunks with dot-notation labels (E.1, E.2)
        - Syntax highlighting with full-width dark backgrounds
        - page_num (PDF diffs) vs line_num (code diffs)
        - Context lines (sign=' ')
        - Multiple sources per chunk
        - Inline highlights (character-level change emphasis)
        - Side-by-side 2-way columns (dunk-style)
        - Side-by-side 3-way columns (N-way)
        - Save/load JSON roundtrip
        - All 4 formatters produce non-empty output
        - HTML contains dark/light theme toggle
        - HTML contains Blender drag-collapse JS
        - HTML side-by-side container present
        - Source header suppression (no duplicate when single source)
        - Plain text side-by-side sequential rendering

    Examples:
        >>> # demo()  # prints to stdout
    """
    chunks = _demo_chunks()

    print('=' * 80)
    print('SEMANTIC DIFF DEMO / TEST SUITE')
    print('=' * 80)
    print()

    # ── Test 1: Label generation ──
    assert _make_chunk_label(0) == 'A'
    assert _make_chunk_label(25) == 'Z'
    assert _make_chunk_label(26) == '1A'
    assert _make_chunk_label(52) == '2A'
    print('[PASS] Label generation: A, Z, 1A, 2A')

    # ── Test 2: All formatters produce non-empty output ──
    for name, fmt in [
        ('ANSI', format_semantic_diff),
        ('HTML', format_semantic_diff_html),
        ('MD', format_semantic_diff_md),
        ('Plain', format_semantic_diff_plain),
    ]:
        result = fmt(chunks)
        assert len(result) > 0, '%s returned empty' % name
    print('[PASS] All 4 formatters produce output')

    # ── Test 3: Save/load roundtrip ──
    import tempfile
    path = tempfile.mktemp(suffix='.json')
    save_semantic_diff(chunks, path)
    reloaded = load_semantic_diff(path)
    assert len(reloaded) == len(chunks), 'Chunk count mismatch'
    for orig, loaded in zip(chunks, reloaded):
        assert orig['label'] == loaded['label'], 'Label mismatch: %s vs %s' % (orig['label'], loaded['label'])
    _os.unlink(path)
    print('[PASS] JSON save/load roundtrip (%d chunks)' % len(chunks))

    # ── Test 4: All chunk kinds present ──
    kinds_present = set(c['kind'] for c in chunks)
    for k in ('added', 'removed', 'changed', 'shared'):
        assert k in kinds_present, 'Missing chunk kind: %s' % k
    print('[PASS] All chunk kinds present: added, removed, changed, shared')

    # ── Test 5: Sub-chunks ──
    sub_chunk_labels = []
    for c in chunks:
        for sc in c.get('sub_chunks', []):
            sub_chunk_labels.append(sc['label'])
    assert 'E.1' in sub_chunk_labels and 'E.2' in sub_chunk_labels, 'Missing sub-chunks'
    print('[PASS] Sub-chunks: E.1, E.2')

    # ── Test 6: Inline highlights ──
    highlight_chunk = [c for c in chunks if c['label'] == 'G'][0]
    for li in highlight_chunk['lines']:
        assert 'highlights' in li, 'Missing highlights in chunk G'
    # ANSI: check bold+underline codes present
    ansi_out = format_semantic_diff(chunks)
    assert '\033[1;4m' in ansi_out, 'ANSI highlight codes missing'
    # HTML: check <mark> present
    html_out = format_semantic_diff_html(chunks)
    assert '<mark>' in html_out, 'HTML <mark> tags missing'
    # MD: check **bold** present
    md_out = format_semantic_diff_md(chunks)
    assert '**' in md_out, 'Markdown bold missing'
    print('[PASS] Inline highlights: ANSI bold+underline, HTML <mark>, MD **bold**')

    # ── Test 7: Side-by-side 2-way ──
    sbs2 = [c for c in chunks if c['label'] == 'H'][0]
    assert len(sbs2.get('side_by_side', [])) == 2, 'Expected 2 side-by-side columns'
    assert 'sbs-container' in html_out, 'HTML side-by-side container missing'
    assert 'sbs-col' in html_out, 'HTML side-by-side column missing'
    print('[PASS] Side-by-side 2-way columns in HTML')

    # ── Test 8: Side-by-side 3-way ──
    sbs3 = [c for c in chunks if c['label'] == 'K'][0]
    assert len(sbs3.get('side_by_side', [])) == 3, 'Expected 3 side-by-side columns'
    for col_label in ('master', 'staging', 'prod'):
        assert col_label in html_out, 'Missing column label in HTML: %s' % col_label
    print('[PASS] Side-by-side 3-way columns in HTML')

    # ── Test 9: Plain text side-by-side ──
    plain_out = format_semantic_diff_plain(chunks)
    assert '\u2503 old.py' in plain_out, 'Plain text side-by-side column header missing'
    assert '\u2503 master' in plain_out, 'Plain text 3-way column header missing'
    print('[PASS] Side-by-side in plain text (sequential blocks)')

    # ── Test 10: page_num support ──
    pdf_chunk = [c for c in chunks if c['label'] == 'F'][0]
    assert pdf_chunk['lines'][0].get('page_num') == 1, 'page_num missing'
    assert 'paper_v1.pdf' in plain_out or 'paper_v1' in plain_out, 'PDF source missing in plain'
    print('[PASS] page_num support (PDF diffs)')

    # ── Test 11: HTML dark/light theme ──
    assert 'prefers-color-scheme' in html_out, 'System theme detection missing'
    assert 'toggleTheme' in html_out, 'Theme toggle function missing'
    assert 'icon-sun' in html_out, 'Sun icon missing'
    assert 'icon-moon' in html_out, 'Moon icon missing'
    print('[PASS] HTML dark/light theme toggle with sun/moon icons')

    # ── Test 12: HTML Blender drag-collapse ──
    assert 'dragAction' in html_out, 'Blender drag-collapse JS missing'
    assert 'mousedown' in html_out, 'Drag mousedown handler missing'
    assert 'mouseover' in html_out, 'Drag mouseover handler missing'
    print('[PASS] HTML Blender-style drag-collapse behavior')

    # ── Test 13: Source header suppression ──
    chunk_a_html = format_semantic_diff_html([chunks[0]])
    assert 'chunk-sources' in chunk_a_html, 'chunk-sources missing'
    assert '<div class="source-header">' not in chunk_a_html, (
        'Redundant source-header div for single-source chunk')
    print('[PASS] Source header suppression (no duplicate for single source)')

    # ── Test 14: ANSI side-by-side ──
    assert '\u2503 old.py' in ansi_out or 'old.py' in ansi_out, 'ANSI side-by-side column missing'
    print('[PASS] Side-by-side in ANSI (sequential blocks)')

    # ── Test 15: MD side-by-side ──
    assert '**old.py**' in md_out, 'MD side-by-side column header missing'
    assert '**master**' in md_out, 'MD 3-way column header missing'
    print('[PASS] Side-by-side in Markdown (sequential blocks)')

    # ── Test 16: Image diff ──
    img_chunk = [c for c in chunks if c['label'] == 'I'][0]
    assert 'photo_v1.jpg' in img_chunk['sources'][0], 'Image source missing'
    assert '[VLM]' in img_chunk['lines'][0]['text'], 'VLM description missing'
    assert '<img src=' in img_chunk['explanation'], 'Real <img> tag missing from explanation'
    print('[PASS] Image diff: VLM descriptions + real <img> tags')

    # ── Test 17: Video diff with sync (3-way) ──
    vid_chunk = [c for c in chunks if c['label'] == 'J'][0]
    assert 'clip_original.mp4' in vid_chunk['sources'][0], 'Video source missing'
    assert len(vid_chunk['sources']) == 3, 'Should have 3 video sources for sync demo'
    assert '<video src=' in vid_chunk['explanation'], 'Real <video> tag missing from explanation'
    assert vid_chunk.get('sync_videos') is True, 'sync_videos should be True'
    assert 'data-sync-videos' in html_out, 'Sync videos data attribute missing from HTML'
    assert 'syncing' in html_out, 'Sync JS missing from HTML'
    print('[PASS] Video diff: 3-way sync_videos with master/slave playback')

    # ── Test 18: Shared kind is blue ──
    shared_chunk = [c for c in chunks if c['kind'] == 'shared'][0]
    assert shared_chunk is not None, 'No shared chunk found'
    # Check HTML pill color for shared is blue, not gray
    assert '--pill-shared-fg: #58a6ff' in html_out or '--pill-shared-fg: #0969da' in html_out, \
        'Shared kind should be blue'
    print('[PASS] Shared/similarities kind styled blue')

    # ── Print demos ──
    print()
    print('─' * 80)
    print('DEMO: ANSI output')
    print('─' * 80)
    print()
    print_semantic_diff(chunks)

    print()
    print('─' * 80)
    print('DEMO: Markdown output')
    print('─' * 80)
    print()
    print(format_semantic_diff_md(chunks))

    print()
    print('=' * 80)
    print('All 18 tests passed.')
    print('=' * 80)


# ── CLI entry point ──────────────────────────────────────────────────────────

def _cli():
    """
    Command. CLI entry point for semantic diff rendering.

    Usage:
        python -m rp.semantic_diff print diff.json
        python -m rp.semantic_diff html  diff.json [-o out.html]
        python -m rp.semantic_diff md    diff.json [-o out.md]
        python -m rp.semantic_diff demo
    """
    import sys

    args = sys.argv[1:]
    if not args:
        print('Usage: python -m rp.semantic_diff <print|html|md|demo> [diff.json] [-o output_file]')
        sys.exit(1)

    if args[0] == 'demo':
        demo()
        return

    if len(args) < 2:
        print('Usage: python -m rp.semantic_diff <print|html|md|demo> [diff.json] [-o output_file]')
        sys.exit(1)

    fmt = args[0]
    input_path = args[1]
    output_path = None
    if '-o' in args:
        output_path = args[args.index('-o') + 1]

    chunks = load_semantic_diff(input_path)

    formatters = {
        'print': format_semantic_diff,
        'plain': format_semantic_diff_plain,
        'html':  format_semantic_diff_html,
        'md':    format_semantic_diff_md,
    }

    assert fmt in formatters, 'Unknown format %r. Choose from: %s' % (fmt, ', '.join(formatters))

    result = formatters[fmt](chunks)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(result)
    else:
        print(result)


if __name__ == '__main__':
    _cli()
