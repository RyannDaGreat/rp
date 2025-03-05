"""
CommandLineInterface for reading Python input.
This can be used for creation of Python REPLs.

::

    cli = PythonCommandLineInterface()
    cli.run()
"""
from __future__ import unicode_literals
import rp.r_iterm_comm as ric
from rp.prompt_toolkit import AbortAction
from rp.prompt_toolkit.auto_suggest import AutoSuggestFromHistory,ConditionalAutoSuggest
from rp.prompt_toolkit.buffer import Buffer
from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.enums import DEFAULT_BUFFER,EditingMode
from rp.prompt_toolkit.filters import Condition,Always
from rp.prompt_toolkit.history import FileHistory,InMemoryHistory
from rp.prompt_toolkit.interface import CommandLineInterface,Application,AcceptAction
from rp.prompt_toolkit.key_binding.defaults import load_key_bindings_for_prompt,load_mouse_bindings
from rp.prompt_toolkit.key_binding.vi_state import InputMode
from rp.prompt_toolkit.key_binding.registry import MergedRegistry,ConditionalRegistry
from rp.prompt_toolkit.layout.lexers import PygmentsLexer
from rp.prompt_toolkit.shortcuts import create_output
from rp.prompt_toolkit.styles import DynamicStyle
from rp.prompt_toolkit.utils import is_windows
from rp.prompt_toolkit.validation import ConditionalValidator

from .completer import PythonCompleter
from .history_browser import create_history_application
from .key_bindings import load_python_bindings,load_sidebar_bindings,load_confirm_exit_bindings
from .layout import create_layout,CompletionVisualisation
from .prompt_style import IPythonPrompt,ClassicPrompt
from .style import get_all_code_styles,get_all_ui_styles,generate_style
from .utils import get_jedi_script_from_document,document_is_multiline_python
from .validator import PythonValidator

from functools import partial

import rp.r_iterm_comm as r_iterm_comm

import six
import __future__

if six.PY2:
    from pygments.lexers import PythonLexer
else:
    from pygments.lexers import Python3Lexer as PythonLexer

__all__=(
    'PythonInput',
    'PythonCommandLineInterface',
)

import rp.r_iterm_comm as ric
def set_debug_height(height):
    ric.debug_height=height
    return height

def set_history_line_limit(number_of_lines):
    from rp.r import _globa_pyin
    _globa_pyin[0].history_number_of_lines=number_of_lines
    return number_of_lines
def get_history_line_limit():
    from rp.r import _globa_pyin
    return _globa_pyin[0].history_number_of_lines

class OptionCategory(object):
    def __init__(self,title,options):
        assert isinstance(title,six.text_type)
        assert isinstance(options,list)

        self.title=title
        self._options=options

    @property
    def options(self):
        return [option for option in self._options if option.is_visible()]
    

class Option(object):
    """
    Ptpython configuration option that can be shown and modified from the
    sidebar.

    :param title: Text.
    :param description: Text.
    :param get_values: Callable that returns a dictionary mapping the
            possible values to callbacks that activate these value.
    :param get_current_value: Callable that returns the current, active value.
    """
    def __init__(self,title,description,get_current_value,get_values,is_visible=lambda:True):
        assert isinstance(title,six.text_type)
        assert isinstance(description,six.text_type)
        assert callable(get_current_value)
        assert callable(get_values)

        self.title=title
        self.description=description
        self.get_current_value=get_current_value
        self.get_values=get_values
        self.is_visible=is_visible

    @property
    def values(self):
        return self.get_values()

    def activate_next(self,_previous=False):
        """
        Activate next value.
        """
        current=self.get_current_value()
        options=sorted(self.values.keys())

        # Get current index.
        try:
            index=options.index(current)
        except ValueError:
            index=0

        # Go to previous/next index.
        if _previous:
            index-=1
        else:
            index+=1

        # Call handler for this option.
        next_option=options[index % len(options)]
        self.values[next_option]()

    def activate_previous(self):
        """
        Activate previous value.
        """
        self.activate_next(_previous=True)

class PythonInput(object):
    """
    Prompt for reading Python input.

    ::

        python_input = PythonInput(...)
        application = python_input.create_application()
        cli = PythonCommandLineInterface(application=application)
        python_code = cli.run()
    """
    def __init__(self,
            get_globals=None,get_locals=None,history_filename=None,
            vi_mode=False,
            # For internal use.
            _completer=None,_validator=None,
            _lexer=None,_extra_buffers=None,_extra_buffer_processors=None,
            _on_start=None,
            _extra_layout_body=None,_extra_toolbars=None,
            _input_buffer_height=None,
            _accept_action=AcceptAction.RETURN_DOCUMENT,
            _on_exit=AbortAction.RAISE_EXCEPTION):
        self.get_globals=get_globals or (lambda:{})
        self.get_locals=get_locals or self.get_globals

        self.show_parenthesis_automator=False

        self._completer=_completer or PythonCompleter(self.get_globals,self.get_locals)
        self._validator=_validator or PythonValidator(self.get_compiler_flags)
        self.history=FileHistory(history_filename) if history_filename else InMemoryHistory()
        self._lexer=_lexer or PygmentsLexer(PythonLexer)
        self._extra_buffers=_extra_buffers
        self._accept_action=_accept_action
        self._on_exit=_on_exit
        self._on_start=_on_start

        self._input_buffer_height=_input_buffer_height
        self._extra_layout_body=_extra_layout_body or []
        self._extra_toolbars=_extra_toolbars or []
        self._extra_buffer_processors=_extra_buffer_processors or []

        # Settings.
        self.show_signature=False
        self.show_docstring=False
        self.show_realtime_input=False
        self.show_vars=False
        self.show_meta_enter_message=True
        self.completion_visualisation=CompletionVisualisation.MULTI_COLUMN
        self.completion_menu_scroll_offset=1

        self.show_line_numbers=False
        self.show_status_bar=True
        self.wrap_lines=True
        self.complete_while_typing=True
        self.vi_mode=vi_mode
        self.paste_mode=False  # When True, don't insert whitespace after newline.
        self.confirm_exit=True  # Ask for confirmation when Control-D is pressed.
        self.accept_input_on_enter=2  # Accept when pressing Enter 'n' times.
        # 'None' means that meta-enter is always required.
        self.enable_open_in_editor=True
        self.enable_system_bindings=True
        self.enable_input_validation=True
        self.enable_auto_suggest=False
        self.enable_mouse_support=False
        self.enable_history_search=False  # When True, like readline, going
        # back in history will filter the
        # history on the records starting
        # with the current input.
        self.highlight_matching_parenthesis=False
        self.show_sidebar=False  # Currently show the sidebar.
        self.show_sidebar_help=True  # When the sidebar is visible, also show the help text.
        self.show_exit_confirmation=False  # Currently show 'Do you really want to exit?'
        self.terminal_title=None  # The title to be displayed in the terminal. (None or string.)
        self.exit_message='Do you really want to exit?'
        self.insert_blank_line_after_output=True  # (For the REPL.)

        # Tokens to be shown at the prompt.
        self.prompt_style='classic'  # The currently active style.

        self.all_prompt_styles={  # Styles selectable from the menu.
            'ipython':IPythonPrompt(self),
            'classic':ClassicPrompt(),
        }

        self.get_input_prompt_tokens=lambda cli: \
            self.all_prompt_styles[self.prompt_style].in_tokens(cli)

        self.get_output_prompt_tokens=lambda cli: \
            self.all_prompt_styles[self.prompt_style].out_tokens(cli)

        #: Load styles.
        self.code_styles=get_all_code_styles()
        self.ui_styles=get_all_ui_styles()
        self._current_code_style_name='default'
        self._current_ui_style_name='default'

        if is_windows():
            self._current_code_style_name='win32'

        self._current_style=self._generate_style()
        self.true_color=False

        # Options to be configurable from the sidebar.
        self.options=self._create_options()
        self.selected_option_index=0

        #: Incremeting integer counting the current statement.
        self.current_statement_index=1

        # Code signatures. (This is set asynchronously after a timeout.)
        self.signatures=[]

        self.waa=True# RYAN BURGERT STUFF
        self.sand_creature='dust ball'

        # Create a Registry for the key bindings.
        self.key_bindings_registry=MergedRegistry([
            ConditionalRegistry(
                registry=load_key_bindings_for_prompt(
                    enable_abort_and_exit_bindings=True,
                    enable_search=True,
                    enable_open_in_editor=Condition(lambda cli:self.enable_open_in_editor),
                    enable_system_bindings=Condition(lambda cli:self.enable_system_bindings),
                    enable_auto_suggest_bindings=Condition(lambda cli:self.enable_auto_suggest)),
                # Disable all default key bindings when the sidebar or the exit confirmation
                # are shown.
                filter=Condition(lambda cli:not (self.show_sidebar or self.show_exit_confirmation))
            ),
            load_mouse_bindings(),
            load_python_bindings(self),
            load_sidebar_bindings(self),
            load_confirm_exit_bindings(self),
        ])

        # Boolean indicating whether we have a signatures thread running.
        # (Never run more than one at the same time.)
        self._get_signatures_thread_running=False

    @property
    def option_count(self):
        " Return the total amount of options. (In all categories together.) "
        return sum(len(category.options) for category in self.options)

    @property
    def selected_option(self):
        " Return the currently selected option. "
        i=0
        for category in self.options:
            for o in category.options:
                if i == self.selected_option_index:
                    return o
                else:
                    i+=1
        return category.options[-1]

    def get_compiler_flags(self):
        """
        Give the current compiler flags by looking for _Feature instances
        in the globals.
        """
        flags=0

        for value in self.get_globals().values():
            if isinstance(value,__future__._Feature):
                flags|=value.compiler_flag

        return flags

    @property
    def add_key_binding(self):
        """
        Shortcut for adding new key bindings.
        (Mostly useful for a .ptpython/config.py file, that receives
        a PythonInput/Repl instance as input.)

        ::

            @python_input.add_key_binding(Keys.ControlX, filter=...)
            def handler(event):
                ...
        """
        # Extra key bindings should not be active when the sidebar is visible.
        sidebar_visible=Condition(lambda cli:self.show_sidebar)

        def add_binding_decorator(*keys,**kw):
            # Pop default filter keyword argument.
            filter=kw.pop('filter',Always())
            assert not kw

            return self.key_bindings_registry.add_binding(*keys,filter=filter & ~sidebar_visible)
        return add_binding_decorator

    def install_code_colorscheme(self,name,style_dict):
        """
        Install a new code color scheme.
        """
        assert isinstance(name,six.text_type)
        assert isinstance(style_dict,dict)

        self.code_styles[name]=style_dict

    def use_code_colorscheme(self,name):
        """
        Apply new colorscheme. (By name.)
        """
        assert name in self.code_styles

        self._current_code_style_name=name
        self._current_style=self._generate_style()

    def install_ui_colorscheme(self,name,style_dict):
        """
        Install a new UI color scheme.
        """
        assert isinstance(name,six.text_type)
        assert isinstance(style_dict,dict)

        self.ui_styles[name]=style_dict

    def use_ui_colorscheme(self,name):
        """
        Apply new colorscheme. (By name.)
        """
        assert name in self.ui_styles

        self._current_ui_style_name=name
        self._current_style=self._generate_style()

    def _generate_style(self):
        """
        Create new Style instance.
        (We don't want to do this on every key press, because each time the
        renderer receives a new style class, he will redraw everything.)
        """
        return generate_style(self.code_styles[self._current_code_style_name],
                              self.ui_styles[self._current_ui_style_name])
    def _create_options(self):
        """
        Create a list of `Option` instances for the options sidebar.
        """
        def enable(attribute,value=True):
            setattr(self,attribute,value)

            # Return `True`, to be able to chain this in the lambdas below.
            return True

        def disable(attribute):
            setattr(self,attribute,False)
            return True

        def simple_option(title,description,field_name,values=None,is_visible=lambda:True):
            " Create Simple on/of option. "
            values=values or ['off','on']

            def get_current_value():
                return values[bool(getattr(self,field_name,'(Broken)'))]

            def get_values():
                return {
                    values[1]:lambda:enable(field_name),
                    values[0]:lambda:disable(field_name),
                }

            return Option(title=title,description=description,
                          get_values=get_values,
                          get_current_value=get_current_value,
                          is_visible=is_visible)
        def doge(self):
            setattr(self,'sand_creature',"Option Camel")
            # This hasn't aged well :( Fuck Trump and fuck elon - they ruined a meme!
            # from doge.core import main
            # main()

        return [
            OptionCategory('Input',[
                simple_option(title='Input mode',
                              description='Vi or emacs key bindings.',
                              field_name='vi_mode',
                              values=['emacs','vi']),
                simple_option(title='Microcompletions',
                              description='When in RP-Emacs mode, should we enable microcompletions?',
                              field_name='enable_microcompletions',
                              values=[False,True]),
                simple_option(title='Paste mode',
                        # is_visible=lambda:getattr(self,'show_all_options',True),
                              description="When enabled, don't indent automatically.",
                              field_name='paste_mode'),
                Option(title='Complete while typing',
                       description="Generate autocompletions automatically while typing. "
                                   'Don\'t require pressing TAB. (Not compatible with "History search".)',
                       get_current_value=lambda:['off','on'][self.complete_while_typing],
                       get_values=lambda:{
                           'on':lambda:enable('complete_while_typing'),
                           'off':lambda:disable('complete_while_typing'),
                       }),
                Option(title='History search',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                       description='When pressing the up-arrow, filter the history on input starting '
                                   'with the current text. (Not compatible with "Complete while typing".)',
                       get_current_value=lambda:['off','on'][self.enable_history_search],
                       get_values=lambda:{
                           'on':lambda:enable('enable_history_search'),
                           'off':lambda:disable('enable_history_search'),
                       }),
                simple_option(title='Mouse support',
                              description='Respond to mouse clicks and scrolling for positioning the cursor, '
                                          'selecting text and scrolling through windows.',
                              field_name='enable_mouse_support'),
                simple_option(title='Confirm on exit',
                    is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Require confirmation when exiting.',
                              field_name='confirm_exit'),
                simple_option(title='Input validation',
                    is_visible=lambda:getattr(self,'show_all_options',True),
                              description='In case of syntax errors, move the cursor to the error '
                                          'instead of showing a traceback of a SyntaxError.',
                              field_name='enable_input_validation'),
                simple_option(title='Auto suggestion',
                    is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Auto suggest inputs by looking at the history. '
                                          'Pressing right arrow or Ctrl-E will complete the entry.',
                              field_name='enable_auto_suggest'),
                Option(title='Accept input on enter',
                    is_visible=lambda:getattr(self,'show_all_options',True),
                       description='Amount of ENTER presses required to execute input when the cursor '
                                   'is at the end of the input. (Note that META+ENTER will always execute.)',
                       get_current_value=lambda:str(self.accept_input_on_enter or 'meta-enter'),
                       get_values=lambda:{
                           '2':lambda:enable('accept_input_on_enter',2),
                           '3':lambda:enable('accept_input_on_enter',3),
                           '4':lambda:enable('accept_input_on_enter',4),
                           'meta-enter':lambda:enable('accept_input_on_enter',None),
                       }),
            ]),
            OptionCategory('Display',[
                Option(title='Completions',
                       description='Visualisation to use for displaying the completions. (Multiple columns, one column, a toolbar or nothing.)',
                       get_current_value=lambda:self.completion_visualisation,
                       get_values=lambda:{
                           CompletionVisualisation.NONE:lambda:enable('completion_visualisation',CompletionVisualisation.NONE),
                           CompletionVisualisation.POP_UP:lambda:enable('completion_visualisation',CompletionVisualisation.POP_UP),
                           CompletionVisualisation.MULTI_COLUMN:lambda:enable('completion_visualisation',CompletionVisualisation.MULTI_COLUMN),
                           CompletionVisualisation.TOOLBAR:lambda:enable('completion_visualisation',CompletionVisualisation.TOOLBAR),
                       }),
                #I DISABLED THIS BECAUSE IT'S DEPRECATED NOW - NOW YOU USE 'SET STYLE'
                # Option(title='Prompt',
                #         is_visible=lambda:getattr(self,'show_all_options',True),
                #        description="Visualisation of the prompt. ('>>>' or 'In [1]:')",
                #        get_current_value=lambda:self.prompt_style,
                #        get_values=lambda:dict((s,partial(enable,'prompt_style',s)) for s in self.all_prompt_styles)),
                simple_option(title='Blank line after output',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                              description='Insert a blank line after the output.',
                              field_name='insert_blank_line_after_output'),
                simple_option(title='Show signature',
                              description='Display function signatures.',
                              field_name='show_signature'),
                simple_option(title='Show docstring',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Display function docstrings.',
                              field_name='show_docstring'),
                simple_option(title='Show line numbers',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Show line numbers when the input consists of multiple lines.',
                              field_name='show_line_numbers'),
                simple_option(title='Show Meta+Enter message',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Show the [Meta+Enter] message when this key combination is required to execute commands. ' +
                                          '(This is the case when a simple [Enter] key press will insert a newline.',
                              field_name='show_meta_enter_message'),
                simple_option(title='Wrap lines',
                              description='Wrap lines instead of scrolling horizontally.',
                              field_name='wrap_lines'),
                                simple_option(title='History Highlighting',
                              description='When using F3 (aka History Broswer) to select entries from history,  '
                                          'should we use syntax highlighting? Its pretty, but slow.',
                              field_name='history_syntax_highlighting'),
                Option(title='History Browser Limit',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                       description='How many lines should we display when using F3 history? Less is faster\nMaking this smaller decreases the latency of pressing F3',
                       get_current_value=lambda:str(get_history_line_limit()).rjust(12),
                       get_values=lambda:{'asdpoa':lambda:None,
                            '           1':lambda:set_history_line_limit(1          ),
                            '           5':lambda:set_history_line_limit(5          ),
                            '          10':lambda:set_history_line_limit(10          ),
                            '          20':lambda:set_history_line_limit(20          ),
                            '          30':lambda:set_history_line_limit(30          ),
                            '          40':lambda:set_history_line_limit(40          ),
                            '          50':lambda:set_history_line_limit(50          ),
                            '         100':lambda:set_history_line_limit(100         ),
                            '         150':lambda:set_history_line_limit(150         ),
                            '         200':lambda:set_history_line_limit(200         ),
                            '         250':lambda:set_history_line_limit(250         ),
                            '         300':lambda:set_history_line_limit(300         ),
                            '         400':lambda:set_history_line_limit(400         ),
                            '         500':lambda:set_history_line_limit(500         ),
                            '         600':lambda:set_history_line_limit(600         ),
                            '         700':lambda:set_history_line_limit(700         ),
                            '         800':lambda:set_history_line_limit(800         ),
                            '         900':lambda:set_history_line_limit(900         ),
                            '        1000':lambda:set_history_line_limit(1000        ),
                            '        1500':lambda:set_history_line_limit(1500        ),
                            '        2000':lambda:set_history_line_limit(2000        ),
                            '        2500':lambda:set_history_line_limit(2500        ),
                            '        3000':lambda:set_history_line_limit(3000        ),
                            '        3500':lambda:set_history_line_limit(3500        ),
                            '        4000':lambda:set_history_line_limit(4000        ),
                            '        4500':lambda:set_history_line_limit(4500        ),
                            '        5000':lambda:set_history_line_limit(5000        ),
                            '        6000':lambda:set_history_line_limit(6000        ),
                            '        7000':lambda:set_history_line_limit(7000        ),
                            '        8000':lambda:set_history_line_limit(8000        ),
                            '        9000':lambda:set_history_line_limit(9000        ),
                            '       10000':lambda:set_history_line_limit(10000       ),
                            '       15000':lambda:set_history_line_limit(15000       ),
                            '       20000':lambda:set_history_line_limit(20000       ),
                            '       25000':lambda:set_history_line_limit(25000       ),
                            '       30000':lambda:set_history_line_limit(30000       ),
                            '       40000':lambda:set_history_line_limit(40000       ),
                            '       50000':lambda:set_history_line_limit(50000       ),
                            '      100000':lambda:set_history_line_limit(100000      ),
                            '     1000000':lambda:set_history_line_limit(1000000     ),
                            '    10000000':lambda:set_history_line_limit(10000000    ),
                            '999999999999':lambda:set_history_line_limit(999999999999),
                       }),

                Option(title='Prompt Height Percent',
                        # is_visible=lambda:getattr(self,'show_all_options',True),

                       description='How many rows of the terminal should the prompt be allowed to take?\n(When using control+e or control+w, this can be useful)\nThis is a hack. Doesnt yet work on Windows (see rp/prompt_toolkit/terminal/vt100_output.py)',
                       get_current_value=lambda:str(100-r_iterm_comm.options['top_space']).rjust(11)+'%',
                       get_values=lambda:{'asdpoa':lambda:None,
                            '          0%':lambda:r_iterm_comm.options.__setitem__('top_space',100-0   ),
                            '          1%':lambda:r_iterm_comm.options.__setitem__('top_space',100-1   ),
                            '          2%':lambda:r_iterm_comm.options.__setitem__('top_space',100-2   ),
                            '          3%':lambda:r_iterm_comm.options.__setitem__('top_space',100-3   ),
                            '          4%':lambda:r_iterm_comm.options.__setitem__('top_space',100-4   ),
                            '          5%':lambda:r_iterm_comm.options.__setitem__('top_space',100-5   ),
                            '         10%':lambda:r_iterm_comm.options.__setitem__('top_space',100-10  ),
                            '         15%':lambda:r_iterm_comm.options.__setitem__('top_space',100-15  ),
                            '         20%':lambda:r_iterm_comm.options.__setitem__('top_space',100-20  ),
                            '         25%':lambda:r_iterm_comm.options.__setitem__('top_space',100-25  ),
                            '         30%':lambda:r_iterm_comm.options.__setitem__('top_space',100-30  ),
                            '         35%':lambda:r_iterm_comm.options.__setitem__('top_space',100-35  ),
                            '         40%':lambda:r_iterm_comm.options.__setitem__('top_space',100-40  ),
                            '         45%':lambda:r_iterm_comm.options.__setitem__('top_space',100-45  ),
                            '         50%':lambda:r_iterm_comm.options.__setitem__('top_space',100-50  ),
                            '         55%':lambda:r_iterm_comm.options.__setitem__('top_space',100-55  ),
                            '         60%':lambda:r_iterm_comm.options.__setitem__('top_space',100-60  ),
                            '         65%':lambda:r_iterm_comm.options.__setitem__('top_space',100-65  ),
                            '         70%':lambda:r_iterm_comm.options.__setitem__('top_space',100-70  ),
                            '         75%':lambda:r_iterm_comm.options.__setitem__('top_space',100-75  ),
                            '         80%':lambda:r_iterm_comm.options.__setitem__('top_space',100-80  ),
                            '         85%':lambda:r_iterm_comm.options.__setitem__('top_space',100-85  ),
                            '         90%':lambda:r_iterm_comm.options.__setitem__('top_space',100-90  ),
                            '         95%':lambda:r_iterm_comm.options.__setitem__('top_space',100-95  ),
                            '        100%':lambda:r_iterm_comm.options.__setitem__('top_space',100-100 ),
                       }),

                # Option(title='Empty Top Space',
                #         # is_visible=lambda:getattr(self,'show_all_options',True),

                #        description='How many lines of free rows should be above the top of the prompt?\n(When using control+e or control+w, this can be useful)',
                #        get_current_value=lambda:str(r_iterm_comm.options['top_space']).rjust(12),
                #        get_values=lambda:{'asdpoa':lambda:None,
                #             '           0':lambda:r_iterm_comm.options.__setitem__('top_space',0   ),
                #             '           1':lambda:r_iterm_comm.options.__setitem__('top_space',1   ),
                #             '           2':lambda:r_iterm_comm.options.__setitem__('top_space',2   ),
                #             '           3':lambda:r_iterm_comm.options.__setitem__('top_space',3   ),
                #             '           4':lambda:r_iterm_comm.options.__setitem__('top_space',4   ),
                #             '           5':lambda:r_iterm_comm.options.__setitem__('top_space',5   ),
                #             '          10':lambda:r_iterm_comm.options.__setitem__('top_space',10  ),
                #             '          15':lambda:r_iterm_comm.options.__setitem__('top_space',15  ),
                #             '          20':lambda:r_iterm_comm.options.__setitem__('top_space',20  ),
                #             '          25':lambda:r_iterm_comm.options.__setitem__('top_space',25  ),
                #             '          30':lambda:r_iterm_comm.options.__setitem__('top_space',30  ),
                #             '          35':lambda:r_iterm_comm.options.__setitem__('top_space',35  ),
                #             '          40':lambda:r_iterm_comm.options.__setitem__('top_space',40  ),
                #             '          45':lambda:r_iterm_comm.options.__setitem__('top_space',45  ),
                #             '          50':lambda:r_iterm_comm.options.__setitem__('top_space',50  ),
                #             '          55':lambda:r_iterm_comm.options.__setitem__('top_space',55  ),
                #             '          60':lambda:r_iterm_comm.options.__setitem__('top_space',60  ),
                #             '          65':lambda:r_iterm_comm.options.__setitem__('top_space',65  ),
                #             '          70':lambda:r_iterm_comm.options.__setitem__('top_space',70  ),
                #             '          75':lambda:r_iterm_comm.options.__setitem__('top_space',75  ),
                #             '          80':lambda:r_iterm_comm.options.__setitem__('top_space',80  ),
                #             '          85':lambda:r_iterm_comm.options.__setitem__('top_space',85  ),
                #             '          90':lambda:r_iterm_comm.options.__setitem__('top_space',90  ),
                #             '          95':lambda:r_iterm_comm.options.__setitem__('top_space',95  ),
                #             '         100':lambda:r_iterm_comm.options.__setitem__('top_space',100 ),
                #             '         125':lambda:r_iterm_comm.options.__setitem__('top_space',125 ),
                #             '         150':lambda:r_iterm_comm.options.__setitem__('top_space',150 ),
                #             '         175':lambda:r_iterm_comm.options.__setitem__('top_space',175 ),
                #             '         200':lambda:r_iterm_comm.options.__setitem__('top_space',200 ),
                #             '         300':lambda:r_iterm_comm.options.__setitem__('top_space',300 ),
                #             '         400':lambda:r_iterm_comm.options.__setitem__('top_space',400 ),
                #             '         500':lambda:r_iterm_comm.options.__setitem__('top_space',500 ),
                #             '         600':lambda:r_iterm_comm.options.__setitem__('top_space',600 ),
                #             '         700':lambda:r_iterm_comm.options.__setitem__('top_space',700 ),
                #             '         800':lambda:r_iterm_comm.options.__setitem__('top_space',800 ),
                #             '         900':lambda:r_iterm_comm.options.__setitem__('top_space',900 ),
                #             '        1000':lambda:r_iterm_comm.options.__setitem__('top_space',1000),
                #        }),

                Option(title='Minimum Prompt Height',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                       description='With respect to the "Prompt Height" option, whats the minimum height of the prompt (in #rows)?',
                       get_current_value=lambda:str(r_iterm_comm.options['min_bot_space']).rjust(12),
                       get_values=lambda:{'asdpoa':lambda:None,
                            '           0':lambda:r_iterm_comm.options.__setitem__('min_bot_space',0   ),
                            '           1':lambda:r_iterm_comm.options.__setitem__('min_bot_space',1   ),
                            '           2':lambda:r_iterm_comm.options.__setitem__('min_bot_space',2   ),
                            '           3':lambda:r_iterm_comm.options.__setitem__('min_bot_space',3   ),
                            '           4':lambda:r_iterm_comm.options.__setitem__('min_bot_space',4   ),
                            '           5':lambda:r_iterm_comm.options.__setitem__('min_bot_space',5   ),
                            '          10':lambda:r_iterm_comm.options.__setitem__('min_bot_space',10  ),
                            '          15':lambda:r_iterm_comm.options.__setitem__('min_bot_space',15  ),
                            '          20':lambda:r_iterm_comm.options.__setitem__('min_bot_space',20  ),
                            '          25':lambda:r_iterm_comm.options.__setitem__('min_bot_space',25  ),
                            '          30':lambda:r_iterm_comm.options.__setitem__('min_bot_space',30  ),
                            '          35':lambda:r_iterm_comm.options.__setitem__('min_bot_space',35  ),
                            '          40':lambda:r_iterm_comm.options.__setitem__('min_bot_space',40  ),
                            '          45':lambda:r_iterm_comm.options.__setitem__('min_bot_space',45  ),
                            '          50':lambda:r_iterm_comm.options.__setitem__('min_bot_space',50  ),
                            '          55':lambda:r_iterm_comm.options.__setitem__('min_bot_space',55  ),
                            '          60':lambda:r_iterm_comm.options.__setitem__('min_bot_space',60  ),
                            '          65':lambda:r_iterm_comm.options.__setitem__('min_bot_space',65  ),
                            '          70':lambda:r_iterm_comm.options.__setitem__('min_bot_space',70  ),
                            '          75':lambda:r_iterm_comm.options.__setitem__('min_bot_space',75  ),
                            '          80':lambda:r_iterm_comm.options.__setitem__('min_bot_space',80  ),
                            '          85':lambda:r_iterm_comm.options.__setitem__('min_bot_space',85  ),
                            '          90':lambda:r_iterm_comm.options.__setitem__('min_bot_space',90  ),
                            '          95':lambda:r_iterm_comm.options.__setitem__('min_bot_space',95  ),
                            '         100':lambda:r_iterm_comm.options.__setitem__('min_bot_space',100 ),
                            '         125':lambda:r_iterm_comm.options.__setitem__('min_bot_space',125 ),
                            '         150':lambda:r_iterm_comm.options.__setitem__('min_bot_space',150 ),
                            '         175':lambda:r_iterm_comm.options.__setitem__('min_bot_space',175 ),
                            '         200':lambda:r_iterm_comm.options.__setitem__('min_bot_space',200 ),
                            '         300':lambda:r_iterm_comm.options.__setitem__('min_bot_space',300 ),
                            '         400':lambda:r_iterm_comm.options.__setitem__('min_bot_space',400 ),
                            '         500':lambda:r_iterm_comm.options.__setitem__('min_bot_space',500 ),
                            '         600':lambda:r_iterm_comm.options.__setitem__('min_bot_space',600 ),
                            '         700':lambda:r_iterm_comm.options.__setitem__('min_bot_space',700 ),
                            '         800':lambda:r_iterm_comm.options.__setitem__('min_bot_space',800 ),
                            '         900':lambda:r_iterm_comm.options.__setitem__('min_bot_space',900 ),
                            '        1000':lambda:r_iterm_comm.options.__setitem__('min_bot_space',1000),
                       }),

                Option(title='Show Battery Life',

                        is_visible=lambda:getattr(self,'show_all_options',True),
                       description='Should we show your laptop\'s battery life?\nIt\'s shown on the bottom right of the terminal.\nWhen it\'s green, that means your laptop is plugged in. When red, it means youre on battery power.',
                       get_current_value=lambda:getattr(self,'show_battery_life','(Broken)'),
                       get_values=lambda:{
                           True:lambda:setattr(self,'show_battery_life',True),# print("Selected Llama"),
                           False:lambda:setattr(self,'show_battery_life',False),# print("Selected Donkey"),
                       }),
                simple_option(title='Show status bar',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Show the status bar at the bottom of the terminal.',
                              field_name='show_status_bar'),
                simple_option(title='Show sidebar help',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='When the sidebar is visible, also show this help text.',
                              field_name='show_sidebar_help'),
                simple_option(title='Highlight parenthesis',
                        is_visible=lambda:getattr(self,'show_all_options',True),
                              description='Highlight matching parenthesis, when the cursor is on or right after one.',
                              field_name='highlight_matching_parenthesis'),

            ]),
            OptionCategory('Ryan Python',[
                # Option(title='Sand Creature',
                #         is_visible=lambda:getattr(self,'show_all_options',True),

                #        description='This is an option selection test that should print stuff',
                #        get_current_value=lambda:getattr(self,'sand_creature','(Broken)'),
                #        get_values=lambda:{
                #            "Option Llama":lambda:setattr(self,'sand_creature',"Option Llama"),# print("Selected Llama"),
                #            "Option Donkey":lambda:setattr(self,'sand_creature',"Option Donkey"),# print("Selected Donkey"),
                #            "Option Camel":lambda:doge(self),# print("Selected Camel"),
                #        }),
                Option(title='Show Last Assignable',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                       description='Should we show the variable in purple box on the bottom of the screen?',
                       get_current_value=lambda:getattr(self,'show_last_assignable','(Broken)'),
                       get_values=lambda:{
                           True:lambda:setattr(self,'show_last_assignable',True),# print("Selected Llama"),
                           False:lambda:setattr(self,'show_last_assignable',False),# print("Selected Donkey"),
                       }),
                Option(title='Space-Functions',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                       description='Turning this on lets pressing the space bar autocomplete a \nfunction for you as well as adding parenthesis around it.\n(Its like pressing tab followed by the spacebar).',
                       get_current_value=lambda:"on" if ric.enable_space_autocompletions else "off",
                       get_values=lambda:{
                           "on":lambda:ric.enable_space_autocompletions.append(None),# print("Selected Llama"),
                           "off":lambda:ric.enable_space_autocompletions.clear(),# print("Selected Donkey"),
                       }),
                Option(title='Completion Type',
                       description='This option determines how autocompletion suggestions are made.\nIf set to \'good\', it will use Jedi to statically analyze your code, providing better insight.\nOtherwise, if set to \'fast\', it will perform mostly simple autocompletions, that will appear much faster.',
                       get_current_value=lambda:"fast" if ric.completion_style==['fast'] else "good",
                       get_values=lambda:{
                           "fast" :lambda:ric.completion_style.__setitem__(0,'fast'),# print("Selected Llama"),
                           "good" :lambda:ric.completion_style.__setitem__(0,'good'),# print("Selected Donkey"),
                       }),
                simple_option(title='Parenthesizer',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                              description='bla',
                              field_name='show_parenthesis_automator'),
                simple_option(title='Realtime Eval',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                              description='bla',
                              field_name='show_realtime_input'),
                simple_option(title='Show VARS',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                              description='bla',
                              field_name='show_vars'),
                Option(title='Debugger UI Height',
                        is_visible=lambda:getattr(self,'show_all_options',True),

                       description='The height of the GUI when running debug()',
                       get_current_value=lambda:str(ric.debug_height),
                       get_values=lambda:{
                            '5':lambda:set_debug_height(5),
                            '10':lambda:set_debug_height(10),
                            '15':lambda:set_debug_height(15),
                            '20':lambda:set_debug_height(20),
                            '25':lambda:set_debug_height(25),
                            '30':lambda:set_debug_height(30),
                            '35':lambda:set_debug_height(35),
                            '40':lambda:set_debug_height(40),
                            '45':lambda:set_debug_height(45),
                            '50':lambda:set_debug_height(50),
                            '55':lambda:set_debug_height(55),
                            '60':lambda:set_debug_height(60),
                            '65':lambda:set_debug_height(65),
                            '70':lambda:set_debug_height(70),
                            '75':lambda:set_debug_height(75),
                            '80':lambda:set_debug_height(80),
                            '85':lambda:set_debug_height(85),
                            '90':lambda:set_debug_height(90),
                            '95':lambda:set_debug_height(95),
                            '100':lambda:set_debug_height(100),
                       }),
            ]),
            OptionCategory('Color Themes',[
                Option(title='Code',
                       description='Color scheme to use for the Python code.',
                       get_current_value=lambda:self._current_code_style_name,
                       get_values=lambda:dict(
                           (name,partial(self.use_code_colorscheme,name)) for name in self.code_styles)
                       ),
                Option(title='User Interface',
                       description='Color scheme to use for the user interface.',
                       get_current_value=lambda:self._current_ui_style_name,
                       get_values=lambda:dict(
                           (name,partial(self.use_ui_colorscheme,name)) for name in self.ui_styles)
                       ),
                simple_option(title='True color (24 bit)',
                        # is_visible=lambda:getattr(self,'show_all_options',True),

                              description='Use 24 bit colors instead of 256 colors\nThis is only supported on some terminal apps\nSome known to support it: Ubuntu\'s default terminal, MacOS iTerm',
                              field_name='true_color'),
            ]),
            OptionCategory('This Menu',[
                                Option(title='Show All Options',
                       description='If turned on, will show more options in this menu.\nIf turned off, will try to keep this menu simple.',
                       get_current_value=lambda:getattr(self,'show_all_options',False),
                       get_values=lambda:{
                           True:lambda:setattr(self,'show_all_options',True),# print("Selected Llama"),
                           False:lambda:setattr(self,'show_all_options',False),# print("Selected Donkey"),
                       }),

            ]),
        ]

    def create_application(self):
        """
        Create an `Application` instance for use in a `CommandLineInterface`.
        """
        buffers={
            'docstring':Buffer(read_only=True),
            'realtime_display':Buffer(read_only=True),
            'vars':Buffer(read_only=True),
            'parenthesizer_buffer':Buffer(read_only=True),
        }
        for key in r_iterm_comm.python_input_buffers:
            buffers[key]=Buffer(read_only=True)
        buffers.update(self._extra_buffers or {})

        return Application(
            layout=create_layout(
                self,
                lexer=self._lexer,
                input_buffer_height=self._input_buffer_height,
                extra_buffer_processors=self._extra_buffer_processors,
                extra_body=self._extra_layout_body,
                extra_toolbars=self._extra_toolbars),
            buffer=self._create_buffer(),
            buffers=buffers,
            key_bindings_registry=self.key_bindings_registry,
            paste_mode=Condition(lambda cli:self.paste_mode),
            mouse_support=Condition(lambda cli:self.enable_mouse_support),
            on_abort=AbortAction.RETRY,
            on_exit=self._on_exit,
            style=DynamicStyle(lambda:self._current_style),
            get_title=lambda:self.terminal_title,
            reverse_vi_search_direction=True,
            on_initialize=self._on_cli_initialize,
            on_start=self._on_start,
            on_input_timeout=self._on_input_timeout)

    def _create_buffer(self):
        """
        Create the `Buffer` for the Python input.
        """
        def is_buffer_multiline():
            return (self.paste_mode or
                    self.accept_input_on_enter is None or
                    document_is_multiline_python(python_buffer.document))

        python_buffer=Buffer(
            is_multiline=Condition(is_buffer_multiline),
            complete_while_typing=Condition(lambda:self.complete_while_typing),
            enable_history_search=Condition(lambda:self.enable_history_search),
            tempfile_suffix='.py',
            history=self.history,
            completer=self._completer,
            validator=ConditionalValidator(
                self._validator,
                Condition(lambda:self.enable_input_validation)),
            auto_suggest=ConditionalAutoSuggest(
                AutoSuggestFromHistory(),
                Condition(lambda cli:self.enable_auto_suggest)),
            accept_action=self._accept_action)

        return python_buffer

    def _on_cli_initialize(self,cli):
        """
        Called when a CommandLineInterface has been created.
        """
        # Synchronize PythonInput state with the CommandLineInterface.
        def synchronize(_=None):
            if self.vi_mode:
                cli.editing_mode=EditingMode.VI
            else:
                cli.editing_mode=EditingMode.EMACS

        cli.input_processor.beforeKeyPress+=synchronize
        cli.input_processor.afterKeyPress+=synchronize
        synchronize()

    def _on_input_timeout(self,cli):
        """
        When there is no input activity,
        in another thread, get the signature of the current code.
        """
        if cli.current_buffer_name != DEFAULT_BUFFER:
            return

        # Never run multiple get-signature threads.
        if self._get_signatures_thread_running:
            return
        self._get_signatures_thread_running=True

        buffer=cli.current_buffer
        document=buffer.document

        def run():
            script=get_jedi_script_from_document(document,self.get_locals(),self.get_globals())
            import rp.r_iterm_comm
            rp.r_iterm_comm.script_debug=script
            # from r import pseudo_terminal
            # pseudo_terminal(locals(),enable_ptpython=False)
            # Show signatures in help text.
            if script:
                try:
                    signatures=script.call_signatures()
                except ValueError:
                    # e.g. in case of an invalid \\x escape.
                    signatures=[]
                except Exception:
                    # Sometimes we still get an exception (TypeError), because
                    # of probably bugs in jedi. We can silence them.
                    # See: https://github.com/davidhalter/jedi/issues/492
                    signatures=[]
                else:
                    # Try to access the params attribute just once. For Jedi
                    # signatures containing the keyword-only argument star,
                    # this will crash when retrieving it the first time with
                    # AttributeError. Every following time it works.
                    # See: https://github.com/jonathanslenders/ptpython/issues/47
                    #      https://github.com/davidhalter/jedi/issues/598
                    try:
                        if signatures:
                            signatures[0].params
                    except AttributeError:
                        pass
            else:
                signatures=[]

            self._get_signatures_thread_running=False

            # Set signatures and redraw if the text didn't change in the
            # meantime. Otherwise request new signatures.
            if buffer.text == document.text:
                self.signatures=signatures

                # Set docstring in docstring buffer.
                if signatures:
                    string=signatures[0].docstring()
                    if not isinstance(string,six.text_type):
                        string=string.decode('utf-8')
                    cli.buffers['docstring'].reset(
                        initial_document=Document(string,cursor_position=0))
                else:
                    cli.buffers['docstring'].reset()

                cli.request_redraw()
            else:
                self._on_input_timeout(cli)
            import rp.r_iterm_comm as r_iterm_comm
            r_iterm_comm.current_input_text=document.text
            if self.show_realtime_input:
                cli.buffers['realtime_display'].reset(initial_document=Document(str(r_iterm_comm.rp_evaluator(document.text))[:100000],cursor_position=0))
                # cli.buffers['realtime_display'].reset(initial_document=Document(str(r_iterm_comm.rp_evaluator(document.text))[::100000],cursor_position=0))
            if self.show_vars:
                cli.buffers['vars'].reset(initial_document=Document(str(r_iterm_comm.rp_VARS_display),cursor_position=0))
            for key in r_iterm_comm.python_input_buffers:
                try:cli.buffers[key].reset(initial_document=Document(str(r_iterm_comm.python_input_buffers[key]),cursor_position=0))
                except:pass
            from rp import parenthesizer_automator
            if self.show_parenthesis_automator:
                xxxxp=str((parenthesizer_automator(document.current_line)))
                r_iterm_comm.parenthesized_line=xxxxp
                cli.buffers['parenthesizer_buffer'].reset(initial_document=Document(xxxxp[:2000],cursor_position=0))
            # cli.buffers['realtime_display'].reset(initial_document=Document(r_iterm_comm.realtime_display_string,cursor_position=0))

        cli.eventloop.run_in_executor(run)

    def on_reset(self,cli):
        self.signatures=[]

    def enter_history(self,cli):
        """
        Display the history.
        """
        cli.vi_state.input_mode=InputMode.NAVIGATION

        def done(result):
            if result is not None:
                cli.buffers[DEFAULT_BUFFER].document=result

            cli.vi_state.input_mode=InputMode.INSERT

        cli.run_sub_application(create_history_application(
            self,cli.buffers[DEFAULT_BUFFER].document),done)

class PythonCommandLineInterface(CommandLineInterface):
    def __init__(self,eventloop=None,python_input=None,input=None,output=None):
        assert python_input is None or isinstance(python_input,PythonInput)

        python_input=python_input or PythonInput()

        # Make sure that the rp.prompt_toolkit 'renderer' knows about the
        # 'true_color' property of PythonInput.
        if output is None:
            output=create_output(true_color=Condition(lambda:python_input.true_color))

        super(PythonCommandLineInterface,self).__init__(
            application=python_input.create_application(),
            eventloop=eventloop,
            input=input,
            output=output)
