"""
Bash/shell completion support for rp's pseudo terminal.

This handles completion for lines starting with '!' which execute shell commands.
Returns raw Candidate objects; parent completer handles fuzzy matching and caching.
"""
from __future__ import unicode_literals

import os
import re
from rp.rp_ptpython.completion_types import Candidate

__all__ = ('BashCompleter',)


def get_apt_completions():
    """Get available apt packages for completion."""
    import subprocess
    try:
        result = subprocess.run(['apt-cache', 'pkgnames'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, timeout=2)
        return result.stdout.strip().split('\n')
    except:
        return []


class BashCompleter:
    """
    Raw candidate provider for shell commands (lines starting with !).

    Handles:
    - System commands
    - Command flags and arguments via completion_schema
    - apt package names
    - Environment variables
    - File paths

    Returns Candidate objects; parent completer handles fuzzy matching and caching.
    """

    def __init__(self):
        self._program_descriptions = {}
        try:
            from rp.rp_ptpython.completion_schema import PROGRAM_DESCRIPTIONS
            self._program_descriptions = PROGRAM_DESCRIPTIONS
        except ImportError:
            pass

    def get_raw_candidates(self, document):
        """Get raw shell command candidates."""
        if not document.text.startswith('!'):
            return []

        origin = document.get_word_before_cursor()
        before_line = document.current_line_before_cursor
        after_line = document.current_line_after_cursor
        
        # Try schema-based completion first (for flags, subcommands, etc.)
        try:
            from rp.rp_ptpython.completion_schema import (
                get_completions_for_command,
                complete_paths,
                tokenize_bash_command,
                find_cursor_token,
            )

            bash_text = document.text.lstrip()[1:]
            bash_cursor_pos = document.cursor_position - (
                len(document.text) - len(document.text.lstrip())
            ) - 1

            # Get tokens for path completion
            tokens = tokenize_bash_command(bash_text)
            cursor_token_idx, is_after = find_cursor_token(tokens, bash_cursor_pos)

            # Check if we're completing a command name (position 0)
            is_completing_command = cursor_token_idx == 0 and not is_after

            schema_completions = get_completions_for_command(bash_text, bash_cursor_pos)

            candidates = []

            # Add schema completions with priority=0 (highest)
            if schema_completions:
                has_descriptions = isinstance(schema_completions, dict)
                completion_list = (
                    list(schema_completions.keys())
                    if has_descriptions
                    else schema_completions
                )

                for text in completion_list:
                    if has_descriptions:
                        value = schema_completions.get(text, '')
                        if isinstance(value, tuple):
                            display, description = value
                        else:
                            display = text
                            description = value
                    else:
                        display = text
                        description = ''

                    candidates.append(Candidate(
                        name=text,
                        display=display,
                        display_meta=description,
                        priority=0
                    ))

            # Add path completions with priority=1 (lower) unless completing command name
            if not is_completing_command and not after_line:
                path_completions = complete_paths(tokens, cursor_token_idx, is_after)
                if path_completions:
                    for path_text, desc in path_completions.items():
                        # Skip if already in schema completions
                        if schema_completions and path_text in (schema_completions if isinstance(schema_completions, dict) else schema_completions):
                            continue
                        candidates.append(Candidate(
                            name=path_text,
                            display_meta=desc,
                            priority=1
                        ))

            if candidates:
                return candidates
        except Exception:
            pass
        
        # Handle environment variables
        if '$' in before_line:
            dollar_idx = before_line.rfind('$')
            text_after_dollar = before_line[dollar_idx + 1:]
            cursor_in_variable = False

            if text_after_dollar == '' or text_after_dollar.replace('_', '').replace('{', '').isalnum():
                cursor_in_variable = True

            if cursor_in_variable:
                env_vars = set(os.environ.keys())

                # Parse buffer for variable assignments
                buffer_vars = set()
                for var_match in re.finditer(
                    r'\b(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=',
                    document.text
                ):
                    buffer_vars.add(var_match.group(1))

                all_vars = sorted(buffer_vars) + sorted(env_vars - buffer_vars)
                return [Candidate(name=var) for var in all_vars]
        
        # Handle apt install
        if before_line.startswith('!sudo apt install'):
            return [Candidate(name=pkg) for pkg in get_apt_completions()]
        
        # Handle system commands
        bls = before_line.split()
        is_command_position = (
            before_line.startswith('!') and
            not (before_line[1:].startswith('/') or before_line[1:].startswith('.')) and
            (
                (len(bls) == 1 and (before_line.strip() == before_line or bls[0] == '!sudo')) or
                (len(bls) == 2 and bls[0] == '!sudo' and
                 (not bls[1].startswith('.') or bls[1].startswith('/')) and
                 before_line == before_line.strip())
            )
        )

        if is_command_position and not after_line:
            import rp
            system_commands = rp.r._get_cached_system_commands()
            return [
                Candidate(name=cmd, display_meta=self._program_descriptions.get(cmd, ''))
                for cmd in system_commands
            ]
        

        return []
