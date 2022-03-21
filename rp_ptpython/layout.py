"""
Creation of the `Layout` instance for the Python input/REPL.
"""
from __future__ import unicode_literals

from rp.prompt_toolkit.enums import DEFAULT_BUFFER, SEARCH_BUFFER
from rp.prompt_toolkit.filters import IsDone, HasCompletions, RendererHeightIsKnown, HasFocus, Condition
from rp.prompt_toolkit.key_binding.vi_state import InputMode
from rp.prompt_toolkit.layout.containers import Window, HSplit, VSplit, FloatContainer, Float, ConditionalContainer, ScrollOffsets
from rp.prompt_toolkit.layout.controls import BufferControl, TokenListControl, FillControl, UIContent
from rp.prompt_toolkit.layout.dimension import LayoutDimension
from rp.prompt_toolkit.layout.lexers import SimpleLexer
from rp.prompt_toolkit.layout.margins import PromptMargin
from rp.prompt_toolkit.layout.menus import CompletionsMenu, MultiColumnCompletionsMenu
from rp.prompt_toolkit.layout.processors import ConditionalProcessor, AppendAutoSuggestion, HighlightSearchProcessor, HighlightSelectionProcessor, HighlightMatchingBracketProcessor, Processor, Transformation
from rp.prompt_toolkit.layout.screen import Char
from rp.prompt_toolkit.layout.toolbars import CompletionsToolbar, ArgToolbar, SearchToolbar, ValidationToolbar, SystemToolbar, TokenListToolbar
from rp.prompt_toolkit.layout.utils import token_list_width
from rp.prompt_toolkit.reactive import Integer
from rp.prompt_toolkit.selection import SelectionType
from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.selection import SelectionState

from .filters import HasSignature, ShowSidebar, ShowSignature, ShowDocstring,ShowRealtimeInput,ShowVarSpace,ShowVarSpaceAndShowRealtimeInput,ShowVarSpaceOrShowRealtimeInput,ShowParenthesisAutomator
from .utils import if_mousedown

from pygments.lexers import PythonLexer
from pygments.token import Token

import platform
import sys

__all__ = (
    'create_layout',
    'CompletionVisualisation',
)


# DisplayMultipleCursors: Only for rp.prompt_toolkit>=1.0.8
try:
    from rp.prompt_toolkit.layout.processors import DisplayMultipleCursors
except ImportError:
    class DisplayMultipleCursors(Processor):
        " Dummy. "
        def __init__(self, *a):
            pass

        def apply_transformation(self, cli, document, lineno,
                                 source_to_display, tokens):
            return Transformation(tokens)


class CompletionVisualisation:
    " Visualisation method for the completions. "
    NONE = 'none'
    POP_UP = 'pop-up'
    MULTI_COLUMN = 'multi-column'
    TOOLBAR = 'toolbar'


def show_completions_toolbar(python_input):
    return Condition(lambda cli: python_input.completion_visualisation == CompletionVisualisation.TOOLBAR)


def show_completions_menu(python_input):
    return Condition(lambda cli: python_input.completion_visualisation == CompletionVisualisation.POP_UP)


def show_multi_column_completions_menu(python_input):
    return Condition(lambda cli: python_input.completion_visualisation == CompletionVisualisation.MULTI_COLUMN)


def python_sidebar(python_input):
    """
    Create the `Layout` for the sidebar with the configurable options.
    """
    def get_tokens(cli):
        tokens = []
        T = Token.Sidebar

        def append_category(category):
            tokens.extend([
                (T, '  '),
                (T.Title, '   %-36s' % category.title),
                (T, '\n'),
            ])

        def append(index, label, status):
            selected = index == python_input.selected_option_index

            @if_mousedown
            def select_item(cli, mouse_event):
                python_input.selected_option_index = index

            @if_mousedown
            def goto_next(cli, mouse_event):
                " Select item and go to next value. "
                python_input.selected_option_index = index
                option = python_input.selected_option
                option.activate_next()

            token = T.Selected if selected else T

            tokens.append((T, ' >' if selected else '  '))
            tokens.append((token.Label, '%-24s' % label, select_item))
            tokens.append((token.Status, ' ', select_item))
            tokens.append((token.Status, '%s' % status, goto_next))

            if selected:
                tokens.append((Token.SetCursorPosition, ''))

            tokens.append((token.Status, ' ' * (13 - len(status)), goto_next))
            tokens.append((T, '<' if selected else ''))
            tokens.append((T, '\n'))

        i = 0
        for category in python_input.options:
            append_category(category)

            for option in category.options:
                append(i, option.title, '%s' % option.get_current_value())
                i += 1

        tokens.pop()  # Remove last newline.

        return tokens

    class Control(TokenListControl):
        def move_cursor_down(self, cli):
            python_input.selected_option_index += 1

        def move_cursor_up(self, cli):
            python_input.selected_option_index -= 1

    return ConditionalContainer(
        content=Window(
            Control(get_tokens, Char(token=Token.Sidebar),
                has_focus=ShowSidebar(python_input) & ~IsDone()),
            width=LayoutDimension.exact(43),
            height=LayoutDimension(min=3),
            scroll_offsets=ScrollOffsets(top=1, bottom=1)),
        filter=ShowSidebar(python_input) & ~IsDone())


def python_sidebar_navigation(python_input):
    """
    Create the `Layout` showing the navigation information for the sidebar.
    """
    def get_tokens(cli):
        tokens = []
        T = Token.Sidebar

        # Show navigation info.
        tokens.extend([
            (T.Separator, ' ' * 43 + '\n'),
            (T, '    '),
            (T.Key, '[Arrows]'),
            (T, ' '),
            (T.Key.Description, 'Navigate'),
            (T, ' '),
            (T.Key, '[F5]'),
            (T, ' '),
            (T.Key.Description, 'Save Settings'),
        ])

        return tokens

    return ConditionalContainer(
        content=Window(
            TokenListControl(get_tokens, Char(token=Token.Sidebar)),
            width=LayoutDimension.exact(43),
            height=LayoutDimension.exact(2)),
        filter=ShowSidebar(python_input) & ~IsDone())


def python_sidebar_help(python_input):
    """
    Create the `Layout` for the help text for the current item in the sidebar.
    """
    token = Token.Sidebar.HelpText

    def get_current_description():
        """
        Return the description of the selected option.
        """
        i = 0
        for category in python_input.options:
            for option in category.options:
                if i == python_input.selected_option_index:
                    return option.description
                i += 1
        return ''

    def get_tokens(cli):
        return [(token, get_current_description())]

    return ConditionalContainer(
        content=Window(
            TokenListControl(get_tokens, Char(token=token)),
            height=LayoutDimension(min=3)),
        filter=ShowSidebar(python_input) &
               Condition(lambda cli: python_input.show_sidebar_help) & ~IsDone())


def signature_toolbar(python_input):
    """
    Return the `Layout` for the signature.
    """
    def get_tokens(cli):
        result = []
        append = result.append
        Signature = Token.Toolbar.Signature

        if python_input.signatures:
            sig = python_input.signatures[0]  # Always take the first one.

            append((Signature, ' '))
            try:
                append((Signature, sig.full_name))
            except:# IndexError but Also AttributeError: 'NoneType' object has no attribute 'split'
                # Workaround for #37: https://github.com/jonathanslenders/python-prompt-toolkit/issues/37
                # See also: https://github.com/davidhalter/jedi/issues/490
                return []

            append((Signature.Operator, '('))

            try:
                enumerated_params = enumerate(sig.params)
            except AttributeError:
                # Workaround for #136: https://github.com/jonathanslenders/ptpython/issues/136
                # AttributeError: 'Lambda' object has no attribute 'get_subscope_by_name'
                return []

            for i, p in enumerated_params:
                try:
                    # Workaround for #47: 'p' is None when we hit the '*' in the signature.
                    #                     and sig has no 'index' attribute.
                    # See: https://github.com/jonathanslenders/ptpython/issues/47
                    #      https://github.com/davidhalter/jedi/issues/598
                    description = (p.description if p else '*') #or '*'
                    sig_index = getattr(sig, 'index', 0)

                    #region Ryan Burgert Code (it was annoying seeing f(param x,param y) etc. So I got rid of the 'param' stuff and now it looks nicer
                    desc_string=str(description)
                    if desc_string.startswith("param "):
                        desc_string=desc_string[6:]
                    #endregion
                    if i == sig_index:
                        # Note: we use `_Param.description` instead of
                        #       `_Param.name`, that way we also get the '*' before args.
                        append((Signature.CurrentName,desc_string))
                    else:
                        append((Signature,desc_string))
                    append((Signature.Operator, ', '))
                except:
                    #NOTE: This used to be printed...but seeing as this bug never seemed to cause any problems and only spammed the terminal, I'm getting rid of it. I bet you'll never notice...
                    # print("(Just caught a bug that would have crashed the prompt-toolkit gui. Why did this happen??)")
                    pass#I don't know why, but this broke pseudo terminal. I don't know what this is but I don't really care...it's not worth crashing over...

            if sig.params:
                # Pop last comma
                result.pop()

            append((Signature.Operator, ')'))
            append((Signature, ' '))
        return result

    return ConditionalContainer(
        content=Window(
            TokenListControl(get_tokens),
            height=LayoutDimension.exact(1)),
        filter=
            # Show only when there is a signature
            HasSignature(python_input) &
            # And there are no completions to be shown. (would cover signature pop-up.)
            ~(HasCompletions() & (show_completions_menu(python_input) |
                                   show_multi_column_completions_menu(python_input)))
            # Signature needs to be shown.
            & ShowSignature(python_input) &
            # Not done yet.
            ~IsDone())


class PythonPromptMargin(PromptMargin):
    """
    Create margin that displays the prompt.
    It shows something like "In [1]:".
    """
    def __init__(self, python_input):
        self.python_input = python_input

        def get_prompt_style():
            return python_input.all_prompt_styles[python_input.prompt_style]

        def get_prompt(cli):
            return get_prompt_style().in_tokens(cli)

        def get_continuation_prompt(cli, width):
            return get_prompt_style().in2_tokens(cli, width)

        super(PythonPromptMargin, self).__init__(get_prompt, get_continuation_prompt,
                show_numbers=Condition(lambda cli: python_input.show_line_numbers))


def status_bar(python_input):
    """
    Create the `Layout` for the status bar.
    """
    TB = Token.Toolbar.Status

    @if_mousedown
    def toggle_mouse_support(cli, mouse_event):
        python_input.enable_mouse_support = not python_input.enable_mouse_support

    @if_mousedown
    def toggle_microcompletions(cli, mouse_event):
        python_input.enable_microcompletions = not python_input.enable_microcompletions

    @if_mousedown
    def toggle_wrap_lines(cli, mouse_event):
        python_input.wrap_lines = not python_input.wrap_lines

    @if_mousedown
    def toggle_paste_mode(cli, mouse_event):
        python_input.paste_mode = not python_input.paste_mode

    @if_mousedown
    def enter_history(cli, mouse_event):
        python_input.enter_history(cli)

    def get_tokens(cli):
        python_buffer = cli.buffers[DEFAULT_BUFFER]

        result = []
        append = result.append

        if hasattr(python_input,'session_title') and python_input.session_title:
            # append((Token.Window.Title, python_input.session_title, toggle_microcompletions))
            append((TB.PseudoTerminalCurrentVariable, python_input.session_title, toggle_microcompletions))
        else:
            pass
        

        append((TB, ' '))
        result.extend(get_inputmode_tokens(cli, python_input))


        # Position in history.
        append((TB, '%i/%i ' % (python_buffer.working_index + 1,
                                len(python_buffer._working_lines))))

        # Shortcuts.
        if not python_input.vi_mode and cli.current_buffer_name == SEARCH_BUFFER:
            append((TB, '[Ctrl-G] Cancel search [Enter] Go to this position.'))
        elif bool(cli.current_buffer.selection_state) and not python_input.vi_mode:
            # Emacs cut/copy keys.
            append((TB, '[Ctrl-W] Cut [Meta-W] Copy [Ctrl-Y] Paste [Ctrl-G] Cancel'))
        else:


            result.extend([
                (TB.Key, '[F3]', enter_history),
                (TB, 'History ', enter_history),
                (TB.Key, '[F6]', toggle_paste_mode),
                # (TB, ' ', toggle_paste_mode),
            ])

            if python_input.paste_mode:
                append((TB.PasteModeOn, 'Paste:On  ', toggle_paste_mode))
            else:
                append((TB, 'Paste:Off ', toggle_paste_mode))

            result.extend([
                (TB.Key, '[F1]', toggle_mouse_support),
            ])
            if python_input.enable_mouse_support:
                append((TB.PasteModeOn, 'Mouse:On  ', toggle_mouse_support))
            else:
                append((TB, 'Mouse:Off ', toggle_mouse_support))

            

            result.extend([
                (TB.Key, '[F7]', toggle_wrap_lines),
            ])
            if hasattr(python_input,'wrap_lines') and python_input.wrap_lines:
                append((TB, 'Wrap:On  ', toggle_wrap_lines))
            else:
                append((TB.PasteModeOn, 'Wrap:Off ', toggle_wrap_lines))



            result.extend([
                (TB.Key, '[F8]', toggle_microcompletions),
            ])
            if hasattr(python_input,'enable_microcompletions') and python_input.enable_microcompletions:
                append((TB, 'Micro:On  ', toggle_microcompletions))
            else:
                append((TB.PasteModeOn, 'Micro:Off ', toggle_microcompletions))
            

            # if hasattr(python_input,'session_title') and python_input.session_title:
            #     # append((Token.Window.Title, python_input.session_title, toggle_microcompletions))
            #     append((TB.PseudoTerminalCurrentVariable, python_input.session_title, toggle_microcompletions))
            # else:
            #     pass
            



        #region RYAN BURGERT CODE GOES HERE FOR PSEUDOTERMINAL STUFF
        if hasattr(python_input,'show_last_assignable') and python_input.show_last_assignable:
            append((TB, ' '))
            @if_mousedown
            def testytest(cli,mouse_event):
                # python_input.enter_history(cli)
                pass
            import rp.r_iterm_comm
            append((TB.PseudoTerminalCurrentVariable,repr(rp.r_iterm_comm.last_assignable_comm),testytest))
            append((TB, ' '))
        return result

    return TokenListToolbar(
        get_tokens,
        default_char=Char(token=TB),
        filter=~IsDone() & RendererHeightIsKnown() &
            Condition(lambda cli: python_input.show_status_bar and
                                  not python_input.show_exit_confirmation))

selection_flag=False
def get_inputmode_tokens(cli, python_input):
    """
    Return current input mode as a list of (token, text) tuples for use in a
    toolbar.

    :param cli: `CommandLineInterface` instance.
    """
    @if_mousedown
    def toggle_vi_mode(cli, mouse_event):
        python_input.vi_mode = not python_input.vi_mode

    token = Token.Toolbar.Status

    mode = cli.vi_state.input_mode
    result = []
    append = result.append

    append((token.InputMode, '[F4] ', toggle_vi_mode))

    #region  RYAN BURGERT CODE: This code is called every time the user makes a selection. I'm going to use this to chage the selection area to make more sense (in my opinion)
    global selection_flag
    buffer=cli.current_buffer
    has_selection=bool(buffer.selection_state)# Handling on_new_selection...
    if has_selection and not selection_flag:# We made a new selection
        document=buffer.document
        assert isinstance(document,Document)
        assert isinstance(document._selection,SelectionState)
        #
        cursor,cursor_orig=document.cursor_position,document._selection.original_cursor_position
        if cursor>cursor_orig:
            cursor-=1
        elif cursor<cursor_orig:
            cursor_orig-=1
        #
        try:
            buffer.document=Document(document.text,cursor_position=cursor,selection=None)
        except:
            pass
        buffer.document._selection=SelectionState(original_cursor_position=cursor_orig,type=document.selection.type)
        #
        # from rp import text_to_speech
        # text_to_speech("HI")# For debugging
    selection_flag=has_selection
    #endregion

    # InputMode
    if python_input.vi_mode:
        if has_selection:
            if buffer.selection_state.type == SelectionType.LINES:
                append((token.InputMode, 'Vi (VISUAL LINE)', toggle_vi_mode))
            elif buffer.selection_state.type == SelectionType.CHARACTERS:
                append((token.InputMode, 'Vi (VISUAL)', toggle_vi_mode))
                append((token, ' '))
            elif buffer.selection_state.type == 'BLOCK':
                append((token.InputMode, 'Vi (VISUAL BLOCK)', toggle_vi_mode))
                append((token, ' '))
        elif mode in (InputMode.INSERT, 'vi-insert-multiple'):
            append((token.InputMode, 'Vi (INSERT)', toggle_vi_mode))
            append((token, '  '))
        elif mode == InputMode.NAVIGATION:
            append((token.InputMode, 'Vi (NAV)', toggle_vi_mode))
            append((token, '     '))
        elif mode == InputMode.REPLACE:
            append((token.InputMode, 'Vi (REPLACE)', toggle_vi_mode))
            append((token, ' '))
    else:
        append((token.InputMode, 'RP-Emacs', toggle_vi_mode))
        append((token, ' '))

    return result


def show_sidebar_button_info(python_input):
    """
    Create `Layout` for the information in the right-bottom corner.
    (The right part of the status bar.)
    """
    @if_mousedown
    def toggle_sidebar(cli, mouse_event):
        " Click handler for the menu. "
        python_input.show_sidebar = not python_input.show_sidebar

    token = Token.Toolbar.Status

    version = sys.version_info
    import datetime
    remove_beginning_zero=lambda x:x[1:] if x[0] == '0' else x
    import rp

    # if not hasattr(python_input,'session_title'):
    #     title=''
    # else:
    #     title=python_input.session_title
    # TB = Token.Toolbar.Status

    get_tokens=lambda cli: [

        # (Token.Window.Title, title),
        # (token.Key, title),
        # (TB.PseudoTerminalCurrentVariable, title),
        (token, ' '),
        *(
            [
                (token.BatteryPluggedIn if rp.battery_plugged_in() else token.BatteryNotPluggedIn,"🔋 "*0+str(rp.battery_percentage())[:6]+'%'),# put the time here
                (token, ' ')
            ]
            if hasattr(python_input,'show_battery_life') and python_input.show_battery_life
            else []
        ),
        (token,(remove_beginning_zero(datetime.datetime.now().strftime("%I:%M%p")).lower())),# put the time here
        (token, ' '),
        (token.Key, '[F2]', toggle_sidebar),
        (token, ' Menu', toggle_sidebar),
        # (token, ' - '),
        # (token.PythonVersion, '%s %i.%i.%i' % (platform.python_implementation(),
        #                                        version[0], version[1], version[2])),
        (token, ' '),
    ]
    width = token_list_width(get_tokens(None))

    # def get_tokens(cli):
    #     Python version
        # return tokens

    return ConditionalContainer(
        content=Window(
            TokenListControl(get_tokens, default_char=Char(token=token)),
            height=LayoutDimension.exact(1),
            width=LayoutDimension.exact(width)),
        filter=~IsDone() & RendererHeightIsKnown() &
            Condition(lambda cli: python_input.show_status_bar and
                                  not python_input.show_exit_confirmation))


def exit_confirmation(python_input, token=Token.ExitConfirmation):
    """
    Create `Layout` for the exit message.
    """
    def get_tokens(cli):
        # Show "Do you really want to exit?"
        return [
            (token, '\n %s ([y]/n)' % python_input.exit_message),
            (Token.SetCursorPosition, ''),
            (token, '  \n'),
        ]

    visible = ~IsDone() & Condition(lambda cli: python_input.show_exit_confirmation)

    return ConditionalContainer(
        content=Window(TokenListControl(
            get_tokens, default_char=Char(token=token), has_focus=visible)),
        filter=visible)


def meta_enter_message(python_input):
    """
    Create the `Layout` for the 'Meta+Enter` message.
    """
    def get_tokens(cli):
        return [(Token.AcceptMessage, ' [Meta+Enter] Execute ')]

    def extra_condition(cli):
        " Only show when... "
        b = cli.buffers[DEFAULT_BUFFER]

        return (
            python_input.show_meta_enter_message and
            (not b.document.is_cursor_at_the_end or
                python_input.accept_input_on_enter is None) and
            b.is_multiline())

    visible = ~IsDone() & HasFocus(DEFAULT_BUFFER) & Condition(extra_condition)

    return ConditionalContainer(
        content=Window(TokenListControl(get_tokens)),
        filter=visible)


def create_layout(python_input,
                  lexer=PythonLexer,
                  extra_body=None, extra_toolbars=None,
                  extra_buffer_processors=None, input_buffer_height=None):
    D = LayoutDimension
    extra_body = [extra_body] if extra_body else []
    extra_toolbars = extra_toolbars or []
    extra_buffer_processors = extra_buffer_processors or []
    input_buffer_height = input_buffer_height or D(min=6)# This is the space between the input prompt and the toolbar. It lets the autocompletion menus have reaonable height.

    def create_python_input_window():
        def menu_position(cli):
            """
            When there is no autocompletion menu to be shown, and we have a signature,
            set the pop-up position at `bracket_start`.
            """
            b = cli.buffers[DEFAULT_BUFFER]

            if b.complete_state is None and python_input.signatures:
                row, col = python_input.signatures[0].bracket_start
                index = b.document.translate_row_col_to_index(row - 1, col)
                return index

        return Window(
            BufferControl(
                buffer_name=DEFAULT_BUFFER,
                lexer=lexer,
                input_processors=[
                    ConditionalProcessor(
                        processor=HighlightSearchProcessor(preview_search=True),
                        filter=HasFocus(SEARCH_BUFFER),
                    ),
                    HighlightSelectionProcessor(),
                    DisplayMultipleCursors(DEFAULT_BUFFER),
                    # Show matching parentheses, but only while editing.
                    ConditionalProcessor(
                        processor=HighlightMatchingBracketProcessor(chars='[](){}'),
                        filter=HasFocus(DEFAULT_BUFFER) & ~IsDone() &
                            Condition(lambda cli: python_input.highlight_matching_parenthesis)),
                    ConditionalProcessor(
                        processor=AppendAutoSuggestion(),
                        filter=~IsDone())
                ] + extra_buffer_processors,
                menu_position=menu_position,

                # Make sure that we always see the result of an reverse-i-search:
                preview_search=True,
            ),
            left_margins=[PythonPromptMargin(python_input)],
            # Scroll offsets. The 1 at the bottom is important to make sure the
            # cursor is never below the "Press [Meta+Enter]" message which is a float.
            scroll_offsets=ScrollOffsets(bottom=1, left=4, right=4),
            # As long as we're editing, prefer a minimal height of 6.
            get_height=(lambda cli: (
                None if cli.is_done or python_input.show_exit_confirmation
                        else input_buffer_height)),
            wrap_lines=Condition(lambda cli: python_input.wrap_lines),
        )
    def title_fill(title,fill=' ',style=Token.Window.TIItleV2):
        height=title.count("\n")+1
        import rp.r_iterm_comm
        rp.r_iterm_comm.python_input_buffers[title]=title
        try:
            return VSplit([
            Window(height=D.exact(height),content=FillControl(fill,token=style)),
            Window(BufferControl(buffer_name=title,lexer=SimpleLexer(default_token=style),),wrap_lines=False,height=D.exact(height),width=D.exact(max(len(x)for x in title.split('\n')))),
            Window(height=D.exact(height),content=FillControl(fill,token=style)),
                    ])
        except:
            return Window(height=D.exact(1),content=FillControl(fill,token=Token.Separator))
    import rp
    return HSplit([
                      VSplit([
                          HSplit([
                              FloatContainer(
                                  content=HSplit(
                                      [create_python_input_window()] + extra_body
                                  ),
                                  floats=[
                                      Float(xcursor=True,
                                            ycursor=True,
                                            content=CompletionsMenu(
                                                scroll_offset=Integer.from_callable(
                                                    lambda:python_input.completion_menu_scroll_offset),
                                                max_height=12,
                                                extra_filter=show_completions_menu(python_input))),
                                      Float(xcursor=True,
                                            ycursor=True,
                                            content=MultiColumnCompletionsMenu(
                                                extra_filter=show_multi_column_completions_menu(python_input))),
                                      Float(xcursor=True,
                                            ycursor=True,
                                            content=signature_toolbar(python_input)),
                                      Float(left=2,
                                            bottom=1,
                                            content=exit_confirmation(python_input)),
                                      Float(bottom=0,right=0,height=1,
                                            content=meta_enter_message(python_input),
                                            hide_when_covering_content=True),
                                      Float(bottom=1,left=1,right=0,content=python_sidebar_help(python_input)),
                                  ]),
                              ArgToolbar(),
                              SearchToolbar(),
                              SystemToolbar(),
                              ValidationToolbar(),
                              CompletionsToolbar(extra_filter=show_completions_toolbar(python_input)),
                              # Docstring region.
                              ConditionalContainer(
                                  content=Window(height=D.exact(1),
                                                 content=FillControl('\u2500',token=Token.Separator)),
                                  filter=HasSignature(python_input) & ShowDocstring(python_input) & ~IsDone()),
                              ConditionalContainer(
                                  content=Window(
                                      BufferControl(
                                          buffer_name='docstring',
                                          lexer=SimpleLexer(default_token=Token.Docstring),
                                          # lexer=PythonLexer,
                                      ),
                                      height=D(max=12)),
                                  filter=HasSignature(python_input) & ShowDocstring(python_input) & ~IsDone(),
                              ),
                              # realtime display region RYAN BURGERT CODE zone
                              # ConditionalContainer(
                              #     content=Window(height=D.exact(1),content=FillControl('\u2500',token=Token.Separator)),
                              #     filter=ShowVarSpaceOrShowRealtimeInput(python_input) & ~IsDone()),
                              ConditionalContainer(


                                  content=
                                  HSplit([
                                      # title_fill("Parenthesis Automator"),
                                      # Window(BufferControl(buffer_name='parenthesizer_buffer',lexer=lexer,),wrap_lines=False,height=D(max=rp.r_iterm_comm.parenthesized_line.count('\n'),min=rp.r_iterm_comm.parenthesized_line.count('\n')    ))
                                      Window(BufferControl(buffer_name='parenthesizer_buffer',lexer=lexer,),wrap_lines=False)
                                      # title_fill(rp.r_iterm_comm.parenthesized_line),
                                  ]),
                                  filter=ShowParenthesisAutomator(python_input) & ~IsDone(),
                              ),
                              VSplit([
                                  ConditionalContainer(
                                      content=
                                      HSplit([
                                          # title_fill("Realtime Evaluator"),
                                          Window(BufferControl(buffer_name='realtime_display',
                                                               # lexer=SimpleLexer(default_token=Token.Docstring)
                                                               lexer=lexer
                                                               ,),wrap_lines=True,height=D(weight=2))
                                      ]),
                                      filter=ShowRealtimeInput(python_input) & ~IsDone(),
                                  ),
                                  ConditionalContainer(
                                      content=Window(width=D.exact(1),
                                                     content=FillControl('│',token=Token.Window.TIItleV2)),
                                      filter=ShowVarSpaceAndShowRealtimeInput(python_input) & ~IsDone()),
                                  ConditionalContainer(


                                      content=
                                      HSplit([
                                          # title_fill("VARS"),
                                          Window(BufferControl(buffer_name='vars',
                                                               lexer=SimpleLexer(default_token=Token.Docstring)
                                                               # lexer=lexer
                                                               ,),wrap_lines=True)
                                      ]),
                                      filter=ShowVarSpace(python_input) & ~IsDone(),
                                  ),
                                ]),
                          ]),
                          HSplit([
                              python_sidebar(python_input),
                              python_sidebar_navigation(python_input),
                          ])
                      ]),
                  ] + extra_toolbars + [
                      VSplit([
                          status_bar(python_input),
                          show_sidebar_button_info(python_input),
                      ])
                  ])
