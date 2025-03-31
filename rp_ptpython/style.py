from __future__ import unicode_literals
from rp.prompt_toolkit.styles.base import Attrs, ANSI_COLOR_NAMES
import rp

def get_all_ui_styles():
    """
    Return a dict mapping {ui_style_name -> style_dict}.
    """
    styles = {
        # 'inverted_1': inverted_1,#Nothing special; this is teh same as default
        'default'    :default_ui_style,
        'blue'       :blue_ui_style,
        'lightning'  :inverted_2,
        'stars'      :inverted_3,
        'cyan'       :cyan,
        'aqua'       :cyan_2,
        'blew'       :cyan_3,
        'seashell'   :cyan_4,
        'snailshell' :cyan_4__02__02,
        'cobra'      :cyan_4__02__02__12,#cyan 4 with channels 0 and 2 swapped then channels 0 and 2 swapped then 1 and 2 swapped
        'eggshell'   :cyan_4__02,
        'jojo'       :color_1,
        'bizarre'    :color_2,
        'adventure'  :color_3,
        'jade'       :pupper,
        'clara'      :clara,
        'claranew'   :new_clara_style,
        'emma'       :emma,
        'dejavu'     :dejavu,
        'anna'       :newstyle,
        'spook'      :sprice,
        'saturn'     :splicer1,
        'atlantic'   :splicer2,
        'hot'        :breeze,
        'plain'      :plain,
        'silver'     :silver,
        'dark'       :dark,
        # 'trance'     :trance,
        'chirpy'     :chirpy,
        'jenny'      :jenny,
        'random'     :random,
        'darkred'    :darkred,
        'nebula'     :stars_2,
        'vaporwave'  :vaporwave,
        'synthwave'  :synthwave,
        'sunset'     :sunset,
        'sunset_warm':sunset_warm,
        'sunset_cool':sunset_cool,
        'solarized_dark'  :solarized_dark,
        'retro_80s'      :retro,
        'onedark' :onedark,
        'nord_arctic'    :nord,
        'night_owl' :night_owl,
        'monokai':monokai,
        'neon'    :neon,
        'material':material,
        'github':github_dark,
        'galaxy'   :galaxy,
        'cyberpunk' :cyberpunk,
        'candi' :candy,
        'cherry'     :cherry,
        'daffodil':daffodil,
        'mahogany'  :mahogany,
        'lemon'    :lemon,
        'walle'    :walle,
        'tokyo_night':tokyo_night,
        'tomorrow'      :tomorrow,
        'tomorrow_night' :tomorrow_night,
        'tomor_night_blu':tomorrow_night_blue,
        'tom_night_brite':tomorrow_night_bright,
        'tom_night_80s'  :tomorrow_night_eighties,
        'sunset_monokai' :sunset_monokai,
        'clara_monokai'  :clara_monokai,
        'synth_monokai'  :synthwave_monokai,
    }
    
    return styles

from pygments.token import Token, Keyword, Name, Comment, String, Operator, Number
from pygments.styles import get_style_by_name, get_all_styles
from rp.prompt_toolkit.styles import DEFAULT_STYLE_EXTENSIONS, style_from_dict
from rp.prompt_toolkit.utils import is_windows, is_conemu_ansi

# New style definitions
vaporwave = {Token.LineNumber: '#e065b9 bg:#2d1b4e', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff71ce', Token.In.Number: '', Token.Out: '#01cdfe', Token.Out.Number: '#01cdfe', Token.Separator: '#a95aef', Token.Toolbar.Search: '#05dd8a noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#05dd8a noinherit', Token.Toolbar.Arg: '#05dd8a noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#5c2e91 #01b6e4', Token.Toolbar.Signature.CurrentName: 'bg:#724bb7 #fffb96 bold', Token.Toolbar.Signature.Operator: '#01cdfe bold', Token.Docstring: '#e0dc87', Token.Toolbar.Validation: 'bg:#2d1b4e #a95aef', Token.Toolbar.Status: 'bg:#2d1b4e #e065b9', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#2d1b4e #05ffa1', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#2d1b4e #a95aef', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#2d1b4e #e0dc87', Token.Toolbar.Status.Key: 'bg:#5c2e91 #e0dc87', Token.Toolbar.Status.PasteModeOn: 'bg:#724bb7 #ff71ce', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#2d1b4e #a95aef', Token.Toolbar.Status.PythonVersion: 'bg:#2d1b4e #01b6e4 bold', Token.Aborted: '#a95aef', Token.Sidebar: 'bg:#5c2e91 #01b6e4', Token.Sidebar.Title: 'bg:#724bb7 #e0dc87 bold', Token.Sidebar.Label: 'bg:#5c2e91 #e0dc87', Token.Sidebar.Status: 'bg:#5c2e91 #05dd8a', Token.Sidebar.Selected.Label: 'bg:#2d1b4e #ff71ce', Token.Sidebar.Selected.Status: 'bg:#2d1b4e #01cdfe bold', Token.Sidebar.Separator: 'bg:#5c2e91 #05dd8a underline', Token.Sidebar.Key: 'bg:#5c2e91 #e0dc87 bold', Token.Sidebar.Key.Description: 'bg:#5c2e91 #05dd8a', Token.Sidebar.HelpText: 'bg:#724bb7 #01b6e4', Token.History.Line: '', Token.History.Line.Selected: 'bg:#5c2e91 #01b6e4', Token.History.Line.Current: 'bg:#724bb7 #e0dc87', Token.History.Line.Selected.Current: 'bg:#724bb7 #01b6e4', Token.History.ExistingInput: '#e065b9', Token.Window.Border: '#05ffa1', Token.Window.Title: 'bg:#5c2e91 #e0dc87', Token.Window.TIItleV2: 'bg:#724bb7 #01cdfe bold', Token.AcceptMessage: 'bg:#5c2e91 #e0dc87', Token.ExitConfirmation: 'bg:#724bb7 #a95aef', Token.SearchMatch: '#fffb96 bg:#5c2e91', Token.SearchMatch.Current: '#01cdfe bg:#724bb7', Token.SelectedText: '#fffb96 bg:#724bb7', Token.Toolbar.Completions: 'bg:#5c2e91 #01b6e4', Token.Toolbar.Completions.Arrow: 'bg:#5c2e91 #e0dc87 bold', Token.Toolbar.Completions.Completion: 'bg:#5c2e91 #01b6e4', Token.Toolbar.Completions.Completion.Current: 'bg:#724bb7 #fffb96', Token.Menu.Completions.Completion: 'bg:#5c2e91 #01b6e4', Token.Menu.Completions.Completion.Current: 'bg:#724bb7 #fffb96', Token.Menu.Completions.Meta: 'bg:#5c2e91 #e065b9', Token.Menu.Completions.Meta.Current: 'bg:#724bb7 #ff71ce', Token.Menu.Completions.ProgressBar: 'bg:#01cdfe', Token.Menu.Completions.ProgressButton: 'bg:#2d1b4e'}

synthwave = {Token.LineNumber: '#ff00ff bg:#1a0933', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff00ff', Token.In.Number: '', Token.Out: '#00aaff', Token.Out.Number: '#00aaff', Token.Separator: '#ff0066', Token.Toolbar.Search: '#ffdd00 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffdd00 noinherit', Token.Toolbar.Arg: '#ffdd00 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#330066 #00aaff', Token.Toolbar.Signature.CurrentName: 'bg:#550088 #ff00ff bold', Token.Toolbar.Signature.Operator: '#00aaff bold', Token.Docstring: '#ffdd00', Token.Toolbar.Validation: 'bg:#1a0933 #ff0066', Token.Toolbar.Status: 'bg:#1a0933 #ff00ff', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#1a0933 #00ffaa', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#1a0933 #ff0066', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#1a0933 #ffdd00', Token.Toolbar.Status.Key: 'bg:#330066 #ffdd00', Token.Toolbar.Status.PasteModeOn: 'bg:#550088 #ff00ff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#1a0933 #ff00ff', Token.Toolbar.Status.PythonVersion: 'bg:#1a0933 #00aaff bold', Token.Aborted: '#ff0066', Token.Sidebar: 'bg:#330066 #00aaff', Token.Sidebar.Title: 'bg:#550088 #ffdd00 bold', Token.Sidebar.Label: 'bg:#330066 #ffdd00', Token.Sidebar.Status: 'bg:#330066 #00ffaa', Token.Sidebar.Selected.Label: 'bg:#1a0933 #ff00ff', Token.Sidebar.Selected.Status: 'bg:#1a0933 #00aaff bold', Token.Sidebar.Separator: 'bg:#330066 #00ffaa underline', Token.Sidebar.Key: 'bg:#330066 #ffdd00 bold', Token.Sidebar.Key.Description: 'bg:#330066 #00ffaa', Token.Sidebar.HelpText: 'bg:#550088 #00aaff', Token.History.Line: '', Token.History.Line.Selected: 'bg:#330066 #00aaff', Token.History.Line.Current: 'bg:#550088 #ffdd00', Token.History.Line.Selected.Current: 'bg:#550088 #00aaff', Token.History.ExistingInput: '#ff00ff', Token.Window.Border: '#00ffaa', Token.Window.Title: 'bg:#330066 #ffdd00', Token.Window.TIItleV2: 'bg:#550088 #00aaff bold', Token.AcceptMessage: 'bg:#330066 #ffdd00', Token.ExitConfirmation: 'bg:#550088 #ff0066', Token.SearchMatch: '#ffdd00 bg:#330066', Token.SearchMatch.Current: '#00aaff bg:#550088', Token.SelectedText: '#ffdd00 bg:#550088', Token.Toolbar.Completions: 'bg:#330066 #00aaff', Token.Toolbar.Completions.Arrow: 'bg:#330066 #ffdd00 bold', Token.Toolbar.Completions.Completion: 'bg:#330066 #00aaff', Token.Toolbar.Completions.Completion.Current: 'bg:#550088 #ffdd00', Token.Menu.Completions.Completion: 'bg:#330066 #00aaff', Token.Menu.Completions.Completion.Current: 'bg:#550088 #ffdd00', Token.Menu.Completions.Meta: 'bg:#330066 #ff00ff', Token.Menu.Completions.Meta.Current: 'bg:#550088 #ff00ff', Token.Menu.Completions.ProgressBar: 'bg:#00aaff', Token.Menu.Completions.ProgressButton: 'bg:#1a0933'}

sunset = {Token.LineNumber: '#e6a44c bg:#4a2d3d', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff7e45', Token.In.Number: '', Token.Out: '#ffcb6b', Token.Out.Number: '#ffcb6b', Token.Separator: '#ffb8d9', Token.Toolbar.Search: '#ff5e8c noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff5e8c noinherit', Token.Toolbar.Arg: '#ff5e8c noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#ff8cb2 #3c1f38', Token.Toolbar.Signature.CurrentName: 'bg:#ff527e #fff1e6 bold', Token.Toolbar.Signature.Operator: '#3c1f38 bold', Token.Docstring: '#ffa68c', Token.Toolbar.Validation: 'bg:#4c344a #ffbec6', Token.Toolbar.Status: 'bg:#4a2d3d #ffbec6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#4a2d3d #ff9273', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#4a2d3d #ffcf73', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#4a2d3d #ffdfeb', Token.Toolbar.Status.Key: 'bg:#3c1f38 #ffa68c', Token.Toolbar.Status.PasteModeOn: 'bg:#b25e73 #fff1e6', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#7a435a #ffbec6', Token.Toolbar.Status.PythonVersion: 'bg:#4a2d3d #fff1e6 bold', Token.Aborted: '#ffa68c', Token.Sidebar: 'bg:#ffb8d9 #3c1f38', Token.Sidebar.Title: 'bg:#ff96ab #fff1e6 bold', Token.Sidebar.Label: 'bg:#ffb8d9 #4a2d3d', Token.Sidebar.Status: 'bg:#ffdeec #3c1f38', Token.Sidebar.Selected.Label: 'bg:#4a2d3d #ffe8f1', Token.Sidebar.Selected.Status: 'bg:#954a6b #fff1e6 bold', Token.Sidebar.Separator: 'bg:#ffb8d9 #fff1e6 underline', Token.Sidebar.Key: 'bg:#ffb8d9 #3c1f38 bold', Token.Sidebar.Key.Description: 'bg:#ffb8d9 #3c1f38', Token.Sidebar.HelpText: 'bg:#fff1e6 #3c1f38', Token.History.Line: '', Token.History.Line.Selected: 'bg:#ff7e45 #3c1f38', Token.History.Line.Current: 'bg:#fff1e6 #3c1f38', Token.History.Line.Selected.Current: 'bg:#ffa88c #3c1f38', Token.History.ExistingInput: '#ffa68c', Token.Window.Border: '#b85a8c', Token.Window.Title: 'bg:#ffb8d9 #3c1f38', Token.Window.TIItleV2: 'bg:#ff96c6 #3c1f38 bold', Token.AcceptMessage: 'bg:#ffb08c #954a6b', Token.ExitConfirmation: 'bg:#b25e73 #fff1e6', Token.SearchMatch: '#fff1e6 bg:#7a4a65', Token.SearchMatch.Current: '#fff1e6 bg:#ff7e6b', Token.SelectedText: '#fff1e6 bg:#b2768c', Token.Toolbar.Completions: 'bg:#ff8cb2 #3c1f38', Token.Toolbar.Completions.Arrow: 'bg:#ff8cb2 #3c1f38 bold', Token.Toolbar.Completions.Completion: 'bg:#ff8cb2 #3c1f38', Token.Toolbar.Completions.Completion.Current: 'bg:#ff527e #fff1e6', Token.Menu.Completions.Completion: 'bg:#ff8cb2 #3c1f38', Token.Menu.Completions.Completion.Current: 'bg:#ff527e #fff1e6', Token.Menu.Completions.Meta: 'bg:#ff8cc6 #3c1f38', Token.Menu.Completions.Meta.Current: 'bg:#ff52ab #3c1f38', Token.Menu.Completions.ProgressBar: 'bg:#ffbec6', Token.Menu.Completions.ProgressButton: 'bg:#3c1f38'}

solarized_dark_style = {Token: '', Token.Comment: 'italic #657b83', Token.Comment.Hashbang: '#657b83', Token.Comment.Multiline: '#657b83', Token.Comment.Preproc: 'noitalic #657b83', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#dc322f', Token.Escape: '#6c71c4', Token.Generic: '', Token.Generic.Deleted: '#dc322f', Token.Generic.Emph: 'italic', Token.Generic.Error: '#dc322f', Token.Generic.Heading: '#268bd2', Token.Generic.Inserted: '#859900', Token.Generic.Output: '#839496', Token.Generic.Prompt: '#93a1a1', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#268bd2', Token.Generic.Traceback: '#dc322f', Token.Keyword: '#859900', Token.Keyword.Constant: '#2aa198', Token.Keyword.Declaration: '#268bd2', Token.Keyword.Namespace: '#cb4b16', Token.Keyword.Pseudo: '#cb4b16', Token.Keyword.Reserved: '#859900', Token.Keyword.Type: '#b58900', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#d33682', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#2aa198', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#2aa198', Token.Literal.String.Doc: '#2aa198', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#6c71c4', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#cb4b16', Token.Literal.String.Other: '#2aa198', Token.Literal.String.Regex: '#dc322f', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#cb4b16', Token.Name: '#839496', Token.Name.Attribute: '#b58900', Token.Name.Builtin: '#b58900', Token.Name.Builtin.Pseudo: '#cb4b16', Token.Name.Class: '#b58900', Token.Name.Constant: '#b58900', Token.Name.Decorator: '#268bd2', Token.Name.Entity: '#839496', Token.Name.Exception: '#cb4b16', Token.Name.Function: '#268bd2', Token.Name.Label: '#839496', Token.Name.Namespace: '#b58900', Token.Name.Other: '#839496', Token.Name.Property: '#839496', Token.Name.Tag: '#268bd2', Token.Name.Variable: '#cb4b16', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#839496', Token.Operator.Word: '#859900', Token.Punctuation: '#839496', Token.Text: '#839496', Token.Text.Whitespace: ''}

solarized_dark = {Token.LineNumber: 'bg:#002b36 #657b83', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #859900', Token.In.Number: '', Token.Out: '#268bd2', Token.Out.Number: '#268bd2', Token.Separator: '#dc322f', Token.Toolbar.Search: '#dc322f noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#dc322f noinherit', Token.Toolbar.Arg: '#dc322f noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#073642 #839496', Token.Toolbar.Signature.CurrentName: 'bg:#002b36 #dc322f bold', Token.Toolbar.Signature.Operator: '#839496 bold', Token.Docstring: '#2aa198', Token.Toolbar.Validation: 'bg:#002b36 #dc322f', Token.Toolbar.Status: 'bg:#002b36 #839496', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#002b36 #859900', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#002b36 #dc322f', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#002b36 #859900', Token.Toolbar.Status.Key: 'bg:#073642 #839496', Token.Toolbar.Status.PasteModeOn: 'bg:#002b36 #dc322f', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#002b36 #859900', Token.Toolbar.Status.PythonVersion: 'bg:#002b36 #268bd2 bold', Token.Aborted: '#dc322f', Token.Sidebar: 'bg:#073642 #839496', Token.Sidebar.Title: 'bg:#002b36 #2aa198 bold', Token.Sidebar.Label: 'bg:#073642 #859900', Token.Sidebar.Status: 'bg:#073642 #839496', Token.Sidebar.Selected.Label: 'bg:#002b36 #dc322f', Token.Sidebar.Selected.Status: 'bg:#002b36 #839496 bold', Token.Sidebar.Separator: 'bg:#073642 #002b36 underline', Token.Sidebar.Key: 'bg:#073642 #dc322f bold', Token.Sidebar.Key.Description: 'bg:#073642 #839496', Token.Sidebar.HelpText: 'bg:#073642 #839496', Token.History.Line: '', Token.History.Line.Selected: 'bg:#073642 #839496', Token.History.Line.Current: 'bg:#002b36 #859900', Token.History.Line.Selected.Current: 'bg:#002b36 #dc322f', Token.History.ExistingInput: '#268bd2', Token.Window.Border: '#657b83', Token.Window.Title: 'bg:#073642 #839496', Token.Window.TIItleV2: 'bg:#002b36 #839496 bold', Token.AcceptMessage: 'bg:#073642 #859900', Token.ExitConfirmation: 'bg:#002b36 #dc322f', Token.SearchMatch: 'bg:#073642 #839496', Token.SearchMatch.Current: 'bg:#002b36 #dc322f underline', Token.SelectedText: 'bg:#073642 #839496', Token.Toolbar.Completions: 'bg:#073642 #839496', Token.Toolbar.Completions.Arrow: 'bg:#073642 #dc322f bold', Token.Toolbar.Completions.Completion: 'bg:#073642 #839496', Token.Toolbar.Completions.Completion.Current: 'bg:#002b36 #859900 underline', Token.Menu.Completions.Completion: 'bg:#073642 #839496', Token.Menu.Completions.Completion.Current: 'bg:#002b36 #859900', Token.Menu.Completions.Meta: 'bg:#073642 #657b83', Token.Menu.Completions.Meta.Current: 'bg:#073642 #268bd2', Token.Menu.Completions.ProgressBar: 'bg:#dc322f', Token.Menu.Completions.ProgressButton: 'bg:#073642'}

retro = {Token.LineNumber: '#33ff33 bg:#000088', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #33ff33', Token.In.Number: '', Token.Out: '#ffff00', Token.Out.Number: '#ffff00', Token.Separator: '#ff8800', Token.Toolbar.Search: '#ffff00 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffff00 noinherit', Token.Toolbar.Arg: '#ffff00 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#0000dd #33ff33', Token.Toolbar.Signature.CurrentName: 'bg:#0000aa #ffffff bold', Token.Toolbar.Signature.Operator: '#33ff33 bold', Token.Docstring: '#ff8800', Token.Toolbar.Validation: 'bg:#000088 #ff0000', Token.Toolbar.Status: 'bg:#000088 #33ff33', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#000088 #33ff33', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#000088 #ff0000', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#000088 #ffff00', Token.Toolbar.Status.Key: 'bg:#0000dd #ffff00', Token.Toolbar.Status.PasteModeOn: 'bg:#0000aa #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#000088 #ff8800', Token.Toolbar.Status.PythonVersion: 'bg:#000088 #ffffff bold', Token.Aborted: '#ff0000', Token.Sidebar: 'bg:#0000dd #33ff33', Token.Sidebar.Title: 'bg:#0000aa #ffffff bold', Token.Sidebar.Label: 'bg:#0000dd #ffff00', Token.Sidebar.Status: 'bg:#0000dd #ffffff', Token.Sidebar.Selected.Label: 'bg:#000088 #ff8800', Token.Sidebar.Selected.Status: 'bg:#000088 #ffffff bold', Token.Sidebar.Separator: 'bg:#0000dd #ffffff underline', Token.Sidebar.Key: 'bg:#0000dd #ffffff bold', Token.Sidebar.Key.Description: 'bg:#0000dd #ffffff', Token.Sidebar.HelpText: 'bg:#0000aa #33ff33', Token.History.Line: '', Token.History.Line.Selected: 'bg:#0000dd #ffffff', Token.History.Line.Current: 'bg:#0000aa #33ff33', Token.History.Line.Selected.Current: 'bg:#0000aa #ffffff', Token.History.ExistingInput: '#ffff00', Token.Window.Border: '#ff8800', Token.Window.Title: 'bg:#0000dd #ffffff', Token.Window.TIItleV2: 'bg:#0000aa #ffffff bold', Token.AcceptMessage: 'bg:#0000dd #33ff33', Token.ExitConfirmation: 'bg:#0000aa #ff0000', Token.SearchMatch: '#ffff00 bg:#0000dd', Token.SearchMatch.Current: '#ff8800 bg:#0000aa', Token.SelectedText: '#ffffff bg:#0000aa', Token.Toolbar.Completions: 'bg:#0000dd #33ff33', Token.Toolbar.Completions.Arrow: 'bg:#0000dd #ffff00 bold', Token.Toolbar.Completions.Completion: 'bg:#0000dd #33ff33', Token.Toolbar.Completions.Completion.Current: 'bg:#0000aa #ffffff', Token.Menu.Completions.Completion: 'bg:#0000dd #33ff33', Token.Menu.Completions.Completion.Current: 'bg:#0000aa #ffffff', Token.Menu.Completions.Meta: 'bg:#0000dd #ffff00', Token.Menu.Completions.Meta.Current: 'bg:#0000aa #ff8800', Token.Menu.Completions.ProgressBar: 'bg:#33ff33', Token.Menu.Completions.ProgressButton: 'bg:#000088'}

onedark_style = {Token: '', Token.Comment: 'italic #5c6370', Token.Comment.Hashbang: '#5c6370', Token.Comment.Multiline: '#5c6370', Token.Comment.Preproc: 'noitalic #5c6370', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#e06c75', Token.Escape: '#56b6c2', Token.Generic: '', Token.Generic.Deleted: '#e06c75', Token.Generic.Emph: 'italic', Token.Generic.Error: '#e06c75', Token.Generic.Heading: '#e5c07b', Token.Generic.Inserted: '#98c379', Token.Generic.Output: '#abb2bf', Token.Generic.Prompt: '#c678dd', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#e5c07b', Token.Generic.Traceback: '#e06c75', Token.Keyword: '#c678dd', Token.Keyword.Constant: '#d19a66', Token.Keyword.Declaration: '#c678dd', Token.Keyword.Namespace: '#c678dd', Token.Keyword.Pseudo: '#d19a66', Token.Keyword.Reserved: '#c678dd', Token.Keyword.Type: '#e5c07b', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#d19a66', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#98c379', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#98c379', Token.Literal.String.Doc: '#98c379', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#56b6c2', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#56b6c2', Token.Literal.String.Other: '#56b6c2', Token.Literal.String.Regex: '#e5c07b', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#56b6c2', Token.Name: '#abb2bf', Token.Name.Attribute: '#d19a66', Token.Name.Builtin: '#e5c07b', Token.Name.Builtin.Pseudo: '#d19a66', Token.Name.Class: '#e5c07b', Token.Name.Constant: '#e5c07b', Token.Name.Decorator: '#61afef', Token.Name.Entity: '#abb2bf', Token.Name.Exception: '#e06c75', Token.Name.Function: '#61afef', Token.Name.Label: '#abb2bf', Token.Name.Namespace: '#e5c07b', Token.Name.Other: '#abb2bf', Token.Name.Property: '#abb2bf', Token.Name.Tag: '#e06c75', Token.Name.Variable: '#e06c75', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#56b6c2', Token.Operator.Word: '#c678dd', Token.Punctuation: '#abb2bf', Token.Text: '#abb2bf', Token.Text.Whitespace: ''}

onedark = {Token.LineNumber: 'bg:#282c34 #5c6370', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #c678dd', Token.In.Number: '', Token.Out: '#61afef', Token.Out.Number: '#61afef', Token.Separator: '#e06c75', Token.Toolbar.Search: '#e06c75 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#e06c75 noinherit', Token.Toolbar.Arg: '#e06c75 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#2c323c #abb2bf', Token.Toolbar.Signature.CurrentName: 'bg:#282c34 #e06c75 bold', Token.Toolbar.Signature.Operator: '#abb2bf bold', Token.Docstring: '#98c379', Token.Toolbar.Validation: 'bg:#282c34 #e06c75', Token.Toolbar.Status: 'bg:#282c34 #abb2bf', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#282c34 #98c379', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#282c34 #e06c75', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#282c34 #98c379', Token.Toolbar.Status.Key: 'bg:#2c323c #abb2bf', Token.Toolbar.Status.PasteModeOn: 'bg:#282c34 #e06c75', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#282c34 #98c379', Token.Toolbar.Status.PythonVersion: 'bg:#282c34 #61afef bold', Token.Aborted: '#e06c75', Token.Sidebar: 'bg:#2c323c #abb2bf', Token.Sidebar.Title: 'bg:#282c34 #98c379 bold', Token.Sidebar.Label: 'bg:#2c323c #98c379', Token.Sidebar.Status: 'bg:#2c323c #abb2bf', Token.Sidebar.Selected.Label: 'bg:#282c34 #e06c75', Token.Sidebar.Selected.Status: 'bg:#282c34 #abb2bf bold', Token.Sidebar.Separator: 'bg:#2c323c #282c34 underline', Token.Sidebar.Key: 'bg:#2c323c #e06c75 bold', Token.Sidebar.Key.Description: 'bg:#2c323c #abb2bf', Token.Sidebar.HelpText: 'bg:#2c323c #abb2bf', Token.History.Line: '', Token.History.Line.Selected: 'bg:#2c323c #abb2bf', Token.History.Line.Current: 'bg:#282c34 #98c379', Token.History.Line.Selected.Current: 'bg:#282c34 #e06c75', Token.History.ExistingInput: '#61afef', Token.Window.Border: '#5c6370', Token.Window.Title: 'bg:#2c323c #abb2bf', Token.Window.TIItleV2: 'bg:#282c34 #abb2bf bold', Token.AcceptMessage: 'bg:#2c323c #98c379', Token.ExitConfirmation: 'bg:#282c34 #e06c75', Token.SearchMatch: 'bg:#2c323c #abb2bf', Token.SearchMatch.Current: 'bg:#282c34 #e06c75 underline', Token.SelectedText: 'bg:#2c323c #abb2bf', Token.Toolbar.Completions: 'bg:#2c323c #abb2bf', Token.Toolbar.Completions.Arrow: 'bg:#2c323c #e06c75 bold', Token.Toolbar.Completions.Completion: 'bg:#2c323c #abb2bf', Token.Toolbar.Completions.Completion.Current: 'bg:#282c34 #98c379 underline', Token.Menu.Completions.Completion: 'bg:#2c323c #abb2bf', Token.Menu.Completions.Completion.Current: 'bg:#282c34 #98c379', Token.Menu.Completions.Meta: 'bg:#2c323c #5c6370', Token.Menu.Completions.Meta.Current: 'bg:#2c323c #61afef', Token.Menu.Completions.ProgressBar: 'bg:#e06c75', Token.Menu.Completions.ProgressButton: 'bg:#2c323c'}

nord_style = {Token: '', Token.Comment: 'italic #616e88', Token.Comment.Hashbang: '#616e88', Token.Comment.Multiline: '#616e88', Token.Comment.Preproc: 'noitalic #5e81ac', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#bf616a', Token.Escape: '#b48ead', Token.Generic: '', Token.Generic.Deleted: '#bf616a', Token.Generic.Emph: 'italic', Token.Generic.Error: '#bf616a', Token.Generic.Heading: '#ebcb8b', Token.Generic.Inserted: '#a3be8c', Token.Generic.Output: '#d8dee9', Token.Generic.Prompt: '#d8dee9', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#ebcb8b', Token.Generic.Traceback: '#bf616a', Token.Keyword: '#81a1c1', Token.Keyword.Constant: '#81a1c1', Token.Keyword.Declaration: '#b48ead', Token.Keyword.Namespace: '#81a1c1', Token.Keyword.Pseudo: '#81a1c1', Token.Keyword.Reserved: '#81a1c1', Token.Keyword.Type: '#b48ead', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#b48ead', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#a3be8c', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#a3be8c', Token.Literal.String.Doc: '#a3be8c', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#88c0d0', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#ebcb8b', Token.Literal.String.Other: '#8fbcbb', Token.Literal.String.Regex: '#ebcb8b', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#ebcb8b', Token.Name: '#d8dee9', Token.Name.Attribute: '#8fbcbb', Token.Name.Builtin: '#88c0d0', Token.Name.Builtin.Pseudo: '#81a1c1', Token.Name.Class: '#8fbcbb', Token.Name.Constant: '#8fbcbb', Token.Name.Decorator: '#88c0d0', Token.Name.Entity: '#d8dee9', Token.Name.Exception: '#bf616a', Token.Name.Function: '#88c0d0', Token.Name.Label: '#d8dee9', Token.Name.Namespace: '#8fbcbb', Token.Name.Other: '#d8dee9', Token.Name.Property: '#d8dee9', Token.Name.Tag: '#81a1c1', Token.Name.Variable: '#d8dee9', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#81a1c1', Token.Operator.Word: '#81a1c1', Token.Punctuation: '#d8dee9', Token.Text: '#d8dee9', Token.Text.Whitespace: ''}

nord = {Token.LineNumber: 'bg:#2e3440 #616e88', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #81a1c1', Token.In.Number: '', Token.Out: '#88c0d0', Token.Out.Number: '#88c0d0', Token.Separator: '#bf616a', Token.Toolbar.Search: '#bf616a noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#bf616a noinherit', Token.Toolbar.Arg: '#bf616a noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#3b4252 #d8dee9', Token.Toolbar.Signature.CurrentName: 'bg:#2e3440 #bf616a bold', Token.Toolbar.Signature.Operator: '#d8dee9 bold', Token.Docstring: '#a3be8c', Token.Toolbar.Validation: 'bg:#2e3440 #bf616a', Token.Toolbar.Status: 'bg:#2e3440 #d8dee9', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#2e3440 #a3be8c', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#2e3440 #bf616a', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#2e3440 #a3be8c', Token.Toolbar.Status.Key: 'bg:#3b4252 #d8dee9', Token.Toolbar.Status.PasteModeOn: 'bg:#2e3440 #bf616a', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#2e3440 #a3be8c', Token.Toolbar.Status.PythonVersion: 'bg:#2e3440 #88c0d0 bold', Token.Aborted: '#bf616a', Token.Sidebar: 'bg:#3b4252 #d8dee9', Token.Sidebar.Title: 'bg:#2e3440 #ebcb8b bold', Token.Sidebar.Label: 'bg:#3b4252 #a3be8c', Token.Sidebar.Status: 'bg:#3b4252 #d8dee9', Token.Sidebar.Selected.Label: 'bg:#2e3440 #bf616a', Token.Sidebar.Selected.Status: 'bg:#2e3440 #d8dee9 bold', Token.Sidebar.Separator: 'bg:#3b4252 #2e3440 underline', Token.Sidebar.Key: 'bg:#3b4252 #bf616a bold', Token.Sidebar.Key.Description: 'bg:#3b4252 #d8dee9', Token.Sidebar.HelpText: 'bg:#3b4252 #d8dee9', Token.History.Line: '', Token.History.Line.Selected: 'bg:#3b4252 #d8dee9', Token.History.Line.Current: 'bg:#2e3440 #a3be8c', Token.History.Line.Selected.Current: 'bg:#2e3440 #bf616a', Token.History.ExistingInput: '#88c0d0', Token.Window.Border: '#616e88', Token.Window.Title: 'bg:#3b4252 #d8dee9', Token.Window.TIItleV2: 'bg:#2e3440 #d8dee9 bold', Token.AcceptMessage: 'bg:#3b4252 #a3be8c', Token.ExitConfirmation: 'bg:#2e3440 #bf616a', Token.SearchMatch: 'bg:#3b4252 #d8dee9', Token.SearchMatch.Current: 'bg:#2e3440 #bf616a underline', Token.SelectedText: 'bg:#3b4252 #d8dee9', Token.Toolbar.Completions: 'bg:#3b4252 #d8dee9', Token.Toolbar.Completions.Arrow: 'bg:#3b4252 #bf616a bold', Token.Toolbar.Completions.Completion: 'bg:#3b4252 #d8dee9', Token.Toolbar.Completions.Completion.Current: 'bg:#2e3440 #a3be8c underline', Token.Menu.Completions.Completion: 'bg:#3b4252 #d8dee9', Token.Menu.Completions.Completion.Current: 'bg:#2e3440 #a3be8c', Token.Menu.Completions.Meta: 'bg:#3b4252 #616e88', Token.Menu.Completions.Meta.Current: 'bg:#3b4252 #88c0d0', Token.Menu.Completions.ProgressBar: 'bg:#bf616a', Token.Menu.Completions.ProgressButton: 'bg:#3b4252'}

night_owl_style = {Token: '', Token.Comment: 'italic #637777', Token.Comment.Hashbang: '#637777', Token.Comment.Multiline: '#637777', Token.Comment.Preproc: 'noitalic #637777', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#ef5350', Token.Escape: '#82aaff', Token.Generic: '', Token.Generic.Deleted: '#ef5350', Token.Generic.Emph: 'italic', Token.Generic.Error: '#ef5350', Token.Generic.Heading: '#82aaff', Token.Generic.Inserted: '#c3e88d', Token.Generic.Output: '#d6deeb', Token.Generic.Prompt: '#c792ea', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#82aaff', Token.Generic.Traceback: '#ef5350', Token.Keyword: '#c792ea', Token.Keyword.Constant: '#82aaff', Token.Keyword.Declaration: '#c792ea', Token.Keyword.Namespace: '#c792ea', Token.Keyword.Pseudo: '#c792ea', Token.Keyword.Reserved: '#c792ea', Token.Keyword.Type: '#ffcb6b', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#f78c6c', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#c3e88d', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#c3e88d', Token.Literal.String.Doc: '#c3e88d', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#89ddff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#89ddff', Token.Literal.String.Other: '#addb67', Token.Literal.String.Regex: '#f78c6c', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#82aaff', Token.Name: '#d6deeb', Token.Name.Attribute: '#ffcb6b', Token.Name.Builtin: '#82aaff', Token.Name.Builtin.Pseudo: '#82aaff', Token.Name.Class: '#ffcb6b', Token.Name.Constant: '#82aaff', Token.Name.Decorator: '#82aaff', Token.Name.Entity: '#d6deeb', Token.Name.Exception: '#ef5350', Token.Name.Function: '#82aaff', Token.Name.Label: '#d6deeb', Token.Name.Namespace: '#ffcb6b', Token.Name.Other: '#d6deeb', Token.Name.Property: '#d6deeb', Token.Name.Tag: '#7fdbca', Token.Name.Variable: '#addb67', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#89ddff', Token.Operator.Word: '#c792ea', Token.Punctuation: '#d9f5dd', Token.Text: '#d6deeb', Token.Text.Whitespace: ''}

night_owl = {Token.LineNumber: 'bg:#011627 #637777', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #c792ea', Token.In.Number: '', Token.Out: '#82aaff', Token.Out.Number: '#82aaff', Token.Separator: '#ef5350', Token.Toolbar.Search: '#ef5350 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ef5350 noinherit', Token.Toolbar.Arg: '#ef5350 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#0b2942 #d6deeb', Token.Toolbar.Signature.CurrentName: 'bg:#011627 #ef5350 bold', Token.Toolbar.Signature.Operator: '#d6deeb bold', Token.Docstring: '#c3e88d', Token.Toolbar.Validation: 'bg:#011627 #ef5350', Token.Toolbar.Status: 'bg:#011627 #d6deeb', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#011627 #c3e88d', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#011627 #ef5350', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#011627 #c3e88d', Token.Toolbar.Status.Key: 'bg:#0b2942 #d6deeb', Token.Toolbar.Status.PasteModeOn: 'bg:#011627 #ef5350', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#011627 #c3e88d', Token.Toolbar.Status.PythonVersion: 'bg:#011627 #82aaff bold', Token.Aborted: '#ef5350', Token.Sidebar: 'bg:#0b2942 #d6deeb', Token.Sidebar.Title: 'bg:#011627 #ffcb6b bold', Token.Sidebar.Label: 'bg:#0b2942 #c3e88d', Token.Sidebar.Status: 'bg:#0b2942 #d6deeb', Token.Sidebar.Selected.Label: 'bg:#011627 #ef5350', Token.Sidebar.Selected.Status: 'bg:#011627 #d6deeb bold', Token.Sidebar.Separator: 'bg:#0b2942 #011627 underline', Token.Sidebar.Key: 'bg:#0b2942 #ef5350 bold', Token.Sidebar.Key.Description: 'bg:#0b2942 #d6deeb', Token.Sidebar.HelpText: 'bg:#0b2942 #d6deeb', Token.History.Line: '', Token.History.Line.Selected: 'bg:#0b2942 #d6deeb', Token.History.Line.Current: 'bg:#011627 #c3e88d', Token.History.Line.Selected.Current: 'bg:#011627 #ef5350', Token.History.ExistingInput: '#82aaff', Token.Window.Border: '#637777', Token.Window.Title: 'bg:#0b2942 #d6deeb', Token.Window.TIItleV2: 'bg:#011627 #d6deeb bold', Token.AcceptMessage: 'bg:#0b2942 #c3e88d', Token.ExitConfirmation: 'bg:#011627 #ef5350', Token.SearchMatch: 'bg:#0b2942 #d6deeb', Token.SearchMatch.Current: 'bg:#011627 #ef5350 underline', Token.SelectedText: 'bg:#0b2942 #d6deeb', Token.Toolbar.Completions: 'bg:#0b2942 #d6deeb', Token.Toolbar.Completions.Arrow: 'bg:#0b2942 #ef5350 bold', Token.Toolbar.Completions.Completion: 'bg:#0b2942 #d6deeb', Token.Toolbar.Completions.Completion.Current: 'bg:#011627 #c3e88d underline', Token.Menu.Completions.Completion: 'bg:#0b2942 #d6deeb', Token.Menu.Completions.Completion.Current: 'bg:#011627 #c3e88d', Token.Menu.Completions.Meta: 'bg:#0b2942 #637777', Token.Menu.Completions.Meta.Current: 'bg:#0b2942 #82aaff', Token.Menu.Completions.ProgressBar: 'bg:#ef5350', Token.Menu.Completions.ProgressButton: 'bg:#0b2942'}

monokai_style = {Token: '', Token.Comment: 'italic #75715e', Token.Comment.Hashbang: '#75715e', Token.Comment.Multiline: '#75715e', Token.Comment.Preproc: 'noitalic #75715e', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#f92672', Token.Escape: '#ae81ff', Token.Generic: '', Token.Generic.Deleted: '#f92672', Token.Generic.Emph: 'italic', Token.Generic.Error: '#f92672', Token.Generic.Heading: '#a6e22e', Token.Generic.Inserted: '#a6e22e', Token.Generic.Output: '#66d9ef', Token.Generic.Prompt: '#f8f8f2', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#a6e22e', Token.Generic.Traceback: '#f92672', Token.Keyword: '#f92672 bold', Token.Keyword.Constant: '#66d9ef italic', Token.Keyword.Declaration: '#f92672 bold', Token.Keyword.Namespace: '#f92672', Token.Keyword.Pseudo: '#f92672', Token.Keyword.Reserved: '#f92672 bold', Token.Keyword.Type: '#66d9ef italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#ae81ff', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#e6db74', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#e6db74', Token.Literal.String.Doc: '#e6db74', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#ae81ff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: 'underline', Token.Literal.String.Other: '#a6e22e', Token.Literal.String.Regex: '#a6e22e', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#a6e22e', Token.Name: '#f8f8f2', Token.Name.Attribute: '#a6e22e', Token.Name.Builtin: '#66d9ef', Token.Name.Builtin.Pseudo: '#66d9ef italic', Token.Name.Class: '#a6e22e bold', Token.Name.Constant: '#66d9ef', Token.Name.Decorator: '#a6e22e', Token.Name.Entity: '#a6e22e', Token.Name.Exception: '#a6e22e bold', Token.Name.Function: '#a6e22e', Token.Name.Label: '#f8f8f2', Token.Name.Namespace: '#f8f8f2', Token.Name.Other: '#f8f8f2', Token.Name.Property: '#f8f8f2', Token.Name.Tag: '#f92672', Token.Name.Variable: '#fd971f', Token.Name.Variable.Class: '#fd971f italic', Token.Name.Variable.Global: '#fd971f bold', Token.Name.Variable.Instance: '#fd971f', Token.Operator: '#f92672', Token.Operator.Word: '#f92672 bold', Token.Punctuation: '#f8f8f2', Token.Punctuation.Marker: '#777777', Token.Punctuation.Bracket: '#e6e6fa', Token.Punctuation.Parenthesis: '#e6e6fa', Token.Text: '#f8f8f2', Token.Text.Whitespace: ''}

monokai = {Token.LineNumber: 'bg:#272822 #75715e', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #a6e22e', Token.In.Number: '', Token.Out: '#66d9ef', Token.Out.Number: '#66d9ef', Token.Separator: '#f92672', Token.Toolbar.Search: '#f92672 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#f92672 noinherit', Token.Toolbar.Arg: '#f92672 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#3e3d32 #f8f8f2', Token.Toolbar.Signature.CurrentName: 'bg:#272822 #f92672 bold', Token.Toolbar.Signature.Operator: '#f8f8f2 bold', Token.Docstring: '#e6db74', Token.Toolbar.Validation: 'bg:#272822 #f92672', Token.Toolbar.Status: 'bg:#272822 #f8f8f2', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#272822 #a6e22e', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#272822 #f92672', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#272822 #a6e22e', Token.Toolbar.Status.Key: 'bg:#3e3d32 #f8f8f2', Token.Toolbar.Status.PasteModeOn: 'bg:#272822 #f92672', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#272822 #a6e22e', Token.Toolbar.Status.PythonVersion: 'bg:#272822 #66d9ef bold', Token.Aborted: '#f92672', Token.Sidebar: 'bg:#3e3d32 #f8f8f2', Token.Sidebar.Title: 'bg:#272822 #e6db74 bold', Token.Sidebar.Label: 'bg:#3e3d32 #a6e22e', Token.Sidebar.Status: 'bg:#3e3d32 #f8f8f2', Token.Sidebar.Selected.Label: 'bg:#272822 #f92672', Token.Sidebar.Selected.Status: 'bg:#272822 #f8f8f2 bold', Token.Sidebar.Separator: 'bg:#3e3d32 #272822 underline', Token.Sidebar.Key: 'bg:#3e3d32 #f92672 bold', Token.Sidebar.Key.Description: 'bg:#3e3d32 #f8f8f2', Token.Sidebar.HelpText: 'bg:#3e3d32 #f8f8f2', Token.History.Line: '', Token.History.Line.Selected: 'bg:#3e3d32 #f8f8f2', Token.History.Line.Current: 'bg:#272822 #a6e22e', Token.History.Line.Selected.Current: 'bg:#272822 #f92672', Token.History.ExistingInput: '#66d9ef', Token.Window.Border: '#75715e', Token.Window.Title: 'bg:#3e3d32 #f8f8f2', Token.Window.TIItleV2: 'bg:#272822 #f8f8f2 bold', Token.AcceptMessage: 'bg:#3e3d32 #a6e22e', Token.ExitConfirmation: 'bg:#272822 #f92672', Token.SearchMatch: 'bg:#3e3d32 #f8f8f2', Token.SearchMatch.Current: 'bg:#272822 #f92672 underline', Token.SelectedText: 'bg:#3e3d32 #f8f8f2', Token.Toolbar.Completions: 'bg:#3e3d32 #f8f8f2', Token.Toolbar.Completions.Arrow: 'bg:#3e3d32 #f92672 bold', Token.Toolbar.Completions.Completion: 'bg:#3e3d32 #f8f8f2', Token.Toolbar.Completions.Completion.Current: 'bg:#272822 #a6e22e underline', Token.Menu.Completions.Completion: 'bg:#3e3d32 #f8f8f2', Token.Menu.Completions.Completion.Current: 'bg:#272822 #a6e22e', Token.Menu.Completions.Meta: 'bg:#3e3d32 #75715e', Token.Menu.Completions.Meta.Current: 'bg:#3e3d32 #66d9ef', Token.Menu.Completions.ProgressBar: 'bg:#f92672', Token.Menu.Completions.ProgressButton: 'bg:#3e3d32'}

neon = {Token.LineNumber: '#ff0099 bg:#14142b', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff00ff', Token.In.Number: '', Token.Out: '#00ffff', Token.Out.Number: '#00ffff', Token.Separator: '#ff77ff', Token.Toolbar.Search: '#00ff99 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#00ff99 noinherit', Token.Toolbar.Arg: '#00ff99 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#00ffaa #0f0f1a', Token.Toolbar.Signature.CurrentName: 'bg:#00ff77 #eeeeff bold', Token.Toolbar.Signature.Operator: '#0f0f1a bold', Token.Docstring: '#ffff00', Token.Toolbar.Validation: 'bg:#1a1a33 #77ffee', Token.Toolbar.Status: 'bg:#14142b #77ffee', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#14142b #00ff77', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#14142b #ff0055', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#14142b #ddffff', Token.Toolbar.Status.Key: 'bg:#0f0f1a #ffff00', Token.Toolbar.Status.PasteModeOn: 'bg:#5500aa #eeeeff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#33007a #77ffee', Token.Toolbar.Status.PythonVersion: 'bg:#14142b #eeeeff bold', Token.Aborted: '#ffff00', Token.Sidebar: 'bg:#ff77ff #0f0f1a', Token.Sidebar.Title: 'bg:#ff00ff #eeeeff bold', Token.Sidebar.Label: 'bg:#ff77ff #14142b', Token.Sidebar.Status: 'bg:#ffaaff #0f0f1a', Token.Sidebar.Selected.Label: 'bg:#14142b #ffeeff', Token.Sidebar.Selected.Status: 'bg:#7700aa #eeeeff bold', Token.Sidebar.Separator: 'bg:#ff77ff #eeeeff underline', Token.Sidebar.Key: 'bg:#ff77ff #0f0f1a bold', Token.Sidebar.Key.Description: 'bg:#ff77ff #0f0f1a', Token.Sidebar.HelpText: 'bg:#eeeeff #0f0f1a', Token.History.Line: '', Token.History.Line.Selected: 'bg:#ff00ff #0f0f1a', Token.History.Line.Current: 'bg:#eeeeff #0f0f1a', Token.History.Line.Selected.Current: 'bg:#ff77ff #0f0f1a', Token.History.ExistingInput: '#ffff00', Token.Window.Border: '#5500aa', Token.Window.Title: 'bg:#ff77ff #0f0f1a', Token.Window.TIItleV2: 'bg:#ff00aa #0f0f1a bold', Token.AcceptMessage: 'bg:#77ffee #7700aa', Token.ExitConfirmation: 'bg:#5500aa #eeeeff', Token.SearchMatch: '#eeeeff bg:#5500aa', Token.SearchMatch.Current: '#eeeeff bg:#00ff77', Token.SelectedText: '#eeeeff bg:#33007a', Token.Toolbar.Completions: 'bg:#280052 #e6e6fa', Token.Toolbar.Completions.Arrow: 'bg:#280052 #ffffff bold', Token.Toolbar.Completions.Completion: 'bg:#280052 #e6e6fa', Token.Toolbar.Completions.Completion.Current: 'bg:#560099 #ffffff', Token.Menu.Completions.Completion: 'bg:#280052 #e6e6fa', Token.Menu.Completions.Completion.Current: 'bg:#560099 #ffffff', Token.Menu.Completions.Meta: 'bg:#280052 #aaaaaa', Token.Menu.Completions.Meta.Current: 'bg:#560099 #cccccc', Token.Menu.Completions.ProgressBar: 'bg:#77ffee', Token.Menu.Completions.ProgressButton: 'bg:#0f0f1a'}

# Tokyo Night theme - based on the popular VSCode theme
tokyo_night_style = {Token: '', Token.Comment: 'italic #565f89', Token.Comment.Hashbang: '#565f89', Token.Comment.Multiline: '#565f89', Token.Comment.Preproc: 'noitalic #565f89', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#f7768e', Token.Escape: '#bb9af7', Token.Generic: '', Token.Generic.Deleted: '#f7768e', Token.Generic.Emph: 'italic', Token.Generic.Error: '#f7768e', Token.Generic.Heading: '#7aa2f7', Token.Generic.Inserted: '#9ece6a', Token.Generic.Output: '#a9b1d6', Token.Generic.Prompt: '#bb9af7', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#7aa2f7', Token.Generic.Traceback: '#f7768e', Token.Keyword: '#bb9af7 bold', Token.Keyword.Constant: '#ff9e64 italic', Token.Keyword.Declaration: '#bb9af7 bold', Token.Keyword.Namespace: '#bb9af7', Token.Keyword.Pseudo: '#ff9e64', Token.Keyword.Reserved: '#bb9af7 bold', Token.Keyword.Type: '#2ac3de italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#ff9e64', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#9ece6a', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#9ece6a', Token.Literal.String.Doc: '#9ece6a italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#bb9af7', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#2ac3de', Token.Literal.String.Other: '#73daca', Token.Literal.String.Regex: '#b4f9f8', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#73daca', Token.Name: '#c0caf5', Token.Name.Attribute: '#ff9e64', Token.Name.Builtin: '#2ac3de bold', Token.Name.Builtin.Pseudo: '#ff9e64 italic', Token.Name.Class: '#2ac3de bold', Token.Name.Constant: '#2ac3de bold', Token.Name.Decorator: '#7aa2f7', Token.Name.Entity: '#c0caf5', Token.Name.Exception: '#f7768e bold', Token.Name.Function: '#7aa2f7', Token.Name.Label: '#c0caf5', Token.Name.Namespace: '#2ac3de', Token.Name.Other: '#c0caf5', Token.Name.Property: '#c0caf5', Token.Name.Tag: '#f7768e', Token.Name.Variable: '#ff9e64', Token.Name.Variable.Class: '#ff9e64 italic', Token.Name.Variable.Global: '#ff9e64 bold', Token.Name.Variable.Instance: '#ff9e64', Token.Operator: '#f7768e', Token.Operator.Word: '#bb9af7 bold', Token.Punctuation: '#89ddff', Token.Punctuation.Marker: '#565f89', Token.Punctuation.Bracket: '#565f89', Token.Punctuation.Parenthesis: '#565f89', Token.Text: '#c0caf5', Token.Text.Whitespace: ''}

tokyo_night = {Token.LineNumber: 'bg:#1a1b26 #565f89', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #bb9af7', Token.In.Number: '', Token.Out: '#7aa2f7', Token.Out.Number: '#7aa2f7', Token.Separator: '#f7768e', Token.Toolbar.Search: '#f7768e noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#f7768e noinherit', Token.Toolbar.Arg: '#f7768e noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#24283b #c0caf5', Token.Toolbar.Signature.CurrentName: 'bg:#1a1b26 #f7768e bold', Token.Toolbar.Signature.Operator: '#c0caf5 bold', Token.Docstring: '#9ece6a', Token.Toolbar.Validation: 'bg:#1a1b26 #f7768e', Token.Toolbar.Status: 'bg:#1a1b26 #c0caf5', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#1a1b26 #9ece6a', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#1a1b26 #f7768e', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#1a1b26 #9ece6a', Token.Toolbar.Status.Key: 'bg:#24283b #c0caf5', Token.Toolbar.Status.PasteModeOn: 'bg:#1a1b26 #f7768e', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#1a1b26 #9ece6a', Token.Toolbar.Status.PythonVersion: 'bg:#1a1b26 #7aa2f7 bold', Token.Aborted: '#f7768e', Token.Sidebar: 'bg:#24283b #c0caf5', Token.Sidebar.Title: 'bg:#1a1b26 #73daca bold', Token.Sidebar.Label: 'bg:#24283b #9ece6a', Token.Sidebar.Status: 'bg:#24283b #c0caf5', Token.Sidebar.Selected.Label: 'bg:#1a1b26 #f7768e', Token.Sidebar.Selected.Status: 'bg:#1a1b26 #c0caf5 bold', Token.Sidebar.Separator: 'bg:#24283b #1a1b26 underline', Token.Sidebar.Key: 'bg:#24283b #f7768e bold', Token.Sidebar.Key.Description: 'bg:#24283b #c0caf5', Token.Sidebar.HelpText: 'bg:#24283b #c0caf5', Token.History.Line: '', Token.History.Line.Selected: 'bg:#24283b #c0caf5', Token.History.Line.Current: 'bg:#1a1b26 #9ece6a', Token.History.Line.Selected.Current: 'bg:#1a1b26 #f7768e', Token.History.ExistingInput: '#7aa2f7', Token.Window.Border: '#565f89', Token.Window.Title: 'bg:#24283b #c0caf5', Token.Window.TIItleV2: 'bg:#1a1b26 #c0caf5 bold', Token.AcceptMessage: 'bg:#24283b #9ece6a', Token.ExitConfirmation: 'bg:#1a1b26 #f7768e', Token.SearchMatch: 'bg:#24283b #c0caf5', Token.SearchMatch.Current: 'bg:#1a1b26 #f7768e underline', Token.SelectedText: 'bg:#24283b #c0caf5', Token.Toolbar.Completions: 'bg:#24283b #c0caf5', Token.Toolbar.Completions.Arrow: 'bg:#24283b #f7768e bold', Token.Toolbar.Completions.Completion: 'bg:#24283b #c0caf5', Token.Toolbar.Completions.Completion.Current: 'bg:#1a1b26 #9ece6a underline', Token.Menu.Completions.Completion: 'bg:#24283b #c0caf5', Token.Menu.Completions.Completion.Current: 'bg:#1a1b26 #9ece6a', Token.Menu.Completions.Meta: 'bg:#24283b #565f89', Token.Menu.Completions.Meta.Current: 'bg:#24283b #7aa2f7', Token.Menu.Completions.ProgressBar: 'bg:#f7768e', Token.Menu.Completions.ProgressButton: 'bg:#24283b'}

# Sunset variants
sunset_warm = {Token.LineNumber: '#ff9e64 bg:#4a2d3d', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff8c75', Token.In.Number: '', Token.Out: '#ffd76b', Token.Out.Number: '#ffd76b', Token.Separator: '#ffb8d9', Token.Toolbar.Search: '#ff6e8c noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff6e8c noinherit', Token.Toolbar.Arg: '#ff6e8c noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#ff9cb2 #3c1f38', Token.Toolbar.Signature.CurrentName: 'bg:#ff627e #fff1e6 bold', Token.Toolbar.Signature.Operator: '#3c1f38 bold', Token.Docstring: '#ffb68c', Token.Toolbar.Validation: 'bg:#5c344a #ffcec6', Token.Toolbar.Status: 'bg:#4a2d3d #ffcec6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#4a2d3d #ffa273', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#4a2d3d #ffdf73', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#4a2d3d #ffefeb', Token.Toolbar.Status.Key: 'bg:#3c1f38 #ffb68c', Token.Toolbar.Status.PasteModeOn: 'bg:#c25e73 #fff1e6', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#8a435a #ffcec6', Token.Toolbar.Status.PythonVersion: 'bg:#4a2d3d #fff1e6 bold', Token.Aborted: '#ffb68c', Token.Sidebar: 'bg:#ffb8d9 #3c1f38', Token.Sidebar.Title: 'bg:#ffa6ab #fff1e6 bold', Token.Sidebar.Label: 'bg:#ffb8d9 #4a2d3d', Token.Sidebar.Status: 'bg:#ffeeec #3c1f38', Token.Sidebar.Selected.Label: 'bg:#4a2d3d #ffebf1', Token.Sidebar.Selected.Status: 'bg:#a54a6b #fff1e6 bold', Token.Sidebar.Separator: 'bg:#ffb8d9 #fff1e6 underline', Token.Sidebar.Key: 'bg:#ffb8d9 #3c1f38 bold', Token.Sidebar.Key.Description: 'bg:#ffb8d9 #3c1f38', Token.Sidebar.HelpText: 'bg:#fff1e6 #3c1f38', Token.History.Line: '', Token.History.Line.Selected: 'bg:#ff8c75 #3c1f38', Token.History.Line.Current: 'bg:#fff1e6 #3c1f38', Token.History.Line.Selected.Current: 'bg:#ffb88c #3c1f38', Token.History.ExistingInput: '#ffb68c', Token.Window.Border: '#c85a8c', Token.Window.Title: 'bg:#ffb8d9 #3c1f38', Token.Window.TIItleV2: 'bg:#ffa6c6 #3c1f38 bold', Token.AcceptMessage: 'bg:#ffb08c #a54a6b', Token.ExitConfirmation: 'bg:#c25e73 #fff1e6', Token.SearchMatch: '#fff1e6 bg:#8a4a65', Token.SearchMatch.Current: '#fff1e6 bg:#ff8c6b', Token.SelectedText: '#fff1e6 bg:#c2768c', Token.Toolbar.Completions: 'bg:#ff9cb2 #3c1f38', Token.Toolbar.Completions.Arrow: 'bg:#ff9cb2 #3c1f38 bold', Token.Toolbar.Completions.Completion: 'bg:#ff9cb2 #3c1f38', Token.Toolbar.Completions.Completion.Current: 'bg:#ff627e #fff1e6', Token.Menu.Completions.Completion: 'bg:#ff9cb2 #3c1f38', Token.Menu.Completions.Completion.Current: 'bg:#ff627e #fff1e6', Token.Menu.Completions.Meta: 'bg:#ff9cc6 #3c1f38', Token.Menu.Completions.Meta.Current: 'bg:#ff62ab #3c1f38', Token.Menu.Completions.ProgressBar: 'bg:#ffcec6', Token.Menu.Completions.ProgressButton: 'bg:#3c1f38'}

sunset_cool = {Token.LineNumber: '#9e64ff bg:#2d324a', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #8c75ff', Token.In.Number: '', Token.Out: '#8ab6ff', Token.Out.Number: '#8ab6ff', Token.Separator: '#b8d9ff', Token.Toolbar.Search: '#6e8cff noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#6e8cff noinherit', Token.Toolbar.Arg: '#6e8cff noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#9cb2ff #1f2a3c', Token.Toolbar.Signature.CurrentName: 'bg:#627eff #e6f1ff bold', Token.Toolbar.Signature.Operator: '#1f2a3c bold', Token.Docstring: '#b68cff', Token.Toolbar.Validation: 'bg:#34445c #cec6ff', Token.Toolbar.Status: 'bg:#2d324a #cec6ff', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#2d324a #73a2ff', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#2d324a #7373ff', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#2d324a #ebefff', Token.Toolbar.Status.Key: 'bg:#1f2a3c #b68cff', Token.Toolbar.Status.PasteModeOn: 'bg:#5e73c2 #e6f1ff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#435a8a #cec6ff', Token.Toolbar.Status.PythonVersion: 'bg:#2d324a #e6f1ff bold', Token.Aborted: '#b68cff', Token.Sidebar: 'bg:#b8d9ff #1f2a3c', Token.Sidebar.Title: 'bg:#a6abff #e6f1ff bold', Token.Sidebar.Label: 'bg:#b8d9ff #2d324a', Token.Sidebar.Status: 'bg:#eeecff #1f2a3c', Token.Sidebar.Selected.Label: 'bg:#2d324a #ebf1ff', Token.Sidebar.Selected.Status: 'bg:#4a6ba5 #e6f1ff bold', Token.Sidebar.Separator: 'bg:#b8d9ff #e6f1ff underline', Token.Sidebar.Key: 'bg:#b8d9ff #1f2a3c bold', Token.Sidebar.Key.Description: 'bg:#b8d9ff #1f2a3c', Token.Sidebar.HelpText: 'bg:#e6f1ff #1f2a3c', Token.History.Line: '', Token.History.Line.Selected: 'bg:#8c75ff #1f2a3c', Token.History.Line.Current: 'bg:#e6f1ff #1f2a3c', Token.History.Line.Selected.Current: 'bg:#8cb8ff #1f2a3c', Token.History.ExistingInput: '#b68cff', Token.Window.Border: '#5a8cc8', Token.Window.Title: 'bg:#b8d9ff #1f2a3c', Token.Window.TIItleV2: 'bg:#a6c6ff #1f2a3c bold', Token.AcceptMessage: 'bg:#8cb0ff #4a6ba5', Token.ExitConfirmation: 'bg:#5e73c2 #e6f1ff', Token.SearchMatch: '#e6f1ff bg:#4a658a', Token.SearchMatch.Current: '#e6f1ff bg:#6b8cff', Token.SelectedText: '#e6f1ff bg:#768cc2', Token.Toolbar.Completions: 'bg:#9cb2ff #1f2a3c', Token.Toolbar.Completions.Arrow: 'bg:#9cb2ff #1f2a3c bold', Token.Toolbar.Completions.Completion: 'bg:#9cb2ff #1f2a3c', Token.Toolbar.Completions.Completion.Current: 'bg:#627eff #e6f1ff', Token.Menu.Completions.Completion: 'bg:#9cb2ff #1f2a3c', Token.Menu.Completions.Completion.Current: 'bg:#627eff #e6f1ff', Token.Menu.Completions.Meta: 'bg:#9cc6ff #1f2a3c', Token.Menu.Completions.Meta.Current: 'bg:#62abff #1f2a3c', Token.Menu.Completions.ProgressBar: 'bg:#cec6ff', Token.Menu.Completions.ProgressButton: 'bg:#1f2a3c'}

material_style = {Token: '', Token.Comment: 'italic #546e7a', Token.Comment.Hashbang: '#546e7a', Token.Comment.Multiline: '#546e7a', Token.Comment.Preproc: 'noitalic #546e7a', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#ff5370', Token.Escape: '#89ddff', Token.Generic: '', Token.Generic.Deleted: '#ff5370', Token.Generic.Emph: 'italic', Token.Generic.Error: '#ff5370', Token.Generic.Heading: '#82aaff', Token.Generic.Inserted: '#c3e88d', Token.Generic.Output: '#eeffff', Token.Generic.Prompt: '#c792ea', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#82aaff', Token.Generic.Traceback: '#ff5370', Token.Keyword: '#c792ea', Token.Keyword.Constant: '#89ddff', Token.Keyword.Declaration: '#c792ea', Token.Keyword.Namespace: '#c792ea', Token.Keyword.Pseudo: '#c792ea', Token.Keyword.Reserved: '#c792ea', Token.Keyword.Type: '#ffcb6b', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#f78c6c', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#c3e88d', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#c3e88d', Token.Literal.String.Doc: '#c3e88d', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#89ddff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#89ddff', Token.Literal.String.Other: '#c3e88d', Token.Literal.String.Regex: '#f78c6c', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#89ddff', Token.Name: '#eeffff', Token.Name.Attribute: '#ffcb6b', Token.Name.Builtin: '#82aaff', Token.Name.Builtin.Pseudo: '#82aaff', Token.Name.Class: '#ffcb6b', Token.Name.Constant: '#89ddff', Token.Name.Decorator: '#82aaff', Token.Name.Entity: '#f78c6c', Token.Name.Exception: '#f07178', Token.Name.Function: '#82aaff', Token.Name.Label: '#eeffff', Token.Name.Namespace: '#ffcb6b', Token.Name.Other: '#eeffff', Token.Name.Property: '#eeffff', Token.Name.Tag: '#f07178', Token.Name.Variable: '#eeffff', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#89ddff', Token.Operator.Word: '#c792ea', Token.Punctuation: '#89ddff', Token.Text: '#eeffff', Token.Text.Whitespace: ''}

material = {Token.LineNumber: 'bg:#263238 #546e7a', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #c792ea', Token.In.Number: '', Token.Out: '#82aaff', Token.Out.Number: '#82aaff', Token.Separator: '#ff5370', Token.Toolbar.Search: '#ff5370 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff5370 noinherit', Token.Toolbar.Arg: '#ff5370 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#2c393f #eeffff', Token.Toolbar.Signature.CurrentName: 'bg:#263238 #ff5370 bold', Token.Toolbar.Signature.Operator: '#eeffff bold', Token.Docstring: '#c3e88d', Token.Toolbar.Validation: 'bg:#263238 #ff5370', Token.Toolbar.Status: 'bg:#263238 #eeffff', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#263238 #c3e88d', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#263238 #ff5370', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#263238 #c3e88d', Token.Toolbar.Status.Key: 'bg:#2c393f #eeffff', Token.Toolbar.Status.PasteModeOn: 'bg:#263238 #ff5370', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#263238 #c3e88d', Token.Toolbar.Status.PythonVersion: 'bg:#263238 #82aaff bold', Token.Aborted: '#ff5370', Token.Sidebar: 'bg:#2c393f #eeffff', Token.Sidebar.Title: 'bg:#263238 #ffcb6b bold', Token.Sidebar.Label: 'bg:#2c393f #c3e88d', Token.Sidebar.Status: 'bg:#2c393f #eeffff', Token.Sidebar.Selected.Label: 'bg:#263238 #ff5370', Token.Sidebar.Selected.Status: 'bg:#263238 #eeffff bold', Token.Sidebar.Separator: 'bg:#2c393f #263238 underline', Token.Sidebar.Key: 'bg:#2c393f #ff5370 bold', Token.Sidebar.Key.Description: 'bg:#2c393f #eeffff', Token.Sidebar.HelpText: 'bg:#2c393f #eeffff', Token.History.Line: '', Token.History.Line.Selected: 'bg:#2c393f #eeffff', Token.History.Line.Current: 'bg:#263238 #c3e88d', Token.History.Line.Selected.Current: 'bg:#263238 #ff5370', Token.History.ExistingInput: '#82aaff', Token.Window.Border: '#546e7a', Token.Window.Title: 'bg:#2c393f #eeffff', Token.Window.TIItleV2: 'bg:#263238 #eeffff bold', Token.AcceptMessage: 'bg:#2c393f #c3e88d', Token.ExitConfirmation: 'bg:#263238 #ff5370', Token.SearchMatch: 'bg:#2c393f #eeffff', Token.SearchMatch.Current: 'bg:#263238 #ff5370 underline', Token.SelectedText: 'bg:#2c393f #eeffff', Token.Toolbar.Completions: 'bg:#2c393f #eeffff', Token.Toolbar.Completions.Arrow: 'bg:#2c393f #ff5370 bold', Token.Toolbar.Completions.Completion: 'bg:#2c393f #eeffff', Token.Toolbar.Completions.Completion.Current: 'bg:#263238 #c3e88d underline', Token.Menu.Completions.Completion: 'bg:#2c393f #eeffff', Token.Menu.Completions.Completion.Current: 'bg:#263238 #c3e88d', Token.Menu.Completions.Meta: 'bg:#2c393f #546e7a', Token.Menu.Completions.Meta.Current: 'bg:#2c393f #82aaff', Token.Menu.Completions.ProgressBar: 'bg:#ff5370', Token.Menu.Completions.ProgressButton: 'bg:#2c393f'}

github_dark_style = {Token: '', Token.Comment: 'italic #8b949e', Token.Comment.Hashbang: '#8b949e', Token.Comment.Multiline: '#8b949e', Token.Comment.Preproc: 'noitalic #8b949e', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#f85149', Token.Escape: '#79c0ff', Token.Generic: '', Token.Generic.Deleted: '#ffa198', Token.Generic.Emph: 'italic', Token.Generic.Error: '#f85149', Token.Generic.Heading: '#e6edf3', Token.Generic.Inserted: '#56d364', Token.Generic.Output: '#c9d1d9', Token.Generic.Prompt: '#c9d1d9', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#e6edf3', Token.Generic.Traceback: '#f85149', Token.Keyword: '#ff7b72', Token.Keyword.Constant: '#79c0ff', Token.Keyword.Declaration: '#ff7b72', Token.Keyword.Namespace: '#ff7b72', Token.Keyword.Pseudo: '#ff7b72', Token.Keyword.Reserved: '#ff7b72', Token.Keyword.Type: '#ff7b72', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#79c0ff', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#a5d6ff', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#a5d6ff', Token.Literal.String.Doc: '#a5d6ff', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#79c0ff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#d2a8ff', Token.Literal.String.Other: '#a5d6ff', Token.Literal.String.Regex: '#a5d6ff', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#79c0ff', Token.Name: '#c9d1d9', Token.Name.Attribute: '#d2a8ff', Token.Name.Builtin: '#79c0ff', Token.Name.Builtin.Pseudo: '#79c0ff', Token.Name.Class: '#ff7b72', Token.Name.Constant: '#79c0ff', Token.Name.Decorator: '#d2a8ff', Token.Name.Entity: '#c9d1d9', Token.Name.Exception: '#ff7b72', Token.Name.Function: '#d2a8ff', Token.Name.Label: '#c9d1d9', Token.Name.Namespace: '#ff7b72', Token.Name.Other: '#c9d1d9', Token.Name.Property: '#c9d1d9', Token.Name.Tag: '#7ee787', Token.Name.Variable: '#ffa657', Token.Name.Variable.Class: '', Token.Name.Variable.Global: '', Token.Name.Variable.Instance: '', Token.Operator: '#c9d1d9', Token.Operator.Word: '#ff7b72', Token.Punctuation: '#c9d1d9', Token.Text: '#c9d1d9', Token.Text.Whitespace: ''}

github_dark = {Token.LineNumber: 'bg:#0d1117 #8b949e', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff7b72', Token.In.Number: '', Token.Out: '#79c0ff', Token.Out.Number: '#79c0ff', Token.Separator: '#f85149', Token.Toolbar.Search: '#f85149 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#f85149 noinherit', Token.Toolbar.Arg: '#f85149 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#161b22 #c9d1d9', Token.Toolbar.Signature.CurrentName: 'bg:#0d1117 #f85149 bold', Token.Toolbar.Signature.Operator: '#c9d1d9 bold', Token.Docstring: '#a5d6ff', Token.Toolbar.Validation: 'bg:#0d1117 #f85149', Token.Toolbar.Status: 'bg:#0d1117 #c9d1d9', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#0d1117 #56d364', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#0d1117 #f85149', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#0d1117 #56d364', Token.Toolbar.Status.Key: 'bg:#161b22 #c9d1d9', Token.Toolbar.Status.PasteModeOn: 'bg:#0d1117 #f85149', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#0d1117 #56d364', Token.Toolbar.Status.PythonVersion: 'bg:#0d1117 #79c0ff bold', Token.Aborted: '#f85149', Token.Sidebar: 'bg:#161b22 #c9d1d9', Token.Sidebar.Title: 'bg:#0d1117 #d2a8ff bold', Token.Sidebar.Label: 'bg:#161b22 #56d364', Token.Sidebar.Status: 'bg:#161b22 #c9d1d9', Token.Sidebar.Selected.Label: 'bg:#0d1117 #f85149', Token.Sidebar.Selected.Status: 'bg:#0d1117 #c9d1d9 bold', Token.Sidebar.Separator: 'bg:#161b22 #0d1117 underline', Token.Sidebar.Key: 'bg:#161b22 #f85149 bold', Token.Sidebar.Key.Description: 'bg:#161b22 #c9d1d9', Token.Sidebar.HelpText: 'bg:#161b22 #c9d1d9', Token.History.Line: '', Token.History.Line.Selected: 'bg:#161b22 #c9d1d9', Token.History.Line.Current: 'bg:#0d1117 #56d364', Token.History.Line.Selected.Current: 'bg:#0d1117 #f85149', Token.History.ExistingInput: '#79c0ff', Token.Window.Border: '#8b949e', Token.Window.Title: 'bg:#161b22 #c9d1d9', Token.Window.TIItleV2: 'bg:#0d1117 #c9d1d9 bold', Token.AcceptMessage: 'bg:#161b22 #56d364', Token.ExitConfirmation: 'bg:#0d1117 #f85149', Token.SearchMatch: 'bg:#161b22 #c9d1d9', Token.SearchMatch.Current: 'bg:#0d1117 #f85149 underline', Token.SelectedText: 'bg:#161b22 #c9d1d9', Token.Toolbar.Completions: 'bg:#161b22 #c9d1d9', Token.Toolbar.Completions.Arrow: 'bg:#161b22 #f85149 bold', Token.Toolbar.Completions.Completion: 'bg:#161b22 #c9d1d9', Token.Toolbar.Completions.Completion.Current: 'bg:#0d1117 #56d364 underline', Token.Menu.Completions.Completion: 'bg:#161b22 #c9d1d9', Token.Menu.Completions.Completion.Current: 'bg:#0d1117 #56d364', Token.Menu.Completions.Meta: 'bg:#161b22 #8b949e', Token.Menu.Completions.Meta.Current: 'bg:#161b22 #79c0ff', Token.Menu.Completions.ProgressBar: 'bg:#f85149', Token.Menu.Completions.ProgressButton: 'bg:#161b22'}

galaxy = {Token.LineNumber: '#8a6bff bg:#1a1c30', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #c792ea', Token.In.Number: '', Token.Out: '#82aaff', Token.Out.Number: '#82aaff', Token.Separator: '#a4a7ff', Token.Toolbar.Search: '#57c7ff noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#57c7ff noinherit', Token.Toolbar.Arg: '#57c7ff noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#79e4e0 #0d111c', Token.Toolbar.Signature.CurrentName: 'bg:#64ffda #eeffff bold', Token.Toolbar.Signature.Operator: '#0d111c bold', Token.Docstring: '#89ddff', Token.Toolbar.Validation: 'bg:#1d2039 #a1eafb', Token.Toolbar.Status: 'bg:#1a1c30 #a1eafb', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#1a1c30 #c3e88d', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#1a1c30 #f07178', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#1a1c30 #dfefff', Token.Toolbar.Status.Key: 'bg:#0d111c #89ddff', Token.Toolbar.Status.PasteModeOn: 'bg:#4a5484 #eeffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#313452 #a1eafb', Token.Toolbar.Status.PythonVersion: 'bg:#1a1c30 #eeffff bold', Token.Aborted: '#89ddff', Token.Sidebar: 'bg:#a4a7ff #0d111c', Token.Sidebar.Title: 'bg:#c792ea #eeffff bold', Token.Sidebar.Label: 'bg:#a4a7ff #1a1c30', Token.Sidebar.Status: 'bg:#d0d2ff #0d111c', Token.Sidebar.Selected.Label: 'bg:#1a1c30 #e8e9ff', Token.Sidebar.Selected.Status: 'bg:#3a4084 #eeffff bold', Token.Sidebar.Separator: 'bg:#a4a7ff #eeffff underline', Token.Sidebar.Key: 'bg:#a4a7ff #0d111c bold', Token.Sidebar.Key.Description: 'bg:#a4a7ff #0d111c', Token.Sidebar.HelpText: 'bg:#eeffff #0d111c', Token.History.Line: '', Token.History.Line.Selected: 'bg:#c792ea #0d111c', Token.History.Line.Current: 'bg:#eeffff #0d111c', Token.History.Line.Selected.Current: 'bg:#89e0ff #0d111c', Token.History.ExistingInput: '#89ddff', Token.Window.Border: '#4a5484', Token.Window.Title: 'bg:#a4a7ff #0d111c', Token.Window.TIItleV2: 'bg:#7986cb #0d111c bold', Token.AcceptMessage: 'bg:#89e0ff #3a4084', Token.ExitConfirmation: 'bg:#4a5484 #eeffff', Token.SearchMatch: '#eeffff bg:#3a4084', Token.SearchMatch.Current: '#eeffff bg:#64ffda', Token.SelectedText: '#eeffff bg:#4a5484', Token.Toolbar.Completions: 'bg:#79e4e0 #0d111c', Token.Toolbar.Completions.Arrow: 'bg:#79e4e0 #0d111c bold', Token.Toolbar.Completions.Completion: 'bg:#79e4e0 #0d111c', Token.Toolbar.Completions.Completion.Current: 'bg:#64ffda #eeffff', Token.Menu.Completions.Completion: 'bg:#79e4e0 #0d111c', Token.Menu.Completions.Completion.Current: 'bg:#64ffda #eeffff', Token.Menu.Completions.Meta: 'bg:#79e4ff #0d111c', Token.Menu.Completions.Meta.Current: 'bg:#64d0ff #0d111c', Token.Menu.Completions.ProgressBar: 'bg:#a1eafb', Token.Menu.Completions.ProgressButton: 'bg:#0d111c'}

cyberpunk = {Token.LineNumber: '#00d9e0 bg:#120458', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff00f6', Token.In.Number: '', Token.Out: '#00d785', Token.Out.Number: '#00d785', Token.Separator: '#e6004c', Token.Toolbar.Search: '#e6d908 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#e6d908 noinherit', Token.Toolbar.Arg: '#e6d908 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#5a00b0 #00d9e0', Token.Toolbar.Signature.CurrentName: 'bg:#9900cc #fcee09 bold', Token.Toolbar.Signature.Operator: '#00d9e0 bold', Token.Docstring: '#e6d908', Token.Toolbar.Validation: 'bg:#120458 #e6004c', Token.Toolbar.Status: 'bg:#120458 #00d9e0', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#120458 #00ff9f', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#120458 #e6004c', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#120458 #e6d908', Token.Toolbar.Status.Key: 'bg:#5a00b0 #e6d908', Token.Toolbar.Status.PasteModeOn: 'bg:#9900cc #00f6ff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#120458 #d900d8', Token.Toolbar.Status.PythonVersion: 'bg:#120458 #00d9e0 bold', Token.Aborted: '#e6004c', Token.Sidebar: 'bg:#5a00b0 #00d9e0', Token.Sidebar.Title: 'bg:#9900cc #fcee09 bold', Token.Sidebar.Label: 'bg:#5a00b0 #e6d908', Token.Sidebar.Status: 'bg:#5a00b0 #00d785', Token.Sidebar.Selected.Label: 'bg:#120458 #ff00f6', Token.Sidebar.Selected.Status: 'bg:#120458 #00d9e0 bold', Token.Sidebar.Separator: 'bg:#5a00b0 #00d785 underline', Token.Sidebar.Key: 'bg:#5a00b0 #e6d908 bold', Token.Sidebar.Key.Description: 'bg:#5a00b0 #00d785', Token.Sidebar.HelpText: 'bg:#9900cc #00d9e0', Token.History.Line: '', Token.History.Line.Selected: 'bg:#5a00b0 #00d9e0', Token.History.Line.Current: 'bg:#9900cc #e6d908', Token.History.Line.Selected.Current: 'bg:#9900cc #00d9e0', Token.History.ExistingInput: '#d900d8', Token.Window.Border: '#00d785', Token.Window.Title: 'bg:#5a00b0 #e6d908', Token.Window.TIItleV2: 'bg:#9900cc #00f6ff bold', Token.AcceptMessage: 'bg:#5a00b0 #e6d908', Token.ExitConfirmation: 'bg:#9900cc #e6004c', Token.SearchMatch: '#fcee09 bg:#5a00b0', Token.SearchMatch.Current: '#00f6ff bg:#9900cc', Token.SelectedText: '#e6d908 bg:#9900cc', Token.Toolbar.Completions: 'bg:#5a00b0 #00d9e0', Token.Toolbar.Completions.Arrow: 'bg:#5a00b0 #e6d908 bold', Token.Toolbar.Completions.Completion: 'bg:#5a00b0 #00d9e0', Token.Toolbar.Completions.Completion.Current: 'bg:#9900cc #fcee09', Token.Menu.Completions.Completion: 'bg:#5a00b0 #00d9e0', Token.Menu.Completions.Completion.Current: 'bg:#9900cc #e6d908', Token.Menu.Completions.Meta: 'bg:#5a00b0 #d900d8', Token.Menu.Completions.Meta.Current: 'bg:#9900cc #ff00f6', Token.Menu.Completions.ProgressBar: 'bg:#00f6ff', Token.Menu.Completions.ProgressButton: 'bg:#120458'}

daffodil = {Token.LineNumber: '#ffeaae bg:#3c4a1e', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ffcc00', Token.In.Number: '', Token.Out: '#ddffaa', Token.Out.Number: '#ddffaa', Token.Separator: '#ffe680', Token.Toolbar.Search: '#f8ffdc noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#f8ffdc noinherit', Token.Toolbar.Arg: '#f8ffdc noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#6b7a3d #ffecbc', Token.Toolbar.Signature.CurrentName: 'bg:#8a9e4e #ffffff bold', Token.Toolbar.Signature.Operator: '#ffecbc bold', Token.Docstring: '#ffd34d', Token.Toolbar.Validation: 'bg:#3c4a1e #fff0c6', Token.Toolbar.Status: 'bg:#3c4a1e #fff0c6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#3c4a1e #bbdd88', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#3c4a1e #ffdb72', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#3c4a1e #ffeb99', Token.Toolbar.Status.Key: 'bg:#6b7a3d #ffeb99', Token.Toolbar.Status.PasteModeOn: 'bg:#8a9e4e #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#3c4a1e #ffcc00', Token.Toolbar.Status.PythonVersion: 'bg:#3c4a1e #ffffff bold', Token.Aborted: '#ffcc00', Token.Sidebar: 'bg:#6b7a3d #ffecbc', Token.Sidebar.Title: 'bg:#8a9e4e #ffffff bold', Token.Sidebar.Label: 'bg:#6b7a3d #ffeb99', Token.Sidebar.Status: 'bg:#6b7a3d #ffffff', Token.Sidebar.Selected.Label: 'bg:#3c4a1e #ffcc00', Token.Sidebar.Selected.Status: 'bg:#3c4a1e #ffffff bold', Token.Sidebar.Separator: 'bg:#6b7a3d #ffffff underline', Token.Sidebar.Key: 'bg:#6b7a3d #ffffff bold', Token.Sidebar.Key.Description: 'bg:#6b7a3d #ffffff', Token.Sidebar.HelpText: 'bg:#8a9e4e #ffecbc', Token.History.Line: '', Token.History.Line.Selected: 'bg:#6b7a3d #ffffff', Token.History.Line.Current: 'bg:#8a9e4e #ffecbc', Token.History.Line.Selected.Current: 'bg:#8a9e4e #ffffff', Token.History.ExistingInput: '#ffeb99', Token.Window.Border: '#ffcc00', Token.Window.Title: 'bg:#6b7a3d #ffffff', Token.Window.TIItleV2: 'bg:#8a9e4e #ffffff bold', Token.AcceptMessage: 'bg:#6b7a3d #ffecbc', Token.ExitConfirmation: 'bg:#8a9e4e #ffcc00', Token.SearchMatch: '#ffeb99 bg:#6b7a3d', Token.SearchMatch.Current: '#ffcc00 bg:#8a9e4e', Token.SelectedText: '#ffffff bg:#8a9e4e', Token.Toolbar.Completions: 'bg:#6b7a3d #ffecbc', Token.Toolbar.Completions.Arrow: 'bg:#6b7a3d #ffeb99 bold', Token.Toolbar.Completions.Completion: 'bg:#6b7a3d #ffecbc', Token.Toolbar.Completions.Completion.Current: 'bg:#8a9e4e #ffffff', Token.Menu.Completions.Completion: 'bg:#6b7a3d #ffecbc', Token.Menu.Completions.Completion.Current: 'bg:#8a9e4e #ffffff', Token.Menu.Completions.Meta: 'bg:#6b7a3d #ffeb99', Token.Menu.Completions.Meta.Current: 'bg:#8a9e4e #ffcc00', Token.Menu.Completions.ProgressBar: 'bg:#ddffaa', Token.Menu.Completions.ProgressButton: 'bg:#3c4a1e'}

mahogany = {Token.LineNumber: '#e5c09f bg:#3b1f1a', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff7f50', Token.In.Number: '', Token.Out: '#d69c74', Token.Out.Number: '#d69c74', Token.Separator: '#b04b2d', Token.Toolbar.Search: '#ffdab9 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffdab9 noinherit', Token.Toolbar.Arg: '#ffdab9 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#5e2c20 #f5deb3', Token.Toolbar.Signature.CurrentName: 'bg:#7d3a2d #ffffff bold', Token.Toolbar.Signature.Operator: '#f5deb3 bold', Token.Docstring: '#deb887', Token.Toolbar.Validation: 'bg:#3b1f1a #ffccb3', Token.Toolbar.Status: 'bg:#3b1f1a #ffccb3', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#3b1f1a #cd853f', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#3b1f1a #c45e34', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#3b1f1a #e5c09f', Token.Toolbar.Status.Key: 'bg:#5e2c20 #e5c09f', Token.Toolbar.Status.PasteModeOn: 'bg:#7d3a2d #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#3b1f1a #ff7f50', Token.Toolbar.Status.PythonVersion: 'bg:#3b1f1a #ffffff bold', Token.Aborted: '#ff7f50', Token.Sidebar: 'bg:#5e2c20 #f5deb3', Token.Sidebar.Title: 'bg:#7d3a2d #ffffff bold', Token.Sidebar.Label: 'bg:#5e2c20 #e5c09f', Token.Sidebar.Status: 'bg:#5e2c20 #ffffff', Token.Sidebar.Selected.Label: 'bg:#3b1f1a #ff7f50', Token.Sidebar.Selected.Status: 'bg:#3b1f1a #ffffff bold', Token.Sidebar.Separator: 'bg:#5e2c20 #ffffff underline', Token.Sidebar.Key: 'bg:#5e2c20 #ffffff bold', Token.Sidebar.Key.Description: 'bg:#5e2c20 #ffffff', Token.Sidebar.HelpText: 'bg:#7d3a2d #f5deb3', Token.History.Line: '', Token.History.Line.Selected: 'bg:#5e2c20 #ffffff', Token.History.Line.Current: 'bg:#7d3a2d #f5deb3', Token.History.Line.Selected.Current: 'bg:#7d3a2d #ffffff', Token.History.ExistingInput: '#e5c09f', Token.Window.Border: '#b04b2d', Token.Window.Title: 'bg:#5e2c20 #ffffff', Token.Window.TIItleV2: 'bg:#7d3a2d #ffffff bold', Token.AcceptMessage: 'bg:#5e2c20 #f5deb3', Token.ExitConfirmation: 'bg:#7d3a2d #ff7f50', Token.SearchMatch: '#e5c09f bg:#5e2c20', Token.SearchMatch.Current: '#ff7f50 bg:#7d3a2d', Token.SelectedText: '#ffffff bg:#7d3a2d', Token.Toolbar.Completions: 'bg:#5e2c20 #f5deb3', Token.Toolbar.Completions.Arrow: 'bg:#5e2c20 #e5c09f bold', Token.Toolbar.Completions.Completion: 'bg:#5e2c20 #f5deb3', Token.Toolbar.Completions.Completion.Current: 'bg:#7d3a2d #ffffff', Token.Menu.Completions.Completion: 'bg:#5e2c20 #f5deb3', Token.Menu.Completions.Completion.Current: 'bg:#7d3a2d #ffffff', Token.Menu.Completions.Meta: 'bg:#5e2c20 #e5c09f', Token.Menu.Completions.Meta.Current: 'bg:#7d3a2d #ff7f50', Token.Menu.Completions.ProgressBar: 'bg:#d69c74', Token.Menu.Completions.ProgressButton: 'bg:#3b1f1a'}

lemon = {Token.LineNumber: '#fffa8c bg:#666500', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #fff000', Token.In.Number: '', Token.Out: '#c1ff72', Token.Out.Number: '#c1ff72', Token.Separator: '#ffdf0f', Token.Toolbar.Search: '#ffffd0 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffffd0 noinherit', Token.Toolbar.Arg: '#ffffd0 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#8c8800 #ffffc0', Token.Toolbar.Signature.CurrentName: 'bg:#b3ae00 #ffffff bold', Token.Toolbar.Signature.Operator: '#ffffc0 bold', Token.Docstring: '#ffd700', Token.Toolbar.Validation: 'bg:#666500 #ffffa0', Token.Toolbar.Status: 'bg:#666500 #ffffa0', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#666500 #d4ff7f', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#666500 #ffd700', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#666500 #fffa8c', Token.Toolbar.Status.Key: 'bg:#8c8800 #fffa8c', Token.Toolbar.Status.PasteModeOn: 'bg:#b3ae00 #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#666500 #fff000', Token.Toolbar.Status.PythonVersion: 'bg:#666500 #ffffff bold', Token.Aborted: '#fff000', Token.Sidebar: 'bg:#8c8800 #ffffc0', Token.Sidebar.Title: 'bg:#b3ae00 #ffffff bold', Token.Sidebar.Label: 'bg:#8c8800 #fffa8c', Token.Sidebar.Status: 'bg:#8c8800 #ffffff', Token.Sidebar.Selected.Label: 'bg:#666500 #fff000', Token.Sidebar.Selected.Status: 'bg:#666500 #ffffff bold', Token.Sidebar.Separator: 'bg:#8c8800 #ffffff underline', Token.Sidebar.Key: 'bg:#8c8800 #ffffff bold', Token.Sidebar.Key.Description: 'bg:#8c8800 #ffffff', Token.Sidebar.HelpText: 'bg:#b3ae00 #ffffc0', Token.History.Line: '', Token.History.Line.Selected: 'bg:#8c8800 #ffffff', Token.History.Line.Current: 'bg:#b3ae00 #ffffc0', Token.History.Line.Selected.Current: 'bg:#b3ae00 #ffffff', Token.History.ExistingInput: '#fffa8c', Token.Window.Border: '#ffdf0f', Token.Window.Title: 'bg:#8c8800 #ffffff', Token.Window.TIItleV2: 'bg:#b3ae00 #ffffff bold', Token.AcceptMessage: 'bg:#8c8800 #ffffc0', Token.ExitConfirmation: 'bg:#b3ae00 #fff000', Token.SearchMatch: '#fffa8c bg:#8c8800', Token.SearchMatch.Current: '#fff000 bg:#b3ae00', Token.SelectedText: '#ffffff bg:#b3ae00', Token.Toolbar.Completions: 'bg:#8c8800 #ffffc0', Token.Toolbar.Completions.Arrow: 'bg:#8c8800 #fffa8c bold', Token.Toolbar.Completions.Completion: 'bg:#8c8800 #ffffc0', Token.Toolbar.Completions.Completion.Current: 'bg:#b3ae00 #ffffff', Token.Menu.Completions.Completion: 'bg:#8c8800 #ffffc0', Token.Menu.Completions.Completion.Current: 'bg:#b3ae00 #ffffff', Token.Menu.Completions.Meta: 'bg:#8c8800 #fffa8c', Token.Menu.Completions.Meta.Current: 'bg:#b3ae00 #fff000', Token.Menu.Completions.ProgressBar: 'bg:#c1ff72', Token.Menu.Completions.ProgressButton: 'bg:#666500'}

walle = {Token.LineNumber: '#f9d48c bg:#594b36', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff7518', Token.In.Number: '', Token.Out: '#77dd77', Token.Out.Number: '#77dd77', Token.Separator: '#d2b48c', Token.Toolbar.Search: '#ffd7a5 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffd7a5 noinherit', Token.Toolbar.Arg: '#ffd7a5 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#7b654a #e6c99f', Token.Toolbar.Signature.CurrentName: 'bg:#9c815d #ffffff bold', Token.Toolbar.Signature.Operator: '#e6c99f bold', Token.Docstring: '#ff9966', Token.Toolbar.Validation: 'bg:#594b36 #f9d48c', Token.Toolbar.Status: 'bg:#594b36 #f9d48c', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#594b36 #4cd964', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#594b36 #ff9966', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#594b36 #f9d48c', Token.Toolbar.Status.Key: 'bg:#7b654a #f9d48c', Token.Toolbar.Status.PasteModeOn: 'bg:#9c815d #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#594b36 #ff7518', Token.Toolbar.Status.PythonVersion: 'bg:#594b36 #ffffff bold', Token.Aborted: '#ff7518', Token.Sidebar: 'bg:#7b654a #e6c99f', Token.Sidebar.Title: 'bg:#9c815d #ffffff bold', Token.Sidebar.Label: 'bg:#7b654a #f9d48c', Token.Sidebar.Status: 'bg:#7b654a #ffffff', Token.Sidebar.Selected.Label: 'bg:#594b36 #ff7518', Token.Sidebar.Selected.Status: 'bg:#594b36 #ffffff bold', Token.Sidebar.Separator: 'bg:#7b654a #ffffff underline', Token.Sidebar.Key: 'bg:#7b654a #ffffff bold', Token.Sidebar.Key.Description: 'bg:#7b654a #ffffff', Token.Sidebar.HelpText: 'bg:#9c815d #e6c99f', Token.History.Line: '', Token.History.Line.Selected: 'bg:#7b654a #ffffff', Token.History.Line.Current: 'bg:#9c815d #e6c99f', Token.History.Line.Selected.Current: 'bg:#9c815d #ffffff', Token.History.ExistingInput: '#f9d48c', Token.Window.Border: '#d2b48c', Token.Window.Title: 'bg:#7b654a #ffffff', Token.Window.TIItleV2: 'bg:#9c815d #ffffff bold', Token.AcceptMessage: 'bg:#7b654a #e6c99f', Token.ExitConfirmation: 'bg:#9c815d #ff7518', Token.SearchMatch: '#f9d48c bg:#7b654a', Token.SearchMatch.Current: '#ff7518 bg:#9c815d', Token.SelectedText: '#ffffff bg:#9c815d', Token.Toolbar.Completions: 'bg:#7b654a #e6c99f', Token.Toolbar.Completions.Arrow: 'bg:#7b654a #f9d48c bold', Token.Toolbar.Completions.Completion: 'bg:#7b654a #e6c99f', Token.Toolbar.Completions.Completion.Current: 'bg:#9c815d #ffffff', Token.Menu.Completions.Completion: 'bg:#7b654a #e6c99f', Token.Menu.Completions.Completion.Current: 'bg:#9c815d #ffffff', Token.Menu.Completions.Meta: 'bg:#7b654a #f9d48c', Token.Menu.Completions.Meta.Current: 'bg:#9c815d #ff7518', Token.Menu.Completions.ProgressBar: 'bg:#77dd77', Token.Menu.Completions.ProgressButton: 'bg:#594b36'}

candy = {Token.LineNumber: '#ffff00 bg:#8800cc', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff66ff', Token.In.Number: '', Token.Out: '#00ffcc', Token.Out.Number: '#00ffcc', Token.Separator: '#ff44aa', Token.Toolbar.Search: '#ffaaff noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ffaaff noinherit', Token.Toolbar.Arg: '#ffaaff noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#cc00cc #00ffcc', Token.Toolbar.Signature.CurrentName: 'bg:#aa00aa #ffff00 bold', Token.Toolbar.Signature.Operator: '#00ffcc bold', Token.Docstring: '#ff44aa', Token.Toolbar.Validation: 'bg:#8800cc #ffaaff', Token.Toolbar.Status: 'bg:#8800cc #ffaaff', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#8800cc #00ffcc', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#8800cc #ff44aa', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#8800cc #ffff00', Token.Toolbar.Status.Key: 'bg:#cc00cc #ffff00', Token.Toolbar.Status.PasteModeOn: 'bg:#aa00aa #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#8800cc #ff44aa', Token.Toolbar.Status.PythonVersion: 'bg:#8800cc #ffffff bold', Token.Aborted: '#ff44aa', Token.Sidebar: 'bg:#cc00cc #00ffcc', Token.Sidebar.Title: 'bg:#aa00aa #ffffff bold', Token.Sidebar.Label: 'bg:#cc00cc #ffff00', Token.Sidebar.Status: 'bg:#cc00cc #ffffff', Token.Sidebar.Selected.Label: 'bg:#8800cc #ff44aa', Token.Sidebar.Selected.Status: 'bg:#8800cc #ffffff bold', Token.Sidebar.Separator: 'bg:#cc00cc #ffffff underline', Token.Sidebar.Key: 'bg:#cc00cc #ffffff bold', Token.Sidebar.Key.Description: 'bg:#cc00cc #ffffff', Token.Sidebar.HelpText: 'bg:#aa00aa #00ffcc', Token.History.Line: '', Token.History.Line.Selected: 'bg:#cc00cc #ffffff', Token.History.Line.Current: 'bg:#aa00aa #00ffcc', Token.History.Line.Selected.Current: 'bg:#aa00aa #ffffff', Token.History.ExistingInput: '#ffff00', Token.Window.Border: '#ff44aa', Token.Window.Title: 'bg:#cc00cc #ffffff', Token.Window.TIItleV2: 'bg:#aa00aa #ffffff bold', Token.AcceptMessage: 'bg:#cc00cc #00ffcc', Token.ExitConfirmation: 'bg:#aa00aa #ff44aa', Token.SearchMatch: '#ffff00 bg:#cc00cc', Token.SearchMatch.Current: '#ff44aa bg:#aa00aa', Token.SelectedText: '#ffffff bg:#aa00aa', Token.Toolbar.Completions: 'bg:#cc00cc #00ffcc', Token.Toolbar.Completions.Arrow: 'bg:#cc00cc #ffff00 bold', Token.Toolbar.Completions.Completion: 'bg:#cc00cc #00ffcc', Token.Toolbar.Completions.Completion.Current: 'bg:#aa00aa #ffffff', Token.Menu.Completions.Completion: 'bg:#cc00cc #00ffcc', Token.Menu.Completions.Completion.Current: 'bg:#aa00aa #ffffff', Token.Menu.Completions.Meta: 'bg:#cc00cc #ffff00', Token.Menu.Completions.Meta.Current: 'bg:#aa00aa #ff44aa', Token.Menu.Completions.ProgressBar: 'bg:#00ffcc', Token.Menu.Completions.ProgressButton: 'bg:#8800cc'}

cherry = {Token.LineNumber: '#f8c0c8 bg:#5a0010', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff3050', Token.In.Number: '', Token.Out: '#ff8095', Token.Out.Number: '#ff8095', Token.Separator: '#ff5070', Token.Toolbar.Search: '#ff9fb5 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff9fb5 noinherit', Token.Toolbar.Arg: '#ff9fb5 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#801020 #ffd0d8', Token.Toolbar.Signature.CurrentName: 'bg:#aa0020 #ffffff bold', Token.Toolbar.Signature.Operator: '#ffd0d8 bold', Token.Docstring: '#ffb0c0', Token.Toolbar.Validation: 'bg:#5a0010 #ffa0b0', Token.Toolbar.Status: 'bg:#5a0010 #ffa0b0', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#5a0010 #ffd0d8', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#5a0010 #ff5070', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#5a0010 #ffb0c0', Token.Toolbar.Status.Key: 'bg:#801020 #ffb0c0', Token.Toolbar.Status.PasteModeOn: 'bg:#aa0020 #ffffff', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#5a0010 #ff5070', Token.Toolbar.Status.PythonVersion: 'bg:#5a0010 #ffffff bold', Token.Aborted: '#ff5070', Token.Sidebar: 'bg:#801020 #ffd0d8', Token.Sidebar.Title: 'bg:#aa0020 #ffffff bold', Token.Sidebar.Label: 'bg:#801020 #ffb0c0', Token.Sidebar.Status: 'bg:#801020 #ffffff', Token.Sidebar.Selected.Label: 'bg:#5a0010 #ff5070', Token.Sidebar.Selected.Status: 'bg:#5a0010 #ffffff bold', Token.Sidebar.Separator: 'bg:#801020 #ffffff underline', Token.Sidebar.Key: 'bg:#801020 #ffffff bold', Token.Sidebar.Key.Description: 'bg:#801020 #ffffff', Token.Sidebar.HelpText: 'bg:#aa0020 #ffd0d8', Token.History.Line: '', Token.History.Line.Selected: 'bg:#801020 #ffffff', Token.History.Line.Current: 'bg:#aa0020 #ffd0d8', Token.History.Line.Selected.Current: 'bg:#aa0020 #ffffff', Token.History.ExistingInput: '#ffb0c0', Token.Window.Border: '#ff5070', Token.Window.Title: 'bg:#801020 #ffffff', Token.Window.TIItleV2: 'bg:#aa0020 #ffffff bold', Token.AcceptMessage: 'bg:#801020 #ffd0d8', Token.ExitConfirmation: 'bg:#aa0020 #ff5070', Token.SearchMatch: '#ffb0c0 bg:#801020', Token.SearchMatch.Current: '#ff5070 bg:#aa0020', Token.SelectedText: '#ffffff bg:#aa0020', Token.Toolbar.Completions: 'bg:#801020 #ffd0d8', Token.Toolbar.Completions.Arrow: 'bg:#801020 #ffb0c0 bold', Token.Toolbar.Completions.Completion: 'bg:#801020 #ffd0d8', Token.Toolbar.Completions.Completion.Current: 'bg:#aa0020 #ffffff', Token.Menu.Completions.Completion: 'bg:#801020 #ffd0d8', Token.Menu.Completions.Completion.Current: 'bg:#aa0020 #ffffff', Token.Menu.Completions.Meta: 'bg:#801020 #ffb0c0', Token.Menu.Completions.Meta.Current: 'bg:#aa0020 #ff5070', Token.Menu.Completions.ProgressBar: 'bg:#ffd0d8', Token.Menu.Completions.ProgressButton: 'bg:#5a0010'}

__all__ = (
    'get_all_code_styles',
    'get_all_ui_styles',
    'generate_style',
    'vaporwave',
    'synthwave',
    'sunset',
    'solarized_dark',
    'retro',
    'onedark',
    'nord',
    'night_owl',
    'monokai',
    'neon',
    'material',
    'github_dark',
    'galaxy',
    'cyberpunk',
    'candy',
    'cherry',
)

def randint(a_inclusive,b_inclusive=0):
    # If both a and b are specified, the range is inclusive, choose from range［a，b] ⋂ ℤ
    # Otherwise, if only a is specified, choose random element from the range ［a，b) ⋂ ℤ
    from random import randint
    return randint(min([a_inclusive,b_inclusive]),max([a_inclusive,b_inclusive]))

def random_index(array_length_or_array_itself):
    # Basically a random integer generator suited for generating array indices.
    # Returns a random integer ∈ ℤ ⋂ [0‚array_length)
    if isinstance(array_length_or_array_itself,int):
        assert array_length_or_array_itself != 0
        return randint(0,array_length_or_array_itself - 1)
    else:
        return random_index(len(array_length_or_array_itself))

def random_element(x):
    return x[random_index(len(x))]
def random_choice(*choices):
    return random_element(choices)



def random_hex_color():
    # return ''
    return '#'+''.join(random_element('0987654321ABCDEF') for _ in range(6))
def random_style():
    # return ''
    style=''
    style+=random_hex_color()
    style+=' '
    style+='bg:'+random_hex_color()
    style+=' '
    style+=random_choice('','underline','bold','italic')
    style+=' '
    style+='noinherit'
    return style
def get_all_code_styles():
    """
    Return a mapping from style names to their classes.
    """
    result = dict((name, get_style_by_name(name).styles) for name in get_all_styles())
    # from rp import mini_terminal_for_pythonista
    # exec(mini_terminal_for_pythonista)
    result['win32'] = win32_code_style
    result['ryan']=ryan_style
    result['clara']=clara_style
    result['newclara']=new_clara_style
    result['viper']=viper_style
    result['stratus']=stratus_style
    result['snape']=snape_style
    result['plain']=plain_style
    result['random']=random_syntax_style
    result['dracula']=dracula#i have no idea how this came to be lol...it just appeared on ws1 one day, even tho no word 'dracula' was on the original rp or any of its files...
    # Add new styles
    # Themes to style code in syntax highlighting
    result['solarized_dark'] = solarized_dark_style
    result['onedark'] = onedark_style
    result['nord'] = nord_style
    result['night_owl'] = night_owl_style
    result['monokai'] = monokai_style
    result['github_dark'] = github_dark_style
    result['tokyo_night'] = tokyo_night_style
    result['tomorrow'] = tomorrow_style
    result['tomorrow_night'] = tomorrow_night_style
    result['tomor_night_blu'] = tomorrow_night_blue_style
    result['tom_night_brite'] = tomorrow_night_bright_style
    result['tom_night_80s'] = tomorrow_night_eighties_style
    result['dejavu'] = dejavu_style
    result['sunset_warm'] = sunset_warm_style
    result['sunset_cool'] = sunset_cool_style
    result['sunset_mono'] = sunset_monokai_style
    result['clara_mono'] = clara_monokai_style
    result['synth_mono'] = synthwave_monokai_style
    
    return result
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Punctuation, Generic, Whitespace
"""
The style used in Lovelace interactive learning environment. Tries to avoid
the "angry fruit salad" effect with desaturated and dim colours.
"""
_KW_BLUE='#2838b0'
_NAME_GREEN='#388038'
_DOC_ORANGE='#b85820'
_OW_PURPLE='#a848a8'
_FUN_BROWN='#785840'
_STR_RED='#b83838'
_CLS_CYAN='#287088'
_ESCAPE_LIME='#709030'
_LABEL_CYAN='#289870'
_EXCEPT_YELLOW='#908828'
ryan_style={Token: '',
            Token.Comment: 'italic #888888',
            Token.Comment.Hashbang: '#287088',
            Token.Comment.Multiline: '#888888',
            Token.Comment.Preproc: 'noitalic #289870',
            Token.Comment.PreprocFile: '',
            Token.Comment.Single: '',
            Token.Comment.Special: '',
            # Token.Error: 'bg:#a848a8',
            Token.Escape: '',
            Token.Generic: '',
            Token.Generic.Deleted: '#c02828',
            Token.Generic.Emph: 'italic',
            Token.Generic.Error: '#c02828',
            Token.Generic.Heading: '#666666',
            Token.Generic.Inserted: '#388038',
            Token.Generic.Output: '#666666',
            Token.Generic.Prompt: '#444444',
            Token.Generic.Strong: 'bold',
            Token.Generic.Subheading: '#444444',
            Token.Generic.Traceback: '#2838b0',
            Token.Keyword: '#2838b0 bold',
            Token.Keyword.Constant: 'italic #444444',
            Token.Keyword.Declaration: 'italic',
            Token.Keyword.Pseudo: '',
            Token.Keyword.Reserved: '',
            Token.Keyword.Type: 'italic',
            Token.Literal: '',
            Token.Literal.Date: '',
            Token.Literal.Number: '#444444',
            Token.Literal.Number.Bin: '',
            Token.Literal.Number.Float: '',
            Token.Literal.Number.Hex: '',
            Token.Literal.Number.Integer: '',
            Token.Literal.Number.Integer.Long: '',
            Token.Literal.Number.Oct: '',
            Token.Literal.String: '#b83838',
            Token.Literal.String.Backtick: '',
            Token.Literal.String.Char: '#a848a8',
            Token.Literal.String.Doc: 'italic #b85820',
            Token.Literal.String.Double: '',
            Token.Literal.String.Escape: '#709030',
            Token.Literal.String.Heredoc: '',
            Token.Literal.String.Interpol: 'underline',
            Token.Literal.String.Other: '#a848a8',
            Token.Literal.String.Regex: '#a848a8',
            Token.Literal.String.Single: '',
            Token.Literal.String.Symbol: '',
            Token.Name: '',
            Token.Name.Attribute: '#388038',
            Token.Name.Builtin: '#388038',
            Token.Name.Builtin.Pseudo: 'italic',
            Token.Name.Class: '#287088',
            Token.Name.Constant: '#b85820',
            Token.Name.Decorator: '#287088',
            Token.Name.Entity: '#709030',
            Token.Name.Exception: '#908828',
            Token.Name.Function: '#785840',
            Token.Name.Label: '#289870',
            Token.Name.Namespace: '#289870',
            Token.Name.Other: '',
            Token.Name.Property: '',
            Token.Name.Tag: '#2838b0',
            Token.Name.Variable: '#b04040',
            Token.Name.Variable.Class: '',
            Token.Name.Variable.Global: '#908828',
            Token.Name.Variable.Instance: '',
            Token.Operator: '#666666',
            Token.Operator.Word: '#a848a8',
            Token.Other: '',
            Token.Punctuation: '#888888',
            Token.Text: '',
            Token.Text.Whitespace: '#a89028'}

plain_style={}
for key in ryan_style:
    plain_style[key]='noinherit'

clara_style={Token: '',
            Token.Comment: 'italic #51a6fb',
            Token.Comment.Hashbang: '#5126db',
            Token.Comment.Multiline: '#51a6fb',
            Token.Comment.Preproc: 'noitalic #3126ff',
            Token.Comment.PreprocFile: '',
            Token.Comment.Single: '',
            Token.Comment.Special: '',
            # Token.Error: 'bg:#7cd1a6',
            Token.Escape: '',
            Token.Generic: '',
            Token.Generic.Deleted: '#00f17b',
            Token.Generic.Emph: 'italic',
            Token.Generic.Error: '#00f17b',
            Token.Generic.Heading: '#2479ce',
            Token.Generic.Inserted: '#003cf0',
            Token.Generic.Output: '#2479ce',
            Token.Generic.Prompt: '#004ca0',
            Token.Generic.Strong: 'bold',
            Token.Generic.Subheading: '#004ca0',
            Token.Generic.Traceback: '#862690',
            Token.Keyword: '#862690 bold',
            Token.Keyword.Constant: 'italic #004ca0',
            Token.Keyword.Declaration: 'italic',
            Token.Keyword.Pseudo: '',
            Token.Keyword.Reserved: '',
            Token.Keyword.Type: 'italic',
            Token.Literal: '',
            Token.Literal.Date: '',
            Token.Literal.Number: '#004ca0',
            Token.Literal.Number.Bin: '',
            Token.Literal.Number.Float: '',
            Token.Literal.Number.Hex: '',
            Token.Literal.Number.Integer: '',
            Token.Literal.Number.Integer.Long: '',
            Token.Literal.Number.Oct: '',
            Token.Literal.String: '#00e690',
            Token.Literal.String.Backtick: '',
            Token.Literal.String.Char: '#7cd1a6',
            Token.Literal.String.Doc: 'italic #00e6bb',
            Token.Literal.String.Double: '',
            Token.Literal.String.Escape: '#0086ff',
            Token.Literal.String.Heredoc: '',
            Token.Literal.String.Interpol: 'underline',
            Token.Literal.String.Other: '#7cd1a6',
            Token.Literal.String.Regex: '#7cd1a6',
            Token.Literal.String.Single: '',
            Token.Literal.String.Symbol: '',
            Token.Name: '',
            Token.Name.Attribute: '#003cf0',
            Token.Name.Builtin: '#003cf0',
            Token.Name.Builtin.Pseudo: 'italic',
            Token.Name.Class: '#5126db',
            Token.Name.Constant: '#00e6bb',
            Token.Name.Decorator: '#5126db',
            Token.Name.Entity: '#0086ff',
            Token.Name.Exception: '#00b1fb',
            Token.Name.Function: '#0091bb',
            Token.Name.Label: '#3126ff',
            Token.Name.Namespace: '#3126ff',
            Token.Name.Other: '',
            Token.Name.Property: '',
            Token.Name.Tag: '#862690',
            Token.Name.Variable: '#00dc9b',
            Token.Name.Variable.Class: '',
            Token.Name.Variable.Global: '#00b1fb',
            Token.Name.Variable.Instance: '',
            Token.Operator: '#2479ce',
            Token.Operator.Word: '#7cd1a6',
            Token.Other: '',
            Token.Punctuation: '#51a6fb',
            Token.Text: '',
            Token.Text.Whitespace: '#00d1ff'}

new_clara_style=clara_style.copy()
new_clara_style_diff={
            Token.Keyword: '#D026B0 bold',
            Token.Name.Builtin: '#008cf0',
            Token.Name.Function: '#21d988',
            Token.Name.Class: '#17ff9a bold',
            Token.Literal.Number: '#55CDFC',
            Token.Literal.Number: '#2196d9',
            Token.Name.Decorator: '#8730ff',
            Token.Keyword.Constant: 'italic #008cD0',
            Token.Keyword.Declaration: 'italic',
            Token.Keyword.Pseudo: '',
            Token.Keyword.Reserved: '',
            Token.Keyword.Type: 'italic',
}
new_clara_style.update(new_clara_style_diff)


random_syntax_style={Token: random_style(),
            Token.Comment: random_style(),
            Token.Comment.Hashbang: random_style(),
            Token.Comment.Multiline: random_style(),
            Token.Comment.Preproc: random_style(),
            Token.Comment.PreprocFile: random_style(),
            Token.Comment.Single: random_style(),
            Token.Comment.Special: random_style(),
            # Token.Error: random_style(),
            Token.Escape: random_style(),
            Token.Generic: random_style(),
            Token.Generic.Deleted: random_style(),
            Token.Generic.Emph: random_style(),
            Token.Generic.Error: random_style(),
            Token.Generic.Heading: random_style(),
            Token.Generic.Inserted: random_style(),
            Token.Generic.Output: random_style(),
            Token.Generic.Prompt: random_style(),
            Token.Generic.Strong: random_style(),
            Token.Generic.Subheading: random_style(),
            Token.Generic.Traceback: random_style(),
            Token.Keyword: random_style(),
            Token.Keyword.Constant: random_style(),
            Token.Keyword.Declaration: random_style(),
            Token.Keyword.Pseudo: random_style(),
            Token.Keyword.Reserved: random_style(),
            Token.Keyword.Type: random_style(),
            Token.Literal: random_style(),
            Token.Literal.Date: random_style(),
            Token.Literal.Number: random_style(),
            Token.Literal.Number.Bin: random_style(),
            Token.Literal.Number.Float: random_style(),
            Token.Literal.Number.Hex: random_style(),
            Token.Literal.Number.Integer: random_style(),
            Token.Literal.Number.Integer.Long: random_style(),
            Token.Literal.Number.Oct: random_style(),
            Token.Literal.String: random_style(),
            Token.Literal.String.Backtick: random_style(),
            Token.Literal.String.Char: random_style(),
            Token.Literal.String.Doc: random_style(),
            Token.Literal.String.Double: random_style(),
            Token.Literal.String.Escape: random_style(),
            Token.Literal.String.Heredoc: random_style(),
            Token.Literal.String.Interpol: random_style(),
            Token.Literal.String.Other: random_style(),
            Token.Literal.String.Regex: random_style(),
            Token.Literal.String.Single: random_style(),
            Token.Literal.String.Symbol: random_style(),
            Token.Name: random_style(),
            Token.Name.Attribute: random_style(),
            Token.Name.Builtin: random_style(),
            Token.Name.Builtin.Pseudo: random_style(),
            Token.Name.Class: random_style(),
            Token.Name.Constant: random_style(),
            Token.Name.Decorator: random_style(),
            Token.Name.Entity: random_style(),
            Token.Name.Exception: random_style(),
            Token.Name.Function: random_style(),
            Token.Name.Label: random_style(),
            Token.Name.Namespace: random_style(),
            Token.Name.Other: random_style(),
            Token.Name.Property: random_style(),
            Token.Name.Tag: random_style(),
            Token.Name.Variable: random_style(),
            Token.Name.Variable.Class: random_style(),
            Token.Name.Variable.Global: random_style(),
            Token.Name.Variable.Instance: random_style(),
            Token.Operator: random_style(),
            Token.Operator.Word: random_style(),
            Token.Other: random_style(),
            Token.Punctuation: random_style(),
            Token.Text: random_style(),
            Token.Text.Whitespace: random_style()}

viper_style={Token: '',
            Token.Comment:                        ' italic      #fb51a6',
            Token.Comment.Hashbang:               '             #db5126',
            Token.Comment.Multiline:              '             #fb51a6',
            Token.Comment.Preproc:                ' noitalic    #ff3126',
            Token.Comment.PreprocFile:            ' ',
            Token.Comment.Single:                 ' ',
            Token.Comment.Special:                ' ',
            # Token.Error:                          ' bg:         #a67cd1',
            Token.Escape:                         ' ',
            Token.Generic:                        ' ',
            Token.Generic.Deleted:                '             #7b00f1',
            Token.Generic.Emph:                   ' italic',
            Token.Generic.Error:                  '             #7b00f1',
            Token.Generic.Heading:                '             #ce2479',
            Token.Generic.Inserted:               '             #f0003c',
            Token.Generic.Output:                 '             #ce2479',
            Token.Generic.Prompt:                 '             #a0004c',
            Token.Generic.Strong:                 ' bold',
            Token.Generic.Subheading:             '             #a0004c',
            Token.Generic.Traceback:              '             #908626',
            Token.Keyword:                        '             #908626 bold',
            Token.Keyword.Constant:               ' italic      #a0004c',
            Token.Keyword.Declaration:            ' italic',
            Token.Keyword.Pseudo:                 ' ',
            Token.Keyword.Reserved:               ' ',
            Token.Keyword.Type:                   ' italic',
            Token.Literal:                        ' ',
            Token.Literal.Date:                   ' ',
            Token.Literal.Number:                 '             #a0004c',
            Token.Literal.Number.Bin:             ' ',
            Token.Literal.Number.Float:           ' ',
            Token.Literal.Number.Hex:             ' ',
            Token.Literal.Number.Integer:         ' ',
            Token.Literal.Number.Integer.Long:    ' ',
            Token.Literal.Number.Oct:             ' ',
            Token.Literal.String:                 '             #9000e6',
            Token.Literal.String.Backtick:        ' ',
            Token.Literal.String.Char:            '             #a67cd1',
            Token.Literal.String.Doc:             ' italic      #bb00e6',
            Token.Literal.String.Double:          ' ',
            Token.Literal.String.Escape:          '             #ff0086',
            Token.Literal.String.Heredoc:         ' ',
            Token.Literal.String.Interpol:        ' underline',
            Token.Literal.String.Other:           '             #a67cd1',
            Token.Literal.String.Regex:           '             #a67cd1',
            Token.Literal.String.Single:          ' ',
            Token.Literal.String.Symbol:          ' ',
            Token.Name:                           ' ',
            Token.Name.Attribute:                 '             #f0003c',
            Token.Name.Builtin:                   '             #f0003c',
            Token.Name.Builtin.Pseudo:            ' italic',
            Token.Name.Class:                     '             #db5126',
            Token.Name.Constant:                  '             #bb00e6',
            Token.Name.Decorator:                 '             #db5126',
            Token.Name.Entity:                    '             #ff0086',
            Token.Name.Exception:                 '             #fb00b1',
            Token.Name.Function:                  '             #bb0091',
            Token.Name.Label:                     '             #ff3126',
            Token.Name.Namespace:                 '             #ff3126',
            Token.Name.Other:                     ' ',
            Token.Name.Property:                  ' ',
            Token.Name.Tag:                       '             #908626',
            Token.Name.Variable:                  '             #9b00dc',
            Token.Name.Variable.Class:            ' ',
            Token.Name.Variable.Global:           '             #fb00b1',
            Token.Name.Variable.Instance:         ' ',
            Token.Operator:                       '             #ce2479',
            Token.Operator.Word:                  '             #a67cd1',
            Token.Other:                          ' ',
            Token.Punctuation:                    '             #fb51a6',
            Token.Text:                           ' ',
            Token.Text.Whitespace:                '             #ff00d1'}


stratus_style={Token: '',
            Token.Comment:                        ' italic      #a6fb51',
            Token.Comment.Hashbang:               '             #26db51',
            Token.Comment.Multiline:              '             #a6fb51',
            Token.Comment.Preproc:                ' noitalic    #26ff31',
            Token.Comment.PreprocFile:            ' ',
            Token.Comment.Single:                 ' ',
            Token.Comment.Special:                ' ',
            # Token.Error:                          ' bg:         #d1a67c',
            Token.Escape:                         ' ',
            Token.Generic:                        ' ',
            Token.Generic.Deleted:                '             #f17b00',
            Token.Generic.Emph:                   ' italic',
            Token.Generic.Error:                  '             #f17b00',
            Token.Generic.Heading:                '             #79ce24',
            Token.Generic.Inserted:               '             #3cf000',
            Token.Generic.Output:                 '             #79ce24',
            Token.Generic.Prompt:                 '             #4ca000',
            Token.Generic.Strong:                 ' bold',
            Token.Generic.Subheading:             '             #4ca000',
            Token.Generic.Traceback:              '             #269086',
            Token.Keyword:                        '             #269086 bold',
            Token.Keyword.Constant:               ' italic      #4ca000',
            Token.Keyword.Declaration:            ' italic',
            Token.Keyword.Pseudo:                 ' ',
            Token.Keyword.Reserved:               ' ',
            Token.Keyword.Type:                   ' italic',
            Token.Literal:                        ' ',
            Token.Literal.Date:                   ' ',
            Token.Literal.Number:                 '             #4ca000',
            Token.Literal.Number.Bin:             ' ',
            Token.Literal.Number.Float:           ' ',
            Token.Literal.Number.Hex:             ' ',
            Token.Literal.Number.Integer:         ' ',
            Token.Literal.Number.Integer.Long:    ' ',
            Token.Literal.Number.Oct:             ' ',
            Token.Literal.String:                 '             #e69000',
            Token.Literal.String.Backtick:        ' ',
            Token.Literal.String.Char:            '             #d1a67c',
            Token.Literal.String.Doc:             ' italic      #e6bb00',
            Token.Literal.String.Double:          ' ',
            Token.Literal.String.Escape:          '             #86ff00',
            Token.Literal.String.Heredoc:         ' ',
            Token.Literal.String.Interpol:        ' underline',
            Token.Literal.String.Other:           '             #d1a67c',
            Token.Literal.String.Regex:           '             #d1a67c',
            Token.Literal.String.Single:          ' ',
            Token.Literal.String.Symbol:          ' ',
            Token.Name:                           ' ',
            Token.Name.Attribute:                 '             #3cf000',
            Token.Name.Builtin:                   '             #3cf000',
            Token.Name.Builtin.Pseudo:            ' italic',
            Token.Name.Class:                     '             #26db51',
            Token.Name.Constant:                  '             #e6bb00',
            Token.Name.Decorator:                 '             #26db51',
            Token.Name.Entity:                    '             #86ff00',
            Token.Name.Exception:                 '             #b1fb00',
            Token.Name.Function:                  '             #91bb00',
            Token.Name.Label:                     '             #26ff31',
            Token.Name.Namespace:                 '             #26ff31',
            Token.Name.Other:                     ' ',
            Token.Name.Property:                  ' ',
            Token.Name.Tag:                       '             #269086',
            Token.Name.Variable:                  '             #dc9b00',
            Token.Name.Variable.Class:            ' ',
            Token.Name.Variable.Global:           '             #b1fb00',
            Token.Name.Variable.Instance:         ' ',
            Token.Operator:                       '             #79ce24',
            Token.Operator.Word:                  '             #d1a67c',
            Token.Other:                          ' ',
            Token.Punctuation:                    '             #a6fb51',
            Token.Text:                           ' ',
            Token.Text.Whitespace:                '             #d1ff00'}


snape_style={Token: '',
            Token.Comment:                        ' italic      #51a6fb',
            Token.Comment.Hashbang:               '             #5126db',
            Token.Comment.Multiline:              '             #51a6fb',
            Token.Comment.Preproc:                ' noitalic    #3126ff',
            Token.Comment.PreprocFile:            ' ',
            Token.Comment.Single:                 ' ',
            Token.Comment.Special:                ' ',
            Token.Error:                          ' bg:         #7cd1a6',
            Token.Escape:                         ' ',
            Token.Generic:                        ' ',
            Token.Generic.Deleted:                '             #00f17b',
            Token.Generic.Emph:                   ' italic',
            Token.Generic.Error:                  '             #00f17b',
            Token.Generic.Heading:                '             #2479ce',
            Token.Generic.Inserted:               '             #003cf0',
            Token.Generic.Output:                 '             #2479ce',
            Token.Generic.Prompt:                 '             #004ca0',
            Token.Generic.Strong:                 ' bold',
            Token.Generic.Subheading:             '             #004ca0',
            Token.Generic.Traceback:              '             #862690',
            Token.Keyword:                        '             #862690 bold',
            Token.Keyword.Constant:               ' italic      #004ca0',
            Token.Keyword.Declaration:            ' italic',
            Token.Keyword.Pseudo:                 ' ',
            Token.Keyword.Reserved:               ' ',
            Token.Keyword.Type:                   ' italic',
            Token.Literal:                        ' ',
            Token.Literal.Date:                   ' ',
            Token.Literal.Number:                 '             #004ca0',
            Token.Literal.Number.Bin:             ' ',
            Token.Literal.Number.Float:           ' ',
            Token.Literal.Number.Hex:             ' ',
            Token.Literal.Number.Integer:         ' ',
            Token.Literal.Number.Integer.Long:    ' ',
            Token.Literal.Number.Oct:             ' ',
            Token.Literal.String:                 '             #00e690',
            Token.Literal.String.Backtick:        ' ',
            Token.Literal.String.Char:            '             #7cd1a6',
            Token.Literal.String.Doc:             ' italic      #00e6bb',
            Token.Literal.String.Double:          ' ',
            Token.Literal.String.Escape:          '             #0086ff',
            Token.Literal.String.Heredoc:         ' ',
            Token.Literal.String.Interpol:        ' underline',
            Token.Literal.String.Other:           '             #7cd1a6',
            Token.Literal.String.Regex:           '             #7cd1a6',
            Token.Literal.String.Single:          ' ',
            Token.Literal.String.Symbol:          ' ',
            Token.Name:                           ' ',
            Token.Name.Attribute:                 '             #003cf0',
            Token.Name.Builtin:                   '             #003cf0',
            Token.Name.Builtin.Pseudo:            ' italic',
            Token.Name.Class:                     '             #5126db',
            Token.Name.Constant:                  '             #00e6bb',
            Token.Name.Decorator:                 '             #5126db',
            Token.Name.Entity:                    '             #0086ff',
            Token.Name.Exception:                 '             #00b1fb',
            Token.Name.Function:                  '             #0091bb',
            Token.Name.Label:                     '             #3126ff',
            Token.Name.Namespace:                 '             #3126ff',
            Token.Name.Other:                     ' ',
            Token.Name.Property:                  ' ',
            Token.Name.Tag:                       '             #862690',
            Token.Name.Variable:                  '             #00dc9b',
            Token.Name.Variable.Class:            ' ',
            Token.Name.Variable.Global:           '             #00b1fb',
            Token.Name.Variable.Instance:         ' ',
            Token.Operator:                       '             #2479ce',
            Token.Operator.Word:                  '             #7cd1a6',
            Token.Other:                          ' ',
            Token.Punctuation:                    '             #51a6fb',
            Token.Text:                           ' ',
            Token.Text.Whitespace:                '             #00d1ff'}


# ryan_style= \
#     {
#         # A rich, colored scheme I made (based on monokai)
#         Comment:"#00ff00",
#         Keyword:'#44ff44',
#         Number:'#378cba',
#         Operator:'',
#         String:'#26b534',
#         Token.Literal.String.Escape :"  #ae81ff",
#         #
#         Name:'',
#         Name.Decorator:'#ff4444',
#         Name.Class:'#ff4444',
#         Name.Function:'#ff4444',
#         Name.Builtin:'#ff4444',
#         #
#         Name.Attribute:'',
#         Name.Constant:'',
#         Name.Entity:'',
#         Name.Exception:'',
#         Name.Label:'',
#         Name.Namespace:'#dcff2d',
#         Name.Tag:'',
#         Name.Variable:'',
#     }


def generate_style(python_style, ui_style, code_invert_colors=False, code_invert_brightness=False, 
                ui_invert_colors=False, ui_invert_brightness=False, code_hue_shift=0, ui_hue_shift=0,
                code_min_brightness=0.0, code_max_brightness=1.0, ui_min_brightness=0.0, ui_max_brightness=1.0,
                code_min_saturation=0.0, code_max_saturation=1.0, ui_min_saturation=0.0, ui_max_saturation=1.0,
                ui_bg_fg_contrast=1.0, code_ui_min_brightness=None, code_ui_max_brightness=None):
    """
    Generate Pygments Style class from two dictionaries
    containing style rules.
    
    :param python_style: Dictionary with the Python code style.
    :param ui_style: Dictionary with the UI style.
    :param code_invert_colors: Boolean indicating whether code colors should be inverted.
    :param code_invert_brightness: Boolean indicating whether code brightness should be inverted 
                                  while preserving hue.
    :param ui_invert_colors: Boolean indicating whether UI colors should be inverted.
    :param ui_invert_brightness: Boolean indicating whether UI brightness should be inverted 
                                while preserving hue.
    :param code_hue_shift: Integer indicating the number of degrees to shift the hue for code elements (0-360).
    :param ui_hue_shift: Integer indicating the number of degrees to shift the hue for UI elements (0-360).
    :param code_min_brightness: Float (0.0-1.0) indicating the minimum brightness for code elements.
    :param code_max_brightness: Float (0.0-1.0) indicating the maximum brightness for code elements.
    :param ui_min_brightness: Float (0.0-1.0) indicating the minimum brightness for UI elements.
    :param ui_max_brightness: Float (0.0-1.0) indicating the maximum brightness for UI elements.
    :param code_min_saturation: Float (0.0-1.0) indicating the minimum saturation for code elements.
    :param code_max_saturation: Float (0.0-1.0) indicating the maximum saturation for code elements.
    :param ui_min_saturation: Float (0.0-1.0) indicating the minimum saturation for UI elements.
    :param ui_max_saturation: Float (0.0-1.0) indicating the maximum saturation for UI elements.
    :param ui_bg_fg_contrast: Float (0.1-3.0) indicating the contrast multiplier between background and foreground colors.
    :param code_ui_min_brightness: Float (0.0-1.0) indicating the minimum brightness for code UI elements 
                             (whitespace, indent guides, row/column highlights). Defaults to 0.0 if None.
    :param code_ui_max_brightness: Float (0.0-1.0) indicating the maximum brightness for code UI elements
                             (whitespace, indent guides, row/column highlights). Defaults to 1.0 if None.
    """
    assert isinstance(python_style, dict)  or isinstance(ui_style,ChaosStyle)
    assert isinstance(ui_style, dict) or isinstance(ui_style,ChaosStyle)

    # Process the python style dictionary with transformations
    processed_python_style = {}
    for token, style_str in python_style.items():
        processed_style = style_str
        
        # Apply code brightness inversion if enabled
        if code_invert_brightness:
            processed_style = invert_brightness_string(processed_style)
            
        # Apply code color inversion if enabled
        if code_invert_colors:
            processed_style = invert_style_string(processed_style)
            
        # Apply code brightness limits
        if code_min_brightness > 0.0 or code_max_brightness < 1.0:
            processed_style = adjust_brightness_range_string(processed_style, code_min_brightness, code_max_brightness)
            
        # Apply code saturation limits
        if code_min_saturation > 0.0 or code_max_saturation < 1.0:
            processed_style = adjust_saturation_range_string(processed_style, code_min_saturation, code_max_saturation)
            
        # Apply code hue shift after saturation changes
        if code_hue_shift != 0:
            processed_style = shift_hue_string(processed_style, code_hue_shift)
            
        processed_python_style[token] = processed_style

    # Process the UI style dictionary with transformations
    processed_ui_style = {}
    for token, style_str in ui_style.items():
        processed_style = style_str
        
        # Apply UI brightness inversion if enabled
        if ui_invert_brightness:
            processed_style = invert_brightness_string(processed_style)
            
        # Apply UI color inversion if enabled
        if ui_invert_colors:
            processed_style = invert_style_string(processed_style)
            
        # Apply UI brightness limits
        if ui_min_brightness > 0.0 or ui_max_brightness < 1.0:
            processed_style = adjust_brightness_range_string(processed_style, ui_min_brightness, ui_max_brightness)
            
        # Apply UI saturation limits
        if ui_min_saturation > 0.0 or ui_max_saturation < 1.0:
            processed_style = adjust_saturation_range_string(processed_style, ui_min_saturation, ui_max_saturation)
            
        # Apply UI hue shift after saturation changes
        if ui_hue_shift != 0:
            processed_style = shift_hue_string(processed_style, ui_hue_shift)
            
        processed_ui_style[token] = processed_style

    # Combine the processed styles
    styles = {}
    styles.update(DEFAULT_STYLE_EXTENSIONS)
    styles.update(processed_python_style)
    styles.update(processed_ui_style)
    
    # Apply contrast adjustment between background and foreground as the very last step
    # This ensures it's applied after all other transformations
    if ui_bg_fg_contrast != 1.0:
        styles = adjust_fg_bg_contrast(styles, ui_bg_fg_contrast)
    
    # Apply code transformations to code-related elements like whitespace, indent guides, and cursor line
    # These are part of the code display, so they should have the same transformations applied
    code_tokens = {
        Token.IndentGuide: '#303030',
        Token.Whitespace: '#252525',
        Token.Whitespace.Space: '#252525',
        Token.Whitespace.Tab: '#FF2525',
        Token.CursorLine: 'bg:#2a3438',
        # Token.CursorColumn: 'bg:#3c464a'
        Token.CursorColumn: 'bg:#1c262a'
    }
    
    # Apply code UI-specific transformations to these tokens
    # Use code_ui_ settings directly, do not fall back to code_ settings
    # This ensures code_ui elements have their own brightness independent of code elements
    code_ui_min_b = 0.0 if code_ui_min_brightness is None else code_ui_min_brightness
    code_ui_max_b = 1.0 if code_ui_max_brightness is None else code_ui_max_brightness
    
    for token, style_str in code_tokens.items():
        processed_style = style_str
        
        # Apply code brightness inversion if enabled
        if code_invert_brightness:
            processed_style = invert_brightness_string(processed_style)
            
        # Apply code color inversion if enabled
        if code_invert_colors:
            processed_style = invert_style_string(processed_style)
            
        # Apply code UI-specific brightness limits
        if code_ui_min_b > 0.0 or code_ui_max_b < 1.0:
            processed_style = adjust_brightness_range_string(processed_style, code_ui_min_b, code_ui_max_b)
            
        # Apply code saturation limits (using code saturation settings)
        if code_min_saturation > 0.0 or code_max_saturation < 1.0:
            processed_style = adjust_saturation_range_string(processed_style, code_min_saturation, code_max_saturation)
            
        # Apply code hue shift after saturation changes
        if code_hue_shift != 0:
            processed_style = shift_hue_string(processed_style, code_hue_shift)
            
        styles[token] = processed_style

    return style_from_dict(styles)

import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB floats (0.0-1.0)"""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    try:
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)
    except Exception:
        return (0, 0, 0)  # Default to black on error

def rgb_to_hex(r, g, b):
    """Convert RGB floats to hex color string"""
    r_hex = '{0:02x}'.format(max(0, min(255, int(r * 255))))
    g_hex = '{0:02x}'.format(max(0, min(255, int(g * 255))))
    b_hex = '{0:02x}'.format(max(0, min(255, int(b * 255))))
    return '#{0}{1}{2}'.format(r_hex, g_hex, b_hex)

def transform_color(color, transform_func):
    """Apply a transform function to a color in hex format"""
    if not color.startswith('#'):
        return color
    try:
        r, g, b = hex_to_rgb(color)
        r, g, b = transform_func(r, g, b)
        return rgb_to_hex(r, g, b)
    except Exception:
        return color

def transform_style_string(style_str, transform_func):
    """Apply a transform function to all colors in a style string"""
    if not style_str:
        return style_str
        
    parts = style_str.split()
    transformed_parts = []
    
    for part in parts:
        if part.startswith('bg:'):
            color = part[3:]
            if color.startswith('#'):
                transformed_hex = transform_color(color, transform_func)
                transformed_parts.append('bg:' + transformed_hex)
            else:
                transformed_parts.append(part)
        elif part.startswith('#'):
            transformed_hex = transform_color(part, transform_func)
            transformed_parts.append(transformed_hex)
        else:
            transformed_parts.append(part)
    
    return ' '.join(transformed_parts)

# Color transformation functions
def shift_hue_transform(degrees):
    """Create transform function that shifts hue"""
    def transform(r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + (degrees/360.0)) % 1.0  # Shift hue and wrap around 0-1
        return colorsys.hsv_to_rgb(h, s, v)
    return transform

def brightness_invert_transform():
    """Create transform function that inverts brightness"""
    def transform(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = 1.0 - l  # Invert lightness
        return colorsys.hls_to_rgb(h, l, s)
    return transform

def color_invert_transform():
    """Create transform function that inverts colors"""
    def transform(r, g, b):
        return (1.0 - r, 1.0 - g, 1.0 - b)
    return transform

def brightness_range_transform(min_brightness=0.0, max_brightness=1.0):
    """Create transform function that rescales brightness to the specified range"""
    def transform(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        # Rescale lightness: x = x * (max - min) + min
        l = l * (max_brightness - min_brightness) + min_brightness
        return colorsys.hls_to_rgb(h, l, s)
    return transform

def saturation_range_transform(min_saturation=0.0, max_saturation=1.0):
    """Create transform function that rescales saturation to the specified range"""
    def transform(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        # Rescale saturation: x = x * (max - min) + min
        s = s * (max_saturation - min_saturation) + min_saturation
        return colorsys.hls_to_rgb(h, l, s)
    return transform

# Style string transformers that use the generic transform_style_string function
def shift_hue_string(style_str, degrees):
    """Shift the hue of colors in a style string"""
    return transform_style_string(style_str, shift_hue_transform(degrees))

def invert_brightness_string(style_str):
    """Invert brightness of colors in a style string"""
    return transform_style_string(style_str, brightness_invert_transform())

def adjust_brightness_range_string(style_str, min_brightness=0.0, max_brightness=1.0):
    """Adjust brightness range of colors in a style string"""
    return transform_style_string(style_str, brightness_range_transform(min_brightness, max_brightness))

def adjust_saturation_range_string(style_str, min_saturation=0.0, max_saturation=1.0):
    """Adjust saturation range of colors in a style string"""
    return transform_style_string(style_str, saturation_range_transform(min_saturation, max_saturation))

def force_black_white(style_dict):
    """
    Force all foreground/background pairs to be black and white.
    
    Args:
        style_dict: Dictionary of token -> style strings
        
    Returns:
        New style dictionary with black and white colors
    """
    new_style_dict = {}
    
    for token, style_str in style_dict.items():
        if not style_str:
            new_style_dict[token] = style_str
            continue
            
        # Parse the style string into components
        parts = style_str.split()
        fg_part = None
        bg_part = None
        other_parts = []
        
        # Identify foreground and background colors
        for part in parts:
            if part.startswith('bg:#'):
                bg_part = part
            elif part.startswith('#'):
                fg_part = part
            else:
                other_parts.append(part)
        
        # If we don't have both fg and bg, skip this token
        if not fg_part or not bg_part:
            new_style_dict[token] = style_str
            continue
        
        # Extract RGB values
        fg_r, fg_g, fg_b = hex_to_rgb(fg_part)
        bg_r, bg_g, bg_b = hex_to_rgb(bg_part[3:])  # Skip the "bg:" prefix
        
        # Calculate brightness for foreground and background
        fg_brightness = 0.299*fg_r + 0.587*fg_g + 0.114*fg_b
        bg_brightness = 0.299*bg_r + 0.587*bg_g + 0.114*bg_b
        
        # Set to black and white based on which was originally brighter
        if fg_brightness >= bg_brightness:
            # Foreground was brighter, so make it white and background black
            new_fg = "#ffffff"
            new_bg = "bg:#000000"
        else:
            # Background was brighter, so make it white and foreground black
            new_fg = "#000000"
            new_bg = "bg:#ffffff"
        
        # Construct the new style string
        new_parts = other_parts + [new_fg, new_bg]
        new_style_dict[token] = ' '.join(new_parts)
    
    return new_style_dict

def adjust_fg_bg_contrast(style_dict, min_brightness_delta=0.0):
    """
    Ensure a minimum brightness difference between foreground and background colors.
    
    Args:
        style_dict: Dictionary of token -> style strings
        min_brightness_delta: Minimum brightness difference (0.0-1.0) 
                             0.0 = no change
                             1.0 = maximum contrast (black/white)
    
    Returns:
        New style dictionary with adjusted colors
    """
    # Ensure min_brightness_delta is in valid range 0.0-1.0
    min_brightness_delta = max(0.0, min(0.98, min_brightness_delta))
    
    if min_brightness_delta <= 0.001:  # Small threshold to handle floating point errors
        # No change needed for very small values
        return style_dict
        
    # Make a copy of the style dictionary
    new_style_dict = {}
    
    # Process each token and its style string
    for token, style_str in style_dict.items():
        if not style_str:
            new_style_dict[token] = style_str
            continue
            
        # Parse the style string into components
        parts = style_str.split()
        fg_part = None
        bg_part = None
        other_parts = []
        
        # Identify foreground and background colors
        for part in parts:
            if part.startswith('bg:#'):
                bg_part = part
            elif part.startswith('#'):
                fg_part = part
            else:
                other_parts.append(part)
        
        # If we don't have both fg and bg, skip this token
        if not fg_part or not bg_part:
            new_style_dict[token] = style_str
            continue
        
        # Extract RGB values
        fg_r, fg_g, fg_b = hex_to_rgb(fg_part)
        bg_r, bg_g, bg_b = hex_to_rgb(bg_part[3:])  # Skip the "bg:" prefix
        
        # Calculate brightness for foreground and background
        # Using the perceived luminance formula: 0.299*R + 0.587*G + 0.114*B
        fg_brightness = 0.299*fg_r + 0.587*fg_g + 0.114*fg_b
        bg_brightness = 0.299*bg_r + 0.587*bg_g + 0.114*bg_b
        
        # Sort by brightness
        if fg_brightness >= bg_brightness:
            lighter_color = (fg_r, fg_g, fg_b)
            darker_color = (bg_r, bg_g, bg_b)
            fg_is_lighter = True
        else:
            lighter_color = (bg_r, bg_g, bg_b)
            darker_color = (fg_r, fg_g, fg_b)
            fg_is_lighter = False
        
        lighter_brightness = max(fg_brightness, bg_brightness)
        darker_brightness = min(fg_brightness, bg_brightness)
        
        # Current brightness difference
        brightness_delta = lighter_brightness - darker_brightness
        
        # If current difference is less than minimum, adjust both colors
        if brightness_delta < min_brightness_delta:
            # How much we need to adjust
            adjustment_needed = min_brightness_delta - brightness_delta
            
            # Blend lighter color with white and darker color with black
            # to achieve the desired brightness difference
            
            # First, determine how much to adjust each color
            # We'll move both equally to maintain the midpoint
            lighter_adjustment = adjustment_needed / 2
            darker_adjustment = adjustment_needed / 2
            
            # Adjust brightness of both colors, but ensure we can't exceed the 0-1 range
            if lighter_brightness + lighter_adjustment > 1.0:
                # Can't go brighter than 1.0, adjust darker color more
                extra = (lighter_brightness + lighter_adjustment) - 1.0
                lighter_adjustment = 1.0 - lighter_brightness
                darker_adjustment += extra
            
            if darker_brightness - darker_adjustment < 0.0:
                # Can't go darker than 0.0, adjust lighter color more
                extra = darker_adjustment - darker_brightness
                darker_adjustment = darker_brightness
                lighter_adjustment += extra
            
            # Now blend with white/black to achieve the new brightness
            # For lighter color, blend with white (1,1,1)
            lighter_blend_amount = lighter_adjustment / (1.0 - lighter_brightness) if lighter_brightness < 1.0 else 0.0
            new_lighter_r = lighter_color[0] * (1 - lighter_blend_amount) + 1.0 * lighter_blend_amount
            new_lighter_g = lighter_color[1] * (1 - lighter_blend_amount) + 1.0 * lighter_blend_amount
            new_lighter_b = lighter_color[2] * (1 - lighter_blend_amount) + 1.0 * lighter_blend_amount
            
            # For darker color, blend with black (0,0,0)
            darker_blend_amount = darker_adjustment / darker_brightness if darker_brightness > 0.0 else 1.0
            new_darker_r = darker_color[0] * (1 - darker_blend_amount) + 0.0 * darker_blend_amount
            new_darker_g = darker_color[1] * (1 - darker_blend_amount) + 0.0 * darker_blend_amount
            new_darker_b = darker_color[2] * (1 - darker_blend_amount) + 0.0 * darker_blend_amount
            
            # Assign the new colors based on which was originally lighter
            if fg_is_lighter:
                fg_r, fg_g, fg_b = new_lighter_r, new_lighter_g, new_lighter_b
                bg_r, bg_g, bg_b = new_darker_r, new_darker_g, new_darker_b
            else:
                bg_r, bg_g, bg_b = new_lighter_r, new_lighter_g, new_lighter_b
                fg_r, fg_g, fg_b = new_darker_r, new_darker_g, new_darker_b
        
        # Convert back to hex color strings
        new_fg = rgb_to_hex(fg_r, fg_g, fg_b)
        new_bg = 'bg:' + rgb_to_hex(bg_r, bg_g, bg_b)
        
        # Construct the new style string
        new_parts = other_parts + [new_fg, new_bg]
        new_style_dict[token] = ' '.join(new_parts)
    
    return new_style_dict

def invert_style_string(style_str):
    """Invert colors in a style string"""
    return transform_style_string(style_str, color_invert_transform())


# Code style for Windows consoles. They support only 16 colors,
# so we choose a combination that displays nicely.
win32_code_style = {
    Comment:                   "#00ff00",
    Keyword:                   '#44ff44',
    Number:                    '',
    Operator:                  '',
    String:                    '#ff44ff',

    Name:                      '',
    Name.Decorator:            '#ff4444',
    Name.Class:                '#ff4444',
    Name.Function:             '#ff4444',
    Name.Builtin:              '#ff4444',

    Name.Attribute:            '',
    Name.Constant:             '',
    Name.Entity:               '',
    Name.Exception:            '',
    Name.Label:                '',
    Name.Namespace:            '',
    Name.Tag:                  '',
    Name.Variable:             '',
}
default_ui_style = {
    Token.LineNumber:'#aa6666 bg:#002222',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',
    
    # Indent guides - using explicit fg color, making sure it doesn't inherit from context
    Token.IndentGuide:                            '#303030 noinherit',
    Token.SpecialIndentGuide:                     '#303030 noinherit',
    Token.Whitespace:                             '#252525 noinherit',
    Token.Whitespace.Space:                       '#252525 noinherit',
    Token.Whitespace.Tab:                         '#252525 noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #008800',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#ff0000',
    Token.Out.Number:                             '#ff0000',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#bbbbbb',

    # Search toolbar.
    Token.Toolbar.Search:                         '#22aaaa noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#22aaaa noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#22aaaa noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#44bbbb #000000',
    Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',
    Token.Toolbar.Signature.Operator:             '#000000 bold',

    Token.Docstring:                              '#888888',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',
    Token.Toolbar.Status.Key:                     'bg:#000000 #888888',
    Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#662266 #aaaaaa',
    Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#888888',

    # The options sidebar.
    Token.Sidebar:                                'bg:#bbbbbb #000000',
    Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',
    Token.Sidebar.Label:                          'bg:#bbbbbb #222222',
    Token.Sidebar.Status:                         'bg:#dddddd #000011',
    Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',
    Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',

    Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',
    Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',
    Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',
    Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#008800  #000000',
    Token.History.Line.Current:                  'bg:#ffffff #000000',
    Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',
    Token.History.ExistingInput:                  '#888888',

    # Help Window.
    Token.Window.Border:                          '#0000bb',
    Token.Window.Title:                           'bg:#bbbbbb #000000',
    Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#ffff88 #444444',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#884444 #ffffff',
}

# Some changes to get a bit more contrast on Windows consoles.
# (They only support 16 colors.)
if is_windows() and not is_conemu_ansi():
    default_ui_style.update({
        Token.Sidebar.Title:                          'bg:#00ff00 #ffffff',
        Token.ExitConfirmation:                       'bg:#ff4444 #ffffff',
        Token.Toolbar.Validation:                     'bg:#ff4444 #ffffff',

        Token.Menu.Completions.Completion:            'bg:#ffffff #000000',
        Token.Menu.Completions.Completion.Current:    'bg:#aaaaaa #000000',
    })


blue_ui_style = {}
blue_ui_style.update(default_ui_style)
blue_ui_style.update({
        # Line numbers.
        Token.LineNumber:                             '#aa6666 bg:#222222',

        # Highlighting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#4444aa',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        # Highlighting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#6666aa',

        # Completer toolbar.
        Token.Toolbar.Completions:                    'bg:#44bbbb #000000',
        Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',
        Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',
        Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',

        # Completer menu.
        Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',
        Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',
        Token.Menu.Completions.Meta:                  'bg:#449999 #000000',
        Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',
        Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        Token.Menu.Completions.ProgressButton:        'bg:#000000',
})


# HOW I MADE THE INVERSION THEME:
#THIS CODE AUTOMATICALLY MODIFIES COLORS IN THESE THEMES WHICH LETS ME MAKE NEW THEMES
# code="""{Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #008800',Token.In.Number:                              '',Token.Out:                                    '#ff0000',Token.Out.Number:                             '#ff0000',Token.Separator:                              '#bbbbbb',Token.Toolbar.Search:                         '#22aaaa noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#22aaaa noinherit',Token.Toolbar.Arg:                            '#22aaaa noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#44bbbb #000000',Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',Token.Toolbar.Signature.Operator:             '#000000 bold',Token.Docstring:                              '#888888',Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',Token.Toolbar.Status.Key:                     'bg:#000000 #888888',Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',Token.Aborted:                                '#888888',Token.Sidebar:                                'bg:#bbbbbb #000000',Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',Token.Sidebar.Label:                          'bg:#bbbbbb #222222',Token.Sidebar.Status:                         'bg:#dddddd #000011',Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#008800  #000000',Token.History.Line.Current:                  'bg:#ffffff #000000',Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',Token.History.ExistingInput:                  '#888888',Token.Window.Border:                          '#0000bb',Token.Window.Title:                           'bg:#bbbbbb #000000',Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',Token.AcceptMessage:                          'bg:#ffff88 #444444',Token.ExitConfirmation:                       'bg:#884444 #ffffff',}"""
# def changecolors(colors):
#     return [np.clip((np.roll([x for x in c],1)*2+np.asarray([0,128,255]))//1.5-100,0,255).astype(int) for c in colors]
# def codewithcolors(colors,code=code):
#     x=keys_and_values_to_dict(tocols(allcols(code)),tocols(colors))
#     print(x)
#     return search_replace_simul(code,x)
# def tocols(cols):
#     return [''.join([hex(x)[2:].rjust(2,'0') for x in y]) for y in cols]
# def allcols(code):
#     import re
#     cols=re.findall('#'+r'[\dA-Fa-f]'*6,code)#Colors like 55aaff or 12abfg
#     cols=[x[1:] for x in cols]
#     cols=set(cols)
#     return [[eval('0x'+''.join(x)) for x in split_into_sublists(w,2)] for w in cols]
# colors=allcols(code)
# ans=codewithcolors(changecolors(colors),code)


inverted_3 = {}
inverted_3.update(default_ui_style)
inverted_3.update({
    # Status toolbar.

    # Token.Toolbar.Status:                         'bg:#dddddd #555555',
    # Token.Toolbar.Status.BatteryPluggedIn:        'bg:#dddddd #dd55dd',
    # Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#dddddd #55dddd',
    # Token.Toolbar.Status.Title:                   'underline',
    # Token.Toolbar.Status.InputMode:               'bg:#dddddd #000055',
    # Token.Toolbar.Status.Key:                     'bg:#ffffff #777777',
    # Token.Toolbar.Status.PasteModeOn:             'bg:#55bbbb #000000',
    # Token.Toolbar.Status.PseudoTerminalCurrentVariable:
    #     'bg:#99dd99 #555555',# RYAN BURGERT STUFF
    # Token.Toolbar.Status.PythonVersion:           'bg:#dddddd #000000 bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#777777',

    # The options sidebar.
    Token.Sidebar:                                'bg:#444444 #ffffff',
    Token.Sidebar.Title:                          'bg:#997700 #000000 bold',
    Token.Sidebar.Label:                          'bg:#444444 #dddddd',
    Token.Sidebar.Status:                         'bg:#222222 #ffffee',
    Token.Sidebar.Selected.Label:                 'bg:#dddddd #111111',
    Token.Sidebar.Selected.Status:                'bg:#bbbbbb #000000 bold',

    Token.Sidebar.Separator:                       'bg:#444444 #000000 underline',
    Token.Sidebar.Key:                            'bg:#442244 #ffffff bold',
    Token.Sidebar.Key.Description:                'bg:#444444 #ffffff',
    Token.Sidebar.HelpText:                       'bg:#111100 #ffffee',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#ff77ff  #ffffff',
    Token.History.Line.Current:                  'bg:#000000 #ffffff',
    Token.History.Line.Selected.Current:         'bg:#770077 #ffffff',
    Token.History.ExistingInput:                  '#777777',

    # Help Window.
    Token.Window.Border:                          '#ffff44',
    Token.Window.Title:                           'bg:#444444 #ffffff',
    Token.Window.TIItleV2:                         'bg:#997744 #ffffff bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#000077 #bbbbbb',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#77bbbb #000000',
})

inverted_3.update({
        # Line numbers.
        Token.LineNumber:                             '#aa6666 bg:#222222',

        # Highlighting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#4444aa',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        # Highlighting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#6666aa',

        # # Completer toolbar.
        # Token.Toolbar.Completions:                    'bg:#44bbbb #000000',
        # Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',
        # Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',
        # Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',

        # # Completer menu.
        # Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',
        # Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',
        # Token.Menu.Completions.Meta:                  'bg:#449999 #000000',
        # Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',
        # Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        # Token.Menu.Completions.ProgressButton:        'bg:#000000',



                Token.Toolbar.Completions:            'bg:#000046 #bf954c',
        Token.Toolbar.Completions.Arrow:              'bg:#000046 #bf954c bold',
        Token.Toolbar.Completions.Completion:         'bg:#000046 #bf954c',
        Token.Toolbar.Completions.Completion.Current: 'bg:#f0ffff #6a5100',



        # Completer menu.
        Token.Menu.Completions.Completion:            'bg:#202046 #ff954c',
        Token.Menu.Completions.Completion.Current:    'bg:#ff954c #202046',
        Token.Menu.Completions.Meta:                  'bg:#000046 #ff684c',
        Token.Menu.Completions.Meta.Current:          'bg:#000046 #ff7e00',
        Token.Menu.Completions.ProgressBar:           'bg:#ff7ed4           ',
        Token.Menu.Completions.ProgressButton:        'bg:#460000           ',
})




stars_2 = {}
stars_2.update(default_ui_style)
stars_2.update({
    # Status toolbar.

    # Token.Toolbar.Status:                         'bg:#dddddd #555555',
    # Token.Toolbar.Status.BatteryPluggedIn:        'bg:#dddddd #dd55dd',
    # Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#dddddd #55dddd',
    # Token.Toolbar.Status.Title:                   'underline',
    # Token.Toolbar.Status.InputMode:               'bg:#dddddd #000055',
    # Token.Toolbar.Status.Key:                     'bg:#ffffff #777777',
    # Token.Toolbar.Status.PasteModeOn:             'bg:#55bbbb #000000',
    # Token.Toolbar.Status.PseudoTerminalCurrentVariable:
    #     'bg:#99dd99 #555555',# RYAN BURGERT STUFF
    # Token.Toolbar.Status.PythonVersion:           'bg:#dddddd #000000 bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#777777',

    # The options sidebar.
    Token.Sidebar:                                'bg:#444444 #ffffff',
    Token.Sidebar.Title:                          'bg:#007799 #000000 bold',
    Token.Sidebar.Label:                          'bg:#444444 #dddddd',
    Token.Sidebar.Status:                         'bg:#222222 #eeffff',
    Token.Sidebar.Selected.Label:                 'bg:#dddddd #111111',
    Token.Sidebar.Selected.Status:                'bg:#bbbbbb #000000 bold',

    Token.Sidebar.Separator:                       'bg:#444444 #000000 underline',
    Token.Sidebar.Key:                            'bg:#442244 #ffffff bold',
    Token.Sidebar.Key.Description:                'bg:#444444 #ffffff',
    Token.Sidebar.HelpText:                       'bg:#001111 #eeffff',

    #lili Sng for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#ff77ff  #ffffff',
    Token.History.Line.Current:                  'bg:#000000 #ffffff',
    Token.History.Line.Selected.Current:         'bg:#770077 #ffffff',
    Token.History.ExistingInput:                  '#777777',

    #plp  HWindow.
    Token.Window.Border:                          '#ffff44',
    Token.Window.Title:                           'bg:#444444 #ffffff',
    Token.Window.TIItleV2:                         'bg:#447799 #ffffff bold',

    #ata- Menter message.
    Token.AcceptMessage:                          'bg:#770000 #bbbbbb',

    #tit  Econfirmation.
    Token.ExitConfirmation:                       'bg:#bbbb77 #000000',
})

stars_2.update({
        #ene  Lnumbers.
        Token.LineNumber:                             '#aa6666 bg:#222222',

        #hlhl Highting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#aa4444',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        #hlhl Highting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#aa6666',

        # C  ##pl Ceter toolbar.
        #enen T.Toolbar.Completions:                    'bg:#bbbb44 #000000',
        #enen T.Toolbar.Completions.Arrow:              'bg:#bbbb44 #000000 bold',
        #enen T.Toolbar.Completions.Completion:         'bg:#bbbb44 #000000',
        #enen T.Toolbar.Completions.Completion.Current: 'bg:#888800 #ffffff',

        # C  ##pl Ceter menu.
        #enen T.Menu.Completions.Completion:            'bg:#bbbb44 #000000',
        #enen T.Menu.Completions.Completion.Current:    'bg:#888800 #ffffff',
        #enen T.Menu.Completions.Meta:                  'bg:#999944 #000000',
        #enen T.Menu.Completions.Meta.Current:          'bg:#aaaa00 #000000',
        #enen T.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        #enen T.Menu.Completions.ProgressButton:        'bg:#000000',



                Token.Toolbar.Completions:            'bg:#460000 #4c95bf',
        Token.Toolbar.Completions.Arrow:              'bg:#460000 #4c95bf bold',
        Token.Toolbar.Completions.Completion:         'bg:#460000 #4c95bf',
        Token.Toolbar.Completions.Completion.Current: 'bg:#fffff0 #00516a',



        #plpl Ceter menu.
        Token.Menu.Completions.Completion:            'bg:#462020 #4c95ff',
        Token.Menu.Completions.Completion.Current:    'bg:#4c95ff #462020',
        Token.Menu.Completions.Meta:                  'bg:#460000 #4c68ff',
        Token.Menu.Completions.Meta.Current:          'bg:#460000 #007eff',
        Token.Menu.Completions.ProgressBar:           'bg:#d47eff           ',
        Token.Menu.Completions.ProgressButton:        'bg:#000046           ',
})





color_1={    Token.LineNumber:'#d47623 bg:#397300',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #7dfb00',    Token.In.Number:                              '',    Token.Out:                                    '#ff0039',    Token.Out.Number:                             '#ff0039',    Token.Separator:                              '#ffdf94',    Token.Toolbar.Search:                         '#2eff1e noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#2eff1e noinherit',    Token.Toolbar.Arg:                            '#2eff1e noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#5cff4c #234600',    Token.Toolbar.Signature.CurrentName:          'bg:#2cfb00 #fff7f0 bold',    Token.Toolbar.Signature.Operator:             '#234600 bold',    Token.Docstring:                              '#fbfb51',    Token.Toolbar.Validation:                     'bg:#4c2000 #ffe97e',    Token.Toolbar.Status:                         'bg:#577300 #ffe97e',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#577300 #9dff00',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#577300 #d40900',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#577300 #ffbe7e',    Token.Toolbar.Status.Key:                     'bg:#234600 #fbfb51',    Token.Toolbar.Status.PasteModeOn:             'bg:#d43500 #fff7f0',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#794824 #ffe97e',    Token.Toolbar.Status.PythonVersion:           'bg:#577300 #fff7f0 bold',    Token.Aborted:                                '#fbfb51',    Token.Sidebar:                                'bg:#ffdf94 #234600',    Token.Sidebar.Title:                          'bg:#79fbaf #444488 bold',    Token.Sidebar.Label:                          'bg:#ffdf94 #577300',    Token.Sidebar.Status:                         'bg:#ffe0c2 #234600',    Token.Sidebar.Selected.Label:                 'bg:#577300 #ffecd9',    Token.Sidebar.Selected.Status:                'bg:#9ba000 #fff7f0 bold',    Token.Sidebar.Separator:                       'bg:#ffdf94 #fff7f0 underline',    Token.Sidebar.Key:                            'bg:#ffdf94 #234600 bold',    Token.Sidebar.Key.Description:                'bg:#ffdf94 #234600',    Token.Sidebar.HelpText:                       'bg:#fff7f0 #234600',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#7dfb00  #234600',    Token.History.Line.Current:                  'bg:#fff7f0 #234600',    Token.History.Line.Selected.Current:         'bg:#fdff51 #234600',    Token.History.ExistingInput:                  '#fbfb51',    Token.Window.Border:                          '#009095',    Token.Window.Title:                           'bg:#ffdf94 #234600',    Token.Window.TIItleV2:                         'bg:#9dfb79 #234600 bold',    Token.AcceptMessage:                          'bg:#ffa851 #9ba000',    Token.ExitConfirmation:                       'bg:#a64c00 #fff7f0',    Token.LineNumber:                             '#d47623 bg:#577300',        Token.SearchMatch:                            '#fff7f0 bg:#4ca053',        Token.SearchMatch.Current:                    '#fff7f0 bg:#cbff00',        Token.SelectedText:                           '#fff7f0 bg:#9ece78',        Token.Toolbar.Completions:                    'bg:#5cff4c #234600',        Token.Toolbar.Completions.Arrow:              'bg:#5cff4c #234600 bold',        Token.Toolbar.Completions.Completion:         'bg:#5cff4c #234600',        Token.Toolbar.Completions.Completion.Current: 'bg:#2cfb00 #000000',        Token.Menu.Completions.Completion:            'bg:#5cff4c #234600',        Token.Menu.Completions.Completion.Current:    'bg:#2c8b00 #ffffff',        Token.Menu.Completions.Meta:                  'bg:#89ff4c #234600',        Token.Menu.Completions.Meta.Current:          'bg:#01ff00 #234600',        Token.Menu.Completions.ProgressBar:           'bg:#ffe97e',        Token.Menu.Completions.ProgressButton:        'bg:#234600',}
color_2={    Token.LineNumber:'#1a1ea2 bg:#410040',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #c900c8',    Token.In.Number:                              '',    Token.Out:                                    '#0094cd',    Token.Out.Number:                             '#0094cd',    Token.Separator:                              '#8876cd',    Token.Toolbar.Search:                         '#cd187f noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#cd187f noinherit',    Token.Toolbar.Arg:                            '#cd187f noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#cd3d91 #140014',    Token.Toolbar.Signature.CurrentName:          'bg:#c90087 #c0c1cd bold',    Token.Toolbar.Signature.Operator:             '#140014 bold',    Token.Docstring:                              '#8440c9',    Token.Toolbar.Validation:                     'bg:#00021a #8765cd',    Token.Toolbar.Status:                         'bg:#300041 #8765cd',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#300041 #b500cd',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#300041 #004aa2',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#300041 #6565cd',    Token.Toolbar.Status.Key:                     'bg:#140014 #8440c9',    Token.Toolbar.Status.PasteModeOn:             'bg:#0028a2 #c0c1cd',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#151847 #8765cd',    Token.Toolbar.Status.PythonVersion:           'bg:#300041 #c0c1cd bold',    Token.Aborted:                                '#8440c9',    Token.Sidebar:                                'bg:#8876cd #140014',    Token.Sidebar.Title:                          'bg:#c96069 #c0c1cd bold',    Token.Sidebar.Label:                          'bg:#8876cd #300041',    Token.Sidebar.Status:                         'bg:#9b9ccd #140014',    Token.Sidebar.Selected.Label:                 'bg:#300041 #aeaecd',    Token.Sidebar.Selected.Status:                'bg:#3a006e #c0c1cd bold',    Token.Sidebar.Separator:                       'bg:#8876cd #c0c1cd underline',    Token.Sidebar.Key:                            'bg:#8876cd #140014 bold',    Token.Sidebar.Key.Description:                'bg:#8876cd #140014',    Token.Sidebar.HelpText:                       'bg:#c0c1cd #140014',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#c900c8  #140014',    Token.History.Line.Current:                  'bg:#c0c1cd #140014',    Token.History.Line.Selected.Current:         'bg:#8841cd #140014',    Token.History.ExistingInput:                  '#8440c9',    Token.Window.Border:                          '#633400',    Token.Window.Title:                           'bg:#8876cd #140014',    Token.Window.TIItleV2:                         'bg:#c960b1 #140014 bold',    Token.AcceptMessage:                          'bg:#4141cd #3a006e',    Token.ExitConfirmation:                       'bg:#000474 #c0c1cd',    Token.LineNumber:                             '#1a1ea2 bg:#300041',        Token.SearchMatch:                            '#c0c1cd bg:#6e344c',        Token.SearchMatch.Current:                    '#c0c1cd bg:#9000cd',        Token.SelectedText:                           '#c0c1cd bg:#9c5a98',        Token.Toolbar.Completions:                    'bg:#cd3d91 #140014',        Token.Toolbar.Completions.Arrow:              'bg:#cd3d91 #140014 bold',        Token.Toolbar.Completions.Completion:         'bg:#cd3d91 #140014',        Token.Toolbar.Completions.Completion.Current: 'bg:#c90087 #c0c1cd',        Token.Menu.Completions.Completion:            'bg:#cd3d91 #140014',        Token.Menu.Completions.Completion.Current:    'bg:#c90087 #c0c1cd',        Token.Menu.Completions.Meta:                  'bg:#cd3db6 #140014',        Token.Menu.Completions.Meta.Current:          'bg:#cd0067 #140014',        Token.Menu.Completions.ProgressBar:           'bg:#8765cd',        Token.Menu.Completions.ProgressButton:        'bg:#140014',}
color_3={    Token.LineNumber:'#5ea28b bg:#202941',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #6482c9',    Token.In.Number:                              '',    Token.Out:                                    '#68cd66',    Token.Out.Number:                             '#68cd66',    Token.Separator:                              '#a1cdc8',    Token.Toolbar.Search:                         '#7e72cd noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#7e72cd noinherit',    Token.Toolbar.Arg:                            '#7e72cd noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#8d85cd #0a0c14',    Token.Toolbar.Signature.CurrentName:          'bg:#6764c9 #c6cdca bold',    Token.Toolbar.Signature.Operator:             '#0a0c14 bold',    Token.Docstring:                              '#84bbc9',    Token.Toolbar.Validation:                     'bg:#0d1a15 #99cbcd',    Token.Toolbar.Status:                         'bg:#203241 #99cbcd',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#203241 #6691cd',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#203241 #51a264',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#203241 #99cdbd',    Token.Toolbar.Status.Key:                     'bg:#0a0c14 #84bbc9',    Token.Toolbar.Status.PasteModeOn:             'bg:#51a275 #c6cdca',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#2e473e #99cbcd',    Token.Toolbar.Status.PythonVersion:           'bg:#203241 #c6cdca bold',    Token.Aborted:                                '#84bbc9',    Token.Sidebar:                                'bg:#a1cdc8 #0a0c14',    Token.Sidebar.Title:                          'bg:#b494c9 #c6cdca bold',    Token.Sidebar.Label:                          'bg:#a1cdc8 #203241',    Token.Sidebar.Status:                         'bg:#b4cdc5 #0a0c14',    Token.Sidebar.Selected.Label:                 'bg:#203241 #bdcdc8',    Token.Sidebar.Selected.Status:                'bg:#37616e #c6cdca bold',    Token.Sidebar.Separator:                       'bg:#a1cdc8 #c6cdca underline',    Token.Sidebar.Key:                            'bg:#a1cdc8 #0a0c14 bold',    Token.Sidebar.Key.Description:                'bg:#a1cdc8 #0a0c14',    Token.Sidebar.HelpText:                       'bg:#c6cdca #0a0c14',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#6482c9  #0a0c14',    Token.History.Line.Current:                  'bg:#c6cdca #0a0c14',    Token.History.Line.Selected.Current:         'bg:#86becd #0a0c14',    Token.History.ExistingInput:                  '#84bbc9',    Token.Window.Border:                          '#633157',    Token.Window.Title:                           'bg:#a1cdc8 #0a0c14',    Token.Window.TIItleV2:                         'bg:#9498c9 #0a0c14 bold',    Token.AcceptMessage:                          'bg:#86cdb8 #37616e',    Token.ExitConfirmation:                       'bg:#3a7460 #c6cdca',    Token.LineNumber:                             '#5ea28b bg:#203241',        Token.SearchMatch:                            '#c6cdca bg:#59516e',        Token.SearchMatch.Current:                    '#c6cdca bg:#66a3cd',        Token.SelectedText:                           '#c6cdca bg:#7b829c',        Token.Toolbar.Completions:                    'bg:#8d85cd #0a0c14',        Token.Toolbar.Completions.Arrow:              'bg:#8d85cd #0a0c14 bold',        Token.Toolbar.Completions.Completion:         'bg:#8d85cd #0a0c14',        Token.Toolbar.Completions.Completion.Current: 'bg:#6764c9 #c6cdca',        Token.Menu.Completions.Completion:            'bg:#8d85cd #0a0c14',        Token.Menu.Completions.Completion.Current:    'bg:#6764c9 #c6cdca',        Token.Menu.Completions.Meta:                  'bg:#858fcd #0a0c14',        Token.Menu.Completions.Meta.Current:          'bg:#7a66cd #0a0c14',        Token.Menu.Completions.ProgressBar:           'bg:#99cbcd',        Token.Menu.Completions.ProgressButton:        'bg:#0a0c14',}

pupper= {    Token.LineNumber:'#23d452 bg:#005073',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #00affb',    Token.In.Number:                              '',    Token.Out:                                    '#6cff00',    Token.Out.Number:                             '#6cff00',    Token.Separator:                              '#94ffc9',    Token.Toolbar.Search:                         '#1e5bff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#1e5bff noinherit',    Token.Toolbar.Arg:                            '#1e5bff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#4c80ff #003046',    Token.Toolbar.Signature.CurrentName:          'bg:#005efb #f0fff4 bold',    Token.Toolbar.Signature.Operator:             '#003046 bold',    Token.Docstring:                              '#51fbd8',    Token.Toolbar.Validation:                     'bg:#004c10 #7effcf',    Token.Toolbar.Status:                         'bg:#006e73 #7effcf',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#006e73 #00d0ff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#006e73 #21d400',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#006e73 #7effa4',    Token.Toolbar.Status.Key:                     'bg:#003046 #51fbd8',    Token.Toolbar.Status.PasteModeOn:             'bg:#00d40b #f0fff4',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247937 #7effcf',    Token.Toolbar.Status.PythonVersion:           'bg:#006e73 #f0fff4 bold',    Token.Aborted:                                '#51fbd8',    Token.Sidebar:                                'bg:#94ffc9 #003046',    Token.Sidebar.Title:                          'bg:#9479fb #f0fff4 bold',    Token.Sidebar.Label:                          'bg:#94ffc9 #006e73',    Token.Sidebar.Status:                         'bg:#c2ffd4 #003046',    Token.Sidebar.Selected.Label:                 'bg:#006e73 #d9ffe4',    Token.Sidebar.Selected.Status:                'bg:#00a084 #f0fff4 bold',    Token.Sidebar.Separator:                       'bg:#94ffc9 #f0fff4 underline',    Token.Sidebar.Key:                            'bg:#94ffc9 #003046 bold',    Token.Sidebar.Key.Description:                'bg:#94ffc9 #003046',    Token.Sidebar.HelpText:                       'bg:#f0fff4 #003046',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#00affb  #003046',    Token.History.Line.Current:                  'bg:#f0fff4 #003046',    Token.History.Line.Selected.Current:         'bg:#51ffde #003046',    Token.History.ExistingInput:                  '#51fbd8',    Token.Window.Border:                          '#7b0095',    Token.Window.Title:                           'bg:#94ffc9 #003046',    Token.Window.TIItleV2:                         'bg:#79b8fb #003046 bold',    Token.AcceptMessage:                          'bg:#51ff85 #00a084',    Token.ExitConfirmation:                       'bg:#00a62b #f0fff4',    Token.LineNumber:                             '#23d452 bg:#006e73',        Token.SearchMatch:                            '#f0fff4 bg:#4c54a0',        Token.SearchMatch.Current:                    '#f0fff4 bg:#00feff',        Token.SelectedText:                           '#f0fff4 bg:#78afce',        Token.Toolbar.Completions:                    'bg:#4c80ff #003046',        Token.Toolbar.Completions.Arrow:              'bg:#4c80ff #003046 bold',        Token.Toolbar.Completions.Completion:         'bg:#4c80ff #003046',        Token.Toolbar.Completions.Completion.Current: 'bg:#005efb #f0fff4',        Token.Menu.Completions.Completion:            'bg:#4c80ff #003046',        Token.Menu.Completions.Completion.Current:    'bg:#005efb #f0fff4',        Token.Menu.Completions.Meta:                  'bg:#4cadff #003046',        Token.Menu.Completions.Meta.Current:          'bg:#0034ff #003046',        Token.Menu.Completions.ProgressBar:           'bg:#7effcf',        Token.Menu.Completions.ProgressButton:        'bg:#003046',}
clara=  {    Token.LineNumber:'#7bced4 bg:#3f3973',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #8a7dfb',    Token.In.Number:                              '',    Token.Out:                                    '#7fffaf',    Token.Out.Number:                             '#7fffaf',    Token.Separator:                              '#c9efff',    Token.Toolbar.Search:                         '#ca8eff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#ca8eff noinherit',    Token.Toolbar.Arg:                            '#ca8eff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#d3a5ff #262346',    Token.Toolbar.Signature.CurrentName:          'bg:#b27dfb #f7feff bold',    Token.Toolbar.Signature.Operator:             '#262346 bold',    Token.Docstring:                              '#a6c8fb',    Token.Toolbar.Validation:                     'bg:#264b4c #bee3ff',    Token.Toolbar.Status:                         'bg:#394273 #bee3ff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#394273 #7f81ff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#394273 #6ad4ae',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#394273 #bef8ff',    Token.Toolbar.Status.Key:                     'bg:#262346 #a6c8fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#6ad4c4 #f7feff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#4e7879 #bee3ff',    Token.Toolbar.Status.PythonVersion:           'bg:#394273 #f7feff bold',    Token.Aborted:                                '#a6c8fb',    Token.Sidebar:                                'bg:#c9efff #262346',    Token.Sidebar.Title:                          'bg:#fbbafa #f7feff bold',    Token.Sidebar.Label:                          'bg:#c9efff #394273',    Token.Sidebar.Status:                         'bg:#e0fcff #262346',    Token.Sidebar.Selected.Label:                 'bg:#394273 #ecfdff',    Token.Sidebar.Selected.Status:                'bg:#506da0 #f7feff bold',    Token.Sidebar.Separator:                       'bg:#c9efff #f7feff underline',    Token.Sidebar.Key:                            'bg:#c9efff #262346 bold',    Token.Sidebar.Key.Description:                'bg:#c9efff #262346',    Token.Sidebar.HelpText:                       'bg:#f7feff #262346',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#8a7dfb  #262346',    Token.History.Line.Current:                  'bg:#f7feff #262346',    Token.History.Line.Selected.Current:         'bg:#a8c9ff #262346',    Token.History.ExistingInput:                  '#a6c8fb',    Token.Window.Border:                          '#954a66',    Token.Window.Title:                           'bg:#c9efff #262346',    Token.Window.TIItleV2:                         'bg:#cebafb #262346 bold',    Token.AcceptMessage:                          'bg:#a8f6ff #506da0',    Token.ExitConfirmation:                       'bg:#53a1a6 #f7feff',    Token.LineNumber:                             '#7bced4 bg:#394273',        Token.SearchMatch:                            '#f7feff bg:#9376a0',        Token.SearchMatch.Current:                    '#f7feff bg:#7f98ff',        Token.SelectedText:                           '#f7feff bg:#a9a3ce',        Token.Toolbar.Completions:                    'bg:#d3a5ff #262346',        Token.Toolbar.Completions.Arrow:              'bg:#d3a5ff #262346 bold',        Token.Toolbar.Completions.Completion:         'bg:#d3a5ff #262346',        Token.Toolbar.Completions.Completion.Current: 'bg:#b27dfb #f7feff',        Token.Menu.Completions.Completion:            'bg:#d3a5ff #262346',        Token.Menu.Completions.Completion.Current:    'bg:#b27dfb #f7feff',        Token.Menu.Completions.Meta:                  'bg:#bca5ff #262346',        Token.Menu.Completions.Meta.Current:          'bg:#cb7fff #262346',        Token.Menu.Completions.ProgressBar:           'bg:#bee3ff',        Token.Menu.Completions.ProgressButton:        'bg:#262346',}
emma=   {    Token.LineNumber:'#7b86d4 bg:#6d3973',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #ee7dfb',    Token.In.Number:                              '',    Token.Out:                                    '#7fe8ff',    Token.Out.Number:                             '#7fe8ff',    Token.Separator:                              '#cec9ff',    Token.Toolbar.Search:                         '#ff8ed9 noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#ff8ed9 noinherit',    Token.Toolbar.Arg:                            '#ff8ed9 noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#ffa4e3 #412346',    Token.Toolbar.Signature.CurrentName:          'bg:#fb7ddf #f7f7ff bold',    Token.Toolbar.Signature.Operator:             '#412346 bold',    Token.Docstring:                              '#c8a6fb',    Token.Toolbar.Validation:                     'bg:#262c4c #cdbeff',    Token.Toolbar.Status:                         'bg:#5e3973 #cdbeff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#5e3973 #e37fff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#5e3973 #6aa5d4',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#5e3973 #bec4ff',    Token.Toolbar.Status.Key:                     'bg:#412346 #c8a6fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#6a8fd4 #f7f7ff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#4e5579 #cdbeff',    Token.Toolbar.Status.PythonVersion:           'bg:#5e3973 #f7f7ff bold',    Token.Aborted:                                '#c8a6fb',    Token.Sidebar:                                'bg:#cec9ff #412346',    Token.Sidebar.Title:                          'bg:#fbbac6 #f7f7ff bold',    Token.Sidebar.Label:                          'bg:#cec9ff #5e3973',    Token.Sidebar.Status:                         'bg:#e0e3ff #412346',    Token.Sidebar.Selected.Label:                 'bg:#5e3973 #ecedff',    Token.Sidebar.Selected.Status:                'bg:#7350a0 #f7f7ff bold',    Token.Sidebar.Separator:                       'bg:#cec9ff #f7f7ff underline',    Token.Sidebar.Key:                            'bg:#cec9ff #412346 bold',    Token.Sidebar.Key.Description:                'bg:#cec9ff #412346',    Token.Sidebar.HelpText:                       'bg:#f7f7ff #412346',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#ee7dfb  #412346',    Token.History.Line.Current:                  'bg:#f7f7ff #412346',    Token.History.Line.Selected.Current:         'bg:#cca8ff #412346',    Token.History.ExistingInput:                  '#c8a6fb',    Token.Window.Border:                          '#956a49',    Token.Window.Title:                           'bg:#cec9ff #412346',    Token.Window.TIItleV2:                         'bg:#fbbaf4 #412346 bold',    Token.AcceptMessage:                          'bg:#a8b0ff #7350a0',    Token.ExitConfirmation:                       'bg:#535ea6 #f7f7ff',    Token.LineNumber:                             '#7b86d4 bg:#5e3973',        Token.SearchMatch:                            '#f7f7ff bg:#a0768b',        Token.SearchMatch.Current:                    '#f7f7ff bg:#cc7fff',        Token.SelectedText:                           '#f7f7ff bg:#cba3ce',        Token.Toolbar.Completions:                    'bg:#ffa4e3 #412346',        Token.Toolbar.Completions.Arrow:              'bg:#ffa4e3 #412346 bold',        Token.Toolbar.Completions.Completion:         'bg:#ffa4e3 #412346',        Token.Toolbar.Completions.Completion.Current: 'bg:#fb7ddf #f7f7ff',        Token.Menu.Completions.Completion:            'bg:#ffa4e3 #412346',        Token.Menu.Completions.Completion.Current:    'bg:#412346 #ffa4e3',        Token.Menu.Completions.Meta:                  'bg:#ffa4fa #412346',        Token.Menu.Completions.Meta.Current:          'bg:#ff7fcc #412346',        Token.Menu.Completions.ProgressBar:           'bg:#cdbeff',        Token.Menu.Completions.ProgressButton:        'bg:#412346',}

base=   {    Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #008800',    Token.In.Number:                              '',    Token.Out:                                    '#ff0000',    Token.Out.Number:                             '#ff0000',    Token.Separator:                              '#bbbbbb',    Token.Toolbar.Search:                         '#22aaaa noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#22aaaa noinherit',    Token.Toolbar.Arg:                            '#22aaaa noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#44bbbb #000000',    Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',    Token.Toolbar.Signature.Operator:             '#000000 bold',    Token.Docstring:                              '#888888',    Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',    Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',    Token.Toolbar.Status.Key:                     'bg:#000000 #888888',    Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',    Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',    Token.Aborted:                                '#888888',    Token.Sidebar:                                'bg:#bbbbbb #000000',    Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',    Token.Sidebar.Label:                          'bg:#bbbbbb #222222',    Token.Sidebar.Status:                         'bg:#dddddd #000011',    Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',    Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',    Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',    Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',    Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',    Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#008800  #000000',    Token.History.Line.Current:                  'bg:#ffffff #000000',    Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',    Token.History.ExistingInput:                  '#888888',    Token.Window.Border:                          '#0000bb',    Token.Window.Title:                           'bg:#bbbbbb #000000',    Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',    Token.AcceptMessage:                          'bg:#ffff88 #444444',    Token.ExitConfirmation:                       'bg:#884444 #ffffff',    Token.LineNumber:                             '#aa6666 bg:#222222',        Token.SearchMatch:                            '#ffffff bg:#4444aa',        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',        Token.SelectedText:                           '#ffffff bg:#6666aa',        Token.Toolbar.Completions:                    'bg:#44bbbb #000000',        Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',        Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',        Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',        Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',        Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',        Token.Menu.Completions.Meta:                  'bg:#449999 #000000',        Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',        Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',        Token.Menu.Completions.ProgressButton:        'bg:#000000',}

inverted_1= {Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #008800',Token.In.Number:                              '',Token.Out:                                    '#ff0000',Token.Out.Number:                             '#ff0000',Token.Separator:                              '#bbbbbb',Token.Toolbar.Search:                         '#22aaaa noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#22aaaa noinherit',Token.Toolbar.Arg:                            '#22aaaa noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#44bbbb #000000',Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',Token.Toolbar.Signature.Operator:             '#000000 bold',Token.Docstring:                              '#888888',Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',Token.Toolbar.Status.Key:                     'bg:#000000 #888888',Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',Token.Aborted:                                '#888888',Token.Sidebar:                                'bg:#bbbbbb #000000',Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',Token.Sidebar.Label:                          'bg:#bbbbbb #222222',Token.Sidebar.Status:                         'bg:#dddddd #000011',Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#008800  #000000',Token.History.Line.Current:                  'bg:#ffffff #000000',Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',Token.History.ExistingInput:                  '#888888',Token.Window.Border:                          '#0000bb',Token.Window.Title:                           'bg:#bbbbbb #000000',Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',Token.AcceptMessage:                          'bg:#ffff88 #444444',Token.ExitConfirmation:                       'bg:#884444 #ffffff',}
inverted_2 ={Token.LineNumber:'#999955 bg:#ddddff',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #77ffff',Token.In.Number:                              '',Token.Out:                                    '#ffff00',Token.Out.Number:                             '#ffff00',Token.Separator:                              '#444444',Token.Toolbar.Search:                         '#5555dd noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#5555dd noinherit',Token.Toolbar.Arg:                            '#5555dd noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#4444bb #ffffff',Token.Toolbar.Signature.CurrentName:          'bg:#7777ff #000000 bold',Token.Toolbar.Signature.Operator:             '#ffffff bold',Token.Docstring:                              '#777777',Token.Toolbar.Validation:                     'bg:#ffffbb #555555',Token.Toolbar.Status:                         'bg:#dddddd #555555',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#dddddd #55dddd',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#dddddd #dddd55',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#dddddd #005500',Token.Toolbar.Status.Key:                     'bg:#ffffff #777777',Token.Toolbar.Status.PasteModeOn:             'bg:#bbbb55 #000000',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#dd9999 #555555',Token.Toolbar.Status.PythonVersion:           'bg:#dddddd #000000 bold',Token.Aborted:                                '#777777',Token.Sidebar:                                'bg:#444444 #ffffff',Token.Sidebar.Title:                          'bg:#770099 #ffffff bold',Token.Sidebar.Label:                          'bg:#444444 #dddddd',Token.Sidebar.Status:                         'bg:#222222 #ffeeff',Token.Sidebar.Selected.Label:                 'bg:#dddddd #111111',Token.Sidebar.Selected.Status:                'bg:#bbbbbb #000000 bold',Token.Sidebar.Separator:                       'bg:#444444 #000000 underline',Token.Sidebar.Key:                            'bg:#224444 #ffffff bold',Token.Sidebar.Key.Description:                'bg:#444444 #ffffff',Token.Sidebar.HelpText:                       'bg:#110011 #ffeeff',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#77ffff  #ffffff',Token.History.Line.Current:                  'bg:#000000 #ffffff',Token.History.Line.Selected.Current:         'bg:#007777 #ffffff',Token.History.ExistingInput:                  '#777777',Token.Window.Border:                          '#ff44ff',Token.Window.Title:                           'bg:#444444 #ffffff',Token.Window.TIItleV2:                         'bg:#774499 #ffffff bold',Token.AcceptMessage:                          'bg:#007700 #bbbbbb',Token.ExitConfirmation:                       'bg:#bbbb77 #000000',}

cyan = {Token.LineNumber:'#6663bb bg:#93d4e8',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #aad4a4',Token.In.Number:                              '',Token.Out:                                    '#aa2aff',Token.Out.Number:                             '#aa2aff',Token.Separator:                              '#2d5882',Token.Toolbar.Search:                         '#38be8d noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#38be8d noinherit',Token.Toolbar.Arg:                            '#38be8d noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#2da782 #aad4ff',Token.Toolbar.Signature.CurrentName:          'bg:#4fd4a4 #002a55 bold',Token.Toolbar.Signature.Operator:             '#aad4ff bold',Token.Docstring:                              '#4f7aa4',Token.Toolbar.Validation:                     'bg:#aaa7ff #38638d',Token.Toolbar.Status:                         'bg:#93bee8 #38638d',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#93bee8 #93be8d',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#93bee8 #9363e8',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#93bee8 #382a55',Token.Toolbar.Status.Key:                     'bg:#aad4ff #4f7aa4',Token.Toolbar.Status.PasteModeOn:             'bg:#7c63d1 #002a55',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#6690e8 #38638d',Token.Toolbar.Status.PythonVersion:           'bg:#93bee8 #002a55 bold',Token.Aborted:                                '#4f7aa4',Token.Sidebar:                                'bg:#2d5882 #aad4ff',Token.Sidebar.Title:                          'bg:#0090a4 #002a55 bold',Token.Sidebar.Label:                          'bg:#2d5882 #93bee8',Token.Sidebar.Status:                         'bg:#16416b #9ed4ff',Token.Sidebar.Selected.Label:                 'bg:#93bee8 #0b3660',Token.Sidebar.Selected.Status:                'bg:#7ca7d1 #002a55 bold',Token.Sidebar.Separator:                       'bg:#2d5882 #002a55 underline',Token.Sidebar.Key:                            'bg:#2d586b #aad4ff bold',Token.Sidebar.Key.Description:                'bg:#2d5882 #aad4ff',Token.Sidebar.HelpText:                       'bg:#003660 #9ed4ff',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#aad4a4  #aad4ff',Token.History.Line.Current:                  'bg:#002a55 #aad4ff',Token.History.Line.Selected.Current:         'bg:#4f7a55 #aad4ff',Token.History.ExistingInput:                  '#4f7aa4',Token.Window.Border:                          '#2dd4ff',Token.Window.Title:                           'bg:#2d5882 #aad4ff',Token.Window.TIItleV2:                         'bg:#2d90a4 #aad4ff bold',Token.AcceptMessage:                          'bg:#4f2a55 #7ca7d1',Token.ExitConfirmation:                       'bg:#7c7ad1 #002a55',}
cyan_2={Token.LineNumber:'#51bbb7 bg:#1b3381',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #0033d2',Token.In.Number:                              '',Token.Out:                                    '#00ff66',Token.Out.Number:                             '#00ff66',Token.Separator:                              '#95c8fb',Token.Toolbar.Search:                         '#884eee noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#884eee noinherit',Token.Toolbar.Arg:                            '#884eee noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#9569fb #003366',Token.Toolbar.Signature.CurrentName:          'bg:#6c33d2 #ccffff bold',Token.Toolbar.Signature.Operator:             '#003366 bold',Token.Docstring:                              '#6ca0d2',Token.Toolbar.Validation:                     'bg:#006966 #88bbee',Token.Toolbar.Status:                         'bg:#1b4e81 #88bbee',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#1b4e81 #1b4eee',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#1b4e81 #1bbb81',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#1b4e81 #88ffff',Token.Toolbar.Status.Key:                     'bg:#003366 #6ca0d2',Token.Toolbar.Status.PasteModeOn:             'bg:#36bb9c #ccffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#518481 #88bbee',Token.Toolbar.Status.PythonVersion:           'bg:#1b4e81 #ccffff bold',Token.Aborted:                                '#6ca0d2',Token.Sidebar:                                'bg:#95c8fb #003366',Token.Sidebar.Title:                          'bg:#cc84d2 #ccffff bold',Token.Sidebar.Label:                          'bg:#95c8fb #1b4e81',Token.Sidebar.Status:                         'bg:#b0e4ff #0d3366',Token.Sidebar.Selected.Label:                 'bg:#1b4e81 #bef1ff',Token.Sidebar.Selected.Status:                'bg:#36699c #ccffff bold',Token.Sidebar.Separator:                       'bg:#95c8fb #ccffff underline',Token.Sidebar.Key:                            'bg:#95c8ff #003366 bold',Token.Sidebar.Key.Description:                'bg:#95c8fb #003366',Token.Sidebar.HelpText:                       'bg:#ccf1ff #0d3366',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#0033d2  #003366',Token.History.Line.Current:                  'bg:#ccffff #003366',Token.History.Line.Selected.Current:         'bg:#6ca0ff #003366',Token.History.ExistingInput:                  '#6ca0d2',Token.Window.Border:                          '#953366',Token.Window.Title:                           'bg:#95c8fb #003366',Token.Window.TIItleV2:                         'bg:#9584d2 #003366 bold',Token.AcceptMessage:                          'bg:#6cffff #36699c',Token.ExitConfirmation:                       'bg:#36a09c #ccffff',}
cyan_3={Token.LineNumber:'#24d4ce bg:#000073',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #0000fb',Token.In.Number:                              '',Token.Out:                                    '#00ff46',Token.Out.Number:                             '#00ff46',Token.Separator:                              '#95eaff',Token.Toolbar.Search:                         '#7e1eff noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#7e1eff noinherit',Token.Toolbar.Arg:                            '#7e1eff noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#954cff #000046',Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',Token.Toolbar.Signature.Operator:             '#000046 bold',Token.Docstring:                              '#51a6fb',Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',Token.Aborted:                                '#51a6fb',Token.Sidebar:                                'bg:#95eaff #000046',Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',Token.Sidebar.Label:                          'bg:#95eaff #001e73',Token.Sidebar.Status:                         'bg:#c2ffff #000046',Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',Token.Sidebar.Key.Description:                'bg:#95eaff #000046',Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#0000fb  #000046',Token.History.Line.Current:                  'bg:#f0ffff #000046',Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',Token.History.ExistingInput:                  '#51a6fb',Token.Window.Border:                          '#950046',Token.Window.Title:                           'bg:#95eaff #000046',Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',Token.AcceptMessage:                          'bg:#51ffff #004ca0',Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',}
cyan_4={    Token.LineNumber:'#24d4ce bg:#000073',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #0000fb',    Token.In.Number:                              '',    Token.Out:                                    '#00ff46',    Token.Out.Number:                             '#00ff46',    Token.Separator:                              '#95eaff',    Token.Toolbar.Search:                         '#7e1eff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#7e1eff noinherit',    Token.Toolbar.Arg:                            '#7e1eff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#954cff #000046',    Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',    Token.Toolbar.Signature.Operator:             '#000046 bold',    Token.Docstring:                              '#51a6fb',    Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',    Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',    Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',    Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',    Token.Aborted:                                '#51a6fb',    Token.Sidebar:                                'bg:#95eaff #000046',    Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',    Token.Sidebar.Label:                          'bg:#95eaff #001e73',    Token.Sidebar.Status:                         'bg:#c2ffff #000046',    Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',    Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',    Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',    Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',    Token.Sidebar.Key.Description:                'bg:#95eaff #000046',    Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#0000fb  #000046',    Token.History.Line.Current:                  'bg:#f0ffff #000046',    Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',    Token.History.ExistingInput:                  '#51a6fb',    Token.Window.Border:                          '#950046',    Token.Window.Title:                           'bg:#95eaff #000046',    Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',    Token.AcceptMessage:                          'bg:#51ffff #004ca0',    Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',    Token.LineNumber:                             '#24d4ce bg:#001e73',        Token.SearchMatch:                            '#f0ffff bg:#7e4ca0',        Token.SearchMatch.Current:                    '#f0ffff bg:#004cff',        Token.SelectedText:                           '#f0ffff bg:#7e79ce',        Token.Toolbar.Completions:                    'bg:#954cff #000046',        Token.Toolbar.Completions.Arrow:              'bg:#954cff #000046 bold',        Token.Toolbar.Completions.Completion:         'bg:#954cff #000046',        Token.Toolbar.Completions.Completion.Current: 'bg:#5100fb #f0ffff',        Token.Menu.Completions.Completion:            'bg:#954cff #000046',        Token.Menu.Completions.Completion.Current:    'bg:#5100fb #f0ffff',        Token.Menu.Completions.Meta:                  'bg:#684cff #000046',        Token.Menu.Completions.Meta.Current:          'bg:#7e00ff #000046',        Token.Menu.Completions.ProgressBar:           'bg:#7ed4ff',        Token.Menu.Completions.ProgressButton:        'bg:#000046',}
cyan_4={
     Token.LineNumber:                                  '    #24d4ce        bg:#000073                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #0000fb                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #00ff46                                       ',
     Token.Out.Number:                                  '    #00ff46                                       ',
     Token.Separator:                                   '    #95eaff                                       ',
     Token.Toolbar.Search:                              '    #7e1eff                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #7e1eff                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #7e1eff                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #000046        bg:#954cff                     ',
     Token.Toolbar.Signature.CurrentName:               '    #f0ffff        bg:#5100fb        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #000046                          bold         ',
     Token.Docstring:                                   '    #51a6fb                                       ',
     Token.Toolbar.Validation:                          '    #7ed4ff        bg:#004c46                     ',
     Token.Toolbar.Status:                              '    #7ed4ff        bg:#001e73                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #7effff        bg:#001e73                     ',
     Token.Toolbar.Status.Key:                          '    #51a6fb        bg:#000046                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #f0ffff        bg:#00d4a0                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #7ed4ff        bg:#247973                     ',
     Token.Toolbar.Status.PythonVersion:                '    #f0ffff        bg:#001e73        bold         ',
     Token.Aborted:                                     '    #51a6fb                                       ',
     Token.Sidebar:                                     '    #000046        bg:#95eaff                     ',
     Token.Sidebar.Title:                               '    #f0ffff        bg:#f079fb        bold         ',
     Token.Sidebar.Label:                               '    #001e73        bg:#95eaff                     ',
     Token.Sidebar.Status:                              '    #000046        bg:#c2ffff                     ',
     Token.Sidebar.Selected.Label:                      '    #d9ffff        bg:#001e73                     ',
     Token.Sidebar.Selected.Status:                     '    #f0ffff        bg:#004ca0        bold         ',
     Token.Sidebar.Separator:                           '    #f0ffff        bg:#95eaff        underline    ',
     Token.Sidebar.Key:                                 '    #000046        bg:#95eaff        bold         ',
     Token.Sidebar.Key.Description:                     '    #000046        bg:#95eaff                     ',
     Token.Sidebar.HelpText:                            '    #000046        bg:#a0f0ff                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #000046        bg:#0000fb                     ',
     Token.History.Line.Current:                        '    #000046        bg:#f0ffff                     ',
     Token.History.Line.Selected.Current:               '    #000046        bg:#51a6ff                     ',
     Token.History.ExistingInput:                       '    #51a6fb                                       ',
     Token.Window.Border:                               '    #950046                                       ',
     Token.Window.Title:                                '    #000046        bg:#95eaff                     ',
     Token.Window.TIItleV2:                             '    #000046        bg:#9579fb        bold         ',
     Token.AcceptMessage:                               '    #004ca0        bg:#51ffff                     ',
     Token.ExitConfirmation:                            '    #f0ffff        bg:#00a6a0                     ',
     Token.LineNumber:                                  '    #24d4ce        bg:#001e73                     ',
     Token.SearchMatch:                                 '    #f0ffff        bg:#7e4ca0                     ',
     Token.SearchMatch.Current:                         '    #f0ffff        bg:#004cff                     ',
     Token.SelectedText:                                '    #f0ffff        bg:#7e79ce                     ',
     Token.Toolbar.Completions:                         '    #000046        bg:#954cff                     ',
     Token.Toolbar.Completions.Arrow:                   '    #000046        bg:#954cff        bold         ',
     Token.Toolbar.Completions.Completion:              '    #000046        bg:#954cff                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #f0ffff        bg:#5100fb                     ',
     Token.Menu.Completions.Completion:                 '    #000046        bg:#954cff                     ',
     Token.Menu.Completions.Completion.Current:         '    #f0ffff        bg:#5100fb                     ',
     Token.Menu.Completions.Meta:                       '    #000046        bg:#684cff                     ',
     Token.Menu.Completions.Meta.Current:               '    #000046        bg:#7e00ff                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#7ed4ff                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#000046                     ',
}



cyan_4__02={
     Token.LineNumber:                                  '    #ce24d4        bg:#730000                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #fb0000                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #4600ff                                       ',
     Token.Out.Number:                                  '    #4600ff                                       ',
     Token.Separator:                                   '    #ff95ea                                       ',
     Token.Toolbar.Search:                              '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fff0ff        bg:#fb5100        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #460000                          bold         ',
     Token.Docstring:                                   '    #fb51a6                                       ',
     Token.Toolbar.Validation:                          '    #ff7ed4        bg:#46004c                     ',
     Token.Toolbar.Status:                              '    #ff7ed4        bg:#73001e                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ff7eff        bg:#73001e                     ',
     Token.Toolbar.Status.Key:                          '    #fb51a6        bg:#460000                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fff0ff        bg:#a000d4                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #ff7ed4        bg:#732479                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fff0ff        bg:#73001e        bold         ',
     Token.Aborted:                                     '    #fb51a6                                       ',
     Token.Sidebar:                                     '    #460000        bg:#ff95ea                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#fbf079        bold         ',
     Token.Sidebar.Label:                               '    #73001e        bg:#ff95ea                     ',
     Token.Sidebar.Status:                              '    #460000        bg:#ffc2ff                     ',
     Token.Sidebar.Selected.Label:                      '    #ffd9ff        bg:#73001e                     ',
     Token.Sidebar.Selected.Status:                     '    #ffffff        bg:#a0004c        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#ff95ea        underline    ',
     Token.Sidebar.Key:                                 '    #460000        bg:#ff95ea        bold         ',
     Token.Sidebar.Key.Description:                     '    #460000        bg:#ff95ea                     ',
     Token.Sidebar.HelpText:                            '    #460000        bg:#ffa0f0                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #460000        bg:#fb0000                     ',
     Token.History.Line.Current:                        '    #460000        bg:#fff0ff                     ',
     Token.History.Line.Selected.Current:               '    #460000        bg:#ff51a6                     ',
     Token.History.ExistingInput:                       '    #fb51a6                                       ',
     Token.Window.Border:                               '    #469500                                       ',
     Token.Window.Title:                                '    #460000        bg:#ff95ea                     ',
     Token.Window.TIItleV2:                             '    #460000        bg:#fb9579        bold         ',
     Token.AcceptMessage:                               '    #a0004c        bg:#ff51ff                     ',
     Token.ExitConfirmation:                            '    #fff0ff        bg:#a000a6                     ',
     Token.LineNumber:                                  '    #ce24d4        bg:#73001e                     ',
     Token.SearchMatch:                                 '    #fff0ff        bg:#a07e4c                     ',
     Token.SearchMatch.Current:                         '    #fff0ff        bg:#ff004c                     ',
     Token.SelectedText:                                '    #fff0ff        bg:#ce7e79                     ',
     Token.Toolbar.Completions:                         '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Completions.Arrow:                   '    #460000        bg:#ff954c        bold         ',
     Token.Toolbar.Completions.Completion:              '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #fff0ff        bg:#fb5100                     ',
     Token.Menu.Completions.Completion:                 '    #460000        bg:#ff954c                     ',
     Token.Menu.Completions.Completion.Current:         '    #fff0ff        bg:#fb5100                     ',
     Token.Menu.Completions.Meta:                       '    #460000        bg:#ff684c                     ',
     Token.Menu.Completions.Meta.Current:               '    #460000        bg:#ff7e00                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#ff7ed4                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#460000                     ',
}






cyan_4__02__02={
     Token.LineNumber:                                  '    #d4ce24        bg:#007300                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #00fb00                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #ff4600                                       ',
     Token.Out.Number:                                  '    #ff4600                                       ',
     Token.Separator:                                   '    #eaff95                                       ',
     Token.Toolbar.Search:                              '    #1eff7e                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #1eff7e                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #1eff7e                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fffff0        bg:#00fb51        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #004600                          bold         ',
     Token.Docstring:                                   '    #a6fb51                                       ',
     Token.Toolbar.Validation:                          '    #d4ff7e        bg:#4c4600                     ',
     Token.Toolbar.Status:                              '    #d4ff7e        bg:#1e7300                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ffff7e        bg:#1e7300                     ',
     Token.Toolbar.Status.Key:                          '    #a6fb51        bg:#004600                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fffff0        bg:#d4a000                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #d4ff7e        bg:#797324                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fffff0        bg:#1e7300        bold         ',
     Token.Aborted:                                     '    #a6fb51                                       ',
     Token.Sidebar:                                     '    #004600        bg:#eaff95                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#79fbf0        bold         ',
     Token.Sidebar.Label:                               '    #1e7300        bg:#eaff95                     ',
     Token.Sidebar.Status:                              '    #004600        bg:#ffffc2                     ',
     Token.Sidebar.Selected.Label:                      '    #ffffd9        bg:#1e7300                     ',
     Token.Sidebar.Selected.Status:                     '    #000000        bg:#4ca000        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#eaff95        underline    ',
     Token.Sidebar.Key:                                 '    #004600        bg:#eaff95        bold         ',
     Token.Sidebar.Key.Description:                     '    #004600        bg:#eaff95                     ',
     Token.Sidebar.HelpText:                            '    #004600        bg:#f0ffa0                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #004600        bg:#00fb00                     ',
     Token.History.Line.Current:                        '    #004600        bg:#fffff0                     ',
     Token.History.Line.Selected.Current:               '    #004600        bg:#a6ff51                     ',
     Token.History.ExistingInput:                       '    #a6fb51                                       ',
     Token.Window.Border:                               '    #004695                                       ',
     Token.Window.Title:                                '    #004600        bg:#eaff95                     ',
     Token.Window.TIItleV2:                             '    #004600        bg:#79fb95        bold         ',
     Token.AcceptMessage:                               '    #4ca000        bg:#ffff51                     ',
     Token.ExitConfirmation:                            '    #fffff0        bg:#a6a000                     ',
     Token.LineNumber:                                  '    #d4ce24        bg:#1e7300                     ',
     Token.SearchMatch:                                 '    #fffff0        bg:#4ca07e                     ',
     Token.SearchMatch.Current:                         '    #fffff0        bg:#4cff00                     ',
     Token.SelectedText:                                '    #fffff0        bg:#79ce7e                     ',
     Token.Toolbar.Completions:                         '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Completions.Arrow:                   '    #004600        bg:#4cff95        bold         ',
     Token.Toolbar.Completions.Completion:              '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #000000        bg:#00fb51                     ',
     Token.Menu.Completions.Completion:                 '    #004600        bg:#4cff95                     ',
     Token.Menu.Completions.Completion.Current:         '    #4cff95        bg:#009966                     ',
     Token.Menu.Completions.Meta:                       '    #004600        bg:#4cff68                     ',
     Token.Menu.Completions.Meta.Current:               '    #004600        bg:#00ff7e                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#d4ff7e                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#004600                     ',
}




cyan_4__02__02__12={
     Token.LineNumber:                                  '    #d424ce        bg:#000073                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #0000fb                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #ff0046                                       ',
     Token.Out.Number:                                  '    #ff0046                                       ',
     Token.Separator:                                   '    #ea95ff                                       ',
     Token.Toolbar.Search:                              '    #1e7eff                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #1e7eff                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #1e7eff                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fff0ff        bg:#0051fb        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #000046                          bold         ',
     Token.Docstring:                                   '    #a651fb                                       ',
     Token.Toolbar.Validation:                          '    #d47eff        bg:#4c0046                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryNotPluggedIn:          '    #ff55aa        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ff7eff        bg:#1e0073                     ',
     Token.Toolbar.Status.Key:                          '    #a651fb        bg:#000046                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fff0ff        bg:#d400a0                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #d47eff        bg:#792473                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fff0ff        bg:#1e0073        bold         ',
     Token.Aborted:                                     '    #a651fb                                       ',
     Token.Sidebar:                                     '    #000046        bg:#ea95ff                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#79f0fb        bold         ',
     Token.Sidebar.Label:                               '    #1e0073        bg:#ea95ff                     ',
     Token.Sidebar.Status:                              '    #000046        bg:#ffc2ff                     ',
     Token.Sidebar.Selected.Label:                      '    #ffd9ff        bg:#1e0073                     ',
     Token.Sidebar.Selected.Status:                     '    #FFFFFF        bg:#4c00a0        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#ea95ff        underline    ',
     Token.Sidebar.Key:                                 '    #000046        bg:#ea95ff        bold         ',
     Token.Sidebar.Key.Description:                     '    #000046        bg:#ea95ff                     ',
     Token.Sidebar.HelpText:                            '    #000046        bg:#f0a0ff                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #000046        bg:#0000fb                     ',
     Token.History.Line.Current:                        '    #000046        bg:#fff0ff                     ',
     Token.History.Line.Selected.Current:               '    #000046        bg:#a651ff                     ',
     Token.History.ExistingInput:                       '    #a651fb                                       ',
     Token.Window.Border:                               '    #009546                                       ',
     Token.Window.Title:                                '    #000046        bg:#ea95ff                     ',
     Token.Window.TIItleV2:                             '    #000046        bg:#7995fb        bold         ',
     Token.AcceptMessage:                               '    #4c00a0        bg:#ff51ff                     ',
     Token.ExitConfirmation:                            '    #fff0ff        bg:#a600a0                     ',
     Token.LineNumber:                                  '    #d424ce        bg:#1e0073                     ',
     Token.SearchMatch:                                 '    #fff0ff        bg:#4c7ea0                     ',
     Token.SearchMatch.Current:                         '    #fff0ff        bg:#4c00ff                     ',
     Token.SelectedText:                                '    #fff0ff        bg:#797ece                     ',
     Token.Toolbar.Completions:                         '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Completions.Arrow:                   '    #000046        bg:#4c95ff        bold         ',
     Token.Toolbar.Completions.Completion:              '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #fff0ff        bg:#0051fb                     ',
     Token.Menu.Completions.Completion:                 '    #000046        bg:#4c95ff                     ',
     Token.Menu.Completions.Completion.Current:         '    #fff0ff        bg:#0051fb                     ',
     Token.Menu.Completions.Meta:                       '    #000046        bg:#4c68ff                     ',
     Token.Menu.Completions.Meta.Current:               '    #000046        bg:#007eff                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#d47eff                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#000046                     ',
}



# plain={
#      Token.LineNumber:                                  '',
#      Token.Prompt:                                      '',
#      Token.Prompt.Dots:                                 '',
#      Token.In:                                          '',
#      Token.In.Number:                                   '',
#      Token.Out:                                         '',
#      Token.Out.Number:                                  '',
#      Token.Separator:                                   '',
#      Token.Toolbar.Search:                              '',
#      Token.Toolbar.Search.Text:                         '',
#      Token.Toolbar.System:                              '',
#      Token.Toolbar.Arg:                                 '',
#      Token.Toolbar.Arg.Text:                            '',
#      Token.Toolbar.Signature:                           '',
#      Token.Toolbar.Signature.CurrentName:               '',
#      Token.Toolbar.Signature.Operator:                  '',
#      Token.Docstring:                                   '',
#      Token.Toolbar.Validation:                          '',
#      Token.Toolbar.Status:                              '',
#      Token.Toolbar.Status.BatteryPluggedIn:             '',
#      Token.Toolbar.Status.BatteryNotPluggedIn:          '',
#      Token.Toolbar.Status.Title:                        '',
#      Token.Toolbar.Status.InputMode:                    '',
#      Token.Toolbar.Status.Key:                          '',
#      Token.Toolbar.Status.PasteModeOn:                  '',
#      Token.Toolbar.Status.PseudoTerminalCurrentVariable:'',
#      Token.Toolbar.Status.PythonVersion:                '',
#      Token.Aborted:                                     '',
#      Token.Sidebar:                                     '',
#      Token.Sidebar.Title:                               '',
#      Token.Sidebar.Label:                               '',
#      Token.Sidebar.Status:                              '',
#      Token.Sidebar.Selected.Label:                      '',
#      Token.Sidebar.Selected.Status:                     '',
#      Token.Sidebar.Separator:                           '',
#      Token.Sidebar.Key:                                 '',
#      Token.Sidebar.Key.Description:                     '',
#      Token.Sidebar.HelpText:                            '',
#      Token.History.Line:                                '',
#      Token.History.Line.Selected:                       '',
#      Token.History.Line.Current:                        '',
#      Token.History.Line.Selected.Current:               '',
#      Token.History.ExistingInput:                       '',
#      Token.Window.Border:                               '',
#      Token.Window.Title:                                '',
#      Token.Window.TIItleV2:                             '',
#      Token.AcceptMessage:                               '',
#      Token.ExitConfirmation:                            '',
#      Token.LineNumber:                                  '',
#      Token.SearchMatch:                                 '',
#      Token.SearchMatch.Current:                         '',
#      Token.SelectedText:                                '',
#      Token.Toolbar.Completions:                         '',
#      Token.Toolbar.Completions.Arrow:                   '',
#      Token.Toolbar.Completions.Completion:              '',
#      Token.Toolbar.Completions.Completion.Current:      '',
#      Token.Menu.Completions.Completion:                 '',
#      Token.Menu.Completions.Completion.Current:         '',
#      Token.Menu.Completions.Meta:                       '',
#      Token.Menu.Completions.Meta.Current:               '',
#      Token.Menu.Completions.ProgressBar:                '',
#      Token.Menu.Completions.ProgressButton:             '',
# }




temp = {
    Token.LineNumber:'#24d4ce bg:#000073',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #0000fb',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#00ff46',
    Token.Out.Number:                             '#00ff46',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#95eaff',

    # Search toolbar.
    Token.Toolbar.Search:                         '#7e1eff noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#7e1eff noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#7e1eff noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#954cff #000046',
    Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',
    Token.Toolbar.Signature.Operator:             '#000046 bold',

    Token.Docstring:                              '#51a6fb',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',
    Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',
    Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',
    Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#51a6fb',

    # The options sidebar.
    Token.Sidebar:                                'bg:#95eaff #000046',
    Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',
    Token.Sidebar.Label:                          'bg:#95eaff #001e73',
    Token.Sidebar.Status:                         'bg:#c2ffff #000046',
    Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',
    Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',

    Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',
    Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',
    Token.Sidebar.Key.Description:                'bg:#95eaff #000046',
    Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#0000fb  #000046',
    Token.History.Line.Current:                  'bg:#f0ffff #000046',
    Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',
    Token.History.ExistingInput:                  '#51a6fb',

    # Help Window.
    Token.Window.Border:                          '#950046',
    Token.Window.Title:                           'bg:#95eaff #000046',
    Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#51ffff #004ca0',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',
}
temp.update({
    Token.Aborted:                                '#3a90e4',
    Token.Sidebar:                                'bg:#004ca0 #f0ffff',
    Token.Sidebar.Title:                          'bg:#00bde4 #000046 bold',
    Token.Sidebar.Label:                          'bg:#004ca0 #c2ffff',
    Token.Sidebar.Status:                         'bg:#001e73 #d9ffff',
    Token.Sidebar.Selected.Label:                 'bg:#c2ffff #00085c',
    Token.Sidebar.Selected.Status:                'bg:#95eaff #000046 bold',
    Token.Sidebar.Separator:                       'bg:#004ca0 #000046 underline',
    Token.Sidebar.Key:                            'bg:#004c73 #f0ffff bold',
    Token.Sidebar.Key.Description:                'bg:#004ca0 #f0ffff',
    Token.Sidebar.HelpText:                       'bg:#00085c #d9ffff',
    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#f0ffe4  #f0ffff',
    Token.History.Line.Current:                  'bg:#000046 #f0ffff',
    Token.History.Line.Selected.Current:         'bg:#3a9046 #f0ffff',
    Token.History.ExistingInput:                  '#3a90e4',
    # Help Window.
    Token.Window.Border:                          '#00ffff',
    Token.Window.Title:                           'bg:#004ca0 #f0ffff',
    Token.Window.TIItleV2:                         'bg:#00bde4 #f0ffff bold',
    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#3a0046 #95eaff',
    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#9590ff #000046',
    # Line numbers.
    Token.LineNumber:                             '#24d4ce bg:#001e73',
    # Highlighting of search matches in document.
    Token.SearchMatch:                            '#f0ffff bg:#7e4ca0',
    Token.SearchMatch.Current:                    '#f0ffff bg:#004cff',
    # Highlighting of select text in document.
    Token.SelectedText:                           '#f0ffff bg:#7e79ce',
    Token.Toolbar.Completions:            'bg:#000046 #01f0ff',
    Token.Toolbar.Completions.Arrow:              'bg:#000046 #01f0ff bold',
    Token.Toolbar.Completions.Completion:         'bg:#000046 #01f0ff',
    Token.Toolbar.Completions.Completion.Current: 'bg:#01f0ff #000046',
    # Completer menu.
    Token.Menu.Completions.Completion:            'bg:#000046 #01ffff',
    Token.Menu.Completions.Completion.Current:    'bg:#01aaf0 #000046',
    Token.Menu.Completions.Meta:                  'bg:#000046 #01ffd0',
    Token.Menu.Completions.Meta.Current:          'bg:#000046 #00ffee',
    Token.Menu.Completions.ProgressBar:           'bg:#b6ffee           ',
    Token.Menu.Completions.ProgressButton:        'bg:#004e46           ',
})
newstyle=temp





temp = {
    Token.LineNumber:'#d3cd23 bg:#007200',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #00fa00',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#fe4500',
    Token.Out.Number:                             '#fe4500',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#e9fe94',

    # Search toolbar.
    Token.Toolbar.Search:                         '#1dfe7d noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#1dfe7d noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#1dfe7d noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#4bfe94 #004500',
    Token.Toolbar.Signature.CurrentName:          'bg:#00fa50 #fefeef bold',
    Token.Toolbar.Signature.Operator:             '#004500 bold',

    Token.Docstring:                              '#a5fa50',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#4b4500 #d3fe7d',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#1d7200 #d3fe7d',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#1d7200 #1dfe00',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#1d7200 #d37200',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#1d7200 #fefe7d',
    Token.Toolbar.Status.Key:                     'bg:#004500 #a5fa50',
    Token.Toolbar.Status.PasteModeOn:             'bg:#d39f00 #fefeef',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#787223 #d3fe7d',
    Token.Toolbar.Status.PythonVersion:           'bg:#1d7200 #fefeef bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#a5fa50',

    # The options sidebar.
    Token.Sidebar:                                'bg:#e9fe94 #004500',
    Token.Sidebar.Title:                          'bg:#78faef #fefeef bold',
    Token.Sidebar.Label:                          'bg:#e9fe94 #1d7200',
    Token.Sidebar.Status:                         'bg:#fefec1 #004500',
    Token.Sidebar.Selected.Label:                 'bg:#1d7200 #fefed8',
    Token.Sidebar.Selected.Status:                'bg:#4b9f00 #fefeef bold',

    Token.Sidebar.Separator:                       'bg:#e9fe94 #fefeef underline',
    Token.Sidebar.Key:                            'bg:#e9fe94 #004500 bold',
    Token.Sidebar.Key.Description:                'bg:#e9fe94 #004500',
    Token.Sidebar.HelpText:                       'bg:#fefeef #004500',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#00fa00  #004500',
    Token.History.Line.Current:                  'bg:#fefeef #004500',
    Token.History.Line.Selected.Current:         'bg:#a5fe50 #004500',
    Token.History.ExistingInput:                  '#a5fa50',

    # Help Window.
    Token.Window.Border:                          '#004594',
    Token.Window.Title:                           'bg:#e9fe94 #004500',
    Token.Window.TIItleV2:                         'bg:#78fa94 #004500 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#fefe50 #4b9f00',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#a59f00 #fefeef',
}
temp.update({
    Token.Aborted:                                '#8fe339',
    Token.Sidebar:                                'bg:#4b9f00 #fefeef',
    Token.Sidebar.Title:                          'bg:#bce300 #004500 bold',
    Token.Sidebar.Label:                          'bg:#4b9f00 #fefec1',
    Token.Sidebar.Status:                         'bg:#1d7200 #fefed8',
    Token.Sidebar.Selected.Label:                 'bg:#fefec1 #075b00',
    Token.Sidebar.Selected.Status:                'bg:#e9fe94 #004500 bold',
    Token.Sidebar.Separator:                       'bg:#4b9f00 #004500 underline',
    Token.Sidebar.Key:                            'bg:#4b7200 #fefeef bold',
    Token.Sidebar.Key.Description:                'bg:#4b9f00 #fefeef',
    Token.Sidebar.HelpText:                       'bg:#075b00 #fefed8',
    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#fee3ef  #fefeef',
    Token.History.Line.Current:                  'bg:#004500 #fefeef',
    Token.History.Line.Selected.Current:         'bg:#8f4539 #fefeef',
    Token.History.ExistingInput:                  '#8fe339',
    # Help Window.
    Token.Window.Border:                          '#fefe00',
    Token.Window.Title:                           'bg:#4b9f00 #fefeef',
    Token.Window.TIItleV2:                         'bg:#bce300 #fefeef bold',
    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#004539 #e9fe94',
    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#8ffe94 #004500',
    # Line numbers.
    Token.LineNumber:                             '#d3cd23 bg:#1d7200',
    # Highlighting of search matches in document.
    Token.SearchMatch:                            '#fefeef bg:#4b9f7d',
    Token.SearchMatch.Current:                    '#fefeef bg:#4bfe00',
    # Highlighting of select text in document.
    Token.SelectedText:                           '#fefeef bg:#78cd7d',
    Token.Toolbar.Completions:                    'bg:#004500 #effe00',
    Token.Toolbar.Completions.Arrow:              'bg:#004500 #effe00 bold',
    Token.Toolbar.Completions.Completion:         'bg:#004500 #effe00',
    Token.Toolbar.Completions.Completion.Current: 'bg:#fefeef #7db100',
    # Completer menu.
    Token.Menu.Completions.Completion:            'bg:#004500 #fefe00',
    Token.Menu.Completions.Completion.Current:    'bg:#fefe00 #004500',
    Token.Menu.Completions.Meta:                  'bg:#004500 #fecf00',
    Token.Menu.Completions.Meta.Current:          'bg:#004500 #feed00',
    Token.Menu.Completions.ProgressBar:           'bg:#feedb5           ',
    Token.Menu.Completions.ProgressButton:        'bg:#4d4500           ',
})
dejavu=temp





temp = {
    Token.LineNumber:'bg:#007200 #d3cd23',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #0000fa bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #fe0045',
    Token.Out.Number:                                     '           #fe0045',
    Token.Separator:                                      '           #e994fe',
    Token.Toolbar.Search:                                 '           #1d7dfe noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #1d7dfe noinherit',
    Token.Toolbar.Arg:                                    '           #1d7dfe noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#4b94fe #000045',
    Token.Toolbar.Signature.CurrentName:                  'bg:#0050fa #feeffe bold',
    Token.Toolbar.Signature.Operator:                     '           #000045            bold',
    Token.Docstring:                                      '           #a550fa',
    Token.Toolbar.Validation:                             'bg:#4b0045 #d37dfe',
    Token.Toolbar.Status:                                 'bg:#1d0072 #d37dfe',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#1d0072 #1d00fe',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#1d0072 #d30072',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#1d0072 #fe7dfe',
    Token.Toolbar.Status.Key:                             'bg:#000045 #a550fa',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#d3009f #feeffe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#782372 #d37dfe',
    Token.Toolbar.Status.PythonVersion:                   'bg:#1d0072 #feeffe bold',
    Token.Aborted:                                        '           #a550fa',
    Token.Sidebar:                                        'bg:#e994fe #000045',
    Token.Sidebar.Title:                                  'bg:#78effa #feeffe bold',
    Token.Sidebar.Label:                                  'bg:#e994fe #1d0072',
    Token.Sidebar.Status:                                 'bg:#fec1fe #000045',
    Token.Sidebar.Selected.Label:                         'bg:#1d0072 #fed8fe',
    Token.Sidebar.Selected.Status:                        'bg:#4b009f #feeffe bold',
    Token.Sidebar.Separator:                              'bg:#e994fe #feeffe underline',
    Token.Sidebar.Key:                                    'bg:#e994fe #000045 bold',
    Token.Sidebar.Key.Description:                        'bg:#e994fe #000045',
    Token.Sidebar.HelpText:                               'bg:#feeffe #000045',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#0000fa #000045',
    Token.History.Line.Current:                           'bg:#feeffe #000045',
    Token.History.Line.Selected.Current:                  'bg:#a550fe #000045',
    Token.History.ExistingInput:                          '           #a550fa',
    Token.Window.Border:                                  '           #009445',
    Token.Window.Title:                                   'bg:#e994fe #000045',
    Token.Window.TIItleV2:                                'bg:#7894fa #000045 bold',
    Token.AcceptMessage:                                  'bg:#fe50fe #4b009f',
    Token.ExitConfirmation:                               'bg:#a5009f #feeffe',
}
temp.update({
    Token.Aborted:                                        '           #8fe339',
    Token.Sidebar:                                        'bg:#4b009f #feeffe',
    Token.Sidebar.Title:                                  'bg:#bc00e3 #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#4b009f #fec1fe',
    Token.Sidebar.Status:                                 'bg:#1d0072 #fed8fe',
    Token.Sidebar.Selected.Label:                         'bg:#fec1fe #07005b',
    Token.Sidebar.Selected.Status:                        'bg:#e994fe #000045 bold',
    Token.Sidebar.Separator:                              'bg:#4b009f #000045 underline',
    Token.Sidebar.Key:                                    'bg:#4b0072 #feeffe bold',
    Token.Sidebar.Key.Description:                        'bg:#4b009f #feeffe',
    Token.Sidebar.HelpText:                               'bg:#07005b #fed8fe',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#feefe3 #feeffe',
    Token.History.Line.Current:                           'bg:#000045 #feeffe',
    Token.History.Line.Selected.Current:                  'bg:#8f3945 #feeffe',
    Token.History.ExistingInput:                          '           #8f39e3',
    Token.Window.Border:                                  '           #fe00fe',
    Token.Window.Title:                                   'bg:#4b009f #feeffe',
    Token.Window.TIItleV2:                                'bg:#bc00e3 #feeffe bold',
    Token.AcceptMessage:                                  'bg:#003945 #e994fe',
    Token.ExitConfirmation:                               'bg:#8f94fe #000045',
    Token.LineNumber:                                     'bg:#1d0072 #d323cd',
    Token.SearchMatch:                                    'bg:#4b7d9f #feeffe',
    Token.SearchMatch.Current:                            'bg:#4b00fe #feeffe',
    Token.SelectedText:                                   'bg:#787dcd #feeffe',
    Token.Toolbar.Completions:                            'bg:#000045 #ef00fe',
    Token.Toolbar.Completions.Arrow:                      'bg:#000045 #ef00fe bold',
    Token.Toolbar.Completions.Completion:                 'bg:#000045 #ef00fe',
    Token.Toolbar.Completions.Completion.Current:         'bg:#feeffe #7d00b1',
    Token.Menu.Completions.Completion:                    'bg:#000045 #fe00fe',
    Token.Menu.Completions.Completion.Current:            'bg:#fe00fe #000045',
    Token.Menu.Completions.Meta:                          'bg:#000045 #fe00cf',
    Token.Menu.Completions.Meta.Current:                  'bg:#000045 #fe00ed',
    Token.Menu.Completions.ProgressBar:                   'bg:#feb5ed           ',
    Token.Menu.Completions.ProgressButton:                'bg:#4d0045           ',
})
sprice=temp



temp = {
    Token.LineNumber:                                     'bg:#000072 #23d3cd',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fa0000 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #45fe00',
    Token.Out.Number:                                     '           #45fe00',
    Token.Separator:                                      '           #fee994',
    Token.Toolbar.Search:                                 '           #fe1d7d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fe1d7d noinherit',
    Token.Toolbar.Arg:                                    '           #fe1d7d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fe4b94 #450000',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fa0050 #fefeef bold',
    Token.Toolbar.Signature.Operator:                     '           #450000            bold',
    Token.Docstring:                                      '           #faa550',
    Token.Toolbar.Validation:                             'bg:#454b00 #fed37d',
    Token.Toolbar.Status:                                 'bg:#721d00 #fed37d',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#721d00 #fe1d00',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#721d00 #72d300',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#721d00 #fefe7d',
    Token.Toolbar.Status.Key:                             'bg:#450000 #faa550',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9fd300 #fefeef',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#727823 #fed37d',
    Token.Toolbar.Status.PythonVersion:                   'bg:#721d00 #fefeef bold',
    Token.Aborted:                                        '           #faa550',
    Token.Sidebar:                                        'bg:#fee994 #450000',
    Token.Sidebar.Title:                                  'bg:#fa78ef #fefeef bold',
    Token.Sidebar.Label:                                  'bg:#fee994 #721d00',
    Token.Sidebar.Status:                                 'bg:#fefec1 #450000',
    Token.Sidebar.Selected.Label:                         'bg:#721d00 #fefed8',
    Token.Sidebar.Selected.Status:                        'bg:#9f4b00 #fefeef bold',
    Token.Sidebar.Separator:                              'bg:#fee994 #fefeef underline',
    Token.Sidebar.Key:                                    'bg:#fee994 #450000 bold',
    Token.Sidebar.Key.Description:                        'bg:#fee994 #450000',
    Token.Sidebar.HelpText:                               'bg:#fefeef #450000',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#fa0000 #450000',
    Token.History.Line.Current:                           'bg:#fefeef #450000',
    Token.History.Line.Selected.Current:                  'bg:#fea550 #450000',
    Token.History.ExistingInput:                          '           #faa550',
    Token.Window.Border:                                  '           #450094',
    Token.Window.Title:                                   'bg:#fee994 #450000',
    Token.Window.TIItleV2:                                'bg:#fa7894 #450000 bold',
    Token.AcceptMessage:                                  'bg:#fefe50 #9f4b00',
    Token.ExitConfirmation:                               'bg:#9fa500 #fefeef',
}
temp.update({
    Token.Aborted:                                        '           #398fe3',
    Token.Sidebar:                                        'bg:#9f4b00 #fefeef',
    Token.Sidebar.Title:                                  'bg:#e3bc00 #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#9f4b00 #fefec1',
    Token.Sidebar.Status:                                 'bg:#721d00 #fefed8',
    Token.Sidebar.Selected.Label:                         'bg:#fefec1 #5b0700',
    Token.Sidebar.Selected.Status:                        'bg:#fee994 #450000 bold',
    Token.Sidebar.Separator:                              'bg:#9f4b00 #450000 underline',
    Token.Sidebar.Key:                                    'bg:#724b00 #fefeef bold',
    Token.Sidebar.Key.Description:                        'bg:#9f4b00 #fefeef',
    Token.Sidebar.HelpText:                               'bg:#5b0700 #fefed8',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#e3feef #fefeef',
    Token.History.Line.Current:                           'bg:#450000 #fefeef',
    Token.History.Line.Selected.Current:                  'bg:#458f39 #fefeef',
    Token.History.ExistingInput:                          '           #e38f39',
    Token.Window.Border:                                  '           #fefe00',
    Token.Window.Title:                                   'bg:#9f4b00 #fefeef',
    Token.Window.TIItleV2:                                'bg:#e3bc00 #fefeef bold',
    Token.AcceptMessage:                                  'bg:#450039 #fee994',
    Token.ExitConfirmation:                               'bg:#fe8f94 #450000',
    Token.LineNumber:                                     'bg:#721d00 #cdd323',
    Token.SearchMatch:                                    'bg:#9f4b7d #fefeef',
    Token.SearchMatch.Current:                            'bg:#fe4b00 #fefeef',
    Token.SelectedText:                                   'bg:#cd787d #fefeef',
    Token.Toolbar.Completions:                            'bg:#450000 #feef00',
    Token.Toolbar.Completions.Arrow:                      'bg:#450000 #feef00 bold',
    Token.Toolbar.Completions.Completion:                 'bg:#450000 #feef00',
    Token.Toolbar.Completions.Completion.Current:         'bg:#fefeef #b17d00',
    Token.Menu.Completions.Completion:                    'bg:#450000 #fefe00',
    Token.Menu.Completions.Completion.Current:            'bg:#fefe00 #450000',
    Token.Menu.Completions.Meta:                          'bg:#450000 #cffe00',
    Token.Menu.Completions.Meta.Current:                  'bg:#450000 #edfe00',
    Token.Menu.Completions.ProgressBar:                   'bg:#edfeb5           ',
    Token.Menu.Completions.ProgressButton:                'bg:#454d00           ',
})
splicer1=temp

temp = {
    Token.LineNumber:                                     'bg:#720000 #cd23d3',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #00fa00 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #0045fe',
    Token.Out.Number:                                     '           #0045fe',
    Token.Separator:                                      '           #94fee9',
    Token.Toolbar.Search:                                 '           #7dfe1d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #7dfe1d noinherit',
    Token.Toolbar.Arg:                                    '           #7dfe1d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#94fe4b #004500',
    Token.Toolbar.Signature.CurrentName:                  'bg:#50fa00 #effefe bold',
    Token.Toolbar.Signature.Operator:                     '           #004500            bold',
    Token.Docstring:                                      '           #50faa5',
    Token.Toolbar.Validation:                             'bg:#00454b #7dfed3',
    Token.Toolbar.Status:                                 'bg:#00721d #7dfed3',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#00721d #00fe1d',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#00721d #0072d3',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#00721d #7dfefe',
    Token.Toolbar.Status.Key:                             'bg:#004500 #50faa5',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#009fd3 #effefe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#237278 #7dfed3',
    Token.Toolbar.Status.PythonVersion:                   'bg:#00721d #effefe bold',
    Token.Aborted:                                        '           #50faa5',
    Token.Sidebar:                                        'bg:#94fee9 #004500',
    Token.Sidebar.Title:                                  'bg:#effa78 #effefe bold',
    Token.Sidebar.Label:                                  'bg:#94fee9 #00721d',
    Token.Sidebar.Status:                                 'bg:#c1fefe #004500',
    Token.Sidebar.Selected.Label:                         'bg:#00721d #d8fefe',
    Token.Sidebar.Selected.Status:                        'bg:#009f4b #effefe bold',
    Token.Sidebar.Separator:                              'bg:#94fee9 #effefe underline',
    Token.Sidebar.Key:                                    'bg:#94fee9 #004500 bold',
    Token.Sidebar.Key.Description:                        'bg:#94fee9 #004500',
    Token.Sidebar.HelpText:                               'bg:#effefe #004500',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#00fa00 #004500',
    Token.History.Line.Current:                           'bg:#effefe #004500',
    Token.History.Line.Selected.Current:                  'bg:#50fea5 #004500',
    Token.History.ExistingInput:                          '           #50faa5',
    Token.Window.Border:                                  '           #944500',
    Token.Window.Title:                                   'bg:#94fee9 #004500',
    Token.Window.TIItleV2:                                'bg:#94fa78 #004500 bold',
    Token.AcceptMessage:                                  'bg:#50fefe #009f4b',
    Token.ExitConfirmation:                               'bg:#009fa5 #effefe',
}
temp.update({
    Token.Aborted:                                        '           #e3398f',
    Token.Sidebar:                                        'bg:#009f4b #effefe',
    Token.Sidebar.Title:                                  'bg:#00e3bc #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#009f4b #c1fefe',
    Token.Sidebar.Status:                                 'bg:#00721d #d8fefe',
    Token.Sidebar.Selected.Label:                         'bg:#c1fefe #005b07',
    Token.Sidebar.Selected.Status:                        'bg:#94fee9 #004500 bold',
    Token.Sidebar.Separator:                              'bg:#009f4b #004500 underline',
    Token.Sidebar.Key:                                    'bg:#00724b #effefe bold',
    Token.Sidebar.Key.Description:                        'bg:#009f4b #effefe',
    Token.Sidebar.HelpText:                               'bg:#005b07 #d8fefe',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#efe3fe #effefe',
    Token.History.Line.Current:                           'bg:#004500 #effefe',
    Token.History.Line.Selected.Current:                  'bg:#39458f #effefe',
    Token.History.ExistingInput:                          '           #39e38f',
    Token.Window.Border:                                  '           #00fefe',
    Token.Window.Title:                                   'bg:#009f4b #effefe',
    Token.Window.TIItleV2:                                'bg:#00e3bc #effefe bold',
    Token.AcceptMessage:                                  'bg:#394500 #94fee9',
    Token.ExitConfirmation:                               'bg:#94fe8f #004500',
    Token.LineNumber:                                     'bg:#00721d #23cdd3',
    Token.SearchMatch:                                    'bg:#7d9f4b #effefe',
    Token.SearchMatch.Current:                            'bg:#00fe4b #effefe',
    Token.SelectedText:                                   'bg:#7dcd78 #effefe',
    Token.Toolbar.Completions:                            'bg:#004500 #00feef',
    Token.Toolbar.Completions.Arrow:                      'bg:#004500 #00feef bold',
    Token.Toolbar.Completions.Completion:                 'bg:#004500 #00feef',
    Token.Toolbar.Completions.Completion.Current:         'bg:#effefe #00b17d',
    Token.Menu.Completions.Completion:                    'bg:#004500 #00fefe',
    Token.Menu.Completions.Completion.Current:            'bg:#00fefe #004500',
    Token.Menu.Completions.Meta:                          'bg:#004500 #00cffe',
    Token.Menu.Completions.Meta.Current:                  'bg:#004500 #00edfe',
    Token.Menu.Completions.ProgressBar:                   'bg:#b5edfe           ',
    Token.Menu.Completions.ProgressButton:                'bg:#00454d           ',
})
splicer2=temp



temp = {
    Token.LineNumber:                                     'bg:#007200 #23cdd3',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fa0000 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #4500fe',
    Token.Out.Number:                                     '           #4500fe',
    Token.Separator:                                      '           #fe94e9',
    Token.Toolbar.Search:                                 '           #fe7d1d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fe7d1d noinherit',
    Token.Toolbar.Arg:                                    '           #fe7d1d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fe944b #450000',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fa5000 #feeffe bold',
    Token.Toolbar.Signature.Operator:                     '           #450000            bold',
    Token.Docstring:                                      '           #fa50a5',
    Token.Toolbar.Validation:                             'bg:#45004b #fe7dd3',
    Token.Toolbar.Status:                                 'bg:#72001d #fe7dd3',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#72001d #fe001d',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#72001d #7200d3',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#72001d #fe7dfe',
    Token.Toolbar.Status.Key:                             'bg:#450000 #fa50a5',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9f00d3 #feeffe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#722378 #fe7dd3',
    Token.Toolbar.Status.PythonVersion:                   'bg:#72001d #feeffe bold',
    Token.Aborted:                                        '           #fa50a5',
    Token.Sidebar:                                        'bg:#fe94e9 #450000',
    Token.Sidebar.Title:                                  'bg:#faef78 #feeffe bold',
    Token.Sidebar.Label:                                  'bg:#fe94e9 #72001d',
    Token.Sidebar.Status:                                 'bg:#fec1fe #450000',
    Token.Sidebar.Selected.Label:                         'bg:#72001d #fed8fe',
    Token.Sidebar.Selected.Status:                        'bg:#9f004b #feeffe bold',
    Token.Sidebar.Separator:                              'bg:#fe94e9 #feeffe underline',
    Token.Sidebar.Key:                                    'bg:#fe94e9 #450000 bold',
    Token.Sidebar.Key.Description:                        'bg:#fe94e9 #450000',
    Token.Sidebar.HelpText:                               'bg:#feeffe #450000',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#fa0000 #450000',
    Token.History.Line.Current:                           'bg:#feeffe #450000',
    Token.History.Line.Selected.Current:                  'bg:#fe50a5 #450000',
    Token.History.ExistingInput:                          '           #fa50a5',
    Token.Window.Border:                                  '           #459400',
    Token.Window.Title:                                   'bg:#fe94e9 #450000',
    Token.Window.TIItleV2:                                'bg:#fa9478 #450000 bold',
    Token.AcceptMessage:                                  'bg:#fe50fe #9f004b',
    Token.ExitConfirmation:                               'bg:#9f00a5 #feeffe',
}
temp.update({
    Token.Aborted:                                        '           #39e38f',
    Token.Sidebar:                                        'bg:#9f004b #feeffe',
    Token.Sidebar.Title:                                  'bg:#e300bc #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#9f004b #fec1fe',
    Token.Sidebar.Status:                                 'bg:#72001d #fed8fe',
    Token.Sidebar.Selected.Label:                         'bg:#fec1fe #5b0007',
    Token.Sidebar.Selected.Status:                        'bg:#fe94e9 #450000 bold',
    Token.Sidebar.Separator:                              'bg:#9f004b #450000 underline',
    Token.Sidebar.Key:                                    'bg:#72004b #feeffe bold',
    Token.Sidebar.Key.Description:                        'bg:#9f004b #feeffe',
    Token.Sidebar.HelpText:                               'bg:#5b0007 #fed8fe',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#e3effe #feeffe',
    Token.History.Line.Current:                           'bg:#450000 #feeffe',
    Token.History.Line.Selected.Current:                  'bg:#45398f #feeffe',
    Token.History.ExistingInput:                          '           #e3398f',
    Token.Window.Border:                                  '           #fe00fe',
    Token.Window.Title:                                   'bg:#9f004b #feeffe',
    Token.Window.TIItleV2:                                'bg:#e300bc #feeffe bold',
    Token.AcceptMessage:                                  'bg:#453900 #fe94e9',
    Token.ExitConfirmation:                               'bg:#fe948f #450000',
    Token.LineNumber:                                     'bg:#72001d #cd23d3',
    Token.SearchMatch:                                    'bg:#9f7d4b #feeffe',
    Token.SearchMatch.Current:                            'bg:#fe004b #feeffe',
    Token.SelectedText:                                   'bg:#cd7d78 #feeffe',
    Token.Toolbar.Completions:                            'bg:#450000 #fe00ef',
    Token.Toolbar.Completions.Arrow:                      'bg:#450000 #fe00ef bold',
    Token.Toolbar.Completions.Completion:                 'bg:#450000 #fe00ef',
    Token.Toolbar.Completions.Completion.Current:         'bg:#feeffe #b1007d',
    Token.Menu.Completions.Completion:                    'bg:#450000 #fe00fe',
    Token.Menu.Completions.Completion.Current:            'bg:#fe00fe #450000',
    Token.Menu.Completions.Meta:                          'bg:#450000 #cf00fe',
    Token.Menu.Completions.Meta.Current:                  'bg:#450000 #ed00fe',
    Token.Menu.Completions.ProgressBar:                   'bg:#edb5fe           ',
    Token.Menu.Completions.ProgressButton:                'bg:#45004d           ',
})
breeze=temp


temp = {
    Token.LineNumber:                                     'noinherit',
    Token.Prompt:                                         'noinherit',
    Token.Prompt.Dots:                                    'noinherit',
    Token.In:                                             'noinherit',
    Token.In.Number:                                      'noinherit',
    Token.Out:                                            'noinherit',
    Token.Out.Number:                                     'noinherit',
    Token.Separator:                                      'noinherit',
    Token.Toolbar.Search:                                 'noinherit',
    Token.Toolbar.Search.Text:                            'noinherit',
    Token.Toolbar.System:                                 'noinherit',
    Token.Toolbar.Arg:                                    'noinherit',
    Token.Toolbar.Arg.Text:                               'noinherit',
    Token.Toolbar.Signature:                              'noinherit',
    Token.Toolbar.Signature.CurrentName:                  'noinherit',
    Token.Toolbar.Signature.Operator:                     'noinherit',
    Token.Docstring:                                      'noinherit',
    Token.Toolbar.Validation:                             'noinherit',
    Token.Toolbar.Status:                                 'noinherit',
    Token.Toolbar.Status.BatteryPluggedIn:                'noinherit',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'noinherit',
    Token.Toolbar.Status.Title:                           'noinherit',
    Token.Toolbar.Status.InputMode:                       'noinherit',
    Token.Toolbar.Status.Key:                             'noinherit',
    Token.Toolbar.Status.PasteModeOn:                     'noinherit',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'noinherit',
    Token.Toolbar.Status.PythonVersion:                   'noinherit',
    Token.Aborted:                                        'noinherit',
    Token.Sidebar:                                        'noinherit',
    Token.Sidebar.Title:                                  'noinherit',
    Token.Sidebar.Label:                                  'noinherit',
    Token.Sidebar.Status:                                 'noinherit',
    Token.Sidebar.Selected.Label:                         'noinherit',
    Token.Sidebar.Selected.Status:                        'noinherit',
    Token.Sidebar.Separator:                              'noinherit',
    Token.Sidebar.Key:                                    'noinherit',
    Token.Sidebar.Key.Description:                        'noinherit',
    Token.Sidebar.HelpText:                               'noinherit',
    Token.History.Line:                                   'noinherit',
    Token.History.Line.Selected:                          'noinherit',
    Token.History.Line.Current:                           'noinherit',
    Token.History.Line.Selected.Current:                  'noinherit',
    Token.History.ExistingInput:                          'noinherit',
    Token.Window.Border:                                  'noinherit',
    Token.Window.Title:                                   'noinherit',
    Token.Window.TIItleV2:                                'noinherit',
    Token.AcceptMessage:                                  'noinherit',
    Token.ExitConfirmation:                               'noinherit',
}
temp.update({
    Token.Aborted:                                        'noinherit',
    Token.Sidebar:                                        'noinherit',
    Token.Sidebar.Title:                                  'noinherit',
    Token.Sidebar.Label:                                  'noinherit',
    Token.Sidebar.Status:                                 'noinherit',
    Token.Sidebar.Selected.Label:                         'noinherit',
    Token.Sidebar.Selected.Status:                        'noinherit',
    Token.Sidebar.Separator:                              'noinherit',
    Token.Sidebar.Key:                                    'noinherit',
    Token.Sidebar.Key.Description:                        'noinherit',
    Token.Sidebar.HelpText:                               'noinherit',
    Token.History.Line:                                   'noinherit',
    Token.History.Line.Selected:                          'noinherit underline',
    Token.History.Line.Current:                           'noinherit',
    Token.History.Line.Selected.Current:                  'noinherit',
    Token.History.ExistingInput:                          'noinherit',
    Token.Window.Border:                                  'noinherit',
    Token.Window.Title:                                   'noinherit',
    Token.Window.TIItleV2:                                'noinherit',
    Token.AcceptMessage:                                  'noinherit',
    Token.ExitConfirmation:                               'noinherit',
    Token.LineNumber:                                     'noinherit',
    Token.SearchMatch:                                    'noinherit',
    Token.SearchMatch.Current:                            'noinherit underline',
    Token.SelectedText:                                   'noinherit',
    Token.Toolbar.Completions:                            'noinherit',
    Token.Toolbar.Completions.Arrow:                      'noinherit',
    Token.Toolbar.Completions.Completion:                 'noinherit',
    Token.Toolbar.Completions.Completion.Current:         'noinherit underline',
    Token.Menu.Completions.Completion:                    'noinherit',
    Token.Menu.Completions.Completion.Current:            'noinherit underline',
    Token.Menu.Completions.Meta:                          'noinherit',
    Token.Menu.Completions.Meta.Current:                  'noinherit underline',
    Token.Menu.Completions.ProgressBar:                   'noinherit',
    Token.Menu.Completions.ProgressButton:                'noinherit',
})
plain=temp



temp = {
    Token.LineNumber:                                     'bg:#000000 #230000',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fa0000 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #450000',
    Token.Out.Number:                                     '           #450000',
    Token.Separator:                                      '           #fe0000',
    Token.Toolbar.Search:                                 '           #fe0000 noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fe0000 noinherit',
    Token.Toolbar.Arg:                                    '           #fe0000 noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fe0000 #450000',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fa0000 #fe0000 bold',
    Token.Toolbar.Signature.Operator:                     '           #450000            bold',
    Token.Docstring:                                      '           #fa0000',
    Token.Toolbar.Validation:                             'bg:#450000 #fe0000',
    Token.Toolbar.Status:                                 'bg:#720000 #fe0000',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#720000 #fe0000',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#720000 #720000',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#720000 #fe0000',
    Token.Toolbar.Status.Key:                             'bg:#450000 #fa0000',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9f0000 #fe0000',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#720000 #fe0000',
    Token.Toolbar.Status.PythonVersion:                   'bg:#720000 #fe0000 bold',
    Token.Aborted:                                        '           #fa0000',
    Token.Sidebar:                                        'bg:#fe0000 #450000',
    Token.Sidebar.Title:                                  'bg:#fa0000 #fe0000 bold',
    Token.Sidebar.Label:                                  'bg:#fe0000 #720000',
    Token.Sidebar.Status:                                 'bg:#fe0000 #450000',
    Token.Sidebar.Selected.Label:                         'bg:#720000 #fe0000',
    Token.Sidebar.Selected.Status:                        'bg:#9f0000 #fe0000 bold',
    Token.Sidebar.Separator:                              'bg:#fe0000 #fe0000 underline',
    Token.Sidebar.Key:                                    'bg:#fe0000 #450000 bold',
    Token.Sidebar.Key.Description:                        'bg:#fe0000 #450000',
    Token.Sidebar.HelpText:                               'bg:#fe0000 #450000',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#fa0000 #450000',
    Token.History.Line.Current:                           'bg:#fe0000 #450000',
    Token.History.Line.Selected.Current:                  'bg:#fe0000 #450000',
    Token.History.ExistingInput:                          '           #fa0000',
    Token.Window.Border:                                  '           #450000',
    Token.Window.Title:                                   'bg:#fe0000 #450000',
    Token.Window.TIItleV2:                                'bg:#fa0000 #450000 bold',
    Token.AcceptMessage:                                  'bg:#fe0000 #9f0000',
    Token.ExitConfirmation:                               'bg:#9f0000 #fe0000',
}                                                                                    
temp.update({                                                                      
    Token.Aborted:                                        '           #390000',
    Token.Sidebar:                                        'bg:#9f0000 #fe0000',
    Token.Sidebar.Title:                                  'bg:#e30000 #600000 bold',
    Token.Sidebar.Label:                                  'bg:#9f0000 #fe0000',
    Token.Sidebar.Status:                                 'bg:#720000 #fe0000',
    Token.Sidebar.Selected.Label:                         'bg:#fe0000 #5b0000',
    Token.Sidebar.Selected.Status:                        'bg:#fe0000 #450000 bold',
    Token.Sidebar.Separator:                              'bg:#9f0000 #450000 underline',
    Token.Sidebar.Key:                                    'bg:#720000 #fe0000 bold',
    Token.Sidebar.Key.Description:                        'bg:#9f0000 #fe0000',
    Token.Sidebar.HelpText:                               'bg:#5b0000 #fe0000',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#e30000 #fe0000',
    Token.History.Line.Current:                           'bg:#450000 #fe0000',
    Token.History.Line.Selected.Current:                  'bg:#450000 #fe0000',
    Token.History.ExistingInput:                          '           #e30000',
    Token.Window.Border:                                  '           #fe0000',
    Token.Window.Title:                                   'bg:#9f0000 #fe0000',
    Token.Window.TIItleV2:                                'bg:#e30000 #fe0000 bold',
    Token.AcceptMessage:                                  'bg:#450000 #fe0000',
    Token.ExitConfirmation:                               'bg:#fe0000 #450000',
    Token.LineNumber:                                     'bg:#720000 #cd0000',
    Token.SearchMatch:                                    'bg:#9f0000 #fe0000',
    Token.SearchMatch.Current:                            'bg:#fe0000 #fe0000',
    Token.SelectedText:                                   'bg:#cd0000 #fe0000',
    Token.Toolbar.Completions:                            'bg:#450000 #fe0000',
    Token.Toolbar.Completions.Arrow:                      'bg:#450000 #fe0000 bold',
    Token.Toolbar.Completions.Completion:                 'bg:#450000 #fe0000',
    Token.Toolbar.Completions.Completion.Current:         'bg:#fe0000 #b10000',
    Token.Menu.Completions.Completion:                    'bg:#450000 #fe0000',
    Token.Menu.Completions.Completion.Current:            'bg:#fe0000 #450000',
    Token.Menu.Completions.Meta:                          'bg:#450000 #cf0000',
    Token.Menu.Completions.Meta.Current:                  'bg:#450000 #ed0000',
    Token.Menu.Completions.ProgressBar:                   'bg:#ed0000           ',
    Token.Menu.Completions.ProgressButton:                'bg:#450000           ',
})
darkred=temp

temp = {
    Token.LineNumber:                                     'bg:#000000 #232323',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fafafa bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #454545',
    Token.Out.Number:                                     '           #454545',
    Token.Separator:                                      '           #fefefe',
    Token.Toolbar.Search:                                 '           #fefefe noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fefefe noinherit',
    Token.Toolbar.Arg:                                    '           #fefefe noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fefefe #454545',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fafafa #fefefe bold',
    Token.Toolbar.Signature.Operator:                     '           #454545            bold',
    Token.Docstring:                                      '           #fafafa',
    Token.Toolbar.Validation:                             'bg:#454545 #fefefe',
    Token.Toolbar.Status:                                 'bg:#727272 #fefefe',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#727272 #fefefe',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#727272 #727272',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#727272 #fefefe',
    Token.Toolbar.Status.Key:                             'bg:#454545 #fafafa',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9f9f9f #fefefe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#727272 #fefefe',
    Token.Toolbar.Status.PythonVersion:                   'bg:#727272 #fefefe bold',
    Token.Aborted:                                        '           #fafafa',
    Token.Sidebar:                                        'bg:#fefefe #454545',
    Token.Sidebar.Title:                                  'bg:#fafafa #fefefe bold',
    Token.Sidebar.Label:                                  'bg:#fefefe #727272',
    Token.Sidebar.Status:                                 'bg:#fefefe #454545',
    Token.Sidebar.Selected.Label:                         'bg:#727272 #fefefe',
    Token.Sidebar.Selected.Status:                        'bg:#9f9f9f #fefefe bold',
    Token.Sidebar.Separator:                              'bg:#fefefe #fefefe underline',
    Token.Sidebar.Key:                                    'bg:#fefefe #454545 bold',
    Token.Sidebar.Key.Description:                        'bg:#fefefe #454545',
    Token.Sidebar.HelpText:                               'bg:#fefefe #454545',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#fafafa #454545',
    Token.History.Line.Current:                           'bg:#fefefe #454545',
    Token.History.Line.Selected.Current:                  'bg:#fefefe #454545',
    Token.History.ExistingInput:                          '           #fafafa',
    Token.Window.Border:                                  '           #454545',
    Token.Window.Title:                                   'bg:#fefefe #454545',
    Token.Window.TIItleV2:                                'bg:#fafafa #454545 bold',
    Token.AcceptMessage:                                  'bg:#fefefe #9f9f9f',
    Token.ExitConfirmation:                               'bg:#9f9f9f #fefefe',
}
temp.update({
    Token.Aborted:                                        '           #393939',
    Token.Sidebar:                                        'bg:#9f9f9f #fefefe',
    Token.Sidebar.Title:                                  'bg:#e3e3e3 #606060 bold',
    Token.Sidebar.Label:                                  'bg:#9f9f9f #fefefe',
    Token.Sidebar.Status:                                 'bg:#727272 #fefefe',
    Token.Sidebar.Selected.Label:                         'bg:#fefefe #5b5b5b',
    Token.Sidebar.Selected.Status:                        'bg:#fefefe #454545 bold',
    Token.Sidebar.Separator:                              'bg:#9f9f9f #454545 underline',
    Token.Sidebar.Key:                                    'bg:#727272 #fefefe bold',
    Token.Sidebar.Key.Description:                        'bg:#9f9f9f #fefefe',
    Token.Sidebar.HelpText:                               'bg:#5b5b5b #fefefe',
    Token.History.Line:                                   '',
    Token.History.Line.Selected:                          'bg:#e3e3e3 #fefefe',
    Token.History.Line.Current:                           'bg:#454545 #fefefe',
    Token.History.Line.Selected.Current:                  'bg:#454545 #fefefe',
    Token.History.ExistingInput:                          '           #e3e3e3',
    Token.Window.Border:                                  '           #fefefe',
    Token.Window.Title:                                   'bg:#9f9f9f #fefefe',
    Token.Window.TIItleV2:                                'bg:#e3e3e3 #fefefe bold',
    Token.AcceptMessage:                                  'bg:#454545 #fefefe',
    Token.ExitConfirmation:                               'bg:#fefefe #454545',
    Token.LineNumber:                                     'bg:#727272 #cdcdcd',
    Token.SearchMatch:                                    'bg:#9f9f9f #fefefe',
    Token.SearchMatch.Current:                            'bg:#fefefe #fefefe',
    Token.SelectedText:                                   'bg:#cdcdcd #fefefe',
    Token.Toolbar.Completions:                            'bg:#454545 #fefefe',
    Token.Toolbar.Completions.Arrow:                      'bg:#454545 #fefefe bold',
    Token.Toolbar.Completions.Completion:                 'bg:#454545 #fefefe',
    Token.Toolbar.Completions.Completion.Current:         'bg:#fefefe #b1b1b1',
    Token.Menu.Completions.Completion:                    'bg:#454545 #fefefe',
    Token.Menu.Completions.Completion.Current:            'bg:#fefefe #454545',
    Token.Menu.Completions.Meta:                          'bg:#454545 #cfcfcf',
    Token.Menu.Completions.Meta.Current:                  'bg:#454545 #ededed',
    Token.Menu.Completions.ProgressBar:                   'bg:#ededed           ',
    Token.Menu.Completions.ProgressButton:                'bg:#454545           ',
})
silver=temp



# #USE THIS AS A COMPLETE TEMPLATE FOR FUTURE STYLES. THIS TEMPLATE CREATES A STYLE IDENTICAL TO THAT OF STARS (aka inverted_3)
# stars={
#     Token.LineNumber:                                     '#aa6666 bg:#002222                    ',
#     Token.Prompt:                                         '                   bold               ',
#     Token.Prompt.Dots:                                    '                             noinherit',
#     Token.In:                                             '#008800            bold               ',
#     Token.In.Number:                                      '                                      ',
#     Token.Out:                                            '#ff0000                               ',
#     Token.Out.Number:                                     '#ff0000                               ',
#     Token.Separator:                                      '#bbbbbb                               ',
#     Token.Toolbar.Search:                                 '#22aaaa                      noinherit',
#     Token.Toolbar.Search.Text:                            '                             noinherit',
#     Token.Toolbar.System:                                 '#22aaaa                      noinherit',
#     Token.Toolbar.Arg:                                    '#22aaaa                      noinherit',
#     Token.Toolbar.Arg.Text:                               '                             noinherit',
#     Token.Toolbar.Signature:                              '#000000 bg:#44bbbb                    ',
#     Token.Toolbar.Signature.CurrentName:                  '#ffffff bg:#008888 bold               ',
#     Token.Toolbar.Signature.Operator:                     '#000000            bold               ',
#     Token.Docstring:                                      '#888888                               ',
#     Token.Toolbar.Validation:                             '#aaaaaa bg:#440000                    ',
#     Token.Toolbar.Status:                                 '#aaaaaa bg:#222222                    ',
#     Token.Toolbar.Status.BatteryPluggedIn:                '#22aa22 bg:#222222                    ',
#     Token.Toolbar.Status.BatteryNotPluggedIn:             '#aa2222 bg:#222222                    ',
#     Token.Toolbar.Status.Title:                           '                   underline          ',
#     Token.Toolbar.Status.InputMode:                       '#ffffaa bg:#222222                    ',
#     Token.Toolbar.Status.Key:                             '#888888 bg:#000000                    ',
#     Token.Toolbar.Status.PasteModeOn:                     '#ffffff bg:#aa4444                    ',
#     Token.Toolbar.Status.PseudoTerminalCurrentVariable:   '#aaaaaa bg:#662266                    ',
#     Token.Toolbar.Status.PythonVersion:                   '#ffffff bg:#222222 bold               ',
#     Token.Aborted:                                        '#888888                               ',
#     Token.Sidebar:                                        '#000000 bg:#bbbbbb                    ',
#     Token.Sidebar.Title:                                  '#ffffff bg:#6688ff bold               ',
#     Token.Sidebar.Label:                                  '#222222 bg:#bbbbbb                    ',
#     Token.Sidebar.Status:                                 '#000011 bg:#dddddd                    ',
#     Token.Sidebar.Selected.Label:                         '#eeeeee bg:#222222                    ',
#     Token.Sidebar.Selected.Status:                        '#ffffff bg:#444444 bold               ',
#     Token.Sidebar.Separator:                              '#ffffff bg:#bbbbbb underline          ',
#     Token.Sidebar.Key:                                    '#000000 bg:#bbddbb bold               ',
#     Token.Sidebar.Key.Description:                        '#000000 bg:#bbbbbb                    ',
#     Token.Sidebar.HelpText:                               '#000011 bg:#eeeeff                    ',
#     Token.History.Line:                                   '                                      ',
#     Token.History.Line.Selected:                          '#000000 bg:#008800                    ',
#     Token.History.Line.Current:                           '#000000 bg:#ffffff                    ',
#     Token.History.Line.Selected.Current:                  '#000000 bg:#88ff88                    ',
#     Token.History.ExistingInput:                          '#888888                               ',
#     Token.Window.Border:                                  '#0000bb                               ',
#     Token.Window.Title:                                   '#000000 bg:#bbbbbb                    ',
#     Token.Window.TIItleV2:                                '#000000 bg:#6688bb bold               ',
#     Token.AcceptMessage:                                  '#444444 bg:#ffff88                    ',
#     Token.ExitConfirmation:                               '#ffffff bg:#884444                    ',
#     Token.Aborted:                                        '#777777                      noinherit',
#     Token.Sidebar:                                        '#ffffff bg:#444444           noinherit',
#     Token.Sidebar.Title:                                  '#080808 bg:#997700 bold      noinherit',
#     Token.Sidebar.Label:                                  '#dddddd bg:#444444           noinherit',
#     Token.Sidebar.Status:                                 '#ffffee bg:#222222           noinherit',
#     Token.Sidebar.Selected.Label:                         '#111111 bg:#dddddd           noinherit',
#     Token.Sidebar.Selected.Status:                        '#080808 bg:#bbbbbb bold      noinherit',
#     Token.Sidebar.Separator:                              '#080808 bg:#444444 underline noinherit',
#     Token.Sidebar.Key:                                    '#ffffff bg:#442244 bold      noinherit',
#     Token.Sidebar.Key.Description:                        '#ffffff bg:#444444           noinherit',
#     Token.Sidebar.HelpText:                               '#ffffee bg:#111100           noinherit',
#     Token.History.Line:                                   '                             noinherit',
#     Token.History.Line.Selected:                          '#ffffff bg:#ff77ff           noinherit',
#     Token.History.Line.Current:                           '#ffffff bg:#000000           noinherit',
#     Token.History.Line.Selected.Current:                  '#ffffff bg:#770077           noinherit',
#     Token.History.ExistingInput:                          '#777777                      noinherit',
#     Token.Window.Border:                                  '#ffff44                      noinherit',
#     Token.Window.Title:                                   '#ffffff bg:#444444           noinherit',
#     Token.Window.TIItleV2:                                '#ffffff bg:#997744 bold      noinherit',
#     Token.AcceptMessage:                                  '#bbbbbb bg:#000077           noinherit',
#     Token.ExitConfirmation:                               '#080808 bg:#77bbbb           noinherit',
#     Token.LineNumber:                                     '#aa6666 bg:#222222           noinherit',
#     Token.SearchMatch:                                    '#ffffff bg:#4444aa           noinherit',
#     Token.SearchMatch.Current:                            '#ffffff bg:#44aa44           noinherit',
#     Token.SelectedText:                                   '#ffffff bg:#6666aa           noinherit',
#     Token.Toolbar.Completions.Arrow:                      '#bf954c bg:#000046 bold      noinherit',
#     Token.Toolbar.Completions.Completion:                 '#bf954c bg:#000046           noinherit',
#     Token.Toolbar.Completions.Completion.Current:         '#6a5100 bg:#f0ffff           noinherit',
#     Token.Menu.Completions.Completion:                    '#ff954c bg:#202046           noinherit',
#     Token.Menu.Completions.Completion.Current:            '#202046 bg:#ff954c           noinherit',
#     Token.Menu.Completions.Meta:                          '#ff684c bg:#000046           noinherit',
#     Token.Menu.Completions.Meta.Current:                  '#ff7e00 bg:#000046           noinherit',
#     Token.Menu.Completions.ProgressBar:                   '        bg:#ff7ed4           noinherit',
#     Token.Menu.Completions.ProgressButton:                '        bg:#460000           noinherit',
# }

dark = {}
dark.update(default_ui_style)
dark.update({
    Token.Aborted:                                '#777777                      ',
    Token.Sidebar:                                '#ffffff bg:#444444           ',
    Token.Sidebar.Title:                          '#000000 bg:#777777 bold      ',
    Token.Sidebar.Label:                          '#dddddd bg:#444444           ',
    Token.Sidebar.Status:                         '#ffffff bg:#222222           ',
    Token.Sidebar.Selected.Label:                 '#111111 bg:#dddddd           ',
    Token.Sidebar.Selected.Status:                '#000000 bg:#bbbbbb bold      ',
    Token.Sidebar.Separator:                      '#000000 bg:#444444 underline ',
    Token.Sidebar.Key:                            '#ffffff bg:#222222 bold      ',
    Token.Sidebar.Key.Description:                '#ffffff bg:#444444           ',
    Token.Sidebar.HelpText:                       '#ffffff bg:#111111           ',
    Token.History.Line:                           '                             ',
    Token.History.Line.Selected:                  '#ffffff bg:#777777           ',
    Token.History.Line.Current:                   '#ffffff bg:#000000           ',
    Token.History.Line.Selected.Current:          '#ffffff bg:#000000           ',
    Token.History.ExistingInput:                  '#777777                      ',
    Token.Window.Border:                          '#ffffff                      ',
    Token.Window.Title:                           '#ffffff bg:#444444           ',
    Token.Window.TIItleV2:                        '#ffffff bg:#777777 bold      ',
    Token.AcceptMessage:                          '#bbbbbb bg:#000000           ',
    Token.ExitConfirmation:                       '#000000 bg:#bbbbbb           ',
    Token.LineNumber:                             '#666666 bg:#222222           ',
    Token.SearchMatch:                            '#ffffff bg:#444444           ',
    Token.SearchMatch.Current:                    '#ffffff bg:#aaaaaa           ',
    Token.SelectedText:                           '#ffffff bg:#666666           ',
    Token.Toolbar.Completions.Arrow:              '#959595 bg:#000000 bold      ',
    Token.Toolbar.Completions.Completion:         '#959595 bg:#000000           ',
    Token.Toolbar.Completions.Completion.Current: '#515151 bg:#ffffff           ',
    Token.Menu.Completions.Completion:            '#959595 bg:#202020           ',
    Token.Menu.Completions.Completion.Current:    '#202020 bg:#959595           ',
    Token.Menu.Completions.Meta:                  '#686868 bg:#000000           ',
    Token.Menu.Completions.Meta.Current:          '#7e7e7e bg:#000000           ',
    Token.Menu.Completions.ProgressBar:           '        bg:#7e7e7e           ',
    Token.Menu.Completions.ProgressButton:        '        bg:#000000           ',
})



chirpy={
    Token.LineNumber:                                     '#aa66aa bg:#220022                    ',
    Token.Prompt:                                         '                   bold               ',
    Token.Prompt.Dots:                                    '                             noinherit',
    Token.In:                                             '#008800            bold               ',
    Token.In.Number:                                      '                                      ',
    Token.Out:                                            '#ff00ff                               ',
    Token.Out.Number:                                     '#ff00ff                               ',
    Token.Separator:                                      '#bbbbbb                               ',
    Token.Toolbar.Search:                                 '#22aa22                      noinherit',
    Token.Toolbar.Search.Text:                            '                             noinherit',
    Token.Toolbar.System:                                 '#22aa22                      noinherit',
    Token.Toolbar.Arg:                                    '#22aa22                      noinherit',
    Token.Toolbar.Arg.Text:                               '                             noinherit',
    Token.Toolbar.Signature:                              '#000000 bg:#bb44bb                    ',
    Token.Toolbar.Signature.CurrentName:                  '#ffffff bg:#880088 bold               ',
    Token.Toolbar.Signature.Operator:                     '#000000            bold               ',
    Token.Docstring:                                      '#888888                               ',
    Token.Toolbar.Validation:                             '#aaaaaa bg:#004400                    ',
    Token.Toolbar.Status:                                 '#aaaaaa bg:#222222                    ',
    Token.Toolbar.Status.BatteryPluggedIn:                '#22aa22 bg:#222222                    ',
    Token.Toolbar.Status.BatteryNotPluggedIn:             '#aa22aa bg:#222222                    ',
    Token.Toolbar.Status.Title:                           '                   underline          ',
    Token.Toolbar.Status.InputMode:                       '#ffffff bg:#222222                    ',
    Token.Toolbar.Status.Key:                             '#888888 bg:#000000                    ',
    Token.Toolbar.Status.PasteModeOn:                     '#ffffff bg:#44aa44                    ',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   '#aaaaaa bg:#226622                    ',
    Token.Toolbar.Status.PythonVersion:                   '#ffffff bg:#222222 bold               ',
    Token.Aborted:                                        '#888888                               ',
    Token.Sidebar:                                        '#000000 bg:#bbbbbb                    ',
    Token.Sidebar.Title:                                  '#ffffff bg:#886688 bold               ',
    Token.Sidebar.Label:                                  '#222222 bg:#bbbbbb                    ',
    Token.Sidebar.Status:                                 '#000000 bg:#dddddd                    ',
    Token.Sidebar.Selected.Label:                         '#eeeeee bg:#222222                    ',
    Token.Sidebar.Selected.Status:                        '#ffffff bg:#444444 bold               ',
    Token.Sidebar.Separator:                              '#ffffff bg:#bbbbbb underline          ',
    Token.Sidebar.Key:                                    '#000000 bg:#ddbbdd bold               ',
    Token.Sidebar.Key.Description:                        '#000000 bg:#bbbbbb                    ',
    Token.Sidebar.HelpText:                               '#000000 bg:#eeeeee                    ',
    Token.History.Line:                                   '                                      ',
    Token.History.Line.Selected:                          '#000000 bg:#880088                    ',
    Token.History.Line.Current:                           '#000000 bg:#ffffff                    ',
    Token.History.Line.Selected.Current:                  '#000000 bg:#ff88ff                    ',
    Token.History.ExistingInput:                          '#888888                               ',
    Token.Window.Border:                                  '#000000                               ',
    Token.Window.Title:                                   '#000000 bg:#bbbbbb                    ',
    Token.Window.TIItleV2:                                '#000000 bg:#886688 bold               ',
    Token.AcceptMessage:                                  '#444444 bg:#ffffff                    ',
    Token.ExitConfirmation:                               '#ffffff bg:#448844                    ',
    Token.Aborted:                                        '#777777                      noinherit',
    Token.Sidebar:                                        '#ffffff bg:#444444           noinherit',
    Token.Sidebar.Title:                                  '#080808 bg:#779977 bold      noinherit',
    Token.Sidebar.Label:                                  '#dddddd bg:#444444           noinherit',
    Token.Sidebar.Status:                                 '#ffffff bg:#222222           noinherit',
    Token.Sidebar.Selected.Label:                         '#111111 bg:#dddddd           noinherit',
    Token.Sidebar.Selected.Status:                        '#080808 bg:#bbbbbb bold      noinherit',
    Token.Sidebar.Separator:                              '#080808 bg:#444444 underline noinherit',
    Token.Sidebar.Key:                                    '#ffffff bg:#224422 bold      noinherit',
    Token.Sidebar.Key.Description:                        '#ffffff bg:#444444           noinherit',
    Token.Sidebar.HelpText:                               '#ffffff bg:#111111           noinherit',
    Token.History.Line:                                   '                             noinherit',
    Token.History.Line.Selected:                          '#ffffff bg:#77ff77           noinherit',
    Token.History.Line.Current:                           '#ffffff bg:#000000           noinherit',
    Token.History.Line.Selected.Current:                  '#ffffff bg:#007700           noinherit',
    Token.History.ExistingInput:                          '#777777                      noinherit',
    Token.Window.Border:                                  '#ffffff                      noinherit',
    Token.Window.Title:                                   '#ffffff bg:#444444           noinherit',
    Token.Window.TIItleV2:                                '#ffffff bg:#779977 bold      noinherit',
    Token.AcceptMessage:                                  '#bbbbbb bg:#000000           noinherit',
    Token.ExitConfirmation:                               '#080808 bg:#bb77bb           noinherit',
    Token.LineNumber:                                     '#aa66aa bg:#222222           noinherit',
    Token.SearchMatch:                                    '#ffffff bg:#444444           noinherit',
    Token.SearchMatch.Current:                            '#ffffff bg:#aa44aa           noinherit',
    Token.SelectedText:                                   '#ffffff bg:#666666           noinherit',
    Token.Toolbar.Completions.Arrow:                      '#bf95bf bg:#000000 bold      noinherit',
    Token.Toolbar.Completions.Completion:                 '#bf95bf bg:#000000           noinherit',
    Token.Toolbar.Completions.Completion.Current:         '#6a516a bg:#fff0ff           noinherit',
    Token.Menu.Completions.Completion:                    '#ff95ff bg:#202020           noinherit',
    Token.Menu.Completions.Completion.Current:            '#202020 bg:#95ff95           noinherit',
    Token.Menu.Completions.Meta:                          '#ff68ff bg:#000000           noinherit',
    Token.Menu.Completions.Meta.Current:                  '#ff7eff bg:#000000           noinherit',
    Token.Menu.Completions.ProgressBar:                   '        bg:#7eff7e           noinherit',
    Token.Menu.Completions.ProgressButton:                '        bg:#004600           noinherit',
}

jenny=plain.copy()
jenny.update({
    Token.LineNumber:                                     '#aa66aa           noinherit',
    Token.Prompt:                                         '        bold      noinherit',
    Token.Prompt.Dots:                                    '                  noinherit',
    Token.In:                                             '#008800 bold      noinherit',
    Token.In.Number:                                      '                  noinherit',
    Token.Out:                                            '#ff00ff           noinherit',
    Token.Out.Number:                                     '#ff00ff           noinherit',
    Token.Separator:                                      '#bbbbbb           noinherit',
    Token.Toolbar.Search:                                 '#22aa22           noinherit',
    Token.Toolbar.Search.Text:                            '                  noinherit',
    Token.Toolbar.System:                                 '#22aa22           noinherit',
    Token.Toolbar.Arg:                                    '#22aa22           noinherit',
    Token.Toolbar.Arg.Text:                               '                  noinherit',
    Token.Toolbar.Signature:                              '#808080           noinherit',
    Token.Toolbar.Signature.CurrentName:                  '#ffffff bold      noinherit',
    Token.Toolbar.Signature.Operator:                     '#808080 bold      noinherit',
    Token.Docstring:                                      '#888888           noinherit',
    Token.Toolbar.Validation:                             '#aaaaaa           noinherit',
    Token.Toolbar.Status:                                 '#aaaaaa           noinherit',
    Token.Toolbar.Status.BatteryPluggedIn:                '#22aa22           noinherit',
    Token.Toolbar.Status.BatteryNotPluggedIn:             '#aa22aa           noinherit',
    Token.Toolbar.Status.Title:                           '        underline noinherit',
    Token.Toolbar.Status.InputMode:                       '#ffffff           noinherit',
    Token.Toolbar.Status.Key:                             '#888888           noinherit',
    Token.Toolbar.Status.PasteModeOn:                     '#ffffff           noinherit',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   '#aaaaaa           noinherit',
    Token.Toolbar.Status.PythonVersion:                   '#ffffff bold      noinherit',
    Token.Aborted:                                        '#888888           noinherit',
    Token.Sidebar:                                        '#808080           noinherit',
    Token.Sidebar.Title:                                  '#ffffff bold      noinherit',
    Token.Sidebar.Label:                                  '#222222           noinherit',
    Token.Sidebar.Status:                                 '#808080           noinherit',
    Token.Sidebar.Selected.Label:                         '#eeeeee           noinherit',
    Token.Sidebar.Selected.Status:                        '#ffffff bold      noinherit',
    Token.Sidebar.Separator:                              '#ffffff underline noinherit',
    Token.Sidebar.Key:                                    '#808080 bold      noinherit',
    Token.Sidebar.Key.Description:                        '#808080           noinherit',
    Token.Sidebar.HelpText:                               '#808080           noinherit',
    Token.History.Line:                                   '                  noinherit',
    Token.History.Line.Selected:                          '#808080           noinherit',
    Token.History.Line.Current:                           '#808080           noinherit',
    Token.History.Line.Selected.Current:                  '#808080           noinherit',
    Token.History.ExistingInput:                          '#888888           noinherit',
    Token.Window.Border:                                  '#808080           noinherit',
    Token.Window.Title:                                   '#808080           noinherit',
    Token.Window.TIItleV2:                                '#808080 bold      noinherit',
    Token.AcceptMessage:                                  '#444444           noinherit',
    Token.ExitConfirmation:                               '#ffffff           noinherit',
    Token.Aborted:                                        '#777777           noinherit',
    Token.Sidebar:                                        '#ffffff           noinherit',
    Token.Sidebar.Title:                                  '#808080 bold      noinherit',
    Token.Sidebar.Label:                                  '#dddddd           noinherit',
    Token.Sidebar.Status:                                 '#ffffff           noinherit',
    Token.Sidebar.Selected.Label:                         '#ffffff underline noinherit',
    Token.Sidebar.Selected.Status:                        '#808080 bold      noinherit',
    Token.Sidebar.Separator:                              '#808080           noinherit',
    Token.Sidebar.Key:                                    '#ffffff bold      noinherit',
    Token.Sidebar.Key.Description:                        '#ffffff           noinherit',
    Token.Sidebar.HelpText:                               '#ffffff           noinherit',
    Token.History.Line:                                   '                  noinherit',
    Token.History.Line.Selected:                          '#ffffff           noinherit',
    Token.History.Line.Current:                           '#ffffff           noinherit',
    Token.History.Line.Selected.Current:                  '#ffffff           noinherit',
    Token.History.ExistingInput:                          '#777777           noinherit',
    Token.Window.Border:                                  '#ffffff           noinherit',
    Token.Window.Title:                                   '#ffffff           noinherit',
    Token.Window.TIItleV2:                                '#ffffff bold      noinherit',
    Token.AcceptMessage:                                  '#bbbbbb           noinherit',
    Token.ExitConfirmation:                               '#808080           noinherit',
    Token.LineNumber:                                     '#aa66aa           noinherit',
    Token.SearchMatch:                                    '#ffffff           noinherit',
    Token.SearchMatch.Current:                            '#ffffff           noinherit',
    Token.SelectedText:                                   '#ffffff           noinherit',
    Token.Toolbar.Completions.Arrow:                      '#bf95bf underline noinherit',
    Token.Toolbar.Completions.Completion:                 '#bf95bf           noinherit',
    Token.Toolbar.Completions.Completion.Current:         '#FFFFFF underline noinherit',
    Token.Menu.Completions.Completion:                    '#ff95ff           noinherit',
    Token.Menu.Completions.Completion.Current:            '#FFFFFF underline noinherit',
    Token.Menu.Completions.Meta:                          '#ff68ff           noinherit',
    Token.Menu.Completions.Meta.Current:                  '#ff7eff           noinherit',
    Token.Menu.Completions.ProgressBar:                   '                  noinherit',
    Token.Menu.Completions.ProgressButton:                '                  noinherit',
})




random=plain.copy()
random.update({
    Token.LineNumber:                                    random_style(),
    Token.Prompt:                                        random_style(),
    Token.Prompt.Dots:                                   random_style(),
    Token.In:                                            random_style(),
    Token.In.Number:                                     random_style(),
    Token.Out:                                           random_style(),
    Token.Out.Number:                                    random_style(),
    Token.Separator:                                     random_style(),
    Token.Toolbar.Search:                                random_style(),
    Token.Toolbar.Search.Text:                           random_style(),
    Token.Toolbar.System:                                random_style(),
    Token.Toolbar.Arg:                                   random_style(),
    Token.Toolbar.Arg.Text:                              random_style(),
    Token.Toolbar.Signature:                             random_style(),
    Token.Toolbar.Signature.CurrentName:                 random_style(),
    Token.Toolbar.Signature.Operator:                    random_style(),
    Token.Docstring:                                     random_style(),
    Token.Toolbar.Validation:                            random_style(),
    Token.Toolbar.Status:                                random_style(),
    Token.Toolbar.Status.BatteryPluggedIn:               random_style(),
    Token.Toolbar.Status.BatteryNotPluggedIn:            random_style(),
    Token.Toolbar.Status.Title:                          random_style(),
    Token.Toolbar.Status.InputMode:                      random_style(),
    Token.Toolbar.Status.Key:                            random_style(),
    Token.Toolbar.Status.PasteModeOn:                    random_style(),
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:  random_style(),
    Token.Toolbar.Status.PythonVersion:                  random_style(),
    Token.Aborted:                                       random_style(),
    Token.Sidebar:                                       random_style(),
    Token.Sidebar.Title:                                 random_style(),
    Token.Sidebar.Label:                                 random_style(),
    Token.Sidebar.Status:                                random_style(),
    Token.Sidebar.Selected.Label:                        random_style(),
    Token.Sidebar.Selected.Status:                       random_style(),
    Token.Sidebar.Separator:                             random_style(),
    Token.Sidebar.Key:                                   random_style(),
    Token.Sidebar.Key.Description:                       random_style(),
    Token.Sidebar.HelpText:                              random_style(),
    Token.History.Line:                                  random_style(),
    Token.History.Line.Selected:                         random_style(),
    Token.History.Line.Current:                          random_style(),
    Token.History.Line.Selected.Current:                 random_style(),
    Token.History.ExistingInput:                         random_style(),
    Token.Window.Border:                                 random_style(),
    Token.Window.Title:                                  random_style(),
    Token.Window.TIItleV2:                               random_style(),
    Token.AcceptMessage:                                 random_style(),
    Token.ExitConfirmation:                              random_style(),
    Token.Aborted:                                       random_style(),
    Token.Sidebar:                                       random_style(),
    Token.Sidebar.Title:                                 random_style(),
    Token.Sidebar.Label:                                 random_style(),
    Token.Sidebar.Status:                                random_style(),
    Token.Sidebar.Selected.Label:                        random_style(),
    Token.Sidebar.Selected.Status:                       random_style(),
    Token.Sidebar.Separator:                             random_style(),
    Token.Sidebar.Key:                                   random_style(),
    Token.Sidebar.Key.Description:                       random_style(),
    Token.Sidebar.HelpText:                              random_style(),
    Token.History.Line:                                  random_style(),
    Token.History.Line.Selected:                         random_style(),
    Token.History.Line.Current:                          random_style(),
    Token.History.Line.Selected.Current:                 random_style(),
    Token.History.ExistingInput:                         random_style(),
    Token.Window.Border:                                 random_style(),
    Token.Window.Title:                                  random_style(),
    Token.Window.TIItleV2:                               random_style(),
    Token.AcceptMessage:                                 random_style(),
    Token.ExitConfirmation:                              random_style(),
    Token.LineNumber:                                    random_style(),
    Token.SearchMatch:                                   random_style(),
    Token.SearchMatch.Current:                           random_style(),
    Token.SelectedText:                                  random_style(),
    Token.Toolbar.Completions.Arrow:                     random_style(),
    Token.Toolbar.Completions.Completion:                random_style(),
    Token.Toolbar.Completions.Completion.Current:        random_style(),
    Token.Menu.Completions.Completion:                   random_style(),
    Token.Menu.Completions.Completion.Current:           random_style(),
    Token.Menu.Completions.Meta:                         random_style(),
    Token.Menu.Completions.Meta.Current:                 random_style(),
    Token.Menu.Completions.ProgressBar:                  random_style(),
    Token.Menu.Completions.ProgressButton:               random_style(),
})

dracula={
    Token                                              : '                                  ',
    Token.Aborted                                      : '#84bbc9                           ',
    Token.AcceptMessage                                : '#37616e    bg:#86cdb8             ',
    Token.AutoSuggestion                               : '#666666                           ',
    Token.ColorColumn                                  : '           bg:#ccaacc             ',
    Token.Comment                                      : '#6272a4                           ',
    Token.Comment.Hashbang                             : '#6272a4                           ',
    Token.Comment.Multiline                            : '#6272a4                           ',
    Token.Comment.Preproc                              : '#ff79c6                           ',
    Token.Comment.PreprocFile                          : '#6272a4                           ',
    Token.Comment.Single                               : '#6272a4                           ',
    Token.Comment.Special                              : '#6272a4                           ',
    Token.CursorColumn                                 : '           bg:#3c464a             ',
    Token.CursorLine                                   : '                         bg:#2a3438',
    Token.Digraph                                      : '#4444ff                           ',
    Token.Docstring                                    : '#84bbc9                           ',
    Token.Error                                        : '#f8f8f2                           ',
    Token.Escape                                       : '                                  ',
    Token.ExitConfirmation                             : '#c6cdca    bg:#3a7460             ',
    Token.Generic                                      : '#f8f8f2                           ',
    Token.Generic.Deleted                              : '#8b080b                           ',
    Token.Generic.Emph                                 : '#f8f8f2                  underline',
    Token.Generic.Error                                : '#f8f8f2                           ',
    Token.Generic.Heading                              : '#f8f8f2                  bold     ',
    Token.Generic.Inserted                             : '#f8f8f2                  bold     ',
    Token.Generic.Output                               : '#44475a                           ',
    Token.Generic.Prompt                               : '#f8f8f2                           ',
    Token.Generic.Strong                               : '#f8f8f2                           ',
    Token.Generic.Subheading                           : '#f8f8f2                  bold     ',
    Token.Generic.Traceback                            : '#f8f8f2                           ',
    Token.History.ExistingInput                        : '#84bbc9                           ',
    Token.History.Line                                 : '                                  ',
    Token.History.Line.Current                         : '#0a0c14    bg:#c6cdca             ',
    Token.History.Line.Selected                        : '#0a0c14    bg:#6482c9             ',
    Token.History.Line.Selected.Current                : '#0a0c14    bg:#86becd             ',
    Token.In                                           : '#6482c9                  bold     ',
    Token.In.Number                                    : '#6482c9                  bold     ',
    Token.Keyword                                      : '#ff79c6                           ',
    Token.Keyword.Constant                             : '#ff79c6                           ',
    Token.Keyword.Declaration                          : '#8be9fd                  italic   ',
    Token.Keyword.Namespace                            : '#ff79c6                           ',
    Token.Keyword.Pseudo                               : '#ff79c6                           ',
    Token.Keyword.Reserved                             : '#ff79c6                           ',
    Token.Keyword.Type                                 : '#8be9fd                           ',
    Token.LineNumber                                   : '#5ea28b    bg:#203241             ',
    Token.LineNumber.Current                           : '#5ea28b    bg:#203241    bold     ',
    Token.Literal                                      : '#f8f8f2                           ',
    Token.Literal.Date                                 : '#f8f8f2                           ',
    Token.Literal.Number                               : '#ffb86c                           ',
    Token.Literal.Number.Bin                           : '#ffb86c                           ',
    Token.Literal.Number.Float                         : '#ffb86c                           ',
    Token.Literal.Number.Hex                           : '#ffb86c                           ',
    Token.Literal.Number.Integer                       : '#ffb86c                           ',
    Token.Literal.Number.Integer.Long                  : '#ffb86c                           ',
    Token.Literal.Number.Oct                           : '#ffb86c                           ',
    Token.Literal.String                               : '#bd93f9                           ',
    Token.Literal.String.Affix                         : '#bd93f9                           ',
    Token.Literal.String.Backtick                      : '#bd93f9                           ',
    Token.Literal.String.Char                          : '#bd93f9                           ',
    Token.Literal.String.Delimiter                     : '#bd93f9                           ',
    Token.Literal.String.Doc                           : '#bd93f9                           ',
    Token.Literal.String.Double                        : '#bd93f9                           ',
    Token.Literal.String.Escape                        : '#bd93f9                           ',
    Token.Literal.String.Heredoc                       : '#bd93f9                           ',
    Token.Literal.String.Interpol                      : '#bd93f9                           ',
    Token.Literal.String.Other                         : '#bd93f9                           ',
    Token.Literal.String.Regex                         : '#bd93f9                           ',
    Token.Literal.String.Single                        : '#bd93f9                           ',
    Token.Literal.String.Symbol                        : '#bd93f9                           ',
    Token.MatchingBracket                              : 'bold                              ',
    Token.MatchingBracket.Cursor                       : '#ffffff    bg:#ff3333    bold     ',
    Token.MatchingBracket.Other                        : '#ffffff    bg:#3333ff    bold     ',
    Token.Menu.Completions                             : '#000000    bg:#bbbbbb             ',
    Token.Menu.Completions.Completion                  : '#0a0c14    bg:#8d85cd             ',
    Token.Menu.Completions.Completion.Current          : '#c6cdca    bg:#6764c9             ',
    Token.Menu.Completions.Meta                        : '#0a0c14    bg:#858fcd             ',
    Token.Menu.Completions.Meta.Current                : '#0a0c14    bg:#7a66cd             ',
    Token.Menu.Completions.MultiColumnMeta             : '#000000    bg:#aaaaaa             ',
    Token.Menu.Completions.ProgressBar                 : '#000000    bg:#99cbcd             ',
    Token.Menu.Completions.ProgressButton              : '#000000    bg:#0a0c14             ',
    Token.MultipleCursors.Cursor                       : '#000000    bg:#ccccaa             ',
    Token.Name                                         : '#f8f8f2                           ',
    Token.Name.Attribute                               : '#50fa7b                           ',
    Token.Name.Builtin                                 : '#8be9fd                           ',
    Token.Name.Builtin.Pseudo                          : '#f8f8f2                           ',
    Token.Name.Class                                   : '#50fa7b                           ',
    Token.Name.Constant                                : '#f8f8f2                           ',
    Token.Name.Decorator                               : '#f8f8f2                           ',
    Token.Name.Entity                                  : '#f8f8f2                           ',
    Token.Name.Exception                               : '#f8f8f2                           ',
    Token.Name.Function                                : '#50fa7b                           ',
    Token.Name.Function.Magic                          : '#50fa7b                           ',
    Token.Name.Label                                   : '#8be9fd                  italic   ',
    Token.Name.Namespace                               : '#f8f8f2                           ',
    Token.Name.Other                                   : '#f8f8f2                           ',
    Token.Name.Property                                : '#f8f8f2                           ',
    Token.Name.Tag                                     : '#ff79c6                           ',
    Token.Name.Variable                                : '#8be9fd                  italic   ',
    Token.Name.Variable.Class                          : '#8be9fd                  italic   ',
    Token.Name.Variable.Global                         : '#8be9fd                  italic   ',
    Token.Name.Variable.Instance                       : '#8be9fd                  italic   ',
    Token.Name.Variable.Magic                          : '#8be9fd                  italic   ',
    Token.Operator                                     : '#ff79c6                           ',
    Token.Operator.Word                                : '#ff79c6                           ',
    Token.Other                                        : '#f8f8f2                           ',
    Token.Out                                          : '#68cd66                           ',
    Token.Out.Number                                   : '#68cd66                           ',
    Token.Prompt                                       : '                         bold     ',
    Token.Prompt.Arg                                   : '                                  ',
    Token.Prompt.Dots                                  : '                                  ',
    Token.Prompt.Search                                : '                                  ',
    Token.Prompt.Search.Text                           : '                                  ',
    Token.Punctuation                                  : '#e6e6fa                           ',
    Token.Scrollbar                                    : '           bg:#888888             ',
    Token.Scrollbar.Arrow                              : '#888888    bg:#222222    bold     ',
    Token.Scrollbar.Button                             : '           bg:#444444             ',
    Token.SearchMatch                                  : '#c6cdca    bg:#59516e             ',
    Token.SearchMatch.Current                          : '#c6cdca    bg:#66a3cd             ',
    Token.SelectedText                                 : '#c6cdca    bg:#7b829c             ',
    Token.Separator                                    : '#a1cdc8                           ',
    Token.Sidebar                                      : '#0a0c14    bg:#a1cdc8             ',
    Token.Sidebar.HelpText                             : '#0a0c14    bg:#c6cdca             ',
    Token.Sidebar.Key                                  : '#0a0c14    bg:#a1cdc8    bold     ',
    Token.Sidebar.Key.Description                      : '#0a0c14    bg:#a1cdc8    bold     ',
    Token.Sidebar.Label                                : '#203241    bg:#a1cdc8             ',
    Token.Sidebar.Selected.Label                       : '#bdcdc8    bg:#203241             ',
    Token.Sidebar.Selected.Status                      : '#c6cdca    bg:#37616e    bold     ',
    Token.Sidebar.Separator                            : '#c6cdca    bg:#a1cdc8    underline',
    Token.Sidebar.Status                               : '#0a0c14    bg:#b4cdc5             ',
    Token.Sidebar.Title                                : '#c6cdca    bg:#b494c9    bold     ',
    Token.Tab                                          : '#999999                           ',
    Token.Text                                         : '#f8f8f2                           ',
    Token.Text.Whitespace                              : '#f8f8f2                           ',
    Token.Tilde                                        : '#8888ff                           ',
    Token.Toolbar.Arg                                  : '#7e72cd                           ',
    Token.Toolbar.Arg.Text                             : '                                  ',
    Token.Toolbar.Completions                          : '#0a0c14    bg:#8d85cd             ',
    Token.Toolbar.Completions.Arrow                    : '#0a0c14    bg:#8d85cd    bold     ',
    Token.Toolbar.Completions.Completion               : '#0a0c14    bg:#8d85cd             ',
    Token.Toolbar.Completions.Completion.Current       : '#c6cdca    bg:#6764c9             ',
    Token.Toolbar.Search                               : '#7e72cd                           ',
    Token.Toolbar.Search.Text                          : '                                  ',
    Token.Toolbar.Signature                            : '#0a0c14    bg:#8d85cd             ',
    Token.Toolbar.Signature.CurrentName                : '#c6cdca    bg:#6764c9    bold     ',
    Token.Toolbar.Signature.Operator                   : '#0a0c14    bg:#8d85cd    bold     ',
    Token.Toolbar.Status                               : '#99cbcd    bg:#203241             ',
    Token.Toolbar.Status.BatteryNotPluggedIn           : '#51a264    bg:#203241             ',
    Token.Toolbar.Status.BatteryPluggedIn              : '#6691cd    bg:#203241             ',
    Token.Toolbar.Status.InputMode                     : '#99cdbd    bg:#203241             ',
    Token.Toolbar.Status.Key                           : '#84bbc9    bg:#0a0c14             ',
    Token.Toolbar.Status.PasteModeOn                   : '#c6cdca    bg:#51a275             ',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable : '#99cbcd    bg:#2e473e             ',
    Token.Toolbar.Status.PythonVersion                 : '#c6cdca    bg:#203241    bold     ',
    Token.Toolbar.Status.Title                         : '#99cbcd    bg:#203241    underline',
    Token.Toolbar.System                               : '#7e72cd                           ',
    Token.Toolbar.System.Text                          : '#7e72cd                           ',
    Token.Toolbar.Validation                           : '#99cbcd    bg:#0d1a15             ',
    Token.TrailingWhiteSpace                           : '#999999                           ',
    Token.Window.Border                                : '#633157                           ',
    Token.Window.TIItleV2                              : '#0a0c14    bg:#9498c9    bold     ',
    Token.Window.Title                                 : '#0a0c14    bg:#a1cdc8             ',
    Token.WindowTooSmall                               : '#ffffff    bg:#550000             ',
}

# DejaVu theme - a clean, modern theme with blue accents
dejavu = {Token.LineNumber: '#5f819d bg:#1d1f21', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #5f819d', Token.In.Number: '', Token.Out: '#81a2be', Token.Out.Number: '#81a2be', Token.Separator: '#cc6666', Token.Toolbar.Search: '#b5bd68 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#b5bd68 noinherit', Token.Toolbar.Arg: '#b5bd68 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#282a2e #c5c8c6', Token.Toolbar.Signature.CurrentName: 'bg:#1d1f21 #cc6666 bold', Token.Toolbar.Signature.Operator: '#c5c8c6 bold', Token.Docstring: '#b5bd68', Token.Toolbar.Validation: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status: 'bg:#1d1f21 #c5c8c6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.Key: 'bg:#282a2e #c5c8c6', Token.Toolbar.Status.PasteModeOn: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.PythonVersion: 'bg:#1d1f21 #81a2be bold', Token.Aborted: '#cc6666', Token.Sidebar: 'bg:#282a2e #c5c8c6', Token.Sidebar.Title: 'bg:#1d1f21 #de935f bold', Token.Sidebar.Label: 'bg:#282a2e #b5bd68', Token.Sidebar.Status: 'bg:#282a2e #c5c8c6', Token.Sidebar.Selected.Label: 'bg:#1d1f21 #cc6666', Token.Sidebar.Selected.Status: 'bg:#1d1f21 #c5c8c6 bold', Token.Sidebar.Separator: 'bg:#282a2e #1d1f21 underline', Token.Sidebar.Key: 'bg:#282a2e #cc6666 bold', Token.Sidebar.Key.Description: 'bg:#282a2e #c5c8c6', Token.Sidebar.HelpText: 'bg:#282a2e #c5c8c6', Token.History.Line: '', Token.History.Line.Selected: 'bg:#282a2e #c5c8c6', Token.History.Line.Current: 'bg:#1d1f21 #b5bd68', Token.History.Line.Selected.Current: 'bg:#1d1f21 #cc6666', Token.History.ExistingInput: '#81a2be', Token.Window.Border: '#3e4452', Token.Window.Title: 'bg:#282a2e #c5c8c6', Token.Window.TIItleV2: 'bg:#1d1f21 #c5c8c6 bold', Token.AcceptMessage: 'bg:#282a2e #b5bd68', Token.ExitConfirmation: 'bg:#1d1f21 #cc6666', Token.SearchMatch: 'bg:#282a2e #c5c8c6', Token.SearchMatch.Current: 'bg:#1d1f21 #cc6666 underline', Token.SelectedText: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions.Arrow: 'bg:#282a2e #cc6666 bold', Token.Toolbar.Completions.Completion: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions.Completion.Current: 'bg:#1d1f21 #b5bd68 underline', Token.Menu.Completions.Completion: 'bg:#282a2e #c5c8c6', Token.Menu.Completions.Completion.Current: 'bg:#1d1f21 #b5bd68', Token.Menu.Completions.Meta: 'bg:#282a2e #5f819d', Token.Menu.Completions.Meta.Current: 'bg:#282a2e #81a2be', Token.Menu.Completions.ProgressBar: 'bg:#cc6666', Token.Menu.Completions.ProgressButton: 'bg:#282a2e'}

# Tomorrow theme - base light theme
tomorrow_style = {Token: '', Token.Comment: 'italic #8e908c', Token.Comment.Hashbang: '#8e908c', Token.Comment.Multiline: '#8e908c', Token.Comment.Preproc: 'noitalic #8e908c', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#c82829', Token.Escape: '#3e999f', Token.Generic: '', Token.Generic.Deleted: '#c82829', Token.Generic.Emph: 'italic', Token.Generic.Error: '#c82829', Token.Generic.Heading: '#4271ae', Token.Generic.Inserted: '#718c00', Token.Generic.Output: '#4d4d4c', Token.Generic.Prompt: '#8959a8', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#4271ae', Token.Generic.Traceback: '#c82829', Token.Keyword: '#8959a8 bold', Token.Keyword.Constant: '#f5871f italic', Token.Keyword.Declaration: '#8959a8 bold', Token.Keyword.Namespace: '#8959a8', Token.Keyword.Pseudo: '#8959a8', Token.Keyword.Reserved: '#8959a8 bold', Token.Keyword.Type: '#eab700 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#f5871f', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#718c00', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#718c00', Token.Literal.String.Doc: '#718c00 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#3e999f', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#3e999f', Token.Literal.String.Other: '#718c00', Token.Literal.String.Regex: '#3e999f', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#f5871f', Token.Name: '#4d4d4c', Token.Name.Attribute: '#eab700', Token.Name.Builtin: '#4271ae bold', Token.Name.Builtin.Pseudo: '#f5871f italic', Token.Name.Class: '#eab700 bold', Token.Name.Constant: '#eab700 bold', Token.Name.Decorator: '#4271ae', Token.Name.Entity: '#4d4d4c', Token.Name.Exception: '#c82829 bold', Token.Name.Function: '#4271ae', Token.Name.Label: '#4d4d4c', Token.Name.Namespace: '#eab700', Token.Name.Other: '#4d4d4c', Token.Name.Property: '#4d4d4c', Token.Name.Tag: '#c82829', Token.Name.Variable: '#c82829', Token.Name.Variable.Class: '#c82829 italic', Token.Name.Variable.Global: '#c82829 bold', Token.Name.Variable.Instance: '#c82829', Token.Operator: '#c82829', Token.Operator.Word: '#8959a8 bold', Token.Punctuation: '#3e999f', Token.Punctuation.Marker: '#8e908c', Token.Punctuation.Bracket: '#8e908c', Token.Punctuation.Parenthesis: '#8e908c', Token.Text: '#4d4d4c', Token.Text.Whitespace: ''}

tomorrow = {Token.LineNumber: 'bg:#ffffff #8e908c', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #8959a8', Token.In.Number: '', Token.Out: '#4271ae', Token.Out.Number: '#4271ae', Token.Separator: '#c82829', Token.Toolbar.Search: '#c82829 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#c82829 noinherit', Token.Toolbar.Arg: '#c82829 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#efefef #4d4d4c', Token.Toolbar.Signature.CurrentName: 'bg:#ffffff #c82829 bold', Token.Toolbar.Signature.Operator: '#4d4d4c bold', Token.Docstring: '#718c00', Token.Toolbar.Validation: 'bg:#ffffff #c82829', Token.Toolbar.Status: 'bg:#ffffff #4d4d4c', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#ffffff #718c00', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#ffffff #c82829', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#ffffff #718c00', Token.Toolbar.Status.Key: 'bg:#efefef #4d4d4c', Token.Toolbar.Status.PasteModeOn: 'bg:#ffffff #c82829', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#ffffff #718c00', Token.Toolbar.Status.PythonVersion: 'bg:#ffffff #4271ae bold', Token.Aborted: '#c82829', Token.Sidebar: 'bg:#efefef #4d4d4c', Token.Sidebar.Title: 'bg:#ffffff #eab700 bold', Token.Sidebar.Label: 'bg:#efefef #718c00', Token.Sidebar.Status: 'bg:#efefef #4d4d4c', Token.Sidebar.Selected.Label: 'bg:#ffffff #c82829', Token.Sidebar.Selected.Status: 'bg:#ffffff #4d4d4c bold', Token.Sidebar.Separator: 'bg:#efefef #ffffff underline', Token.Sidebar.Key: 'bg:#efefef #c82829 bold', Token.Sidebar.Key.Description: 'bg:#efefef #4d4d4c', Token.Sidebar.HelpText: 'bg:#efefef #4d4d4c', Token.History.Line: '', Token.History.Line.Selected: 'bg:#efefef #4d4d4c', Token.History.Line.Current: 'bg:#ffffff #718c00', Token.History.Line.Selected.Current: 'bg:#ffffff #c82829', Token.History.ExistingInput: '#4271ae', Token.Window.Border: '#8e908c', Token.Window.Title: 'bg:#efefef #4d4d4c', Token.Window.TIItleV2: 'bg:#ffffff #4d4d4c bold', Token.AcceptMessage: 'bg:#efefef #718c00', Token.ExitConfirmation: 'bg:#ffffff #c82829', Token.SearchMatch: 'bg:#efefef #4d4d4c', Token.SearchMatch.Current: 'bg:#ffffff #c82829 underline', Token.SelectedText: 'bg:#efefef #4d4d4c', Token.Toolbar.Completions: 'bg:#efefef #4d4d4c', Token.Toolbar.Completions.Arrow: 'bg:#efefef #c82829 bold', Token.Toolbar.Completions.Completion: 'bg:#efefef #4d4d4c', Token.Toolbar.Completions.Completion.Current: 'bg:#ffffff #718c00 underline', Token.Menu.Completions.Completion: 'bg:#efefef #4d4d4c', Token.Menu.Completions.Completion.Current: 'bg:#ffffff #718c00', Token.Menu.Completions.Meta: 'bg:#efefef #8e908c', Token.Menu.Completions.Meta.Current: 'bg:#efefef #4271ae', Token.Menu.Completions.ProgressBar: 'bg:#c82829', Token.Menu.Completions.ProgressButton: 'bg:#efefef'}

# Tomorrow Night theme - dark base theme
tomorrow_night_style = {Token: '', Token.Comment: 'italic #969896', Token.Comment.Hashbang: '#969896', Token.Comment.Multiline: '#969896', Token.Comment.Preproc: 'noitalic #969896', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#cc6666', Token.Escape: '#66cccc', Token.Generic: '', Token.Generic.Deleted: '#cc6666', Token.Generic.Emph: 'italic', Token.Generic.Error: '#cc6666', Token.Generic.Heading: '#81a2be', Token.Generic.Inserted: '#b5bd68', Token.Generic.Output: '#c5c8c6', Token.Generic.Prompt: '#b294bb', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#81a2be', Token.Generic.Traceback: '#cc6666', Token.Keyword: '#b294bb bold', Token.Keyword.Constant: '#de935f italic', Token.Keyword.Declaration: '#b294bb bold', Token.Keyword.Namespace: '#b294bb', Token.Keyword.Pseudo: '#b294bb', Token.Keyword.Reserved: '#b294bb bold', Token.Keyword.Type: '#f0c674 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#de935f', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#b5bd68', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#b5bd68', Token.Literal.String.Doc: '#b5bd68 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#66cccc', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#66cccc', Token.Literal.String.Other: '#b5bd68', Token.Literal.String.Regex: '#66cccc', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#de935f', Token.Name: '#c5c8c6', Token.Name.Attribute: '#f0c674', Token.Name.Builtin: '#81a2be bold', Token.Name.Builtin.Pseudo: '#de935f italic', Token.Name.Class: '#f0c674 bold', Token.Name.Constant: '#f0c674 bold', Token.Name.Decorator: '#81a2be', Token.Name.Entity: '#c5c8c6', Token.Name.Exception: '#cc6666 bold', Token.Name.Function: '#81a2be', Token.Name.Label: '#c5c8c6', Token.Name.Namespace: '#f0c674', Token.Name.Other: '#c5c8c6', Token.Name.Property: '#c5c8c6', Token.Name.Tag: '#cc6666', Token.Name.Variable: '#cc6666', Token.Name.Variable.Class: '#cc6666 italic', Token.Name.Variable.Global: '#cc6666 bold', Token.Name.Variable.Instance: '#cc6666', Token.Operator: '#cc6666', Token.Operator.Word: '#b294bb bold', Token.Punctuation: '#66cccc', Token.Punctuation.Marker: '#969896', Token.Punctuation.Bracket: '#969896', Token.Punctuation.Parenthesis: '#969896', Token.Text: '#c5c8c6', Token.Text.Whitespace: ''}

tomorrow_night = {Token.LineNumber: 'bg:#1d1f21 #969896', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #b294bb', Token.In.Number: '', Token.Out: '#81a2be', Token.Out.Number: '#81a2be', Token.Separator: '#cc6666', Token.Toolbar.Search: '#cc6666 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#cc6666 noinherit', Token.Toolbar.Arg: '#cc6666 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#282a2e #c5c8c6', Token.Toolbar.Signature.CurrentName: 'bg:#1d1f21 #cc6666 bold', Token.Toolbar.Signature.Operator: '#c5c8c6 bold', Token.Docstring: '#b5bd68', Token.Toolbar.Validation: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status: 'bg:#1d1f21 #c5c8c6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.Key: 'bg:#282a2e #c5c8c6', Token.Toolbar.Status.PasteModeOn: 'bg:#1d1f21 #cc6666', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#1d1f21 #b5bd68', Token.Toolbar.Status.PythonVersion: 'bg:#1d1f21 #81a2be bold', Token.Aborted: '#cc6666', Token.Sidebar: 'bg:#282a2e #c5c8c6', Token.Sidebar.Title: 'bg:#1d1f21 #f0c674 bold', Token.Sidebar.Label: 'bg:#282a2e #b5bd68', Token.Sidebar.Status: 'bg:#282a2e #c5c8c6', Token.Sidebar.Selected.Label: 'bg:#1d1f21 #cc6666', Token.Sidebar.Selected.Status: 'bg:#1d1f21 #c5c8c6 bold', Token.Sidebar.Separator: 'bg:#282a2e #1d1f21 underline', Token.Sidebar.Key: 'bg:#282a2e #cc6666 bold', Token.Sidebar.Key.Description: 'bg:#282a2e #c5c8c6', Token.Sidebar.HelpText: 'bg:#282a2e #c5c8c6', Token.History.Line: '', Token.History.Line.Selected: 'bg:#282a2e #c5c8c6', Token.History.Line.Current: 'bg:#1d1f21 #b5bd68', Token.History.Line.Selected.Current: 'bg:#1d1f21 #cc6666', Token.History.ExistingInput: '#81a2be', Token.Window.Border: '#969896', Token.Window.Title: 'bg:#282a2e #c5c8c6', Token.Window.TIItleV2: 'bg:#1d1f21 #c5c8c6 bold', Token.AcceptMessage: 'bg:#282a2e #b5bd68', Token.ExitConfirmation: 'bg:#1d1f21 #cc6666', Token.SearchMatch: 'bg:#282a2e #c5c8c6', Token.SearchMatch.Current: 'bg:#1d1f21 #cc6666 underline', Token.SelectedText: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions.Arrow: 'bg:#282a2e #cc6666 bold', Token.Toolbar.Completions.Completion: 'bg:#282a2e #c5c8c6', Token.Toolbar.Completions.Completion.Current: 'bg:#1d1f21 #b5bd68 underline', Token.Menu.Completions.Completion: 'bg:#282a2e #c5c8c6', Token.Menu.Completions.Completion.Current: 'bg:#1d1f21 #b5bd68', Token.Menu.Completions.Meta: 'bg:#282a2e #969896', Token.Menu.Completions.Meta.Current: 'bg:#282a2e #81a2be', Token.Menu.Completions.ProgressBar: 'bg:#cc6666', Token.Menu.Completions.ProgressButton: 'bg:#282a2e'}

# Tomorrow Night Blue theme
tomorrow_night_blue_style = {Token: '', Token.Comment: 'italic #7285b7', Token.Comment.Hashbang: '#7285b7', Token.Comment.Multiline: '#7285b7', Token.Comment.Preproc: 'noitalic #7285b7', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#ff9da4', Token.Escape: '#bbdaff', Token.Generic: '', Token.Generic.Deleted: '#ff9da4', Token.Generic.Emph: 'italic', Token.Generic.Error: '#ff9da4', Token.Generic.Heading: '#bbdaff', Token.Generic.Inserted: '#d1f1a9', Token.Generic.Output: '#ffffff', Token.Generic.Prompt: '#ebbbff', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#bbdaff', Token.Generic.Traceback: '#ff9da4', Token.Keyword: '#ebbbff bold', Token.Keyword.Constant: '#ffeead italic', Token.Keyword.Declaration: '#ebbbff bold', Token.Keyword.Namespace: '#ebbbff', Token.Keyword.Pseudo: '#ebbbff', Token.Keyword.Reserved: '#ebbbff bold', Token.Keyword.Type: '#ffd280 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#ffeead', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#d1f1a9', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#d1f1a9', Token.Literal.String.Doc: '#d1f1a9 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#99ffff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#99ffff', Token.Literal.String.Other: '#d1f1a9', Token.Literal.String.Regex: '#99ffff', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#ffeead', Token.Name: '#ffffff', Token.Name.Attribute: '#ffd280', Token.Name.Builtin: '#bbdaff bold', Token.Name.Builtin.Pseudo: '#ffeead italic', Token.Name.Class: '#ffd280 bold', Token.Name.Constant: '#ffd280 bold', Token.Name.Decorator: '#bbdaff', Token.Name.Entity: '#ffffff', Token.Name.Exception: '#ff9da4 bold', Token.Name.Function: '#bbdaff', Token.Name.Label: '#ffffff', Token.Name.Namespace: '#ffd280', Token.Name.Other: '#ffffff', Token.Name.Property: '#ffffff', Token.Name.Tag: '#ff9da4', Token.Name.Variable: '#ff9da4', Token.Name.Variable.Class: '#ff9da4 italic', Token.Name.Variable.Global: '#ff9da4 bold', Token.Name.Variable.Instance: '#ff9da4', Token.Operator: '#ff9da4', Token.Operator.Word: '#ebbbff bold', Token.Punctuation: '#99ffff', Token.Punctuation.Marker: '#7285b7', Token.Punctuation.Bracket: '#7285b7', Token.Punctuation.Parenthesis: '#7285b7', Token.Text: '#ffffff', Token.Text.Whitespace: ''}

tomorrow_night_blue = {Token.LineNumber: 'bg:#002451 #7285b7', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ebbbff', Token.In.Number: '', Token.Out: '#bbdaff', Token.Out.Number: '#bbdaff', Token.Separator: '#ff9da4', Token.Toolbar.Search: '#ff9da4 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff9da4 noinherit', Token.Toolbar.Arg: '#ff9da4 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#00346e #ffffff', Token.Toolbar.Signature.CurrentName: 'bg:#002451 #ff9da4 bold', Token.Toolbar.Signature.Operator: '#ffffff bold', Token.Docstring: '#d1f1a9', Token.Toolbar.Validation: 'bg:#002451 #ff9da4', Token.Toolbar.Status: 'bg:#002451 #ffffff', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#002451 #d1f1a9', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#002451 #ff9da4', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#002451 #d1f1a9', Token.Toolbar.Status.Key: 'bg:#00346e #ffffff', Token.Toolbar.Status.PasteModeOn: 'bg:#002451 #ff9da4', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#002451 #d1f1a9', Token.Toolbar.Status.PythonVersion: 'bg:#002451 #bbdaff bold', Token.Aborted: '#ff9da4', Token.Sidebar: 'bg:#00346e #ffffff', Token.Sidebar.Title: 'bg:#002451 #ffd280 bold', Token.Sidebar.Label: 'bg:#00346e #d1f1a9', Token.Sidebar.Status: 'bg:#00346e #ffffff', Token.Sidebar.Selected.Label: 'bg:#002451 #ff9da4', Token.Sidebar.Selected.Status: 'bg:#002451 #ffffff bold', Token.Sidebar.Separator: 'bg:#00346e #002451 underline', Token.Sidebar.Key: 'bg:#00346e #ff9da4 bold', Token.Sidebar.Key.Description: 'bg:#00346e #ffffff', Token.Sidebar.HelpText: 'bg:#00346e #ffffff', Token.History.Line: '', Token.History.Line.Selected: 'bg:#00346e #ffffff', Token.History.Line.Current: 'bg:#002451 #d1f1a9', Token.History.Line.Selected.Current: 'bg:#002451 #ff9da4', Token.History.ExistingInput: '#bbdaff', Token.Window.Border: '#7285b7', Token.Window.Title: 'bg:#00346e #ffffff', Token.Window.TIItleV2: 'bg:#002451 #ffffff bold', Token.AcceptMessage: 'bg:#00346e #d1f1a9', Token.ExitConfirmation: 'bg:#002451 #ff9da4', Token.SearchMatch: 'bg:#00346e #ffffff', Token.SearchMatch.Current: 'bg:#002451 #ff9da4 underline', Token.SelectedText: 'bg:#00346e #ffffff', Token.Toolbar.Completions: 'bg:#00346e #ffffff', Token.Toolbar.Completions.Arrow: 'bg:#00346e #ff9da4 bold', Token.Toolbar.Completions.Completion: 'bg:#00346e #ffffff', Token.Toolbar.Completions.Completion.Current: 'bg:#002451 #d1f1a9 underline', Token.Menu.Completions.Completion: 'bg:#00346e #ffffff', Token.Menu.Completions.Completion.Current: 'bg:#002451 #d1f1a9', Token.Menu.Completions.Meta: 'bg:#00346e #7285b7', Token.Menu.Completions.Meta.Current: 'bg:#00346e #bbdaff', Token.Menu.Completions.ProgressBar: 'bg:#ff9da4', Token.Menu.Completions.ProgressButton: 'bg:#00346e'}

# Tomorrow Night Bright theme
tomorrow_night_bright_style = {Token: '', Token.Comment: 'italic #969896', Token.Comment.Hashbang: '#969896', Token.Comment.Multiline: '#969896', Token.Comment.Preproc: 'noitalic #969896', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#d54e53', Token.Escape: '#70c0b1', Token.Generic: '', Token.Generic.Deleted: '#d54e53', Token.Generic.Emph: 'italic', Token.Generic.Error: '#d54e53', Token.Generic.Heading: '#7aa6da', Token.Generic.Inserted: '#b9ca4a', Token.Generic.Output: '#eaeaea', Token.Generic.Prompt: '#c397d8', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#7aa6da', Token.Generic.Traceback: '#d54e53', Token.Keyword: '#c397d8 bold', Token.Keyword.Constant: '#e7c547 italic', Token.Keyword.Declaration: '#c397d8 bold', Token.Keyword.Namespace: '#c397d8', Token.Keyword.Pseudo: '#c397d8', Token.Keyword.Reserved: '#c397d8 bold', Token.Keyword.Type: '#e7c547 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#e78c45', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#b9ca4a', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#b9ca4a', Token.Literal.String.Doc: '#b9ca4a italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#70c0b1', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#70c0b1', Token.Literal.String.Other: '#b9ca4a', Token.Literal.String.Regex: '#70c0b1', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#e78c45', Token.Name: '#eaeaea', Token.Name.Attribute: '#e7c547', Token.Name.Builtin: '#7aa6da bold', Token.Name.Builtin.Pseudo: '#e78c45 italic', Token.Name.Class: '#e7c547 bold', Token.Name.Constant: '#e7c547 bold', Token.Name.Decorator: '#7aa6da', Token.Name.Entity: '#eaeaea', Token.Name.Exception: '#d54e53 bold', Token.Name.Function: '#7aa6da', Token.Name.Label: '#eaeaea', Token.Name.Namespace: '#e7c547', Token.Name.Other: '#eaeaea', Token.Name.Property: '#eaeaea', Token.Name.Tag: '#d54e53', Token.Name.Variable: '#d54e53', Token.Name.Variable.Class: '#d54e53 italic', Token.Name.Variable.Global: '#d54e53 bold', Token.Name.Variable.Instance: '#d54e53', Token.Operator: '#d54e53', Token.Operator.Word: '#c397d8 bold', Token.Punctuation: '#70c0b1', Token.Punctuation.Marker: '#969896', Token.Punctuation.Bracket: '#969896', Token.Punctuation.Parenthesis: '#969896', Token.Text: '#eaeaea', Token.Text.Whitespace: ''}

tomorrow_night_bright = {Token.LineNumber: 'bg:#000000 #969896', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #c397d8', Token.In.Number: '', Token.Out: '#7aa6da', Token.Out.Number: '#7aa6da', Token.Separator: '#d54e53', Token.Toolbar.Search: '#d54e53 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#d54e53 noinherit', Token.Toolbar.Arg: '#d54e53 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#2a2a2a #eaeaea', Token.Toolbar.Signature.CurrentName: 'bg:#000000 #d54e53 bold', Token.Toolbar.Signature.Operator: '#eaeaea bold', Token.Docstring: '#b9ca4a', Token.Toolbar.Validation: 'bg:#000000 #d54e53', Token.Toolbar.Status: 'bg:#000000 #eaeaea', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#000000 #b9ca4a', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#000000 #d54e53', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#000000 #b9ca4a', Token.Toolbar.Status.Key: 'bg:#2a2a2a #eaeaea', Token.Toolbar.Status.PasteModeOn: 'bg:#000000 #d54e53', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#000000 #b9ca4a', Token.Toolbar.Status.PythonVersion: 'bg:#000000 #7aa6da bold', Token.Aborted: '#d54e53', Token.Sidebar: 'bg:#2a2a2a #eaeaea', Token.Sidebar.Title: 'bg:#000000 #e7c547 bold', Token.Sidebar.Label: 'bg:#2a2a2a #b9ca4a', Token.Sidebar.Status: 'bg:#2a2a2a #eaeaea', Token.Sidebar.Selected.Label: 'bg:#000000 #d54e53', Token.Sidebar.Selected.Status: 'bg:#000000 #eaeaea bold', Token.Sidebar.Separator: 'bg:#2a2a2a #000000 underline', Token.Sidebar.Key: 'bg:#2a2a2a #d54e53 bold', Token.Sidebar.Key.Description: 'bg:#2a2a2a #eaeaea', Token.Sidebar.HelpText: 'bg:#2a2a2a #eaeaea', Token.History.Line: '', Token.History.Line.Selected: 'bg:#2a2a2a #eaeaea', Token.History.Line.Current: 'bg:#000000 #b9ca4a', Token.History.Line.Selected.Current: 'bg:#000000 #d54e53', Token.History.ExistingInput: '#7aa6da', Token.Window.Border: '#969896', Token.Window.Title: 'bg:#2a2a2a #eaeaea', Token.Window.TIItleV2: 'bg:#000000 #eaeaea bold', Token.AcceptMessage: 'bg:#2a2a2a #b9ca4a', Token.ExitConfirmation: 'bg:#000000 #d54e53', Token.SearchMatch: 'bg:#2a2a2a #eaeaea', Token.SearchMatch.Current: 'bg:#000000 #d54e53 underline', Token.SelectedText: 'bg:#2a2a2a #eaeaea', Token.Toolbar.Completions: 'bg:#2a2a2a #eaeaea', Token.Toolbar.Completions.Arrow: 'bg:#2a2a2a #d54e53 bold', Token.Toolbar.Completions.Completion: 'bg:#2a2a2a #eaeaea', Token.Toolbar.Completions.Completion.Current: 'bg:#000000 #b9ca4a underline', Token.Menu.Completions.Completion: 'bg:#2a2a2a #eaeaea', Token.Menu.Completions.Completion.Current: 'bg:#000000 #b9ca4a', Token.Menu.Completions.Meta: 'bg:#2a2a2a #969896', Token.Menu.Completions.Meta.Current: 'bg:#2a2a2a #7aa6da', Token.Menu.Completions.ProgressBar: 'bg:#d54e53', Token.Menu.Completions.ProgressButton: 'bg:#2a2a2a'}

# Tomorrow Night Eighties theme
tomorrow_night_eighties_style = {Token: '', Token.Comment: 'italic #999999', Token.Comment.Hashbang: '#999999', Token.Comment.Multiline: '#999999', Token.Comment.Preproc: 'noitalic #999999', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#f2777a', Token.Escape: '#66cccc', Token.Generic: '', Token.Generic.Deleted: '#f2777a', Token.Generic.Emph: 'italic', Token.Generic.Error: '#f2777a', Token.Generic.Heading: '#6699cc', Token.Generic.Inserted: '#99cc99', Token.Generic.Output: '#cccccc', Token.Generic.Prompt: '#cc99cc', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#6699cc', Token.Generic.Traceback: '#f2777a', Token.Keyword: '#cc99cc bold', Token.Keyword.Constant: '#f99157 italic', Token.Keyword.Declaration: '#cc99cc bold', Token.Keyword.Namespace: '#cc99cc', Token.Keyword.Pseudo: '#cc99cc', Token.Keyword.Reserved: '#cc99cc bold', Token.Keyword.Type: '#ffcc66 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#f99157', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#99cc99', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#99cc99', Token.Literal.String.Doc: '#99cc99 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#66cccc', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#66cccc', Token.Literal.String.Other: '#99cc99', Token.Literal.String.Regex: '#66cccc', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#f99157', Token.Name: '#cccccc', Token.Name.Attribute: '#ffcc66', Token.Name.Builtin: '#6699cc bold', Token.Name.Builtin.Pseudo: '#f99157 italic', Token.Name.Class: '#ffcc66 bold', Token.Name.Constant: '#ffcc66 bold', Token.Name.Decorator: '#6699cc', Token.Name.Entity: '#cccccc', Token.Name.Exception: '#f2777a bold', Token.Name.Function: '#6699cc', Token.Name.Label: '#cccccc', Token.Name.Namespace: '#ffcc66', Token.Name.Other: '#cccccc', Token.Name.Property: '#cccccc', Token.Name.Tag: '#f2777a', Token.Name.Variable: '#f2777a', Token.Name.Variable.Class: '#f2777a italic', Token.Name.Variable.Global: '#f2777a bold', Token.Name.Variable.Instance: '#f2777a', Token.Operator: '#f2777a', Token.Operator.Word: '#cc99cc bold', Token.Punctuation: '#66cccc', Token.Punctuation.Marker: '#999999', Token.Punctuation.Bracket: '#999999', Token.Punctuation.Parenthesis: '#999999', Token.Text: '#cccccc', Token.Text.Whitespace: ''}

# Dejavu style - based on Tomorrow Night with some adjustments
dejavu_style = {Token: '', Token.Comment: 'italic #5f819d', Token.Comment.Hashbang: '#5f819d', Token.Comment.Multiline: '#5f819d', Token.Comment.Preproc: 'noitalic #5f819d', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#cc6666', Token.Escape: '#b5bd68', Token.Generic: '', Token.Generic.Deleted: '#cc6666', Token.Generic.Emph: 'italic', Token.Generic.Error: '#cc6666', Token.Generic.Heading: '#81a2be', Token.Generic.Inserted: '#b5bd68', Token.Generic.Output: '#c5c8c6', Token.Generic.Prompt: '#b294bb', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#81a2be', Token.Generic.Traceback: '#cc6666', Token.Keyword: '#b294bb bold', Token.Keyword.Constant: '#de935f italic', Token.Keyword.Declaration: '#b294bb bold', Token.Keyword.Namespace: '#b294bb', Token.Keyword.Pseudo: '#b294bb', Token.Keyword.Reserved: '#b294bb bold', Token.Keyword.Type: '#f0c674 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#de935f', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#b5bd68', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#b5bd68', Token.Literal.String.Doc: '#b5bd68 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#8abeb7', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#8abeb7', Token.Literal.String.Other: '#b5bd68', Token.Literal.String.Regex: '#8abeb7', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#de935f', Token.Name: '#c5c8c6', Token.Name.Attribute: '#f0c674', Token.Name.Builtin: '#81a2be bold', Token.Name.Builtin.Pseudo: '#de935f italic', Token.Name.Class: '#f0c674 bold', Token.Name.Constant: '#f0c674 bold', Token.Name.Decorator: '#81a2be', Token.Name.Entity: '#c5c8c6', Token.Name.Exception: '#cc6666 bold', Token.Name.Function: '#81a2be', Token.Name.Label: '#c5c8c6', Token.Name.Namespace: '#f0c674', Token.Name.Other: '#c5c8c6', Token.Name.Property: '#c5c8c6', Token.Name.Tag: '#cc6666', Token.Name.Variable: '#cc6666', Token.Name.Variable.Class: '#cc6666 italic', Token.Name.Variable.Global: '#cc6666 bold', Token.Name.Variable.Instance: '#cc6666', Token.Operator: '#cc6666', Token.Operator.Word: '#b294bb bold', Token.Punctuation: '#8abeb7', Token.Punctuation.Marker: '#5f819d', Token.Punctuation.Bracket: '#5f819d', Token.Punctuation.Parenthesis: '#5f819d', Token.Text: '#c5c8c6', Token.Text.Whitespace: ''}

# Sunset Warm - warm variant of sunset theme
sunset_warm_style = {Token: '', Token.Comment: 'italic #bb8a7a', Token.Comment.Hashbang: '#bb8a7a', Token.Comment.Multiline: '#bb8a7a', Token.Comment.Preproc: 'noitalic #bb8a7a', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#ff627e', Token.Escape: '#ffb68c', Token.Generic: '', Token.Generic.Deleted: '#ff627e', Token.Generic.Emph: 'italic', Token.Generic.Error: '#ff627e', Token.Generic.Heading: '#ff9e64', Token.Generic.Inserted: '#ffa273', Token.Generic.Output: '#ffcec6', Token.Generic.Prompt: '#ff8c75', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#ff9e64', Token.Generic.Traceback: '#ff627e', Token.Keyword: '#ff8c75 bold', Token.Keyword.Constant: '#ffd76b italic', Token.Keyword.Declaration: '#ff8c75 bold', Token.Keyword.Namespace: '#ff8c75', Token.Keyword.Pseudo: '#ff8c75', Token.Keyword.Reserved: '#ff8c75 bold', Token.Keyword.Type: '#ffa273 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#ffd76b', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#ffa273', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#ffa273', Token.Literal.String.Doc: '#ffa273 italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#ffb68c', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#ffb68c', Token.Literal.String.Other: '#ffa273', Token.Literal.String.Regex: '#ffb68c', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#ffd76b', Token.Name: '#ffcec6', Token.Name.Attribute: '#ffa273', Token.Name.Builtin: '#ff9e64 bold', Token.Name.Builtin.Pseudo: '#ffd76b italic', Token.Name.Class: '#ffa273 bold', Token.Name.Constant: '#ffa273 bold', Token.Name.Decorator: '#ff9e64', Token.Name.Entity: '#ffcec6', Token.Name.Exception: '#ff627e bold', Token.Name.Function: '#ff9e64', Token.Name.Label: '#ffcec6', Token.Name.Namespace: '#ffa273', Token.Name.Other: '#ffcec6', Token.Name.Property: '#ffcec6', Token.Name.Tag: '#ff627e', Token.Name.Variable: '#ff627e', Token.Name.Variable.Class: '#ff627e italic', Token.Name.Variable.Global: '#ff627e bold', Token.Name.Variable.Instance: '#ff627e', Token.Operator: '#ff627e', Token.Operator.Word: '#ff8c75 bold', Token.Punctuation: '#ffb68c', Token.Punctuation.Marker: '#bb8a7a', Token.Punctuation.Bracket: '#bb8a7a', Token.Punctuation.Parenthesis: '#bb8a7a', Token.Text: '#ffcec6', Token.Text.Whitespace: ''}

# Sunset Cool - cool variant of sunset theme
sunset_cool_style = {Token: '', Token.Comment: 'italic #7a8abb', Token.Comment.Hashbang: '#7a8abb', Token.Comment.Multiline: '#7a8abb', Token.Comment.Preproc: 'noitalic #7a8abb', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: '#627eff', Token.Escape: '#8cb6ff', Token.Generic: '', Token.Generic.Deleted: '#627eff', Token.Generic.Emph: 'italic', Token.Generic.Error: '#627eff', Token.Generic.Heading: '#9e64ff', Token.Generic.Inserted: '#73a2ff', Token.Generic.Output: '#cec6ff', Token.Generic.Prompt: '#8c75ff', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#9e64ff', Token.Generic.Traceback: '#627eff', Token.Keyword: '#8c75ff bold', Token.Keyword.Constant: '#7373ff italic', Token.Keyword.Declaration: '#8c75ff bold', Token.Keyword.Namespace: '#8c75ff', Token.Keyword.Pseudo: '#8c75ff', Token.Keyword.Reserved: '#8c75ff bold', Token.Keyword.Type: '#73a2ff italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#7373ff', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#73a2ff', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#73a2ff', Token.Literal.String.Doc: '#73a2ff italic', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#8cb6ff', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: '#8cb6ff', Token.Literal.String.Other: '#73a2ff', Token.Literal.String.Regex: '#8cb6ff', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#7373ff', Token.Name: '#cec6ff', Token.Name.Attribute: '#73a2ff', Token.Name.Builtin: '#9e64ff bold', Token.Name.Builtin.Pseudo: '#7373ff italic', Token.Name.Class: '#73a2ff bold', Token.Name.Constant: '#73a2ff bold', Token.Name.Decorator: '#9e64ff', Token.Name.Entity: '#cec6ff', Token.Name.Exception: '#627eff bold', Token.Name.Function: '#9e64ff', Token.Name.Label: '#cec6ff', Token.Name.Namespace: '#73a2ff', Token.Name.Other: '#cec6ff', Token.Name.Property: '#cec6ff', Token.Name.Tag: '#627eff', Token.Name.Variable: '#627eff', Token.Name.Variable.Class: '#627eff italic', Token.Name.Variable.Global: '#627eff bold', Token.Name.Variable.Instance: '#627eff', Token.Operator: '#627eff', Token.Operator.Word: '#8c75ff bold', Token.Punctuation: '#8cb6ff', Token.Punctuation.Marker: '#7a8abb', Token.Punctuation.Bracket: '#7a8abb', Token.Punctuation.Parenthesis: '#7a8abb', Token.Text: '#cec6ff', Token.Text.Whitespace: ''}

# Sunset Monokai - a monokai variant with sunset colors
sunset_monokai_style = {Token: '', Token.Comment: 'italic #bb8a7a', Token.Comment.Hashbang: '#bb8a7a', Token.Comment.Multiline: '#bb8a7a', Token.Comment.Preproc: 'noitalic #bb8a7a', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#ff627e', Token.Escape: '#ffd76b', Token.Generic: '', Token.Generic.Deleted: '#ff627e', Token.Generic.Emph: 'italic', Token.Generic.Error: '#ff627e', Token.Generic.Heading: '#ffa273', Token.Generic.Inserted: '#ffa273', Token.Generic.Output: '#ff9e64', Token.Generic.Prompt: '#ffcec6', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#ffa273', Token.Generic.Traceback: '#ff627e', Token.Keyword: '#ff627e bold', Token.Keyword.Constant: '#ff9e64 italic', Token.Keyword.Declaration: '#ff627e bold', Token.Keyword.Namespace: '#ff627e', Token.Keyword.Pseudo: '#ff627e', Token.Keyword.Reserved: '#ff627e bold', Token.Keyword.Type: '#ff9e64 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#ffd76b', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#ffa273', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#ffa273', Token.Literal.String.Doc: '#ffa273', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#ffd76b', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: 'underline', Token.Literal.String.Other: '#ffa273', Token.Literal.String.Regex: '#ffa273', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#ffa273', Token.Name: '#ffcec6', Token.Name.Attribute: '#ffa273', Token.Name.Builtin: '#ff9e64 bold', Token.Name.Builtin.Pseudo: '#ff9e64 italic', Token.Name.Class: '#ffa273 bold', Token.Name.Constant: '#ff9e64', Token.Name.Decorator: '#ffa273', Token.Name.Entity: '#ffa273', Token.Name.Exception: '#ffa273 bold', Token.Name.Function: '#ffa273', Token.Name.Label: '#ffcec6', Token.Name.Namespace: '#ffcec6', Token.Name.Other: '#ffcec6', Token.Name.Property: '#ffcec6', Token.Name.Tag: '#ff627e', Token.Name.Variable: '#ffb68c', Token.Name.Variable.Class: '#ffb68c italic', Token.Name.Variable.Global: '#ffb68c bold', Token.Name.Variable.Instance: '#ffb68c', Token.Operator: '#ff627e', Token.Operator.Word: '#ff627e bold', Token.Punctuation: '#ffcec6', Token.Punctuation.Marker: '#bb8a7a', Token.Punctuation.Bracket: '#e6e6fa', Token.Punctuation.Parenthesis: '#e6e6fa', Token.Text: '#ffcec6', Token.Text.Whitespace: ''}

# Clara Monokai - a monokai variant with clara-inspired colors
clara_monokai_style = {Token: '', Token.Comment: 'italic #8BADD9', Token.Comment.Hashbang: '#8BADD9', Token.Comment.Multiline: '#8BADD9', Token.Comment.Preproc: 'noitalic #8BADD9', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#D026B0', Token.Escape: '#55CDFC', Token.Generic: '', Token.Generic.Deleted: '#D026B0', Token.Generic.Emph: 'italic', Token.Generic.Error: '#D026B0', Token.Generic.Heading: '#21d988', Token.Generic.Inserted: '#21d988', Token.Generic.Output: '#008cf0', Token.Generic.Prompt: '#F5F5F5', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#21d988', Token.Generic.Traceback: '#D026B0', Token.Keyword: '#D026B0 bold', Token.Keyword.Constant: '#008cD0 italic', Token.Keyword.Declaration: '#D026B0 bold italic', Token.Keyword.Namespace: '#D026B0', Token.Keyword.Pseudo: '#D026B0', Token.Keyword.Reserved: '#D026B0 bold', Token.Keyword.Type: '#008cf0 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#55CDFC', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#FFFF64', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#FFFF64', Token.Literal.String.Doc: '#FFFF64', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#55CDFC', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: 'underline', Token.Literal.String.Other: '#21d988', Token.Literal.String.Regex: '#21d988', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#21d988', Token.Name: '#F5F5F5', Token.Name.Attribute: '#21d988', Token.Name.Builtin: '#008cf0 bold', Token.Name.Builtin.Pseudo: '#008cf0 italic', Token.Name.Class: '#17ff9a bold', Token.Name.Constant: '#008cf0', Token.Name.Decorator: '#8730ff', Token.Name.Entity: '#21d988', Token.Name.Exception: '#D026B0 bold', Token.Name.Function: '#21d988', Token.Name.Label: '#F5F5F5', Token.Name.Namespace: '#F5F5F5', Token.Name.Other: '#F5F5F5', Token.Name.Property: '#F5F5F5', Token.Name.Tag: '#D026B0', Token.Name.Variable: '#F5A9B8', Token.Name.Variable.Class: '#F5A9B8 italic', Token.Name.Variable.Global: '#F5A9B8 bold', Token.Name.Variable.Instance: '#F5A9B8', Token.Operator: '#D026B0', Token.Operator.Word: '#D026B0 bold', Token.Punctuation: '#F5F5F5', Token.Punctuation.Marker: '#8BADD9', Token.Punctuation.Bracket: '#e6e6fa', Token.Punctuation.Parenthesis: '#e6e6fa', Token.Text: '#F5F5F5', Token.Text.Whitespace: ''}

# Synthwave Monokai - a monokai variant with synthwave-inspired colors
synthwave_monokai_style = {Token: '', Token.Comment: 'italic #6B7A99', Token.Comment.Hashbang: '#6B7A99', Token.Comment.Multiline: '#6B7A99', Token.Comment.Preproc: 'noitalic #6B7A99', Token.Comment.PreprocFile: '', Token.Comment.Single: '', Token.Comment.Special: '', Token.Error: 'bg:#FF1654', Token.Escape: '#EA00D9', Token.Generic: '', Token.Generic.Deleted: '#FF1654', Token.Generic.Emph: 'italic', Token.Generic.Error: '#FF1654', Token.Generic.Heading: '#0ABDC6', Token.Generic.Inserted: '#0ABDC6', Token.Generic.Output: '#00B0F0', Token.Generic.Prompt: '#F8F8F2', Token.Generic.Strong: 'bold', Token.Generic.Subheading: '#0ABDC6', Token.Generic.Traceback: '#FF1654', Token.Keyword: '#FF1654 bold', Token.Keyword.Constant: '#711C91 italic', Token.Keyword.Declaration: '#FF1654 bold', Token.Keyword.Namespace: '#FF1654', Token.Keyword.Pseudo: '#FF1654', Token.Keyword.Reserved: '#FF1654 bold', Token.Keyword.Type: '#711C91 italic', Token.Literal: '', Token.Literal.Date: '', Token.Literal.Number: '#EA00D9', Token.Literal.Number.Bin: '', Token.Literal.Number.Float: '', Token.Literal.Number.Hex: '', Token.Literal.Number.Integer: '', Token.Literal.Number.Integer.Long: '', Token.Literal.Number.Oct: '', Token.Literal.String: '#FFDD57', Token.Literal.String.Backtick: '', Token.Literal.String.Char: '#FFDD57', Token.Literal.String.Doc: '#FFDD57', Token.Literal.String.Double: '', Token.Literal.String.Escape: '#EA00D9', Token.Literal.String.Heredoc: '', Token.Literal.String.Interpol: 'underline', Token.Literal.String.Other: '#0ABDC6', Token.Literal.String.Regex: '#0ABDC6', Token.Literal.String.Single: '', Token.Literal.String.Symbol: '#0ABDC6', Token.Name: '#F8F8F2', Token.Name.Attribute: '#0ABDC6', Token.Name.Builtin: '#711C91 bold', Token.Name.Builtin.Pseudo: '#711C91 italic', Token.Name.Class: '#0ABDC6 bold', Token.Name.Constant: '#711C91', Token.Name.Decorator: '#0ABDC6', Token.Name.Entity: '#0ABDC6', Token.Name.Exception: '#0ABDC6 bold', Token.Name.Function: '#0ABDC6', Token.Name.Label: '#F8F8F2', Token.Name.Namespace: '#F8F8F2', Token.Name.Other: '#F8F8F2', Token.Name.Property: '#F8F8F2', Token.Name.Tag: '#FF1654', Token.Name.Variable: '#FCEE0C', Token.Name.Variable.Class: '#FCEE0C italic', Token.Name.Variable.Global: '#FCEE0C bold', Token.Name.Variable.Instance: '#FCEE0C', Token.Operator: '#FF1654', Token.Operator.Word: '#FF1654 bold', Token.Punctuation: '#F8F8F2', Token.Punctuation.Marker: '#6B7A99', Token.Punctuation.Bracket: '#e6e6fa', Token.Punctuation.Parenthesis: '#e6e6fa', Token.Text: '#F8F8F2', Token.Text.Whitespace: ''}

# UI styles for the monokai variants
sunset_monokai = {Token.LineNumber: '#ffd76b bg:#4a2d3d', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #ff627e', Token.In.Number: '', Token.Out: '#ffa273', Token.Out.Number: '#ffa273', Token.Separator: '#ff627e', Token.Toolbar.Search: '#ff627e noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#ff627e noinherit', Token.Toolbar.Arg: '#ff627e noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#bb8a7a #ffcec6', Token.Toolbar.Signature.CurrentName: 'bg:#4a2d3d #ff627e bold', Token.Toolbar.Signature.Operator: '#ffcec6 bold', Token.Docstring: '#ffa273', Token.Toolbar.Validation: 'bg:#4a2d3d #ff627e', Token.Toolbar.Status: 'bg:#4a2d3d #ffcec6', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#4a2d3d #ffa273', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#4a2d3d #ff627e', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#4a2d3d #ffa273', Token.Toolbar.Status.Key: 'bg:#bb8a7a #ffcec6', Token.Toolbar.Status.PasteModeOn: 'bg:#4a2d3d #ff627e', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#4a2d3d #ffa273', Token.Toolbar.Status.PythonVersion: 'bg:#4a2d3d #ff9e64 bold', Token.Aborted: '#ff627e', Token.Sidebar: 'bg:#bb8a7a #ffcec6', Token.Sidebar.Title: 'bg:#4a2d3d #ffd76b bold', Token.Sidebar.Label: 'bg:#bb8a7a #ffa273', Token.Sidebar.Status: 'bg:#bb8a7a #ffcec6', Token.Sidebar.Selected.Label: 'bg:#4a2d3d #ff627e', Token.Sidebar.Selected.Status: 'bg:#4a2d3d #ffcec6 bold', Token.Sidebar.Separator: 'bg:#bb8a7a #4a2d3d underline', Token.Sidebar.Key: 'bg:#bb8a7a #ff627e bold', Token.Sidebar.Key.Description: 'bg:#bb8a7a #ffcec6', Token.Sidebar.HelpText: 'bg:#bb8a7a #ffcec6', Token.History.Line: '', Token.History.Line.Selected: 'bg:#bb8a7a #ffcec6', Token.History.Line.Current: 'bg:#4a2d3d #ffa273', Token.History.Line.Selected.Current: 'bg:#4a2d3d #ff627e', Token.History.ExistingInput: '#ff9e64', Token.Window.Border: '#ff9e64', Token.Window.Title: 'bg:#bb8a7a #ffcec6', Token.Window.TIItleV2: 'bg:#4a2d3d #ffcec6 bold', Token.AcceptMessage: 'bg:#bb8a7a #ffa273', Token.ExitConfirmation: 'bg:#4a2d3d #ff627e', Token.SearchMatch: 'bg:#bb8a7a #ffcec6', Token.SearchMatch.Current: 'bg:#4a2d3d #ff627e underline', Token.SelectedText: 'bg:#bb8a7a #ffcec6', Token.Toolbar.Completions: 'bg:#bb8a7a #ffcec6', Token.Toolbar.Completions.Arrow: 'bg:#bb8a7a #ff627e bold', Token.Toolbar.Completions.Completion: 'bg:#bb8a7a #ffcec6', Token.Toolbar.Completions.Completion.Current: 'bg:#4a2d3d #ffa273 underline', Token.Menu.Completions.Completion: 'bg:#bb8a7a #ffcec6', Token.Menu.Completions.Completion.Current: 'bg:#4a2d3d #ffa273', Token.Menu.Completions.Meta: 'bg:#bb8a7a #bb8a7a', Token.Menu.Completions.Meta.Current: 'bg:#bb8a7a #ff9e64', Token.Menu.Completions.ProgressBar: 'bg:#ff627e', Token.Menu.Completions.ProgressButton: 'bg:#bb8a7a'}

clara_monokai = {Token.LineNumber: '#55CDFC bg:#282a36', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #D026B0', Token.In.Number: '', Token.Out: '#21d988', Token.Out.Number: '#21d988', Token.Separator: '#D026B0', Token.Toolbar.Search: '#D026B0 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#D026B0 noinherit', Token.Toolbar.Arg: '#D026B0 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#8BADD9 #F5F5F5', Token.Toolbar.Signature.CurrentName: 'bg:#282a36 #D026B0 bold', Token.Toolbar.Signature.Operator: '#F5F5F5 bold', Token.Docstring: '#21d988', Token.Toolbar.Validation: 'bg:#282a36 #D026B0', Token.Toolbar.Status: 'bg:#282a36 #F5F5F5', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#282a36 #21d988', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#282a36 #D026B0', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#282a36 #21d988', Token.Toolbar.Status.Key: 'bg:#8BADD9 #F5F5F5', Token.Toolbar.Status.PasteModeOn: 'bg:#282a36 #D026B0', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#282a36 #21d988', Token.Toolbar.Status.PythonVersion: 'bg:#282a36 #008cf0 bold', Token.Aborted: '#D026B0', Token.Sidebar: 'bg:#8BADD9 #F5F5F5', Token.Sidebar.Title: 'bg:#282a36 #55CDFC bold', Token.Sidebar.Label: 'bg:#8BADD9 #21d988', Token.Sidebar.Status: 'bg:#8BADD9 #F5F5F5', Token.Sidebar.Selected.Label: 'bg:#282a36 #D026B0', Token.Sidebar.Selected.Status: 'bg:#282a36 #F5F5F5 bold', Token.Sidebar.Separator: 'bg:#8BADD9 #282a36 underline', Token.Sidebar.Key: 'bg:#8BADD9 #D026B0 bold', Token.Sidebar.Key.Description: 'bg:#8BADD9 #F5F5F5', Token.Sidebar.HelpText: 'bg:#8BADD9 #F5F5F5', Token.History.Line: '', Token.History.Line.Selected: 'bg:#8BADD9 #F5F5F5', Token.History.Line.Current: 'bg:#282a36 #21d988', Token.History.Line.Selected.Current: 'bg:#282a36 #D026B0', Token.History.ExistingInput: '#008cf0', Token.Window.Border: '#008cf0', Token.Window.Title: 'bg:#8BADD9 #F5F5F5', Token.Window.TIItleV2: 'bg:#282a36 #F5F5F5 bold', Token.AcceptMessage: 'bg:#8BADD9 #21d988', Token.ExitConfirmation: 'bg:#282a36 #D026B0', Token.SearchMatch: 'bg:#8BADD9 #F5F5F5', Token.SearchMatch.Current: 'bg:#282a36 #D026B0 underline', Token.SelectedText: 'bg:#8BADD9 #F5F5F5', Token.Toolbar.Completions: 'bg:#8BADD9 #F5F5F5', Token.Toolbar.Completions.Arrow: 'bg:#8BADD9 #D026B0 bold', Token.Toolbar.Completions.Completion: 'bg:#8BADD9 #F5F5F5', Token.Toolbar.Completions.Completion.Current: 'bg:#282a36 #21d988 underline', Token.Menu.Completions.Completion: 'bg:#8BADD9 #F5F5F5', Token.Menu.Completions.Completion.Current: 'bg:#282a36 #21d988', Token.Menu.Completions.Meta: 'bg:#8BADD9 #8BADD9', Token.Menu.Completions.Meta.Current: 'bg:#8BADD9 #008cf0', Token.Menu.Completions.ProgressBar: 'bg:#D026B0', Token.Menu.Completions.ProgressButton: 'bg:#8BADD9'}

synthwave_monokai = {Token.LineNumber: '#EA00D9 bg:#262335', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #FF1654', Token.In.Number: '', Token.Out: '#0ABDC6', Token.Out.Number: '#0ABDC6', Token.Separator: '#FF1654', Token.Toolbar.Search: '#FF1654 noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#FF1654 noinherit', Token.Toolbar.Arg: '#FF1654 noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#6B7A99 #F8F8F2', Token.Toolbar.Signature.CurrentName: 'bg:#262335 #FF1654 bold', Token.Toolbar.Signature.Operator: '#F8F8F2 bold', Token.Docstring: '#0ABDC6', Token.Toolbar.Validation: 'bg:#262335 #FF1654', Token.Toolbar.Status: 'bg:#262335 #F8F8F2', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#262335 #0ABDC6', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#262335 #FF1654', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#262335 #0ABDC6', Token.Toolbar.Status.Key: 'bg:#6B7A99 #F8F8F2', Token.Toolbar.Status.PasteModeOn: 'bg:#262335 #FF1654', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#262335 #0ABDC6', Token.Toolbar.Status.PythonVersion: 'bg:#262335 #711C91 bold', Token.Aborted: '#FF1654', Token.Sidebar: 'bg:#6B7A99 #F8F8F2', Token.Sidebar.Title: 'bg:#262335 #EA00D9 bold', Token.Sidebar.Label: 'bg:#6B7A99 #0ABDC6', Token.Sidebar.Status: 'bg:#6B7A99 #F8F8F2', Token.Sidebar.Selected.Label: 'bg:#262335 #FF1654', Token.Sidebar.Selected.Status: 'bg:#262335 #F8F8F2 bold', Token.Sidebar.Separator: 'bg:#6B7A99 #262335 underline', Token.Sidebar.Key: 'bg:#6B7A99 #FF1654 bold', Token.Sidebar.Key.Description: 'bg:#6B7A99 #F8F8F2', Token.Sidebar.HelpText: 'bg:#6B7A99 #F8F8F2', Token.History.Line: '', Token.History.Line.Selected: 'bg:#6B7A99 #F8F8F2', Token.History.Line.Current: 'bg:#262335 #0ABDC6', Token.History.Line.Selected.Current: 'bg:#262335 #FF1654', Token.History.ExistingInput: '#711C91', Token.Window.Border: '#711C91', Token.Window.Title: 'bg:#6B7A99 #F8F8F2', Token.Window.TIItleV2: 'bg:#262335 #F8F8F2 bold', Token.AcceptMessage: 'bg:#6B7A99 #0ABDC6', Token.ExitConfirmation: 'bg:#262335 #FF1654', Token.SearchMatch: 'bg:#6B7A99 #F8F8F2', Token.SearchMatch.Current: 'bg:#262335 #FF1654 underline', Token.SelectedText: 'bg:#6B7A99 #F8F8F2', Token.Toolbar.Completions: 'bg:#6B7A99 #F8F8F2', Token.Toolbar.Completions.Arrow: 'bg:#6B7A99 #FF1654 bold', Token.Toolbar.Completions.Completion: 'bg:#6B7A99 #F8F8F2', Token.Toolbar.Completions.Completion.Current: 'bg:#262335 #0ABDC6 underline', Token.Menu.Completions.Completion: 'bg:#6B7A99 #F8F8F2', Token.Menu.Completions.Completion.Current: 'bg:#262335 #0ABDC6', Token.Menu.Completions.Meta: 'bg:#6B7A99 #6B7A99', Token.Menu.Completions.Meta.Current: 'bg:#6B7A99 #711C91', Token.Menu.Completions.ProgressBar: 'bg:#FF1654', Token.Menu.Completions.ProgressButton: 'bg:#6B7A99'}

tomorrow_night_eighties = {Token.LineNumber: 'bg:#2d2d2d #999999', Token.Prompt: 'bold', Token.Prompt.Dots: 'noinherit', Token.In: 'bold #cc99cc', Token.In.Number: '', Token.Out: '#6699cc', Token.Out.Number: '#6699cc', Token.Separator: '#f2777a', Token.Toolbar.Search: '#f2777a noinherit', Token.Toolbar.Search.Text: 'noinherit', Token.Toolbar.System: '#f2777a noinherit', Token.Toolbar.Arg: '#f2777a noinherit', Token.Toolbar.Arg.Text: 'noinherit', Token.Toolbar.Signature: 'bg:#393939 #cccccc', Token.Toolbar.Signature.CurrentName: 'bg:#2d2d2d #f2777a bold', Token.Toolbar.Signature.Operator: '#cccccc bold', Token.Docstring: '#99cc99', Token.Toolbar.Validation: 'bg:#2d2d2d #f2777a', Token.Toolbar.Status: 'bg:#2d2d2d #cccccc', Token.Toolbar.Status.BatteryPluggedIn: 'bg:#2d2d2d #99cc99', Token.Toolbar.Status.BatteryNotPluggedIn: 'bg:#2d2d2d #f2777a', Token.Toolbar.Status.Title: 'underline', Token.Toolbar.Status.InputMode: 'bg:#2d2d2d #99cc99', Token.Toolbar.Status.Key: 'bg:#393939 #cccccc', Token.Toolbar.Status.PasteModeOn: 'bg:#2d2d2d #f2777a', Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#2d2d2d #99cc99', Token.Toolbar.Status.PythonVersion: 'bg:#2d2d2d #6699cc bold', Token.Aborted: '#f2777a', Token.Sidebar: 'bg:#393939 #cccccc', Token.Sidebar.Title: 'bg:#2d2d2d #ffcc66 bold', Token.Sidebar.Label: 'bg:#393939 #99cc99', Token.Sidebar.Status: 'bg:#393939 #cccccc', Token.Sidebar.Selected.Label: 'bg:#2d2d2d #f2777a', Token.Sidebar.Selected.Status: 'bg:#2d2d2d #cccccc bold', Token.Sidebar.Separator: 'bg:#393939 #2d2d2d underline', Token.Sidebar.Key: 'bg:#393939 #f2777a bold', Token.Sidebar.Key.Description: 'bg:#393939 #cccccc', Token.Sidebar.HelpText: 'bg:#393939 #cccccc', Token.History.Line: '', Token.History.Line.Selected: 'bg:#393939 #cccccc', Token.History.Line.Current: 'bg:#2d2d2d #99cc99', Token.History.Line.Selected.Current: 'bg:#2d2d2d #f2777a', Token.History.ExistingInput: '#6699cc', Token.Window.Border: '#999999', Token.Window.Title: 'bg:#393939 #cccccc', Token.Window.TIItleV2: 'bg:#2d2d2d #cccccc bold', Token.AcceptMessage: 'bg:#393939 #99cc99', Token.ExitConfirmation: 'bg:#2d2d2d #f2777a', Token.SearchMatch: 'bg:#393939 #cccccc', Token.SearchMatch.Current: 'bg:#2d2d2d #f2777a underline', Token.SelectedText: 'bg:#393939 #cccccc', Token.Toolbar.Completions: 'bg:#393939 #cccccc', Token.Toolbar.Completions.Arrow: 'bg:#393939 #f2777a bold', Token.Toolbar.Completions.Completion: 'bg:#393939 #cccccc', Token.Toolbar.Completions.Completion.Current: 'bg:#2d2d2d #99cc99 underline', Token.Menu.Completions.Completion: 'bg:#393939 #cccccc', Token.Menu.Completions.Completion.Current: 'bg:#2d2d2d #99cc99', Token.Menu.Completions.Meta: 'bg:#393939 #999999', Token.Menu.Completions.Meta.Current: 'bg:#393939 #6699cc', Token.Menu.Completions.ProgressBar: 'bg:#f2777a', Token.Menu.Completions.ProgressButton: 'bg:#393939'}

for sty in [tomorrow_night_eighties,synthwave_monokai,clara_monokai,sunset_monokai,synthwave_monokai_style,monokai_style,monokai]:
    #Parenthesis coloring
            sty[Token.Punctuation]='             #fb51a6'

