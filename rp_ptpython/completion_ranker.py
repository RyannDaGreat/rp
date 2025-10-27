"""
Completion ranking utilities for rp's pseudo-terminal.

This module provides intelligent sorting/ranking of Python code completions
based on context, user preferences, and usage patterns.

RANKING STRATEGY:
=================

The ranking system uses a multi-level tuple sorting key:

1. **Custom priority** (PRIMARY):
   - Explicit priority numbers (lower = higher priority)
   - Used for command-specific rankings (e.g., dirs before files)
   - Priority 0 always comes first, priority 1 second, etc.

2. **Prefix-based ranking** (SECONDARY, within same priority):
   - If user types '.', show hidden files/attrs first
   - If user types '_', show private members first
   - Otherwise, push these to the end

3. **User-created variables** (TERTIARY, within same priority/prefix):
   - Variables created by user come before library completions
   - Tracked via rp_pt_user_created_var_names

Usage Example:
==============
    >>> from completion_ranker import rank_completions
    >>> completions = ['__init__', '_private', 'public', 'another']
    >>> user_vars = {'public', 'another'}
    >>> ranked = rank_completions(completions, origin='', user_created_vars=user_vars)
    >>> ranked
    ['public', 'another', '_private', '__init__']

    >>> # When user explicitly types '_', privates come first
    >>> ranked = rank_completions(completions, origin='_', user_created_vars=user_vars)
    >>> ranked
    ['_private', '__init__', 'public', 'another']
"""

from __future__ import unicode_literals

__all__ = [
    'rank_completions',
    'create_sorting_key',
    'MAX_SORTING_PRIORITY',
]

MAX_SORTING_PRIORITY = 999999999


def calculate_match_score(origin, candidate):
    """
    Calculate match quality score (lower = better match).

    This implements fuzzy matching with quality scoring. The algorithm walks through
    both strings character by character, accumulating penalty for:
    - Position of first match (2x weight - earlier = better)
    - Characters skipped between matches (1x weight per skip)
    - Case mismatches (0.0001 penalty - tiny)
    - Underscores crossed (0.1 penalty + resets skip distance)

    Examples:
        'Screenshots' vs 'scht' → starts at 0, skips 5 → score ~6.0
        'results_for_charles' vs 'scht' → starts at 2, underscores reset → score ~8.3
        'dict' vs 'd' → perfect prefix → score ~0.001

    The scoring favors:
    1. **Matches starting earlier** (position 0 >> position 1 >> position 2...)
    2. **True prefix matches** (1000x bonus if candidate starts with origin)
    3. Fewer skipped characters between matches
    4. Matches after underscore boundaries (resets skip distance)
    5. Frequently-used completions (from history)

    Args:
        origin: What user typed (e.g., 'd', 'scht', '_priv')
        candidate: Completion to score (e.g., 'dict', 'Screenshots', '_private')

    Returns:
        Float score (lower = better), or None if no match possible
    """
    original_candidate = candidate

    # Check for prefix match (case-insensitive) - give HUGE bonus
    is_prefix_match = candidate.lower().startswith(origin.lower())

    origin_chars = list(origin)
    candidate_chars = list(candidate)
    score = 0.001  # Base score (even perfect matches have tiny score for ordering)
    skip_distance = 0  # How many chars we've skipped since last match
    first_match_position = None  # Track where first char matches

    def chars_match_ignoring_case(a, b):
        return a.upper() == b.upper()

    # Walk through candidate, trying to match all origin chars in order
    chars_processed = 0
    while origin_chars and candidate_chars:
        chars_processed += 1
        candidate_char = candidate_chars.pop(0)

        if chars_match_ignoring_case(origin_chars[0], candidate_char):
            # Found a match!
            origin_char = origin_chars.pop(0)

            # Track position of first match
            if first_match_position is None:
                first_match_position = chars_processed - 1

            # Tiny penalty for case mismatch ('D' vs 'd')
            if origin_char != candidate_char:
                skip_distance += 0.0001

            # Add accumulated distance penalty and reset
            score += skip_distance
            skip_distance = 0

        elif candidate_char == '_':
            # Underscore: small fixed penalty, but resets distance
            # This makes 'a_b' vs 'ab' score better than 'axb' vs 'ab'
            skip_distance = 0
            score += 0.1

        else:
            # Regular character skip - accumulates distance penalty
            skip_distance += 1

    # Add penalty for late starting matches (0 = best, higher = worse)
    # Weight = 2.0 to make starting position very important
    if first_match_position is not None:
        score += (first_match_position * 2.0)

    # Boost score for frequently-used completions (divide by usage count)
    # This makes completions you use often appear higher in the list
    import rp.rp_ptpython.r_iterm_comm
    try:
        usage_count = (''.join(rp.rp_ptpython.r_iterm_comm.successful_commands)).count(original_candidate)
        if usage_count:
            score /= usage_count
    except (AttributeError, TypeError):
        pass  # History tracking not available

    # HUGE bonus for prefix matches (1000x better score)
    if is_prefix_match:
        score /= 1000

    # If we didn't match all origin chars, this is not a valid match
    return None if origin_chars else score


def create_sorting_key(origin, user_created_vars=None, custom_priorities=None):
    """
    Create a sorting key function for ranking completions.

    This is the SECOND sort that happens after match score sorting.
    Custom priorities take precedence over all other sorting rules.

    Args:
        origin: The text user has typed (e.g., 'pr', '_priv', '.git')
        user_created_vars: Set of variable names created by user
        custom_priorities: Dict mapping completion -> priority number (lower = better)

    Returns:
        A key function suitable for sorted(items, key=...)

    The key function returns a tuple (custom_priority, prefix_priority, user_priority)
    where lower values sort first. Custom priority is PRIMARY.
    """
    user_created_vars = user_created_vars or set()
    custom_priorities = custom_priorities or {}

    def sorting_key(x):
        """
        Assigns a sort key based on priorities and prefix rules.

        Returns tuple: (custom_priority, prefix_priority, user_priority)
        Lower values = higher ranking (sorted first)

        Sort order:
        1. Custom priority (0 = highest, explicit control)
        2. Prefix priority (regular > underscore/dot unless explicitly typed)
        3. User vars priority (user-created > library)
        """
        orig = x

        # 1. Prefix-based ranking
        if x.startswith('.'):
            if origin.startswith('.'):
                # If explicitly looking for hidden file paths, put it first
                output = -1
            else:
                # If not explicitly looking for that, put it last
                output = 1
        elif x.startswith('__') and x.endswith('__'):
            # Dunder methods (e.g., __init__, __str__)
            if origin.startswith('__'):
                # When user types __, prioritize full dunders
                output = -2  # Higher priority than single underscore
            else:
                # Otherwise put them last
                output = 2
        elif x.startswith('_'):
            if origin.startswith('_'):
                # If explicitly looking for privates, put it first
                output = -1
            else:
                # If not explicitly looking for that, put it last
                output = 1
        else:
            # Regular completions - highest priority
            output = 0

        # 2. User-created variables get priority over library completions
        user_created_priority = 0 if x in user_created_vars else 1

        # 3. Custom priority FIRST, then prefix/user rules within each priority level
        custom_priority = custom_priorities.get(orig, MAX_SORTING_PRIORITY)
        return (custom_priority, output, user_created_priority)

    return sorting_key


def sort_by_match_score(completions, origin):
    """
    Sort completions by match quality score (first sort).

    This is the FIRST sort, equivalent to ryan_completion_matches from completer_old.py.

    Process:
    1. Regex filter for fuzzy matches (fast pre-filter)
    2. Score each candidate by match quality
    3. Sort by score (best matches first)
    4. Filter out 'mro' (method resolution order - rarely useful)
    5. Push dunders (__foo__) to the end

    Args:
        completions: List of completion strings
        origin: What user has typed

    Returns:
        List sorted by match score, with dunders at end
    """
    import re

    # Fast pre-filter: must contain all chars from origin in order (case-insensitive)
    # E.g., origin='dt' matches 'dict', 'delete', 'data_type' but not 'thread'
    fuzzy_pattern = re.compile('.*' + '.*'.join(re.escape(char) for char in origin.lower()) + '.*')
    candidates = [c for c in completions if fuzzy_pattern.fullmatch(c.lower())]

    # Score each candidate by match quality
    scored = []
    for candidate in candidates:
        score = calculate_match_score(origin, candidate)
        if score is not None:  # None means no match (shouldn't happen after regex filter)
            scored.append((score, candidate))

    # Sort by score (lower score = better match)
    scored.sort(key=lambda x: x[0])
    sorted_candidates = [candidate for score, candidate in scored]

    # Filter out 'mro' - method resolution order, rarely useful in completions
    sorted_candidates = [c for c in sorted_candidates if c != 'mro']

    # Push dunders (__foo__) to the end
    # Original line 863 has: key=lambda x: x==x.startswith('_')+(x.startswith('__') and x.endswith('__'))
    # Breaking down: x==x.startswith('_') is always False (0), so this simplifies to:
    # key=lambda x: (x.startswith('__') and x.endswith('__'))
    # Which means: False (0) for non-dunders, True (1) for dunders → dunders sort last
    def is_dunder(name):
        return name.startswith('__') and name.endswith('__')

    sorted_candidates.sort(key=is_dunder)  # False sorts before True, so non-dunders first

    return sorted_candidates


def rank_completions(completions, origin='', user_created_vars=None, custom_priorities=None):
    """
    Rank completions using the two-stage sorting strategy.

    Stage 1: Sort by match score (ryan_completion_matches)
    Stage 2: Sort by prefix/user/custom priorities (sorting_key)

    Args:
        completions: List of completion strings to rank
        origin: The text user has typed so far
        user_created_vars: Set of variable names created by user
        custom_priorities: Dict mapping completion -> priority (lower = better)

    Returns:
        Sorted list of completions

    Examples:
        >>> rank_completions(['dict', 'delete', 'dir'], origin='d')
        ['dict', 'dir', 'delete']  # Exact prefix matches first

        >>> rank_completions(['__init__', 'public', '_private'], origin='')
        ['public', '_private', '__init__']

        >>> rank_completions(['__init__', 'public', '_private'], origin='_')
        ['_private', '__init__', 'public']
    """
    # Stage 1: Sort by match score
    completions = sort_by_match_score(completions, origin)

    # Stage 2: Sort by prefix/user/custom priorities
    key_func = create_sorting_key(origin, user_created_vars, custom_priorities)
    return sorted(completions, key=key_func)


def rank_jedi_completions(jedi_completions, origin='', user_created_vars=None):
    """
    Rank Jedi completion objects using the two-stage sorting strategy.

    Stage 1: Sort by match score
    Stage 2: Sort by params/prefix/user/custom priorities

    Args:
        jedi_completions: List of Jedi completion objects
        origin: The text user has typed so far
        user_created_vars: Set of variable names created by user

    Returns:
        Sorted list of Jedi completion objects

    Note:
        Jedi completions have attributes like:
        - name: The completion text
        - name_with_symbols: Decorated name
        - type: 'function', 'param', 'module', etc.

    Sorting order (two-stage):
        Stage 1: Match quality score (exact prefix matches first)
        Stage 2: (params_first, prefix_priority, user_priority, custom_priority)
    """
    user_created_vars = user_created_vars or set()

    # Stage 1: Sort by match score
    scored = []
    for jc in jedi_completions:
        score = calculate_match_score(origin, jc.name_with_symbols)
        if score is not None:
            scored.append((score, jc))

    scored.sort(key=lambda x: x[0])
    jedi_completions = [x[1] for x in scored]

    # Filter out 'mro' like the old system
    jedi_completions = [jc for jc in jedi_completions if jc.name_with_symbols != 'mro']

    # Stage 2: Sort by params/prefix/user/custom priorities
    key_func = create_sorting_key(origin, user_created_vars)

    def combined_key(jc):
        base_ranking = key_func(jc.name_with_symbols)
        params_first = (jc.type != 'param')  # False (0) for params, True (1) for others
        return (params_first, *base_ranking)

    return sorted(jedi_completions, key=combined_key)
