from __future__ import unicode_literals, absolute_import
from pygments.token import Token

from rp.prompt_toolkit.enums import DEFAULT_BUFFER
from rp.prompt_toolkit.layout.processors import AfterInput

from rp.rp_ptpdb.commands import completion_hints


class CompletionHint(AfterInput):
    """
    Completion hint to be shown after the input.
    """
    def __init__(self):
        def get_tokens(cli):
            buffer = cli.buffers[DEFAULT_BUFFER]
            words = buffer.document.text.split()
            if len(words) == 1:
                word = words[0]

                for commands, help in completion_hints:
                    if word in commands:
                        return [(Token, ' ')] + self._highlight_completion(help)

            return []
        super(CompletionHint, self).__init__(get_tokens)

    def _highlight_completion(self, text):
        """
        Choose tokens for special characters in the text of the completion
        hint.
        """
        def highlight_char(c):
            if c in '[:]|.()':
                return Token.CompletionHint.Symbol, c
            else:
                return Token.CompletionHint.Parameter, c
        return [highlight_char(c) for c in text]
