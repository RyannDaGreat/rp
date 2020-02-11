# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
#TODO: Turn the comments at the beginning of each function into docstrings so they can be read by the builtin help function
# python /Users/Ryan/PycharmProjects/Py27RyanStandard2.7/Groupie.py ftF11dwbP61OfPf9QsXBfS5usCdQdBkkMieObdvZ -g 'The Think Tank'
# Imports that are necessary for the 'r' module:
# Imports I tend to use a lot and include so they their names can be directly imported from th:
# region Import
# This is useful for running things on the terminal app or in blender
# import r# For rinsp searches for functions in the r module, so I don't need to keep typing 'import r' over and over again
import sys
import threading
from builtins import *#For autocompletion with pseudo_terminal
from time import sleep
sys.path.append(__file__[:-len("r.py")])

# Places I want to access no matter where I launch r.py
# sys.path.append('/Users/Ryan/PycharmProjects/RyanBStandards_Python3.5')
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages')
# endregion
# region ［entuple， detuple］

try:
    import numpy as np
except:
    print("Warning: Cannot import numpy. Please excuse any 'np is None' errors, or try pip_install('numpy')")

def entuple(x):
    # For pesky petty things.
    if isinstance(x,tuple):
        return x
    return x,
def detuple(x):
    # For pesky petty things. Code is simpler than explanation here.
    try:
        if len(x) == 1:
            return x[0]
    except:
        pass
    return x
# endregion
# region ［enlist， delist］
def enlist(x):
    # For pesky petty things.
    if isinstance(x,list):
        return x
    return [x]

def delist(x):
    # For pesky petty things. Code is simpler than explanation here.
    try:
        if len(x) == 1:
            return x[0]
    except:
        pass
    return x
# endregion
# region  rCode: ［itc‚ run‚ fog‚ scoop‚ seq_map‚ par_map‚ seq‚ par‚ rev‚ pam‚ identity，list_pop，summation，product］
#   ∞
#   ∫𝓍²∂𝓍
# ﹣∞
def itc(f,x):
    #itc ==== iterate to convergence, where f(x)==x.
    #In other words, we iterate f on x until we reach a fixed point.
    while True:
        y=f(x)
        if y==x:
            return y
        x=y
# region  ［run‚ fog］
def run(f,*g,**kwg):  # Pop () ⟶ )(
    return f(*g,**kwg)
def fog(f,*g,**kwg):  # Encapsulate )( ⟶ ()      'fog' ≣ ƒ ∘ g‚ where g can be any number of parameters.
    return lambda:f(*g,**kwg)
# endregion
# region［scoop］
# scoop could have been implemented with seq. I chose not to.
def scoop(funcⵓscoopˏnew,list_in,init_value=None):
    from copy import copy,deepcopy
    # Try to make a copy just in case init_value is a list
    try:
        scoop_value=deepcopy(init_value)
    except:
        try:
            scoop_value=copy(init_value)
        except:
            scoop_value=init_value
    for element in list_in:
        scoop_value=funcⵓscoopˏnew(scoop_value,element)
    return scoop_value
# endregion
# region ［seq_map‚ par_map］
def seq_map(func,*iterables):
    # Like par_map, this def features non-lazy evaluation! (Unlike python's map function, which does not. Proof: map(print,['hello']) does not print anything, but [*map(print,['hello'])] does.)
    return list(map(func,*iterables))  # Basically it's exactly like python's built-in map function, except it forces it to evaluate everything inside it before it returns the output.
from multiprocessing.dummy import Pool as ThreadPool  # ⟵ par_map uses ThreadPool. We import it now so we don't have to later, when we use par_map.
def par_map(func,*iterables,number_of_threads=None,chunksize=None):
    # Multi-threaded map function. When I figure out a way to do parallel computations, this def (conveniently high-level) will be replaced.
    try:
        par_pool=ThreadPool(number_of_threads)
        try:
            out=par_pool.map(lambda args:func(*args),zip(*iterables),chunksize=chunksize)  # ⟵ A more complicated version of out=par_pool.map(func,iterable,chunksize=chunksize). Current version lets func accept multiple arguments.
        except:
            out=par_pool.map(func,iterables,chunksize=chunksize)
        par_pool.terminate()  # ⟵ If we don't have this line here, the number of threads running AKA threading.active_count() will continue to grow even after this def has returned, ∴ eventually causing the RunTime error exception mentioned below.
        return out
    except RuntimeError:  # ⟵ Assuming we got "RuntimeError: can't start new thread", we will calculate it sequentially instead. It will give the same result, but it won't be in parallel.
        return seq_map(func,*iterables)
# endregion
# region ［seq‚ par］
def seq(funcs,*init):
    # The current flagship function of rCode. This function can, in theory, single-handedly replace all other rCode functions (except par, which is analogous to seq). (Though it might be inconvenient to do so)
    # Possible future add-on: Enable recursive calls with a special value of func? (Probably won't though)
    try:  # Usually funcs will be an iterable. But if it is not, this test will catch it. This is because seq(print,'hello world')≣seq([print],'hello world')
        funcs=list(funcs)  # A simple check to find out whether funcs is iterable or not. If it is, it becomes a list (even if it was originally, let's say, a tuple).
    except TypeError:  # 'funcs' was not iterable; ∴ 'funcs' must be a single, callable function
        return funcs(*init)  # Because we have not yet iterated, we contain certain that 'init' is a tuple.

    # assert isinstance(funcs,list) # Internal logic assertion. This should always be true because of 'funcs=[*funcs]'
    for func in funcs:  # If we reach this line, we know ∴ 'funcs' is a list.
        temp=func(*init) if isinstance(init,tuple) else func(init)
        if temp is not None:
            init=temp
    return init
def par(funcsᆢvoids,*params):
    # NOTE: PARAMS NEVER CHANGES!!! The applications of that would be too limited to justify the effort of creating it. Instead, this def simply treats all functions as voids in the same way that seq could.
    # seq's little sister, and child of par_map. Only analagous to seq in specific contexts. This function is NOT capable of returning anything useful due to the inherent nature of multi-threading.
    par_map(lambda func:func(*params),funcsᆢvoids)  # Shares a similar syntax to seq. AKA multiple functions with a single set of parameters.
# endregion
# region  ［rev］
rev=lambda f,n:lambda *𝓍_:seq([f] * n,*𝓍_)  # Pseudo-revolutions (technically iterations)     Ex: rev(lambda x:x+1,5)(0) == 5
# endregion
# region ［pam］
def pam(funcs,*args,**kwargs):
    # pam is map spelt backwards. pam maps multiple defs onto a single set of arguments (instead of map, which maps multiple sets of arguments onto one function)
    assert is_iterable(funcs),str(funcs) + " ≣ funcs，is NOT iterable. Don't bother using pam! Pam is meant for mapping multiple functions onto one set of arguments; and from what I can tell you only have one function."
    return [f(*args,**kwargs) for f in funcs]
# endregion
# region ［identity］
def identity(*args):
    # The identity function. ƒ﹙𝓍﹚﹦ 𝓍    where   ƒ ≣ identity
    #Examples:
    #   identity(2) == 2
    #   identity('Hello World!') == 'Hello World!'
    #   identity(1,2,3) == (1,2,3)  #When given multiple args, returns a tuple
    return detuple(args)
# endregion
# region ［list_pop］ (a bit of a misnomer; I know that now, after having taken CSE214.)
list_pop=lambda list_2d:scoop(lambda old,new:list(old) + list(new),list_2d,[])
# endregion
# region ［summation，product］
def product(x):
    # Useful because this literally uses the '*' operator over and over again instead of necessarily treating the elements as numbers.
    return scoop(lambda 𝓍,𝓎:𝓍 * 𝓎,x,x[0]) if len(x) else 1
    # assert is_iterable(x)
    # try:
    #     out=x[0]
    # except:
    #     return 1# x has no indices
    # for y in x[1:]:
    #     out*=y
    # return out
def summation(x,start=None):
    # Useful because this literally uses the '+' operator over and over again instead of necessarily treating the elements as numbers.
    # list_pop(l)≣summation(l)
    # sum(x,[])≣summation(x)
    # sum(x)≣summation(x)
    return scoop(lambda 𝓍,𝓎:𝓍 + 𝓎,x,start if start is not None else x[0]) if len(x) else start
    # assert is_iterable(x)
    # try:
    #     out=x[0]
    # except:
    #     return 0# x has no indices
    # for y in x[1:]:
    #     out+=y
    # return out

# endregion
# endregion
# region  Time:［gtoc，tic‚ toc‚ ptoc‚ ptoctic‚ millis，micros，nanos］
import time
_global_tic=time.time()
gtoc=time.time  # global toc
def tic() -> callable:
    global _global_tic
    _global_tic=local_tic=time.time()
    def local_toc():  # Gives a permanent toc to this tic, specifically
        return gtoc() - local_tic
    return local_toc  # Returns a method so you can do a=tic();a.toc() ⟵ Gives a local (not global) toc value so each tic can be used as a new timer
def toc() -> float:
    return gtoc() - _global_tic
def ptoc(new_line=True) -> None:
    print(str(toc()) + " seconds",end='\n'if new_line else '')
def ptoctic(label='') -> None:
    print(label,end='')
    ptoc()
    tic()
# ⁠⁠⁠⁠                                        ⎧                                      ⎫
# ⁠⁠⁠⁠                                        ⎪     ⎧                               ⎫⎪
# ⁠⁠⁠⁠                                        ⎪     ⎪⎧                         ⎫    ⎪⎪
_milli_micro_nano_converter=lambda s,n:int(round((s() if callable(s) else s) * n))
# ⁠⁠⁠⁠                                        ⎪     ⎪⎩                         ⎭    ⎪⎪
# ⁠⁠⁠⁠                                        ⎪     ⎩                               ⎭⎪
# ⁠⁠⁠⁠                                        ⎩                                      ⎭
# You can do millis(tic()) ⟵ Will probably be about 0， millis(toc)， millis(1315)， millis() ⟵ Gets global time by default
def seconds(seconds=gtoc) -> int:
    return _milli_micro_nano_converter(seconds,10 ** 0)
def millis(seconds=gtoc) -> int:
    return _milli_micro_nano_converter(seconds,10 ** 3)
def micros(seconds=gtoc) -> int:
    return _milli_micro_nano_converter(seconds,10 ** 6)
def nanos(seconds=gtoc) -> int:
    return _milli_micro_nano_converter(seconds,10 ** 9)

# endregion
# region  Files and such: ［get_current_directory‚ get_all_file_names］
import glob,sys
def get_current_directory():
    # Get the result of 'cd' in a shell. This is the current folder where save or load things by default.
    # SUMMARY: get_current_directory() ≣ sys.path[0] ﹦ ﹙default folder_path﹚ ﹦ ﹙current directory﹚ ﹦ /Users/Ryan/PycharmProjects/RyanBStandards_Python3.5
    import os
    return os.getcwd()

def get_all_file_names(file_name_ending: str = '',file_name_must_contain: str = '',folder_path: str = get_current_directory(),show_debug_narrative: bool = False):
    # SUMMARY: This method returns a list of all file names files in 'folder_path' that meet the specifications set by 'file_name_ending' and 'file_name_must_contain'
    # Leave file_name_ending blank to return all file names in the folder.
    # To find all file names of a specific extension, make file_name_ending ﹦ '.jpg' or 'png' etc.
    # Note: It does not matter if you have '.png' vs 'png'! It will return a list of all files whose name's ends…
    #     …with file_name_ending (whether that comes from the file type extension or not). Note that you can use this to search…
    #     …for specific types of file names that YOU made arbitrarily, like 'Apuppy.png','Bpuppy.png' ⟵ Can both be found with…
    #     …file_name_ending ﹦ 'puppy.png'
    # file_name_must_contain ⟶ all names in the output list must contain this character sequence
    # show_debug_narrative ⟶ controls whether to print out details about what this function is doing that might help to debug something.
    #     …By default this is disabled to avoid spamming the poor programmer who dares use this function.
    # ;;::O(if)OOO
    os.chdir(folder_path)
    if show_debug_narrative:
        print(get_all_file_names.__name__ + ": (Debug Narrative) Search Directory ﹦ " + folder_path)
    output=[]
    for file_name in glob.glob("*" + file_name_ending):
        if file_name_must_contain in file_name:
            output.append(file_name)  # I tried doing it with the '+' operator, but it returned a giant list of individual characters. This way works better.
            if show_debug_narrative:
                print(get_all_file_names.__name__ + ": (Debug Narrative) Found '" + file_name + "'")
    if show_debug_narrative:
        print(get_all_file_names.__name__ + ' (Debug Narrative) Output ﹦ ' + str(output))
    return output
# endregion
# region String ⟷ Integer List:  ［int_list_to_string‚ string_to_int_list］
int_list_to_string=lambda int_list:"".join(list(chr(i) for i in int_list))
string_to_int_list=lambda string:list(ord(i) for i in string)
# USAGE EXAMPLE:
#   print((lambda x:int_list_to_string(range(ord(x)-500,ord(x)+500)))("⚢"))
#   print(int_list_to_string([*(a+1 for a in string_to_int_list("♔"))]))
#   #♈♉♊♋♌♍♎♏♐♑♒♓ ♔♕♖♗♘♙♚♛♜♝♞♟ gen
#   #⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯ ❨❩❪❫❬❭❮❯❰❱❲❳❴❵ ⚀⚁⚂⚃⚄⚅ ♔♕♖♗♘♙♚♛♜♝♞♟
# endregion
# region Fansi:［fansi，fansi_print，print_fansi_reference_table，fansi_syntax_highlighting］   (Format-ANSI colors and styles for the console)
# noinspection PyShadowingBuiltins
def currently_running_windows():
    import os
    return os.name=='nt'
def currently_running_posix():
    import os
    return os.name=='posix'
def currently_running_mac():
    import platform
    return platform.system()=='Darwin'
def currently_running_linux():
    import platform
    return platform.system()=='Linux'

currently_running_unix=currently_running_posix#Technically posix!=unix, but realistically we don't care...i mean what OS is posix and not unix that somebody's likely to run rp on?
def terminal_supports_ansi():
    if currently_running_windows():
        try:
            from colorama import init
            init()  # Trying to enable ANSI coloring on windows console
            return True
        except:
            return False
    return True
    # return sys.stdout.isatty()# There are probably more sophistacated, better ways to check, but I don't know them.
def terminal_supports_unicode():
    if currently_running_windows():# Try to enable unicode, but fail if we can't
        try:
            from win_unicode_console import enable
            enable()  # Trying to enable unicode characters on windows console
            return True
        except:
            return False
    # ∴ we are not running Windows
    return True# I don't know how to check whether you can render characters such as ⮤, ✔, or ⛤ etc


def fansi_is_enabled():
    #Returns true IFF fansi is enabled
    return not _disable_fansi
def fansi_is_disabled():
    #Returns true IFF fansi is disabled
    return _disable_fansi
_disable_fansi=False
def disable_fansi():
    global _disable_fansi
    _disable_fansi=True
def enable_fansi():
    global _disable_fansi
    _disable_fansi=False

from contextlib import contextmanager
@contextmanager
def without_fansi():
    #To run a block of code without using fansi.
    #Example:
    #   f=lambda:fansi_print("Hello World",'cyan','bold','red')
    #   f()#With fansi
    #   with without_fansi():
    #       f()#Without fansi
    global _disable_fansi
    old_disable_fansi=_disable_fansi
    _disable_fansi=True
    try:
        yield
    finally:
        _disable_fansi=old_disable_fansi


def fansi(text_string,text_color=None,style=None,background_color=None,*,per_line=False):
    #This function uses ANSI escape sequnces to make colored text in a terminal.
    #It can also make bolded, underlined, or highlighted text.
    #It uses ANSI escape sequences to do this...
    #    ...and so calling it 'fansi' is a pun on 'fancy' and 'ansi'
    # 'fansi' is a pun, referring to ANSI and fancy
    # Uses ANSI formatting to give the terminal color outputs.
    # There are only 8 possible choices from each category, in ［０‚７］⋂ ℤ
    # Adding 0,30,and 40 because of the ANSI codes. Subtracting 1 later on because the syntax
    # of this def says that '0' is the absence of any style etc, whereas 1-8 are active styles.
    # The 'per_line' option applies fansi to every line, which is useful when trying to draw tables and such
    # Some terminals cant handle ansi escape sequences and just print garbage, so if _disable_fansi is turned on this function just returns unformatted text.
    #   (This is usually only the case with more obscure terminals, such as one I have for ssh'ing on my phone. But they do exist)
    # To undo the effect of this function on a string (aka to un-format a string) use rp.strip_ansi_escapes()  (see its documentation for more details)
    # EXAMPLE: print(fansi('ERROR:','red','bold')+fansi(" ATE TOO MANY APPLES!!!",'blue','underlined','yellow'))
    if per_line:
        lines=line_split(text_string)
        lines=[fansi(line,text_color,style,background_color,per_line=False) for line in lines]
        return line_join(lines)
    if _disable_fansi:
        return text_string#This is for terminals that dont support colors. I don't have a method wrapper for this yet, though.
    text_string=str(text_string)
    if not terminal_supports_ansi():# We cannot guarentee we have ANSI support; we might get ugly crap like '\[0Hello World\[0' or something ugly like that!
        return text_string# Don't format it; just leave it as-is
    if text_string=='':# Without this, print(fansi("",'blue')+'Hello World'
        return ''
    if isinstance(text_color,str):  # if text_color is a string, convert it into the correct integer and handle the associated exceptions
        text_colors={'black':0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'gray':7,'grey':7}
        try:
            text_color=text_colors[text_color.lower()]
        except:
            print("ERROR: def fansi: input-error: text_color = '{0}' BUT '{0}' is not a valid key! Replacing text_color as None. Please choose from {1}".format(text_color,str(list(text_colors))))
            text_color=None
    if isinstance(style,str):  # if background_color is a string, convert it into the correct integer
        styles={'bold':1,'faded':2,'underlined':4,'blinking':5,'outlined':7}
        try:
            style=styles[style.lower()]  # I don't know what the other integers do.
        except:
            print("ERROR: def fansi: input-error: style = '{0}' BUT '{0}' is not a valid key! Replacing style as None. Please choose from {1}".format(style,str(list(styles))))
            style=None
    if isinstance(background_color,str):  # if background_color is a string, convert it into the correct integer
        background_colors={'black':0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'gray':7,'grey':7}
        try:
            background_color=background_colors[background_color.lower()]
        except:
            print("ERROR: def fansi: input-error: background_color = '{0}' BUT '{0}' is not a valid key! Replacing background_color as None. Please choose from {1}".format(background_color,str(list(background_colors))))
            background_color=None

    format=[]
    if style is not None:
        assert 0 <= style <= 7,"style == " + str(style) + " ∴ ¬﹙0 <= style <= 7﹚ ∴ AssertionError"
        style+=0
        format.append(str(style))
    if text_color is not None:
        assert 0 <= text_color <= 7,"text_color == " + str(text_color) + " ∴ ¬﹙0 <= text_color <= 7﹚ ∴ AssertionError"
        text_color+=30
        format.append(str(text_color))
    if background_color is not None:
        assert 0 <= background_color <= 7,"background_color == " + str(background_color) + " ∴ ¬﹙0 <= background_color <= 7﹚ ∴ AssertionError"
        background_color+=40
        format.append(str(background_color))

    return "\x1b[%sm%s\x1b[0m" % (';'.join(format),str(text_string))  # returns a string with the appropriate formatting applied
# region fansi Examples
# print(fansi('ERROR:','red','bold')+fansi(" ATE TOO MANY APPLES!!!",'blue','underlined','yellow'))
# from random import randint
# print(seq([lambda old:old+fansi(chr(randint(0,30000)),randint(0,7),randint(0,7),randint(0,7))]*100,''))
# endregion
def fansi_print(text_string: object,text_color: object = None,style: object = None,background_color: object = None,new_line=True) -> object:
    #This function prints colored text in a terminal.
    #It can also print bolded, underlined, or highlighted text.
    #It uses ANSI escape sequences to do this...
    #    ...and so calling it 'fansi' is a pun on 'fancy' and 'ansi'
    # Example: print(fansi('ERROR:','red','bold')+fansi(" ATE TOO MANY APPLES!!!",'blue','underlined','yellow'))
    print(fansi(text_string,text_color=text_color,style=style,background_color=background_color),end='\n' if new_line else'',flush=True)
# noinspection PyShadowingBuiltins
def print_fansi_reference_table() -> None:
    # prints table of formatted text format options for fansi. For reference
    for style in range(8):
        for fg in range(30,38):
            s1=''
            for bg in range(40,48):
                format=';'.join([str(style),str(fg),str(bg)])
                s1+='\x1b[%sm %s \x1b[0m' % (format,format)
            print(s1)
        print('\n')
def fansi_syntax_highlighting(code: str,namespace=(),style_overrides={}):
    # PLEASE NOTE THAT I DID NOT WRITE SOME OF THIS CODE!!! IT CAME FROM https://github.com/akheron/cpython/blob/master/Tools/scripts/highlight.py
    # Assumes code was written in python.
    # Method mainly intended for rinsp.
    # I put it in the r class for convenience.
    # Works when I paste methods in but doesn't seem to play nicely with rinsp. I don't know why yet.
    # See the highlight_sourse_in_ansi module for more stuff including HTML highlighting etc.
    default_ansi={
        'comment':('\033[0;31m','\033[0m'),
        'string':('\033[0;32m','\033[0m'),
        'docstring':('\033[0;32m','\033[0m'),
        'keyword':('\033[0;33m','\033[0m'),
        'builtin':('\033[0;35m','\033[0m'),
        'definition':('\033[0;33m','\033[0m'),
        'defname':('\033[0;34m','\033[0m'),
        'operator':('\033[0;33m','\033[0m'),
    }
    default_ansi.update(style_overrides)
    try:
        import keyword,tokenize,cgi,re,functools
        try:
            import builtins
        except ImportError:
            import builtins as builtins
        def is_builtin(s):
            'Return True if s is the name of a builtin'
            return hasattr(builtins,s) or s in namespace
        def combine_range(lines,start,end):
            'Join content from a range of lines between start and end'
            (srow,scol),(erow,ecol)=start,end
            if srow == erow:
                return lines[srow - 1][scol:ecol],end
            rows=[lines[srow - 1][scol:]] + lines[srow: erow - 1] + [lines[erow - 1][:ecol]]
            return ''.join(rows),end
        def analyze_python(source):
            '''Generate and classify chunks of Python for syntax highlighting.
               Yields tuples in the form: (category, categorized_text).
            '''
            lines=source.splitlines(True)
            lines.append('')
            readline=functools.partial(next,iter(lines),'')
            kind=tok_str=''
            tok_type=tokenize.COMMENT
            written=(1,0)
            for tok in tokenize.generate_tokens(readline):
                prev_tok_type,prev_tok_str=tok_type,tok_str
                tok_type,tok_str,(srow,scol),(erow,ecol),logical_lineno=tok
                kind=''
                if tok_type == tokenize.COMMENT:
                    kind='comment'
                elif tok_type == tokenize.OP and tok_str[:1] not in '{}[](),.:;@':
                    kind='operator'
                elif tok_type == tokenize.STRING:
                    kind='string'
                    if prev_tok_type == tokenize.INDENT or scol == 0:
                        kind='docstring'
                elif tok_type == tokenize.NAME:
                    if tok_str in ('def','class','import','from'):
                        kind='definition'
                    elif prev_tok_str in ('def','class'):
                        kind='defname'
                    elif keyword.iskeyword(tok_str):
                        kind='keyword'
                    elif is_builtin(tok_str) and prev_tok_str != '.':
                        kind='builtin'
                if kind:
                    if written != (srow,scol):
                        text,written=combine_range(lines,written,(srow,scol))
                        yield '',text
                    text,written=tok_str,(erow,ecol)
                    yield kind,text
            line_upto_token,written=combine_range(lines,written,(erow,ecol))
            yield '',line_upto_token
        def ansi_highlight(classified_text,colors=default_ansi):
            'Add syntax highlighting to source code using ANSI escape sequences'
            # http://en.wikipedia.org/wiki/ANSI_escape_code
            result=[]
            for kind,text in classified_text:
                opener,closer=colors.get(kind,('',''))
                result+=[opener,text,closer]
            return ''.join(result)
        return ansi_highlight(analyze_python(code))
    except:
        return code  # Failed to highlight code, presumably because of an import error.

# endregion
# region  Copy/Paste: ［string_to_clipboard，string_from_clipboard］
import os
_local_clipboard_string=''#if we can't access a system OS clipboard, try and fake it with a local clipboard istead. Of course, you need to use the string_to_clipboard and clipboard_to_string functions to make this work, but that's ok
_local_clipboard_string_path=__file__+'.rp_local_clipboard'
def _get_local_clipboard_string():
    #Try to get the string from a file (so we can share our fake clipboard across processes. THis is important over SSH into headless systems that don't support clipboards, but we still want to keep our clipboard between sessions).
    #If we can't write or read from a file, just keep _local_clipboard_string as a local variable in this process as a last resort.
    try:
        return text_file_to_string(_local_clipboard_string_path)
    except OSError:
        return _local_clipboard_string
def _set_local_clipboard_string(string):
    global _local_clipboard_string
    _local_clipboard_string=string
    string_to_text_file(_local_clipboard_string_path,string)
def string_to_clipboard(string):
    #Copies a string to the clipboard so you can paste it later
    #First tries to copy the string to the system clipboard.
    #If that doesn't work, it falls back to writing your string to a local file called '.rp_local_clipboard', and uses that to copy/paste along with the string_from_clipboard function. This is useful over SSH where pyperclip fails on linux systems. Because it uses a file, it's synced across rp processes and is persistent even after we close and reopen rp, even while over ssh on a system whose clipboard we can't modify for some reason.
    #If that doesn't work, it falls back to reading/writing to a global variable called _local_clipboard_string. This string is lost if rp is closed.
    #I decided not to label this function 'copy' because 'copy' could refer to copying objects such as lists etc, like [1,2,3].copy()
    global _local_clipboard_string
    _set_local_clipboard_string(string)
    try:
        try:
            from rp.Pyperclip import paste,copy
            copy(string)
        except:
            os.system("echo '%_s' | pbcopy" % string)
    except:
        return
        fansi_print("string_to_clipboard: error: failed to copy a string to the clipboard",'red')

def string_from_clipboard():
    #Pastes the string from the clipboard and returns that value
    #First tries to paste the string from the system clipboard.
    #If that doesn't work, it falls back to reading your string from a local file called '.rp_local_clipboard'
    #If that doesn't work, it falls back to writing to a global variable called _local_clipboard_string
    try:
        from rp.Pyperclip import paste,copy
        return paste()
    except:
        return _get_local_clipboard_string()
        fansi_print("string_from_clipboard: error: failed to get a string from clipboard",'red')
# endregion
# region pseudo_terminal
# EXAMPLE CODE TO USE pseudo_terminal:
# The next 3 lines are used to import pseudo_terminal
# region pseudo_terminal definition
# #from r import make_pseudo_terminal
# def pseudo_terminal():pass # Easiest way to let PyCharm know that this is a valid def. The next line redefines it.
# exec(make_pseudo_terminal)
# endregion
# NOTE: In my PyCharm Live Templates, I made a shortcut to create the above three lines.
# make pseudo terminal     ⟵ The template keyword.


#   print("Result = "+str(pseudo_terminal()))
# endregion
# region 2d Methods:［width，height，rgb_to_grayscale，gauss_blur，flat_circle_kernel，med_filter，med_filter，med_filter，grid2d，grid2d_map，resize_image］
# noinspection PyShadowingNames
def width(image) -> int:
    return len(image)
def height(image) -> int:
    return len(image[0])
def rgb_to_grayscale(image):  # A demonstrative implementation of this pair
    # Takes an image with multiple color channels
    # Takes a 3d tensor as an input (X,Y,RGB)
    # Outputs a matrix (X,Y ⋀ Grayscale value)
    # Calculated by taking the average of the three channels.
    try:
        return np.average(image,2).astype(image.dtype)  # Very fast if possible
    except:
        # The old way, when I used nested lists to represent images
        # (Only doing this if the numpy way fails so my older scripts don't break)
        # 'z' denotes the grayscale channel.
        # z ﹦﹙r﹢g﹢b﹚÷３
        x,y,r,g,b=image_to_xyrgb_lists(image)
        # z=[*map(lambda a,b,c:(a+b+c)/3.,r,g,b)] ⟵ Got overflow errors!
        z=list(range(assert_equality(len(x),len(y),len(r),len(g),len(b))))
        for i in z:
            z[i]=(float(r[i]) / 256 + float(g[i]) / 256 + float(b[i]) / 256) / 3
        return xyrgb_lists_to_image(x,y,z.copy(),z.copy(),z.copy())
def grayscale_to_rgb(matrix,number_of_channels=3):
    return np.stack((matrix,) * number_of_channels,-1)
def gauss_blur(image,σ,single_channel: bool = False,mode: str = 'reflect',shutup: bool = False):
    # NOTE: order refers to the derivative of the gauss curve; for edge detection etc.
    if σ == 0:
        return image
    mode=mode.lower()
    assert mode in {'constant','nearest','reflect','mirror','wrap'},"r.med_filter: Invalid mode for blurring edge-areas of image. mode=" + str(mode)
    # single_channel: IMPORTANT: This determines the difference between
    #       [1,2,3,4,5]
    #  and
    #       [[1],[2],[3],[4],[5]] (when False)
    # Works in RGB, RGBA, or any other number of color channels!
    from scipy.ndimage.filters import gaussian_filter
    gb=lambda x:gaussian_filter(x,sigma=σ,mode=mode)
    tp=np.transpose
    # noinspection PyTypeChecker
    sh=np.shape(image)
    assert isinstance(sh,tuple)
    if not single_channel and not sh[-1] <= 4 and not shutup:  # Generally if you have more than 4 channels you are using a single_channel image.
        fansi_print("r.gauss_blur: Warning: Last channel has length of " + str(sh[-1]) + "; you results might be weird. Consider setting optional parameter 'single_channel' to True?",'red')
    s=list(range(len(sh)))
    if len(s) == 1 or single_channel:  # We don't have channels of colors, we only have 1 color channel (AKA we extracted the red of an image etc)
        return gb(image)

    #        ⎛                                                                      ⎞
    #        ⎜⎛                                               ⎞                     ⎟
    #        ⎜⎜                 ⎛                            ⎞⎟                     ⎟
    #        ⎜⎜                 ⎜      ⎛     ⎞       ⎛      ⎞⎟⎟     ⎛     ⎞   ⎛    ⎞⎟
    return tp([gb(x) for x in tp(image,[s[-1]] + list(s[:-1]))],list(s[1:]) + [s[0]])  # Blur each channel individually.
    #        ⎜⎜                 ⎜      ⎝     ⎠       ⎝      ⎠⎟⎟     ⎝     ⎠   ⎝    ⎠⎟
    #        ⎜⎜                 ⎝                            ⎠⎟                     ⎟
    #        ⎜⎝                                               ⎠                     ⎟
    #        ⎝                                                                      ⎠

    # NOTE:
    #     ⮤ _s=(0,1,2)
    #     ⮤ [_s[-1]] + list(_s[:-1])
    # ans=[2,0,1]
    #     ⮤ list(_s[1:]) + [_s[0]]
    # ans=[1,2,0]

    # region Works with RGB but fails on single channels
    # cv2=pip_import('cv2')
    # # noinspection PyUnresolvedReferences
    # return cv2.GaussianBlur(image,(radius,radius),0)
    # endregion
    # def med_filter(image,σ):
    #     # Works in RGB, RGBA, or any other number of color channels!
    #     from scipy.ndimage.filters import gaussian_filter as gb
    #     tp=np.transpose
    #     return tp([gb(x,σ) for x in tp(image,[2,0,1])],[1,2,0])# Blur each channel individually.
    #     # region Works with RGB but fails on single channels
    #     # cv2=pip_import('cv2')
    #     # # noinspection PyUnresolvedReferences
    #     # return cv2.GaussianBlur(image,(radius,radius),0)
    #     # endregion
_flat_circle_kernel_cache={}
def flat_circle_kernel(diameter):
    if diameter not in _flat_circle_kernel_cache:
        d=int(diameter)
        v=np.linspace(-1,1,d) ** 2
        m=np.zeros([d,d])
        m+=v
        m=np.transpose(m)
        m+=v
        m=m<=1
        _flat_circle_kernel_cache[diameter]=m
    return _flat_circle_kernel_cache[diameter]

_gaussian_circle_kernel_cache={}
def gaussian_kernel(size=21, sigma=3,dim=2):
    """Returns a normalized 2D Gaussian kernel.
    Please note that increasing 'size' does NOT increase 'sigma': you must manually increase sigma proportionally if you want a bigger blur!
    Parameters
    ----------
    size : float, the kernel size (will be square)

    sigma : float, the sigma Gaussian parameter

    Returns
    -------
    out : array, shape = (size, size)
      an array with the centered gaussian kernel
    """
    args=size,sigma,dim
    if args not in _gaussian_circle_kernel_cache:
        x = np.linspace(- (size // 2), size // 2,num=size)
        x /= np.sqrt(2)*sigma
        x2 = x**2
        assert dim==2 or dim==1,'Only 1d and 2d gaussians are supported right now'
        kernel = np.exp(- x2[:, None] - x2[None, :]) if dim==2 else np.exp(-x2)
        _gaussian_circle_kernel_cache[args]=kernel / kernel.sum()
    return _gaussian_circle_kernel_cache[args]

def max_filter(image,diameter,single_channel: bool = False,mode: str = 'reflect',shutup: bool = False):
    # NOTE: order refers to the derivative of the gauss curve; for edge detection etc.
    if diameter == 0:
        return image
    mode=mode.lower()
    assert mode in {'constant','nearest','reflect','mirror','wrap'},"r.max_filter: Invalid mode for max-filtering edge-areas of image. mode=" + str(mode)
    # single_channel: IMPORTANT: This determines the difference between
    #       [1,2,3,4,5]
    #  and
    #       [[1],[2],[3],[4],[5]] (when False)
    # Works in RGB, RGBA, or any other number of color channels!
    from scipy.ndimage.filters import maximum_filter as filter
    kernel=flat_circle_kernel(diameter)
    f=lambda x:filter(x,footprint=kernel,mode=mode)
    tp=np.transpose
    sh=np.shape(image)
    assert isinstance(sh,tuple)
    if not single_channel and not sh[-1] <= 4 and not shutup:  # Generally if you have more than 4 channels you are using a single_channel image.
        fansi_print("r.med_filter: Warning: Last channel has length of " + str(sh[-1]) + "; you results might be weird. Consider setting optional parameter 'single_channel' to True?",'red')
    s=list(range(len(sh)))
    if len(s) == 1 or single_channel:  # We don't have channels of colors, we only have 1 color channel (AKA we extracted the red of an image etc)
        return f(image)

    #        ⎛                                                                     ⎞
    #        ⎜⎛                                              ⎞                     ⎟
    #        ⎜⎜                ⎛                            ⎞⎟                     ⎟
    #        ⎜⎜                ⎜      ⎛     ⎞       ⎛      ⎞⎟⎟     ⎛     ⎞   ⎛    ⎞⎟
    return tp([f(x) for x in tp(image,[s[-1]] + list(s[:-1]))],list(s[1:]) + [s[0]])  # Blur each channel individually.
    #        ⎜⎜                ⎜      ⎝     ⎠       ⎝      ⎠⎟⎟     ⎝     ⎠   ⎝    ⎠⎟
    #        ⎜⎜                ⎝                            ⎠⎟                     ⎟
    #        ⎜⎝                                              ⎠                     ⎟
    #        ⎝                                                                     ⎠

    # NOTE:
    #     ⮤ _s=(0,1,2)
    #     ⮤ [_s[-1]] + list(_s[:-1])
    # ans=[2,0,1]
    #     ⮤ list(_s[1:]) + [_s[0]]
    # ans=[1,2,0]
def min_filter(image,diameter,single_channel: bool = False,mode: str = 'reflect',shutup: bool = False):
    # NOTE: order refers to the derivative of the gauss curve; for edge detection etc.
    if diameter == 0:
        return image
    mode=mode.lower()
    assert mode in {'constant','nearest','reflect','mir3ror','wrap'},"r.min_filter: Invalid mode for min-filtering edge-areas of image. mode=" + str(mode)
    # single_channel: IMPORTANT: This determines the difference between
    #       [1,2,3,4,5]
    #  and
    #       [[1],[2],[3],[4],[5]] (when False)
    # Works in RGB, RGBA, or any other number of color channels!
    from scipy.ndimage.filters import minimum_filter as filter
    kernel=flat_circle_kernel(diameter)
    f=lambda x:filter(x,footprint=kernel,mode=mode)
    tp=np.transpose
    sh=np.shape(image)
    assert isinstance(sh,tuple)
    if not single_channel and not sh[-1] <= 4 and not shutup:  # Generally if you have more than 4 channels you are using a single_channel image.
        fansi_print("r.med_filter: Warning: Last channel has length of " + str(sh[-1]) + "; you results might be weird. Consider setting optional parameter 'single_channel' to True?",'red')
    s=list(range(len(sh)))
    if len(s) == 1 or single_channel:  # We don't have channels of colors, we only have 1 color channel (AKA we extracted the red of an image etc)
        return f(image)

    #        ⎛                                                                     ⎞
    #        ⎜⎛                                              ⎞                     ⎟
    #        ⎜⎜                ⎛                            ⎞⎟                     ⎟
    #        ⎜⎜                ⎜      ⎛     ⎞       ⎛      ⎞⎟⎟     ⎛     ⎞   ⎛    ⎞⎟
    return tp([f(x) for x in tp(image,[s[-1]] + list(s[:-1]))],list(s[1:]) + [s[0]])  # Blur each channel individually.
    #        ⎜⎜                ⎜      ⎝     ⎠       ⎝      ⎠⎟⎟     ⎝     ⎠   ⎝    ⎠⎟
    #        ⎜⎜                ⎝                            ⎠⎟                     ⎟
    #        ⎜⎝                                              ⎠                     ⎟
    #        ⎝                                                                     ⎠

    # NOTE:
    #     ⮤ _s=(0,1,2)
    #     ⮤ [_s[-1]] + list(_s[:-1])
    # ans=[2,0,1]
    #     ⮤ list(_s[1:]) + [_s[0]]
    # ans=[1,2,0]
def med_filter(image,diameter,single_channel: bool = False,mode: str = 'reflect',shutup: bool = False):
    # NOTE: order refers to the derivative of the gauss curve; for edge detection etc.
    if diameter == 0:
        return image
    mode=mode.lower()
    assert mode in {'constant','nearest','reflect','mirror','wrap'},"r.med_filter: Invalid mode for med-filtering edge-areas of image. mode=" + str(mode)
    # single_channel: IMPORTANT: This determines the difference between
    #       [1,2,3,4,5]
    #  and
    #       [[1],[2],[3],[4],[5]] (when False)
    # Works in RGB, RGBA, or any other number of color channels!
    from scipy.ndimage.filters import median_filter as filter
    kernel=flat_circle_kernel(diameter)
    f=lambda x:filter(x,footprint=kernel,mode=mode)
    tp=np.transpose
    sh=np.shape(image)
    assert isinstance(sh,tuple)
    if not single_channel and not sh[-1] <= 4 and not shutup:  # Generally if you have more than 4 channels you are using a single_channel image.
        fansi_print("r.med_filter: Warning: Last channel has length of " + str(sh[-1]) + "; you results might be weird. Consider setting optional parameter 'single_channel' to True?",'red')
    s=list(range(len(sh)))
    if len(s) == 1 or single_channel:  # We don't have channels of colors, we only have 1 color channel (AKA we extracted the red of an image etc)
        return f(image)

    #        ⎛                                                                     ⎞
    #        ⎜⎛                                              ⎞                     ⎟
    #        ⎜⎜                ⎛                            ⎞⎟                     ⎟
    #        ⎜⎜                ⎜      ⎛     ⎞       ⎛      ⎞⎟⎟     ⎛     ⎞   ⎛    ⎞⎟
    return tp([f(x) for x in tp(image,[s[-1]] + list(s[:-1]))],list(s[1:]) + [s[0]])  # Blur each channel individually.
    #        ⎜⎜                ⎜      ⎝     ⎠       ⎝      ⎠⎟⎟     ⎝     ⎠   ⎝    ⎠⎟
    #        ⎜⎜                ⎝                            ⎠⎟                     ⎟
    #        ⎜⎝                                              ⎠                     ⎟
    #        ⎝                                                                     ⎠

    # NOTE:
    #     ⮤ _s=(0,1,2)
    #     ⮤ [_s[-1]] + list(_s[:-1])
    # ans=[2,0,1]
    #     ⮤ list(_s[1:]) + [_s[0]]
    # ans=[1,2,0]
def range_filter(image,diameter,single_channel: bool = False,mode: str = 'reflect',shutup: bool = False):
    args=image,diameter,single_channel,mode,shutup
    return max_filter(*args) - min_filter(*args)
def grid2d(width: int,height: int,fᆢrowˏcolumn=lambda r,c:None) -> list:
    from copy import deepcopy
    # Perhaps I'll make a future version that extends this to n-dimensions, like rmif in MatLab
    out=deepcopy_multiply([[[None]] * height],width)
    for column in range(height):
        for row in range(width):
            out[row][column]=fᆢrowˏcolumn(row,column)
    return out
def grid2d_map(grid2d_input,value_func=identity) -> list:
    # Similar to rmvf (ryan matrix value function), except restricted to just 2d grids.
# ⁠⁠⁠⁠               ⎧                                                                                  ⎫
# ⁠⁠⁠⁠               ⎪                                                              ⎧                  ⎫⎪
# ⁠⁠⁠⁠               ⎪     ⎧            ⎫       ⎧            ⎫                      ⎪            ⎧ ⎫⎧ ⎫⎪⎪
    return grid2d(width(grid2d_input),height(grid2d_input),lambda x,y:value_func(grid2d_input[x][y]))
# ⁠⁠⁠               ⎪     ⎩            ⎭       ⎩            ⎭                      ⎪            ⎩ ⎭⎩ ⎭⎪⎪
# ⁠⁠⁠               ⎪                                                              ⎩                  ⎭⎪
# ⁠⁠⁠               ⎩                                                                                  ⎭
def resize_image(image,scale,interp='bilinear'):
    """
    resize_image resizes images. Who woulda thunk it? Stretchy-squishy image resizing!
    This method could use some more love...it's kinda wonky atm (because scipy.misc no longer contains imresize, it's starting to fall back onto the other methods that dont support interp etc...)
    :param image: a numpy array, preferably. But it can also handle pure-python list-of-lists if that fails.
    :param scale: can either be a scalar (get it? for SCALE? lol ok yeah that died quickly) or a tuple of integers to specify the new dimensions we want like (128,128)
    :param interp: ONLY APPLIES FOR numpy arrays! interp ∈ {'nearest','bilinear','bicubic','cubic'}
    :return: returns the resized image
    """
    assert interp in {'nearest','bilinear','bicubic','cubic'}
    if scale == 1:
        return image
    try:
        from scipy.misc import imresize
        return imresize(image,float(scale),interp)#We multiply scale by 100 because it's measured in percent
    except:pass
    try:
        assert is_image(image)
        pip_import("skimage")
        from skimage.transform import resize
        height,width=image.shape[:2]
        height=int(height*scale)
        width =int(width *scale)
        return resize(image,(height,width))
    except:pass
    if is_number(scale):
        try:
            return cv_apply_affine_to_image(dog,scale_affine_2d(scale),output_resolution=scale)#Doesn't support 'interp'
        except:pass
    return grid2d(int(len(image) * scale),int(len(image[0]) * scale),lambda x,y:image[int(x / scale)][int(y / scale)])#The slowest method of all...doesn't support 'interp'
# endregion
# region  xyrgb lists ⟷ image:［image_to_xyrgb_lists，xyrgb_lists_to_image，xyrgb_normalize，image_to_all_normalized_xy_rgb_training_pairs，extract_patches］     (Invertible Pair)

# try:from sklearn.feature_extraction.image import extract_patches
# except:pass
def image_to_xyrgb_lists(image):
    # expects an array like, for example 'image=[[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]]'
    out_x=[]
    out_y=[]
    out_r=[]
    out_g=[]
    out_b=[]
    for x_index,x_val in enumerate(image):
        for y_index,y_val in enumerate(x_val):
            out_x.append(x_index)
            out_y.append(y_index)
            out_r.append(y_val[0])
            out_g.append(y_val[1])
            out_b.append(y_val[2])
    return out_x,out_y,out_r,out_g,out_b
def xyrgb_lists_to_image(*xyrgb_lists_as_tuple):
    xyrgb_lists_as_tuple=detuple(xyrgb_lists_as_tuple)  # So we can either accept 5 arguments or one tuple argument with 5 elements.
    assert len(xyrgb_lists_as_tuple) == 5,"One element:list for each channel: X Y R G B"
    x,y,r,g,b=xyrgb_lists_as_tuple
    assert len(x) == len(y) == len(r) == len(g) == len(b),"An outside-noise assumption. If this assertion fails then there is something wrong with the input parameters ⟹ this def is not to blame."
    xyrgb_length=len(x)  # =len(y)=len(r)=len(g)=len(b) etc. We rename it 'xyrgb_length' to emphasize this symmetry.
    out_image=deepcopy_multiply([[None] * (max(y) + 1)],(max(x) + 1))  # Pre-allocating the pixels. [R,G,B] is inserted into each pixel later.
    for index in range(xyrgb_length):
        out_image[x[index]][y[index]]=[r[index],g[index],b[index]]
    return out_image
def xyrgb_normalize(*xyrgb,rgb_old_max=255,rgb_new_max=1,x_new_max=1,y_new_max=1):
    # Converts the (X and Y values, originally ﹙integers: the pixel X and Y indexes﹚) into float values between 0 and 1
    # Also converts the R,G, and B values from the range ［0‚255］⋂ ℤ into the range ［0‚1］⋂ ℝ
    x,y,r,g,b=detuple(xyrgb)
    x_factor=x_new_max / max(x)
    y_factor=y_new_max / max(y)
    x=list(ⵁ * x_factor for ⵁ in x)
    y=list(ⵁ * y_factor for ⵁ in y)

    rgb_factor=rgb_new_max / rgb_old_max
    r=list(ⵁ * rgb_factor for ⵁ in r)
    g=list(ⵁ * rgb_factor for ⵁ in g)
    b=list(ⵁ * rgb_factor for ⵁ in b)

    return x,y,r,g,b
def image_to_all_normalized_xy_rgb_training_pairs(image):
    x,y,r,g,b=xyrgb_normalize(image_to_xyrgb_lists(image))
    return list(zip(x,y)),list(zip(r,g,b))

    # NOTE: This def exists for efficiency purposes.
    # To create a training batch from the image, the minimal syntax would be:
    #     random_parallel_batch(*image_to_all_normalized_xy_rgb_training_pairs(image),a,b)
    # BUT NOTE: It is very inneficient to recalculate this def over and over again.
    # Store the output of this as a vairable, and use like so:
    # precalculated=image_to_all_normalized_xy_rgb_training_pairs(image)
    # new_batch=random_parallel_batch(*precalculated,a,b)


    # region Explanatory Example:
    # # Goal: create input and output from XY to RGB from image and turn them into a random batch for NN input outputs
    # #from r import *
    # x=['x₁','x₂','x₃']
    # y=['y₁','y₂','y₃']
    # r=['r₁','r₂','r₃']
    # g=['g₁','g₂','g₃']
    # b=['b₁','b₂','b₃']
    #
    # inputs=list(zip(x,y))
    # outputs=list(zip(r,g,b))
    # io_pairs=list(zip(inputs,outputs))
    #
    #  ⁠⁠⁠⁠    ⎧                                    ⎫
    #  ⁠⁠⁠⁠    ⎪    ⎧                              ⎫⎪
    # ⁠⁠⁠⁠     ⎪    ⎪   ⎧                         ⎫⎪⎪
    # print(list(zip(*random_batch(io_pairs,2))))
    #  ⁠⁠⁠⁠    ⎪    ⎪   ⎩                         ⎭⎪⎪
    #  ⁠⁠⁠⁠    ⎪    ⎩                              ⎭⎪
    #  ⁠⁠⁠⁠    ⎩                                    ⎭
    #
    #  ⁠⁠⁠⁠ ⎧                                                                      ⎫
    #  ⁠⁠⁠⁠ ⎪⎧                          ⎫  ⎧                                      ⎫⎪
    # # [(('x₂', 'y₂'), ('x₃', 'y₃')), (('r₂', 'g₂', 'b₂'), ('r₃', 'g₃', 'b₃'))]
    #  ⁠⁠⁠⁠ ⎪⎩                          ⎭  ⎩                                      ⎭⎪
    #  ⁠⁠⁠⁠ ⎩                                                                      ⎭
    # endregion
# endregion
# region Randomness:［random_index，random_element，random_permutation，randint，random_float，random_chance，random_batch，shuffled，random_parallel_batch］
import random
def random_index(array_length_or_array_itself):
    # Basically a random integer generator suited for generating array indices.
    # Returns a random integer ∈ ℤ ⋂ [0‚array_length)
    if isinstance(array_length_or_array_itself,int):
        assert array_length_or_array_itself != 0
        return randint(0,array_length_or_array_itself - 1)
    else:
        return random_index(len(array_length_or_array_itself))
def random_element(x):
    assert is_iterable(x)
    return x[random_index(len(x))]
def random_choice(*choices):
    return random_element(choices)
def random_permutation(n) -> list or str:
    # Either n is an integer (as a length) OR n is an iterable
    if is_iterable(n):  # random_permutation([1,2,3,4,5]) ⟶ [3, 2, 4, 5, 1]
        return shuffled(n)
    return list(np.random.permutation(n))  # random_permutation(5) ⟶ [3, 2, 1, 4, 0]
def randint(a_inclusive,b_inclusive=0):
    # If both a and b are specified, the range is inclusive, choose from range［a，b] ⋂ ℤ
    # Otherwise, if only a is specified, choose random element from the range ［a，b) ⋂ ℤ
    from random import randint
    return randint(min([a_inclusive,b_inclusive]),max([a_inclusive,b_inclusive]))
random_int=randint
def randints(N,a_inclusive=99,b_inclusive=0):
    # Generate N random integers
    # Example: randints(10)   ====   [9, 36, 82, 49, 13, 9, 62, 81, 80, 66]
    # This function exists for convenience when using pseudo_terminal (wasn't really meant for use in long-term code, though it totally could be)
    assert N>=0 and N==int(N),'Cannot have a non-counting-number length: N='+repr(N)
    out=[randint(a_inclusive,b_inclusive) for _ in range(N)]
    try:out=np.asarray(out)#Do this IFF we have numpy for convenience's sake
    except:pass
    return out
random_ints=randints
def randint_complex(*args,**kwargs):
    #Arguments passed to this function are passed to 'randint'
    #The only difference between this function and randints is that this also generates a complex component
    #EXAMPLE:
    #  >>> randints_complex(100)
    # ans = 56.+64.j
    #  >>> randint_complex(1)
    # ans = (1+1j)
    #  >>> randint_complex(1)
    # ans = 0j
    #  >>> randint_complex(1)
    # ans = (1+0j)
    #  >>> randint_complex(1)
    # ans = 0j
    return randint(*args,**kwargs)+randint(*args,**kwargs)*1j
random_int_complex=randint_complex
def randints_complex(*args,**kwargs):
    #Arguments passed to this function are passed to 'randints'
    #The only difference between this function and randints is that this also generates a complex component
    #EXAMPLE:
    # ⮤ randints_complex(10)
    # ans = [56.+64.j 61. +9.j 58.+42.j 93.+71.j 67.+57.j 67.+67.j 24. +3.j 14.+98.j 92.+96.j 32.+29.j]
    return randints(*args,**kwargs)+randints(*args,**kwargs)*1j
random_ints_complex=randints_complex
def random_float(exclusive_max: float = 1,inclusive_min=0) -> float:
    inclusive_min,exclusive_max=sorted([inclusive_min,exclusive_max])
    return (random.random())*(exclusive_max-inclusive_min)+inclusive_min
def random_floats(N,exclusive_max=1,inclusive_min=0):
    # Generate N uniformly distributed random floats
    # Example: random_floats(10)   ====   [0.547 0.516 0.421 0.698 0.732 0.885 0.947 0.668 0.857 0.237]
    # This function exists for convenience when using pseudo_terminal (wasn't really meant for use in long-term code, though it totally could be)
    assert N>=0 and N==int(N),'Cannot have a non-counting-number length: N='+repr(N)
    inclusive_min,exclusive_max=sorted([inclusive_min,exclusive_max])
    try:return (np.random.rand(N))*(exclusive_max-inclusive_min)+inclusive_min#Do this IFF we have numpy for convenience's sake
    except:pass
    return [random_float(a_inclusive,b_inclusive) for _ in range(N)]
def random_floats_complex(*args,**kwargs):
    #Arguments passed to this function are passed to 'random_floats'
    #The only difference between this function and randints is that this also generates a complex component
    #EXAMPLE:
    # >>> random_floats_complex(10)
    #ans = [0.611+0.569j 0.371+0.036j 0.469+0.336j 0.615+0.069j 0.329+0.16j  0.896+0.22j  0.22 +0.668j 0.901+0.741j 0.827+0.937j 0.619+0.513j]
    # >>> random_floats_complex(10,-1)
    #ans = [-0.504-0.998j -0.668-0.345j -0.104-0.952j -0.532-0.019j -0.949-0.488j -0.02 -0.82j  -0.805-0.194j -0.021-0.287j -0.708-0.231j -0.152-0.159j]
    # >>> random_floats_complex(10,-1,0)
    #ans = [-0.433-0.792j -0.71 -0.633j -0.395-0.383j -0.782-0.336j -0.176-0.176j -0.78 -0.16j  -0.505-0.978j -0.199-0.963j -0.98 -0.456j -0.231-0.775j]
    # >>> random_floats_complex(10,-1,1)
    #ans = [-0.139-0.101j  0.84 -0.259j  0.347+0.632j -0.362+0.036j  0.002-0.942j -0.685+0.176j  0.852-0.988j  0.188-0.134j  0.011-0.434j -0.578-0.883j]
    # >>> random_floats_complex(10,0,100)
    #ans = [40.909+10.029j 51.376+61.357j 15.713+25.714j 99.301+76.956j  5.253+21.822j  8.723+75.36j  15.964+85.891j 20.968+12.191j 37.997+92.09j  87.132+89.107j]

    return random_floats(*args,**kwargs)+random_floats(*args,**kwargs)*1j

def random_chance(probability: float = .5) -> bool:
    return random_float() < probability
def random_batch(full_list,batch_size: int = None,retain_order: bool = False):
    # Input conditions, assertions and rCode algebra:
    # rCode: Let ⨀ ≣ random_batch ∴
    #       ⨀ a None b ≣ ⨀ a len a b
    #       list a ≣ ⨀ a None True
    #       b ≣ len ⨀ a b
    if batch_size is None:  # The default if not specified
        # If we don't specify the batch size, assume that we simply want a shuffled version of the full_list
        if retain_order:
            return full_list  # A result of the rCode algebra. This simply speeds up the process.
        batch_size=len(full_list)
    else:
        assert 0 <= batch_size <= len(full_list),"batch_size == " + str(batch_size) + " ⋀ len(full_list) == " + str(len(full_list)) + "，∴  ¬ (0 <= batch_size <= len﹙full_list﹚)   Explanation: We do not allow duplicates, ∴ we cannot generate a larger batch than we have elements to choose from full_list"

    ⵁ=list(range(len(full_list)))  # All possible indices of full_list
    random.shuffle(ⵁ)  # This shuffles the ⵁ array but doesn't return anything
    ⵁ=ⵁ[0:batch_size]
    if retain_order:
        ⵁ.sort()
    return list(full_list[i] for i in ⵁ)
def shuffled(l):
    # Shuffle a list
    if isinstance(l,str):  # random_permutation("ABCDE") ⟶ 'EDBCA' special case: if its a string we want a string output, so we can jumble letters in words etc.
        return ''.join(shuffled(list(l)))
    return random_batch(l)  # Due to an r-code identity in random_batch
def random_parallel_batch(*full_lists,batch_size: int = None,retain_order: bool = False):
    # Created for machine learning input/output training-pairs generation.
    # rCode:
    # ⁠⁠⁠⁠       ⎧                                     ⎫
    # ⁠⁠⁠⁠       ⎪   ⎧                                ⎫⎪
    # ⁠⁠⁠⁠       ⎪   ⎪             ⎧                 ⎫⎪⎪
    # ⁠⁠⁠⁠       ⎪   ⎪             ⎪    ⎧       ⎫    ⎪⎪⎪
    #    list(zip(*random_batch(list(zip(*a)),b,c))) ≣ random_parallel_batch(*a,b,c)
    # ⁠⁠⁠⁠       ⎪   ⎪             ⎪    ⎩       ⎭    ⎪⎪⎪
    # ⁠⁠⁠⁠       ⎪   ⎪             ⎩                 ⎭⎪⎪
    # ⁠⁠⁠⁠       ⎪   ⎩                                ⎭⎪
    # ⁠⁠⁠⁠       ⎩                                     ⎭
    # print(parallel_batch(['a','b','c','d'],[1,2,3,4],batch_size=3)) ⟹ [['c', 'b', 'd'], [3, 2, 4]]
    # assert_equality(*full_lists,equality_check=lambda a,b:len(a)==len(b))# All lists ∈ full_lists must have the same length
    # ⁠⁠⁠⁠                        ⎧                                                                               ⎫
    # ⁠⁠⁠⁠                        ⎪    ⎧                         ⎫                                                ⎪
    # ⁠⁠⁠⁠                        ⎪    ⎪     ⎧                  ⎫⎪                                                ⎪
    # ⁠⁠⁠⁠                        ⎪    ⎪     ⎪   ⎧             ⎫⎪⎪                                                ⎪
    batch_indexes=random_batch(list(range(len(full_lists[0]))),batch_size=batch_size,retain_order=retain_order)  # Select random possible indices that will be synchronized across all lists of the output
    # ⁠⁠⁠⁠                        ⎪    ⎪     ⎪   ⎩             ⎭⎪⎪                                                ⎪
    # ⁠⁠⁠⁠                        ⎪    ⎪     ⎩                  ⎭⎪                                                ⎪
    # ⁠⁠⁠⁠                        ⎪    ⎩                         ⎭                                                ⎪
    # ⁠⁠⁠⁠                        ⎩                                                                               ⎭
    # ⁠⁠⁠⁠         ⎧                                                                ⎫
    # ⁠⁠⁠⁠         ⎪   ⎧                                                           ⎫⎪
    # ⁠⁠⁠⁠         ⎪   ⎪              ⎧                                ⎫           ⎪⎪
    # ⁠⁠⁠⁠         ⎪   ⎪              ⎪   ⎧                           ⎫⎪           ⎪⎪
    return list(map(lambda x:tuple(map(lambda i:x[i],batch_indexes)),full_lists))  # Note that batch_indexes is referenced inside a lambda statement that is called multiple times. This is why it is declared as a separate variable above.
    # ⁠⁠⁠⁠         ⎪   ⎪              ⎪   ⎩                           ⎭⎪           ⎪⎪
    # ⁠⁠⁠⁠         ⎪   ⎪              ⎩                                ⎭           ⎪⎪
    # ⁠⁠⁠⁠         ⎪   ⎩                                                           ⎭⎪
    # ⁠⁠⁠⁠         ⎩                                                                ⎭
    # The single-lined return statement shown directly above this line is ≣ to the next 5 lines of code:
    # out=deepcopy_multiply([[]],len(full_lists))
    # for i in batch_indexes:
    #     for j in range(len(out)):
    #         out[j].append(full_lists[j][i])
    # return out
# endregion
# region rant/ranp: ［run_as_new_thread，run_as_new_process］
def run_as_new_thread(funcᆢvoid,*args,**kwargs):  # ⟵ THIS IS DUBIOUS. I DON'T KNOW IF IT DOES WHAT ITS SUPPOSED TO....
    # Used when we simply don't need/want all the complexities of the threading module.
    # An anonymous thread that only ceases once the def is finished.
    new_thread=threading.Thread
    new_thread=new_thread(target=funcᆢvoid,args=args,kwargs=kwargs)
    new_thread.start()
    return new_thread
def run_as_new_process(funcᆢvoid,*args,**kwargs):
    # Used when we simply don't need/want all the complexities of the threading module.
    # An anonymous thread that only ceases once the def is finished.
    import multiprocessing as mp
    new_process=mp.Process(target=funcᆢvoid,args=args,kwargs=kwargs)
    new_process.start()  # can't tell the difference between start and run
    return new_process
# endregion
def is_valid_url(url):
    from urllib.parse import urlparse
    if not isinstance(url,str):
        return False
    try:
        result=urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
# region  Saving/Loading Images: ［load_image，load_image_from_url，save_image，save_image_jpg］

_load_image_cache={}#TODO Test this and make sure it works. This is currently untested.
def load_image(location,*,from_cache=False):
    #Automatically detect if location is a URL or a file path and try to smartly choose the appropriate function to load the image
    assert isinstance(location,str),'load_image error: location should be a string representing a URL or file path. However, location is not a string. type(location)=='+repr(type(location))+' and location=='+repr(location)
    if from_cache and location in _load_image_cache and from_cache:
        return _load_image_cache[location].copy()
    if is_valid_url(location):
        out = load_image_from_url (location)
    else:
        out = load_image_from_file(location)
    _load_image_cache[location]=out
    return out

def load_images(*locations,from_cache=False,display_progress=False):
    #Simply the plural form of load_image
    locations=delist(detuple(locations))
    output=[]
    show_time_remaining=eta(len(locations))
    for i,location in enumerate(locations):
        image=load_image(location,from_cache=from_cache)
        output.append(image)
        if display_progress:
            show_time_remaining(i)

    return [load_image(location,from_cache=from_cache) for location in locations]

def load_image_from_file(file_name):
    #Can try opencv as a fallback if this ever breaks
    try               :return _load_image_from_file_via_scipy (file_name)
    except ImportError:return _load_image_from_file_via_opencv(file_name)#Expecting that scipy.misc.imread doesn't exist on the interpereter for whatever reason

def _load_image_from_file_via_scipy(file_name):
    from scipy.misc import imread
    return imread(file_name)

def _load_image_from_file_via_opencv(file_name):
    cv2=pip_import('cv2')
    image=cv2.imread(file_name)
    if image is None:
        raise FileNotFoundError("Cannot find an image file at the file path: "+file_name)#By default, opencv doesn't raise an error when the file isn't found, and just returns None....which is dumb. It should act like scipy.misc.imread, which throws a FileNotFoundError when given an invalid path.
    return cv_bgr_rgb_swap(image)#OpenCV is really weird and doesn't use RGB: It uses BGR for some strange legacy reason. We have to swap the channels to make it useful.



def load_image_from_url(url: str):
    assert is_valid_url(url),'load_image_from_url error: invalid url: '+repr(url)
    pip_import('PIL')
    from PIL import Image
    requests=pip_import('requests')
    from io import BytesIO
    response=requests.get(url)
    return np.add(Image.open(BytesIO(response.content)),0)  # Converts it to a numpy array by adding 0 to it.

def save_image(image,file_name=None,add_png_extension: bool = True):
    #Simply save a numpy image to a file.
    #The add_png_extension is annoying legacy stuff...sorry...it would break some of my other scripts to change that right now.
    #Provide several fallbacks to saving an image file
    try:
        from scipy.misc import imsave
    except:
        try:
            from skimage.io import imsave
        except:
            try:
                pip_import('cv2')
                from cv2 import imwrite
                imsave=lambda filename,data: imwrite(filename,cv_bgr_rgb_swap(as_rgba_image(as_byte_image(data))))
            except:
                pass
    if file_name is None:
        file_name=str(millis()) + ".png"  # ⟵ Default image name
    if add_png_extension and not has_file_extension(file_name):#Save a png file by default
        file_name+=".png"
    imsave(file_name,image)

def temp_saved_image(image):
    #Return the path of an image, and return the path we saved it to
    #Originally used for google colab to display images nicely:
    #   from IPython.display import Image
    #   Image(temp_saved_image(‹some numpy image›,retina=True)) #<-- Displays image at FULL resolution, optimized for a retina monitor. 'retina=True' is totally optional, it  just looks really nice on my macbook.
    image_name="rp_temp_saved_image_"+random_namespace_hash(10)
    save_image(as_byte_image(as_rgba_image(as_float_image(image))),image_name)
    return image_name+'.png'

def save_image_jpg(image,path,*,quality=100,add_extension=True):
    #If add_extension is True, will add a '.jpg' or '.jpeg' extension to path IFF it doesn't allready end with such an extension (AKA 'a/b/c.jpg' -> 'a/b/c.jpg' BUT 'a/b/c.png' -> 'a/b/c.png.jpg')
    image=np.asarray(image)
    assert 0<=quality<=100,'Jpg quality is measured in percent'
    if is_image(image):image=as_rgb_image(image)
    from PIL import Image
    if not get_file_extension(path).lower() in {'jpeg','jpg'}:
        path+='.jpg'
    return Image.fromarray(image).save(path, "JPEG", quality=quality, optimize=False, progressive=True)

# endregion
# region Text-To-Speech: ［text_to_speech，text_to_speech_via_apple，text_to_speech_via_google，text_to_speech_voices_comparison，text_to_speech_voices_for_apple，text_to_speech_voices_for_google，text_to_speech_voices_all，text_to_speech_voices_favorites］
# region ［text_to_speech_via_apple］
text_to_speech_voices_for_apple=['Alex','Alice','Alva','Amelie','Anna','Carmit','Damayanti','Daniel','Diego','Ellen','Fiona','Fred','Ioana','Joana','Jorge','Juan','Kanya','Karen','Kyoko','Laura','Lekha','Luca','Luciana','Maged','Mariska','Mei-Jia','Melina','Milena','Moira','Monica','Nora','Paulina','Samantha','Sara','Satu','Sin-ji','Tessa','Thomas','Ting-Ting','Veena','Victoria','Xander','Yelda','Yuna','Yuri','Zosia','Zuzana']  # The old voices (that don't work on sierra. They used to work on el-capitan though): ["Samantha",'Bad News','Bahh','Bells','Boing','Bubbles','Cellos','Deranged','Good News','Hysterical','Pipe Organ','Trinoids','Whisper','Zarvox','Agnes','Kathy','Princess','Vicki','Victoria','Alex','Bruce','Fred','Junior','Ralph','Albert']
# Favorites (in this order): Samantha, Alex, Moira, Tessa, Fiona, Fred
def text_to_speech_via_apple(text: str,voice="Samantha",run_as_thread=True,rate_in_words_per_minute=None,filter_characters=True):
    # region  All text_to_speech_via_apple voices along with their descriptions (type 'say -v ?' into terminal to get this):
    """
    Alex                en_US    # Most people recognize me by my voice.
    Alice               it_IT    # Salve, mi chiamo Alice e sono una voce italiana.
    Alva                sv_SE    # Hej, jag heter Alva. Jag är en svensk röst.
    Amelie              fr_CA    # Bonjour, je m’appelle Amelie. Je suis une voix canadienne.
    Anna                de_DE    # Hallo, ich heiße Anna und ich bin eine deutsche Stimme.
    Carmit              he_IL    # שלום. קוראים לי כרמית, ואני קול בשפה העברית.
    Damayanti           id_ID    # Halo, nama saya Damayanti. Saya berbahasa Indonesia.
    Daniel              en_GB    # Hello, my name is Daniel. I am a British-English voice.
    Diego               es_AR    # Hola, me llamo Diego y soy una voz española.
    Ellen               nl_BE    # Hallo, mijn naam is Ellen. Ik ben een Belgische stem.
    Fiona               en-scotland # Hello, my name is Fiona. I am a Scottish-English voice.
    Fred                en_US    # I sure like being inside this fancy computer
    Ioana               ro_RO    # Bună, mă cheamă Ioana . Sunt o voce românească.
    Joana               pt_PT    # Olá, chamo-me Joana e dou voz ao português falado em Portugal.
    Jorge               es_ES    # Hola, me llamo Jorge y soy una voz española.
    Juan                es_MX    # Hola, me llamo Juan y soy una voz mexicana.
    Kanya               th_TH    # สวัสดีค่ะ ดิฉันชื่อKanya
    Karen               en_AU    # Hello, my name is Karen. I am an Australian-English voice.
    Kyoko               ja_JP    # こんにちは、私の名前はKyokoです。日本語の音声をお届けします。
    Laura               sk_SK    # Ahoj. Volám sa Laura . Som hlas v slovenskom jazyku.
    Lekha               hi_IN    # नमस्कार, मेरा नाम लेखा है.Lekha मै हिंदी मे बोलने वाली आवाज़ हूँ.
    Luca                it_IT    # Salve, mi chiamo Luca e sono una voce italiana.
    Luciana             pt_BR    # Olá, o meu nome é Luciana e a minha voz corresponde ao português que é falado no Brasil
    Maged               ar_SA    # مرحبًا اسمي Maged. أنا عربي من السعودية.
    Mariska             hu_HU    # Üdvözlöm! Mariska vagyok. Én vagyok a magyar hang.
    Mei-Jia             zh_TW    # 您好，我叫美佳。我說國語。
    Melina              el_GR    # Γεια σας, ονομάζομαι Melina. Είμαι μια ελληνική φωνή.
    Milena              ru_RU    # Здравствуйте, меня зовут Milena. Я – русский голос системы.
    Moira               en_IE    # Hello, my name is Moira. I am an Irish-English voice.
    Monica              es_ES    # Hola, me llamo Monica y soy una voz española.
    Nora                nb_NO    # Hei, jeg heter Nora. Jeg er en norsk stemme.
    Paulina             es_MX    # Hola, me llamo Paulina y soy una voz mexicana.
    Samantha            en_US    # Hello, my name is Samantha. I am an American-English voice.
    Sara                da_DK    # Hej, jeg hedder Sara. Jeg er en dansk stemme.
    Satu                fi_FI    # Hei, minun nimeni on Satu. Olen suomalainen ääni.
    Sin-ji              zh_HK    # 您好，我叫 Sin-ji。我講廣東話。
    Tessa               en_ZA    # Hello, my name is Tessa. I am a South African-English voice.
    Thomas              fr_FR    # Bonjour, je m’appelle Thomas. Je suis une voix française.
    Ting-Ting           zh_CN    # 您好，我叫Ting-Ting。我讲中文普通话。
    Veena               en_IN    # Hello, my name is Veena. I am an Indian-English voice.
    Victoria            en_US    # Isn't it nice to have a computer that will talk to you?
    Xander              nl_NL    # Hallo, mijn naam is Xander. Ik ben een Nederlandse stem.
    Yelda               tr_TR    # Merhaba, benim adım Yelda. Ben Türkçe bir sesim.
    Yuna                ko_KR    # 안녕하세요. 제 이름은 Yuna입니다. 저는 한국어 음성입니다.
    Yuri                ru_RU    # Здравствуйте, меня зовут Yuri. Я – русский голос системы.
    Zosia               pl_PL    # Witaj. Mam na imię Zosia, jestem głosem kobiecym dla języka polskiego.
    Zuzana              cs_CZ    # Dobrý den, jmenuji se Zuzana. Jsem český hlas."""
    # endregion
    # Only works on macs
    assert voice in text_to_speech_voices_for_apple
    text=str(text)
    if filter_characters:  # So you don't have to worry about confusing the terminal with command characters like '|', which would stop the terminal from reading anything beyond that.
        text=''.join(list(c if c.isalnum() or c in ".," else " " for c in text))  # remove_characters_that_confuse_the_terminal
    if rate_in_words_per_minute is not None and not 90 <= rate_in_words_per_minute <= 720:
        fansi_print("r.text_to_speech_via_apple: The rate you chose is ineffective. Empirically, I found that only rates between 90 and 720 have any effect in terminal, \n and you gave me a rate of " + str(rate_in_words_per_minute) + " words per minute. This is the same thing as not specifying a rate at all, as it won't cap off at the max or min.")
#⁠⁠⁠⁠                                                ⎧                                                                                                                                   ⎫
#⁠⁠⁠⁠                                                ⎪   ⎧                                                                                                                              ⎫⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎧                                                                                                              ⎫⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎪                    ⎧                                                                           ⎫             ⎪⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎪                    ⎪⎧                                      ⎫                                   ⎪             ⎪⎪⎪
#⁠⁠⁠⁠   ⎧                                           ⎫⎪   ⎪              ⎪                    ⎪⎪            ⎧                        ⎫⎪                                   ⎪             ⎪⎪⎪
    (run_as_new_thread if run_as_thread else run)(fog(shell_command,("say -v " + voice + ((" -r " + str(rate_in_words_per_minute)) if rate_in_words_per_minute else"") + " " + text)))
#⁠⁠⁠⁠   ⎩                                           ⎭⎪   ⎪              ⎪                    ⎪⎪            ⎩                        ⎭⎪                                   ⎪             ⎪⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎪                    ⎪⎩                                      ⎭                                   ⎪             ⎪⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎪                    ⎩                                                                           ⎭             ⎪⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎪              ⎩                                                                                                              ⎭⎪⎪
#⁠⁠⁠⁠                                                ⎪   ⎩                                                                                                                              ⎭⎪
#⁠⁠⁠⁠                                                ⎩                                                                                                                                   ⎭

# OLD, DIRTIER CODE: (for example, it references shell_command twice!! The new one of course doesn't do that.)
# def text_to_speech_via_apple(msg:str,voice="Samantha",run_as_thread=True,filter_characters=True):
#     if filter_characters:
#         msg=''.join(list(c if c.isalnum() or c in ".," else " " for c in msg))# remove_characters_that_confuse_the_terminal
#     # Only works on macs
#     assert voice in text_to_speech_voices_for_apple
#     if run_as_thread:
#         run_as_new_thread(lambda :shell_command("say -v "+voice+" "+msg))
#     else:
#         shell_command("say -v " + voice + " " + msg)
# endregion
# region ［text_to_speech_via_google］
text_to_speech_voices_for_google=['fr','es-us','el','sr','sv','la','af','lv','zh-tw','sq','da','en-au','ko','cy','mk','id','hy','es','ro','is','zh-yue','hi','zh-cn','th','ta','it','de','ca','sw','ar','nl','pt','cs','sk','ja','tr','zh','hr','es-es','eo','pt-br','pl','fi','hu','en','ru','en-uk','bn','no','en-us','vi']
def text_to_speech_via_google(text: str,voice='en',mp3_file_path: str = 'temp.mp3',play_sound: bool = True,run_as_thread: bool = True):
    # This only works when online, and has a larger latency than the native OSX text-to-speech function
    # Favorite voices: da
    # region gTTS: My own version of https://github.com/pndurette/gTTS (I modified it so that it can actually play voices from other languages, which it couldn't do before. I put that functionality in a comment because I don't know how to use Github yet (Feb 2017))
    import re,requests
    from gtts_token.gtts_token import Token
    class gTTS:
        """ gTTS (Google Text to Speech): an interface to Google'_s Text to Speech API """

        GOOGLE_TTS_URL='https://translate.google.com/translate_tts'
        MAX_CHARS=100  # Max characters the Google TTS API takes at a time
        LANGUAGES={
            'af':'Afrikaans',
            'sq':'Albanian',
            'ar':'Arabic',
            'hy':'Armenian',
            'bn':'Bengali',
            'ca':'Catalan',
            'zh':'Chinese',
            'zh-cn':'Chinese (Mandarin/China)',
            'zh-tw':'Chinese (Mandarin/Taiwan)',
            'zh-yue':'Chinese (Cantonese)',
            'hr':'Croatian',
            'cs':'Czech',
            'da':'Danish',
            'nl':'Dutch',
            'en':'English',
            'en-au':'English (Australia)',
            'en-uk':'English (United Kingdom)',
            'en-us':'English (United States)',
            'eo':'Esperanto',
            'fi':'Finnish',
            'fr':'French',
            'de':'German',
            'el':'Greek',
            'hi':'Hindi',
            'hu':'Hungarian',
            'is':'Icelandic',
            'id':'Indonesian',
            'it':'Italian',
            'ja':'Japanese',
            'ko':'Korean',
            'la':'Latin',
            'lv':'Latvian',
            'mk':'Macedonian',
            'no':'Norwegian',
            'pl':'Polish',
            'pt':'Portuguese',
            'pt-br':'Portuguese (Brazil)',
            'ro':'Romanian',
            'ru':'Russian',
            'sr':'Serbian',
            'sk':'Slovak',
            'es':'Spanish',
            'es-es':'Spanish (Spain)',
            'es-us':'Spanish (United States)',
            'sw':'Swahili',
            'sv':'Swedish',
            'ta':'Tamil',
            'th':'Thai',
            'tr':'Turkish',
            'vi':'Vietnamese',
            'cy':'Welsh'
        }

        def __init__(self,text,lang='en',debug=False):
            self.debug=debug
            if lang.lower() not in self.LANGUAGES:
                raise Exception('Language not supported: %s' % lang)
            else:
                self.lang=lang.lower()

            if not text:
                raise Exception('No text to speak')
            else:
                self.text=text

            # Split text in parts
            if len(text) <= self.MAX_CHARS:
                text_parts=[text]
            else:
                text_parts=self._tokenize(text,self.MAX_CHARS)

                # Clean
            def strip(x):
                return x.replace('\n','').strip()
            text_parts=[strip(x) for x in text_parts]
            text_parts=[x for x in text_parts if len(x) > 0]
            self.text_parts=text_parts

            # Google Translate token
            self.token=Token()

        def save(self,savefile):
            """ Do the Web request and save to `savefile` """
            with open(savefile,'wb') as f:
                self.write_to_fp(f)
                f.close()

        def write_to_fp(self,fp):
            LANGUAGES={'af':'Afrikaans','sq':'Albanian','ar':'Arabic','hy':'Armenian','bn':'Bengali','ca':'Catalan','zh':'Chinese','zh-cn':'Chinese (Mandarin/China)','zh-tw':'Chinese (Mandarin/Taiwan)','zh-yue':'Chinese (Cantonese)','hr':'Croatian','cs':'Czech','da':'Danish','nl':'Dutch','en':'English','en-au':'English (Australia)','en-uk':'English (United Kingdom)','en-us':'English (United States)','eo':'Esperanto','fi':'Finnish','fr':'French','de':'German','el':'Greek','hi':'Hindi','hu':'Hungarian','is':'Icelandic','id':'Indonesian','it':'Italian','ja':'Japanese','ko':'Korean','la':'Latin','lv':'Latvian','mk':'Macedonian','no':'Norwegian','pl':'Polish','pt':'Portuguese','pt-br':'Portuguese (Brazil)','ro':'Romanian','ru':'Russian','sr':'Serbian','sk':'Slovak','es':'Spanish','es-es':'Spanish (Spain)','es-us':'Spanish (United States)','sw':'Swahili','sv':'Swedish','ta':'Tamil','th':'Thai','tr':'Turkish','vi':'Vietnamese','cy':'Welsh'}
            """ Do the Web request and save to a file-like object """
            for idx,part in enumerate(self.text_parts):
                payload={'ie':'UTF-8',
                         'q':part,
                         'tl':self.lang,
                         'total':len(self.text_parts),
                         'idx':idx,
                         'client':'tw-ob',
                         'textlen':len(part),
                         'tk':self.token.calculate_token(part)}
                headers={
                    "Referer":"http://translate.google.com/",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
                }
                if self.debug: print(payload)
                try:
                    r=requests.get(self.GOOGLE_TTS_URL,params=payload,headers=headers)
                    if self.debug:
                        print("Headers: {}".format(r.request.headers))
                        print("Reponse: {}, Redirects: {}".format(r.status_code,r.history))
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=1024):
                        fp.write(chunk)
                except Exception as e:
                    raise

        def _tokenize(self,text,max_size):
            """ Tokenizer on basic roman punctuation """

            punc="¡!()[]¿?.,;:—«»\n"
            punc_list=[re.escape(c) for c in punc]
            pattern='|'.join(punc_list)
            parts=re.split(pattern,text)

            min_parts=[]
            for p in parts:
                min_parts+=self._minimize(p," ",max_size)
            return min_parts

        def _minimize(self,thestring,delim,max_size):
            """ Recursive function that splits `thestring` in chunks
            of maximum `max_size` chars delimited by `delim`. Returns list. """

            if len(thestring) > max_size:
                idx=thestring.rfind(delim,0,max_size)
                return [thestring[:idx]] + self._minimize(thestring[idx:],delim,max_size)
            else:
                return [thestring]
                # endregion
    # endregion
    if run_as_thread:
        return run_as_new_thread(text_to_speech_via_google(text=text,voice=voice,mp3_file_path=mp3_file_path,play_sound=play_sound,run_as_thread=False))
    # Note that this method has to save a sound file in order for it to work. I put a default sound_file_path so that it will overwrite itself each time, so that I can avoid putting a ,delete_sound_file_afterwards:bool=True parameter in there (in case you do infact want to save a file)
    # NOTE: sound_file_path is only compatible with .mp3 files, so don't try putting a wav extension on it (it will break it)!
    lang=voice
    assert lang in text_to_speech_voices_for_google,'r.text_to_speech_via_google: The language you input, "' + lang + '", is not a valid option! Please choose one of the following values for lang instead: ' + ', '.join(text_to_speech_voices_for_google)  # These are the available languages we can choose from.
    gTTS(text=text,lang=lang).save(mp3_file_path)  # gTTS is a class, and .save is a function of an instance of that class.
    if play_sound:
        play_sound_file(mp3_file_path)
# endregion
text_to_speech_voices_all=text_to_speech_voices_for_apple + text_to_speech_voices_for_google
text_to_speech_voices_favorites=['da','en-au','zh-yue','hi','sk','zh','en','it','Samantha','Alex','Moira','Tessa','Fiona','Fred']
def text_to_speech_voices_comparison(text="Hello world",time_per_voice=2,voices=text_to_speech_voices_favorites + shuffled(text_to_speech_voices_all)):
    # Will cycle through different voices so you can choose which one you like best. I selected my favorite voices to be the beginning, and it will cycle through all available voices by the end.
    for voice in voices:
        print("Voice: " + voice)
        text_to_speech(text=text,voice=voice,run_as_thread=True)
        sleep(time_per_voice)
def text_to_speech(text: str,voice: str = None,run_as_thread=True):
    # An abstract combination of the other two text-to-speech methods that automatically selects the right one depending on platform compatiability/whether you specified a compatiable voice etc.
    # Feel free to add more methods into this one: This is what makes the r module so generalizable.
    if run_as_thread:
        run_as_new_thread(text_to_speech,text=text,voice=voice,run_as_thread=False)
    else:
        kwargs=dict(text=text,run_as_thread=False)
        if voice is not None:
            if voice.lower() == 'random':  # A little tidbit i decided to throw in
                voice=random_element(text_to_speech_voices_favorites)
            kwargs['voice']=voice
        try:
            text_to_speech_via_apple(**kwargs)
        except:
            text_to_speech_via_google(**kwargs)
# endregion
# region Audio/Sound Functions: ［load_sound_file，play_sound_from_samples，play_sound_file，play_sound_file_via_afplay，play_sound_file_via_pygame，stop_sound，mp3_to_wav］
np=None
def _module_loader():
    try:
        import numpy#importing numpy takes bootup time
        global np
        np=numpy
        np.set_printoptions(precision=3)#My personal default print option preference: I don't want to see all those digits.
    except:
        pass

fig=None
def _fig():
    #initialize the fig singleton
    global fig
    if fig is None:
        global plt
        plt=_get_plt()
        fig=plt.gcf()#to Get Current Figure
        fig=plt.figure()#Commented this line out because this created a second figure. This has to be done in the main thread or else Mac OS Mojave will crash
    return fig

def set_numpy_print_options(**kwargs):
    #np.set_printoptions is used to format the printed output of arrays. It makes the terminal output much easier to read depending on your context.
    #However, it has a flaw: you can't set a single option without resetting all the other options to the default values.
    #In other words, when you use np.set_printoptions, such as...
    #       np.set_printoptions(precision=3,suppress=True,edgeitems=123,linewidth=get_terminal_width()),
    #...only every parameter you didn't specify will be reset to the default value. This isn't as useful as it could be.
    #Introducing set_numpy_print_options: This function takes the same arguments that np.set_printoptions does, except it sets only the arguments you give it.
    #See np.set_printoptions?/ for more documentation on what these arguments do.
    #EXAMPLE: set_numpy_print_options(precision=8) #Prints floating points with up to 8 decimals of precision
    import numpy as np
    for kwarg in kwargs:
        #Make sure we feed only valid parameters to np.set_printoptions
        assert kwarg in np.get_printoptions(),'set_numpy_print_options: '+repr(kwarg)+' is not a valid argument name. Available print options: '+repr(np.get_printoptions())#Prints something like this: "AssertionError: set_numpy_print_options: 'sodf' is not a valid argument name. Available print options: {'nanstr': 'nan', 'precision': 3, 'floatmode': 'maxprec', 'linewidth': 152, 'formatter': None, 'suppress': False, 'edgeitems': 3, 'infstr': 'inf', 'sign': '-', 'legacy': False, 'threshold': 1000}"
    np.set_printoptions(**{**np.get_printoptions(),**kwargs})

_module_loader()# run_as_new_thread(_module_loader) <--- This caused problems when I tried to show images, so the bootup speed increase (like .1 seconds) is definately not worth it

def load_sound_file(file_path: str,samplerate_adjustment=False,override_extension: str = None) :
    #TODO: Use the 'audioread' library to decode more than just .wav files, using more than just ffmpeg. This will make this function more robust. https://github.com/beetbox/audioread
    # Opens sound files and turns them into numpy arrays! Unfortunately right now it only supports mp3 and wav files.
    # Supports only .mp3 and .wav files.
    # samplerate_adjustment:
    # If true, your sound will be re-sampled to match the Đ_samplerate.
    # If false, it will leave it as-is.
    # If it'_s None, this function will output a tuple containing (the original sound, the original samplerate)
    # Otherwise, it should be a number representing the desired samplerate it will re-sample your sound to match the given samplerate.
    # Set override_extension to either 'mp3' or 'wav' to ignore the extension of the file name you gave it. For example, using override_extension='mp3' on 'music.wav' will force it to read music as an mp3 file instead.
    if file_path.endswith(".mp3") or override_extension is not None and 'mp3' in override_extension:
        file_path=mp3_to_wav(file_path)
    else:
        assert file_path.endswith(".wav") or 'wav' in override_extension,'sound_file_to_samples: ' + file_path + " appears to be neither an mp3 nor wav file." + " Try overriding the extension?" * (override_extension is None)
    pip_import('scipy')
    import scipy.io.wavfile as wav
    samplerate,samples=wav.read(file_path)
    try:
        samples=np.ndarray.astype(samples,float) / np.iinfo(samples.dtype).max  # ⟶ All samples ∈ [-1,1]
    except:
        pass

    if samplerate_adjustment is False:
        return samples
    if samplerate_adjustment is None:
        return samples,samplerate
    new_samplerate=Đ_samplerate if samplerate_adjustment is True else samplerate_adjustment
    if new_samplerate == samplerate:  # Don't waste time by performing unnecessary calculations.
        return samples
    from scipy.signal import resample
    length_in_seconds=len(samples) / samplerate
    new_number_of_samples=int(length_in_seconds * new_samplerate)
    return resample(samples,num=new_number_of_samples)

def save_wav(samples,path,samplerate=None) -> None:  # Usually samples should be between -1 and 1
    pip_import('scipy')
    from scipy.io import wavfile
    if samples.dtype == np.float64:
        samples=samples.astype(np.float32)
    wavfile.write(path,samplerate or Đ_samplerate,samples)

Đ_samplerate=44100  # In (Hz ⨯ Sample). Used for all audio methods in the 'r' class.
def play_sound_from_samples(samples,samplerate=None,blocking=False,loop=False,**kwargs):
    # For stereo, use a np matrix
    # Example: psfs((x%100)/100 for x in range(100000))
    # Each sample should ∈ [-1,1] or else it will be clipped (if it wasn't clipped it would use modular arithmeti
    # c on the int16, which would be total garbage for sound)
    # Just like matlab'_s 'sound' method, except this one doesn't let you play sounds on top of one-another.
    pip_import('sounddevice')
    if not running_in_ipython():
        import sounddevice
        wav_wave=np.array(np.minimum(2 ** 15 - 1,2 ** 15 * np.maximum(-1,np.minimum(1,np.matrix(list(samples)))).transpose()),dtype=np.int16)  # ⟵ Converts the samples into wav format. I tried int32 and above: None of them worked. 16-bit seems to be the highest resolution available.
        sounddevice.play(wav_wave,samplerate=samplerate or Đ_samplerate,blocking=blocking,loop=loop,**kwargs)
    else:
        #This works in google colab!
        from IPython.display import Audio
        assert not loop,'This function cannot currently play looped audio when running in Jupyter'
        assert not blocking,'This function cannot currently block while playing audio when running in Jupyter'#This might change in future versions of rp
        Audio(samples,rate=samplerate,autoplay=True)

def play_sound_file(path):
    # THIS Function is an abstraction of playing sound files. Just plug in whatever method works on your computer into this one to make it work
    # NOTE: These functions should all run on separate threads from the main thread by default!
    try:
        from playsound import playsound
        playsound(path)# Worked on windows, but didn't work on my mac
    except:
        try:
            play_sound_file_via_afplay(path)
        except:
            play_sound_file_via_pygame(path)

def play_sound_file_via_afplay(absolute_file_path_and_name: str,volume: float = None,rate: float = None,rate_quality: float = None,parallel: bool = True,debug: bool = True):
    # Use stop_sound to stop it.
    # If parallel==False, the code will pause until the song is finished playing.
    # If parallel==True the sound is run in a new process, and returns this process so you can .terminate() it later. It lets things continue as usual (no delay before the next line of code)
    # This seems to be a higher quality playback. On the other hand, I can't figure out any way to stop it.
    # This version doesn't require any dependencies BUT doesn't work on windows and doesn't let us play .mp3 files. The new version uses pygame and DOES allow us to.
    # Only tested on my MacBook. Uses a terminal command called 'afplay' to play a sound file.
    # Might not work with windows or linux.
    command="afplay '" + absolute_file_path_and_name + "'"
    if rate is not None:
        assert rate > 0,"r.play_sound_file_via_afplay: Playback rate cannot rate=" + str(rate)
        command+=' -r ' + str(rate)
    if rate_quality is not None:
        if rate is None and debug:
            print("r.play_sound_file_via_afplay: There'_s no reason for rate_quality not to be none: rate==None, so rate_quality doesn't matter. Just sayin'. To make me shut up, turn the debug parameter in my method to True.")
        command+=' -q ' + str(rate_quality)
    if volume is not None:
        command+=' -v ' + str(volume)
    return (run_as_new_thread if parallel else run)(shell_command,command)  # If parallel==True, returns the process so we can terminate it later.

def play_sound_file_via_pygame(file_name: str,return_simple_stopping_function=True):
    # Old because it uses the pygame.mixer.sound instead of pygame.mixer.music, which accepts more file types and has more controls than this one does.
    # Though, audio and file things are weird. I'm keeping this in case the other two fail for some reason. Other than being a backup like that, this method serves no purpose.
    # noinspection PyUnresolvedReferences
    pip_import('pygame')
    import pygame
    pygame.init()
    pygame.mixer.init()
    sound=pygame.mixer.Sound(file_name)
    assert isinstance(sound,pygame.mixer.Sound)
    sound.play()
    if return_simple_stopping_function:
        return sound.stop  # The 'Sound' class has only two methods: play and stop. Because we've already used the play method, the only other possible method we would want is the stop() method.
    return sound  # This version gives us a little more control; it gives us the 'play' method too. That'_s the only difference. but python doesn't tell us the method names! This gives us options to, perhaps, stop the sound later on via sound.stop()

def stop_sound():
    # Stop sounds from all sources I know of that the 'r' module can make.
    # So far I have been unsuccessful in stopping
    try:
        shell_command("killall afplay")  # Used with 'play_sound_file_via_afplay' on macs.
    except:
        pass
    # try:run_as_new_thread(shell_command,"killall com.apple.speech.speechsynthesisd")# ⟵ Works when I enter the command in terminal, but doesn't work when called from python! It'_s not very important atm though, so I'm not gonna waste time over it.
    # except:pass
    try:
        import sounddevice
        sounddevice.stop()
    except:
        pass
    try:
        import pygame
        pygame.mixer.stop()
    except:
        pass

_Đ_wav_output_path='r.mp3_to_wav_temp.wav'  # Expect this file to be routinely overwritten.
def mp3_to_wav(mp3_file_path: str,wav_output_path: str = _Đ_wav_output_path,samplerate=None) -> str:
    # This is a audio file converter that converts mp3 files to wav files.
    # You must install 'lame' to use this function.
    # Saves a new wav file derived from the mp3 file you gave it.
    # shell_command('lame --decode '+mp3_file_path+" "+wav_output_path)# From https://gist.github.com/kscottz/5898352
    shell_command('lame ' + str(samplerate or Đ_samplerate) + ' -V 0 -h --decode ' + mp3_file_path + " " + wav_output_path)  # From https://gist.github.com/kscottz/5898352
    return wav_output_path
# endregionx
# region  Matplotlib: ［display_image，brutish_display_image，display_color_255，display_grayscale_image，line_graph，block，clf］

def display_image(image,block=False):
    #Very simple to understand: this function displays an image.
    #At first, it tries to use matplotlib and if that errors it falls back to opencv's imshow function.
    #By default this function will not halt your code, but if you set block=True, it will.
    #This function works in Jupyter Notebooks such as google colab, and will automatically scale the DPI of the output such that the full-resolution image is shown (don't take this for granted)
    #You can pass this function binary, rgb, rgba, grayscale matrices -- most types of images (see rp.is_image() for more information)
    if isinstance(image,str):
        fansi_print("display_image usually meant for use with numpy arrays, but you passed it a string, so we'll try to load the image load_image("+repr(image)+") and display that.")
        image=load_image(image)
    if not isinstance(image,np.ndarray) and not isinstance(image,list):
        try:
            import torch
            if isinstance(image,torch.autograd.Variable):
                image=image.data
            elif isinstance(image,torch.Tensor):
                image=image.cpu().numpy()
        except:pass
    global plt
    plt=_get_plt()
    if is_image(image):
        image=as_rgb_image(as_float_image(image))
    try:
        plt.clf()
        if running_in_ipython():
            fig=plt.figure()#Make a new figure. When jupyter, this makes sense; but normally we don't want this (it will make a bazillion windows)
            mpl=pip_import('matplotlib')
            # import matplotlib as mpl
            #region Set the jupyter resolution to the true image size (it usually squashes the image too small for comfort)
            old_dpi,old_figsize=mpl.rcParams['figure.dpi'],mpl.rcParams['figure.figsize']#
            arbitrary_number=100
            mpl.rcParams['figure.dpi'] = arbitrary_number
            mpl.rcParams['figure.figsize']=[image.shape[0]/arbitrary_number,image.shape[1]/arbitrary_number]
        else:
            fig = _fig()
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(image, aspect='equal')
        plt.show(block=block)
        if not block:
            plt.pause(0.0001)
        if running_in_ipython():
            plt.close(fig)#I don't know if this is necessary. It's a hunch it might make it faster in the long term if we have 239239872 figures opened in jupyter. It doesn't hurt, though, so I'm keeping it here.
            mpl.rcParams['figure.dpi'],mpl.rcParams['figure.figsize']=old_dpi,old_figsize
    except:
        if not running_in_google_colab():
            image=np.asarray(image)
            #The above seems not to work anymore, so the next thing to try is opencv's image display (in the event that it fails)...
            ndim=len(image.shape)
            assert ndim in {2,3},'Image tensor must have either two or three dimensions (either a grayscale image or '
            if ndim==2:
                image=grayscale_to_rgb(image)
            if image.dtype==bool:
                image=image.astype(float)
            cv_imshow(image,wait=10 if not block else 1000000)#Hit esc in the image to exit it

def brutish_display_image(image):
    from copy import deepcopy
    global plt
    plt=_get_plt()
    image=deepcopy(image)
    for x_index,x in enumerate(image):
        for y_index,y in enumerate(x):
            for channel_index,channel in enumerate(y):
                image[x_index][y_index][channel_index]=max(0,min(1,channel))
    display_image(image)
    plt.show(block=True)
def display_color_255(*color: list):
    # noinspection PyUnresolvedReferences
    # Example: display_color_255(255,0,0)# ⟵ Displays Red
    display_image([(np.matrix(detuple(color)) / 256).tolist()])
def display_grayscale_image(matrix,pixel_interpolation_method_name: str = 'bicubic',refresh=True):
    pixel_interpolation_method_name=str(pixel_interpolation_method_name).lower()  # Note that None⟶'none'
    assert pixel_interpolation_method_name in [None,'none','nearest','bilinear','bicubic','spline16','spline36','hanning','hamming','hermite','kaiser','quadric','catrom','gaussian','bessel','mitchell','sinc','lanczos']  # These are the options. See http://stackoverflow.com/questions/14722540/smoothing-between-pixels-of-imagesc-imshow-in-matlab-like-the-matplotlib-imshow/14728122#14728122
    global plt
    plt=_get_plt()
    plt.imshow(matrix,cmap=plt.get_cmap('gray'),interpolation=pixel_interpolation_method_name)  # "cmap=plt.get_cmap('gray')" makes it show a black/white image instead of a color map.
    if refresh:
        plt.draw()
        plt.show(block=False)  # You can also use the r.block() method at any time if you want to make the plot usable.
        plt.pause(0.0001)  # This is nessecary, keep it here or it will crash. I don't know WHY its necessary, but empirically speaking it seems to be.
def bar_graph(values,*,width=.9,align='center',block=False):
    #Create a bar graph with the given y-values
    #The 'values' parameter is a list of bar heights. They should all be real numbers.
    #The 'width'  parameter sets the width of each bar
    #The 'align'  parameter sets whether the bars are to the center, right or left of each index
    #EXAMPLE: bar_graph(randints(10))
    pip_import('matplotlib')
    plt=_get_plt()

    assert align in {'center','left','right'}
    if align=='right':
        #The right of the bars touch the index numbers, like in a right-riemann-sum
        #According to matplotlib, to do this we set align to 'edge' and multiply width by -1
        width*=-1
        align='edge'
    if align=='left':
        #Vice versa, see 'right' above
        align='edge'

    x=list(range(len(values)))

    plt.clf()
    plt.bar(x,values,width=width,align=align)
    plt.show(block=block)
    plt.pause(.001)
def line_graph(*y_values,show_dots: bool = False,clf: bool = True,y_label: str = None,x_label: str = None,use_dashed_lines: bool = False,line_color: str = None,graph_title=None,block: bool = False,background_image=None) -> None:
    # This is mainly here as a simple reference for how to create a line-graph with matplotlib.pyplot.
    # There are plenty of options you can configure for it, such as the color of the line, label of the
    # axes etc. For more information on this, see http://matplotlib.org/users/pyplot_tutorial.html
    global plt
    pip_import('matplotlib')
    plt=_get_plt()
    if clf:
        plt.clf()

    def plot(values):
        kwargs={}
        if show_dots:
            # Put a dot on each point on the line-graph.
            kwargs['marker']='o'
        if use_dashed_lines:
            kwargs['linestyle']='--'
        if line_color:
            kwargs['color']=line_color  # could be 'red' 'green' 'cyan' 'blue' etc
        plt.plot(values,**kwargs)

    try:
        plot(*y_values)  # If this works, then y_values must have been a single-graph.
    except:  # y_values must have been an iterable of iterables, so we will graph each one on top of each other.
        # old_hold_value=plt.ishold() #This uses deprecated matplotlib stuff: https://github.com/matplotlib/matplotlib/issues/12337/
        # plt.hold(True)  # This lets us plot graphs on top of each other.
        for y in y_values:
            plot(y)
        # plt.hold(old_hold_value)

    if y_label:
        plt.ylabel(y_label)
    if x_label:
        plt.xlabel(x_label)
    if graph_title:
        plt.title(graph_title)

    plt.draw()
    plt.show(block=block)  # You can also use the r.block() method at any time if you want to make the plot useable.
    plt.pause(.001)
def block(on_click=None,on_unclick=None):
    _fig()#Initialize fig
    # You may specify methods you would like to overwrite here.
    # Makes the plot interactive, but also prevents python script from running until the user clicks closes the graph window.
    pip_import('matplotlib')
    import matplotlib.backend_bases
    def handler(function,event_data: matplotlib.backend_bases.MouseEvent):
        args=event_data.xdata,event_data.ydata,event_data.button,event_data.dblclick
        if None not in args:
            function(*args)
    handler_maker=lambda function:lambda event:handler(function,event)
    if on_click is not None:
        assert callable(on_click)
        # def on_click(x,y,button,dblclick)
        _fig.canvas.mpl_connect('button_press_event',handler_maker(on_click))
    if on_unclick is not None:
        assert callable(on_unclick)
        # def on_unclick(x,y,button,dblclick)
        _fig.canvas.mpl_connect('button_release_event',handler_maker(on_unclick))
    # PLEASE NOTE THAT MORE METHODS CAN BE ADDED!!!!! A LIST OF THEM IS IN THE BELOW COMMENT:
    # - 'button_press_event'
    # - 'button_release_event'
    # - 'draw_event'
    # - 'key_press_event'
    # - 'key_release_event'

    # - 'motion_notify_event'
    # - 'pick_event'
    # - 'resize_event'
    # - 'scroll_event'
    # - 'figure_enter_event',
    # - 'figure_leave_event',
    # - 'axes_enter_event',
    # - 'axes_leave_event'
    # - 'close_event'
    plt.show(True)
def clf():
    plt.clf()
# endregion
# region Min/Max Indices/Elements:［min_valued_indices，max_valued_indices，min_valued_elements，max_valued_elements，max_valued_index，min_valued_index］
def _minmax_indices(l,f=None):
    if len(l) == 0:
        return l.copy()  # An empty list/tuple/set or whatever
    # A helper method for the min/max methods below. f is either 'min' or 'max'
    return matching_indices(f(l),l)
def min_valued_indices(l):
    # Returns the indices with the minimum-valued elements
    return _minmax_indices(l,min)
def max_valued_indices(l):
    # Returns the indices with the maximum-valued elements
    return _minmax_indices(l,max)
def min_valued_elements(l):
    # Returns the elements with the smallest values
    return gather(l,min_valued_indices(l))
def max_valued_elements(l):
    # Returns the elements with the largest values
    return gather(l,max_valued_indices(l))
def max_valued_index(l):
    return list(l).index(max(l))  # Gets the index of the maximum value in list 'l'. This is a useful def by rCode standards because it references 'l' twice.
def min_valued_index(l):
    return list(l).index(min(l))  # Gets the index of the minimum value in list 'l'. This is a useful def by rCode standards because it references 'l' twice.
# endregion
# region  Blend≣Lerp/sign: ［blend，iblend，lerp，interp，linterp］
def blend(𝓍,𝓎,α):  # Also known as 'lerp'
    return (1 - α) * 𝓍 + α * 𝓎  # More α ⟹ More 𝓎 ⋀ Less 𝓍
def iblend(z,𝓍,𝓎):  # iblend≣inverse blend. Solves for α， given 𝓏﹦blend(𝓍,𝓎,α)
    z-=𝓍
    z/=𝓎-𝓍
    return z
def interp(x,x0,x1,y0,y1):  # 2 point interpolation
    return (x - x0) / (x1 - x0) * (y1 - y0) + y0  # https://www.desmos.com/calculator/bqpv7tfvpy
def linterp(x,l,cyclic=False):# Where l is a list or vector etc
    try:
        if cyclic:
            x%=len(l)
            l=l+[l[0]]# Don't use append OR += (which acts the same way apparently); this will mutate l!
        assert x>=0
        x0=int(np.floor(x))
        x1=int(np.ceil(x))
        if x0==x1:
            return l[int(x)]
        return blend(l[x0],l[x1],iblend(x,x0,x1))
    except IndexError as ⵁ:
        if cyclic:
            fansi_print("ERROR: r.linterp: encountered an index error; did you mean to enable the 'cyclic' parameter?",'red')
        raise ⵁ
# def sign(x):
#     return 1 if x>0 else (0 if x==0 else -1)
# endregion
# region  Gathering/Matching: ［matching_indices，gather，pop_gather］
def matching_indices(x,l,check=lambda x,y:x == y):
    # Returns the matching indices of element 'x' in list 'l'
    out=[]
    for i,y in enumerate(l):
        if check(x,y):
            out.append(i)
    return out
def gather(iterable,*indices):
    # indices ∈ list of integers
    indices=detuple(indices)
    assert is_iterable(iterable),"The 'iterable' parameter you fed in is not an iterable!"
    assert is_iterable(indices),"You need to feed in a list of indices, not just a single index.  indices == " + str(indices)
    return [iterable[i] for i in indices]  # ≣list(map(lambda i:iterable[i],indices))
def pop_gather(x,*indices):
    indices=detuple(indices)
    out=gather(x,indices)
    # Uses CSE214 definition of 'pop', in the context of popping stacks.
    # It is difficult to simultaneously delete multiple indices in a list.
    # My algorithm goes through the indices chronologically, compensating for
    # the change in indices by subtracting incrementally larger values from them
    # Example:
    #  ⮤ ⵁ = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    #  ⮤ pop_gather(ⵁ,1,3,5,7,9)
    # ans = ['a', 'c', 'e', 'g', 'i']
    #  ⮤ g
    # ans = ['0', 'b', 'd', 'f', 'h']
    for a,b in enumerate(sorted(set(indices))):
        del x[b - a]
    return out
# endregion
# region  List/Dict Functions/Displays: ［list_to_index_dict，invert_dict，invert_dict，invert_list_to_dict，dict_to_list，list_set，display_dict，display_list］
def list_to_index_dict(l: list) -> dict:
    # ['a','b','c'] ⟶ {0: 'a', 1: 'b', 2: 'c'}
    return {i:v for i,v in enumerate(l)}
def invert_dict(d: dict,bijection=True) -> dict:
    if bijection:
        # {0: 'a', 1: 'b', 2: 'c'} ⟶ {'c': 2, 'b': 1, 'a': 0}
        return {v:k for v,k in zip(d.values(),d.keys())}
    else:
        # {0: 'a', 1: 'a', 2: 'b'} ⟶ {'a': (0,1), 'b': (2,)}
        out={}
        for k,v in d.items():
            if v in out:
                out[v]+=k,
            else:
                out[v]=k,
        return out
def invert_list_to_dict(l: list) -> dict:
    # ['a','b','c'] ⟶ {'c': 2, 'a': 0, 'b': 1}
    assert len(set(l)) == len(l),'r.dict_of_values_to_indices: l contains duplicate values, so we cannot return a 1-to-1 function; and thus ∄ a unique dict that converts values to indices for this list!'
    return invert_dict(list_to_index_dict(l))
def dict_to_list(d: dict) -> list:
    # Assumes keys should be in ascending order
    return gather(d,sorted(d.keys()))
def list_set(x):
    # Similar to performing list(set(x)), except that it preserves the original order of the items.
    # You could also think of it as list_set≣remove_duplicates
    # Demo:
    #       ⮤ l=[5,4,4,3,3,2,1,1,1]
    #       ⮤ list(set(l))
    #       ans=[1,2,3,4,5]
    #       ⮤ list_set(l)  ⟵ This method
    #       ans=[5,4,3,2,1]
    from  more_itertools import unique_everseen  # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-whilst-preserving-order
    return list(unique_everseen(x))
# ――――――――――――――――――――――
# Three fansi colors (see the fansi function for all possible color names):
Đ_display_key_color=lambda x123:fansi(x123,'cyan')
Đ_display_arrow_color=lambda x123:fansi(x123,'green')
Đ_display_value_color=lambda x123:fansi(x123,'blue')
def display_dict(d: dict,
                 key_color      = Đ_display_key_color,
                 arrow_color    = Đ_display_arrow_color,
                 value_color    = Đ_display_value_color,
                 clip_width     = False,
                 post_processor = identity,
                 key_sorter     = sorted,
                 print_it       = True,
                 arrow          = " ⟶  "
                 ) -> None:
    # Made by Ryan Burgert for the purpose of visualizing large dictionaries.
    # EXAMPLE DISPLAY:
    '''
     ⮤ display_dict({'name': 'Zed', 'age': 39, 'height': 6 * 12 + 2})
    age ⟶  39
    height ⟶  74
    name ⟶  Zed
    '''
    # Of course, in the console you will see the appropriate colors for each section.
    return (print if print_it else identity)((((lambda x:clip_string_width(x,max_wraps_per_line=2,clipped_suffix='………')) if clip_width else identity)(post_processor('\n'.join((key_color(key) + arrow_color(arrow) + value_color(d[key])) for key in key_sorter(d.keys()))))))  # Theres a lot of code here because we're trying to make large amounts of text user-friendly in a terminal environment. Thats why this is so complicated and possibly perceived as messy
def display_list(l: list,
                 key_color   = Đ_display_key_color,
                 arrow_color = Đ_display_arrow_color,
                 value_color = Đ_display_value_color,
                 print_it    = True) -> None:
    # also works with tuples etc
    return display_dict(d=list_to_index_dict(l),key_color=key_color,arrow_color=arrow_color,value_color=value_color,print_it=print_it)
# endregion
# region  'youtube_dl'﹣dependent methods: ［rip_music，rip_info］
# noinspection SpellCheckingInspection

Đ_rip_music_output_filename="rip_music_temp"
def rip_music(URL: str,output_filename: str = Đ_rip_music_output_filename,desired_output_extension: str = 'wav',quiet=False):
    # Ryan Burgert Jan 15 2017
    # Rips a music file off of streaming sites and downloads it to the default directory…
    # URL: Can take URL's from youtube, Vimeo, SoundCloud...apparently youtube_dl supports over 400 sites!!
    # output_filename: Shouldn't include an extension, though IDK if it would hurt. By default the output file is saved to the default directory.
    # desired_output_extension: Could be 'wav', or 'mp3', or 'ogg' etc. You have the freedom to choose the type of file you want to download regardless of the type of the original online file; it will be converted automatically (because youtube is a huge mess of file types)
    #   NOTE: ‘brew install ffmpeg’ (run command in terminal) is necessary for some desired_output_extension types.
    # This method returns the name of the file it created.
    # Dependency: youtube_dl  ﹙See: https://rg3.github.io/youtube-dl/﹚
    # Quiet: If this is true, then nothing will display on the console as this method downloads and converts the file.
    # NOTE: youtube_dl has MANY more cool capabilities such as extracting the title/author/cover picture of the songs…
    #   …as well as breing able to download entire play-lists at once! youtube_dl can also rip videos; which could be very useful in another context!
    # EXAMPLE: play_sound_file_via_afplay(rip_music('https://www.youtube.com/watch?v=HcgEHrwdSO4'))
    import youtube_dl
    ydl_opts= \
        {
            'format':'bestaudio/best',  # Basically, grab the highest quality that we can get.
            'outtmpl':output_filename + ".%(ext)s",  # https://github.com/rg3/youtube-dl/issues/7870  ⟵ Had to visit this because it kept corrupting the audio files: Now I know why! Don't change this line.
            'postprocessors':
                [{
                    'key':'FFmpegExtractAudio',
                    'preferredcodec':desired_output_extension,
                    # 'preferredquality': '192',
                }],
            'quiet':quiet,  # If this is not enough, you can add a new parameter, 'verbose', to make it jabber even more. You can find these parameters in the documentation of the module that contains the 'YoutubeDL' method (used in a line below this one)
            'noplaylist':True,  # only download single song, not playlist
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    return output_filename + "." + desired_output_extension
def rip_info(URL: str):
    # A companion method for rip_music, this will give you all the meta-data of each youtube video or vimeo or soundcloud etc.
    # It will give you this information in the form of a dictionary.
    # Known keys:
    # ［abr，acodec，age_limit，alt_title，annotations，automatic_captions，average_rating，…
    # … categories，creator，description，dislike_count，display_id，duration，end_time，ext，…
    # … extractor，extractor_key，format，format_id，formats，fps，height，id，is_live，license，…
    # … like_count，playlist，playlist_index，requested_formats，requested_subtitles，resolution，…
    # … start_time，stretched_ratio，subtitles，tags，thumbnail，thumbnails，title，upload_date，…
    # … uploader，uploader_id，uploader_url，vbr，vcodec，view_count，webpage_url，webpage_url_basename，width］
    from youtube_dl import YoutubeDL
    return YoutubeDL().extract_info(URL,download=False)
# endregion
# region  Sending and receiving emails: ［send_gmail_email，gmail_inbox_summary，continuously_scan_gmail_inbox］
from rp.r_credentials import Đ_gmail_address   # ⟵ The email address we will send emails from and whose inbox we will check in the methods below.
from rp.r_credentials import Đ_gmail_password  # ⟵ Please don't be an asshole: Don't steal this account! This is meant for free use!
Đ_max_ↈ_emails=100  # ≣ _default_max_number_of_emails to go through in the gmail_inbox_summary method.
def send_gmail_email(recipientⳆrecipients,subject: str = "",body: str = "",gmail_address: str = Đ_gmail_address,password: str = Đ_gmail_password,attachmentⳆattachments=None,shutup=False):
    # For attachmentⳆattachments, include either a single string or iterable of strings containing file paths that you'd like to upload and send.
    # param recipientⳆrecipients: Can be either a string or a list of strings: all the emails we will be sending this message to.
    # Heavily modified but originally from https://www.linkedin.com/pulse/python-script-send-email-attachment-using-your-gmail-account-singh
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    import smtplib
    emaillist=[x.strip().split(',') for x in enlist(recipientⳆrecipients)]
    msg=MIMEMultipart()
    msg['Subject']=subject
    # msg['From']='presidentstanely@gmail.com'# ⟵       I couldn't find any visible effect from keeping this active, so I decided to remove it.
    # msg['Reply-to']='ryancentralorg@gmail.com' # ⟵    I couldn't find any visible effect from keeping this active, so I decided to remove it.
    # msg.preamble='Multipart massage mushrooms.\n' # ⟵ I couldn't find any visible effect from keeping this active, so I decided to remove it.
    msg.attach(MIMEText(body))
    if attachmentⳆattachments:
        for filename in enlist(attachmentⳆattachments):
            assert isinstance(filename,str)  # These should be file paths.
            part=MIMEApplication(open(filename,"rb").read())
            part.add_header('Content-Disposition','attachment',filename=filename)  # ⟵ I tested getting rid of this line. If you get rid of the line, it simply lists the attachment as a file on the bottom of the email, …
            # … and wouldn't show (for example) an image. With it, though, the image is displayed. Also, for files it really can't display (like .py files), it will simply act as if this line weren't here and won't cause any sort of error.
            msg.attach(part)
    try:
        with smtplib.SMTP("smtp.gmail.com:587") as server:
            server.ehlo()
            server.starttls()
            server.login(gmail_address,password)
            server.sendmail(gmail_address,emaillist,msg.as_string())
            server.close()
        if not shutup:
            print('r.send_gmail_email: successfully sent your email to ' + str(recipientⳆrecipients))
    except Exception as E:
        if not shutup:
            print('r.send_gmail_email: failed to send your email to ' + str(recipientⳆrecipients) + ". Error message: " + str(E))
# region Old version of send_gmail_email (doesn't support attachments):
"""def send_gmail_email(recipientⳆrecipients, subject:str="", body:str="",gmail_address:str=Đ_gmail_address,password:str=Đ_gmail_password,shutup=False):
    # param recipientⳆrecipients: Can be either a string or a list of strings: all the emails we will be sending this message to.
    import smtplib
    FROM = gmail_address
    TO = enlist(recipientⳆrecipients)# Original code: recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = "From: %s\nTo: %s\nSubject: %s\n\n%s\n" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_address, password)
        server.sendmail(FROM, TO, message)
        server.close()
        if not shutup:
            print('r: send_gmail_email: successfully sent the mail')
    except:
        if not shutup:
            print( "r: send_gmail_email: failed to send mail")"""
# endregion
def gmail_inbox_summary(gmail_address: str = Đ_gmail_address,password: str = Đ_gmail_password,max_ↈ_emails: int = Đ_max_ↈ_emails,just_unread_emails: bool = True):
    # Parameters captured in this summary include the fields (for the dicts in the output list) of
    # TODO［millis，sender，receiver，subject，sender_email，sender_name］  (Just using a TODO so that it's a different color in the code so it stands out more)  (all accessed as strings, of course)
    # returns a list of dictionaries. The length of this list ﹦ the number of emails in the inbox (both read and unread).
    # max_ↈ_emails ≣ max_number_of_emails ⟹ caps the number of emails in the summary, starting with the most recent ones.
    '''Example output:
    [{'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484416777000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Computing Society] 10 games in 10 days. Today\'s game is "Purple...', 'receiver': 'Stony Brook Computing Society <sb.computing@groups.facebook.com>'},
    {'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484368779000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Game Developers (SBGD)] New link', 'receiver': '"Stony Brook Game Developers (SBGD)" <sbgamedev@groups.facebook.com>'},
    {'sender_email': 'no-reply@accounts.google.com', 'sender': 'Google <no-reply@accounts.google.com>', 'millis': 1484366367000, 'sender_name': 'Google', 'subject': 'New sign-in from Safari on iPhone', 'receiver': 'ryancentralorg@gmail.com'},
    {'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484271805000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Computing Society] 10 games in 10 days. Today\'s game is "Jet LIfe"....', 'receiver': 'Stony Brook Computing Society <sb.computing@groups.facebook.com>'},
    {'sender_email': 'noreply@sendowl.com', 'sender': 'imitone sales <noreply@sendowl.com>', 'millis': 1484240836000, 'sender_name': 'imitone sales', 'subject': 'A new version of imitone is available!', 'receiver': 'ryancentralorg@gmail.com'}]'''
    # The following code I got of the web somewhere and modified a lot, I don't remember where though. Whatevs.
    import datetime
    import email
    import imaplib

    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        # ptoc()
        mail.login(gmail_address,password)
        # ptoc()
        mail.list()
        # ptoc()
        mail.select('inbox')
        # ptoc()
        result,data=mail.uid('search',None,"UNSEEN" if just_unread_emails else "ALL")  # (ALL/UNSEEN)
        # ptoc()

        email_summaries=[]  # A list of dictionaries. Will be added to in the for loop shown below.
        ↈ_emails=len(data[0].split())
        for x in list(reversed(range(ↈ_emails)))[:min(ↈ_emails,max_ↈ_emails)]:
            latest_email_uid=data[0].split()[x]
            result,email_data=mail.uid('fetch',latest_email_uid,'(RFC822)')
            # result, email_data = conn.store(num,'-FLAGS','\\Seen')
            # this might work to set flag to seen, if it doesn't already
            raw_email=email_data[0][1]
            raw_email_string=raw_email.decode('utf-8')
            email_message=email.message_from_string(raw_email_string)

            # Header Details
            date_tuple=email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date=datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                # local_message_date=local_date.ctime()# formats the date in a nice readable way
                local_message_date=local_date.timestamp()  # Gets seconds since 1970
                local_message_date=int(1000 * local_message_date)  # millis since 1970
            email_from=str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_to=str(email.header.make_header(email.header.decode_header(email_message['To'])))
            subject=str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            # noinspection PyUnboundLocalVariable
            email_summaries.append(dict(millis=local_message_date,sender=email_from,receiver=email_to,subject=subject,sender_email=email_from[1 + email_from.find('<'):-1] if '<' in email_from else email_from,sender_name=email_from[:email_from.find('<') - 1]))
            # print('\n'.join(map(str,email_summaries)))//⟵Would display all email summaries in console
    return email_summaries
def _Đ_what_to_do_with_unread_emails(x):
    # An arbitrary default as an example example so that 'continuously_scan_gmail_inbox' can be run with no arguments
    # Example: continuously_scan_gmail_inbox()
    # By default, the continuous email scan will print out the emails and also read their subjects aloud via text-to-speech. (Assumes you're using a mac for that part).
    print(x)
    text_to_speech_via_apple(x['subject'],run_as_thread=False)
    send_gmail_email(x['sender_email'],'EMAIL RECEIVED: ' + x['subject'])
def continuously_scan_gmail_inbox(what_to_do_with_unread_emails: callable = _Đ_what_to_do_with_unread_emails,gmail_address: str = Đ_gmail_address,password: str = Đ_gmail_password,max_ↈ_emails: int = Đ_max_ↈ_emails,include_old_but_unread_emails: bool = False):
    # returns a new thread that is ran constantly unless you kill it. It will constantly scan the subjects of all emails received
    #  …AFTER the thread has been started. When it received a new email, it will run the summary of that email through the
    #  …'what_to_do_with_unread_emails' method, as a triggered event. It returns the thread it's running on so you can do stuff with it later on.
    #  …Unfortunately, I don't know how to make it stop though...
    # include_old_but_unread_emails: If this is false, we ignore any emails that were sent before this method was called. Otherwise, if include_old_but_unread_emails is true, …
    #  …we look at all emails in the inbox (note: this is only allowed to be used in this context because python marks emails as 'read' when it accesses them, …
    #  …and we hard-code just_unread_emails=True in this method so thfat we never read an email twice.)
    return run_as_new_thread(_continuously_scan_gmail_inbox,what_to_do_with_unread_emails,gmail_address,password,max_ↈ_emails,include_old_but_unread_emails)
def _continuously_scan_gmail_inbox(what_to_do_with_unread_emails,gmail_address,password,max_ↈ_emails,include_old_but_unread_emails):
    # This is a helper method because it loops infinitely and is therefore run on a new thread each time.
    exclusive_millis_min=millis()

    # times=[] # ⟵ For debugging. Look at the end of the while loop block to see more.
    while True:
        tic()
        # max_millis=exclusive_millis_min
        for x in gmail_inbox_summary(gmail_address,password,max_ↈ_emails):
            assert isinstance(x,dict)  # x's type is determined by gmail_inbox_summary, which is a blackbox that returns dicts. This assertion is for type-hinting.
            if x['millis'] > exclusive_millis_min or include_old_but_unread_emails:
                #     if x['millis']>max_millis:
                #         max_millis=x['millis']
                what_to_do_with_unread_emails(x)
                # exclusive_millis_min=max_millis

                # times.append(toc())
                # line_graph(times)
                # ptoctic()# UPDATE: It's fine. Original (disproved) thought ﹦ (I don't know why, but the time here just keeps growing and growing...)
# endregion
# region Suppress/Restore all console output/warnings: ［suppress_console_output，restore_console_output，force_suppress_console_output，force_restore_console_output，force_suppress_warnings，force_restore_warnings］
# b=sys.stdout.write;sys.stdout.write=None;sys.stdout.write=b
_original_stdout_write=sys.stdout.write  # ⟵ DO NOT ALTER THIS! It will cause your code to crash.
def _muted_stdout_write(x: str):
    assert isinstance(x,str)  # ⟵ The original method only accepts strings.
    return len(x)  # ⟵ The original method returns the length of the string; I don't know why. '
_console_output_level=1
def suppress_console_output():  # Will turn off ALL console output until restore_console_output() is called.
    global _console_output_level
    _console_output_level-=1
    if _console_output_level < 1:
        sys.stdout.write=_muted_stdout_write
def restore_console_output():  # The antidote for suppress_console_output
    global _console_output_level
    _console_output_level+=1
    if _console_output_level >= 1:
        sys.stdout.write=_original_stdout_write
def force_suppress_console_output():  # Will turn off ALL console output until restore_console_output() is called.
    global _console_output_level
    _console_output_level=0
    sys.stdout.write=_muted_stdout_write
def force_restore_console_output():
    global _console_output_level
    _console_output_level=1
    sys.stdout.write=_original_stdout_write
import warnings
def force_suppress_warnings():
    warnings.filterwarnings("ignore")
def force_restore_warnings():
    warnings.filterwarnings("default")
# def toggle_console_output ⟵ I was going to implement this, but then decided against it: it could get really annoying/confusing if used often.
# endregion
# region Ryan's Inspector: ［rinsp］
def get_bytecode(obj):
    import dis
    return dis.Bytecode(lambda x:x + 1).dis()
_rinsp_temp_object=None
def rinsp(object,search_or_show_documentation:bool=False,show_source_code:bool=False,show_summary: bool = False,max_str_lines: int = 5,*,fansi=fansi) -> None:  # r.inspect
    # This method is really uglily written because I made no attempt to refactor it. But it works and its really useful.
    # search_or_show_documentation: If this is a string, it won't show documentation UNLESS show_source_code ⋁ show_summary. BUT it will limit dir⋃dict to entries that contain search_or_show_documentation. Used for looking up that function name you forgot.

    """
    rinsp report (aka Ryan's Inspection):
    	OBJECT: rinsp(object, show_source_code=False, max_str_lines:int=5)
    	TYPE: class 'function'
    	FROM MODULE: module '__main__' from '/Users/Ryan/PycharmProjects/RyanBStandards_Python3.5/r.py'
    	STR: <function rinsp at 0x109eb10d0>"""
    search_filter=isinstance(search_or_show_documentation,str) and search_or_show_documentation or ''
    if search_filter:
        search_or_show_documentation=False or show_source_code or show_summary
    import inspect as i
    tab='   '
    colour='cyan'
    col=lambda x:fansi(x,colour,'bold')
    ⵁ=col('rinsp report (aka Ryan\'s Inspection):\n' + tab + 'OBJECT: ')
    try:
        ⵁ+=object.__name__
    except Exception as e:
        ⵁ+='[cannot obtain object.__name__ without error: ' + str(e) + ']'
    try:
        ⵁ+=str(i.signature(object))
    except:
        pass
    print(ⵁ)
    try:
        temp=object
        from types import ModuleType
        try:print(col(tab+"LEN: ")+str(len(object)))
        except:pass
        if hasattr(object,'shape'):print(col(tab + "SHAPE: ")+repr(object.shape),flush=False)
        if isinstance(object,ModuleType):
            submodulenames=[x.split('.')[1] for x in get_all_submodule_names(object)]
            if submodulenames:
                print(col(tab + "SUBPACKAGES: ")+(', '.join(submodulenames)),end="\n",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
        try:  # noinspection PyStatementEffect
            object.__dict__
            print(col(tab + "DIR⋃DICT: "),end="",flush=False)
        except:
            temp=type(object)
            print(col(tab + "DIR⋃TYPE.DICT: "),end="",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
        dict_used=set(temp.__dict__)
        dict_used=dict_used.union(set(dir(object)))
        d=dict_used
        if search_filter:
            print(fansi(tab + "FILTERED: ",'yellow','bold'),end="",flush=False)
            d={B for B in d if search_filter in B}
        def sorty(d):
            A=sorted([x for x in d if x.startswith("__") and x.endswith("__")])  # Moving all built-ins and private variables to the end of the list
            B=sorted([x for x in d if x.startswith("_") and not x.startswith("__") and not x.endswith("__")])
            C=sorted(list(set(d) - set(A) - set(B)))
            return C + B + A
        dict_used=sorty(d)
        if len(dict_used) != 0:
            global _rinsp_temp_object
            _rinsp_temp_object=object
            attrs={}
            for attrname in dict_used:
                try:
                    attrs[attrname]=(eval('_rinsp_temp_object.' + attrname))
                except:
                    attrs[attrname]=(fansi("ERROR: Cannot evaluate",'red'))
            def color(attr):
                try:
                    attr=eval('_rinsp_temp_object.' + attr)  # callable(object.__dir__.__get__(attr))
                except:
                    return 'red',None
                if callable(attr):
                    return 'green',  # Green if callable
                return [None]  # Plain and boring if else
            dict_used_with_callables_highlighted_green=[fansi(x,*color(x)) for x in dict_used]
            print_string=(str(len(dict_used)) + ' things: [' + ', '.join(dict_used_with_callables_highlighted_green) + "]")  # Removes all quotes in the list so you can rad ) +" ⨀ ⨀ ⨀ "+str(dict_used).replace("\n","\\n"))
            print_string=print_string.replace('\x1b[0m','')#Make rendering large amounts of commas etc faster (switching between formats seems to make terminal rendering slow and even crashes windows)
            if currently_running_windows():
                print_string=strip_ansi_escapes(print_string)#This is to prevent really slowwww crashes on windows cause windows sucks lol
            print(print_string)
        else:
            print(end="\r")  # Erase the previous line (aka "DICT: " or "TYPE.DICT: ")
    except:
        pass
    def parent_class_names(x,exclude={'object'}):
        #returns a set of strings containing the names of x's parent classes, exclu
        if not isinstance(x,type):
            x=type(x)
        return {y.__name__ for y in x.__bases__}-exclude
    parents=parent_class_names(object)
    parent_string=''
    if parents:
        prefix='PARENT'
        if len(parents)>1:
            prefix+='S'
        parent_string=col(', '+prefix+': ')+', '.join(sorted(parents))
    def get_parent_hierarchy(object):
        from collections import OrderedDict
        # out=OrderedDict()
        out={}
        if not isinstance(object,type):
            object=object.__class__
        for parent in object.__bases__:
            out[parent.__name__]=get_parent_hierarchy(parent)
        return out

    print(col(tab + "PARENT HIERARCHY: ") + repr(get_parent_hierarchy(object)))#This is presenred in an ugly format right now and should eventually replace "parent". But this can be done later.

    print(col(tab + "TYPE: ") + str(type(object))[1:-1]+parent_string)
    if i.getmodule(object) is not None:
        print(col(tab + "FROM MODULE: ") + str(i.getmodule(object))[1:-1])
    def errortext(x):
        return fansi(x,'red','underlined')
    def linerino(x):
        number_of_lines=x.count("\n") + 1
        return '\n'.join(x.split('\n')[:max_str_lines]) + (fansi("\n" + tab + "\t………continues for " + str(number_of_lines - max_str_lines) + " more lines………",colour) if (number_of_lines > max_str_lines + 1) else "")  # max_str_lines+1 instead of just max_str_lines so we dont get '………continues for 1 more lines………'
    try:
        # GETTING CHARACTER FOR TEMP
        def is_module(x):
            import types
            return isinstance(x,types.ModuleType)
        if not is_module(object):
            print(col(tab + "STR: ") + linerino(str(object)))
    except:
        pass
    if show_summary:
        def to_str(x):
            if x is None:
                return str(x)

            outtype='str()'
            out=str(x)
            if out and out[0] == '<' and out[-1] == '>':
                out=x.__doc__
                if out is None:
                    try:
                        out=i.getcomments(object)
                        outtype='doc()'
                    except:
                        out=str(out)
                        outtype='str()'
                else:
                    outtype='doc()'

            typestr=str(type(x))
            if typestr.count("'") >= 2:
                typestr=typestr[typestr.find("'") + 1:]
                typestr=typestr[:typestr.find("'")]
            elif typestr.count('"') >= 2:
                typestr=typestr[typestr.find('"') + 1:]
                typestr=typestr[:typestr.find('"')]

            out=fansi('[' + typestr + " : " + outtype + "]",'green') + " " + fansi(out,'blue')
            if '\n' in out:
                indent_prefix=''  # '···'
                out='\n'.join((indent_prefix + x) for x in out.split('\n'))
                while '\n\n' in out:
                    out=out.replace('\n\n','\n')
                out=linerino(out)
                out=out.lstrip()
                out=out.rstrip()
            return out
        print(col(tab + "SUMMARY:"))
        print_string=display_dict(attrs,print_it=False,key_sorter=sorty,value_color=to_str,arrow_color=lambda x:fansi(x,'green'),key_color=lambda x:fansi(x,'green','bold'),clip_width=True,post_processor=lambda x:'\n'.join(2 * tab + y for y in x.split('\n')))
        if currently_running_windows():
            print_string=strip_ansi_escapes(print_string)#To avoid crashing windows terminals, cut down on the terminal colorings...
        print(print_string)
    if show_source_code:
        print(col(tab + "SOURCE CODE:") + fansi("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――",'cyan','blinking'))
        ⵁ=code_string_with_comments=''
        ⵁ+=i.getcomments(object) or ''  # ≣i.getc omments(object) if i.getcomments(object) is not None else ''
        ⵁ=fansi_syntax_highlighting(ⵁ)
        try:
            try:
                ⵁ+=fansi_syntax_highlighting(str(i.getsource(object)))
            except:
                ⵁ+=fansi_syntax_highlighting(str(i.getsource(object.__class__)))
        except Exception as e:
            ⵁ+=2 * tab + errortext('[Cannot retrieve source code! Error: ' + linerino(str(e)) + "]")
        print(ⵁ)
    if search_or_show_documentation:
        print(col(tab + "DOCUMENTATION: "))
        try:
            if object.__doc__ and not object.__doc__ in ⵁ:
                print(fansi(str(object.__doc__),'gray'))
            else:
                if not object.__doc__:
                    print(2 * tab + errortext("[__doc__ is empty]"))
                else:  # ∴ object.__doc__ in ⵁ
                    print(2 * tab + errortext("[__doc__ can be found in source code, which has already been printed]"))
        except Exception as e:
            print(2 * tab + errortext("[Cannot retrieve __doc__! Error: " + str(e) + "]"))
# endregion
# region Arduino: ［arduino，read_line］
def arduino(baudrate: int = 115200,port_description_keywords:list=['arduino','USB2.0-Serial'],timeout: float = .1,manually_chosen_port: str = None,shutup: bool = False,return_serial_instead_of_read_write=False,marco_polo_timeout=0) -> (callable,callable):# 'USB2.0-Serial' is for a cheap knock-off arduino I got
    #NOTE: This function uses a library called 'serial', got from 'pip install pyserial'.
    #BUT THERE'S A SECOND LIBRARY: 'pip install serial' will give errors, as it's module is also called 'serial'. If you get this error, uninstall 'pip uninstall serial' then 'pip install pyserial'
    # Finds an arduino, connects to it, and returns the read/write methods you use to communicate with it.
    # Example: read,write=arduino()
    # read() ⟵ Returns a single byte (of length 1)
    # write(x:bytes) ⟵ Writes bytes to the arduino, which reads them as individual characters (the 'char' primitive)
    # If you don't want this method to automatically locate an arduino, set manually_chosen_port to the port name you wish to connect to.
    # marco_polo_timeout is optional: It's used for a situation where the arduino responds marco-polo style with the python code
    '''
    //Simple example code for the arduino to go along with this method: It simply parrots back the bytes you write to it.
    void setup()
    {
      Serial.begin(115200);// set the baud rate
    }
    void loop()
    {
      if (Serial.available())// only send data back if data has been sent
      {
        char inByte = Serial.read(); // read the incoming data
        Serial.write(inByte); // send the data back as a single byte.
      }
    }
    '''
    serial=pip_import('serial','pyserial')
    def speak(x: str) -> None:
        if not shutup:
            print("r.arduino: " + x)
    def find_arduino_port(keywords: list = port_description_keywords) -> str:
        # Attempts to automatically determine which port the arduino is on.
        import serial.tools.list_ports
        port_list=serial.tools.list_ports.comports()
        port_descriptions=[port.description for port in port_list]
        keyword_in_port_descriptions=[any(keyword.lower() in port_description.lower()for keyword in keywords) for port_description in port_descriptions]
        number_of_arduinos_detected=sum(keyword_in_port_descriptions)
        assert number_of_arduinos_detected > 0,'r.arduino: No arduinos detected! Port descriptions = ' + str(port_descriptions)
        arduino_port_indices=max_valued_indices(keyword_in_port_descriptions)  # All ports that have 'arduino' in their description.
        if number_of_arduinos_detected > 1:
            speak("Warning: Multiple arduinos detected. Choosing the leftmost of these detected arduino ports: " + str(gather(port_descriptions,arduino_port_indices)))
        chosen_arduino_device=port_list[arduino_port_indices[0]]
        speak("Chosen arduino device: " + chosen_arduino_device.device)
        return chosen_arduino_device.device
    ser=serial.Serial(manually_chosen_port or find_arduino_port(),baudrate=baudrate,timeout=timeout)  # Establish the connection on a specific port. NOTE: manually_chosen_port or find_arduino_port() ≣ manually_chosen_port if manually_chosen_port is not None else find_arduino_port()
    if return_serial_instead_of_read_write:
        return ser
    read_bytes,_write_bytes=ser.read,ser.write  # NOTE: If read_bytes()==b'', then there is nothing to read at the moment.
    def write_bytes(x,new_line=False):
        _write_bytes(printed((x if isinstance(x,bytes) else str(x).encode())+(b'\n'if new_line else b'')))
    start=tic()
    # (next 4 lines) Make sure that the arduino is able to accept write commands before we release it into the wild (the return function):
    arbitrary_bytes=b'_'  # It doesn't matter what this is, as long as it's not empty
    assert arbitrary_bytes != b''  # ⟵ This is the only requirement for that read_bytes must be.
    if marco_polo_timeout:
        while not read_bytes() and start()<marco_polo_timeout: write_bytes(arbitrary_bytes)  # ≣ while read_bytes()==b''
        while read_bytes() and start()<marco_polo_timeout: pass  # ≣ while read_bytes()!=b''. Basically the idea is to clear the buffer so it's primed and ready-to-go as soon as we return it.
        if start()>marco_polo_timeout and not shutup:
            print("Marco Polo Timed Out")
    speak("Connection successful! Returning read and write methods.")
    return read_bytes,write_bytes  # Returns the methods that you use to read and write from the arduino
    # NOTE: read_bytes() returns 1 byte; but read_byte(n ∈ ℤ) returns n bytes (all in one byte―string)!
    # Future: Possibly helpful resources: http://stackoverflow.com/questions/24420246/c-function-to-convert-float-to-byte-array  ⨀ ⨀ ⨀   http://forum.arduino.cc/index.php?topic=43222.0
def read_line(getCharFunction,return_on_blank=False) -> bytes:
    # Example: read,write=arduino();print(read_line(read))
    f=getCharFunction
    t=tic()
    o=b''
    while True:
        n=new=f()
        if n == b'\n' or return_on_blank and n == b'':
            return o
        o+=n
# endregion
# region Webcam: ［load_image_from_webcam, load_image_from_webcam_in_jupyter_notebook］
_cameras=[]
def _initialize_cameras():
    if _cameras:
        return  # Allready initialized
    fansi_print("r._initialize_cameras: Initializing camera feeds; this will take a few seconds...",'green',new_line=False)
    # noinspection PyUnresolvedReferences
    pip_import('cv2')
    from cv2 import VideoCapture
    i=0
    while True:
        cam=VideoCapture(i)
        if not cam.read()[0]:
            break
        _cameras.append(cam)
        fansi_print("\rr._initialize_cameras: Added camera #" + str(i),'green',new_line=False)
        i+=1
    fansi_print("\rr._initialize_cameras: Initialization complete!",'green')
def load_image_from_webcam(webcam_index: int = 0,shutup=False):
    if running_in_google_colab():return _load_image_from_webcam_in_jupyter_notebook()
    # Change webcam_index if you have multiple cameras
    # EX: while True: display_image(med_filter(load_image_from_webcam(1),σ=0));sleep(0);clf()#⟵ Constant webcam display
    _initialize_cameras()
    # _,img=_cameras[webcam_index].read()
    # if webcam_index>=_cameras.__len__():
    #     if not shutup:
    #         print("r.load_image_from_webcam: Warning: Index is out of range: webcam_index="+str(webcam_index)+" BUT len(_cameras)=="+str(len(_cameras))+", setting webcam_index to 0")
    #     webcam_index=0
    img=np.add(_cameras[webcam_index].read()[1],0)  # Turns it into numpy array
    img=np.add(img,0)  # Turns it into numpy array
    x=img + 0  # Making it unique/doesnt mutate img
    img[:,:,0],img[:,:,2]=x[:,:,2],x[:,:,0]

    return img

def load_image_from_screenshot():
    #Take a screeshot, and return the result as a numpy-array-style image
    #EXAMPLE: display_image(load_image_from_screenshot())
    #TODO: Make this faster. the 'mss' package from pypi got much better performance, so if you need higher FPS try using that for the inner workings of this function.
    pyscreenshot=pip_import('pyscreenshot')
    im = pyscreenshot.grab(childprocess=False)
    return np.asarray(im)

def _load_image_from_webcam_in_jupyter_notebook():
    from IPython.display import HTML, Image
    from google.colab.output import eval_js
    from base64 import b64decode

    VIDEO_HTML = """
    <video autoplay
     width=800 height=600></video>
    <script>
    var video = document.querySelector('video')
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream=> video.srcObject = stream)

    var data = new Promise(resolve=>{
      video.onclick = ()=>{
        var canvas = document.createElement('canvas')
        var [w,h] = [video.offsetWidth, video.offsetHeight]
        canvas.width = w
        canvas.height = h
        canvas.getContext('2d')
              .drawImage(video, 0, 0, w, h)
        video.srcObject.getVideoTracks()[0].stop()
        video.replaceWith(canvas)
        resolve(canvas.toDataURL('image/jpeg', %f))
      }
    })
    </script>
    """
    def take_photo(filename='photo.jpg', quality=0.8):
      display(HTML(VIDEO_HTML % quality))
      data = eval_js("data")
      binary = b64decode(data.split(',')[1])
      with open(filename, 'wb') as f:
        f.write(binary)
      return len(binary)
# endregion
# region  Audio Recording: ［record_mono_audio］
Đ_audio_stream_chunk_size=1024  # chunk_size determines the resolution of time_in_seconds as the samplerate. Look in the code for more explanation idk how to describe it.
Đ_audio_mono_input_stream=None  # Initialized in the record_mono_audio function
def record_mono_audio(time_in_seconds,samplerate=Đ_samplerate,stream=None,chunk_size=Đ_audio_stream_chunk_size) :
    # You can count on this method having a delay (between when you call the method and when it actually starts recording) on the order of magnitude of 10⁻⁵ seconds
    # PLEASE NOTE: time_in_seconds is not interpreted precisely
    # EXAMPLE: play_sound_from_samples(record_mono_audio(2))
    pip_import('pyaudio')
    if stream is None:  # then use Đ_audio_mono_input_stream instead
        global Đ_audio_mono_input_stream
        if Đ_audio_mono_input_stream is None:  # Initialize it.
            import pyaudio  # You need this module to use this function. Download it if you don't have it.
            Đ_audio_mono_input_stream=pyaudio.PyAudio().open(format=pyaudio.paInt16,channels=1,rate=Đ_samplerate,input=True,frames_per_buffer=Đ_audio_stream_chunk_size)
        stream=Đ_audio_mono_input_stream
    number_of_chunks_needed=np.ceil(time_in_seconds * samplerate / chunk_size)  # Rounding up.
    out=np.hstack([np.fromstring(stream.read(num_frames=chunk_size,exception_on_overflow=False),dtype=np.int16) for _ in [None] * int(number_of_chunks_needed)])  # Record the audio
    out=np.ndarray.astype(out,float)  # Because by default it's an integer (not a floating point thing)
    out/=2 ** 15  # ⟹ ∈［﹣1，1］ because we use pyaudio.paInt16. I confirmed this by banging on the speaker loudly and seeing 32743.0 as the max observed value.  ﹙# out/=max([max(out),-min(out)]) ⟵ originally this﹚
    # stream.stop_stream();stream.close() ⟵ Is slow. Takes like .1 seconds. I profiled this method so that it runs very, very quickly (response time is about a 1% of a millisecond)
    return out
# endregion
# region MIDI Input/Output: ［MIDI_input，MIDI_output］
__midiout=None
def MIDI_output(message: list):
    """
    Key:
    NOTE_OFF = [0x80, note, velocity]
    NOTE_ON = [0x90, note, velocity]
    POLYPHONIC_PRESSURE = [0xA0, note, velocity]
    CONTROLLER_CHANGE = [0xB0, controller, value]
    PROGRAM_CHANGE = [0xC0, program]
    CHANNEL_PRESSURE = [0xD0, pressure]
    PITCH_BEND = [0xE0, value-lo, value-hi]
    For more: see http://pydoc.net/Python/python-rtmidi/0.4.3b1/rtmidi.midiconstants/
    """
    pip_import('rtmidi')
    try:
        # Can control applications like FL Studio etc
        # Use this for arduino etc
        global __midiout
        if not __midiout:
            import rtmidi  # pip3 install python-rtmidi
            __midiout=rtmidi.RtMidiOut()
            try:
                available_ports=__midiout.get_ports()
            except AttributeError:#AttributeError: 'midi.RtMidiOut' object has no attribute 'get_ports': See https://stackoverflow.com/questions/38166344/attributeerror-in-python-rtmidi-sample-code
                available_ports=__midiout.ports
            if available_ports:
                __midiout.open_port(0)
                print("r.MIDI_output: Port Output Name: '" + __midiout.get_ports()[0])
            else:
                __midiout.open_virtual_port("My virtual output")
        __midiout.send_message(message)  # EXAMPLE MESSGES: # note_on = [0x90, 98, 20] # channel 1, middle C, velocity 112   note_off = [0x80, 98, 0]
    except OverflowError as e:
        fansi_print("ERROR: r.MIDI_Output: " + str(e) + ": ",'red',new_line=False)
        fansi_print(message,'cyan')
def MIDI_control(controller_number: int,value: float):  # Controller_number is custom integer, and value is between 0 and 1
    MIDI_output([176,controller_number,int(float_clamp(value,0,1) * 127)])
def MIDI_control_precisely(coarse_controller_number: int,fine_controller_number: int,value: float):  # TWO bytes of data!!
    value=float_clamp(value,0,1)
    value*=127
    MIDI_output([176,coarse_controller_number,int(value)])
    MIDI_output([176,fine_controller_number,int((value % 1) * 127)])
def MIDI_jiggle_control(controller_number: int):  # Controller_number is custom integer, and value is between 0 and 1
    MIDI_control(controller_number,0)
    sleep(.1)
    MIDI_control(controller_number,1)
def MIDI_note_on(note: int,velocity: float = 1):  # velocity ∈ ［0，1］
    MIDI_output([144,int_clamp(note,0,255),int(velocity * 127)])  # Notes can only be between 0 and 255, inclusively
def MIDI_note_off(note: int,velocity: float = 0):
    MIDI_output([128,note,int(velocity * 127)])
MIDI_pitch_bend_min=-2  # Measured in Δsemitones.
MIDI_pitch_bend_max=6  # Note: These min/max numbers are Based on the limitations of the pitch bender, which is DAW dependent. This is what it appears to be in FL Studio on my computer. Note that these settings
def MIDI_pitch_bend(Δsemitones: float):  # Δsemitones ∈ [-2,6] ⟵ ACCORDING TO FL STUDIO
    Δsemitones=float_clamp(Δsemitones,MIDI_pitch_bend_min,MIDI_pitch_bend_max)
    coarse=int(((Δsemitones + 2) / 8) * 255)
    fine=0  # ∈ [0,255] Note that fine is...REALLY REALLY FINE...So much so that I can't really figure out a good way to use it
    MIDI_output([224,fine,coarse])
def MIDI_all_notes_off():
    for n in range(256):
        MIDI_note_off(n)
def MIDI_breath(value: float):
    MIDI_output([0x02,int(float_clamp(value,0,1) * 127)])
#
__midiin=None  # This variable exists so the garbage collector doesn't gobble up your midi input if you decide not to assign a variable to the output (aka the close method)
def MIDI_input(ƒ_callback: callable = print) -> callable:
    # Perfect example:
    # close_midi=MIDI_input(MIDI_output) # ⟵ This simply regurgitates the midi-piano's input to a virtual output. You won't be able to tell the difference ;)
    # Then, when you're bored of it...
    # close_midi()# ⟵ This stops the midi from doing anything.
    print("r.MIDI_input: Please specify the details of your request:")
    pip_import('rtmidi')
    from rtmidi.midiutil import open_midiport  # pip3 install python-rtmidi
    global __midiin
    __midiin,port_name=open_midiport()
    __midiin.set_callback(lambda x,y:ƒ_callback(x[0]))
    return __midiin.close_port  # Returns the method needed to kill the thread
# endregion
# region  Comparators: ［cmp_to_key，sign］
def cmp_to_key(mycmp):
    # From: http://code.activestate.com/recipes/576653-convert-a-cmp-function-to-a-key-function/
    # Must use for custom comparators in the 'sorted' builtin function!
    # Instead of using sorted(ⵁ,cmp=x) which gives syntax error, use…
    # …sorted(ⵁ,key=cmp_to_key(x))
    # I.E., in rCode:
    #       sorted(ⵁ,cmp=x) ⭆ sorted(ⵁ,key=cmp_to_key(x))   ≣   cmp=x ⭆ key=cmp_to_key(x)
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self,obj,*args): self.obj=obj
        def __lt__(self,other): return mycmp(self.obj,other.obj) < 0
        def __gt__(self,other): return mycmp(self.obj,other.obj) > 0
        def __eq__(self,other): return mycmp(self.obj,other.obj) == 0
        def __le__(self,other): return mycmp(self.obj,other.obj) <= 0
        def __ge__(self,other): return mycmp(self.obj,other.obj) >= 0
        def __ne__(self,other): return mycmp(self.obj,other.obj) != 0
    return K


    # noinspection PyShadowingNames
def sign(x,zero=0):
    # You can redefine zero depending on the context. It basically becomes a comparator.
    if x > zero:
        return 1
    elif x < zero:
        return -1
    return zero
# endregion
# region  Pickling:［load_pickled_value，save_pickled_value］
import pickle
# Pickling is just a weird name the python devs came up with to descript putting the values of variables into files, essentially 'pickling' them for later use
def load_pickled_value(file_name: str):
    # Filenames are relative to the current file path
    pickle.load(open(file_name,"rb"))
def save_pickled_value(file_name: str,*variables):
    # Filenames are relative to the current file path
    pickle.dump(detuple(variables),open(file_name,'wb'))
    # load_pickled_value=lambda file_name:pickle.load(open(file_name,"rb"))
# endregion
# region  .txt ⟷ str: ［string_to_text_file，text_file_to_string］
def string_to_text_file(file_path: str,string: str,) -> None:
    file=open(file_path,"w")
    try:
        file.write(string)
    except:
        file=open(file_path,"w",encoding='utf-8')
        file.write(string,)

    file.close()
def text_file_to_string(file_path: str) -> str:
    # file=open(file_path,"r")
    # try:
    #     return file.read()
    # except Exception as e:
    #     print_stack_trace()
    # finally:
    #     file.close()
    return open(file_path).read()
# endregion
# region MATLAB Integration: ［matlab_session，matlab，matlab_pseudo_terminal］
def matlab_session(matlabroot: str = '/Applications/MATLAB_R2016a.app/bin/matlab',print_matlab_stdout: bool = True):  # PLEASE NOTE: this 'matlabroot' was created on my Macbook Pro, and is unlikely to work on your computer unless you specify your own matlab path!
    # This method is used as an easy-to-use wrapper for creating MATLAB sessions using the pymatbridge module
    # Worth noting: There's a legit purpose for creating a new matlab session before using it:
    #   Each session you create will be separate and will have a separate namespace!
    #   In other words, you can run them simultaneously/separately. For example:
    #         ⮤ sess1=matlab_session();sess2=matlab_session();
    #         ⮤ sess1.run_code("x=1");sess2.run_code("x=1");
    #         ⮤ sess1.get_variable("x"),sess2.get_variable("x")
    #         ans=(1,2)
    # Also worth noting: You can use whatever functions you normally use in MATLAB, including .m files that you wrote and kept in your default matlab function/script saving directory.
    fansi_print("(A message from Ryan): About to try connecting to MATLAB. Please be a patient, this can take a few seconds! (There is a timeout though, so you won't be kept waiting forever if it fails). Another message will be printed when it's done loading.",None,'bold')
    pip_import('pymatbridge')
    import pymatbridge  # pip3 install pymatbridge     (see https://arokem.github.io/python-matlab-bridge/ )
    session=pymatbridge.Matlab(executable=matlabroot,maxtime=60)  # maxtime=60⟹Wait 1 minute to get a connection before timing out. I got this 'matlabroot' parameter by running "matlabroot" ﹙without quotes﹚in my Matlab IDE (and copy/pasting the output)
    session.start()  # If wait_for_matlab_to_load is true, then this method won't return anything until it'_s made a connection, which will time out if it takes more than max_loading_time_before_giving_up_in_seconds seconds.
    assert session.is_connected(),'(A message from Ryan): MATLAB failed to connect! (So we gotta stop here). I made this assertion error to prevent any further confusion if you try to write methods that use me. If I get too annoying, feel free to delete me (the assertion). \n' \
                                  'Troubleshooting: Perhaps the path you specified in the "matlabroot" argument of this method isn\'t really your matlab root? See the comments in this method for further information.'

    print_matlab_stdout=[print_matlab_stdout]  # Turn the value into a list make it mutable
    def handle_matlab_stdout(x: dict):
        # x will look something like this: ans = {'result': [], 'success': True, 'content': {'datadir': '/private/tmp/MatlabData/', 'stdout': 'a =\n     5\n', 'figures': []}}
        nonlocal print_matlab_stdout
        is_error=not x['success']  # Is a boolean.
        if print_matlab_stdout[0]:
            if is_error:
                fansi_print("MATLAB ERROR: ",'red','bold',new_line=False)
            fansi_print(x['content']['stdout'],'red' if is_error else'gray')
        else:
            return x  # If we're not printing out the output, we give them ALL the data
    def wrapper(code: str = '',**assignments):
        assert isinstance(code,str),'The "Code" parameter should always be a string. If you wish to assign values to variables in the MATLAB namespace, use this method\'_s kwargs instead.'
        assert len(assignments) == 1 or not assignments,'Either one variable assignment or no variable assignments.'
        assert not (code and assignments),'You should either use this method as a way to get values/execute code, XOR to assign variables to non-strings like numpy arrays. NOT both! That could be very confusing to read, and make it difficult for new people to learn how to use this function of the r class. NOTE: This method limits you to a single variable assignment because sessions returns things when you do that, and this wrapper has to return that output. '
        # Note that code and va can be used like booleans, because we know that code is a string and we know that va is a dict that has string-based keys (because of the nature of kwargs).
        nonlocal session,handle_matlab_stdout
        if code:
            eval_attempt=session.get_variable(code)
            return handle_matlab_stdout(session.run_code(code)) if eval_attempt is None else eval_attempt  # If eval_attempt is None, it means MATLAB didn't return a value for the code you gave it (like saying disp('Hello World')), or resulted in an error or something (like saying a=1/0).
        if assignments:
            for var_name in assignments:
                return handle_matlab_stdout(session.set_variable(var_name,assignments[var_name]))
        return session  # If we receive no arguments, return the raw session (generated by the pymatbridge module).

    session.print_matlab_stdout=[print_matlab_stdout]  # A list to make it mutable
    def enable_stdout():  # Enables the pseudo-matlab to print out, on the python console, what a real matlab would print.
        nonlocal print_matlab_stdout
        print_matlab_stdout[0]=True
    def disable_stdout():
        nonlocal print_matlab_stdout
        print_matlab_stdout[0]=False
    wrapper.disable_stdout=disable_stdout
    wrapper.enable_stdout=enable_stdout
    wrapper.reboot=lambda *_:[fansi_print("Rebooting this MATLAB session...",None,'bold'),session.stop(),session.start(),fansi_print("...reboot complete!",None,'bold')] and None  # wrapper.reboot() in case you accidentally call an infinite loop or something
    wrapper.stop=session.stop  # I put this here explicitly, so you don't have to hunt around before figuring out that wrapper().stop() does the same thing as (what now is) wrapper.stop()
    wrapper.start=session.start  # This exists for the same reason that the one above it exists.

    return wrapper

_static_matlab_session=matlab_disable_stdout=matlab_enable_stdout=matlab_reboot=matlab_stop=matlab_start=None  # Should be None by default. This is the default Matlab session, which is kept in the r module.
# noinspection PyUnresolvedReferences
def _initialize_static_matlab_session():
    global _static_matlab_session,matlab_disable_stdout,matlab_enable_stdout,matlab_reboot,matlab_stop,matlab_start
    _static_matlab_session=matlab_session()
    matlab_disable_stdout=_static_matlab_session.disable_stdout
    matlab_enable_stdout=_static_matlab_session.enable_stdout
    matlab_reboot=_static_matlab_session.reboot
    matlab_stop=_static_matlab_session.stop
    matlab_start=_static_matlab_session.start
# noinspection PyUnresolvedReferences
def matlab(*code,**assignments):  # Please note: you can create simultaneous MATLAB sessions by using the matlab_session method!
    # This method seriously bends over-back to make using matlab in python more convenient. You don't even have to create a new session when using this method, it takes care of that for you ya lazy bastard! (Talking about myself apparently...)
    global _static_matlab_session,matlab_disable_stdout,matlab_enable_stdout,matlab_reboot,matlab_stop,matlab_start
    if _static_matlab_session is None:
        fansi_print("r.matlab: Initializing the static matlab session...",None,'bold')
        _initialize_static_matlab_session()
    return _static_matlab_session(*code,**assignments)

def matlab_pseudo_terminal(pseudo_terminal):  # Gives a flavour to a given pseudo_terminal function
    # Example usage: matlab_pseudo_terminal(pseudo_terminal)
    _initialize_static_matlab_session()
    pseudo_terminal("pseudo_terminal() ⟹ Entering interactive MATLAB console! (Running inside of the 'r' module)",lambda x:"matlab('" + x + "')")
# endregion
# region Mini-Terminal: ［mini_terminal:str］
# PLEASE READ: This is not meant to be called from the r class.
# Example usage: import r;exec(r.mini_terminal)
# Intended for use everywhere; including inside other functions (places with variables that pseudo_terminal can't reach)
mini_terminal="""#from r import fansi,fansi_print,string_from_clipboard,fansi_syntax_highlighting
_history=[]
fansi_print("Ryan's Mini-Terminal: A miniature pseudo-terminal for running inside functions!",'blue','bold')
fansi_print("\\tValid commands: ［PASTE，END，HISTORY］",'blue')
while True:
    try:
        _header="--> "
        _s=input(fansi(_header,'cyan','bold')).replace(_header,"").lstrip()
        if not _s:
            continue
        if _s == "PASTE":
            fansi_print("PASTE ⟶ Entering command from clipboard",'blue')
            _s=string_from_clipboard
        if _s == 'END':
            fansi_print("END ⟶ Ending mini-terminal session",'blue')
            break
        elif _s == 'HISTORY':
            fansi_print("HISTORY ⟶ Printing out list of commands you entered that didn't cause errors",'blue')
            fansi_print(fansi_syntax_highlighting('\\n'.join(_history)))
        else:
            try:
                _temp=eval(_s)
                if _temp is not None:
                    _ans=_temp
                    fansi_print('_ans = ' + str(_ans),'green')
                _history.append(_s)
            except:
                try:
                    exec(_s)
                    _history.append(_s)
                except Exception as _error:
                    print(fansi("ERROR: ",'red','bold') + fansi(_error,'red'))
    except KeyboardInterrupt:
        print("Miniterminal: Caught keyboard interrupt (type END to exit)")
"""
# endregion
# region socketWrapper: ［socket_writer，socket_reader，socket_read，socket_write，socket_reading_thread，get_my_ip］
Đ_socket_port=13000
_socket_writers={}# A whole bunch of singletons
def socket_writer(targetIP: str,port: int = None):
    if (targetIP,port) in _socket_writers:
        return _socket_writers[(targetIP,port)]
    from socket import AF_INET,SOCK_DGRAM,socket
    # Message Sender
    host=targetIP  # IP address of target computer. Find yours with print_my_ip
    port=port or Đ_socket_port
    addr=(host,port)
    UDPSock=socket(AF_INET,SOCK_DGRAM)  # UDPSock.close()
    def write(asciiData: str):
        UDPSock.sendto(str(asciiData).encode("ascii"),addr)
    write.targetIP=targetIP# A bit of decorating...
    write.port=port# A bit of decorating...
    _socket_writers[(targetIP,port)]=write
    assert socket_writer(targetIP,port) is write  # Should have been added to _socket_writers
    return write
def socket_write(targetIP,port,message):
    socket_writer(targetIP,port)(message)# Takes advantage of the singleton structure of _socket_writers
_socket_readers={}# A whole bunch of singletons
def socket_reader(port: int = None):# Blocks current thread until it gets a response
    if port in _socket_readers:
        return _socket_readers[port]
    # Message Receiver
    from socket import AF_INET,socket,SOCK_DGRAM
    host=""
    port=port or Đ_socket_port
    buf=1024
    addr=(host,port)
    UDPSock=socket(AF_INET,SOCK_DGRAM)  # UDPSock.close()
    UDPSock.bind(addr)
    # UDPSock.close()
    def read(just_data_if_true_else_tuple_with_data_then_ip_addr:bool=True):
        data,addr=UDPSock.recvfrom(buf)
        data=data.decode("ascii")
        return data if just_data_if_true_else_tuple_with_data_then_ip_addr else (data,addr[0])# addr[0] is a string for ip. addr=tuple(string,int)
    read.port=port# A bit of decorating
    _socket_readers[port]=read
    assert socket_reader(port) is read
    return read
def socket_read(port,just_data_if_true_else_tuple_with_data_then_ip_addr:bool=True):
    return socket_reader(port)(just_data_if_true_else_tuple_with_data_then_ip_addr) # Takes advantage of the singleton structure of _socket_readers
def socket_reading_thread(handler,port:int=None,just_data_if_true_else_tuple_with_data_then_ip_addr:bool=True):
    read=socket_reader(port)
    def go():
        while True:
            handler(read(just_data_if_true_else_tuple_with_data_then_ip_addr=just_data_if_true_else_tuple_with_data_then_ip_addr))
    return run_as_new_thread(go)
def get_my_ip() -> str:
    import socket
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    try:
        return s.getsockname()[0]
    finally:
        s.close()
# endregion
# region OSC≣'Open Sound Control' Output ［OSC_output］:
Đ_OSC_port=12345
try:Đ_OSC_ip=get_my_ip()
except:pass
_OSC_client=None# This is a singleton
_OSC_values={}
def OSC_output(address,value):
    address=str(address)
    if not address[0]=='/':
        address='/'+address
    global Đ_OSC_ip
    Đ_OSC_ip=Đ_OSC_ip or get_my_ip()
    from rp.TestOSC import SimpleUDPClient
    global _OSC_client
    if not _OSC_client:
        _OSC_client=SimpleUDPClient(address=Đ_OSC_ip,port=Đ_OSC_port)
    _OSC_client.send_message(address=address,value=value)
    _OSC_values[address]=value# Attempt to keep track of them (though it might sometimes drift out of sync etc idk i haven't tested it as of writing this)
def OSC_jiggle(address):
    address=str(address)
    if address in _OSC_values:
        original_value=_OSC_values[address]
    OSC_output(address,1)
    sleep(.1)
    OSC_output(address,0)
    sleep(.1)
    if address in _OSC_values:
        # noinspection PyUnboundLocalVariable
        OSC_output(address,original_value)
# endregion
# Intended for use everywhere; including inside other functions (places with variables that pseudo_terminal can't reach)
mini_terminal_for_pythonista="""
_history=[]
print("Ryan's Mini-Terminal For Pythonista: A microscopic pseudo-terminal for running inside functions; optimized for Pythonista!")
print("\\tValid commands: ［PASTE，END，HISTORY］")
while True:
    _header=">>> "
    _s=input(_header).replace(_header,"").lstrip()
    if not _s:
        continue
    if _s == "PASTE":
        import clipboard
        print("PASTE: Entering command from clipboard",'blue')
        _s=clipboard.get()
    if _s == 'END':
        print("END: Ending mini-terminal session",'blue')
        break
    elif _s == 'HISTORY':
        print("HISTORY: Printing out list of commands you entered that didn't cause errors",'blue')
        print('\\n'.join(_history))
    else:
        try:
            _temp=eval(_s)
            if _temp is not None:
                _=_temp
                print('_ = ' + str(_))
            _history.append(_s)
        except:
            try:
                exec(_s)
                _history.append(_s)
            except BaseException as _error:
                print("ERROR: " + str(_error))"""
# endregion
# Other stuff I don't know which category to put in:
def k_means_analysis(data_vectors,k_or_initial_centroids,iterations,tries):
    pip_import('scipy')
    from scipy.cluster.vq import kmeans,vq
    centroids,total_distortion=kmeans(obs=data_vectors,k_or_guess=k_or_initial_centroids,iter=iterations)  # [0] returns a list of the centers of the means of each centroid. TRUE. [1] returns the 'distortion' ＝ ∑||𝓍﹣μ(𝓍ʹs cluster)||² ＝ the sum of the squared distances between each point and it's respective cluster's mean
    for _ in range(tries - 1):
        proposed_centroids,proposed_total_distortion=kmeans(obs=data_vectors,k_or_guess=k_or_initial_centroids,iter=iterations)
        if proposed_total_distortion < total_distortion:
            total_distortion=proposed_total_distortion
            centroids=proposed_centroids
    parent_centroid_indexes,parent_centroid_distances=vq(data_vectors,centroids)  # ⟵ assign each sample to a cluster
    # The rCode Identities section should answer most questions you may have about this def.
    # rCode Identities: Let c≣centroids  ⋀  i≣parent_centroid_indexes  ⋀  d≣parent_centroid_distances …
    # … ⋀  v≣data_vectors  ⋀  dist(a,b)≣﹙the euclidean distance between vectors a and b﹚  ⋀  k≣k_or_initial_centroids
    #   ∴ len(v) == len(i) == len(d)
    #   ∴ ∀ 𝓍 ∈ i， d[𝓍] == dist(v[𝓍],c[𝓍])
    #   ∴ total_distortion == ∑d²
    #   ∴ len(c) == k ⨁ len(c) == len(k)
    return centroids,total_distortion,parent_centroid_indexes,parent_centroid_distances
def is_iterable(x):
    try:
        for _ in x: pass
        return True
    except:
        return False
def space_split(x: str) -> list:
    return list(filter(lambda y:y != '',x.split(" ")))  # Splits things by spaces but doesn't allow empty parts
def deepcopy_multiply(iterable,factor: int):
    # Used for multiplying lists without copying their addresses
    out=[]
    from copy import deepcopy
    for i in range(factor):
        out+=deepcopy(iterable)
    return out
def assert_equality(*args,equality_check=identity):
    # When you have a,b,c,d and e and they're all equal and you just can't choose...when the symmetry is just too much symmetry!
    # PLEASE NOTE: This does not check every combination: it assumes that equality_check is symmetric!
    length=len(args)
    if length == 0:
        return None
    base=args[0]
    if length == 1:
        return base
    for arg in args:
        base_check=equality_check(base)
        arg_check=equality_check(arg)
        assert (base_check == arg_check)," assert_equality check failed, because " + str(base_check) + " ≠ " + str(arg_check)
        base=arg
    return base
def get_nested_value(list_to_be_accessed,*address_int_list,ignore_errors: bool = False):
    # Needs to be better documented. ignore_errors will simply stop tunneling through the array if it gets an error and return the latest value created.
    # Also note: this could con
    # a[b][c][d] ≣ get_nested_value(a,b,c,d)
    for i in detuple(address_int_list):
        try:
            list_to_be_accessed=list_to_be_accessed[i]
        except:
            if ignore_errors:
                break
            else:
                raise IndexError
    return list_to_be_accessed
def shell_command(command: str,as_subprocess=False,return_printed_stuff_as_string: bool = True) -> str or None:
    # region OLD VERSION: had an argument called return_printed_stuff_as_string, which I never really used as False, and run_as_subprocess when True might not return a string anyay. If I recall correctly, I implemented return_printed_stuff_as_string simply because it was sometimes annoying to see the output when using pseudo_terminal
    #       def shell_command(command: str,return_printed_stuff_as_string: bool = True,run_as_subprocess=False) -> str or None:
    #           if return_printed_stuff_as_string:
    #               return (lambda ans:ans[ans.find('\n') + 1:][::-1])(os.popen(command).read()[::-1])  # EX: print(shell_command("pwd")) <-- Gets the current directory
    #           from os import system
    #           system(command)
    # endregion
    if as_subprocess:
        from subprocess import run
        if return_printed_stuff_as_string:
            stdout=run(command,shell=True).stdout
            if stdout is not None:
                return (lambda ans:ans[ans.find('\n') + 1:][::-1])(stdout[::-1])  # EX: print(shell_command("pwd")) <-- Gets the current directory
        else:
            run(command)
    else:
        if return_printed_stuff_as_string:
            return (lambda ans:ans[ans.find('\n') + 1:][::-1])(os.popen(command).read()[::-1])  # EX: print(shell_command("pwd")) <-- Gets the current directory
        else:
            from os import system
            system(command)
def printed(message,value_to_be_returned=None,end='\n'):  # For debugging...perhaps this is obsolete now that I have pseudo_terminal though.
    print(str(value_to_be_returned if value_to_be_returned is not None else message),end=end)
    return value_to_be_returned or message
def blob_coords(image,small_end_radius=10,big_start_radius=50):
    #TODO: wtf is this? lollll should I delete it?
    # small_end_radius is the 'wholeness' that we look for. Without it we might-as-well pickthe global max pixel we start with, which is kinda junky.
    assert big_start_radius >= small_end_radius
    if len(image.shape) == 3:
        image=tofloat(rgb_to_grayscale(image))
    def global_max(image):
        # Finds max-valued coordinates. Randomly chooses if multiple equal maximums. Assumes image is SINGLE CHANNEL!!
        assert isinstance(image,np.ndarray)
        assert len(image.shape) == 2  # SHOULD BE SINGLE CHANNEL!!
        return random_element(np.transpose(np.where(image == image.max()))).tolist()
    def get(x,y):
        try:
            return image[x,y]
        except IndexError:
            return 0
    def local_max(image,x0,y0):
        # Gradient ascent pixel-wise. Assumes image is SINGLE CHANNEL!!
        assert isinstance(image,np.ndarray)
        assert len(image.shape) == 2  # SHOULD BE SINGLE CHANNEL!!
        def get(x,y):
            try:
                return image[x,y]
            except IndexError:
                return 0
        def step(x,y):  # A single gradient ascent step
            best_val=0  # We're aiming to maximize this
            best_x=x
            best_y=y
            for Δx in [-1,0,1]:
                for Δy in [-1,0,1]:
                    if get(x + Δx,y + Δy) > best_val:
                        best_val=get(x + Δx,y + Δy)
                        best_x,best_y=x + Δx,y + Δy
            return best_x,best_y
        while step(x0,y0) != (x0,y0):
            x0,y0=step(x0,y0)
        return x0,y0
    # image is now a single channel.
    def blurred(radius):
        return gauss_blur(image,radius,single_channel=True)  # ,mode='constant')
    x,y=global_max(blurred(big_start_radius))
    for r in reversed(range(small_end_radius,big_start_radius)):
        x,y=local_max(blurred(r + 1),x,y)
    return x,y
def tofloat(ndarray):
    # Things like np.int16 or np.int64 will all be scaled down by their max values; resulting in
    # elements that in sound files would be floats ∈ [-1,1] and in images [0,255] ⟶ [0-1]
    return np.ndarray.astype(ndarray,float) / np.iinfo(ndarray.dtype).max

def _get_plt():
    pip_import('matplotlib')
    global plt
    import matplotlib.pyplot as plt
    locals()['plt']=plt
    return plt


def display_dot(x,y,color='red',size=3,shape='o',block=False):
    #Used to be called 'dot', in-case any of my old code breaks...
    #EXAMPLE: for theta in np.linspace(0,tau): display_dot(np.sin(theta),np.cos(theta));sleep(.1)
    plt=_get_plt()
    plt.plot([x],[y],marker=shape,markersize=size,color=color)
    plt.show(block=block)
    if not block:
        plt.pause(0.0001)
def translate(to_translate,to_language="auto",from_language="auto"):
    # I DID NOT WRITE THIS!! I GOT IT FROM https://github.com/mouuff/mtranslate/blob/master/mtranslate/core.py
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?
    """

    LANGUAGES={
            'af'    :'Afrikaans',
            'sq'    :'Albanian',
            'ar'    :'Arabic',
            'hy'    :'Armenian',
            'bn'    :'Bengali',
            'ca'    :'Catalan',
            'zh'    :'Chinese',
            'zh-cn' :'Chinese (Mandarin/China)',
            'zh-tw' :'Chinese (Mandarin/Taiwan)',
            'zh-yue':'Chinese (Cantonese)',
            'hr'    :'Croatian',
            'cs'    :'Czech',
            'da'    :'Danish',
            'nl'    :'Dutch',
            'en'    :'English',
            'en-au' :'English (Australia)',
            'en-uk' :'English (United Kingdom)',
            'en-us' :'English (United States)',
            'eo'    :'Esperanto',
            'fi'    :'Finnish',
            'fr'    :'French',
            'de'    :'German',
            'el'    :'Greek',
            'hi'    :'Hindi',
            'hu'    :'Hungarian',
            'is'    :'Icelandic',
            'id'    :'Indonesian',
            'it'    :'Italian',
            'ja'    :'Japanese',
            'ko'    :'Korean',
            'la'    :'Latin',
            'lv'    :'Latvian',
            'mk'    :'Macedonian',
            'no'    :'Norwegian',
            'pl'    :'Polish',
            'pt'    :'Portuguese',
            'pt-br' :'Portuguese (Brazil)',
            'ro'    :'Romanian',
            'ru'    :'Russian',
            'sr'    :'Serbian',
            'sk'    :'Slovak',
            'es'    :'Spanish',
            'es-es' :'Spanish (Spain)',
            'es-us' :'Spanish (United States)',
            'sw'    :'Swahili',
            'sv'    :'Swedish',
            'ta'    :'Tamil',
            'th'    :'Thai',
            'tr'    :'Turkish',
            'vi'    :'Vietnamese',
            'cy'    :'Welsh'
        }
    LANGUAGES['auto']='(automatic)'
    valid_languages=set(LANGUAGES)
    is_valid=lambda x:x in valid_languages
    assert is_valid(to_language) and is_valid(from_language),'Invalid language! Cannot translate. Valid languages: \n'+strip_ansi_escapes(indent(display_dict(LANGUAGES,print_it=False,arrow=' --> ')))

    import sys
    import re
    if sys.version_info[0] < 3:
        # noinspection PyUnresolvedReferences
        import urllib2
        import urllib
        # noinspection PyUnresolvedReferences
        import HTMLParser
    else:
        import html.parser
        import urllib.request
        import urllib.parse
    agent={'User-Agent':
               "Mozilla/4.0 (\
                 compatible;\
                 MSIE 6.0;\
                 Windows NT 5.1;\
                 SV1;\
                 .NET CLR 1.1.4322;\
                 .NET CLR 2.0.50727;\
                 .NET CLR 3.0.04506.30\
                 )"}
    def unescape(text):
        if sys.version_info[0] < 3:
            parser=HTMLParser.HTMLParser()
        else:
            parser=html.parser.HTMLParser()
        try:
            # noinspection PyDeprecation
            return parser.unescape(text)
        except:
            return html.unescape(text)
    base_link="http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    if sys.version_info[0] < 3:
        # noinspection PyUnresolvedReferences
        to_translate=urllib.quote_plus(to_translate)
        link=base_link % (to_language,from_language,to_translate)
        request=urllib2.Request(link,headers=agent)
        raw_data=urllib2.urlopen(request).read()
    else:
        to_translate=urllib.parse.quote(to_translate)
        link=base_link % (to_language,from_language,to_translate)
        request=urllib.request.Request(link,headers=agent)
        raw_data=urllib.request.urlopen(request).read()
    data=raw_data.decode("utf-8")
    expr=r'class="t0">(.*?)<'
    re_result=re.findall(expr,data)
    if len(re_result) == 0:
        result=""
    else:
        result=unescape(re_result[0])
    return result
def sync_sorted(*lists_in_descending_sorting_priority,key=identity):
    # Sorts main_list and reorders all *lists_in_descending_sorting_priority the same way, in sync with main_list
    return tuple(zip(*sorted(zip(*lists_in_descending_sorting_priority),key=lambda x:tuple(map(key,x)))))
sync_sort=sync_sorted#For backwards compatiability
# noinspection PyAugmentAssignment
def full_range(x,min=0,max=1):
    try:
        if x.dtype==bool:
            x=x.astype(float)
    except AttributeError:
        pass
    try:
        x=x - np.min(x)
        x=x / np.max(x)  # Augmented Assignment, AKA x-= or x/= causes numpy errors. I don't know why I wonder if its a bug in numpy.
        x=x * (max - min)
        x=x + min
        return x
    except:
        # Works with pytorch, numpy, etc
        x=x - x.min()
        x=x / x.max()  # Augmented Assignment, AKA x-= or x/= causes numpy errors. I don't know why I wonder if its a bug in numpy.
        x=x * (max - min)
        x=x + min
        return x

# region Math constants (based on numpy)
π=pi=3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862
τ=tau=2 * π
# endregion

# region Tone Generators
# Note: All Tone Sample Generators have an amplitude of [-1,1]
def sine_tone_sampler(ƒ=None,T=None,samplerate=None):
    T=T or Đ_tone_seconds
    samplerate=samplerate or Đ_samplerate
    ƒ=ƒ or Đ_tone_frequency
    ↈλ=ƒ * T  # ≣number of wavelengths
    return np.sin(np.linspace(0,τ * ↈλ,T * (samplerate or Đ_samplerate)))

def triangle_tone_sampler(ƒ=None,T=None,samplerate=None):
    return 2 / π * np.arcsin(sine_tone_sampler(ƒ,T,samplerate))

def sawtooth_tone_sampler(ƒ=None,T=None,samplerate=None):
    T=T or Đ_tone_seconds
    samplerate=samplerate or Đ_samplerate
    ƒ=ƒ or Đ_tone_frequency
    ↈλ=ƒ * T  # ≣number of wavelengths
    return (np.linspace(0,ↈλ,T * (samplerate or Đ_samplerate)) % 1) * 2 - 1

def square_tone_sampler(ƒ=None,T=None,samplerate=None):
    return np.sign(sawtooth_tone_sampler(ƒ,T,samplerate))

Đ_tone_frequency=440  # also known as note A4
Đ_tone_sampler=sine_tone_sampler
Đ_tone_seconds=1
def play_tone(hz=None,seconds=None,samplerate=None,tone_sampler=None,blocking=False):  # Plays a sine tone
    ƒ,T=hz or Đ_tone_frequency,seconds or Đ_tone_seconds  # Frequency, Time
    play_sound_from_samples((tone_sampler or Đ_tone_sampler)(ƒ,T),samplerate or Đ_samplerate,blocking=blocking)
def play_semitone(ↈ_semitones_from_A4_aka_440hz=0,seconds=None,samplerate=None,tone_sampler=None,blocking=False):
    ↈ=ↈ_semitones_from_A4_aka_440hz
    play_tone(semitone_to_hz(ↈ),seconds,samplerate,tone_sampler,blocking)
def semitone_to_hz(ↈ):
    return 440 * 2 ** (ↈ / 12)
def play_chord(*semitones:list,t=1,block=True,sampler=triangle_tone_sampler):
    play_sound_from_samples(full_range(min=-1,x=sum(sampler(semitone_to_hz(x),T=t)for x in semitones)),blocking=block)
# endregion

from itertools import product as cartesian_product
def mini_editor(out: str = "",namespace=(),message=""):  # Has syntax highlighting. Creates a curses pocket-universe where you can edit text, and then press fn+enter to enter the results. It's like like a normal input() except multiline and editable.
    # message=message or "Enter text here and then press fn+enter to exit. Supported controls: Arrow keys, backspace, delete, tab, shift+tab, enter"
    # Please note: You must be using a REAL terminal to run this! Just using pycharm's "run" is not sufficient. Using apple's terminal app, for example, IS however.
    import curses
    stdscr=curses.initscr()

    # region Initialize curses colors:
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(0,curses.COLOR_BLACK,curses.COLOR_BLACK)
    black=curses.color_pair(0)
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    red=curses.color_pair(1)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
    green=curses.color_pair(2)
    curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    yellow=curses.color_pair(3)
    curses.init_pair(4,curses.COLOR_BLUE,curses.COLOR_BLACK)
    blue=curses.color_pair(4)
    curses.init_pair(5,curses.COLOR_CYAN,curses.COLOR_BLACK)
    cyan=curses.color_pair(5)
    curses.init_pair(6,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    magenta=curses.color_pair(6)
    curses.init_pair(7,curses.COLOR_WHITE,curses.COLOR_BLACK)
    gray=curses.color_pair(7)
    # endregion
    def main(stdscr):
        print(message,end='',flush=True)
        # region http://colinmorris.github.io/blog/word-wrap-in-pythons-curses-library
        class WindowFullException(Exception):
            pass

        def addstr_wordwrap(window,s,mode=0):
            """ (cursesWindow, str, int, int) -> None
            Add a string to a curses window with given dimensions. If mode is given
            (e.g. curses.A_BOLD), then format text accordingly. We do very
            rudimentary wrapping on word boundaries.

            Raise WindowFullException if we run out of room.
            """
            # TODO Is there really no way to get the dimensions of a window programmatically?
            # passing in height and width feels ugly.

            height,width=window.getmaxyx()
            height-=1
            width-=1
            (y,x)=window.getyx()  # Coords of cursor
            # If the whole string fits on the current line, just add it all at once
            if len(s) + x <= width:
                window.addstr(s,mode)
            # Otherwise, split on word boundaries and write each token individually
            else:
                for word in words_and_spaces(s):
                    if len(word) + x <= width:
                        window.addstr(word,mode)
                    else:
                        if y == height - 1:
                            # Can't go down another line
                            raise WindowFullException()
                        window.addstr(y + 1,0,word,mode)
                    (y,x)=window.getyx()

        def words_and_spaces(s):
            import itertools
            """
            >>> words_and_spaces('spam eggs ham')
            ['spam', ' ', 'eggs', ' ', 'ham']
            """
            # Inspired by http://stackoverflow.com/a/8769863/262271
            return list(itertools.chain.from_iterable(zip(s.split(),itertools.repeat(' '))))[:-1]  # Drop the last space

        # endregion
        nonlocal out
        cursor_shift=0
        while True:
            # region  Keyboard input:
            stdscr.nodelay(1)  # do not wait for input when calling getch
            c=stdscr.getch()  # get keyboard input
            typing=False
            updown=None
            if c != -1:  # getch() returns -1 if none available
                # text_to_speech(c)
                if chr(c) in "":  # ⟵ Up/Down/Left/Right arrow keys (Up/Down ≣ Scroll up down) are not currently implemented. I don't know how.
                    pass
                elif c == ord("Ą"):  # left arrow key
                    cursor_shift+=1
                    cursor_shift=min(len(out),cursor_shift)
                elif c == ord("ą"):  # right arrow key
                    cursor_shift-=1
                    cursor_shift=max(0,cursor_shift)
                elif c == ord("ă"):  # up arrow key
                    updown='up'
                elif c == ord("Ă"):  # down arrow key
                    updown='down'
                elif c == ord('ŗ') == 343:  # fn+enter was pressed# c==10:# Enter key was pressed
                    return out
                else:
                    typing=True
                    # out+=chr(c)

            # out_lines=out.split("\n")
            # cursor_y=len(out_lines)-1
            # while cursor_x<0:
            #     cursor_x+=len(out_lines[cursor_y])
            #     cursor_y-=1

            out_lines=out.split("\n")
            cursor_y=0
            cursor_x=len(out) - cursor_shift
            assert cursor_x >= 0

            if updown:
                if updown == 'up':
                    i0=out[:cursor_x].rfind("\n")
                    i1=out[:i0].rfind("\n")
                    cursor_x=min(len(out) - 1,max(0,min(cursor_x - i0,i0 - i1) + i1))
                    cursor_shift=len(out) - cursor_x

                else:
                    assert updown == 'down'
                    i0=out[:cursor_x].rfind("\n")
                    i1=out.find("\n",i0 + 1)
                    cursor_x=min(len(out) - 1,max(0,min(cursor_x - i0,i1 - i0) + i1))
                    cursor_shift=len(out) - cursor_x

            elif typing:
                if c == 127:  # Backspace key was pressed
                    if cursor_x:
                        out=out[:cursor_x - 1] + out[cursor_x:]
                elif c == ord("Ŋ"):  # Delete key was pressed
                    if cursor_x < len(out):
                        out=out[:cursor_x] + out[cursor_x + 1:]
                        cursor_shift-=1
                        cursor_x+=1
                elif c == ord('\t'):  # tab
                    out=out[:cursor_x] + "    " + out[cursor_x:]  # 4 spaces per tab
                elif c == ord('š'):  # shift+tab
                    if cursor_x:
                        out=out[:max(0,cursor_x - 4)] + out[cursor_x:]  # 4 backspaces
                else:
                    out=out[:cursor_x] + chr(c) + out[cursor_x:]

            for i in range(len(out_lines) - 1):
                out_lines[i]+="\n"  # So that ∑out_lines ＝ out
            while cursor_x > len(out_lines[cursor_y]):
                cursor_x-=len(out_lines[cursor_y])
                cursor_y+=1
            try:
                if out[len(out) - cursor_shift - 1] == "\n":  # c_x+1?
                    cursor_x=0
                    cursor_y+=1
            except:
                pass

            # endregion
            # region Real-time display:
            stdscr.erase()
            stdscr.move(0,0)  # return curser to start position to re-print everything
            height,width=stdscr.getmaxyx()
            height-=1
            width-=1
            def print_fansi_colors_in_curses(stdscr,s: str):  # Only supports text colors; DOES NOT support anything else at the moment. Assumes we are given a fansi sequence.
                text_color=None
                while True:  # Until string is empty.
                    if s.startswith("\x1b["):
                        while s.startswith("["):  # Oddly without this I got -------...... ⭆ ^[[0;33m-^[[0;33m-^[[0;33m-^[[0;33m-^[[0;33m-^[.......
                            s=s[1:]
                        i=s.find('m')  # there should always be a m somewhere, print(repr(fansi_print("h",'red','bold'))) for example.
                        ss=s[:i].split(';')
                        s=s[i + 1:]  # +1 to take care of the m which is gone now
                        if '30' in ss:  # black
                            text_color=black
                        elif '31' in ss:  # red
                            text_color=red
                        elif '32' in ss:  # green
                            text_color=green
                        elif '33' in ss:  # yellow
                            text_color=yellow
                        elif '34' in ss:  # blue
                            text_color=blue
                        elif '35' in ss:  # magenta
                            text_color=magenta
                        elif '36' in ss:  # cyan
                            text_color=cyan
                        elif '37' in ss:  # gray
                            text_color=gray
                        else:  # if'0'in ss:# clear style
                            text_color=None
                    if not s:
                        break  # avoid trying to access indexes in an empty string
                    if text_color is not None:
                        # stdscr.addstr(s[0],text_color)
                        addstr_wordwrap(stdscr,s[0],text_color)
                    else:
                        # stdscr.addstr(s[0])
                        addstr_wordwrap(stdscr,s[0])
                    s=s[1:]
            print_fansi_colors_in_curses(stdscr,fansi_syntax_highlighting(out,namespace))
            assert isinstance(out,str)

            while cursor_x > width:
                cursor_y+=1
                cursor_x-=width
            cursor_y=min(height,cursor_y)
            stdscr.move(cursor_y,cursor_x)
            stdscr.refresh()
            # endregion
    curses.wrapper(main)
    return out

def get_terminal_size():  # In (ↈcolumns，ↈrows) tuple form
    # From http://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python/14422538#14422538
    import os
    env=os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl,termios,struct,os
            cr=struct.unpack('hh',fcntl.ioctl(fd,termios.TIOCGWINSZ,
                                              '1234'))
        except:
            return
        return cr
    cr=ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd=os.open(os.ctermid(),os.O_RDONLY)
            cr=ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr=(env.get('LINES',25),env.get('COLUMNS',80))

        ### Use get(key[, default]) instead of a try/catch
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except:
        #    cr = (25, 80)
    return int(cr[1]),int(cr[0])
def get_terminal_width():
    return get_terminal_size()[0]
def get_terminal_height():
    return get_terminal_size()[1]

def is_namespaceable(c: str) -> bool:  # If character can be used as the first of a python variable's name
    return str.isidentifier(c) or c==''#Maintaining original functionality but doing it much much faster
    import re
    try:
        c+=random_permutation("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Just in case this overrides some other variable somehow (I don't know how it would do that but just in case)
        exec(c + "=None")
        exec("del " + c)
        return True
    except:
        return False

def is_literal(c: str) -> bool:  # If character can be used as the first of a python variable's name
    return c==":" or (is_namespaceable(c) or c.isalnum())and not c.lstrip().rstrip() in ['False','def','if','raise','None','del','import','return','True','elif','in','try','and','else','is','while','as','except','lambda','with','assert','finally','nonlocal','yield','break','for','not','class','from','or','continue','global','pass']

def clip_string_width(x: str,max_width=None,max_wraps_per_line=1,clipped_suffix='…'):  # clip to terminal size. works with multi lines at once.
    max_width=(max_width or get_terminal_width()) * max_wraps_per_line
    return '\n'.join((y[:max_width - len(clipped_suffix)] + clipped_suffix) if len(y) > max_width else y for y in x.split('\n'))

def properties_to_xml(src_path,target_path):  # Found this during my 219 hw4 assignment when trying to quickly convert a .properties file to an xml file to get more credit
    # SOURCE: https://www.mkyong.com/java/how-to-store-properties-into-xml-file/
    # Their code was broken so I had to fix it. It works now.
    src=open(src_path)
    target=open(target_path,'w')
    target.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n')
    target.write('<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n')
    target.write('<properties>\n')

    for line in src.readlines():
        word=line.split('=')
        key=word[0]
        message='='.join(word[1:]).strip()  # .decode('unicode-escape')
        # message=unicode('='.join(word[1:]).strip(),'unicode-escape')
        target.write('\t<entry key="' + key + '"><![CDATA[' + message.encode('utf8').decode() + ']]></entry>\n')

    target.write('</properties>')
    target.close()

def split_letters_from_digits(s: str) -> list:
    # Splits letters from numbers into a list from a string.
    # EXAMPLE: "ads325asd234" -> ['ads', '325', 'asd', '234']
    # SOURCE: http://stackoverflow.com/questions/28290492/python-splitting-numbers-and-letters-into-sub-strings-with-regular-expression
    import re
    return re.findall(r'[A-Za-z]+|\d+',s)

def split_camel_case(s: str) -> list:
    # Split camel case names into lists. Example: camel_case_split("HelloWorld")==["Hello","World"]
    from re import finditer
    matches=finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',s)
    return [m.group(0) for m in matches]

def split_python_tokens(string,return_tokens=False,ignore_errors=True):
    #return_tokens is as opposed to returning the strings of those tokens, and thus returning a list of strings (the default behaviour)
    #if ignore_errors, ignore any parsing errors and keep parsing tokens (return all tokens, even the ones that causes errors such as unterminated strings etc)
    #EXAMPLES:
    #    ⮤ split_python_tokens('aosid aoisjd aois   j d; ')
    #    ans = ['aosid', 'aoisjd', 'aois', 'j', 'd', ';']
    #    ⮤ split_python_tokens(' lambda x: 3,1')
    #    ans = [' ', 'lambda', 'x', ':', '3', ',', '1', '']
    import tokenize
    i=iter(string.splitlines())
    def f():return next(i).encode()
    token_iterator=tokenize.tokenize(f)
    tokens=[]
    while True:
        try:
            tokens.append(next(token_iterator))
        except StopIteration:
            break
        except:
            if ignore_errors:
                continue
            else:
                raise
    tokens=tokens[1:]#The first and last token are never useful (just begin/end of field tokens. Even tokenizing an empty string would yield these two tokens.)
    if tokens and tokens[-1].type==tokenize.ENDMARKER:#This token is useless imho. Especially when we're trying to return strings split from python tokens. It just adds an empty string to the end of the output. Useless...
        del tokens[-1]
    if return_tokens:
        return tokens
    else:
        return [token.string for token in tokens]

def int_clamp(x: int,min_value: int,max_value: int) -> int:
    return min([max([min_value,x]),max_value])
def float_clamp(x: float,min_value: float,max_value: float) -> float:
    # noinspection PyTypeChecker
    return int_clamp(x,min_value,max_value)

#region stack traces
def pop_exception_traceback(exception,n=1):
    #Takes an exception, mutates it, then returns it
    #Often when writing my repl, tracebacks will contain an annoying level of function calls (including the 'exec' that ran the code)
    #This function pops 'n' levels off of the stack trace generated by exception
    #For example, if print_stack_trace(exception) originally printed:
    #   Traceback (most recent call last):
    #   File "<string>", line 2, in <module>
    #   File "<string>", line 2, in f
    #   File "<string>", line 2, in g
    #   File "<string>", line 2, in h
    #   File "<string>", line 2, in j
    #   File "<string>", line 2, in k
    #Then print_stack_trace(pop_exception_traceback(exception),3) would print:
    #   File "<string>", line 2, in <module>
    #   File "<string>", line 2, in j
    #   File "<string>", line 2, in k
    #(It popped the first 3 levels, aka f g and h off the traceback)
    #Edge case: If we start with let's say only 4 levels, but n=1000, only pop 4 levels (trying to more would result in an error)
    for _ in range(n):
        if exception.__traceback__ is None:
            break
        exception.__traceback__=exception.__traceback__.tb_next
    return exception

def print_verbose_stack_trace(exception):
    stackprinter=pip_import('stackprinter')
    try:
        if _disable_fansi:
            stackprinter.show(exception,file=sys.stdout)
        else:
            stackprinter.show(exception,style='darkbg2',file=sys.stdout)
    except ValueError:#ERROR: ValueError: Can't format KeyboardInterrupt(). Expected an exception instance, sys.exc_info() tuple,a frame or a thread object.
        print_stack_trace(exception)#Fallback when this fails


def print_stack_trace(error:BaseException,full_traceback: bool = True,header='r.print_stack_trace: ERROR: ',print_it=True):
    from traceback import format_exception,format_exception_only
    #                                       ┌                                                                                                                                                                                                ┐
    #                                       │                                  ┌                                                                                                                                                            ┐│
    #                                       │                                  │       ┌                                                           ┐                               ┌                                            ┐           ││
    #      ┌                               ┐│     ┌                   ┐        │       │                ┌                                         ┐│                               │                     ┌                     ┐│┌   ┐      ││
    return (print if print_it else identity)(fansi(header,'red','bold') + fansi(''.join(format_exception(error.__class__,error,error.__traceback__)) if full_traceback else ''.join(format_exception_only(error.__class__,error))[:-1],'red'))
    #      └                               ┘│     └                   ┘        │       │                └                                         ┘│                               │                     └                     ┘│└   ┘      ││
    #                                       │                                  │       └                                                           ┘                               └                                            ┘           ││
    #                                       │                                  └                                                                                                                                                            ┘│
    #                                       └                                                                                                                                                                                                ┘

#endregion

def audio_stretch(mono_audio, new_number_of_samples):# Does not take into account the last bit of looping audio
    # ⮤ audio_stretch([1,10],10)
    # ans = [1,2,3,4,5,6,7,8,9,10]
    return [ linterp(x,mono_audio) for x in np.linspace(0,len(mono_audio)-1,new_number_of_samples)]

def cartesian_to_polar(x, y, ϴ_unit=τ)->tuple:
    """Input conditions: x，y ∈ ℝ ⨁ x﹦［x₀，x₁，x₂……］⋀ y﹦［y₀，y₁，y₂……］
    returns: (r, ϴ) where r ≣ radius，ϴ ≣ angle and 0 ≤ ϴ < ϴ_unit. ϴ_unit﹦τ ⟹ ϴ is in radians，ϴ_unit﹦360 ⟹ ϴ is in degrees"""
    return np.hypot(x,y),np.arctan2(y,x)/τ%1*ϴ_unit  # Order of operations: % has same precedence as * and /
def complex_to_polar(complex,ϴ_unit=τ)->tuple:
    """returns: (r, ϴ) where r ≣ radius，ϴ ≣ angle and 0 ≤ ϴ < ϴ_unit. ϴ_unit﹦τ ⟹ ϴ is in radians，ϴ_unit﹦360 ⟹ ϴ is in degrees.
    Input conditions: c ≣ complex ⋀ c ∈ ℂ ⨁ c﹦［c₀，c₁，c₂……］
    Returns r and ϴ either as numbers OR as two lists: all the r's and then all the ϴ's"""
    return np.abs(complex),np.angle(complex)# np.abs is calculated per number, not vector etc
Đ_left_to_right_sum_ratio=0# By default, take a left hand sum
def riemann_sum(f,x0,x1,N,left_to_right_sum_ratio=None):# Verified ✔
    # Desmos: https://www.desmos.com/calculator/tgyr42ezjq
    # left_to_right_sum_ratio﹦0  ⟹ left hand sum
    # left_to_right_sum_ratio﹦.5 ⟹ midpoint hand sum
    # left_to_right_sum_ratio﹦1  ⟹ right hand sum
    # The x1 bound MUST be exclusive as per definition of a left riemann sum
    c=left_to_right_sum_ratio or Đ_left_to_right_sum_ratio
    w=(x1-x0)/N# Width of the bars
    return sum(f(x0+w*(i+c))*w for i in range(N))
def riemann_mean(f,x0,x1,N,left_to_right_sum_ratio=None):# To prevent redundancy of the N parameter
    return riemann_sum(f,x0,x1,N,left_to_right_sum_ratio) / (x1-x0)

def fourier(cyclic_function,freq,cyclic_period=τ,ↈ_riemann_terms=100):
    # Can enter a vector of frequencies to two vectors of outputs if you so desire
    # Returns polar coordinates representing amplitude,phase  (AKA r,ϴ)
    # With period=τ, sin(x) has a freq of 1.
    # With period=1, sin(x) has a freq of 1/τ.
    # ⁠⁠⁠⁠                     ⎧                                                                                                        ⎫
    # ⁠⁠⁠⁠                     ⎪            ⎧                                                                                          ⎫⎪
    # ⁠⁠⁠⁠                     ⎪            ⎪               ⎧                 ⎫                  ⎧               ⎫                     ⎪⎪
    return complex_to_polar(riemann_mean(lambda x:np.exp(freq * τ * x * 1j) * cyclic_function(x*cyclic_period),0,1,ↈ_riemann_terms))
    # ⁠⁠⁠                     ⎪            ⎪               ⎩                 ⎭                  ⎩               ⎭                     ⎪⎪
    # ⁠⁠⁠                     ⎪            ⎩                                                                                          ⎭⎪
    # ⁠⁠⁠                     ⎩                                                                                                        ⎭
def discrete_fourier(cyclic_vector,freq):# Assuming that cyclic_vector is a single wave-cycle, freq represents the number of its harmonic
    # Can enter a vector of frequencies to two vectors of outputs if you so desire
    # Returns polar coordinates representing amplitude,phase  (AKA r,ϴ)
    return fourier(cyclic_function=lambda x:linterp(x,cyclic_vector,cyclic=True),freq=freq,cyclic_period=len(cyclic_vector),ↈ_riemann_terms=len(cyclic_vector))
def matrix_to_tuples(m,filter=lambda r,c,val:True):# Filter can significantly speed it up
    # ⁠⁠⁠⁠             ⎧                                                                                        ⎫
    # ⁠⁠⁠⁠             ⎪⎧                                                                                      ⎫⎪
    # ⁠⁠⁠⁠             ⎪⎪⎧                                                             ⎫                       ⎪⎪
    # ⁠⁠⁠⁠             ⎪⎪⎪                            ⎧         ⎫                      ⎪                       ⎪⎪
    # ⁠⁠⁠⁠             ⎪⎪⎪⎧           ⎫               ⎪   ⎧    ⎫⎪          ⎧          ⎫⎪               ⎧      ⎫⎪⎪
    return list_pop([[(r,c,m[r][c]) for c in range(len(m[r])) if filter(r,c,m[r,c])] for r in range(len(m))])# Creates list of coordinates, (x,y,value). WARNING: Can be very slow
    #              ⎪⎪⎪⎩           ⎭               ⎪   ⎩    ⎭⎪          ⎩          ⎭⎪               ⎩      ⎭⎪⎪
    #              ⎪⎪⎪                            ⎩         ⎭                      ⎪                       ⎪⎪
    #              ⎪⎪⎩                                                             ⎭                       ⎪⎪
    #              ⎪⎩                                                                                      ⎭⎪
    #              ⎩                                                                                        ⎭
def perpendicular_bisector_function(x0,y0,x1,y1):
    A,B=x0,y0
    Y,X=x1,y1
    def linear_function(x):
        return ((B+Y)/2)-(X-A)/(Y-B)*(x-(A+X)/2)  # https://www.desmos.com/calculator/1ykebsqtoa
    return linear_function

def harmonic_analysis_via_least_squares(wave,harmonics:int):
    #My attempt to analyze frequencies by taking the least-squares fit of a bunch of sinusoids to a signal instead of using the fourier transform. It had interesting results, but it's not nearly as fast as a FFT.
    prod=np.matmul
    inv=np.linalg.inv
    b=wave  # In terms of linear algebra in Ax~=b
    samples=len(b)
    m=np.asmatrix(np.linspace(1,harmonics,harmonics)).T*np.matrix(np.linspace(0,tau,samples,endpoint=False))
    A=np.asmatrix(np.concatenate([np.sin(m),np.cos(m)])).T
    Api=prod(inv(prod(A.T,A)),A.T)  # Api====A pseudo inverse
    out=np.asarray(prod(Api,b))[0]
    out=np.reshape(out,[2,len(out)//2])  # First vector is the sin array second is the cos array
    amplitudes=sum(out**2)**.5
    phases=np.arctan2(*out)
    return np.asarray([amplitudes,phases])  # https://www.desmos.com/calculator/fnlwi71n9x

def cluster_filter(vec,filter=identity):  # This has a terrible name...I'm not sure what to rename it so if you think of something, go for it!
    # EXAMPLE: cluster_filter([2,3,5,9,4,6,1,2,3,4],lambda x:x%2==1) --> [[3, 5, 9], [1], [3]]  <---- It separated all chunks of odd numbers
    # region Unoptimized, much slower version (that I kept because it might help explain what this function does):
    # def mask_clusters(vec,filter=identity):
    #  out=[]
    #  temp=[]
    #  for val in vec:
    #    if filter(val):
    #      temp.append(val)
    #    elif temp:
    #      out.append(temp)
    #      temp=[]
    #  return out
    # endregion

    out=[]
    s=None  # start
    for i,val in enumerate(vec):
        if filter(val):
            if s is None:
                s=i
        elif s is not None:
            out.append(vec[s:i])
            s=None
    if s is not None:
        out.append(vec[s:])
    return out

# region Originally created for the purpose of encoding 3 bytes of precision into a single image via r,g,b being three digits
def proportion_to_digits(value,base=256,number_of_digits=3):  # Intended for values between 0 and 1
    digits=[]
    x=value
    while len(digits)<number_of_digits:
        x*=base
        temp=np.floor(x)
        digits.append(temp)
        x-=np.floor(x)
    return digits
def digits_to_proportion(digits,base=256):  # Intended for values between 0 and 1
    return np.sum(np.asarray(digits)/base**np.linspace(1,len(digits),len(digits)),0)
def rgb_encoded_matrix(m):# Encoded precision of values between 0 and 1 as r,g,b (in 8-bit color) values where r g and b are each digits, with b being the most precise and r being the least precise
    m=np.matrix(m)
    assert len(m.shape)==2,"r.rgb_encoded_matrix: Input should be a matrix of values between 0 and 1, which is not what you gave it! \n m.shape = \n"+str(m.shape)
    r,g,b=proportion_to_digits(m,base=256,number_of_digits=3)
    out=np.asarray([r,g,b])
    out=np.transpose(out,[1,2,0])
    out=out.astype(np.uint8)
    return out
def matrix_decoded_rgb(rgb):
    rgb=np.asarray(rgb)
    assert len(rgb.shape)==3 and rgb.shape[-1]==3,"r.rgb_encoded_matrix: Input should be an rgb image (with 3 color channels), which is not what you gave it! \n m.shape = \n"+str(rgb.shape)
    return digits_to_proportion(rgb.transpose([2,0,1]))
def print_all_git_paths():
    fansi_print("Searching for all git repositories on your computer...",'green','underlined')
    tmp = shell_command("find ~ -name .git")# Find all git repositories on computer
    dirpaths=[x[:-4]for x in tmp.split('\n')]
    aliasnames=[(lambda s:(s[:s.find("/")])[::-1])((x[::-1])[1:])for x in dirpaths]
    dirpaths,aliasnames=sync_sort(dirpaths,aliasnames)
    for x in sorted(zip(aliasnames,dirpaths)):
        print(fansi(x[0],'cyan')+" "*(max(map(len,aliasnames))-len(x[0])+3)+fansi(x[1],None))
    return dirpaths,aliasnames

def is_int_literal(s:str):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def is_string_literal(s:str):
    try:
        s=eval(s)
        assert isinstance(s,str)
        return True
    except:
        return False

def indentify(s:str,indent='\t'):
    return '\n'.join(indent + x for x in s.split('\n'))
def lrstrip_all_lines(s:str):
    return '\n'.join([x.lstrip().rstrip()for x in s.split('\n')])

random_unicode_hash=lambda l:int_list_to_string([randint(0x110000-1)for x in range(l)])
def search_replace_simul(s:str,replacements:dict):
    if not replacements:
        return s
    # ⮤ search_replace_simul("Hello world",{"Hello":"world","world":"Hello"})
    l1 = replacements.keys()
    l2 = replacements.values()
    l3 = [random_unicode_hash(10) for x in replacements]
    ⵁ,l1,l2,l3=sync_sort([-len(x)for x in l1],l1,l2,l3)# Sort the keys in descending number of characters     # Safe replacements: f and fun as keys: f won't be seen as in 'fun'
    for a,b in zip(l1,l3):
        s=s.replace(a,b)
    for a,b in zip(l3,l2):
        s=s.replace(a,b)
    return s

def shorten_url(url:str)->str:
    import contextlib
    try:
        from urllib.parse import urlencode
    except ImportError:
        from urllib import urlencode
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    import sys
    request_url=('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')
    # Update: The following commented code is deprecated, since Google discontinued the ability to create new goo.gl URL's
    #   # goo.gl links are supposed to last forever, according to https://groups.google.com/forum/#!topic/google-url-shortener/Kt0bc5hx9HE
    #   # SOURCE: https://stackoverflow.com/questions/17357351/how-to-use-google-shortener-api-with-python
    #   # API Key source: https://console.developers.google.com/apis/credentials?project=dark-throne-182400
    #   #  ⮤ goo_shorten_url('ryan-central.org')
    #   # ans = https://goo.gl/Gkgp86
    #   import requests
    #   import json
    #   post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyBbNJ4ZPCAeDBGAVQKDikwruo3dD4NcsU4'# AIzaSyBbNJ4ZPCAeDBGAVQKDikwruo3dD4NcsU4 is my account's API key.
    #   payload = {'longUrl': url}
    #   headers = {'content-type': 'application/json'}
    #   r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    #   # RIGHT NOW: r.text==
    #   # '''{
    #   #     "kind":"urlshortener#url",
    #   #     "id":"https://goo.gl/ZNp1VZ",
    #   #     "longUrl":"https://console.developers.google.com/apis/credentials?project=dark-throne-182400"
    #   # }'''
    #   out=eval(r.text)
    #   assert isinstance(out,dict)
    #   return out['id']

def gist(gist_body="Body",gist_filename="File.file",gist_description="Description"):
    # Older version:
    # def gist(code:str,file_name:str='CodeGist.code',username='sqrtryan@gmail.com',password='d0gememesl0l'):
    #     # Posts a gist with the given code and filename.
    #     #  ⮤ gist("Hello, World!")
    #     # ans = https://gist.github.com/b5b3e404c414f7974c4ccb12106c4fe7
    #     import requests,json
    #     r = requests.post('https://api.github.com/gists',json.dumps({'files':{file_name:{"content":code}}}),auth=requests.auth.HTTPBasicAuth(username, password))
    #     try:
    #         return r.json()['html_url']# Returns the URL
    #     except KeyError as e:
    #         fansi_print("r.gist ERROR:",'red','bold',new_line=False)
    #         fansi_print(" "+str(e)+" AND r.json() = "+str(r.json()),'red')

    from urllib.request import urlopen
    import json
    gist_post_data={'description':gist_description,
                    'public':True,
                    'files':{gist_filename:{'content':gist_body}}}

    json_post_data=json.dumps(gist_post_data).encode('utf-8')

    def upload_gist():
        # print('sending')
        url='https://api.github.com/gists'
        json_to_parse=urlopen(url,data=json_post_data)

        # print('received response from server')
        found_json=(b'\n'.join(json_to_parse.readlines()))
        return json.loads(found_json.decode())['html_url']
    return upload_gist()

sgist=lambda *x:seq([gist,printed,open_url,shorten_url],*x)# Open the url of a gist and print it

def random_namespace_hash(n:int=10,chars_to_choose_from:str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
    # ⮤ random_namespace_hash(10)
    # ans=DZC7B8GV74
    out=''
    for n in [None]*n:
        out+=random_element(chars_to_choose_from)
    return out

def latex_image(equation: str):
    # Returns an rgba image with the rendered latex string on it in numpy form
    import os,requests
    def formula_as_file(formula,file,negate=False):  # Got this code off the web somewhere but i dont remember where now
        tfile=file
        if negate:
            tfile='tmp.png'
        r=requests.get('http://latex.codecogs.com/png.latex?\dpi{300} \huge %s' % formula)
        f=open(tfile,'wb')
        f.write(r.content)
        f.close()
        if negate:
            os.system('convert tmp.png -channel RGB -negate -colorspace rgb %s' % file)
    formula_as_file(equation,'temp.png')
    return load_image('temp.png')

def display_image_in_terminal(image):
    pip_import('drawille')
    from drawille import Canvas
    i=as_binary_image(as_grayscale_image(image))
    c=Canvas()
    for x in range(width(i)):
        for y in range(height(i)):
            if i[x,y]:
                c.set(y,x)
    print(c.frame())

def auto_canny(image,sigma=0.33,lower=None,upper=None):
    pip_import('cv2')
    cv2=pip_import('cv2')
    if image.dtype!=np.uint8:
        image=full_range(image,0,255).astype(np.uint8)

    # compute the median of the single channel pixel intensities
    v=np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower=int(max(0,(1.0 - sigma) * v)) if lower is None else lower
    upper=int(min(255,(1.0 + sigma) * v)) if upper is None else upper

    edged=cv2.Canny(image,lower,upper)

    # return the edged image
    return edged


def skeletonize(image):
    try:
        return _skimage_skeletonize(image)
    except:
        #Warning: The current _cv_skeletonize method produces different and inferior results than that of _skimage_skeletonize
        return _cv_skeletonize(image)

def _skimage_skeletonize(image):
    # https://scikit-image.org/docs/dev/auto_examples/edges/plot_skeleton.html
    image=as_binary_image(as_grayscale_image(image))
    pip_import('skimage')
    from skimage.morphology import skeletonize
    return skeletonize(image)

def _cv_skeletonize(img):
    """ OpenCV function to return a skeletonized version of img, a Mat object"""
    cv2=pip_import('cv2')
    # Found this on the web somewhere
    #  hat tip to http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/
    img=img.astype(np.uint8)
    img=img.copy()  # don't clobber original
    skel=img.copy()

    skel[:,:]=0
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

    while True:
        eroded=cv2.morphologyEx(img,cv2.MORPH_ERODE,kernel)
        temp=cv2.morphologyEx(eroded,cv2.MORPH_DILATE,kernel)
        temp=cv2.subtract(img,temp)
        skel=cv2.bitwise_or(skel,temp)
        img[:,:]=eroded[:,:]
        if cv2.countNonZero(img) == 0:
            break

    return skel

# noinspection PyTypeChecker
def print_latex_image(latex: str,thin=True,scale=.17,threshold=20):
    # ⮤ print_latex_image("\sum_{n=3}^7x^2")
    # ⠀⠀⠀⠀⠠⠟⢉⠟
    # ⠀⠀⠀⠀⠀⠀⡏
    # ⠀⠀⠀⠀⠀⠀⠃
    # ⢀⢀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡀
    # ⠀⠙⠄⠀⠀⠀⠀⠀⠀⠈⠉⢦⠀⠀⠀⠀⠀⠀⠀⠛⠀⡸
    # ⠀⠀⠈⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⣡
    # ⠀⠀⠀⠀⠑⡀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠋⣹⠉⠃⠈⠉⠉
    # ⠀⠀⠀⢀⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣠⣏⣠⠆
    # ⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⣠
    # ⢀⢼⣤⣤⣤⣤⣤⡤⠤⠤⠴⠁
    #
    # ⢀⠀⣀⠀⠀⠀⠀⠀⠀⠐⠏⢹
    # ⢣⠏⢨⠃⢘⣛⣛⣛⣋⢀⠈⠙⡄
    # ⠘⠀⠘⠊⠀⠀⠀⠀⠀⠘⠒⠚
    # Prints it in the console
    # @formatter:off
    DisplayThin=   lambda latex:display_image_in_terminal((resize_image(skeletonize(255 - latex_image(latex)[:,:,0]),scale) > threshold) * 1)
    DisplayRegular=lambda latex:display_image_in_terminal((resize_image(           (255 - latex_image(latex)[:,:,0]),scale) > threshold) * 1)
    #@formatter:on
    if thin:
        DisplayThin(latex)
    else:
        DisplayRegular(latex)

cd=os.chdir
image_acro="""di=display_image
li=load_image
dgi=display_grayscale_image
lg=line_graph
cv2=pip_import('cv2')
"""

# def remove_alpha_channel(image:np.ndarray,shutup=False):
#     # Strips an image of its' alpha channel if it has one, otherwise basically leaves the image alone.
#     sh=image.shape
#     l=len(sh)
#     if l==2 and not shutup:
#         # Don't break the user's script but warn them: this image is not what they thought it was.
#         print("r.remove_alpha_channel: WARNING: You fed in a matrix; len(image.shape)==2")
#         return image
#     if
#     assert l==3,'Assuming that it has color channels to begin with, and that its not just a matrix of numbers'
#     assert 3<=sh[2]<=4,'Assuming it has R,G,B or R,G,B,A'
#
#     return image[:,:,:2]

def is_valud_url(url: str) -> bool:
    # PROBLEM:
    #     ⮤ ivu("google.com")
    # ans=False

    # I DID NOT WRITE THIS WHOLE FUNCTION ∴ IT MIGHT NOT WORK PERFECTLY. THIS IS FROM: http://stackoverflow.com/questions/452104/is-it-worth-using-pythons-re-compile
    import re
    regex=re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',re.IGNORECASE).match(url)
    return regex is not None and (lambda ans:ans.pos == 0 and ans.endpos == len(url))(g.fullmatch(url))
import rp.rp_ptpython.prompt_style as ps
ps.__all__+=("PseudoTerminalPrompt",)


_prompt_style_path=__file__+'.rp_prompt_style'
_get_prompt_style_cached=None
def _get_prompt_style():
    global _get_prompt_style_cached
    if _get_prompt_style_cached is None:
        try:
            out=text_file_to_string(_prompt_style_path)
        except:
            out=' >>> '

        _get_prompt_style_cached=out
    return _get_prompt_style_cached

def set_prompt_style(style:str=None):
    print('Running rp.set_prompt_style:')
    default_prompt_styles=[' ⮤ ',' >>> ',' >> ',' > ',' ▶ ',' ▶▶ ',' ►► ' ,' ▷▷ ',' ▷ ',' --> ',' ––> ',' 🠥 ','',' 🡩 ',' ➤ ',' ⮨ ']
    cancel_message='Cancelled setting new prompt style.'

    if style is None:
        custom_option='(custom prompt style)'
        cancel_option='(cancel)'

        option=input_select('No style was specified. Please select a new prompt style:',[custom_option,cancel_option]+default_prompt_styles)
        if option==custom_option:
            print('Enter a custom prompt style:')
            style=input()
        elif option==cancel_option:
            print(cancel_message)
            return
        else:
            style=option

    assert isinstance(repr(style),str)
    fansi_print("Displaying current prompt style:",'blue')
    print(repr(_get_prompt_style()))
    fansi_print("Displaying new prompt style:",'blue')
    print(repr(style))
    print(fansi('Some other styles you might want to consider: ','blue')+repr(default_prompt_styles)[1:-1])

    if input_yes_no("Are you sure you want to switch?"):
        try:
            string_to_text_file(_prompt_style_path,style)
            global _get_prompt_style_cached
            _get_prompt_style_cached=None#Invalidate the cache, forcing it to reload
        except BaseException as e:
            print("Failed to save new prompt...displaying error")
            print_stack_trace(e)
    else:
        print('...ok. Will not save new prompt style')
        if input_yes_no('Would you like to select a different style instead?'):
            set_prompt_style()
        else:
            print(cancel_message)
            return

class PseudoTerminalPrompt(ps.ClassicPrompt):
    def in_tokens(self,cli):
        pip_import('pygments')
        from pygments.token import Token
        return [(Token.Prompt,_get_prompt_style())]
setattr(ps,'PseudoTerminalPrompt',PseudoTerminalPrompt)
Đ_python_input_eventloop = None  # Singleton for python_input
# def python_input(namespace):
#     try:
#         from rp.prompt_toolkit.shortcuts import create_eventloop
#         from ptpython.python_input import PythonCommandLineInterface,PythonInput as Pyin
#         global Đ_python_input_eventloop
#         pyin=Pyin(get_globals=lambda:namespace)
#         pyin.enable_mouse_support=False
#         pyin.enable_history_search=True
#         pyin.highlight_matching_parenthesis=True
#         pyin.enable_input_validation=False
#         pyin.enable_auto_suggest=False
#         pyin.show_line_numbers=True
#         pyin.enable_auto_suggest=True
#         # exec(mini_terminal)
#         pyin.all_prompt_styles['Pseudo Terminal']=ps.PseudoTerminalPrompt()
#         # ps.PseudoTerminalPrompt=PseudoTerminalPrompt
#         pyin.prompt_style='Pseudo Terminal'
#
#         Đ_python_input_eventloop=Đ_python_input_eventloop or PythonCommandLineInterface(create_eventloop(),python_input=pyin)
#         #
#         # try:
#         code_obj = Đ_python_input_eventloop.run()
#         if code_obj.text is None:
#             print("THE SHARKMAN SCREAMS")
#         return code_obj.text
#     except Exception as E:
#         print_stack_trace(E)
#     # except BaseException as re:
#     # print_stack_trace(re)
#     # print("THE DEMON SCREAMS")
def split_into_sublists(l,sublist_len:int,strict=True,keep_remainder=True):
    # If strict: sublist_len MUST evenly divide len(l)
    # keep_remainder is not applicable if strict
    # if not keep_remainder and sublist_len DOES NOT evenly divide len(l), we can be sure that all tuples in the output are of len sublist_len, even though the total number of elements in the output is less than in l.
    # EXAMPLES:
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,3 ,0)   ⟶ [(1,2,3),(4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,0)   ⟶ [(1,2,3,4),(5,6,7,8),(9,)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,5 ,0)   ⟶ [(1,2,3,4,5),(6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,6 ,0)   ⟶ [(1,2,3,4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0)   ⟶ [(1,2,3,4,5,6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0,1) ⟶ [(1,2,3,4,5,6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0,0) ⟶ []
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,5 ,0,0) ⟶ [(1,2,3,4,5)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,0,0) ⟶ [(1,2,3,4),(5,6,7,8)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,3 ,0,0) ⟶ [(1,2,3),(4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,1,0) ⟶ ERROR: ¬ 4 | 9
    if strict:
        assert not len(l)%sublist_len,'len(l)=='+str(len(l))+' and sublist_len=='+str(sublist_len)+': strict mode is turned on but the sublist size doesnt divide the list input evenly. len(l)%sublist_len=='+str(len(l)%sublist_len)+'!=0'
    n=sublist_len
    return list(zip(*(iter(l),) * n))+([tuple(l[len(l)-len(l)%n:])] if len(l)%n and keep_remainder else [])

def rotate_image(image, angle_in_degrees):
    # GOT CODE FROM URL: https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    angle=angle_in_degrees
    cv2=pip_import('cv2')
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def open_url(url:str):
    from webbrowser import open
    open(url)

def restart_python():
    from os import system
    print("killall Python\nsleep 2\npython3 "+repr(__file__))
    system("killall Python\nsleep 2\npython3 "+repr(__file__))

def eta(total_n,min_interval=.3,title="r.eta"):
    # DEMO:
    # a = eta(2000,title='test')
    # for i in range(2000):
    #     sleep(.031)
    #     a(i)
    #
    # This method is slopily written.
    timer=tic()
    interval_timer=[tic()]
    title='\r'+title+": "
    def display_eta(proportion_completed,time_elapsed_in_seconds,TOTAL_TO_CIMPLET,COMPLETSOFAR,print_out=True):
        if interval_timer[0]()>=min_interval:
            interval_timer[0]=tic()
            # Estimated time of arrival printer
            from datetime import timedelta
            out_method=(lambda x:print(x,end='') if print_out else identity)
            temp=timedelta(seconds=time_elapsed_in_seconds)
            completerey="\tProgress: " + str(COMPLETSOFAR) + "/" + str(TOTAL_TO_CIMPLET)
            if proportion_completed<=0:
                return out_method(title +"NO PROGRESS; INFINITE TIME REMAINING. T=" +str(temp) +(completerey))
            # exec(mini_terminal)
            eta=float(time_elapsed_in_seconds) / proportion_completed  # Estimated time of arrival
            etr=eta- time_elapsed_in_seconds # Estimated time remaining
            return out_method(title+(("ETR=" + str(timedelta(seconds=etr)) + "\tETA=" + str(timedelta(seconds=eta)) + "\tT="+str(temp) + completerey if etr > 0 else "COMPLETED IN " + str(temp)+completerey+"\n")))
    def out(n,print_out=True):
        return display_eta(n/total_n,timer(),print_out=print_out,TOTAL_TO_CIMPLET=total_n,COMPLETSOFAR=n)
    return out




# @memoized
def get_all_submodule_names(module):
    #Takes a module and returns a list of strings.
    #Example:
    #    >>> all_submodule_names(np)
    #    ans = ['numpy.core', 'numpy.fft', 'numpy.linalg', 'numpy.compat', 'numpy.conftest', ...(etc)... ]
    #This function is NOT recursive
    #This function IS safe to run (unlike get_all_submodules)
    import types,pkgutil
    assert isinstance(module,types.ModuleType),'This function accepts a module as an input, but you gave it type '+repr(type(module))

    if not hasattr(module,'__path__'):
        return []

    submodule_names=[]
    prefix = module.__name__ + "."
    path   = module.__path__
    for importer, modname, ispkg in pkgutil.iter_modules(path, prefix):
        submodule_names.append(modname)
    return submodule_names

# def get_all_submodules(module,recursive=True):
#     #NOTE: This function is dangerous and may have unintended side-effects if importing a certain module runs unwanted code.
#     #Attempt to return as many imported modules as we can...skip all the ones that have errors when importing...
#     import types,pkgutil,importlib
#     assert isinstance(module,types.ModuleType),'This function accepts a module as an input, but you gave it type '+repr(type(module))

#     def recursion_helper(module):
#         yield module
#         for submodule in all_submodules(module,recursive=False):
#             yield from recursion_helper(submodule)

#     for submodule_name in all_submodule_names(module):
#         try:
#             submodule=importlib.import_module(submodule_name)
#         except:
#             pass
#         else:
#             if recursive:
#                 yield from recursion_helper(submodule)
#             else:
#                 yield submodule

# def get_all_submodule_names(module):  #OLD CODE
#     # SOURCE: https://stackoverflow.com/questions/832004/python-finding-all-packages-inside-a-package
#     return [x.split('.')[1] for x in get_all_submodule_names(module)]
#     dir = os.path.dirname(module.__file__)
#     def is_package(d):
#         d = os.path.join(dir, d)
#         return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))
#     return list(filter(is_package, os.listdir(dir)))

def merged_dicts(*dict_args):
    """
    SOURCE: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def keys_and_values_to_dict(keys,values):
    #EXAMPLE:
    # >>> keys_and_values_to_dict([1,2,3,4],['a','b','c','d'])
    #ans = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    out={}
    for key,value in zip(keys,values):
        out[key]=value
    return out

def get_source_file(object):
    # Might throw an exception
    import inspect
    return inspect.getfile(inspect.getmodule(object))

# region Editor Launchers
def edit(file_or_object,editor_command='atom'):
    if isinstance(file_or_object,str):
        return shell_command(editor_command +" " + repr(file_or_object),as_subprocess=True)# Idk if there's anything worth returning but maybe there is? run_as_subprocess is true so we can edit things in editors like vim, suplemon, emacs etc.
    else:
        return edit(get_source_file(object=file_or_object),editor_command=editor_command)
subl=lambda x:edit(x,'sublime')
atom=lambda x:edit(x,'atom')
vim=lambda x:edit(x,'vim')
# initialize editor methods. Easier to understand when analyzing this code dynamically; static analysis might be really confusing
__known_editors=['vim','emacs','suplemon','atom','sublime']# NONE of these names should intersect any methods or varables in the r module or else they will be overwritten!
for __editor in __known_editors:
    exec("""
def X(file_or_object):
    edit(file_or_object,editor_command='X')""".replace('X',__editor))
del __known_editors,__editor# This is just a setup section to create methods for us, so get rid of the leftovers. __known_editors and __editor are assumed to be unused anywhere else in our current namespace!dz
def xo(file_or_object):# FYI: 'xo' stands for 'exofrills', a console editor. I haven't used it much though. I don't really use console based editors much…
    import xo
    try:
        if not isinstance(file_or_object,str):
            file_or_object=get_source_file(file_or_object)
        xo.main([file_or_object])
    except:
        print("Failed to start exofrills editor")
# endregion
def graph_resistance_distance(n, d, x, y):
    # Originally from Fodor's CSE307 HW 2, Spring 2018
    # d is dictionary to contain graph edges
    # n is number of nodes
    # x is entry node
    # y is exit node
    # Reference: wikipedia.org/wiki/Resistance_distance
    # Example from acmgnyr.org/year2017/problems/G-SocialDist.pdf
    #     graph_resistance_distance(6,{2:(0,1,3),3:(1,4,5),4:(1,5)},1,0) ⟶ 34/21
    e=[[] for _ in range(n)]
    for k in d:
        for i in d[k]:
            e[k].append(i)
            e[i].append(k)
    c = []
    s = len(e)
    for i, l in enumerate(e):
        v = [0]*s
        for j in l:
            v[i] += 1
            v[j] -= 1
        c.append(v)
    r = [0] * s
    r[x] =  1
    r[y] = -1
    m = max(x,y)
    c = [x[:m] + x[m + 1:] for x in c]
    c.pop(0)
    r.pop(0)
    M = [c[i] + [r[i]] for i in range(len(c))]
    M=reduced_row_echelon_form(M)
    return abs(M[min(x,y)][-1])

namespace="set(list(locals())+list(globals())+list(dir()))"  # eval-uable
xrange=range  # To make it more compatiable when i copypaste py2 code

term='pseudo_terminal(locals(),globals())'# For easy access: exec(term). Can use in the middle of other methods!

def is_valid_python_syntax(code,mode='exec'):
    assert isinstance(code,str),'Code should be a string'
    import ast, traceback
    valid = True
    try:
        ast.parse(code,mode=mode)
    except SyntaxError:
        valid = False
    return valid

def _ipython_exeval_maker(scope={}):
    pip_import('IPython','ipython')#Make sure we have ipython
    from IPython.terminal.embed import InteractiveShellEmbed as Shell
    shell=Shell(user_ns=scope)
    shell.showtraceback = lambda *args,**kwargs:None
    def ipython_exeval(code,_ignored_1,_ignored_2):
        # fansi_print(scope,'yellow')
        result=shell.run_cell(code)#,silent=True)#silent=True avoids making variables like _,__ etc that ipython typically does
        exception=result.error_before_exec or result.error_in_exec
        if exception:
            if not isinstance(exception,SyntaxError):#If it is a syntaxerror, ipython will print its own error...and then we would print 2 errors...
                raise exception
        return result.result
    return ipython_exeval
_ipython_exeval=None

# region This section MUST come last! This is for if we're running the 'r' class as the main thread (runs pseudo_terminal)―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
def exeval(code,*dicts,exec,eval,tictoc=False,profile=False,ipython=False):
    # Evaluate or execute within descending hierarchy of dicts
    # merged_dict=merged_dicts(*reversed(dicts))# # Will merge them in descending priority of dicts' namespaces
    # region HOPEFULLY just a temporary patch
    # assert len(dicts)<=1
    # if len(dicts)<=1:
    # print("exeval")
    merged_dict=dicts[0]
    # endregion

    if profile:
        pyinstrument=pip_import('pyinstrument')#https://github.com/joerick/pyinstrument
        profiler = pyinstrument.Profiler()
        profiler.start()

    if ipython:
        exec=eval=_ipython_exeval
    import rp.patch_linecache as patch
    from time import time as _time
    _end_time=None
    try:
        try:
            if is_valid_python_syntax(code,mode='eval'):
                _start_time=_time()
                ans=patch.run_code(code,'eval',merged_dict,eval)
                # ans=eval(code,merged_dict,merged_dict)
                _end_time=_time()
            else:
                _start_time=_time()
                ans=patch.run_code(code,'exec',merged_dict,exec)
                # ans=exec(code,merged_dict,merged_dict)# ans = None unless using ipython, in which case it might not be
                _end_time=_time()
        finally:
            if tictoc:
                fansi_print("TICTOC: "+('%.5f'%((_end_time or _time())-_start_time)).ljust(10)[:10]+' seconds','blue','bold')
        for d in dicts:# Place updated variables back in descending order of priority
            temp=set()
            for k in d:
                if k in merged_dict:
                    d[k]=merged_dict.pop(k)
                else:
                    temp.add(k)
            for k in temp:
                del d[k]
        for k in merged_dict:# If we declared new variables, put them on the top-priority dict
            dicts[0][k]=merged_dict[k]
        return ans,None
    except BaseException as e:
        if ipython:
            pop_exception_traceback(e,1)
        pop_exception_traceback(e,2)
        return None,e
    finally:
        if profile:
            if (_end_time or _time())-_start_time>1/1000:#Only show profiler data if it takes more than a millisecond to run your code...
                profiler.stop()
                prof_display_start_time=_time()
                fansi_print("Preparing the PROF display (the profiler, toggle with PROF)...",'blue','underlined')
                print(profiler.output_text(unicode=True, color=True,timeline=False,show_all=_PROF_DEEP).replace('\n\n','\n')[1:-1])#show_all is useful but SOOO verbose it's almost unbearable...
                fansi_print("...took "+str(_time()-prof_display_start_time)+" seconds to diplay the PROF output",'blue','underlined')
_PROF_DEEP=False

# def parse(code):
#     # Takes care ofmillisecond to run your code...:
#     #   - Lazy parsers
#     #   - Indentation fixes
#     #   -
#     pass

def dec2bin(f):
    # Works with fractions
    # SOURCE: http://code.activestate.com/recipes/577488-decimal-to-binary-conversion/
    import math
    if f >= 1:
        g = int(math.log(float(f), 2))
    else:
        g = -1
    h = g + 1
    ig = math.pow(2, g)
    st = ""
    while f > 0 or ig >= 1:
        if f < 1:
            if len(st[h:]) >= 10: # 10 fractional digits max
                break
        if f >= ig:
            st = st + "1"
            f = f - ig
        else:
            st += "0"
        ig /= 2
    st = st[:h] + "." + st[h:]
    return sxt

if __name__=='__main__':fansi_print("Booting rp...",'blue','bold',new_line=False)
import rp.rp_ptpython.prompt_style as ps
from rp.prompt_toolkit.shortcuts import create_eventloop#Unless this can be sped up (inlining just pushes the problem to the next imoprt)
        # def create_eventloop(inputhook=None, recognize_win32_paste=True):
        #     """
        #     Create and return an
        #     :class:`~prompt_toolkit.eventloop.base.EventLoop` instance for a
        #     :class:`~prompt_toolkit.interface.CommandLineInterface`.
        #     """
        #     def is_windows():
        #         """
        #         True when we are using Windows.
        #         """
        #         return sys.platform.startswith('win')  # E.g. 'win32', not 'darwin' or 'linux2'

        #     if is_windows():
        #         from rp.prompt_toolkit.eventloop.win32 import Win32EventLoop as Loop
        #         return Loop(inputhook=inputhook, recognize_paste=recognize_win32_paste)
        #     else:
        #         from rp.prompt_toolkit.eventloop.posix import PosixEventLoop as Loop
        #         return Loop(inputhook=inputhook)
from rp.rp_ptpython.python_input import PythonCommandLineInterface,PythonInput as Pyin
Đ_python_input_eventloop = None  # Singleton for python_input
Đ_ipython_shell = None  # Singleton for python_input
pyin=None# huge speed increase when using this as a singleton
_iPython=False
_printed_a_big_annoying_pseudo_terminal_error=False

# Đ_pseudo_terminal_settings_file=__file__+".pseudo_terinal_settings"
# _pseudo_terminal_settings={
# "pyin.enable_history_search":True,
# "pyin.highlight_matching_parenthesis":True,
# "pyin.enable_input_validation":False,
# "pyin.enable_auto_suggest":True,
# "pyin.show_line_numbers":True,
# "pyin.show_signature":True,
# }
# def _load_pseudo_terminal_settings_from_file(file=None):
#     import ast
#     global _pseudo_terminal_settings
#     _pseudo_terminal_settings=eval(text_file_to_string(file or Đ_pseudo_terminal_settings_file))
#     return None
# def _save_pseudo_terminal_settings_to_file(file=None):
#     import ast
#     global _pseudo_terminal_settings
#     string_to_text_file(file or Đ_pseudo_terminal_settings_file,repr(_pseudo_terminal_settings))
#     return None


def _multi_line_python_input(prompt):
    #Enter '/' to enter after entering a multiline prompt, and '\' to delete the previous line
    def mli(p):#multilineinput
        from re import fullmatch as re
        ol=[]#output lines
        mlm= lambda x: re(r'( +.*)|(.*[\;\:] *)',x)#multi line marker
        bkl= '\\'#back line
        ent= '/'#enter
        st=True#started
        while True:
            i=input(p if not ol else '')#input
            if i!=ent and i!=bkl:
                if set(i)<={';',' '}:#Just spaces and ';'s will just be used to create a new line; nothing more
                    ol.append('')
                else:
                    ol.append(i)
            if i==ent or not mlm(i) and st:
                break
            st=False
            if i==bkl and ol:
                ol=ol[:-1]
                if ol:
                    print(p+ol[0])
                    if len(ol)>1:
                        for l in ol[1:]:
                            print(l)
                if not ol:
                    return ''
        return line_join(ol)
    return mli(prompt)

    #Simple version:
    out=input(prompt)
    if out!=out.lstrip() or out.endswith(':') or out.endswith(';'):
        return out+'\n'+_multi_line_python_input(' '*len(prompt))
    return out

_default_pyin_settings=dict(
enable_mouse_support=False,
enable_history_search=True,
highlight_matching_parenthesis=True,
enable_input_validation=False,
enable_auto_suggest=True,
show_line_numbers=True,
show_signature=True,
_current_ui_style_name='default',
_current_code_style_name='default',

show_docstring=False,
show_realtime_input=False,
show_vars=False,
show_meta_enter_message=True,
completion_visualisation='multi-column' if not currently_running_windows() else 'pop-up',
completion_menu_scroll_offset=1,

show_status_bar=True,
wrap_lines=True,
complete_while_typing=True,
vi_mode=False,
paste_mode=False  ,
confirm_exit=True  ,
accept_input_on_enter=2  ,
enable_open_in_editor=True,
enable_system_bindings=True,
    )
_pyin_settings_file_path=__file__+'.rp_pyin_settings'
def _load_pyin_settings_file():
    try:
        settings=eval(text_file_to_string(_pyin_settings_file_path))
        for setting in _default_pyin_settings:
            assert setting in settings
    except:
        settings=_default_pyin_settings.copy()

    def _load_pyin_settings_from_dict(d):
        pyin.use_ui_colorscheme(d['_current_ui_style_name'])
        pyin.use_code_colorscheme(d['_current_code_style_name'])
        for attr in _default_pyin_settings:
            setattr(pyin,attr,d[attr])

    _load_pyin_settings_from_dict(settings)

def _save_pyin_settings_file():
    settings={}
    for attr in _default_pyin_settings:
        settings[attr]=getattr(pyin,attr)
    string_to_text_file(_pyin_settings_file_path,repr(settings))

def _delete_pyin_settings_file():
    delete_file(_pyin_settings_file_path)


_pt_pseudo_terminal_init_settings=False
history_filename=__file__ + ".history.txt"
def python_input(scope,header='',enable_ptpython=True,iPython=False):
    import rp.rp_ptpython.completer as completer
    # print(completer.completion_cache_pre_origin_doc.keys())
    completer.completion_cache_pre_origin_doc={'':tuple(scope())}#clear the cache because variables might change between inputs (in fact, almost certainly they will). BUT for a speed boost, we'll pre-calculate the initial autocompletion now, because we know it starts with an empty string and should be the scope when doing that.
    global Pyin
    global pyin,_iPython
    global _printed_a_big_annoying_pseudo_terminal_error
    if not enable_ptpython or _printed_a_big_annoying_pseudo_terminal_error:
        return _multi_line_python_input(header)
    try:
        if iPython:
            from rp.rp_ptpython.ipython import IPythonInput as Pyin,InteractiveShellEmbed
            global Đ_ipython_shell
            if Đ_ipython_shell is None:
                Đ_ipython_shell=InteractiveShellEmbed()
            if not pyin or _iPython!=iPython:
                pyin=Pyin(Đ_ipython_shell,get_globals=scope,history_filename=history_filename)
        else:
            if not pyin or _iPython!=iPython:
                # exec(mini_terminal)
                from rp.rp_ptpython.python_input import PythonCommandLineInterface,PythonInput as Pyin
                pyin=Pyin(get_globals=scope,history_filename=history_filename)
        _iPython=iPython
        global Đ_python_input_eventloop
        # global _pseudo_terminal_settings
        global _pt_pseudo_terminal_init_settings
        if not _pt_pseudo_terminal_init_settings:
            _load_pyin_settings_file()
            _pt_pseudo_terminal_init_settings=True

        pyin.all_prompt_styles['default']=ps.PseudoTerminalPrompt()
        if not currently_running_windows():
            pyin.prompt_style='default'
        # ps.PseudoTerminalPrompt=PseudoTerminalPrompt

        Đ_python_input_eventloop=Đ_python_input_eventloop or PythonCommandLineInterface(create_eventloop(),python_input=pyin)
        #
        # try:
        code_obj = Đ_python_input_eventloop.run()
        # gotta_save=False#Sorry about this clusterfuck of code. I'm really tired, and this code really doesn't affect anybody else in the whole world but me...and I know how it works, despite how yucky it is. (my ide makes it really easy to write this way with multiple cursors)
        # if _pseudo_terminal_settings["pyin.enable_history_search"]!=pyin.enable_history_search:_pseudo_terminal_settings["pyin.enable_history_search"]=pyin.enable_history_search;gotta_save=True;print("CHANGESD")
        # if _pseudo_terminal_settings["pyin.highlight_matching_parenthesis"]!=pyin.highlight_matching_parenthesis:_pseudo_terminal_settings["pyin.highlight_matching_parenthesis"]=pyin.highlight_matching_parenthesis;gotta_save=True;print("CHANGESD")
        # if _pseudo_terminal_settings["pyin.enable_input_validation"]!=pyin.enable_input_validation:_pseudo_terminal_settings["pyin.enable_input_validation"]=pyin.enable_input_validation;gotta_save=True;print("CHANGESD")
        # if _pseudo_terminal_settings["pyin.enable_auto_suggest"]!=pyin.enable_auto_suggest:_pseudo_terminal_settings["pyin.enable_auto_suggest"]=pyin.enable_auto_suggest;gotta_save=True;print("CHANGESD")
        # if _pseudo_terminal_settings["pyin.show_line_numbers"]!=pyin.show_line_numbers:_pseudo_terminal_settings["pyin.show_line_numbers"]=pyin.show_line_numbers;gotta_save=True;print("CHANGESD")
        # if _pseudo_terminal_settings["pyin.show_signature"]!=pyin.show_signature:_pseudo_terminal_settings["pyin.show_signature"]=pyin.show_signature;gotta_save=True;print("CHANGESD")
        # if gotta_save:_save_pseudo_terminal_settings_to_file()

        return code_obj.text
    except EOFError:
        fansi_print("Caught EOFError ⟹ RETURN",'blue','bold')# Presumably in ptpython when you use control+d and then select yes; AKA the exit prompt they built
        return "RETURN"
    except Exception as E:
        if not _printed_a_big_annoying_pseudo_terminal_error:
            if not running_in_google_colab():#No reason to scare
                print_stack_trace(E)
                fansi_print("The prompt_toolkit version of pseudo_terminal crashed; reverting to the command-line version...",'cyan','bold')
            else:
                fansi_print("Defaulting to the command-line version because you're running in google colab...",'cyan','bold')
            _printed_a_big_annoying_pseudo_terminal_error=True

        return input(header)
class pseudo_terminal_style:
    def __init__(self):
        self.message="pseudo_terminal() ⟹ Entering interactive session! "
"""
TODO:
    - Does NOT return anything
    - Can be used like MiniTerminal
    - But should be able to accept arguments for niche areas! Not sure how yet; should be modular though somehow...
    - History for every variable
    - Scope Hierarchy: [globals(),locals(),others()]:
        - Create new dict that's the composed of all the others then update them accordingly
    - HIST: Contains a list of dicts, whose differences can be seen

"""

class _Module:
    def __init__(self,name,module):
        from inspect import getsourcefile
        self.name=name
        self.module=module
        self.path=getsourcefile(module)
        self.date_last_updated=get_current_date()
        if not isinstance(self.path,str):
            raise TypeError()
    def update(self):
        #Will check to see if the module is out of date. If it is, it will reload it.
        if date_modified(self.path)>self.date_last_updated:
            try:
                #We should reload this module
                from time import time as __time__
                starttime=__time__()
                fansi_print('RELOAD: Reloading module '+repr(self.name)+'...','blue','bold',new_line=False)
                from importlib import reload
                reload(self.module)
                fansi_print('done in '+str(__time__()-starttime)[:10]+' seconds!','blue','bold')
            except BaseException as e:
                fansi_print('RELOAD: ERROR: Failed to reload module '+repr(self.name)+"\nStack trace shown below:",'blue','bold')
                print_stack_trace(e)
            self.date_last_updated=get_current_date()
    def __hash__(self):
        return self.name
_modules={}
def _reload_modules():
    #Re-import any modules that have been modified after the last time we called _reload_modules
    for name,module in sys.modules.items():
        if name not in _modules:
            try:
                _modules[name]=_Module(name,module)
            except TypeError:pass
            except Exception as e:
                print_stack_trace(e)
        else:
            _modules[name].update()


def pseudo_terminal(*dicts,get_user_input=python_input,modifier=None,style=pseudo_terminal_style(),enable_ptpython=True,eval=eval,exec=exec):
    try:
        import signal
        signal.signal(signal.SIGABRT,lambda:"rpy: pseudo terminal: sigabrt avoided!")
    except Exception as E:
        fansi_print("Warning: This pseudo_terminal is being started in a separate thread",'yellow')
        # print_stack_trace(E)
    import re

    # TODO: Make better error reports than are available by default in python! Let it debug things like nested parenthesis and show where error came from instead of just throwing a tantrum.
    # @author: Ryan Burgert 2016，2017，2018
    try:
        import readline# Makes pseudo_terminal nicer to use if in a real terminal (AKA if using pseudo_terminal on the terminal app on a mac); aka you can use the up arrow key to go through history etc.
        import rlcompleter
        readline.parse_and_bind("tab: complete")#Enable autocompletion even with PT OFF https://docs.python.org/2/library/rlcompleter.html
    except:
        pass# Not important if it fails, especially on windows (which doesn't support readline)
    # from r import fansi_print,fansi,space_split,is_literal,string_from_clipboard,mini_editor,merged_dicts,print_stack_trace# Necessary imports for this method to function properly.
    import rp.r_iterm_comm# Used to talk to ptpython

    def level_label(change=0):
        return (("(Level "+str(rp.r_iterm_comm.pseudo_terminal_level+change)+")")if rp.r_iterm_comm.pseudo_terminal_level else "")
    try:
        fansi_print(style.message + level_label(),'blue','bold')
        rp.r_iterm_comm.pseudo_terminal_level+=1

        from copy import deepcopy,copy

        def dictify(d):# If it's an object and not a dict, use it's __dict__ attribute
            if isinstance(d,dict):
                return d
            return d.__dict__
        dicts=[get_scope(1)]
        dicts[0]['ans']=None
        # dicts=[{"ans":None,'blarge':1234}]#,*map(dictify,dicts)]# Keeping the 'ans' variable separate. It has highest priority

        def dupdate(d,key,default=None):  # Make sure a key exists inside a dict without nessecarily overwriting it
            if key not in d:
                d[key]=default
        try:
            dupdate(dicts[0],'ans')
        except:pass

        def scope():
            return merged_dicts(*reversed(dicts))

        def equal(a,b):
            if a is b:
                return True

            try:
                if get_bytecode(a)==get_bytecode(b)!=get_bytecode(None):# becaue get_bytecode(None)==get_bytecode(3)==get_bytecode(3498234)
                    return True# Don't return false otherwise
            except:pass
            try:
                try:
                    import numpy as np
                    if isinstance(a,np.ndarray) or isinstance(b,np.ndarray):
                        if isinstance(a,np.ndarray) != isinstance(b,np.ndarray):
                            return False
                        if isinstance(a,np.ndarray) and isinstance(b,np.ndarray):
                            if not a.shape==b.shape:
                                return False
                        return np.all(a==b)
                except:
                    pass
                if a==b:
                    return True
                # else:
                #     exec(mini_terminal)
                return a==b # Fails on numpy arrays
            except:pass
            return a is b # Will always return SOMETHING at least

        def deep_dark_dict_copy(d):
            # out={}
            # for k in d:
            #     out[k]=d[k]
            # return out
            out={}
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")# /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/copy.py:164: RuntimeWarning: use movie: No module named 'pygame.movie'
                for k in d:
                    try:
                        import types
                        if isinstance(d[k],types.ModuleType):
                            raise Exception# When copying xonsh, the process below was reallly really slow. These are just some special cases worth putting out there to optimize this method.
                        try:
                            q=deepcopy(d[k])
                            if equal(d[k],q):
                                out[k]=deepcopy(d[k])
                            else:
                                raise Exception
                        except:
                            # print("Deepcopy failed: "+k)
                            q=copy(d[k])
                            if equal(d[k],q):
                                out[k]=copy(d[k])
                            else:
                                raise Exception
                    except:
                        # print("Copy failed: "+k)
                        out[k]=d[k]# Failed to copy
            return out

        def get_snapshot():# Snapshot of our dicts/scope
            # exec(mini_terminal)
            return list(map(deep_dark_dict_copy,dicts))
        def set_snapshot(snapshot):
            # snapshot is a list of dicts to replace *dicts
            for s,d in zip(snapshot,dicts):
                assert isinstance(d,dict)
                assert isinstance(s,dict)
                sk=set(s)  # snapshot keys
                dk=set(d)  # dict keys
                changed=False
                for k in dk-sk :  # -{'__builtins__'}:# '__builtins__' seems to be put there as a consequence of using eval or exec, no matter what we do with it. It also is confusing and annoying to see it pop up when reading the results of UNDO
                    # assert isinstance(k,str)
                    print(fansi("    - Removed: ",'red')+k)
                    changed=True
                    del d[k]
                for k in sk-dk :  # -{'__builtins__'}:
                    # assert isinstance(k,str)
                    print(fansi("    - Added: ",'green')+k)
                    changed=True
                    d[k]=s[k]
                for k in dk&sk :  # -{'__builtins__'}:
                    assert k in dk
                    assert k in sk
                    assert isinstance(k,str)
                    if not equal(s[k],d[k]):# To avoid spam
                        print(fansi("    - Changed: ",'blue')+k)
                        changed=True
                        d[k]=s[k]
                return changed
        gave_undo_warning=False
        def take_snapshot():
            nonlocal gave_undo_warning
            start=tic()
            if snapshots_enabled:
                snapshot_history.append(get_snapshot())
            if not gave_undo_warning and start()>.25:#.25 seconds is way too long to wait for a new prompt. We're delaying the prompt, and this can get annoying quickly...
                fansi_print("NOTE: ",'blue','bold',new_line=False)
                fansi_print("pseudo_terminal took "+str(start())[:5]+" seconds to save the UNDO snapshot, which might be because of a large namespace. If your prompts are lagging, this is probably why. You can fix this by using 'UNDO ALL', 'UNDO OFF'. This message will only show once.",'blue','bold')
                gave_undo_warning=True

        def get_ans():
            dupdate(dicts[0],'ans')
            return  dicts[0]['ans']# This should exist

        # A little python weridness demo: ⮤print(999 is 999)⟶True BUT ⮤a=999⮤print(a is 999)⟶False
        use_ans_history=True
        def set_ans(val,save_history=True,snapshot=True):
            import rp.r_iterm_comm as ric
            ric.ans=val
            save_history&=use_ans_history
            dupdate(dicts[0],'ans')
            if snapshot:# default: save changes in a snapshot BEFORE making modifications to save current state! snapshot_history is independent of ans_history
                take_snapshot()
            if save_history:
                ans_history.append(val)
            dicts[0]['ans']=val
            val_str=str(val)
            try:
                import numpy as np
                set_numpy_print_options(linewidth=max(0,get_terminal_width()-len('ans = ')))#Make for prettier numpy printing, by dynamically adjusting the linewidth each time we enter a command
                if isinstance(val,np.ndarray) and len(line_split(val_str))>1:
                    #It will take more than one line to print this numpy array.
                    #Example:
                    #    ans = [[ 1 -3 -5  0  0  0]
                    #    [ 0  1  0  1  0  0]
                    #    [ 0  0  2  0  1  0]
                    #    [ 0  3  2  0  0  1]]
                    #The above is ugly, because the top row isn't aligned with the others, because it takes up multiple lines.
                    #There's a way to handle it, which prevents a line containing just 'ans=' from existing:
                    val_str=line_split(val_str)
                    val_str=[val_str[0]]+[' '*len('ans = ')+line for line in val_str[1:]]
                    val_str='\n'.join(val_str,)
                    #The result:
                    #    ans = [[ 1 -3 -5  0  0  0]
                    #           [ 0  1  0  1  0  0]
                    #           [ 0  0  2  0  1  0]
                    #           [ 0  3  2  0  0  1]]
                    #Which is much prettier.
            except:pass#print("Failed to set numpy width")# AttributeError: readonly attribute '__module__'
            fansi_print("ans = " + val_str,('green'if save_history else 'yellow')if use_ans_history else 'gray')

        def print_history():
            fansi_print("HISTORY ⟹ Here is a list of all valid python commands you have entered so far (green means it is a single-line command, whilst yellow means it is a multi-lined command):",'blue','underlined')
            flipflop=False
            for x in  successful_command_history:
                multiline='\n' in x
                if x.strip():#And x.strip() because we don't want to alternate bolding if it's invisible cause then it would look like we have two bold in a row
                    flipflop=not flipflop#Print every other yellow prompt in bold
                fansi_print(x,'yellow' if multiline else'green','bold' if multiline and flipflop else None)  # Single line commands are green, and multi-line commands are yellow

        def show_error(E):
            nonlocal error,display_help_message_on_error,error_message_that_caused_exception
            if display_help_message_on_error:
                display_help_message_on_error=False
                fansi_print("""Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command aborted.
            Type 'HELP' for instructions on how to use pseudo_terminal in general.
            To see the full traceback of any error, type either 'MORE' or 'MMORE' (or alt+m as a shortcut).
            NOTE: This will be the last time you see this message, unless you enter 'HELP' without quotes.""",'red','bold')
            error_message_that_caused_exception=user_message# so we can print it in magenta if asked to by 'MORE'
            print_stack_trace(E,False,'ERROR: ')
            error=E
        error_message_that_caused_exception=None
        display_help_message_on_error=True# A flag that will turn off the first time it displays "Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command aborted. Type 'HELP' for instructions on pseudo_terminal. To see the full error traceback, type 'MORE'." so that we don't bombard the user with an unnessecary amount of stuff
        successful_command_history=[]
        all_command_history=[]
        snapshot_history=[]
        ans_redo_history=[]
        snapshots_enabled=False#Turning this on can break flann_dict. I haven't investigated why. Heres's some code that can break with it turned on:
        # (Example code)       f=FlannDict()
        # (Example code)       for _ in range(2000):
        # (Example code)           f[randint(100),randint(100)]=randint(100)
        # (Example code)       ans=f[34,23]
        # (Example code)       ans=f[34,23]
        # (Example code)       ans=f[34,23]
        # (Example code)       ans=f[34,23]
        ans_history=[]
        _tictoc=False
        _profiler=False
        _use_ipython_exeval=False
        user_created_var_names=set()
        allow_keyboard_interrupt_return=False
        use_modifier=True# Can be toggled with pseudo_terminal keyword commands, enumerated via 'HELP'
        error=None# For MORE
        last_assignable=last_assignable_candidate=None
        assignable_history={}
        do_garbage_collection_before_input=False#I'm going to see if this makes it faster when doing stuff with pytorch
        _reload=False#If this is true, call _reload_modules right before each exeval is called
        # garbage_collector_timer=tic()

        try:
            #TODO: For some reason psuedo_terminal doesnt capture the scope it was called in. IDK why. Fix that. The next few lines are a patch and should eventually not be nesecay once bugs are fixed.
            exeval("None",*dicts,exec=exec,eval=eval)#I don't know why this is necessary (and haven't really tried to debug it) but without running something before importing all from rp nothihng works....
            exeval("from rp import *",*dicts,exec=exec,eval=eval)#Try to import RP
        except BaseException as e:
            print("PSEUDO TERMINAL ERROR: FAILED TO IMPORT RP...THIS SHOULD BE IMPOSSIBLE...WAT")
            print_stack_trace(e)
        def add_to_successful_command_history(x):
            successful_command_history.append(x)
            import rp.r_iterm_comm
            rp.r_iterm_comm.successful_commands=successful_command_history.copy()
        try:
            import rp.r_iterm_comm
            rp.r_iterm_comm.globa=scope()#prime it and get it ready to go (before I had to enter some valid command like '1' etc to get autocomplete working at 100%)
            while True:
                try:
                    # region Get user_message, xor exit with second keyboard interrupt
                    try:
                        def evaluable_part(cmd:str):
                            # DOesn't take into account the ';' character
                            cmd=cmd.rstrip().split('\n')[-1]
                            # TODO Make everything evaluable like in ipython
                        # region Communicate with ptpython via r_iterm_comm
                        def try_eval(x,true=False):# If true==True, then we return the actual value, not a formatted string
                            if x==rp.r_iterm_comm.try_eval_mem_text:
                                return rp.r_iterm_comm.rp_evaluator_mem# Text hasn't changed, so don't evaluate it again
                            rp.r_iterm_comm.try_eval_mem_text=x
                            temp=sys.stdout.write
                            try:
                                sys.stdout.write=_muted_stdout_write
                                s=scope()
                                # true_value=eval(x,merged_dicts(s,globals(),locals()))
                                if x.count('RETURN')==1:
                                    exec(x.split('RETURN')[0],rp.r_iterm_comm.globa)# If we have a RETURN in it,
                                    x=x.split('RETURN')[1].lstrip()# lstrip also removes newlines
                                out="eval("+repr(x)+") = \n"
                                true_value=eval(x,rp.r_iterm_comm.globa)
                                if true:
                                    return true_value
                                from pprint import pformat
                                out=out+(str if isinstance(true_value,str) else repr)((true_value))  # + '\nans = '+str(dicts[0]['ans'])
                                rp.r_iterm_comm.rp_evaluator_mem=out
                                return str(out)+"\n"
                            except Exception as E:
                                return str(rp.r_iterm_comm.rp_evaluator_mem)+"\nERROR: "+str(E)
                            finally:
                                sys.stdout.write=temp
                        rp.r_iterm_comm.rp_evaluator=try_eval
                        rp.r_iterm_comm.rp_VARS_display=str(' '.join(sorted(list(user_created_var_names))))
                        # endregion
                        import gc as garbage_collector
                        if do_garbage_collection_before_input:
                            garbage_collector.collect()#Sometimes we run into memory issues, maybe this is what's making it slow when using pytorch and big tensors?
                            # print("GC!")
                            # garbage_collector_timer=tic()
                        user_message=get_user_input(lambda:scope(),header=_get_prompt_style(),enable_ptpython=enable_ptpython)
                        try:set_numpy_print_options(linewidth=max(0,get_terminal_width()-len('ans = ')))#Make for prettier numpy printing, by dynamically adjusting the linewidth each time we enter a command
                        except:pass#print("Failed to set numpy width")
                        if not user_message:
                            continue# A bit of optimization for aesthetic value when we hold down the enter key
                        allow_keyboard_interrupt_return=False
                    except KeyboardInterrupt:
                        if allow_keyboard_interrupt_return:
                            fansi_print("Caught repeated KeyboardInterrupt ⟹ RETURN",'cyan','bold')
                            while True:
                                try:
                                    if input_yes_no("Are you sure you want to RETURN?"):
                                        user_message="RETURN"
                                        break
                                    else:
                                        break
                                except:
                                    print("<KeyboardInterrupt>\nCaught another KeyboardInterrupt...if you'd like to RETURN, please enter 'yes'")
                                    pass
                        else:
                            allow_keyboard_interrupt_return=True
                            raise
                    # endregion
                    user_created_var_names&=set(scope())# Make sure that the only variables in this list actually exist. For example, if we use 'del' in pseudo_terminal, ∄ code to remove it from this list (apart from this line of course)
                    # region Non-exevaluable Terminal Commands (Ignore user_message)
                    if user_message == 'RETURN':
                        if get_ans() is None:
                            fansi_print("r.pseudo_terminal() ⟹ Session end. No value returned.",'blue','bold')
                        else:
                            fansi_print("r.pseudo_terminal() ⟹ Session end. Returning ans = " + str(get_ans()),'blue','bold')
                        return get_ans()
                    elif user_message=='HHELP':
                        fansi_print("HHELP --> Displaying full documentation for rp:",'blue','bold')
                        import rp
                        ans=rp.__file__
                        ans=get_parent_directory(ans)
                        ans=path_join(ans,'documentation.py')
                        ans=text_file_to_string(ans)
                        ans=ans.replace('\t','    ')
                        try:
                            string_pager(ans)
                        except:
                            print(ans)
                        fansi_print("HHELP --> Finished printing documentation.",'blue','bold')

                    elif user_message == 'HELP':
                        def columnify_strings(strings_input):
                            height=30#Total height of output
                            spacing=' '*4#Spacing between columns
                            #strings_input is a string separated by newlines and double-newlines
                            assert isinstance(strings_input,str)
                            strings_input=strings_input.strip()
                            for _ in range(100) :
                                strings_input=strings_input.replace('\n\n\n','\n\n')
                            strings=strings_input.split('\n\n')
                            bl=strings
                            o=[]
                            s=[]
                            for l in bl:
                                l=horizontally_concatenated_strings(l,spacing,rectangularize=True)
                                l=l.strip()
                                #l+='\n'
                                if (line_join(s+[l])).count('\n')<=height:
                                    s+=[l,'']
                                else:
                                    o+=[line_join(s)]
                                    s=[l,'']
                            if s:
                                o+=[line_join(s)]
                            ans=horizontally_concatenated_strings(o,rectangularize=True)
                            return ans
                        strings_input="""
                        <Input Modifier>
                        MODIFIER ON
                        MODIFIER OFF
                        MODIFIER SET
                        SMODIFIER SET

                        <Stack Traces>
                        MORE
                        MMORE
                        DMORE

                        <Command History>
                        HISTORY
                        AHISTORY
                        GHISTORY
                        CHISTORY

                        <Clipboard>
                        COPY
                        PASTE
                        SPASTE

                        <'ans' History>
                        NEXT
                        PREV
                        PREV ON
                        PREV OFF
                        PREV CLEAR
                        PREV ALL

                        <Namespace History>
                        UNDO
                        UNDO ON
                        UNDO OFF
                        UNDO CLEAR
                        UNDO ALL

                        <Prompt Toolkit>
                        PT ON
                        PT OFF

                        <Saving Settings>
                        PT SAVE
                        PT RESET
                        SET STYLE

                        <Shell Commands>
                        !
                        !!

                        <Inspection>
                        ?/
                        ?.
                        ?
                        ??
                        ???
                        ????
                        ?????

                        <Simple Timer>
                        TICTOC
                        TICTOC ON
                        TICTOC OFF

                        <Profiler>
                        PROF
                        PROF ON
                        PROF OFF
                        PROF DEEP

                        <Toggle Colors>
                        FANSI ON
                        FANSI OFF

                        <Others>
                        RETURN
                        SUSPEND
                        SHELL
                        LEVEL
                        DITTO
                        EDIT
                        VARS
                        RANT
                        FORK
                        ARG

                        <File System>
                        CD
                        LS
                        PWD
                        CAT
                        RUN
                        CDP
                        CPWD
                        NCAT
                        CCAT
                        OPEN

                        <Documentation>
                        HELP
                        HHELP

                        <Module Reloading>
                        RELOAD ON
                        RELOAD OFF

                        <Deprecated>
                        IPYTHON
                        IPYTHON ON
                        IPYTHON OFF
                        RETURN NOW
                        GC OFF
                        GC ON
                        """
                        strings_input=lrstrip_all_lines(strings_input)
                        command_list=columnify_strings(strings_input)

                        display_help_message_on_error=True# Seems appropriate if they're looking for help
                        fansi_print("HELP ⟹ Here are the instructions:",'blue','underlined')
                        fansi_print("""    For those of you unfamiliar, this will basically attempt to exec(input()) repeatedly.",'blue')
        For more documentation, type 'HHELP'
        Note that you must import any modules you want to access; this terminal runs inside a def.
            If the command you enter returns a value other than None, a variable called 'ans' will be assigned that value.
        If the command you enter returns an error, pseudo_terminal will try to fix it, and if it can't it will display a summary of the error.
        To set different prompt styles, use set_prompt_style(' >> ') or set_prompt_style(' ⮤ ') etc. This currently only works with PT ON. This setting will be saved between sessions.
        To launch the debugger, type debug() on the top of your code. HINT: Typing the microcompletion '\\de' will toggleååååå this for you.
        Enter 'HISTORY' without quotes to get a list of all valid python commands you have entered so far, so you can copy and paste them into your code.
        Enter 'PASTE' without quotes to run what is copied to your clipboard, allowing you to run multiple lines at the same time
        Enter 'MORE' without quotes to see the full error traceback of the last error, assuming the last attempted command caused an error.
        Enter 'RETURN' without quotes to end the session, and return ans as the output value of this function.
        Games: Type 'import pychess', 'import snake', 'import py2048', 'import sudoku', 'import mario', 'import tetris', or 'import flappy' (Tetris has to be fixed, its currently a big buggy)
        Enter 'CD directory/path/etc' to cd into a directory, adding it to the system path (so you can use local imports etc with RUN)
        Enter 'RUN pythonfile.py -arg1 --args --blah' to run a python file with the given args
        Enter 'PT OFF' to turn prompt-toolkit off. This saves battery life, and has less features. It's the default when using a non-tty command line
        When PT OFF, use '\\' to delete previous line of input and '/' to enter a multiline input. Yes, you can use multi-line even if PT OFF.
        Enter 'EDIT0' or 'EDIT1' etc to edit the n'th last entry in an external editor (for multiline input when PT OFF)
        Enter 'import shotgun' to attempt to pip-install a bunch of useful optional dependencies
        Note: rinsp is automatically imported into every pseudo_terminal instance; use it to debug your code really easily!
        "rinsp ans 1" is parsed to "rinsp(ans,1)" for convenience (generalized to literals etc)
        "+ 8" is parsed to "ans + 8" and ".shape" is parsed into
        play_sound_from_samples([.1,.2,.3,.4,.5,.5,.6,.6,.6,.6,.6,.6,.6,.6]*238964,3000) ⟵ Play that sound or something like it to debug speed in rp
        ALL COMMANDS:\n"""+indentify(command_list,' '*4*3), "blue")
        # Other commands: 'MODIFIER ON', 'MODIFIER OFF', 'SMODIFIER SET', 'MODIFIER SET', 'VARS', 'MORE', 'MMORE', 'RETURN NOW', 'EDIT', 'AHISTORY', GHISTORY', 'COPY', 'SPASTE', 'CHISTORY', 'DITTO', 'LEVEL', 'PREV', 'NEXT', 'UNDO', 'PT ON', 'PT OFF', 'RANT', '!', '!!', '?/', '?.', '?', '??', '???', '????', '?????','SHELL', 'IPYTHON', 'UNDO ALL', 'PREV ALL', 'UNDO ON', 'UNDO OFF', 'PREV ON', 'PREV OFF', 'PREV CLEAR', 'UNDO CLEAR', 'GC ON', 'GC OFF', 'SUSPEND', 'TICTOC ON', 'TICTOC OFF', 'TICTOC', 'FANSI ON', 'FANSI OFF', 'RUN', 'CD', 'PROF ON', 'PROF OFF', 'PROF', 'IPYTHON ON', 'IPYTHON OFF', 'PROF DEEP', 'SET STYLE', 'PT SAVE', 'PT RESET', 'RELOAD ON', 'RELOAD OFF', 'PWD', 'CPWD', 'LS', 'FORK'

                    elif user_message =='PT SAVE':
                        try:
                            fansi_print("Saving your Prompt-Toolkit-based GUIs settings, such as the UI and Code color themes, whether to use mouse mode, etc...", 'blue', 'underlined')
                            _save_pyin_settings_file()
                            fansi_print("...done!", 'blue', 'underlined')
                        except Exception as e:
                            fansi_print("...failed to PT SAVE!", 'red', 'underlined')
                            print_stack_trace(e)
                    elif user_message =='PT RESET':
                        try:
                            if input_yes_no("Are you sure you want to delete your settings file? This will reset all your settings to the defaults. This might sometimes be necessary if an invalid settings file prevents you from using PT ON. You can't undo this unless you've made a backup of "+repr(_pyin_settings_file_path)):
                                fansi_print("Deleting your settings file...", 'blue', 'underlined')
                                _delete_pyin_settings_file()
                                fansi_print("...done! When you restart rp, your changes should take effect. If you change your mind before you close this session and want to keep your settings, use PT SAVE before exiting.", 'blue', 'underlined')
                            else:
                                fansi_print("...very well then. We don't reset your PT settings file.", 'blue', 'underlined')
                        except Exception as e:
                            fansi_print("...failed to PT RESET!", 'red', 'underlined')
                            print_stack_trace(e)
                    elif user_message == 'SET STYLE':
                        set_prompt_style()
                    elif user_message == 'PROF DEEP':
                        global _PROF_DEEP
                        if not _PROF_DEEP:
                            if not _profiler:
                                fansi_print("Turned PROFILER on. This will profile each command you run. To turn if off use PROF OFF.", 'blue', 'underlined')
                                _profiler=True
                            _PROF_DEEP=True
                            fansi_print("Toggled _PROF_DEEP. We just the PROFILER to DEEP mode ON. This means we record all functions, even ones from external libraries. It's more verbose. Use PROF DEEP again to go back to shallow mode.", 'blue', 'underlined')
                        else:
                            fansi_print("Toggled _PROF_DEEP. We just the PROFILER to DEEP mode OFF. Use PROF DEEP again to go back to deep mode.", 'blue', 'underlined')
                            _PROF_DEEP=False
                    elif user_message == 'PROF ON':
                        fansi_print("Turned PROFILER on. This will profile each command you run. To get more detailed profiles, use 'PROF DEEP'. Note: Commands that take under a millisecond to run will not be profiled, to maintain both accuracy and your sanity.", 'blue', 'underlined')
                        _profiler=True
                    elif user_message == 'PROF OFF':
                        fansi_print("Turned PROFILER off.", 'blue', 'underlined')
                        _profiler=False
                    elif user_message == 'PROF':
                        _profiler=not _profiler
                        if _profiler:
                            fansi_print("Turned PROFILER on. This will profile each command you run. To get more detailed profiles, use 'PROF DEEP'", 'blue', 'underlined')
                        else:
                            fansi_print("Turned PROFILER off.",'blue','underlined')

                    elif user_message == 'TICTOC ON':
                        fansi_print("Turned TICTOC on. This will display the running time of each command.", 'blue', 'underlined')
                        _tictoc=True
                    elif user_message == 'TICTOC OFF':
                        fansi_print("Turned TICTOC off.",'blue','underlined')
                        _tictoc=False
                    elif user_message == 'TICTOC':
                        _tictoc=not _tictoc
                        if _tictoc:
                            fansi_print("Turned TICTOC on. This will display the running time of each command.",'blue','underlined')
                        else:
                            fansi_print("Turned TICTOC off.",'blue','underlined')

                    elif user_message == 'RELOAD ON':
                        _reload_modules()
                        fansi_print("Turned RELOAD ON. This will re-import any modules that changed at the beginning of each of your commands.",'blue','underlined')
                        _reload=True
                    elif user_message == 'RELOAD OFF':
                        fansi_print("Turned RELOAD OFF",'blue','underlined')
                        _reload=False

                    elif user_message=='FORK':
                        #TODO: Make this work with PT ON
                        #TODO: Right now this is just a proof of concept, of how to set checkpoints. Might rename this CHECKPOINT, but that's a long name...fork is nicer...\
                        #Used in-case you wanna try something risky that even UNDO can't fix...like mutating tons of variables etc...
                        #But unlike UNDO, it won't use tons and tons of memory (in theory) because of copy-on-write
                        #TODO: Handle Ctrl+C events from being propogaetd to each process at once
                        #TODO: Properly handle stdout so we can support PT ON
                        import os, sys
                        fansi_print("FORK -> Attempting to fork...",'blue','underlined')

                        child_pid = os.fork()
                        if child_pid == 0:
                            fansi_print("...spawning child process. Note: PT ON is not supported while forking yet. Also, please don't use control+c yet, that's not supported either. To exit, use RETURN.",'blue','underlined')#PT ON gives OSError: [Errno 9] Bad file descriptor
                            enable_ptpython=False
                            # child process
                            # os.system('ping -c 20 www.google.com >/tmp/ping.out')
                            # sys.exit(0)
                        else:
                            pid, status = os.waitpid(child_pid, 0)
                            fansi_print("FORK: resuming parent process...",'blue','underlined')

                    elif user_message == 'HISTORY':print_history()
                    elif user_message == 'AHISTORY':fansi_print("AHISTORY ⟹ Displaying all history, including failures:",'blue','bold');display_list(all_command_history)
                    elif user_message == 'SUSPEND':
                        try:
                            psutil=pip_import('psutil')
                            fansi_print("Suspending this python session...",'blue','underlined')
                            import psutil,os
                            psutil.Process(os.getpid()).suspend()
                            fansi_print("...restored!",'blue','underlined')
                        except ImportError:
                            fansi_print("ERROR: psutil not installed. Try pip install psutil.",'red')
                    elif user_message == 'GHISTORY':
                        fansi_print("GHISTORY ≣ GREEN HISTORY ⟹ Here is a list of all valid single-lined python commands you have entered so far:",'blue','underlined')
                        for x in successful_command_history:
                            fansi_print(x if '\n' not in x else '','green')  # x if '\\n' not in x else '' ≣ '\\n' not in x and x or ''
                    elif user_message == 'CHISTORY':
                        fansi_print("CHISTORY ≣ COPY HISTORY ⟹ Copied history to clipboard!",'blue','underlined')
                        string_to_clipboard('\n'.join(successful_command_history))
                    elif user_message == "MORE":
                        fansi_print("The last command that caused an error is shown below in magenta:",'red','bold')
                        fansi_print(error_message_that_caused_exception,'magenta')
                        if error is None:# full_exception_with_traceback is None ⟹ Last command did not cause an error
                            fansi_print( "(The last command did not cause an error)",'red')
                        else:
                            print_stack_trace(error,True,'')
                    elif user_message == "MMORE":
                        fansi_print("The last command that caused an error is shown below in magenta:",'red','bold')
                        fansi_print(error_message_that_caused_exception,'magenta')
                        fansi_print("A detailed stack trace is shown below:",'red','bold')
                        if error is None:# full_exception_with_traceback is None ⟹ Last command did not cause an error
                            fansi_print( "(The last command did not cause an error)",'red')
                        else:
                            print_verbose_stack_trace(error)
                    elif user_message == 'DMORE':
                        fansi_print("DMORE ⟹ Entering a post-mortem debugger","blue")
                        pip_import('pudb').post_mortem(error.__traceback__)
                        # fansi_print("DMORE has not yet been implemented. It will be a post mortem debugger for your error using rp_ptpdb",'red','bold')

                    elif user_message.startswith('MODIFIER SET'):
                        cursor='|'
                        if cursor in user_message:
                            def string_to_modifier(string):
                                #Treat the string as a template.
                                return lambda input:string.replace(cursor,input)
                            template_string=user_message[len('MODIFIER SET'):].lstrip()
                            fansi_print("MODIFIER SET: Setting template with cursor="+repr(cursor)+" string to "+repr(template_string),'blue','bold')
                            fansi_print(repr(cursor)+" will be replaced with user_message",'blue')
                            modifier=string_to_modifier(template_string)
                            if not use_modifier:
                                fansi_print("MODIFIER ON ⟹ use_modifier=True","blue")
                                use_modifier=True
                        else:
                            fansi_print("Failed to set modifier because you didn't use the cursor anywhere. You should use "+repr(cursor)+" somewhere in your modifier string.\nEXAMPLE:\nMODIFIER SET print("+str(cursor)+")",'red','bold')

                    elif user_message.startswith('SMODIFIER SET'):
                        cursor='|'
                        if cursor in user_message:
                            def repr_string_to_modifier(string):
                                #Treat the string as a template.
                                return lambda input:string.replace(cursor,repr(input))
                            template_string=user_message[len('SMODIFIER SET'):].lstrip()
                            fansi_print("SMODIFIER SET: (aka String-modifier set) Setting template with cursor="+repr(cursor)+" string to "+repr(template_string),'blue','bold')
                            fansi_print(repr(cursor)+" will be replaced with repr(user_message)",'blue')
                            modifier=repr_string_to_modifier(template_string)
                            if not use_modifier:
                                fansi_print("MODIFIER ON ⟹ use_modifier=True","blue")
                                use_modifier=True
                        else:
                            fansi_print("Failed to set string-modifier because you didn't use the cursor anywhere. You should use "+repr(cursor)+" somewhere in your modifier string.\nEXAMPLE:\nMODIFIER SET print("+str(cursor)+")",'red','bold')

                    elif user_message == "MODIFIER OFF":
                        fansi_print("MODIFIER OFF ⟹ use_modifier=False","blue")
                        use_modifier=False
                    elif user_message == "MODIFIER ON":
                        fansi_print("MODIFIER ON ⟹ use_modifier=True","blue")
                        use_modifier=True
                    elif user_message=='FANSI ON':
                        enable_fansi()
                        fansi_print("FANSI ON ⟹ enable_fansi()","blue")
                    elif user_message=='FANSI OFF':
                        disable_fansi()
                        fansi_print("FANSI OFF ⟹ disable_fansi()","blue")
                    elif user_message == "PT ON":
                        fansi_print("PROMPT TOOLKIT ON ⟹ enable_ptpython=True","blue")
                        global _printed_a_big_annoying_pseudo_terminal_error
                        if _printed_a_big_annoying_pseudo_terminal_error:
                            fansi_print("Warning: PT ON crashed, so PT ON might not be available right now. This could be because PT ON crashed, or you're using a terminal that doesn't support it. Will attempt to PT ON anyway, though.","red")
                        _printed_a_big_annoying_pseudo_terminal_error=False
                        enable_ptpython=True
                    elif user_message == "PT OFF":
                        fansi_print("PROMPT TOOLKIT OFF ⟹ enable_ptpython=False","blue")
                        enable_ptpython=False
                        use_modifier=True
                    elif user_message == "LEVEL":
                        fansi_print("LEVEL ⟹ "+level_label(-1),"blue")
                        use_modifier=True
                    elif user_message == "COPY":
                        from rp import string_to_clipboard as copy
                        fansi_print("COPY ⟹ r.string_to_clipboard(str(ans))","blue")
                        copy(str(get_ans()))
                    elif user_message == "VARS":
                        fansi_print("VARS ⟹ ans = user_created_variables (AKA all the names you created in this pseudo_terminal session):","blue")
                        fansi_print("  • NOTE: ∃ delete_vars(ans) and globalize_vars(ans)","blue")
                        set_ans(user_created_var_names,save_history=True)

                    elif user_message in {"#PREV","PREV"}:
                        fansi_print("PREV ⟹  ans = ‹the previous value of ans›:","blue",'bold')
                        if ans_history:
                            ans_redo_history.append(ans_history.pop())
                        if not ans_history:
                            fansi_print("    [Cannot get PREV ans because ans_history is empty]",'red')
                        else:
                            set_ans(ans_history[-1],save_history=False)
                            successful_command_history.append("#PREV")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"#NEXT","NEXT"}:
                        if not ans_redo_history:
                            fansi_print("    [Cannot get NEXT ans because ans_redo_history is empty. NEXT is to PREV as REDO is to UNDO. Try using PREV before using NEXT.]",'red')
                        else:
                            fansi_print("NEXT ⟹  ans = ‹the next value of ans› (PREV is to UNDO as NEXT is to REDO):","blue",'bold')
                            set_ans(ans_redo_history.pop(),save_history=True)
                            successful_command_history.append("#NEXT")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO","#UNDO"}:
                        fansi_print("UNDO ⟹ UNDO:","blue")
                        if not snapshot_history:
                            fansi_print("    [Cannot UNDO anything right now because snapshot_history is empty"+(' becuase UNDO is OFF (enable it with UNDO ON)' if not snapshots_enabled else '')+"]",'red')
                        else:
                            while snapshot_history and not set_snapshot(snapshot_history.pop()):# Keep undoing until something changes
                                successful_command_history.append("#UNDO")# We put this here in case the user wants to analyze the history when brought back into normal python code
                            successful_command_history.append("#UNDO")# We put this here in case the user wants to analyze the history when brought back into normal python code
                            # set_snapshot([{},{},{}])
                    elif user_message in {"UNDO ALL","#UNDO ALL"}:
                        fansi_print("UNDO ALL ⟹ snapshot_history=[] (Doing UNDO over and over again):\n\tCleared %i entries"%len(snapshot_history),"blue")
                        if snapshot_history:set_snapshot(snapshot_history[0])
                        else:fansi_print("\t(snapshot_history is allready empty, so no changes were made)",'blue')
                        snapshot_history=[]
                        successful_command_history.append("#UNDO ALL")
                    elif user_message in {"PREV ALL","#PREV ALL"}:
                        fansi_print("PREV ALL ⟹ ans_history=[] (Doing PREV over and over again):\n\tCleared %i entries"%len(ans_history),"blue")
                        fansi
                        if ans_history:set_ans(ans_history[0])
                        else:fansi_print("\t(ans_history is allready empty, so no changes were made)",'blue')
                        ans_history=[]
                        successful_command_history.append("#PREV ALL")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO CLEAR","#UNDO CLEAR"}:
                        fansi_print("UNDO ALL ⟹ snapshot_history=[] (Clearing the UNDO history):\n\tCleared %i entries"%len(snapshot_history),"blue")
                        snapshot_history=[]
                        successful_command_history.append("#UNDO CLEAR")
                    elif user_message in {"PREV CLEAR","#PREV CLEAR"}:
                        fansi_print("PREV CLEAR ⟹ ans_history=[] (Clearing the PREV history):\n\tCleared %i entries"%len(ans_history),"blue")
                        ans_history=[]
                        successful_command_history.append("#PREV CLEAR")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO ON","#UNDO ON"}:
                        fansi_print("UNDO ON ⟹ snapshots_enabled=True (Enables future UNDO history recording)","blue")
                        snapshots_enabled=True
                        successful_command_history.append("#UNDO ON")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"UNDO OFF","#UNDO OFF"}:
                        fansi_print("UNDO OFF ⟹ snapshots_enabled=False (Disables future UNDO history recording)","blue")
                        snapshots_enabled=False
                        successful_command_history.append("#UNDO OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"PREV OFF","#PREV OFF"}:
                        fansi_print("PREV OFF ⟹ use_ans_history=False (Disables future PREV history recording)","blue")
                        use_ans_history=False
                        successful_command_history.append("#PREV OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"PREV ON","#PREV ON"}:
                        fansi_print("PREV ON ⟹ use_ans_history=True (Enables future PREV history recording)","blue")
                        use_ans_history=True
                        successful_command_history.append("#PREV ON")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"GC ON","#GC ON"}:
                        fansi_print("GC ON ⟹ do_garbage_collection_before_input=True ('GC ON' Forcibly invokes the garbage collector upon each user prompt)","blue")
                        do_garbage_collection_before_input=True
                        successful_command_history.append("#GC ON")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"GC OFF","#GC OFF"}:
                        fansi_print("GC OFF ⟹ do_garbage_collection_before_input=False ('GC ON' Forcibly invokes tgarbage collector upon each user prompt)","blue")
                        do_garbage_collection_before_input=False
                        successful_command_history.append("#GC OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    # endregion
                    # region  Short-hand rinsp
                    elif user_message.startswith('?.'):
                        user_message=user_message[2:]
                        if user_message:
                            fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in ans:","blue")
                            rinsp_search(get_ans(),user_message)
                        else:
                            fansi_print("You didn't give ?. a query. You must follow ?. by a query. For example, '?.print' when ans is rp","red")
                    elif '\n' not in user_message and re.fullmatch(r'[a-zA-Z0-9_]*\.\?.*',user_message[::-1]):
                        #if user_message like 'some_value[0](x,y,z)?.query'
                        split=[x[::-1] for x in user_message[::-1].split('.?',1)][::-1]#Split on the last ?.
                        assert len(split)==2
                        value=eval(split[0],scope())
                        query=split[1]
                        if query:
                            fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in "+split[0]+":","blue")
                            rinsp_search(value,query)
                        else:
                            fansi_print("You didn't give some_value?. a query. You must follow some_value?. by a query. For example, 'thing?.print' is ok while 'thing?.' is not","red")
                    elif user_message == "?":
                        fansi_print("? ⟹ rinsp(ans)","blue")
                        rinsp(get_ans())
                    elif user_message == "??":
                        fansi_print("?? ⟹ rinsp(ans,1)","blue")
                        rinsp(get_ans(),1)
                    elif user_message == "???":
                        fansi_print("??? ⟹ rinsp(ans,1,1)","blue")
                        rinsp(get_ans(),1,1)
                    elif user_message == "????":
                        fansi_print("???? ⟹ rinsp(ans,1,0,1)","blue")
                        rinsp(get_ans(),1,0,1)
                    elif user_message == "?????":
                        fansi_print("????? ⟹ rinsp(ans,1,1,1)","blue")
                        rinsp(get_ans(),1,1,1)
                    elif user_message == "?/":
                        fansi_print("?/ ⟹ help(ans)","blue")
                        help(get_ans())
                    elif user_message.endswith("?/"):
                        fansi_print("◊?/ ⟹ help(◊)","blue")
                        help(eval(user_message[:-2],scope()))
                    elif user_message.endswith("?????"):
                        fansi_print("◊????? ⟹ rinsp(◊,1,1,1)","blue")
                        rinsp(eval(user_message[:-5],scope()))
                    elif user_message.endswith("????"):
                        fansi_print("◊???? ⟹ rinsp(◊,1,0,1)","blue")
                        rinsp(eval(user_message[:-4],scope()),1,0,1)
                    elif user_message.endswith("???"):
                        fansi_print("◊??? ⟹ rinsp(◊,1,1)","blue")
                        rinsp(eval(user_message[:-3],scope()),1,1)
                    elif user_message.endswith("??"):
                        fansi_print("◊?? ⟹ rinsp(◊,1)","blue")
                        rinsp(eval(user_message[:-2],scope()),1)
                    elif user_message.endswith("?"):
                        fansi_print("◊? ⟹ rinsp(◊)","blue")
                        rinsp(eval(user_message[:-1],scope()))

                    elif user_message=='PWD':
                        import posix
                        fansi_print("PWD: "+posix.getcwd(),"blue")
                    elif user_message=='CPWD':
                        import posix
                        fansi_print("PWD: Copied to clipboard: "+posix.getcwd(),"blue")
                        string_to_clipboard(posix.getcwd())

                    elif user_message.startswith('CAT ') or user_message.startswith('NCAT ') :

                        file_name=user_message[user_message.find(' '):].strip()

                        line_numbers=user_message.startswith('N')#Should we print with line numbers
                        highlight   =get_file_extension(file_name)=='py'#Should we do syntax highlighting

                        if line_numbers:
                            if highlight:
                                fansi_print("NCAT: Printing (with line numbers and python syntax highlighting) the contents of "+repr(file_name),"blue")
                            else:
                                fansi_print("NCAT: Printing (with line numbers) the contents of "+repr(file_name),"blue")
                        else:
                            if highlight:
                                fansi_print("CAT: Printing (with python syntax highlighting) the contents of "+repr(file_name),"blue")
                            else:
                                fansi_print("CAT: Printing the contents of "+repr(file_name),"blue")

                        contents=text_file_to_string(file_name)

                        def print_code(code,highlight=False,line_numbers=False):
                            s=code
                            l=s.splitlines()#code lines
                            if not l:return#Nothing to print, don't cause errors...
                            n=list(map(str,range(len(l))))#numbers
                            c=max(map(len,n))#max number of chars in any number
                            for line,num in zip(s.splitlines(),n):
                                if line_numbers:
                                    num=num.rjust(c)
                                    num=fansi(num,'black','bold','blue')
                                else:
                                    num=''
                                if highlight:
                                    line=fansi_syntax_highlighting(line)
                                print(num+line)

                        print_code(contents,highlight,line_numbers)

                    elif user_message.startswith('CCAT '):

                        file_name=user_message[user_message.find(' '):].strip()
                        fansi_print("CCAT: Copying to your clipboard sthe contents of "+repr(file_name),"blue")
                        string_to_clipboard(text_file_to_string(file_name))

                    elif user_message=='LS':
                        import os
                        for item in sorted(sorted(os.listdir()),key=is_a_directory):
                            if is_a_directory(item):
                                fansi_print(item,'cyan','bold')
                            elif is_a_file(item):
                                fansi_print(item,'gray')
                            else:
                                fansi_print(item,'red')

                    elif user_message=='IPYTHON ON':
                        fansi_print("IPYTHON ON ⟹ running all commands with an ipython interpereter for better tracebacks etc. Run '%magic' to see help for all available iPython magics commands. (pro-tip: for line magics, you don't even need to use %, so just 'magic' works too)","blue",'underlined')
                        global _ipython_exeval
                        try:
                            if _ipython_exeval is None:
                                _ipython_exeval=_ipython_exeval_maker(dicts[0])#Right now this is global. This is seriously messy. But since pseudoterminal's namespace is allready F'd up right now, who cares...I'll fix this when I rewrite pseudoterminal
                            _use_ipython_exeval=True
                        except ImportError:
                            fansi_print("IPYTHON ON failed due to an import error",'red','bold')
                            _use_ipython_exeval=False
                    elif user_message=='IPYTHON OFF':
                        fansi_print("IPYTHON OFF ⟹ running your inputs as regular ol' python again","blue")
                        _use_ipython_exeval=False
                    # endregion
                    else:
                        if user_message == "SHELL":
                            fansi_print("SHELL ⟹ entering Xonsh shell","blue",'bold')
                            xonsh=pip_import('xonsh')
                            # xonsh.execer.Execer.__del__=lambda *x:None# This prevents it from unimportant error messages after we leave the shell
                            # xonsh.execer.print_exception=lambda *x:None# This prevents it from unimportant error messages after we leave the shell
                            fansi_print('Will try to run Xonsh (a python-based alternative to bash). Note that its the same runtime as. If it fails to launch properly, try "pip3 install prompt-toolkit pygments --upgrade". If it\'s fine, ignore this message.','blue')
                            user_message='import xonsh.main;xonsh.main.main();sys.path.append(".")'  # Import xonsh, run the shell, then update the directory

                        elif user_message == "IPYTHON":
                            fansi_print("WARNING: Use 'IPYTHON ON' or 'IPYTHON OFF' for now on, 'IPYTHON' is broken until further notice. Will try to do it anyway, though.",'red','bold')
                            fansi_print("IPYTHON ⟹ embedding iPython","blue")
                            # user_message='import IPython;IPython.embed()'
                            user_message='import rp.rp_ptpython.ipython;rp.rp_ptpython.ipython.embed()'

                        # region Alternate methods of user_input (PASTE/EDIT/DITTO etc)
                        elif user_message == 'PASTE':
                            fansi_print("PASTE ⟹ Running code from your clipboard (shown in yellow below):",'blue','underlined')
                            user_message=string_from_clipboard()
                            fansi_print(user_message,"yellow")
                        elif user_message.startswith("RANT "):
                            user_message="run_as_new_thread(exec,"+repr(user_message[5:].strip())+",globals(),locals())"
                        elif user_message.startswith("RANP "):
                            user_message="run_as_new_process(exec,"+repr(user_message[5:].strip())+",globals(),locals())"
                        elif user_message == 'SPASTE':
                            fansi_print("SPASTE ⟹ ans=str(string_from_clipboard()):",'blue','underlined')
                            user_message=repr(string_from_clipboard())
                        elif user_message.startswith('DITTO'):
                            ditto_arg=user_message[len('DITTO'):]
                            try: ditto_number=int(ditto_arg.strip())
                            except: ditto_number=1
                            if not successful_command_history:
                                fansi_print("DITTO ⟹ Cannot use DITTO, the successful_command_history is empty!",'red')
                                user_message=""# Ignore it
                            else:
                                fansi_print("DITTO ⟹ re-running last successful command "+str(ditto_number)+" times, shown below in yellow:",'blue','underlined')
                                user_message='\n'.join([successful_command_history[-1]]*ditto_number)
                                fansi_print(user_message,"yellow")
                        elif user_message.startswith('RUN '):
                            import shlex
                            command=shlex.split(user_message[4:])#shlex handles quoted strings even if there are spaces in them. https://stackoverflow.com/questions/899276/python-how-to-parse-strings-to-look-like-sys-argv
                            script_path=command[0]
                            script_path=script_path.strip()
                            if not script_path:
                                fansi_print("RUN ⟹ Error: Please specify a python script. Example: 'RUN test.py --args",'red')
                            else:
                                fansi_print("RUN ⟹ Executing python script at file with args: "+script_path,'blue')
                                lines=line_split(text_file_to_string(script_path))
                                for i,line in enumerate(lines):
                                    if line.strip() and not line.startswith('from __future__'):#These must come first
                                        lines.insert(i,'sys.argv='+repr(command))
                                        break
                                user_message=line_join(lines)
                                fansi_print("Printing script below: "+script_path,'blue')
                                fansi_print("Parsed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')
                        # elif not is_valid_python_syntax(user_message) and re.fullmatch(,user_message):
                        elif user_message and 'print'.startswith(user_message) and not any(user_message in dict for dict in dicts):
                            fansi_print("Variable "+repr(user_message)+" does not exist, so parsed command into print(ans)",'magenta')
                            user_message='print(ans)'

                        elif user_message=='CD' or user_message.startswith('CD ') or user_message=='CDP':
                            if user_message=='CDP':
                                new_dir=string_from_clipboard()
                                fansi_print("CDP ⟹ CD Paste (CD to the string in your clipboard, aka "+repr(new_dir),'blue')
                            else:
                                new_dir=user_message[2:].strip()
                            if not new_dir:
                                fansi_print("CD ⟹ Error: Please specify a directory. Example: 'CD /Users/Ryan'"+new_dir,'red')
                            else:
                                import posix
                                _pwd=posix.getcwd()
                                cd(new_dir)
                                fansi_print("CD ⟹ Current directory = "+(posix.getcwd()),'blue')
                                cd(_pwd)
                            user_message='sys.path.append('+repr(new_dir)+')\ncd('+repr(new_dir)+')'
                            # fansi_print("Parsed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')
                        elif user_message == 'EDIT' or re.fullmatch(r'EDIT[0-9]+',user_message):
                            # pip install python-editor
                            start=''
                            give_up=False
                            if re.fullmatch(r'EDIT[0-9]+',user_message):
                                n=int(user_message[4:])
                                fansi_print("EDIT"+str(n)+" ⟹ Editing your "+str(n)+'th last entry:','blue','underlined')
                                try:
                                    start=all_command_history[-(n+1)]
                                except IndexError:
                                    if not all_command_history:
                                        fansi_print("EDIT"+str(n)+" ⟹ Error: Can't go back into AHISTORY, you haven't entered any commands yet.",'red','underlined')
                                    else:
                                        fansi_print("EDIT"+str(n)+" ⟹ Error: Can't go back that far into AHISTORY; try a lower value of n",'red','underlined')
                                    give_up=True
                            if not give_up:
                                fansi_print("EDIT ⟹ Replacing EDIT with your custom text, shown below in yellow:",'blue','underlined')
                                try:
                                    editor=pip_import('editor')
                                    user_message=editor.edit(contents=start,use_tty=True,suffix='.py').decode()
                                except ImportError:
                                    user_message=mini_editor(start,list(scope()))
                                fansi_print(user_message,'yellow')
                            else:
                                user_message=''
                        elif user_message.startswith('ARG '):
                            import sys,shlex
                            args_string=user_message[len('ARG '):]
                            fansi_print('ARG: Old sys.argv: '+repr(sys.argv),'blue','bold')
                            sys.argv=command=[sys.argv[0]]+shlex.split(args_string)
                            fansi_print('ARG: New sys.argv: '+repr(sys.argv),'blue','bold')
                            user_message='sys.argv='+repr(sys.argv)

                        elif user_message.startswith('OPEN '):
                            file_path=user_message[len('OPEN '):]

                            user_message='open_file_with_default_application('+repr(file_path)+')'
                            fansi_print("Parsed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')

                        # endregion
                        # region Modifier
                        if use_modifier and modifier is not None:
                            try:
                                new_message=modifier(user_message)
                                original_user_message=user_message
                                user_message=new_message
                            except Exception as E:
                                original_user_message=None
                                fansi_print("ERROR: Failed to modify your command. Attempting to execute it without modifying it.","red","bold")
                        # endregion
                        # region Lazy-Parsers:Try to parse things like 'rinsp ans' into 'rinsp(ans)' and '+7' into 'ans+7'
                        # from r import space_split
                        current_var=rp.r_iterm_comm.last_assignable_comm
                        if current_var is not None and user_message in ['+','-','*','/','%','//','**','&','|','^','>>','<<']+['and','or','not','==','!=','>=','<=']+['>','<','~']:
                            user_message='ans ' + user_message +' ' + current_var
                            fansi_print("Parsed command into " + repr(user_message),'magenta')
                        else:
                            if user_message.startswith("!!"):# For shell commands
                                user_message="shell_command("+repr(user_message[2:])+")"
                                fansi_print("Parsed command into " + repr(user_message),'magenta')
                            elif user_message.startswith("!"):# For shell commands
                                user_message="shell_command("+repr(user_message[1:])+",True)"
                                fansi_print("Parsed command into " + repr(user_message) ,'magenta')
                            if True and len(user_message.split("\n")) == 1 and not enable_ptpython:  # If we only have 1 line: no pasting BUT ONLY USE THIS IF WE DONT HAVE ptpython because sometimes this code is a bit glitchy and its unnessecary if we have ptpython
                                _thing=space_split(user_message)
                                if len(_thing) > 1:
                                    # from r import is_literal
                                    bracketeers="()"
                                    try:
                                        if hasattr(eval(_thing[0]),'__getitem__'):
                                            bracketeers="[]"
                                    except:
                                        pass
                                    flaggy=False
                                    if all(map(is_literal,_thing)):  # If there are no ';' or ',' in the arguments; just 'rinsp' or 'ans' etc
                                        user_message=_thing[0] + bracketeers[0] + ','.join(_thing[1:]) + bracketeers[1]
                                        flaggy=True
                                    elif is_literal(_thing[0]):
                                        user_message=_thing[0] + bracketeers[0] + " " + repr(user_message[len(_thing[0]):]) + bracketeers[1]
                                        flaggy=True
                                    if flaggy:
                                        fansi_print("Parsed command into " + repr(user_message),'magenta')
                            if user_message.lstrip():
                                try:
                                    float(user_message)  # could be a negative number; we dont want Parsed command into 'ans -1324789'
                                except:
                                    arg_0=user_message.lstrip()
                                    if arg_0=='=' or last_assignable and (arg_0[0] == '=' and arg_0[1] != "=" or arg_0[0:2] in ['+=','-=','*=','/=','&=','|=','^=','%='] or arg_0[:3] in ['//=','**=','<<=','>>=']):
                                        if not last_assignable in assignable_history:
                                            assignable_history[last_assignable]=[]
                                        else:
                                            assignable_history[last_assignable].append(eval(last_assignable,scope()))
                                        user_message=last_assignable + user_message
                                        fansi_print("Parsed command into " + repr(user_message),'magenta')
                                    elif arg_0[0] in '.+-/*^=><&|' or space_split(user_message.lstrip().rstrip())[0] in ['and','or','is']:
                                        user_message='ans ' + user_message
                                        fansi_print("Parsed command into " + repr(user_message),'magenta')
                            if user_message.rstrip().endswith("="):
                                user_message=user_message + ' ans'
                                fansi_print("Parsed command into " + repr(user_message),'magenta')
                            # from r import is_namespaceable
                            if True and (user_message.replace("\n","").lstrip().rstrip() and not '\n' in user_message and (("=" in user_message.replace("==","") and not any(x in user_message for x in ["def ",'+=','-=','*=','/=','&=','|=','^=','%='] + ['//=','**=','<<=','>>='])) or is_namespaceable(''.join(set(user_message) - set(",.:[] \\t1234567890"))))):  # Doesn't support tuple unpacking because it might confuse it with function calls. I.E. f(x,y)=z looks like (f,x)=y to it
                                last_assignable_candidate=user_message.split("=")[0].lstrip().rstrip()
                                if last_assignable_candidate.startswith("import "):
                                    last_assignable_candidate=last_assignable_candidate[7:]
                            else:
                                pass
                        # endregion
                        while user_message:  # Try to correct any errors we might find in their code that may be caused mistakes made in the pseudo_terminal environment
                            # region Try to evaluate/execute user_message
                            if last_assignable_candidate not in ['',None,'ans']:
                                last_assignable=last_assignable_candidate
                                import rp.r_iterm_comm
                                last_assignable=regex_replace(last_assignable,'from .* import ','')#remove the 'from x import y' from that name, it's gibberish
                                last_assignable=itc(lambda x:regex_replace(x,r'\w+\s+as\s+(\w+)',r'\1'),last_assignable)#a as b --> b; and "a as b,c as d"-->b,d
                                rp.r_iterm_comm.last_assignable_comm=last_assignable
                            try:
                                scope_before=set(scope())
                                take_snapshot()# Taken BEFORE modifications to save current state!
                                _temp_old_ans=get_ans()
                                all_command_history.append(user_message)
                                if _reload:
                                    try:
                                        _reload_modules()
                                    except BaseException as E:
                                        fansi_print('RELOAD Error: Failed to reload modules because: '+str(E),'blue')
                                result,__error=exeval(user_message,
                                                      *dicts,
                                                      exec=exec,
                                                      eval=eval,
                                                      tictoc=_tictoc,
                                                      profile=_profiler,
                                                      ipython=_use_ipython_exeval)
                                if __error is not None:
                                    if isinstance(__error,IndentationError):
                                        raise __error#Catch this by the indendation fixer
                                    show_error(__error)
                                if get_ans() is not _temp_old_ans:#This is here so we can say ' ⮤ ans=234' and still rely on PREV
                                    set_ans(get_ans())
                                del _temp_old_ans#
                                # raise KeyboardInterrupt()
                                if __error is None and result is None:
                                    add_to_successful_command_history(user_message)
                                elif __error is None:
                                    dupdate(dicts[0],'ans')
                                    set_ans(result,save_history=not equal(result,dicts[0]['ans']),snapshot=False)# snapshot=False beacause we've already taken a snapshot! Only saves history if ans changed, though. If it didn't, you'll see yellow text instead of green text
                                    if user_message.lstrip().rstrip()!='ans':# Don't record 'ans=ans'; that's useless. Thus, we can view 'ans' without clogging up successful_command_history
                                        add_to_successful_command_history("ans="+user_message)# ans_history is only changed if there is a change to ans, but command history is always updated UNLESS user_message=='ans' (having "ans=ans" isn't useful to have in history)
                                user_created_var_names=user_created_var_names|(set(scope())-scope_before)
                                break
                            # endregion
                            # region  Try to fix user_input, or not use modifier etc
                            except IndentationError as E:
                                if _get_prompt_style() in user_message:  # They probably just copied and pasted one of their previous commands from the console. If they did that it would contain the header which would cause an error. So, we delete the header.
                                    print(type(E))
                                    fansi_print("That command caused an error, but it contained '" + _get_prompt_style() + "' without quotes. Running your command without any '" + _get_prompt_style() + "'_s, shown below in magenta:","red","bold")
                                    user_message=user_message.replace(_get_prompt_style(),"")  # If we get an error here, try getting rid of the headers and then try again via continue...
                                    fansi_print(user_message,"magenta")
                                elif user_message.lstrip() != user_message:  # If our string is only one line long, try removing the beginning whitespaces...
                                    fansi_print("That command caused an error, but it contained whitespace in the beginning. Running your command without whitespace in the beginning, shown below in magenta:","red","bold")
                                    def number_of_leading_spaces(string):#strip spaces from every line...
                                        i=0
                                        for x in string:
                                            if not x.strip():
                                                i+=1
                                            else:
                                                break
                                        return i
                                    old_user_message=user_message
                                    _nls=number_of_leading_spaces(user_message)
                                    user_message=user_message.split('\n')
                                    for i,user_message_line in enumerate(user_message):
                                        user_message[i]=user_message_line[min(_nls,number_of_leading_spaces(user_message_line)):]
                                    user_message='\n'.join(user_message) # If we get an error here, try getting rid of the headers and then try again via continue...
                                    user_message=user_message.lstrip()
                                    if user_message==old_user_message:
                                        assert "Failed to fix indentation error...aborting your command..."
                                    fansi_print(user_message,"magenta")
                                else:
                                    raise  # We failed to fix the indentation error. We can't fix anything, so return the error and effectively break the while loop.
                            except:
                                if use_modifier and modifier is not None and original_user_message is not None:# If we're using the modifier and we get a syntax error, perhaps it'_s because the user tried to input a regular command! Let them do that, meaning they have to use the 'MODIFIER ON' and 'MODIFIER OFF' keywords less than they did before.
                                    fansi_print("That command caused an error, but it might have been because of the modifier. Trying to run the original command (without the modifier) shown below in magenta:","red","bold")
                                    # noinspection PyUnboundLocalVariable
                                    fansi_print(user_message,"magenta")
                                    user_message=original_user_message # ⟵ We needn't original_user_message=None. This will literally never happen when use_modifier==True
                                    original_user_message=None# We turn original_user_message to None so that we don't get an infinite loop if we get a syntax error with use_modifier==True.
                                else:
                                    raise
                            # endregion
                    rp.r_iterm_comm.globa=scope()
                except Exception as E:
                    show_error(E)
                except KeyboardInterrupt:
                    print(fansi('Caught keyboard interrupt','cyan','bold'),end='')
                    if allow_keyboard_interrupt_return:
                        print(fansi(': Interrupt again to RETURN','cyan','bold'),end='')
                    print()
        except BaseException as E:
            print(fansi('FATAL ERROR: Something went very, very wrong. Printing HISTORY so you can recover!','red','bold'))
            print_stack_trace(E)
            print_history()
    finally:
        rp.r_iterm_comm.pseudo_terminal_level-=1
        if level_label():
            fansi_print("    - Exiting pseudo-terminal at "+level_label(),'blue' ,'bold')

# @formatter:off
try:from setproctitle import setproctitle as set_process_title \
        ,getproctitle as get_process_title
except:pass
#@formatter:on
def parenthesizer_automator(x:str):
    # Parenthesis automator for python
    l=lambda q:''.join('(' if x in '([{' else ')' if x in ')]}' else ' ' for x in q)
    def p(x,r=True):
        y=list(l(x))
        if not r and ('(' not in y or ')' not in y):
            return [x]
        n=None
        for i,e in enumerate(y):
            if e == '(':
                n=i
            elif e == ')':
                if n is not None:
                    y[i]='>'
                    y[n]='<'
                    n=None
            else:
                y[i]=' '
        y=''.join(y)
        if r:
            y=p(y,False)
            assert isinstance(y,list)
            y=[x.replace('(','│').replace(')','│').replace('<','┌').replace('>','┐') for x in y]
            z=[x.replace('┌','└').replace('┐','┘') for x in y]
            return '\n'.join(y[::-1] + [x] + z)
        return [x] + p(y,False)
    return p(x)

def timeout(f,t):
    import signal

    class TimeoutException(BaseException):   # Custom exception class
        pass

    def timeout_handler(signum, frame):   # Custom signal handler
        raise TimeoutException

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    # https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
    # Start the timer. Once 5 seconds are over, a SIGALRM signal is sent.
    signal.alarm(t)
    # This try/except loop ensures that
    #   you'll catch TimeoutException when it's sent.
    try:
        return f()
    except TimeoutException:
        return "[Timed out]"# continue the for loop if function A takes more than 5 second
try:
    from numpngw import write_apng as save_animated_png#Takes numpy ndarray as input
except:
    pass
#region Wrappers for psutil
def battery_percentage()->float:
    try:
        import psutil
        return psutil.sensors_battery().percent
    except:
        return 100#Don't crash pseudoterminal just because we don't have psutil installed....it's unnessecary. It's just nice, that's all. Perhaps we're not even on a laptop...so default to 100%.
def battery_plugged_in()->bool:
    try:
        import psutil
        return psutil.sensors_battery().power_plugged
    except:
        return True
def battery_seconds_remaining():
    try:
        import psutil
        return psutil.sensors_battery().secsleft
    except:
        return float('inf')
#endregion


def total_disc_bytes(path):
    # path can be either a folder or a file; it will detect that for you. Implemented recursively (checks subfolders)
    # returns total size in bytes

    def get_file_size(path):
        return os.path.getsize(path)
    def get_folder_size(folder):
        # Get the total disc space of a given directory
        # Source: stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python/1392549
        total_size = get_file_size(folder)
        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                total_size += get_file_size(itempath)
            elif os.path.isdir(itempath):
                total_size += get_folder_size(itempath)
        return total_size

    if os.path.isfile(path):
        return get_file_size(path)
    elif os.path.isdir(path):
        return get_folder_size(path)
    else:
        assert False,'r.get_disc_space ERROR: '+path+' is neither a folder nor a file!'

def inherit_def(parent,child=None):
    # Needs examples for documentation.
    if child is None:
        return lambda z:inherit_def(parent,z)
    # Author: Ryan Burgert
    # This decorator modifies the child in-place without copying it!
    # Made because I don't like creating classes when it can be avoided; I'd much rather crate new functions.
    # This is a decorator used to override default method inputs.
    assert callable(child )
    assert callable(parent)
    #
    import inspect as inspect
    child_spec =inspect.getfullargspec(child )
    parent_spec=inspect.getfullargspec(parent)
    #region  Example of getfullargspec results:
    #      ⎧                                    ⎫
    # def f(a, b:str, c=0, d:int=1, *e, f=2, **g):pass
    #      ⎩                                    ⎭
    #             ⎧                                                                                                                                                                   ⎫
    #             ⎪     ⎧                  ⎫                                   ⎧    ⎫             ⎧   ⎫                 ⎧      ⎫              ⎧                                      ⎫⎪
    #  FullArgSpec(args=['a', 'b', 'c', 'd'], varargs='e', varkw='g', defaults=(0, 1), kwonlyargs=['f'], kwonlydefaults={'f': 2}, annotations={'b': <class 'str'>, 'd': <class 'int'>})
    #             ⎪     ⎩                  ⎭                                   ⎩    ⎭             ⎩   ⎭                 ⎩      ⎭              ⎩                                      ⎭⎪
    #             ⎩                                                                                                                                                                   ⎭
    #endregion
    child_args            =child_spec .args

    from rp import mini_terminal_for_pythonista
    exec(mini_terminal_for_pythonista)

    parent_defaults=parent_spec.defaults or []
    child_defaults=child_spec.defaults or []
    undefaulted_child_args=child_args [:len(child_defaults)]
    parent_args           =parent_spec.args or []
    defaulted_parent_args =parent_args[-len(parent_defaults):]
    #
    parent_defaults=dict(zip(parent_args,parent_defaults))# parent_spec.defaults ≣ parent.__defaults__
    parent_defaults.update(parent.__kwdefaults__ or {})# Should be no overrides
    #
    flag=True
    for arg,default in reversed(undefaulted_child_args):# All un-defaulted child args
        if arg in parent_defaults:
            assert flag,'Error: Please rearrange arguments, this is a vague error message (that could easily be improved) but you cant extend functions like that'
            # Assertion Explanation:
            # NOTE: All default args MUST come before undefaulted args, by rules of python syntax.
            #     def parent(a=5):pass
            #     def child(z,a,x):pass
            #   First possiblity for handling this: x is None, and no longer required (which modifies the child)
            #     def child(z,a=5,x=None):pass
            #   Second possiblity for handling this: (reordering arguments; could be REALLY hard to debug if misused, which might be easy to do)
            #     def child(z,x,a=5):pass
            # This method should use neither method for handling it and instead just throw an error.
            child.__defaults__=(parent_defaults[arg],)+child.__defaults__
        else:
            flag=False
    from rp import merged_dicts
    for key in set(parent.__kwdefaults__ or {})-set(child.__defaults__ or {})-set(parent_args)-set(child_args):
        child.__kwdefaults__=[key]=parent.__kwdefaults__[key]
    #
    return child

def num_args(f):# https://stackoverflow.com/questions/847936/how-can-i-find-the-number-of-arguments-of-a-python-function
    from inspect import isfunction, getargspec
    if isfunction(f):
        return len(getargspec(f).args)
    else:
        spec = f.__doc__.split('\n')[0]
        args = spec[spec.find('(')+1:spec.find(')')]
        return args.count(',')+1 if args else 0

def pretty_print(d:dict,with_lines=True):
    #Used to print out highly-nested dicts and lists etc, which are hard to read when it's all in one line.
    #Particularly useful for JSON objets from web requests.
    from pprint import pformat
    string=pformat(d)
    def pretty_lines(s):
        s=string_transpose(string_transpose(s))  # Ensure all have same length
        l=s.split('\n')
        h=len(l)
        w=len(l[0])
        for i in range(1,h):
            t=l[i - 1]  # top
            b=l[i]  # bottom
            for j in range(w):
                c=''
                if t[j] in '({[' + '│├└':
                    if not b[:j + 1].lstrip():
                        if b[j + 1].lstrip():
                            c='├'
                        else:
                            c='│'
                if c:
                    l[i]=l[i][:j] + c + l[i][j + 1:]
        l[h-1]=l[h-1].replace('│',' ').replace('├','└')
        for i in reversed(range(1,h)):
            t=l[i - 1]  # top
            b=l[i]  # bottom
            for j in range(w):
                c=''
                if b[j] not in '├│└':
                    if t[j] in '├':
                        c='└'
                    if t[j] in '│':
                        c=' '
                if c:
                    l[i - 1]=l[i - 1][:j] + c + l[i - 1][j + 1:]
        l=[x.rstrip() for x in l]
        l='\n'.join(l)
        for c in '├│└':
            l=l.replace(c,fansi(c,'gray'))
        return l
    if with_lines:
        string=pretty_lines(string)
    print(fansi_syntax_highlighting(string,style_overrides={'operator':('\033[0;34m','\033[0m'),'string':('\033[0;35m','\033[0m')}))

def string_transpose(x,fill=' '):
    ''' ⮤ string_transpose("Hello\nWorld")
    ans =
    HW
    eo
    lr
    ll
    od
    '''
    assert len(fill) == 1
    assert isinstance(fill,str)
    l=x.split('\n')
    out=''
    m=0
    for s in l:
        m=max(m,len(s))
    for i,s in enumerate(l):
        l[i]=s + fill * (m - len(s))
    return '\n'.join(''.join(i) for i in zip(*l))

def print_to_string(f,*args,**kwargs):
    #args and kwargs are passed to f
    #Example: assert print_to_string(lambda:print("Hello World"))=="Hello World"
    assert callable(f)
    out=''
    def patch(x):
        nonlocal out
        out+=x
    import sys
    temp=sys.stdout.write
    sys.stdout.write=sys.stdout.write,patch
    f(*args,**kwargs)
    sys.stdout.write=temp
    return out

def reduced_row_echelon_form(M):
    pip_import('sympy')
    import sympy
    return sympy.matrix2numpy(sympy.Matrix(M).rref()[0])

def qterm():
    # Enables both vispy and
    def _exeval(f,*x,**y):
        nonlocal _error
        assert _done == _todo == []
        # _todo.insert(0,fog(print,'Hello wurlzy'))
        _todo.insert(0,fog(f,*x,**y))
        while not _done and not _error:
            pass
        assert _todo == []
        if _error:
            assert not _done
            temp=_error
            _error=None
            raise temp
        out=_done.pop()
        assert not _done
        return out
    def _exec(*x,**y):
        return _exeval(exec,*x,**y)
    def _eval(*x,**y):
        return _exeval(eval,*x,**y)

    _error=None
    _todo=[]
    _done=[]  # Results of _todo

    import rp.r_iterm_comm as ric
    _level=ric.pseudo_terminal_level
    run_as_new_thread(pseudo_terminal,globals(),exec=_exec,eval=_eval)
    while ric.pseudo_terminal_level==_level:
        pass
    while 1:
        if ric.pseudo_terminal_level==_level:
            break
        try:
            from vispy import app
            app.process_events()
        except:
            print("harry potwar strikes again! keep chuggin...")
            pass
        if _todo:
            try:
                _done.append(_todo.pop()())
            except BaseException as e:
                _error=e
        assert not _todo
    print('...aaaannndddd were DONE chuggin.')
    app.quit()  # NOT nessecary but PERHAPS its nicer than having a crashy window...make this optional though!!!

def UCB1(w,n,N,c=2**.5):
    #w ÷ n + c √(㏑(N) ÷ n)
    #From wikipedia.org/wiki/Monte_Carlo_tree_search:
    #   · w﹦number of wins for the node
    #   · n﹦number of simulations for the node
    #   · N﹦total number of simulations among all nodes
    #   · c﹦the exploration parameter—theoretically equal to √2; in practice usually chosen empirically
    from math import log as ln
    return w/n+c*(ln(N)/n)**.5

def all_rolls(vector,axis=None):
    #TODO: See if this is the same thing as a toeplitz matrix
    #TODO: There might be a faster way of doing this, but until then this implementation works. It can be swapped out later.
    #Return all circshifts of a vector
    #EXAMPLE:
    #    CODE: print(all_rolls([1,2,3,4,5]))
    #    Output:
    #       [[1 2 3 4 5]
    #        [5 1 2 3 4]
    #        [4 5 1 2 3]
    #        [3 4 5 1 2]
    #        [2 3 4 5 1]]
    #EXAMPLE:
    #    THIS
    #        [[7 8 9]
    #         [1 2 3]
    #         [4 5 6]]
    #    BECOMES
    #       [[[7 8 9]
    #         [1 2 3]
    #         [4 5 6]]
    #
    #        [[4 5 6]
    #         [7 8 9]
    #         [1 2 3]]
    #
    #        [[1 2 3]
    #         [4 5 6]
    #         [7 8 9]]]
    vector=np.asarray(vector)#If this breaks, it's the fault of the user of this function
    out=[]
    for _ in range(len(vector)):
        out.append(vector)
        vector=np.roll(vector,1,axis=axis)
    return np.asarray(out)

def circular_diff(array,axis=0):
    #Returns the diff of an array along the axis, taking into account looping unlike numpy's implementation (aka np.diff)
    #Example: circular_diff([1,2,3,4,5])  ->  [ 1  1  1  1 -4]   VS   np.diff([1,2,3,4,5])  ->  [1 1 1 1]
    return np.roll(array,shift=-1,axis=axis)-array
circ_diff=circular_diff#For convenience's sake
def circular_quotient(array,axis=0):
    # ⮤ circular_quotient([1,2,4,8])
    # ans = [2.    2.    2.    0.125]
    return np.roll(array,shift=-1,axis=axis)/array
circ_quot=circular_quotient#For convenience's sake
def circular_convolve(a,b):
    #Convolve vector a with vector b with wrapping on the boundaries
    #Works with any numpy dtype, and returns the same kind of dtype inputted
    #Examples: circular_convolve([1,0,0,0,0],[1,2,3,4,5]) --> [1 2 3 4 5]
    #Examples: circular_convolve([0,1,0,0,0],[1,2,3,4,5]) --> [5 1 2 3 4] #Notice how it wrapped around
    a=np.asarray(a)
    b=np.asarray(b)
    assert len(a.shape)==len(b.shape)==1,'Right now, circ_conv requires that both inputs are vectors. This may be generalized in the future to n-d convolutions.'
    assert a.shape==b.shape,'Right now, circ_conv requires that both vectors are the same length. This may change in the future.'
    if len(a)==len(b)==0:
        return np.asarray([],np.find_common_type([a.dtype,b.dtype],[]))#If the length of a and b are 0, return an empty array with the maximal dtype. Otherwise this function would throw an error that you can't take the FFT of a vector with 0 elements.
    l=len(a)#Should be the same as len(b)
    f=np.fft.fft
    i=np.fft.ifft
    with warnings.catch_warnings():
        output_type=(a+b).dtype
        warnings.filterwarnings('ignore',message='Casting complex values to real discards the imaginary part',category=np.ComplexWarning)#We're going to output the same type of number that we inputted
        return i(f(a)*f(b)).astype(output_type)
circ_conv=circular_convolve#For convenience's sake
def circular_cross_correlate(a,b):
    #TODO let varargs input (because circular_cross_correlate is associative)
    #Let a★b = circular_cross_correlate(a,b)
    #Cross correltation is convolution where the kernel is flipped.
    #Cross correlation contains the element dot(a,b) whereas convolution does NOT (cross correlation can compare similarities)
    #Properties:
    #FOR ALL INT 'n':   (a★b)[n] = np.dot(a,np.roll(b,n))
    #AND THEREFORE...   (a★b)[0] = np.dot(a,b)
    #UNLIKE Convolution, a★b ≠ b★a
    #UNLIKE Convolution, a★b ≠ ifft(fft(a)*fft(b))
    #UNLIKE Convolution, a★b = ifft(fft(a)*fft(b).conj)
    def reverse(x):
        #NOT the same as x[::-1], due to the way FFT works...
        #Same as ifft(fft(x).conj()), but faster...
        #Example: reverse([1,2,3,4])  ->  [1 4 3 2]
        return np.roll(np.flip(x,axis=0),1)
    return circular_convolve(reverse(a).conj(),b)#This is according to what I think the wikipedia defintion is...
circ_cross_corr=circular_cross_correlate
def circular_auto_correlate(a):
    #TODO extend to multiple dimenations etc.
    #According to wikipedia, auto-correlation is defined as a vector's cross-correlation with itself.
    #The first element of the output is dot(a,a), AKA
    #   circular_auto_correlate(a)[0]  ====  np.dot(a,a)
    #This function returns a shift-invariant descriptor of vector 'a', with half the degrees of freedom of a
    return circular_cross_correlate(a,a)
circ_auto_corr=circular_auto_correlate
def circular_gaussian_blur(vector,sigma=1):
    vector=np.asarray(vector)
    assert len(vector.shape)==1,'Right now input must be a vector. This may change in the future.'
    if sigma==0:return np.copy(vector)
    #  ⮤ circ_gauss_blur([1,0,0,0,0,0])
    # ans = [0.4   0.095 0.005 0.005 0.095 0.4  ]
    #  ⮤ circ_gauss_blur([1,0,0,0,0])
    # ans = [0.403 0.244 0.054 0.054 0.244]
    kernel=gaussian_kernel(size=len(vector),sigma=sigma,dim=1)
    kernel=np.roll(kernel,int(np.ceil(len(kernel)/2)))#Shift it over so that the blur doesn't shift the original vector
    assert len(kernel)==len(vector),'Internal logic assertion to circular_gaussian_blur'
    return circular_convolve(vector,kernel)
circ_gauss_blur=circular_gaussian_blur
def circular_extrema_indices(x):
    #Return the indices of all local extrema, treating the input as cyclic (TODO: perhaps add a non-cyclic version later)
    #If there is a continuous area where the derivative is 0, return the indices of the whole area (example: circular_extrema_indices([1,2,2,2,3]))
    #The order of the extremas returned is the relative order they originally appear in the input (as opposed to being sorted by value etc)
    #EXAMPLE: circular_extrema_indices([1,2,3,4])      -> [0 3]     #In this and the next three examples, notice how the shift affects the indices
    #EXAMPLE: circular_extrema_indices([4,1,2,3])      -> [0 1]     #Note how because this function treats the input as cyclic, and therefore the 3 at the end is not an extrema
    #EXAMPLE: circular_extrema_indices([3,4,1,2])      -> [1 2]
    #EXAMPLE: circular_extrema_indices([2,3,4,1])      -> [2 3]
    #EXAMPLE: circular_extrema_indices([0,1,2,3,2,1])  -> [0 3]     #Captures both local minima AND local maxima, aka the 0 and the 3
    #EXAMPLE: circular_extrema_indices([0,0,0,1,2,3])  -> [0 1 2 5] #Notice how areas with a derivative of 0 are all treated as extrema (aka the first three 0's)
    #EXAMPLE: circular_extrema_indices([])             -> []        #No elements in the input means no elements in the output
    #EXAMPLE: circular_extrema_indices([])             -> []        #No elements in the input means no elements in the output
    #EXAMPLE: circular_extrema_indices([A])            -> [A]       #True for all numeric values A. If we only have one point, it is technically an extrema.
    #EXAMPLE: circular_extrema_indices([A,B])          -> [A B]     #True for all numeric values A and B. If we only have two points, both are technically extremas.
    x=np.asarray(x)
    assert len(x.shape)==1,'Currently, only vectors are supported. This may change in the future.'
    r=np.roll(x, 1)#Right
    l=np.roll(x,-1)#Left
    return np.argwhere((x>r) & (x>l) | (x<r) & (x<l) | (x==r) | (x==l)).squeeze()
circ_extrema=circular_extrema_indices

def circ_diff_inverse(x):
    #Note that we lose a constant of integration
    #circ_diff(circ_diff_inverse(circ_diff(x))) == circ_diff(x)
    return np.cumsum(np.concatenate(([0],x)))[:-1]

def gcd(*i):#Unlike the default gcd, this can accept varargs
    from math import gcd as _gcd#_gcd because it took me a while to read this after coming back to it: there is no recursion involved
    from functools import reduce
    return reduce(_gcd,i,0)
gcf=gcd#Greatest common denominator and Greatest Common Factor are synonyms
def lcm(*i):#lcm doesn't exist in the math module
    from functools import reduce
    return reduce(lambda x,y:x*y//gcd(x,y),i,1)
def product(*i):#redefined from earlier in r.py, but it does the same thing. It's just written differntly (in a way that makes it less dependent on r.py; the last one used the 'scoop' function)
    from functools import reduce
    return reduce(lambda x,y:x*y,i,1)

from math import factorial
def ncr(n, r):
    #choose r objects from n
    from functools import reduce
    import operator as op
    r = min(r, n-r)
    numer = reduce(op.mul, xrange(n, n-r, -1), 1)
    denom = reduce(op.mul, xrange(1, r+1), 1)
    return numer//denom

def get_process_memory():
    import os
    pip_import('psutil')
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss#Get this process's total memory in bytes

def regex_match(string,regex):
    #returns true if the regex describes the whole string
    import re
    return bool(re.fullmatch(regex,string))
def regex_replace(string,regex,replacement):
    #Regex replacement. Example: regex_replace('from abc import def','from .* import (.*)',r'\1') == 'def'
    import re
    return re.sub(regex,replacement,string)

def ring_terminal_bell():
    print(end=chr(7),flush=True)#This character should ring the TTY's bell, if that's possible.

def pterm():
    pseudo_terminal(locals(),globals())

def set_cursor_to_bar():
    print(end="\033[6 q")#I'm not sure what the escape codes are for different terminals; tmux for example is a mystery.

def line_number():
    #Return the line number of the caller
    import inspect
    return inspect.currentframe().f_back.f_lineno

def is_number(x):
    #returns true if x is a number
    #Verified to work with numpy values as well as vanilla Python values
    #Also works with torch tensors
    #Examples:
    #   is_number(float)              ==True
    #   is_number(np.uint8)           ==True
    #   is_number(123)                ==True
    #   is_number(5.6)                ==True
    #   is_number(np.int32(123))      ==True
    #   is_number("Hello")            ==False
    #   is_number("123")              ==False
    #   is_number(np.asarray([1,2,3]))==False
    from numbers import Number
    if isinstance(x,Number) or isinstance(x,type) and issubclass(x,Number):
        return True
    #Does NOT work with torch tensors. I don't know if I should include that or not, so for now it returns false on torch tensors but the code is commented out and be uncommented.
    # try:
    #     #The above check fails for torch tensors. Here's a modification:
    #     if x.__class__.__name__=='Tensor' or x.__name__=='Tensor':#Try to avoid importing torch, as that takes a while...
    #         import torch#...we might not even have torch, which is why this is in a try-catch block
    #         if isinstance(x,torch.Tensor) or isinstance(x,type) and issubclass(x,torch.Tensor):
    #             return True
    # except:pass#Maybe we don't have torch.
    return False


def line_join(iterable,separator='\n'):
    return separator.join(map(str,iterable))

def pip_install(pip_args:str):
    assert isinstance(pip_args,str),'pip_args must be a string like "numpy --upgrade" or "rp --upgrade --no-cache --user" etc'
    import os
    if currently_running_unix():
        #Attempt to get root priveleges. Sometimes we need root priveleges to install stuff. If we're on unix, attempt to become the root for this process. There's probably a better way to do this but idk how and don't really care that much even though I probably should...
        os.system('sudo echo')#This should only prompt for a password once...making the next command run in sudo.
    os.system(sys.executable+' -m pip install '+pip_args)
    #DONT DELETE THIS COMMENT BLOCK: An alternative way to install things with pip:
    #    from pip.__main__ import _main as pip
    #    errored=pip(['install', package_name]+['--upgrade']*upgrade)
    #    if errored:
    #        assert False,'pip_install: installation of module '+repr(package_name)+' failed.'

def module_exists(module_name):
    # https://www.tutorialspoint.com/How-to-check-if-a-python-module-exists-without-importing-it
    import imp
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

known_pypi_module_package_names={
    # A list of some non-obvious pypi package names given their module names, used by pip_import
    # Let's make this dict as big as we can! More the merrier...
    'cv2':'opencv-python',
    'prompt_toolkit':'prompt-toolkit',
    'editor':'python-editor',
    'rtmidi':'python-rtmidi',
    'PIL':'Pillow',
    'skvideo.io':'sk-video',
    'lib2to3':'2to3',
    'skimage':'scikit-image',
    'serial':'pyserial',#WARNING: there is a 'pip install serial' which ALSO creates a 'serial' module. This module is the WRONG SERIAL MODULE.
}
def pip_import(module_name,package_name=None):
    #Attempts to import a module, and if successful returns it.
    #If it's unsuccessful, it attempts to find it on pypi, and if
    #    it can, it asks you if you'd like to install it, and if
    #    you say 'yes', rp will attempt to install it for you.
    #
    #The rp module uses tons and tons of packages from pypi.
    #You don't need to install all of them to make rp work,
    #    because not all functions need all of these packages.
    #However, when you DO need a certain package's module,
    #    and we try importing it, we get an import error.
    #Normally, this isn't a problem, because most packages on pypi
    #    have the same package name as the module name.
    #For example: 'pip install rp' allows 'import rp', because the pypi-name
    #    and the import name are the same thing.
    #Some modules break this rule though. For example, opencv:
    #    opencv is installed with 'pip install opencv-python' and imported like 'cv2=pip_import('cv2')'.
    #Obviously, "cv2"!="opencv-python". And because of this, when you get an error "can't cv2=pip_import('cv2')",
    #    you can't just fix it with 'pip install cv2'. You have to google it. That's annoying.
    #THIS FUNCTION addresses that problem. pip

    assert isinstance(module_name,str),'pip_import: error: module_name must be a string, but got type '+repr(type(module_name))#Probably better done with raise typerror but meh whatever

    if package_name is None:
        package_name=module_name
    if package_name in known_pypi_module_package_names:
        package_name=known_pypi_module_package_names[package_name]

    import importlib
    try:
        return importlib.import_module(module_name)
    except ImportError:
        if module_exists(module_name):
            raise #We're getting an import error for some reason other than not having installed the module
        if connected_to_internet():
            if input_yes_no("Failed to import module "+repr(module_name)+'. You might be able to get this module by installing package '+repr(package_name)+' with pip. Would you like to try that?'):
                print("Attempting to install",package_name,'with pip...')
                pip_install(package_name)
                fansi_print("pip_import: successfully installed package "+repr(package_name)+"; attempting to import it...",'green',new_line=False)
                assert module_exists(module_name),'pip_import: error: Internal assertion failed (rp thought we successfully installed your package, but perhaps it didnt actually work. Right now I dont know how to detect this). pip_import needs to be fixed if you see this message.'
                out=pip_import(module_name,package_name)#This shouldn't recurse more than once
                fansi_print("success!",'green')
                return out
            else:
                print("...very well then. Throwing an import error...")
                raise
        else:
            #We would fail to install the package becuase we have no internet
            fansi_print("pip_import: normally we would try to install your package via pip, but you're not connected to the internet. Failed to pip_install("+repr(package_name)+')')
            raise

def powerset(iterable,reverse=False):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    #From https://stackoverflow.com/questions/18035595/powersets-in-python-using-itertools
    from itertools import chain, combinations
    s = list(iterable)
    order=range(len(s)+1)
    if reverse:
        order=reversed(order)
    return chain.from_iterable(combinations(s, r) for r in order)

def print_fix(ans):
    #Meant to use this command in the pseudoterminal: `print_fix\py
    #Turn all python2 print statements (without the parenthesis) into python3-style statements
    #Example: print_fix('if True:\n\tprint 5')    ====    'if True:\n\tprint(5)'
    ans=ans.splitlines()
    for i,e in enumerate(ans):
        if e.lstrip().startswith('print '):
            j=len(e)-len(e.lstrip())+len('print')
            e=e[:j]+'('+e[j+1:]+')'
            ans[i]=e
    ans=line_join(ans)
    return ans

def remove_all_whitespace(string):
    return ''.join(string.split())#Remove all whitespace

def delete_empty_lines(string):
    return '\n'.join(line for line in string.splitlines() if line.strip())

#region OpenCV Helpers

def _single_line_cv_text_to_image(text,*,scale,font,thickness,color):
    #EXAMPLE:
    #    display_image(cv_text_to_image('HELLO WORLD! '))
    #This is a helper function for cv_text_to_image, which can handle multi-line text
    assert isinstance(text,str)
    assert isinstance(font,int)
    cv2=pip_import('cv2')
    dims=cv2.getTextSize(text,font,scale,thickness)[0][::-1] #The dimensions of the output image
    image=np.zeros((dims[0]+thickness//2+1,dims[1],3),np.uint8)
    return cv2.putText(image,text,(0,dims[0]),font,scale,color,thickness)
def cv_text_to_image(text,*,scale=2,font=3,thickness=2,color=(255,255,255)):
    lines=text.splitlines()
    images=[]
    for line in lines:
        images.append(_single_line_cv_text_to_image(line,scale=scale,font=font,thickness=thickness,color=color))
    return vertically_concatenated_images(images)

def cv_bgr_rgb_swap(image_or_video):
    #Works for both images AND video
    #Opencv has an annoying feature: it uses BGR instead of RGB. Heckin' hipsters. This swaps RGB to BGR, vice-versa.
    image_or_video=np.asarray(image_or_video)
    image_or_video=image_or_video.copy()
    temp=image_or_video.copy()
    image_or_video[...,0],image_or_video[...,2]=temp[...,2],temp[...,0]
    return image_or_video
cv_rgb_bgr_swap=cv_bgr_rgb_swap#In-case you forgot what to type. It's all the same thing though.

def cv_imshow(img,label="cvImshow",*,
        img_is_rgb=True,#As opposed to BGR. If this is true, then the R and B channels are swapped before the image is displayed.
        wait=10,#Set to None to skip waiting all-together (will have to wait at some point or else the images won't display)
        on_mouse_down =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_mouse_move =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_mouse_up   =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_key_press  =None  #Either set to None or some function like lambda key:print(key).
        # on_key_press will either be sent a character representing the key (such as pressing 'a' makes key='a') or else a multi-character string describing it. Examples: 'left','right','backspace','delete'
        ):
    #A non-blocking image display, using OpenCV
    tensor_shape=img.shape
    ndim=len(tensor_shape)
    assert ndim in {2,3},'Cannot display img, because img.shape == '+str(img.shape)
    if not np.prod(tensor_shape):
        return#If the dimensions are like (0,0,3) it means we have no height and width, and opencv will cause an error if we try to display that image. This is not useful, so we just return and don't display the image.
    img_is_grayscale=ndim==2#If there are only two dimensions
    assert(len(img))
    cv2=pip_import('cv2')
    if img_is_rgb and not img_is_grayscale:
        img=cv_bgr_rgb_swap(img)
    if is_binary_image(img):
        img=as_byte_image(img)#Avoid ERROR: TypeError: mat data type = 0 is not supported thrown by opencv's imshow
    assert isinstance(label,str),"cvImshow: Inputted label is not a string: repr(label) == "+repr(label)
    def mouse_callback(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN and on_mouse_down:on_mouse_down(x=x,y=y)
        if event==cv2.EVENT_MOUSEMOVE   and on_mouse_move:on_mouse_move(x=x,y=y)
        if event==cv2.EVENT_LBUTTONUP   and on_mouse_up  :on_mouse_up  (x=x,y=y)
    cv2.namedWindow(label,cv2.WINDOW_KEEPRATIO)#cv2.WINDOW_KEEPRATIO lets us resize the window in the window's gui. By the way, for future reference, this function (cv2.namedWindow) has no effect if the window allready exists.
    if on_mouse_down or on_mouse_move or on_mouse_up:#If any of these are set (and not None), then we overwrite the mousecallback for this namedWindow
        cv2.setMouseCallback(label,mouse_callback)#This makes it interactive. It will also overwrite any

    if running_in_google_colab():
        pass
        print("rp.cv_imshow: Warning: Cannot use cv_imshow in google colab. Sorry. Maybe this will change in the future.")
        # from google.colab.patches cv2=pip_import('cv2')_imshow#[From google colab documentation] The cv2.imshow() and cv.imshow() functions from the opencv-python package are incompatible with Jupyter notebook
        # cv2_imshow(label,img)#https://github.com/jupyter/notebook/issues/3935
    else:
        cv2.imshow(label,img)#Wait is in millis

    if wait is not None:
        key=cv2.waitKey(max(1,wait//2))
        if key==-1:
            key=None#Opencv returns -1 when key was pressed. I'll call it None.
        if on_key_press and key is not None:
            # https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv
            try:
                key=chr(key)
            except ValueError:#Something like "ValueError: chr() arg not in range(0x110000)", which means we pressed a non-character key like delete or the left arrow key etc
                pass#This section doesn't work well right now
                # recognized_keys={
                #     2490368:'up',
                #     2621440:'down',
                #     2424832:'left',
                #     2555904:'right',
                #     3014656:'delete',
                #     }
                # if key in recognized_keys:
                #     key=recognized_keys[key]
                # else:
                    #Unrecognized key
                    # key=None
            if key=='\r':
                key='\n'#The enter key returns '\r' using opencv, but we want it to return the more familiar '\n'
            if key!=None:
                on_key_press(key)

def _cv_helper(*,image,copy,antialias):
    cv2=pip_import('cv2')
    #This function exists to remove redundancy from other OpenCV helper functions in rp
    kwargs={}
    if antialias:kwargs['lineType']=cv2.LINE_AA#Whether to antialias the things we draw
    if copy     :image=image.copy();#s_byte_image(as_rgb_image(image))#Decide whether we should mutate an image or create a new one (which is less efficient but easier to write in my opinion)
    return image,kwargs

class Contour(np.ndarray):
    # __slots__ = ['parent','children','_descendants_cache','_is_inner_cache']#Prevent adding new attriutes. This makes it faster.
    @property
    def is_inner(self):
        #https://stackoverflow.com/questions/45323590/do-contours-returned-by-cvfindcontours-have-a-consistent-orientation
        if hasattr(self,'_is_inner_cache'):
            return self._is_inner_cache
        self._is_inner_cache=is_counter_clockwise(self)#Edge case I don't know what to do with: what should we return if  len(self)<=2?
        return self._is_inner_cache

    @property
    def is_outer(self):
        return not self.is_inner#Edge case I don't know what to do with: what should we return if  len(self)<=2? Same problem as in is_inner

    @property
    def is_solid_white(self):
        return not self.children and self.is_outer

    @property
    def is_solid_black(self):
        return not self.children and self.is_inner

    @property
    def descendants(self):
        #Return not just the immediate children, but their children's children etc recursively
        if hasattr(self,'_descendants_cache'):
            return self._descendants_cache
        def helper():
            for child in self.children:
                yield child.descendants()
            yield self
        self._descendants_cache = list(helper())
        return self._descendants_cache
def cv_find_contours(image,*,include_every_pixel=False):
    cv2=pip_import('cv2')
    #Contours are represented in the form [[x,y],[x,y],[x,y]].
    #If you want to get rid of the extra, useless dimension, don't forget to use .squeeze()
    #NOTE: This doesn't return normal numpy arrays: The output arrays subclass numpy.ndarray and have these attributes:
    #   parent, children, descendants, is_inner, is_outer, is_solid_white, is_solid_black
    #This is really useful, because it's like hierarchy but much easier to use. The parent of a contour is the contour immediately and completely surrounding it (None if no such contour exists.) This is calculated from the hierarchy.
    # 'contour.is_inner' is always the same as 'not contour.is_outer'. It returns whether it is an inner or an outer contour
    #If include_every_pixel is true, we include every single coordinate in our contour, using CHAIN_APPROX_NONE. Otherwise, opencv will simplify vertical and horizontal segments of pixels into a single edge (which is almost lossless)
    image=as_grayscale_image(image)
    raw_contours, hierarchy = cv2.findContours(image,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE if include_every_pixel else cv2.CHAIN_APPROX_SIMPLE)[-2:]


    contours=[as_points_array(raw_contour).view(Contour) for raw_contour in raw_contours]#This is how we subclass numpy arrays (by using (some ndarray).view(wrapper class))

    for contour in contours:
        contour.parent=None
        contour.children=[]

    try:
        hierarchy=hierarchy[0]
        for info,contour in zip(hierarchy,contours):
            parent_index=info[3]
            if parent_index != -1:#Opencv tells us that the contour has no parents by telling us it is its own parent, and therefore is its own child. I think it makes more sense to say its parent is None (which is the default value)
                parent=contours[parent_index]#How to read the opencv contour hierarchy: https://stackoverflow.com/questions/22240746/recognize-open-and-closed-shapes-opencv
                contour.parent=parent
                parent.children.append(contour)
    except TypeError:pass#ERROR: TypeError: 'NoneType' object is not iterable (due to hierarchy being None before hierarchy=hierarchy[0])

    return contours

def cv_distance_to_contour(contour,x,y):
    #Return the distance from x,y to the point on contour closest to x,y
    cv2=pip_import('cv2')
    contour=as_cv_contour(contour)
    return abs(cv2.pointPolygonTest(contour,(x,y),True))

def cv_closest_contour_point(contour,x,y):
    #Return the point on contour closest to x,y
    cv2=pip_import('cv2')
    points=as_points_array(points)
    diffs=points-[x,y]
    squared_diffs=diffs**2
    squared_dists=sum(diffs**2,1)
    index=min_valued_index(squared_dists)
    return tuple(points[index])

def cv_closest_contour(contours,x,y):
    #Return the contour with a point closest to x,y
    cv2=pip_import('cv2')
    assert len(contours)!=0,'cv_closest_contour: error: There are no contours to pick from because len(contours)==0'
    def distance(contour):
        return cv_distance_to_contour(contour,x,y)
    return min(contours,key=distance)

def cv_draw_contours(image,contours,color=(255,255,255),width=1,*,fill=False,antialias=True,copy=True):
    #TODO: Important: This must somehow preserve whether the contour is closed or not??
    cv2=pip_import('cv2')
    contours=list(map(as_cv_contour,contours))
    image,kwargs=_cv_helper(image=image,copy=copy,antialias=antialias)
    cv2.drawContours(image,contours,-1,color,width,**kwargs)
    if fill:cv2.fillPoly(image,contours,color)
    return image

def cv_draw_contour(image,contour,*args,**kwargs):
    return cv_draw_contours(image,[contour],*args,**kwargs)

def cv_contour_length(contour,closed=False):
    cv2=pip_import('cv2')
    contour=as_cv_contour(contour)
    return cv2.arcLength(contour,closed=closed)

def cv_contour_area(contour,closed=False):
    cv2=pip_import('cv2')
    contour=as_cv_contour(contour)
    return cv2.contourArea(contour)

def cv_draw_circle(image,x,y,radius=5,color=(255,255,255),*,antialias=True,copy=True):
    cv2=pip_import('cv2')
    image,kwargs=_cv_helper(image=image,copy=copy,antialias=antialias)
    cv2.circle(image,(x,y),radius,color,-1,**kwargs)
    return image

def cv_apply_affine_to_image(image,affine,output_resolution=None):
    #Warps an image to the affine matrix provided (of shape 2,3)
    #output_resolution is to speed things up when we don't want the full resolution of the original image. It can be specified as None to get the default (original) image resolution, or some tuple with 2 ints to represent resolution
    #EXAMPLE: display_image(cv_apply_affine_to_image(pup,rotation_affine_2d(60/360*tau)))
    cv2=pip_import('cv2')
    image=np.asarray(image)
    affine=np.asarray(affine)
    if output_resolution is None:
        output_resolution=image.shape[:2][::-1]
    if is_number(output_resolution):
        output_resolution=tuple(x*output_resolution for x in image.shape[:2][::-1])#If output resolution is just a number, we use it as a scaling factor to the original image (so .5 means 1/2 the dimensions of the original image etc)
    assert isinstance(output_resolution,tuple) and len(output_resolution)==2
    return cv2.warpAffine(image,np.asarray(affine).astype(np.float32),output_resolution)



def cv_manually_selected_contours(contours,image=None):
    #Let the user manually pick out a set of contours by clicking them, then hitting the enter key to confirm their selection
    #It shows you an image with contours. Click to toggle the contours on and off.
    #Optionally, you can specify a background image to be shown during this selection. This is particularly useful if the contours originally came from that image. I personally like to divide that image by 2 to make it darker, letting the contours pop out more apparently.
    #Special keys: press "b" to toggle a black background with your image, to help see the contours better
    #Special keys: press "a" to select all contours
    #Special keys: press "d" to deselect all contours
    #Special keys: press "\n" confirm your selection

    assert not running_in_google_colab(),'Sorry, cv_manually_selected_contours uses OpenCVs gui and cannot be used inside a Jupyter notebook'
    assert len(contours)!=0,'manually_selected_contours: error: There are no contours to pick from because len(contours)==0'

    #Set up the background image
    if image is None:
        #Specifying 'image' is optional
        image=contours_to_image(contours,crop=False)
    image=as_byte_image(image)
    image= as_rgb_image(image)
    alternative_image=image*0#Swap between these by pressing "b"

    display_needs_update=True

    #Record where the mouse moves and which contour it's selecting
    mouse_x=mouse_y=mouse_contour=None
    def on_mouse_move(x,y):
        nonlocal mouse_x,mouse_y,mouse_contour,display_needs_update
        mouse_x=x
        mouse_y=y
        new_mouse_contour=cv_closest_contour(contours,mouse_x,mouse_y)
        if id(mouse_contour)!=id(new_mouse_contour):
            display_needs_update=True
            mouse_contour=new_mouse_contour

    selected_contours=dict()#dict mapping id(contour) to contour
    def on_mouse_down(x,y):
        nonlocal display_needs_update
        if mouse_contour is None:
            return
        key=id(mouse_contour)#We keep track of the countours by memory address because numpy arrays are not hashable and we never create new contours in this function

        #Toggle the existence of mouse_contour in selected_contours
        if key in selected_contours:
            del selected_contours[key]
        else:
            selected_contours[key]=mouse_contour
        display_needs_update=True

    done=False
    def on_key_press(key):
        nonlocal done,image,alternative_image,display_needs_update,contours,selected_contours
        if key=='b':
            #Swap the background image between black and the original.
            #Has no meaningful effect if we didn't specify a background image in the first place, because the default is black
            image,alternative_image=alternative_image,image
            display_needs_update=True
        elif key=='a':
            #Select all contours
            selected_contours.update({id(contour):contour for contour in contours})
            display_needs_update=True
        elif key=='d':
            #Deselect all contours
            selected_contours.clear()
            display_needs_update=True
        elif key=='\n':
            #Pressing the enter key makes it return the result
            done=True

    while True:
        if display_needs_update:
            #Don't re-render unless necessary
            display_needs_update=False

            #Draw the contours
            display    =image.copy()
            if mouse_contour is not None:
                display=cv_draw_contour (display,mouse_contour             ,color=(255,255,255),width=5,antialias=False)
            display    =cv_draw_contours(display,contours                  ,color=(255,0  ,0  ),width=2,antialias=False)
            display    =cv_draw_contours(display,selected_contours.values(),color=(0  ,255,255),width=2,antialias=False)

            #Display the result
        cv_imshow(display                    ,
                  on_mouse_move=on_mouse_move,
                  on_mouse_down=on_mouse_down,
                  on_key_press =on_key_press)

        #Check to see if we're done
        if done:
            return list(selected_contours.values())



def cv_manually_selected_contour(contours,image=None):
    #TODO Merge cv_manually_selected_contours with cv_manually_selected_contour to eliminate redundancy
    #Let the user manually pick out a contour by clicking it, then hitting the enter key to confirm your selection
    #It shows you an image with contours. Click to toggle the contours on and off.
    #Optionally, you can specify a background image to be shown during this selection. This is particularly useful if the contours originally came from that image. I personally like to divide that image by 2 to make it darker, letting the contours pop out more apparently.
    #Special keys: press "b" to toggle a black background with your image, to help see the contours better
    #Special keys: press "\n" confirm your selection

    assert not running_in_google_colab(),'Sorry, cv_manually_selected_contours uses OpenCVs gui and cannot be used inside a Jupyter notebook'
    assert len(contours)!=0,'manually_selected_contours: error: There are no contours to pick from because len(contours)==0'

    #Set up the background image
    if image is None:
        #Specifying 'image' is optional
        image=contours_to_image(contours,crop=False)
    image=as_byte_image(image)
    image= as_rgb_image(image)
    alternative_image=image*0#Swap between these by pressing "b"

    display_needs_update=True

    #Record where the mouse moves and which contour it's selecting
    mouse_x=mouse_y=mouse_contour=None
    def on_mouse_move(x,y):
        nonlocal mouse_x,mouse_y,mouse_contour,display_needs_update
        mouse_x=x
        mouse_y=y
        new_mouse_contour=cv_closest_contour(contours,mouse_x,mouse_y)
        if id(mouse_contour)!=id(new_mouse_contour):
            display_needs_update=True
            mouse_contour=new_mouse_contour

    selected_contour=None
    def on_mouse_down(x,y):
        nonlocal display_needs_update,mouse_contour,selected_contour
        if mouse_contour is None:
            return
        key=id(mouse_contour)#We keep track of the countours by memory address because numpy arrays are not hashable and we never create new contours in this function

        selected_contour=mouse_contour#Select the contour we clicked
        display_needs_update=True

    done=False
    def on_key_press(key):
        nonlocal done,image,alternative_image,display_needs_update,contours,selected_contour
        if key=='b':
            #Swap the background image between black and the original.
            #Has no meaningful effect if we didn't specify a background image in the first place, because the default is black
            image,alternative_image=alternative_image,image
            display_needs_update=True
        elif key=='\n':
            #Pressing the enter key makes it return the result
            if selected_contour is not None:#To return the result we must have selected a contour
                done=True

    while True:
        if display_needs_update:
            #Don't re-render unless necessary
            display_needs_update=False

            #Draw the contours
            display    =image.copy()
            if mouse_contour    is not None:
                display=cv_draw_contour (display,mouse_contour   ,color=(255,255,255),width=5,antialias=False)
            display    =cv_draw_contours(display,contours        ,color=(255,0  ,0  ),width=2,antialias=False)
            if selected_contour is not None:
                display=cv_draw_contour (display,selected_contour,color=(0  ,255,255),width=2,antialias=False)

            #Display the result
        cv_imshow(display                    ,
                  on_mouse_move=on_mouse_move,
                  on_mouse_down=on_mouse_down,
                  on_key_press =on_key_press)

        #Check to see if we're done
        if done:
            return selected_contour

def cosine_similarity(x,y):
    return np.sum(normalized(x)*normalized(y).conj())

# def fourier_descriptor(contour,*,order=10,normalize=True):
#     # import pyefd
#     # contour=np.asarray(contour).squeeze()
#     # descriptor=pyefd.elliptic_fourier_descriptors(contour, order=order, normalize=normalize).flatten()[3 if normalize else 0:]
#     # # descriptor/=np.arange(len(descriptor))+1#Make higher harmonics worth less
#     # return descriptor
#     def complex_descriptors(points,approach='mean'):
#         assert approach in 'mean','delta'#Try both of these and see which is better
#         #TODO: How do we ensure all of these points are clockwise?
#         #TODO: Right now we just assume all of these points are clockwise...this function shouldn't need that assumption, though.
#         #EXAMPLE: complex_descriptors([[1,1],[1,2],[2,2],[2,1]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #four points of a square  (... means there are just 4 duplicate elements with this value in the array)
#         #EXAMPLE: complex_descriptors([[0,0],[0,1],[1,1],[1,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #translated down by 1
#         #EXAMPLE: complex_descriptors([[0,1],[1,1],[1,0],[0,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #rotated 90 degrees (shifted order of points)
#         #EXAMPLE: complex_descriptors([[0,2],[2,2],[2,0],[0,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #scaled up by 2
#         #EXAMPLE: complex_descriptors([[1,2],[2,2],[2,0],[0,0]])  -> [[-0.5-1.j   0.2-0.4j  0. -2.j  -0. -1.j ]
#         #                                                             [ 0. -2.j  -0. -1.j  -0.5-1.j   0.2-0.4j]
#         #                                                             [-0. -1.j  -0.5-1.j   0.2-0.4j  0. -2.j ]
#         #                                                             [ 0.2-0.4j  0. -2.j  -0. -1.j  -0.5-1.j ]]#Made it asymmetrical; so now we have four different possible shifts
#         points=np.asarray(points,np.complex128)
#         assert points.shape[1]==2

#         #Make turn all the 2d points (x,y) into complex scalars x+yi (where i is the imaginary constant)
#         points=points[:,0]+points[:,1]*1j

#         #Right now we're still dealing with complex numbers...

#         if approach=='delta':points=np.roll(points,-1)-points#Get raw difference points (position invariance)
#         if approach=='mean' :points=points-np.mean(points,0) #Altenrative approach: Subtract the mean (position invariance)
#         points=np.roll(points,-1)/points#Get rotation vectors required (both scale and rotation invariance)
#         #Note that we do NOT have to explicitly normalize any vectors to obtain scale invariance. Division does that implicitly.
#         return points
#         #Return every possible shift for these points
#         #return np.abs(np.fft.fft(points))
#         #return all_rolls(points)

#     #If normalize, invariant to scale, rotation, and position
#     #Notes: this seems to be invariant to subdivision (taking one edge and breaking it into two while keeping the same shape)
#     #   fourier_descriptor([[0,0],[0,1],[1,1],[1,0]])  ====  fourier_descriptor([[0,0],[0,1],[1,1],[1,.5],[1,0]])  (They're exactly equal on almost all of the elements of the result, barring two of the descriptors' floating point errors)
#     #   Therefore it is probably safe to decimate a contour first if speed is important.
#     return np.abs(np.fft.fft(complex_descriptors(evenly_split_path(np.squeeze(contour),250))))[:20]

# def fourier_descriptor_distance(contour_1,contour_2,**fourier_descriptor_kwargs):
#     #For guidance on how to use fourier_descriptor_kwargs, see the kwargs of fourier_descriptor
#     return euclidean_distance(fourier_descriptor(contour_1,**fourier_descriptor_kwargs),
#                               fourier_descriptor(contour_2,**fourier_descriptor_kwargs))

# def fourier_descriptor_similarity(contour_1,contour_2,**fourier_descriptor_kwargs):
#     #For guidance on how to use fourier_descriptor_kwargs, see the kwargs of fourier_descriptor
#     normalized_dot_product(fourier_descriptor(contour_1,**fourier_descriptor_kwargs),
#                                   fourier_descriptor(contour_2,**fourier_descriptor_kwargs))
#     return normalized_dot_product(fourier_descriptor(contour_1,**fourier_descriptor_kwargs),
#                                   fourier_descriptor(contour_2,**fourier_descriptor_kwargs))

# def cv_contour_match(a,b,scale_invariant=False):

#     def conv_circ( signal, kernel ):
#         '''
#             signal: real 1D array
#             kernel: real 1D array
#             signal and kernel must have same shape/length
#         '''
#         return np.fft.ifft(np.fft.fft(signal)*np.fft.fft(kernel))

#     def complex_descriptor(points,approach='mean'):
#         assert approach in 'mean','delta'#Try both of these and see which is better
#         #TODO: How do we ensure all of these points are clockwise?
#         #TODO: Right now we just assume all of these points are clockwise...this function shouldn't need that assumption, though.
#         #EXAMPLE: complex_descriptors([[1,1],[1,2],[2,2],[2,1]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #four points of a square  (... means there are just 4 duplicate elements with this value in the array)
#         #EXAMPLE: complex_descriptors([[0,0],[0,1],[1,1],[1,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #translated down by 1
#         #EXAMPLE: complex_descriptors([[0,1],[1,1],[1,0],[0,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #rotated 90 degrees (shifted order of points)
#         #EXAMPLE: complex_descriptors([[0,2],[2,2],[2,0],[0,0]])  -> [[ 0.-1.j -0.-1.j -0.-1.j  0.-1.j]...]  #scaled up by 2
#         #EXAMPLE: complex_descriptors([[1,2],[2,2],[2,0],[0,0]])  -> [[-0.5-1.j   0.2-0.4j  0. -2.j  -0. -1.j ]
#         #                                                             [ 0. -2.j  -0. -1.j  -0.5-1.j   0.2-0.4j]
#         #                                                             [-0. -1.j  -0.5-1.j   0.2-0.4j  0. -2.j ]
#         #                                                             [ 0.2-0.4j  0. -2.j  -0. -1.j  -0.5-1.j ]]#Made it asymmetrical; so now we have four different possible shifts
#         points=np.asarray(points,np.complex128)
#         assert points.shape[1]==2

#         #Make turn all the 2d points (x,y) into complex scalars x+yi (where i is the imaginary constant)
#         points=points[:,0]+points[:,1]*1j

#         #Right now we're still dealing with complex numbers...

#         if approach=='delta':points=np.roll(points,-1)-points#Get raw difference points (position invariance)
#         if approach=='mean' :points=points-np.mean(points,0) #Altenrative approach: Subtract the mean (position invariance)
#         points=np.roll(points,-1)/points#Get rotation vectors required (both scale and rotation invariance)
#         #Note that we do NOT have to explicitly normalize any vectors to obtain scale invariance. Division does that implicitly.

#         return points

#     def ryan_match(from_points,to_points):
#         df=complex_descriptor(from_points)#Descriptor from
#         dt=complex_descriptor(  to_points)#Descriptor to
#         df=df/np.linalg.norm(df)
#         dt=dt/np.linalg.norm(dt)
#         c=conv_circ(df,np.conjugate(dt[::-1]))#This is just a hunch...I dont completely understand what Im doing yet
#         c=c.real
#         return 1-max(c)


#     return ryan_match(a.squeeze(),b.squeeze())

#     #QUICK HACK GET RID OF THIS
#     #Compare two contours: a and b. Returns a float.
#     #The closer the output is to 0, the better the match between a and b.
#     #This is invariant to rotation, scale, and translation (it uses hu moments to compare contours)
#     #https://docs.opencv.org/3.1.0/d5/d45/tutorial_py_contours_more_functions.html
#     cv2=pip_import('cv2')
#     # out=cv2.matchShapes(a,b,1,0.0)
#     n=lambda x:x/np.linalg.norm(x)
#     hu=lambda contour:cv2.HuMoments(cv2.moments(contour))
#     da=[*n(fourier_descriptor(a))*1]#,*n(hu(a))]#descriptor a
#     db=[*n(fourier_descriptor(b))*1]#,*n(hu(b))]#descriptor b
#     return 1-np.dot(da,db)
#     if not scale_invariant:
#         #There should be some way to make the hu moments simply not be invariant to scale, but I don't know how to do this
#         #TODO: Do that ^
#         #This doesn't seem to have much effect...and I think that's OK for now...
#         #TODO: Clean this function up...in particular, right here:
#         #For now, we'll just add the contour length to the output
#         out*=np.exp((np.log(cv_contour_length(a)+1)-np.log(cv_contour_length(b)+1))**2)
#         out*=np.exp((np.log(cv_contour_area  (a)+1)-np.log(cv_contour_area  (b)+1))**2)
#         pass
#     # out+=cv2.createHausdorffDistanceExtractor().computeDistance(a,b)
#     return out
# def cv_best_match_contour(contour,contours,**kwargs):
#     #Given a target contour and a list of contours, return the closest match to contour among contours
#     #(Intended to be used to search for a contour in an image)
#     assert is_iterable(contours)
#     return min(contours,key=lambda candidate:cv_contour_match(contour,candidate,**kwargs))
# def cv_best_match_contours(contour,contours,n=None,**kwargs):
#     #Return the n best matches to contour in contours
#     assert is_iterable(contours)
#     return sorted(contours,key=lambda candidate:cv_contour_match(contour,candidate,**kwargs))[:n or len(contours)]

def _cv_morphological_helper(image,diameter,cv_method,*,copy,circular,iterations):
    #Used for erosion, dilation, and other functions.
    #Please see the documentation if you'd like to know what a morpholocical filter is:
    #https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    original_dtype=image.dtype
    if image.dtype==bool:image=image.astype(np.uint8)
    if copy:image=image.copy()
    if diameter==0:return image
    if circular:
        kernel=flat_circle_kernel(diameter)
        kernel=kernel.astype(image.dtype)
        image  = cv_method(image,kernel,iterations=iterations)
    else:
        #Uses a box kernel. Runs very quickly because it takes two orthoganal 1-d passes.
        for kernel in (diameter,1),(1,diameter):
            kernel = np.ones(kernel,image.dtype)
            image  = cv_method(image,kernel,iterations=iterations)
    if original_dtype==bool:image=image.astype(bool)
    return image
def cv_erode (image,diameter=2,*,copy=True,circular=False,iterations=1):
    #TODO min_filter is now kinda redundant, and slower if you dont have opencv. What to do about that?
    cv2=pip_import('cv2')
    return _cv_morphological_helper(image,diameter,cv_method=cv2.erode ,copy=copy,circular=circular,iterations=iterations)
def cv_dilate(image,diameter=2,*,copy=True,circular=False,iterations=1):
    #Dilates image with a box kernel. Runs very quickly because it takes two orthoganal 1-d passes.
    #TODO max_filter is now kinda redundant, and slower if you dont have opencv. What to do about that?
    cv2=pip_import('cv2')
    return _cv_morphological_helper(image,diameter,cv_method=cv2.dilate,copy=copy,circular=circular,iterations=iterations)

def cv_gauss_blur(image,sigma=1):
    cv2=pip_import('cv2')
    sigma=int(sigma)
    if not sigma%2:
        sigma+=1#Make sigma odd
    return cv2.GaussianBlur(image,(sigma,sigma),0)



#endregion

def rotation_matrix(angle,out_of=tau):
    #Set out_of to 360 to use degrees instead of radians
    theta = angle/out_of*tau#Convert to radians
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c,-s), (s, c)))
    return R

def loop_direction_2d(loop):
    #loop is like [(x,y),(x,y)...]
    #Given a list of 2d points, return a negative number if they're clockwise else a positive number if theyre conuter-clockwise
    #https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
    #Of course, if a loop has 0, or 1 points, then it's neither counter clockwise nor clockwise so it returns 0
    loop=as_points_array(loop)
    if len(loop)<=2:return 0#If we have 2 or less points in this loop, it doesn't make sense to say that it's clockwise or counter-clockwise
    assert loop.shape[1]==2,'loop_direction_2d is for 2d loops only'
    next=np.roll(loop,-1,axis=0)
    next[:,0]*=-1
    return np.sum(np.prod(loop+next,1))
def is_clockwise(loop):
    #loop is like [(x,y),(x,y)...] (two dimensions)
    return loop_direction_2d(loop)<0
def is_counter_clockwise(loop):
    #loop is like [(x,y),(x,y)...] (two dimensions)
    return loop_direction_2d(loop)>0
def cv_make_clockwise(contour):
    return contour if is_clockwise(contour) else contour[::-1]



def scatter_plot(x,y=None,*,block=False,clear=True,dot_size=1):
    #Parameters:
    #   x and y:
    #       There are three ways to give this function points:
    #          - One is by specifying x and y as lists of numbers, where x and y are the same length, like x==[x0,x1,x2...] and y==[y0,y1,y2...]
    #          - Another is by leaving y None, and x is a list of points like [(x0,y0),(x1,y1),(x2,y2)...] or the numpy equivalent
    #          - Another is to specify x as a complex vector and leave y blank
    #   clear: if this is true, wipe the plot clean before drawing (if it's false, this plot will be drawn over whatever happens to exist there allready)
    #   block: whether to pause the python program and make the plot interactive until closed (blocks the main thread I think)
    #   dot_size: how big/thick should the points on the plot be?
    #EXAMPLE: scatter_plot(randints_complex(100))
    #EXAMPLE: x=np.linspace(0,tau);scatter_plot(np.cos(x),np.sin(x))
    #EXAMPLE: scatter_plot((.9+.2j)**np.linspace(0,10*tau))#A spiral
    if is_complex_vector(x):
        assert y is None,'scatter_plot: x is a complex vector but y is not None. This is an invalid input combination as the imaginary part of x ARE the y-values'
        x=as_points_array(x)
    if y is None:
        #x was given as a point list where x==[(x0,y0),(x1,y1),(x2,y2)...] and y==None
        if len(x):
            x,y=zip(*x)#Convert to x==[x0,x1,x2...] and y==[y0,y1,y2...]
        else:
            x=y=[]
    global plt
    pip_import('matplotlib')
    plt=_get_plt()
    if clear and plt:
        #Clear the plot (wipe it clean of any(previous drawings)
        plt.clf()
    plt.scatter(x,y,
        s=dot_size#The size of the dots. Smaller value --> smaller dots. The default is too big for my taste.
        )
    plt.show(block=block)
    if not block:
        plt.pause(.01)

def line_split(string):
    #I find myself often wishing this function exists for a few seconds before remembering String.splitlines exists
    #EXAMPLE: line_split('hello\nworld')==['hello','world']
    return string.splitlines()
def line_join(lines):
    #EXAMPLE: line_join(['hello','world'])=='hello\nworld'
    return '\n'.join(lines)

#region numpy utilities
def append_uniform_row(matrix,scalar=0):
    #Adds a row to the bottom of a matrix with a constant value equal to scalar
    #Example: append_uniform_row([[1,2,3],[4,5,6],[7,8,9]],0)   ====   [[1,2,3,0],[4,5,6,0],[7,8,9,0]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    matrix=np.asarray(matrix)#If this line cause errors, then it's up to the user of this function to figure out why.
    return np.row_stack((matrix,scalar*np.ones((1,matrix.shape[1]))))
def append_zeros_row(matrix):
    #Adds a row of zeros to the bottom of a matrix
    #Example: append_zeros_row([[1,2,3],[4,5,6],[7,8,9]])   ====   [[1,2,3,0],[4,5,6,0],[7,8,9,0]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    return append_uniform_row(matrix,0)
def append_ones_row(matrix):
    #Adds a row of ones to the bottom of a matrix
    #Example: append_zeros_row([[1,2,3],[4,5,6],[7,8,9]])   ====   [[1,2,3,1],[4,5,6,1],[7,8,9,1]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    return append_uniform_row(matrix,1)

def append_uniform_column(matrix,scalar=0):
    #Adds a column to the bottom of a matrix with a constant value equal to scalar
    #Example: append_uniform_column([[1,2,3],[4,5,6],[7,8,9]],0)   ====   [[1,2,3],[4,5,6],[7,8,9],[0,0,0]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    matrix=np.asarray(matrix)#If this line cause errors, then it's up to the user of this function to figure out why.
    return np.column_stack((matrix,scalar*np.ones((matrix.shape[0],1))))
def append_zeros_column(matrix):
    #Adds a column of zeros to the bottom of a matrix
    #Example: append_zeros_column([[1,2,3],[4,5,6],[7,8,9]])   ====   [[1,2,3],[4,5,6],[7,8,9],[0,0,0]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    return append_uniform_column(matrix,0)
def append_ones_column(matrix):
    #Adds a column of ones to the bottom of a matrix
    #Example: append_zeros_column([[1,2,3],[4,5,6],[7,8,9]])   ====   [[1,2,3],[4,5,6],[7,8,9],[1,1,1]]
    #Meant for use with numpy, and returns a numpy array.
    #Does NOT mutate matrix. It makes a copy.
    return append_uniform_column(matrix,1)
#endregion

#region some more math stuff
def squared_euclidean_distance(from_point,to_point):
    #This function exists so you don't have to use euclidean_distance then square it (which is both inefficient and can lead to floating point errors)
    #from_point and to_point are like (x0,y0,...) or [x0,y0,z0,...], or some numpy equivalent
    #Example:   euclidean_distance([0,0,0],[1,1,0]) ==== 2
    return np.sum(np.abs((np.asarray(to_point)-np.asarray(from_point)))**2)

def euclidean_distance(from_point,to_point):
    #from_point and to_point are like (x0,y0,...) or [x0,y0,z0,...], or some numpy equivalent
    #Example:   euclidean_distance([0,0,0],[1,1,0]) ==== sqrt(2)
    return squared_euclidean_distance(from_point,to_point)**.5

def cumulative_euclidean_distances(points,*,include_zero=False,loop=False):
    #If loop is true, as also add the distance from the last point to the first point at the end (one extra element in the output)
    #'points' represents a list of points
    #Returns an array of the cumulative distances from each point to each next point
    #Examples:
    #    cumulative_euclidean_distances([[0,1],[0,0],[1,0]],include_zero=False)  ->     [1. 2.]
    #    cumulative_euclidean_distances([[0,1],[0,0],[1,0]],include_zero= True)  ->  [0. 1. 2.]
    points=np.asarray(points)
    if loop:points=np.asarray([*points,points[0]])
    deltas=np.diff(points,axis=0)
    dists =np.sum(deltas**2,axis=1)**.5
    cumsum=np.cumsum(dists)
    return np.asarray([0,*cumsum]) if include_zero else cumsum

def evenly_split_path(path,number_of_pieces=100,*,loop=False):
    #Path is a list of points. Can be any number of dimensions.
    #The euclidean distance from each point to the next point in the output of this function is NOT guarenteed to be even by iteself; however it is guarenteed to be equidistant ALONG the path given to this function
    #Evenly splits the path into number_of_pieces pieces
    #PRO TIP: This function works with points of any dimension! (Not just 2d, as shown in the examples below)
    #Example:
        #CODE: evenly_split_path([[0,0],[0,1],[1,1],[1,0]],7,loop=False)
        #OUTPUT: [[0.  0. ]
        #         [0.  0.5]
        #         [0.  1. ]
        #         [0.5 1. ]
        #         [1.  1. ]
        #         [1.  0.5]
        #         [1.  0. ]]
    #Example:
        #CODE: evenly_split_path([[0,0],[0,1],[1,1],[1,0]],8,loop=True)
        #OUTPUT: [[0.  0. ]
        #         [0.  0.5]
        #         [0.  1. ]
        #         [0.5 1. ]
        #         [1.  1. ]
        #         [1.  0.5]
        #         [1.  0. ]
        #         [0.5 0. ]]
    #Tip: Also, try graphing these examples with scatter_plot(ans)
    path=np.asarray(path)
    path=as_points_array(path)
    cum_dists=cumulative_euclidean_distances(path,include_zero=True,loop=loop)
    total_dist=cum_dists[-1]
    out_dists=np.linspace(0,total_dist,num=number_of_pieces,endpoint=not loop)#The distances along the path where we ouput a point. They're evenly spaced along the path.
    path=path.T#Turns [(x,y),(x,y)...] into ([x,x,...],[y,y,...])
    out=[]
    for dimension in path:
        out.append(np.interp(x=out_dists,xp=cum_dists[:-1] if loop else cum_dists,fp=dimension,period=total_dist if loop else None))
    return np.transpose(out)

#region Conversions between path types
def is_complex_vector(x):
    #Return True iff x is like [1+2j,3+4j,5+6j,...]
    x=np.asarray(x)
    return len(x.shape)==1 and np.iscomplexobj(x)
def is_points_array(x):
    #Return True iff x is like [[1,2],[3,4],[5,6],...]
    x=np.asarray(x)
    return len(x.shape)==2 and x.shape[1]==2
def is_cv_contour(x):
    #Return True iff x is like [[[1,2]],[[3,4]],[[5,6]],...] and dtype=np.int32
    x=np.asarray(x)#TODO this might cast it to a type other than np.int32 if given a list...though it wouldn't be WRONG to say it's not a cv contour in this case...idk should I change this or leave it be?
    return len(x.shape)==3 and x.shape[1]==1 and x.shape[2]==2 and x.dtype==np.int32

#All the manual conversions (might be hidden later after we have automatic conversions) (the number of functions grows at (number of types)^2 )
def _points_array_to_complex_vector(points_array):
    #_points_array_to_complex_vector([[1,2],[3,4]])  ->  [1.+3.j 2.+4.j]
    points_array=np.asarray(points_array)
    assert is_points_array(points_array)
    return points_array[:,0]+1j*points_array[:,1]
def _points_array_to_cv_contour(points_array):
    points_array=np.asarray(points_array)
    assert is_points_array(points_array)
    return np.expand_dims(points_array,1).astype(np.int32)

def _complex_vector_to_points_array(complex_vector):
    #_complex_vector_to_points_array([1.+3.j ,2.+4.j])  ->  [[1. 3.],[2. 4.]]
    complex_vector=np.asarray(complex_vector)
    assert is_complex_vector(complex_vector)
    return np.transpose([complex_vector.real,complex_vector.imag])
def _complex_vector_to_cv_contour(complex_vector):
    complex_vector=np.asarray(complex_vector)
    assert is_complex_vector(complex_vector)
    return _points_array_to_cv_contour(_complex_vector_to_points_array(complex_vector))

def _cv_contour_to_points_array(cv_contour):
    assert is_cv_contour(cv_contour)
    return cv_contour.squeeze(1)
def _cv_contour_to_complex_vector(cv_contour):
    assert is_cv_contour(cv_contour)
    return _points_array_to_complex_vector(_cv_contour_to_points_array(cv_contour))

#Automatic path conversions (tries to detect the type of path then convert appropriately)
def as_complex_vector(path):
    #Automatically convert path path data
    if   is_complex_vector(path):return                        np.asarray(path.copy())
    elif is_points_array  (path):return   _points_array_to_complex_vector(path)
    elif is_cv_contour    (path):return     _cv_contour_to_complex_vector(path)
    else:assert False,'Cannot convert 2d path: path='+repr(path)
def as_points_array(path):
    #Automatically convert path data
    if   is_complex_vector(path):return _complex_vector_to_points_array(path)
    elif is_points_array  (path):return                      np.asarray(path.copy())
    elif is_cv_contour    (path):return     _cv_contour_to_points_array(path)
    else:assert False,'Cannot convert 2d path: path='+repr(path)
def as_cv_contour(path):
    #Automatically convert path data
    if   is_complex_vector(path):return _complex_vector_to_cv_contour(path)
    elif is_points_array  (path):return   _points_array_to_cv_contour(path)
    elif is_cv_contour    (path):return                    np.asarray(path.copy())
    else:assert False,'Cannot convert 2d path: path='+repr(path)
# EXAMPLES:
#       ⮤ as_complex_vector([[1,2],[3,4],[5,6]])
#      ans = [1.+2.j 3.+4.j 5.+6.j]
#       ⮤ as_cv_contour(ans)
#      ans = [[[1 2]]
#       [[3 4]]
#       [[5 6]]]
#       ⮤ as_complex_vector(ans)
#      ans = [1.+2.j 3.+4.j 5.+6.j]
#       ⮤ as_points_array(ans)
#      ans = [[1. 2.]
#       [3. 4.]
#       [5. 6.]]
#       ⮤ as_cv_contour(ans)
#      ans = [[[1 2]]
#       [[3 4]]
#       [[5 6]]]
#       ⮤ as_complex_vector(ans)
#      ans = [1.+2.j 3.+4.j 5.+6.j]
#       ⮤ as_points_array(ans)
#      ans = [[1. 2.]
#       [3. 4.]
#       [5. 6.]]



def contours_to_image(contours,*,scale=1,crop=True,**kwargs):
    #Returns a grayscale binary image of dtype bool
    #This function draws the given path onto a blank, black image scaled to fit the contour
    #By increasing 'scale' from 1 to some larger number, you increase the resolution of the output
    #TODO add flags for whether these contours are loops, for padding/margin etc, color/thickness of contours
    #Give this function contours and it will turn it into a black and white image
    #Hint: kwarg fill=True
    #You don't need to specify the size; that will be auto-calculated for you (which is why this function is so convenient)
    #EXAMPLE:
    #   tris=[randints_complex(randint(3,10))for _ in range(3)]#Three Triangles
    #   img=contours_to_image(tris)
    #   display_image(img)
    contours=[contour for contour in contours if len(contour)>1]#Gives errors otherwise
    if not contours:
        return np.asarray([[]],bool)#Return an empty image if we have no contours. This is to avoid errors later on.
    contours=list(map(as_points_array,contours))
    corner_point=lambda func:func([func(contour,0) for contour in contours],0)
    if crop:
        min_point=corner_point(np.min)
        contours=[contour-min_point for contour in contours]#If we use crop, we lose the original coordinates of the values of each contour point
    contours=[contour*scale     for contour in contours]
    max_point=corner_point(np.max)
    dims=np.floor(max_point+1).astype(int)
    dims=dims[::-1]#I'm not sure why but opencv seems to need this otherwise it gets the dimensions backwards
    contours=list(map(as_cv_contour,contours))
    image=np.zeros(dims)
    return cv_draw_contours(image,contours,**kwargs)>0

def contour_to_image(contour,**kwargs):
    #The singular form of contours_to_image (just give it one contour instead of a list of contours)
    return contours_to_image([contour],**kwargs)

#endregion
def squared_distance_matrix(from_points,to_points=None):
    #if to_points is None, it defaults to from_points (returning a symmetric matrix)
    #This function exists so you don't have to use distance_matrix then square it (which is both inefficient and can lead to floating point errors)
    #from_points and to_points are like [(x0,y0,...), (x1,y1,...), ...] or [(x0,y0,z0,...), (x1,y1,z1,...), ...], or some numpy equivalent
    #Returns a matrix M such that M[i,j] ==== euclidean_distance(from_points[i],to_points[j])**2
    #Example: squared_distance_matrix([[0,0],[10,10],[-10,-10]], [[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]]).shape   ====   (3,6)
    #Example: squared_distance_matrix([[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]], [[0,0],[10,10],[-10,-10]]).shape   ====   (6,3)
    if to_points is None:to_points=from_points
    if is_complex_vector(from_points) or is_cv_contour(from_points):from_points=as_points_array(from_points)
    if is_complex_vector(to_points  ) or is_cv_contour(to_points  ):to_points  =as_points_array(to_points  )
    from_points=np.expand_dims(np.asarray(from_points),1)
    to_points  =np.expand_dims(np.asarray(to_points  ),0)
    return np.sum((to_points-from_points)**2,2)#Use numpy's broadcasting rules to make this function fast and concise

def distance_matrix(from_points,to_points=None):
    #if to_points is None, it defaults to from_points (returning a symmetric matrix)
    #from_points and to_points are like [(x0,y0,...), (x1,y1,...), ...] or [(x0,y0,z0,...), (x1,y1,z1,...), ...], or some numpy equivalent
    #Returns a matrix M such that M[i,j] ==== euclidean_distance(from_points[i],to_points[j])
    #Example: distance_matrix([[0,0],[10,10],[-10,-10]], [[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]]).shape   ====   (3,6)
    #Example: distance_matrix([[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]], [[0,0],[10,10],[-10,-10]]).shape   ====   (6,3)
    return squared_distance_matrix(from_points,to_points)**.5

def closest_points(from_points,to_points=None,*,return_values=False):
    #if to_points is None, it defaults to from_points (returning a symmetric matrix)
    #This function was originally created to help implement the ICP algorithm (Iterative Closest Point algorithm), but has other uses as well
    #from_points and to_points are like [(x0,y0,...), (x1,y1,...), ...] or [(x0,y0,z0,...), (x1,y1,z1,...), ...], or some numpy equivalent
    #In the edge-case where two to_points are equidistant from some point in from_points, a single index will be selected arbitrarily by numpy.argmin
    #Outputs a list of indices referring to elements in to_points, with the same length as from_points.
    #NOTE there is an exception: if return_values is True, we return the actual points themselves instead of their indices in to_points
    #Takes a set of points from_points, and a set of to_points, and returns [index of closest point in to_points to P for P in from_points]
    #Example: closest_points([[0,0],[10,10],[-10,-10]], [[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]])   ====   [0 2 5]
    #Example: closest_points([[1,0],[0,1],[5,6],[4,5],[-1,-1],[-5,-6]], [[0,0],[10,10],[-10,-10]])   ====   [0 0 1 0 0 2]
    #return_values is False by defualt because there could be duplicate values, but there can never be duplicate indices. Therefore, returning indices gives more information.
    to_points  =np.asarray(to_points  )#If this or the next line cause errors, then it's up to the user of this function to figure out why.
    from_points=np.asarray(from_points)
    indices=np.argmin(distance_matrix(from_points,to_points),1)
    return to_points[indices] if return_values else indices

def least_squares_euclidean_affine(from_points,to_points,*,include_correlation=False):
    #TODO: Inspect this function! Is it right?!?!? It seems to follow
    #This function is strictly limited to two dimensions.
    #This function is like least_squares_affine, except skew is skipped. Only translation, rotation and scale are considered here.
    #This function is meant as an alternative to OpenCV's estimateRigidTransform function (with fullAffine=False), which I find frustrating to use (it sometimes returns None, and can only take certain numerical data types). Unlike OpenCV, this does NOT use ransac.
    #Returns an affine matrix with shape (2,3) that attempts to transform points in from_points to points to their respective point in to_points
    #from_points and to_points are like [(x0,y0), (x1,y1), ...] or [[x0,y0], [x1,y1],...], or some numpy equivalent
    #If include_extra is False, this function will just return the affine matrix. No fuss.
    #However, if include_extra is True, this function will return a tuple in the form (affine,correlation)
    #This function was written with the help of https://nghiaho.com/?p=2208 (or https://archive.is/UVROT or https://web.archive.org/web/20190611175717/https://nghiaho.com/?p=2208 if the link is broken)
    #Test Example:
    #  # CODE:
    #  #  from_points=np.array([[0,0],[1,0],[0 ,1],[-1,0] ,[0,-1]])      #A plus-shape
    #  #  to_points  =np.array([[0,0],[1.1,0.9],[-1.2,.9],[-.8,-1.1],[1,-1]])+[0,1]#An x-shape shifted up by 1 with a bit of noise
    #  #  affine=least_squares_euclidean_affine(from_points,to_points)
    #  #  ans=apply_affine(from_points,affine)
    #  #  print('affine=\n',affine)
    #  #  print('ans=\n',ans)
    #  #  print('to_points=\n',to_points)
    #  # OUTPUT:
    #  #  affine=
    #  #   [[ 0.95 -1.05  0.02]
    #  #   [ 1.05   0.95  0.94]]
    #  #  ans=
    #  #   [[ 0.02  0.94]
    #  #   [ 0.97   1.99]
    #  #   [-1.03   1.89]
    #  #   [-0.93  -0.11]
    #  #   [ 1.07  -0.01]]
    #  #  to_points=
    #  #   [[ 0.   1. ]
    #  #   [ 1.1   1.9]
    #  #   [-1.2   1.9]
    #  #   [-0.8  -0.1]
    #  #   [ 1.    0. ]]
    #  # ANALYSIS:
    #  #   You can see that to_points is close to ans, which means it worked pretty well.

    #TODO Clean this up. Here's the newer implementation which runs faster than the old one:
    from_points=as_complex_vector(from_points)
    to_points=as_complex_vector(to_points)
    m,b,r=least_squares_regression_line_coeffs(as_complex_vector(from_points),as_complex_vector(to_points),include_correlation=True)
    affine=complex_linear_coeffs_to_euclidean_affine(m,b)
    if include_correlation:
        return affine,r
    return affine
        #Comparison of the new vs old methods:
    #   ⮤ y=randints_complex(10000)
    #   2 x=randints_complex(10000)
    #   3 m=6-4j
    #   4 b=3+7j
    #   5 y=m*x+b
    #   6 tic();[least_squares_regression_line_coeffs(x,y)for _ in range(10000)];ptoc()
    #   7 xp=as_points_array(x)
    #   8 yp=as_points_array(y)
    #   9 tic();[least_squares_euclidean_affine(xp,yp)for _ in range(10000)];ptoc()
    #  2.905686140060425 seconds
    #  19.899923086166382 seconds  <--- Using the old implementation, it's about 2 times slower

    if False:#The old method whose code works but is complicated by comparison
        to_points  =np.asarray(to_points  )#If this or the next line cause errors, then it's up to the user of this function to figure out why.
        from_points=np.asarray(from_points)
        assert from_points.shape[1]==to_points.shape[1]==2,'All points must be two dimensional. from_points and to_points should both have shapes like (N,2), where N is any integer >=2. from_points.shape=='+str(from_points.shape)+' and to_points.shape=='+str(to_points.shape)
        assert len(from_points>=2) and len(to_points>=2),'To fit a euclidean 2d transform (including only translation, rotation and scale), we must have at least two points. However, len(from_points)='+str(len(from_points))+' and len(to_points)='+str(len(to_points))
        assert len(from_points   ) ==  len(to_points   ),'You must have the same number of points in both from_points and to_points, or else it doesnt make sense to say theres a 1-to-1 correspondence between the to_points and from_points. len(from_points)='+str(len(from_points))+' and len(to_points)='+str(len(to_points))
        A=np.insert(from_points,slice(None),from_points,0)#[x1  y1;x1 y1;x2  y2;x2 y2;...]  (Note: A is commonly seen in AX=B when describing least-squares fit using matrices)
        A[1::2]=A[1::2,::-1]                              #[x1  y1;y1 x1;x2  y2;y2 x2;...]
        A[::2]*=[1,-1]                                    #[x1 -y1;y1 x1;x2 -y2;y2 x2;...]
        Z=np.zeros(A.shape)                               #[ 0   0; 0  0; 0   0; 0  0;...]  (Note: Z stands for Zeros)
        Z[::2,0]=Z[1::2,1]=1                              #[ 1   0; 0  1; 1   0; 0  1;...]
        A=np.column_stack((A,Z))                          #[x1 -y1  1  0;y1  x1  0  1;x2 -y2 1 0;y2 x2 0 1;...]
        B=np.reshape(to_points,-1)                        #[x0  y0 x1 y1...] (Where x0 and y0 etc refer to to_points as opposed to from_points, like x0,y0 etc do above this line)
        # exec(mini_terminal)
        X,(error,),_,residuals=np.linalg.lstsq(A,B,rcond=None)#Solving least-squares for X given AX=B where A is a square matrix, and X and B are vectors. The variable named '_' is useless; I don't understand why numpy included it. It just returns the length of the result, which we allready know. rcond=None exists to make numpy shut up (it gives future warnings blah blah....all completely harmless but annoying)
        a,b,c,d=X                                         #Individual numbers that make up the affine matrix. Same variables used on the website's tutorial (URL posted above)
        affine=np.asarray([[a,-b,c],[b,a,d]])
        if not include_extra:
            return affine
        class result:pass
        result.affine   =affine
        result.error    =error
        result.residuals=residuals
        return result

def least_squares_affine(from_points,to_points,*,include_extra=False):
    #TODO Clean this function up and make it more like least_squares_euclidean_affine
    #from_points and to_points are like [(x0,y0), (x1,y1), ...] or [[x0,y0], [x1,y1],...], or some numpy equivalent
    #If include_extra is False, this function will just return the affine matrix. No fuss.
    #However, if include_extra is True, this function will return a class (with static values) in this form: {'affine':‹the affine matrix (a 2x3 matrix)›, 'error':‹total error (a number)›, 'residuals':‹individual errors for every point (a list of numbers)›) (Access it with result.affine, result.error, result.residuals, etc.)
    to_points  =np.asarray(to_points  )#If this or the next line cause errors, then it's up to the user of this function to figure out why.
    from_points=np.asarray(from_points)
    assert from_points.shape[1]==to_points.shape[1]==2,'All points must be two dimensional. from_points and to_points should both have shapes like (N,2), where N is any integer >=2. from_points.shape=='+str(from_points.shape)+' and to_points.shape=='+str(to_points.shape)
    assert len(from_points>=2) and len(to_points>=2),'To fit a euclidean 2d transform (including only translation, rotation and scale), we must have at least two points. However, len(from_points)='+str(len(from_points))+' and len(to_points)='+str(len(to_points))
    assert len(from_points   ) ==  len(to_points   ),'You must have the same number of points in both from_points and to_points, or else it doesnt make sense to say theres a 1-to-1 correspondence between the to_points and from_points. len(from_points)='+str(len(from_points))+' and len(to_points)='+str(len(to_points))
    from_points_1=append_ones_column(from_points)
    for_to_x=np.insert(np.zeros_like(from_points_1),slice(None),from_points_1,0)
    for_to_y=np.insert(from_points_1,slice(None),np.zeros_like(from_points_1),0)
    A=np.column_stack((for_to_x,for_to_y))
    piA=np.linalg.pinv(A)#Pseudo-inverse of A
    b=np.reshape(to_points,-1)
    out_a,out_b,out_c,out_d,out_e,out_f=np.matmul(piA,b)
    affine=[[out_a,out_b,out_c],[out_d,out_e,out_f]]
    if not include_extra:
        return affine
    class result:pass
    result.affine   =affine
    result.error    ='TODO'
    result.residuals='TODO'
    return result

def translation_affine(vector):
    # EXAMPLE:
    #   CODE:
    #     translation_affine([20,30])
    #   RESULT:
    #     [[ 1.  0. 20.]
    #      [ 0.  1. 30.]]
    return np.column_stack((np.eye(len(vector)),vector))

def rotation_affine_2d(angle,pivot=[0,0],*,out_of=tau):
    #EXAMPLE:
    #  CODE:
    #    rotation_affine_2d(90,out_of=360)
    #  RESULT:
    #    [[ 0. -1.  0.]
    #     [ 1.  0.  0.]]
    #EXAMPLE:
    #  CODE:
    #    print(apply_affine([[0 ,0]],rotation_affine_2d(180,pivot=[1,1],out_of=360)))
    #    print(apply_affine([[-1,1]],rotation_affine_2d(180,pivot=[1,1],out_of=360)))
    #    print(apply_affine([[-1,1]],rotation_affine_2d(180,pivot=[0,0],out_of=360)))
    #  RESULT:
    #    [[ 2.  2.]]
    #    [[ 3.  1.]]
    #    [[ 1. -1.]]
    #  ANALYSIS:
    #    Note how (in the second two lines) the change from pivot [1,1] to [0,0] changed the result
    pivot   =np.asarray(pivot)
    shift   =translation_affine(-pivot)                                   #Shift pivot to origin
    rotation=np.column_stack((rotation_matrix(angle,out_of=out_of),[0,0]))#Rotate about the origin
    unshift =translation_affine(pivot)                                    #Put the pivot back again
    return combined_affine(shift,rotation,unshift)

def inverse_affine(affine):
    #QUICK AND DIRTY EXAMPLE:
        #  ⮤ A
        # ans = [[11. 62. 90.]
        #  [29.  9. 98.]]
        #  ⮤ apply_affine([[2,4],[5,6],[7,8]],A)
        # ans = [[360. 192.]
        #  [517. 297.]
        #  [663. 373.]]
        #  ⮤ apply_affine(ans,affine_inverse(A))
        # ans = [[2. 4.]
        #  [5. 6.]
        #  [7. 8.]]
    affine=append_zeros_row(affine)
    affine[-1][-1]=1
    return np.linalg.inv(affine)[:2]

def identity_affine(ndim=2):
    # EXAMPLE:
    #   CODE:
    #     identity_affine(2)
    #   RESULT:
    #     [[1. 0. 0.]
    #      [0. 1. 0.]]
    # EXAMPLE:
    #   CODE:
    #     identity_affine(3)
    #   RESULT:
    #     [[1. 0. 0. 0.]
    #      [0. 1. 0. 0.]
    #      [0. 0. 1. 0.]]
    return append_zeros_column(np.eye(ndim))

def combined_affine(*affines):
    #Return the affine matrix needed to apply all matrices in 'affines' in the order they were given
    #TODO: Add more input assertions, such as all affines must have same shape, etc
    #apply_affine(points,combined_affine(affine_1,affine_2))  is the same as  apply_affine(apply_affine(points,affine_1),affine_2)
    #PROPERTIES:
    #  Associative:  C(a,C(b,c)) ==== C(C(a,b),c) ==== C(a,b,c)  where C is combined_affine
    #EXAMPLE:
    #  CODE:
    #     af1=[[5, 3, 8], [8, 3, 6]]
    #     af2=[[8, 3, 3], [1, 5, 3]]
    #     p  =[[3, 6], [8, 4], [9,2]]
    #     print(apply_affine(apply_affine(p,af1),af2))
    #     print(apply_affine(p,combined_affine(af1,af2)))
    #  OUTPUT:
    #    [[475. 284.]
    #     [729. 473.]
    #     [727. 482.]]
    #    [[475. 284.]
    #     [729. 473.]
    #     [727. 482.]]
    #  ANALYSIS:
    #    Note that the two outputs are exactly equivalent.
    assert affines,'combined_affine must take in at least one affine or else it has no idea what matrix shape to return'
    affines=tuple(map(np.asarray,affines))#If this breaks, its up to the user of this function to fix any errors
    shape=affines[0].shape
    out=np.eye(shape[1])
    for affine in affines:
        affine=np.asarray(affine)
        assert affine.shape[1]==affine.shape[0]+1,'m doesnt have the dimensions of an affine matrix'
        affine=append_zeros_row(affine)
        affine[-1,-1]=1
        out=np.matmul(affine,out)
    return out[:2]

def apply_affine(points,affine):#,*,copy=True):
    #This function applies a given affine transform (specified as a matrix) to a list of points and returns the list of resulting points
    #This function generalizes to affines of all dimensions (not just 2d)
    #'points' is like [(x0,y0), (x1,y1), ...] or [[x0,y0], [x1,y1],...], or some numpy equivalent
    #affine is a 2x3 (for 2d) or 3x4 (for 3d) or 4x5 (for 4d) or (etc) affine-transform matrix.
    #EXAMPLE: For examples, see the documentation for least_squares_euclidean_affine (it's a function in r.py, which can be obtained in a pypi package called 'rp')
    affine=np.asarray(affine)#If this or the next line cause errors, then it's up to the user of this function to figure out why.
    points=np.asarray(points)
    assert len(points.shape)==2,'Points should be a matrix, but points.shape=='+str(points.shape)
    assert len(affine.shape)==2,'Affine should be a matrix, but affine.shape=='+str(affine.shape)
    npoint=points.shape[0]#npoint stands for 'number of points'
    ndim  =points.shape[1]#ndim stands for 'number of dimensions'. This function should generalize to n-dimensional space, not just 2d or 3d etc.
    assert affine.shape==(ndim,ndim+1),'An affine transform matrix for '+str(ndim)+'-dimensional points should have shape '+str((ndim,ndim+1))+', but instead affine.shape=='+str(affine.shape)
    return (affine@append_ones_row(points.T)).T#The '@' character is a matrix multiplication operator in numpy

def icp_least_squares_euclidean_affine(from_points,to_points,max_iter=5,*,include_extra=False):
    #icp stands for "iterative closest point". It's an algorithm used to match point-clouds.
    #The length of from_points and to_points does NOT have to match. However, they must both have at least two points each (otherwise it's impossible to determine a euclidean transform between them).
    #In this function we're matching point clouds, but in specifically two dimensions, and allowing only translation, rotation and scale
    #from_points and to_points are like [(x0,y0,...), (x1,y1,...), ...] or [(x0,y0,z0,...), (x1,y1,z1,...), ...], or some numpy equivalent
    #Returns a 2x3 affine transform matrix
    #TEST CODE:
    #   a=random_element(contours).squeeze()
    #   b=random_element(contours).squeeze()
    #   scatter_plot([])
    #   scatter_plot(b,clear=False)
    #   scatter_plot(a,clear=False)
    #   for _ in range(5):
    #       result=icp_least_squares_euclidean_affine(a,b,include_extra=True,max_iter=_+1)
    #       scatter_plot(result.points,clear=False)
    #END TEST CODE
    from_points=np.asarray(from_points)#If this or the next line cause errors, then it's up to the user of this function to figure out why.
    to_points=np.asarray(to_points)
    # from_points=from_points+(np.mean(to_points,0)-np.mean(from_points,0))
    def point_cloud_angle(points):
        x,y=zip(*points)
        #x and y are lists of x and y values for a point cloud
        #return an angle describing the point cloud's rotation, calculated via looking at the most stretched-out part of the covariance matrix
        #Note: When testing contours, must try both this and this flipped by 180 degrees
        points=np.matrix([x,y])
        cov=np.cov(points)
        eig_vals,eig_vecs=np.linalg.eig(cov)
        index=max_valued_index(eig_vals)#index of the larger eigenvector/value
        vec=eig_vecs[:,index]
        vec_x,vec_y=vec
        angle=np.arctan(vec_y/vec_x)
        angle%=pi
        return angle


    #Calculate initial guess:
    output_affine=combined_affine(translation_affine(-from_points.mean(0)),
                                  rotation_affine_2d(point_cloud_angle(to_points)-point_cloud_angle(from_points)),
                                  translation_affine(to_points.mean(0))
                                 )#output_affine will be modified as this ICP algorithm iterates. This is just our initial guess.
    fit_points=apply_affine(from_points,output_affine)

    assert max_iter>=0,'Cannot have a negative number of iterations!'
    if not max_iter:
        assert not include_extra,'include_extra is not (currently) supported when there are no iterations'#This can be implemented in the future if it's important
        return output_affine#is currently the identity affine
    for _ in range(max_iter):
        # exec(mini_terminal)
        matched_points=closest_points(fit_points,to_points,return_values=True)
        # print("==========================================",
            # fit_points,
            # "+++++++++++++++++"
            # ,to_points,matched_points)
        number_of_unique_matched_points=len(np.unique(matched_points,axis=0))
        fit_result   =least_squares_euclidean_affine(fit_points,matched_points,include_extra=True)
        fit_affine   =fit_result.affine
        fit_error    =fit_result.error
        fit_residuals=fit_result.residuals
        fit_scale_factor=np.sum(fit_affine[:,0]**2)**.5#The total difference in scale caused by fit_affine
        #TODO: This is NOT clean. fit_error, for example, will give the wrong result if number_of_unique_matched_points starts/ends as 1.
        if number_of_unique_matched_points<=1:
            #This is a degerate edge case (picture matching two circles that don't overlap, and so all points on one circle get matched to exactly one point on the other circle)
            #In the event that all points get matched to the same place, only allow translation.
            #Don't allow scale or rotation, because it will collapse to a single point - even though we know at least two points exist in both from_points and to_points.
            #**I'm not sure, but this might be why implementations I've found online keep failing.
            # fit_affine[:,:2]=np.eye(2)#This is a degenerate case where all points are matched to the same place, and the scale gets reduced to 0. If this happens, undo this change, and force neither the scale nor rotation to change. Translation is left untouched.
            delta_x,delta_y=np.mean(matched_points,0)-np.mean(fit_points,0)
            fit_affine=np.asarray([[1,0,delta_x],[0,1,delta_y]])
            # print("FIT AFFINE:\n",fit_affine,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # print(fit_affine,matched_points,to_points)
            #MY HACK: Randomly select one point from both to_points and fit_points and align them via just translation.
            # random_from_point=random_element(from_points)
            # random_to_point=random_element(to_points)
            # fit_points=from_points+random_to_point-random_from_point
        else:
            #We're OK, we've matched MORE than one point...
            pass#(This is intentionally an empty statement so i can explicitly say what it means to be here in the above comment)
        output_affine=combined_affine(output_affine,fit_affine)
        fit_points=apply_affine(from_points,output_affine)
        # exec(mini_terminal)
    if not include_extra:
        return fit_affine
    class result:
        affine   =output_affine
        error    =fit_error
        residuals=fit_residuals
        points   =fit_points
    return result

def is_euclidean_affine(affine):
    affine=np.asarray(affine)
    if not is_affine_matrix(affine):
        return False
    return affine[0][0]==affine[1,1] and affine[1][0]==-affine[0][1]
def is_affine_matrix(affine):
    affine=np.asarray(affine)
    return affine.shape==(2,3)
def euclidean_affine_to_complex_linear_coeffs(affine):
    #mx+b in the complex plane corresponds to a euclidean transform
    #This function takes a euclidean affine and returns it's complex m, b coeffs (from the y=mx+b convention)
    #Example:
    #Given affine matrix [[a  b  c]
    #                     [d  e  f]]
    #We can assert that a=e and d=-b because it's euclidean and rewrite it as
    #                    [[a -d  c]
    #                     [d  a  f]]
    #Which corresponds to a transform represented by transforming complex number x:
    #   x' = mx+b = (a+di)x+(c+fi)
    #And therefore m=a+di and b=c+fi
    assert is_euclidean_affine(affine),'The given affine is not a euclidean transform. affine=='+repr(affine)
    m=affine[0][0]+affine[1][0]*1j #Corresponds to rotation and scale
    b=affine[0][2]+affine[1][2]*1j #Corresponds to tranlation
    return m,b
def complex_linear_coeffs_to_euclidean_affine(m,b):
    #This is the inverse of euclidean_affine_to_complex_linear_coeffs
    #Where F=complex_linear_coeffs_to_euclidean_affine and G=euclidean_affine_to_complex_linear_coeffs,
    #F(*G(X))  ==== X for all euclidean affines X and
    #G(F(m,b)) ==== m,b for all complex numbers m,b
    #Please see euclidean_affine_to_complex_linear_coeffs's documentation for an explanation of what this function does
    return np.asarray([[m.real,-m.imag,b.real],[m.imag,m.real,b.imag]])




#region Hashing functions

class HandyHashable:
    #A wrapper for any data that makes it hashable
    def __init__(self,value):
        self.value=value
        self._hash=handy_hash(value)
    def __hash__(self):
        return self._hash
    def __eq__(self,x):
        if not isinstance(x,HandyHashable):
            return False
        try:
            return self.value==x.value
        except ValueError:#ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
            handy_hash(self.value)==handy_hash(x.value)
    def __repr__(self):
        return "HandyHashable("+repr(self.value)+")"

class HandyDict(dict):
    #A dict that can use more than just normal keys by using handyhash
    #This class might get more methods over time.
    def __init__(self,*args,**kwargs):
        return dict.__init__(self,*args,**kwargs)
    def __setitem__(self, key, value):
        return dict.__setitem__(self,HandyHashable(key),value)
    def __delitem__(self, key):
        return dict.__delitem__(self,HandyHashable(key))
    def __getitem__(self, key):
        return dict.__getitem__(self,HandyHashable(key))
    def __iter__(self):
        return (key.value for key in dict.__iter__(self))
    def __contains__(self,x):
        return dict.__contains__(self,HandyHashable(x))

#TODO: HandySet

def handy_hash(value,fallback=None):
    #This function is really handy!
    #Meant for hashing things that can't normally be hashed, like lists and dicts and numpy arrays. It pretends they're immutable.
    #This function can hash all sorts of values. Anything mutable should be frozen, we're not just returning an ID.
    #For example, lists are turned into tuples, and dicts like {"A":"B","C":"D"} are turned into ((""))
    #If it can't hash something, it will just use fallback to hash it. By default, though, fallback is
    def default_fallback(value):
        fansi_print('Warning: fallback_hash was called on value where repr(value)=='+repr(value),'yellow')
        return id(value)
    fallback=fallback or default_fallback
    value_type=type(value)
    try:return hash(value)
    except:pass#This is probably going to happen a lot in this function lol (that's kinda the whole point)
    hasher=__hashers[value_type] if value_type in __hashers else fallback
    return hasher(value)

#region Type-specific hashers
__secret_number=71852436691752251090#Used for hashing things. Don't use this value anywhere! It's not generated dynamically (aka it doesnt use randint) because we want consistent hash values across python processes.
__hashers={}#Used by handy_hash

try:#Attempt to add numpy arrays to the hashers used by handy_hash
    import numpy as np
    def _numpy_hash(x):
        assert isinstance(x,np.ndarray)
        return hash((__secret_number,'_numpy_hash',x.tobytes()))#Strings such as '_numpy_hash' are put in here to distinguish this function's output from some other hasher which, by some strange coincidence, generate a (__secret_number,‹same bytestring›) but isnt a numpy array. This same technique is also used in the other hasher functions near this one.
    __hashers[np.ndarray]=_numpy_hash
except ImportError:pass
except BaseException as e:
    try:
        fansi_print('Upon booting rp, failed to import numpy. Stack trace shown below:','red','bold')
        print_stack_trace(e)
    except:
        pass#Don't prevent rp from booting no matter what

def _set_hash(x):
    assert isinstance(x,set)
    return hash((__secret_number,frozenset(x)))
__hashers[set]=_set_hash

def _dict_hash(x,value_hasher=handy_hash):
    assert isinstance(x,dict)
    set_to_hash=set()
    for key,value in x.items():
        set_to_hash.add(hash((__secret_number,'dict_hash_pair',key,value_hasher(value))))
    return hash((__secret_number,frozenset(set_to_hash)))
__hashers[dict]=_dict_hash

def _list_hash(x,value_hasher=handy_hash):
    assert isinstance(x,list)
    return hash((__secret_number,'_list_hash',tuple(map(value_hasher,x))))
__hashers[list]=_list_hash

def _tuple_hash(x,value_hasher=handy_hash):
    assert isinstance(x,tuple)
    return hash((__secret_number,'_tuple_hash',tuple(map(value_hasher,x))))
__hashers[tuple]=_tuple_hash

def _slice_hash(x,value_hasher=handy_hash):
    assert isinstance(x,slice)
    return hash((__secret_number,'_slice_hash',(value_hasher(x.start),value_hasher(x.step),value_hasher(x.stop))))
__hashers[slice]=_slice_hash

#endregion


def args_hash(function,*args,**kwargs):
    #Return the hashed input that would be passed to 'function', using handy_hash. This function is used for memoizers. function must be provided for context so that arguments passed that can be passed as either kwargs or args both return the same hash.
    assert callable(function),'Cant hash the inputs of function because function isnt callable and therefore doesnt receive arguments. repr(function)=='+repr(function)
    args=list(args)
    try:
        #Whenever we can, we take things from args and put them in kwargs instead...
        from inspect import getfullargspec
        arg_names=list(getfullargspec(function).args)#This often doesn't work, particularly for built-in functions. TODO this is possible to fix, given that rp can complete argument names of even opencv functions. But for the most part, memoization is used in loops where the function is called with the same signature over and over again, so I'm going to push off improving this till later.
    except:
        #...but it's not a necessity, I GUESS...(if the function is always called the same way)
        arg_names=[]
        pass
    while arg_names and args:
        #Take things from args and put them in kwargs instead, for as many args as we know the names of...
        kwargs[arg_names.pop(0)]=args.pop(0)
    hashes=set()
    for index,arg in enumerate(args):
        hashes.add(hash(('arg',index,handy_hash(arg))))
    for kw   ,arg in kwargs.items() :
        hashes.add(hash(('kwarg',kw ,handy_hash(arg))))
    return hash(frozenset(hashes))


def memoized(function):
    #TODO: when trying to @memoize fibbonacci, and calling fibbonacci(4000), python crashes with SIGABRT. I have no idea why. This function really doesn't use any non-vanilla python code.
    #Uses args_hash to hash function inputs...
    #This is meant to be a permanent cache (as opposed to a LRU aka 'Least Recently Used' cache, which deletes cached values if they haven't been used in a while)
    #If you wish to temporarily memoize a function (let's call if F), you can create a new function cached(F), and put it in a scope that will run out eventually so that there are no memory leaks.
    #Some things can't be hashed by default, I.E. lists etc. But all lists can be converted to tuples, which CAN be hashed. This is where hashers come in. Hashers are meant to help you memoize functions that might have non-hashable arguments, such as numpy arrays.
    cache=dict()
    assert callable(function),'You can\'t memoize something that isn\'t a function (you tried to memoize '+repr(function)+', which isn\'t callable)'
    def output(*args,**kwargs):
        key=args_hash(function,*args,**kwargs)
        if not key in cache:
            cache[key]=function(*args,**kwargs)
        return cache[key]
    return output

#endregion

def strip_file_extension(file_path):
    #'x.png'        --> 'x'
    #'text.txt'     --> 'text'
    #'text'         --> 'text'
    #'text.jpg.txt' --> 'text.jpg'
    #'a/b/c.png'    --> 'a/b/c'
    #'a/b/c'        --> 'a/b/c'
    # For more, see: https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
    return os.path.splitext(file_path)[0]

def get_file_extension(file_path):
    #'x.png'        --> 'png'
    #'text.txt'     --> 'txt'
    #'text'         --> ''
    #'text.jpg.txt' --> 'txt'
    #'a/b/c.png'    --> 'png'
    #'a/b/c'        --> ''
    # For more, see: https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    return os.path.splitext(file_path)[1].rpartition('.')[2]

def get_path_name(path,include_file_extension=True):
    #'/tmp/d/a.dat' --> 'a.dat'
    # For more, see: https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    from pathlib import Path
    output= Path(path).name
    if not include_file_extension:
        output=strip_file_extension(output)
    return output
get_folder_name=get_directory_name=get_file_name=get_path_name

def get_relative_path(path,parent_directory=None):
    #Take an absolute path, and turn it into a relative path starting from parent_directory
    #parent_directory's default is get_current_directory()
    if parent_directory is None:
        parent_directory=get_current_directory()
    assert isinstance(parent_directory,str),'parent_directory must be a string representing the root path to compare the given path against'
    return os.path.relpath(path,parent_directory)

def get_absolute_path(path):
    #Given a relative path, return its absolute path
    return os.path.abspath(path)

def has_file_extension(file_path):
    return get_file_extension(file_path)!=''

def date_modified(path):
    #Get the date a path was modified
    timestamp=os.path.getmtime(path)#Measured in seconds
    import datetime
    return datetime.datetime.fromtimestamp(timestamp)
def date_created(path):
    #Get the date a path was created
    timestamp=os.path.getctime(path)#Measured in seconds
    import datetime
    return datetime.datetime.fromtimestamp(timestamp)
def date_accessed(path):
    #Get the date a path was accessed
    timestamp=os.path.getatime(path)#Measured in seconds
    import datetime
    return datetime.datetime.fromtimestamp(timestamp)
    
def get_file_paths(*directory_path                  ,
                    sort_by                 = None  ,
                    file_extension_filter   = None  ,
                    recursive               = False ,
                    include_files           = True  ,
                    include_folders         = False ,
                    just_file_names         = False ,
                    include_file_extensions = True  ,
                    relative                = False
                    ):
    #Returns global paths.
    #If relative is False, we return global paths. Otherwise, we return relative paths to the current working directory 
    #If relative is a string, we return paths relative to that string (otherwise if it's just True, we default to directory_path)
    #TODO: Make sure this function isn't redundant before committing to keeping it forever!
    #TODO: In particular, make sure this isn't redundant with respect to get_all_file_names, or else merge them together.
    #TODO: Add a recursive option, filters, etc.
    #NOTE: Sort by number is SUPER useful when you have files like [frame0,frame1,frame2...frame10,frame11,frame12...] because if you sort them alphabetically you get [frame1,frame10,frame11,...frame2,frame20,frame21...] BUT ...
    # ... when you sort_by='number', it will order them correctly even without digit padding because names with shorter lengths will come first. This means ['frame1','frame2',...frame10,frame11,...]
    #directory_path can be composed of multiple paths (specified in varargs); this function will join them for you.
    #If include_global_path is true, we return the whole global file path of all files in the directory (as opposed to just returning their names)
    #If file_extension_filter is not None and file_types is a space-separated string, only accept those file extensions
    #sort_by can be None, or it can be a string
    #EXAMPLES:
    #
    #    ⮤ get_file_paths('Tests/First','Inputs',sort_by='name')
    #    ans = ['Tests/First/Inputs/01.png',
    #           'Tests/First/Inputs/02.jpg',
    #           'Tests/First/Inputs/03.gif',
    #           'Tests/First/Inputs/04.bmp']
    #
    #    ⮤ get_file_paths('Tests/First','Inputs')                 #Without sort_by specified, the output could potentially be shuffled
    #    ans = ['Tests/First/Inputs/02.jpg',
    #           'Tests/First/Inputs/04.bmp',
    #           'Tests/First/Inputs/03.gif',
    #           'Tests/First/Inputs/01.png']
    #
    #    ⮤ get_file_paths('Tests/First','Inputs',sort_by='name',just_file_names=True)
    #    ans =  ['01.png', '02.jpg', '03.gif', '04.bmp']
    #
    #    ⮤ get_file_paths('Tests/First','Inputs',sort_by='name',just_file_names=True,include_file_extension=False)
    #    ans =  ['01', '02', '03', '04']
    #
    #    ⮤ get_file_paths('Tests/First','Inputs',sort_by='name',just_file_names=True,include_file_extension=False,file_extension_filter='bmp png')  #Filtering the extension type to just .bmp and .png images
    #    ans =  ['01', '04']
    #

    if sort_by is not None:
        sort_by=sort_by.lower()#Don't be case-sensitive. That's annoying. Reassign it here so we dont need to make it nonlocal.

    if directory_path==():#If the user didn't specify a path...
        directory_path=get_current_directory()#...default to the current directory
    else:
        directory_path=os.path.join(*directory_path)#Turn ('Ryan','Documents','Images') into 'Ryan/Documents/Images'

    def recursion_helper(directory_path):
        assert isinstance(directory_path,str),'This is an internal assertion that should never fail. If this assertion does fail, get_file_paths has a bug.'
        assert directory_exists(directory_path),'get_file_paths error: '+repr(directory_path)+' is not a directory'

        all_paths=[os.path.join(directory_path,name) for name in os.listdir(directory_path)]
        subdirectory_paths=list(filter(directory_exists,all_paths))
        file_paths        =list(filter(file_exists     ,all_paths))
        #OLD VERSION: file_paths=[os.path.join(directory_path,file_name) for file_name in next(os.walk(directory_path))[2]]#next(os.walk(...)) returns something like (‹directory_path›, [], ['0.png','1.png',...])

        output=[]
        if include_files  :output+=file_paths
        if include_folders:output+=subdirectory_paths

        if recursive:
            for subdirectory_path in subdirectory_paths:
                output+=recursion_helper(subdirectory_path)

        if sort_by is not None:
            #If sort_by is None, don't bother trying to sort the file paths (they could appear in some random order. Setting sort_by to None implies this doesn't matter. Technically it's a bit faster, too (but likely not by much))
            assert type(sort_by)==str,'sort_by should either be None or be a string, but instead repr(type(sort_by))=='+repr(type(sort_by))
            sort_by_options={
                #sort_by_options's are Functions that take a file path and return values that we can sort file paths by
                'name':identity,
                'size':os.path.getsize,
                'date':date_modified,#By default, date refers to the date last modified. This might change. 'date' is an option here as syntactic sugar!
                'date modified':date_modified,
                'date created' :date_created ,
                'date accessed':date_accessed,
                'number':lambda x:(len(x),x)
            }
            assert sort_by in sort_by_options,'get_file_paths: sort_by specifies how to sort the files. Please set sort_by to one of the following strings: '+', '.join(map(repr,sorted(sort_by_options)))+'. (You chose repr(sort_by)=='+repr(sort_by)+' with repr(type(sort_by))=='+repr(type(sort_by))
            output.sort(key=sort_by_options[sort_by])

        if file_extension_filter is not None:
            #'x.png' --> 'x', 'text.txt' --> 'txt', etc. (See strip_file_extension for more details)
            assert type(file_extension_filter)==str,'get_file_paths: For file_extension_filter, right now only space-split whitelists are supported, such as "png jpg bmp gif"'
            file_extension_whitelist=file_extension_filter.split()
            output=[path for path in output if get_file_extension(path) in file_extension_whitelist]

        if just_file_names:
            #Extract the file names from each file path (these could have been sorted, which is why we aren't re-using the file names we got when we originally calculated file_paths)
            #Example: if not include_file_extensions, then 'Documents/Textures/texture.png'  --->  'texture.png' (see get_path_file_name for more details)
            output=list(map(get_path_file_name,output))

        if not include_file_extensions:
            #'x.png' --> 'x', 'text.txt' --> 'txt', etc. (See strip_file_extension for more details)
            output=list(map(strip_file_extension,output))

        return output

    output=recursion_helper(directory_path)

    if relative:
        #Return relative paths instead of absolute paths
        relative_to=relative if isinstance(relative,str) else directory_path
        output=[get_relative_path(path,relative_to) for path in output]

    return output
get_all_paths=get_file_paths

#endregion

def fractional_integral_in_frequency_domain(coefficients,n=1):
    #WARNING: Make sure to use the right kind of fft (np.fft.rfft vs np.fft.fft)
    #This function integrates or differentiates signals using just their fourier coefficients, and returns a new set coefficients
    #n is the number of times we integrate this function. n can be negative, which would imply a derivative. The 0'th coefficient (the average value of the respective time domain) is preserved with this function; even when taking the derivative. This is because of a division by zero error that would occur otherwise and must therefore be handled somehow.
    #Some properties:
    #  Let f=fractional_integral_in_frequency_domain
    #  For all c: f(c,0) = c
    #  For all n, m and c: f(f(c,n),m) = f(c,n+m)
    coefficients=np.asarray(coefficients,np.complex128)
    assert is_complex_vector(coefficients),'coefficients should be a complex vector'
    coefficients[1:]*=(1j/np.arange(len(coefficients))[1:])**n
    return coefficients


class FlannDict:
    #TODO: Finish bundling PyFlann's binaries into rp.
    #FLANN is an algorithm that calculates the (approximate) nearest neigbours of a point very, very quickly. Originally called nearest_neighbor_dict, but this is ambiguous in the case that we wish to use other algorithms.
    #in addition to real keys, FlannDict supports complex keys of any numpy shape. But, just try to be consistent else it will throw errors (by design).
    #This is abstraction above FLANN that lets you use nearest neighbor search with the interface of a dictionary; automatically rebuilding the index as needed (for a huge performance boost).
    #This interface can be replaced by a brute force search...but why do that?
    #FlannDict caches any queries you make, so if you query the same point twice it will just reuse those calculations. This cache is automatically reset upon rebuilding the FLANN tree.
    #Uses nearest-neighbor to match keys. Currently uses FLANN.
    #Use splicing to get k nearest neighbours like this: d[point:k] (will return a list with k nearest neighbours.) K must be >=0.
    #nn stands for nearest neighbor, and knn stands for 'k nearest neighbours'
    #Example:
    # >>> n=FlannDict()
    # >>> n[[0,0,0,0]]='Hello!'
    # >>> n[[1,0,0,0]]='First!'
    # >>> n[[0,1,0,0]]='Second!'
    # >>> n[[0,0,1,0]]='Third!'
    # >>> n[[0,0,0,1]]='Fourth!'
    #
    # >>> n[[0,0,799,75]]
    # ans = Third!
    #
    # >>> n[[0,0,0]]
    # ERROR: AssertionError: Wrong key shape! key.shape==(3,) but self._key_shape==(4,)
    #
    # >>> n[[0,0,7,75]]
    # ans = Fourth!
    #
    #ANOTHER EXAMPLE:
    #  d=FlannDict()
    #  d[1,2,3]=3
    #  d[1,2,3.1]=1
    #  d[1,2,3.2]=2
    #  d[1,2,3.3]=3
    #  d[1,2,3.4]=4
    #  ans=d[1,2,3.2:3] #Returns ans=[2, 3, 1]

    def __init__(self,*,branching=32,iterations=7,checks=160,complex_keys=False,include_dists=False):
        # pip_import('pyflann')#I would use this library, but it's broken for python3 and has to be fixed with 2to3 before using it (even the one on pypi)
        from rp.libs.pyflann import FLANN#See https://github.com/primetang/pyflann
        self._flann=FLANN()
        self.branching=branching
        self.iterations=iterations
        self.checks=checks
        self.include_dists=include_dists
        self._keys=[]
        self._original_keys=[]
        self._values=[]
        self._need_to_rebuild_index=True
        self._key_shape=None#This is set the first time you set an item
        self._complex_keys=complex_keys#This is set the first time you set an item
        # self._use_cache#It's kinda glitchy because handyhash has a problem hashing numpy arrays because checking for equality with == fails
        self._cache=HandyDict()
        self._old_settings_hash=self._settings_hash()

    def _settings_hash(self):
        #Clear _cache when checks, iterations, branching, or include_dists, etc changes
        return hash((self.branching,self.iterations,self.checks,self.include_dists))#Used to determine whether we have to clear _cache

    def __getitem__(self,key):
        if self._old_settings_hash!=self._settings_hash():
            self._old_settings_hash=self._settings_hash()
            self._cache=HandyDict()#Clear the cache if settings change
        original_key=key
        k=1#k as in "k nearest neighbours. This can be set in slicing.
        if isinstance(key,tuple) and isinstance(key[-1],slice):
            #This is what lets the following code work: d[1,2,3:4] (as opposed to d[(1,2,3):4], which allready works)
            #This part of the code converts d[1,2,3:4] to d[(1,2,3):4]
            #Because (1, 2, slice(3, 4))   ->   slice((1,2,3),4)
            key=slice((*key[:-1],key[-1].start),key[-1].stop)
        return_multiple=False#Whether to return a list of results
        if isinstance(key,slice):
            return_multiple=True
            key,k=key.start,key.stop
            assert isinstance(k,int),'To get k nearest neighbours, use some F=FlannDict() like this: F[point:k]. But you gave k as a non-integer: '+str(k)
            assert k>=0,'Negative values of k are not supported. k='+str(k)
            k=min(k,len(self))
        assert self._keys,'FlannDict is empty!'
        key=self._keyify(key)
        if original_key in self._cache:
            return self._cache[original_key]
        if self._need_to_rebuild_index:#Will be set to true upon adding data
            self._flann.build_index(np.asarray(self._keys).astype(float))#Only do this upon getting; not setting.
            self._cache=HandyDict()#Clear the cache
            self._need_to_rebuild_index=False
        results,dists=self._flann.nn_index(qpts=np.asarray([key]),num_neighbors=k,algorithm="kmeans",branching=self.branching,iterations=self.iterations,checks=self.checks)
        #We're only querying one point, so results and dists should both have length 1...
        dists=dists.squeeze()
        if return_multiple:
            out= [self._values[result] for result in results[0]]
            if self.include_dists:
                out=out,dists**.5#pyflann returns the squared distances, so we must take the square root to find the actual distances
        else:
            out= self._values[results[0]]
            if self.include_dists:
                out= out,dists[0]**.5
        self._cache[original_key]=out
        return out
    def __setitem__(self,key,value):
        self._original_keys.append(key)
        key=self._keyify(key)
        self._keys.append(key)
        self._values.append(value)
        self._need_to_rebuild_index=True
    def __len__(self):
        assert len(self._keys)==len(self._values)
        return len(self._keys)
    def __iter__(self):
        return iter(original_key for original_key in self._original_keys)
    def _keyify(self,key):
        key=np.asarray(key)
        if  self._key_shape is None:
            self._key_shape=key.shape
            self._complex_keys=self._complex_keys or np.iscomplexobj(key)
        else:assert key.shape==self._key_shape,'FlannDict: error: you can\'t use inconsistently-shaped keys -- how are we supposed to compare them? key.shape=='+repr(key.shape)+' but self._key_shape=='+repr(self._key_shape)
        if self._complex_keys:
            key=np.concatenate(([key.real],[key.imag]))
        else:
            assert not np.iscomplexobj(key),'FlannDict: error: you can\' use complex keys with this FlannDict. Please create another with \'complex_keys\' set to True in the constructor.'
        key=key.flatten().astype(float)#Let us use non-vector keys
        return key.tolist()

def best_flann_dict_matches(queries,flann_dict,n:int=None,query_to_vector=lambda x:x):
    #Match multiple vectors to points in a FlannDict and return the results in sorted order of distance as tuples [(query,flann_result,distance)...]
    #Return the top n matches for each query, all sorted by flann's distance metric
    #HINT: If this function is too slow, try set
    #EXAMPLE:
    #    f=FlannDict()
    #    for c in [4+6j,2+9j,1+1j,0+0j]:
    #        f[c]=c
    #    class test:
    #        def __init__(self,x):self.x=x
    #        def __repr__(self):return 'test('+str(self.x)+')'
    #    print(closest_flann_matches([test(3+1j),test(3+6j),test(7+301j)],flann_dict=f,n=3,query_to_vector=lambda _:_.x))
    #PRINTS:
    # [((4+6j), test((3+6j  )), 1.0000),
    #  ((1+1j), test((3+1j  )), 2.0000),
    #  ((0+0j), test((3+1j  )), 3.1622),
    #  ((2+9j), test((3+6j  )), 3.1622),
    #  ((4+6j), test((3+1j  )), 5.0990),
    #  ((1+1j), test((3+6j  )), 5.3851),
    #  ((2+9j), test((7+301j)), 292.04),
    #  ((4+6j), test((7+301j)), 295.01),
    #  ((1+1j), test((7+301j)), 300.05)]

    assert isinstance(flann_dict,FlannDict)
    assert callable(query_to_vector)
    assert n is None or n>=0
    if n is None:n=len(flann_dict)#By default, use the largest (and slowest) possible value of n (that returns the most accurate results)

    old_include_dists=flann_dict.include_dists
    flann_dict.include_dists=True

    matches=[]
    for query in queries:
        results,dists=flann_dict[query_to_vector(query):n]
        matches+=[(result[1],random_float(),(result[0],query,result[1])) for result in zip(results,dists)]#The random_float is to prevent it from trying to sort something that might not be sortable if we have two identical distances (which is a very real possibility)
    matches=sorted(matches)#TODO: If this is a bottle neck, we can use heapq.merge to return a lazy result that merges all the results together in a generator (in-case we just want the top-N results among all of these)
    matches=[match[2]for match in matches]#Just keep the results

    flann_dict.include_dists=old_include_dists

    return matches

def knn_clusters(vectors,k=5,spatial_dict=FlannDict):
    #Given a list of vectors, return a list of sets of vectors belonging to each cluster resulting from the k-nearest neighbor clustering algorithm
    #Requires MUTUAL neighbors to make an edge (aka given two vertices a and b, a must be within b's first closest k neighbours AND b must be within a's closest k neighbours to form an edge. This condition is both sufficient and necessary to form an edge.)
    #EXAMPLE WITH VISUALIZATION: (Try changing n and k)
    #     def test(n=40,k=3):
    #         r=10#Resolution multiplier
    #         image=np.zeros((r*100,r*100,3))
    #         ans=randints_complex(n)
    #         ans=as_points_array(ans)
    #         p= ans
    #         ans=knn_clusters(p,k)
    #         for s in ans:
    #             for c in s:
    #                 for C in s:
    #                     image=cv_draw_contour(image,np.asarray([c,C])*r,color=(0,255,255))

    #         for pp in p:
    #             image=cv_draw_circle(image,*(pp*r).astype(int),radius=3)
    #         display_image(image,False)
    #     test()

    spatial_dict=spatial_dict()#If you want to override the default FlannDict paramers, pass a lambda through this function's spatial_dict parameter
    #Note: This method is logically clean-ish but is probably much less efficient than it could be. If it matters, there's probably many better ways to implement this function.
    assert k>=1
    vectors=np.asarray(vectors)
    assert len(vectors.shape)==2
    vectors=set(map(tuple,vectors))#Make them all hashable...
    for vector in vectors:
        spatial_dict[vector]=vector
    @memoized
    def neighbors(vector):
        return set(map(tuple,spatial_dict[vector:k]))
    unvisited=set(vectors)
    def helper(vector):
        unvisited.remove(vector)
        yield vector
        for neighbor in neighbors(vector):
            if neighbor in unvisited and vector in neighbors(neighbor):
                yield from helper(neighbor)
    out=[]
    while unvisited:
        out.append(set(helper(next(iter(unvisited)))))
    out=sorted(out,key=len,reverse=True)
    return out

def r_transform(path):
    #Stands for Ryan-Transform. Used for path matching in my 2019 Zebra summer internship. Removes translation, rotation and scale freedom from the path.
    #NOTE: According to wolfram alpha, d/dx ln(d/dx f(x)) == f''(x)/f'(x) (this is not true in the discrete domain, however.)
    path=as_complex_vector(path)
    path=circ_diff(path)#Translation invariance: Get all the deltas of the curve. Essentially, take the derivative.
    path=circ_quot(path)#Scale and rotation invariance: essentially get the rotation vectors needed to proportionally scale and twist one delta to the next
    path=np.log(path)#Secret sauce (makes it more useful s.t. when direction/speed doesnt change much, then that part of the output will have a small magnitude. Also taking the log usually raised my eyebrows because of the multiple solution issue. However, there are several reasons this is not a problem. First of all, as we subdivide our cirve more (assuming it's continuously differentiable everywhere, which is why we need a gauss blur), the changes in angle will become very small and will never wrap around pi. Secondly, assuming it's a closed path with no self-intersections, it's accurate to say that a 179 degree turn is very different from a -179 degree turn, because an exact 180 degree turn is impossible (it would imply the curve self-intersects), and that one degree difference determines the direction of the next points on the curve (because they can't self-intersect.) Therefore, even if we DON'T subdivide the curve too much, log is STILL a good measurement and we still don't have to worry about the multiple-solutions of the complex logarithm.)
    return path

def r_transform_inverse(path):
    #Note that we lose scale, rotation and translational information
    #r_transform(r_transform_inverse(r_transform(path))) == r_transform(path)
    path=as_complex_vector(path)
    path=circ_diff_inverse(path)
    path=np.exp(path)
    path=circ_diff_inverse(path)
    return path


def horizontally_concatenated_images(*image_list):
    image_list=detuple(image_list)
    #First image in image_list goes on the left
    #TODO: Handle non-RGB images (include RGBA, grayscale, etc)
    #This is different from np.column_stack because it handles images of different resolutions.
    #It also can mix RGB, greyscale, and RGBA images.

    image_list=[as_rgba_image(as_float_image(image)) for image in image_list]#Right now, bring the images to the max possible format for compatiability. Might make it smarter later such as to preserve the format if all input images are binary, for example.
    max_height=max(img.shape[0]for img in image_list)
    def heightify(img):
        s=list(img.shape)
        s[0]=max_height
        out=np.zeros(tuple(s))
        out[:img.shape[0]]+=img
        return out
    #Make all images RGB instead of RGBA as a hack...
    return np.column_stack(tuple([heightify(img) for img in image_list]))
def vertically_concatenated_images(*image_list):
    #First image in image_list goes on the top
    image_list=detuple(image_list)
    return np.rot90(horizontally_concatenated_images([np.rot90(image,-1) for image in reversed(image_list)]))

def least_squares_regression_line_coeffs(X,Y=None,include_correlation=False):
    #Return m, b such that Y ≈ m*X+b
    #TODO I can't figure out why vectorization makes this SLOWER in bulk....attempted code below...
    #Note: This generalizes to complex numbers (and can be used to calculate least-squares euclidean affine in LINEAR TIME)!
    #If include_correlation is True, it will include the correlation coefficient (r), and so this function would return a tuple of length 3 instead of length 2 (return m,b,r instead of just m,b)
    #Has O(n) complexity as opposed to least_squares_euclidean_affine's original matrix implementation, which takes at least O(n^3) time because of numpy's matrix multiplication implementation
    #X and Y can be separate X,Y values, or X can be a list of points (AKA either X=[2,5,7,3...] and Y=[2,4,8,3...] or X=[[1,2],[4,5],[6,7]...] and Y=None)
    if Y is None:
        X,Y=zip(*X)
    Y=np.asarray(Y)
    X=np.asarray(X)
    # assert len(X.shape)==1
    # assert len(Y.shape)==1
    assert X.shape==Y.shape
    Σ=lambda x:np.sum(x)
    μ=lambda x:np.mean(x)
    Xn=X-μ(X)#Xn is short for 'X normalized'
    Yn=Y-μ(Y)
    ΣXnYn=Σ(Xn*Yn)
    ΣXnXn=Σ(Xn*Xn)
    m=ΣXnYn/ΣXnXn
    b=μ(Y)-μ(m*X)
    if include_correlation:
        #Formula from https://www.statsdirect.com/help/regression_and_correlation/simple_linear.htm
        normalized=lambda x:x/np.linalg.norm(x)
        r=np.sum(normalized(Xn)*np.conj(normalized(Yn)))#Centered-about-the-mean, normalized cosine-similarity is the same thing as correlation
        return m,b,r
    else:
        return m,b

def magnitude(x,**kwargs):
    #Get the total magnitude
    return np.sqrt(np.sum(np.abs(x)**2,**kwargs))

def normalized(x,axis=None):
    #Normalize the vector/matrix/etc to have total magnitude 1
    x=np.asarray(x)
    return x/magnitude(x,axis=axis,keepdims=True)

_javascript_runtime=None#We have a global JS runtime. If you wish to have multiple runtimes, you'd best just use js2py directly.
def _get_javascript_runtime():
    pip_import('js2py')
    import js2py #This library runs javascript, implemented in pure python.
    global _javascript_runtime
    if _javascript_runtime is None:
        _javascript_runtime=js2py.EvalJs()
    return _javascript_runtime
def javascript(code):
    #I created this function to reuse code that I wrote in javascript.
    #Evaluate code written in javascript and return it.
    assert isinstance(code,str)
    return _get_javascript_runtime().eval(code)
js=javascript
def javascript_console():
    #Enter the javascript console, which
    return _get_javascript_runtime().console()

#region Image Channel Conversions
def is_image(image):
    #An image must be either grayscale, rgb, or rgba and have be either a bool, np.uint8, or floating point dtype
    image=np.asarray(image)
    return (is_grayscale_image(image) or is_rgb_image (image) or is_rgba_image  (image))  and\
           (is_float_image    (image) or is_byte_image(image) or is_binary_image(image))

def is_grayscale_image(image):
    #Basically,
    image=np.asarray(image)
    return len(image.shape)==2
def is_rgb_image(image):
    image=np.asarray(image)
    shape=image.shape
    if len(shape)!=3:return False
    number_of_channels=shape[2]
    return number_of_channels==3
def is_rgba_image(image):
    image=np.asarray(image)
    shape=image.shape
    if len(shape)!=3:return False
    number_of_channels=shape[2]
    return number_of_channels==4

def _grayscale_image_to_grayscale_image(image):return image.copy()
def _grayscale_image_to_rgb_image      (image):return grayscale_to_rgb(image)
def _grayscale_image_to_rgba_image     (image):return _rgb_image_to_rgba_image(_grayscale_image_to_rgb_image(image))

def _rgb_image_to_grayscale_image      (image):return rgb_to_grayscale(image)
def _rgb_image_to_rgb_image            (image):return image.copy()
def _rgb_image_to_rgba_image           (image):
    # assert False,'_rgb_image_to_rgba_image: Please fix me Im broken?!'
    return np.concatenate((image,np.ones((*image.shape[:2],255 if is_byte_image(image) else 1),image.dtype)),2)#TODO TEST ME!!!

def _rgba_image_to_grayscale_image     (image):return _rgb_image_to_grayscale_image(_rgba_image_to_rgb_image(image))
def _rgba_image_to_rgb_image           (image):return image[:,:,:3]
def _rgba_image_to_rgba_image          (image):return image.copy()

def as_grayscale_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_grayscale_image(image):return _grayscale_image_to_grayscale_image(image)
    if is_rgb_image      (image):return       _rgb_image_to_grayscale_image(image)
    if is_rgba_image     (image):return      _rgba_image_to_grayscale_image(image)
    assert False,'This line should be impossible to reach because is_image(image).'

def as_rgb_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_grayscale_image(image):return _grayscale_image_to_rgb_image(image)
    if is_rgb_image      (image):return       _rgb_image_to_rgb_image(image)
    if is_rgba_image     (image):return      _rgba_image_to_rgb_image(image)
    assert False,'This line should be impossible to reach because is_image(image).'

def as_rgba_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_grayscale_image(image):return _grayscale_image_to_rgba_image(image)
    if is_rgb_image      (image):return       _rgb_image_to_rgba_image(image)
    if is_rgba_image     (image):return      _rgba_image_to_rgba_image(image)
    assert False,'This line should be impossible to reach because is_image(image).'

# Channel dtype conversions:
def is_float_image(image):
    #A float image is made with floating-point real values between 0 and 1
    # https://stackoverflow.com/questions/37726830/how-to-determine-if-a-number-is-any-type-of-int-core-or-numpy-signed-or-not?noredirect=1&lq=1
    image=np.asarray(image)
    return np.issubdtype(image.dtype,np.floating)

def is_byte_image(image):
    #A byte image is made of unsigned bytes (aka np.uint8)
    #Return true if the datatype is an integer between 0 and 255
    image=np.asarray(image)
    return image.dtype==np.uint8

def is_binary_image(image):
    #A binary image is made of boolean values (AKA true or false)
    image=np.asarray(image)
    return image.dtype==bool

def _float_image_to_float_image  (image):return image.copy()
def _float_image_to_byte_image   (image):return (np.asarray(image,dtype=float)*255).astype(np.uint8)
def _float_image_to_binary_image (image):return np.round(image).astype(bool)
def _byte_image_to_float_image   (image):return np.asarray(image,dtype=float)/255
def _byte_image_to_byte_image    (image):return image.copy()
def _byte_image_to_binary_image  (image):return _float_image_to_binary_image(_byte_image_to_float_image(image))
def _binary_image_to_float_image (image):return np.asarray(image,dtype=float)
def _binary_image_to_byte_image  (image):return _float_image_to_byte_image(_binary_image_to_float_image(image))
def _binary_image_to_binary_image(image):return image.copy()

_channel_conversion_error_message='The given input image has an unrecognized dtype (there are no converters for it)'
def as_float_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_float_image (image):return  _float_image_to_float_image(image)
    if is_byte_image  (image):return   _byte_image_to_float_image(image)
    if is_binary_image(image):return _binary_image_to_float_image(image)
    assert False,_channel_conversion_error_message

def as_byte_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_float_image (image):return  _float_image_to_byte_image(image)
    if is_byte_image  (image):return   _byte_image_to_byte_image(image)
    if is_binary_image(image):return _binary_image_to_byte_image(image)
    assert False,_channel_conversion_error_message

def as_binary_image(image):
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_float_image (image):return  _float_image_to_binary_image(image)
    if is_byte_image  (image):return   _byte_image_to_binary_image(image)
    if is_binary_image(image):return _binary_image_to_binary_image(image)
    assert False,_channel_conversion_error_message

def random_rgb_byte_color():
    return (randint(255),randint(255),randint(255))
def random_rgba_byte_color():
    return (randint(255),randint(255),randint(255),randint(255))
def random_grayscale_byte_color():
    return (randint(255))

def random_rgb_float_color():
    return (random_float(1),random_float(1),random_float(1))
def random_rgba_float_color():
    return (random_float(1),random_float(1),random_float(1),random_float(1))
def random_grayscale_float_color():
    return (random_float(1))

def random_rgb_binary_color():
    return (random_chance(1/2),random_chance(1/2),random_chance(1/2))
def random_rgba_binary_color():
    return (random_chance(1/2),random_chance(1/2),random_chance(1/2),random_chance(1/2))
def random_grayscale_binary_color():
    return (random_chance(1/2))

def is_binary_color(color):
    return all(np.asarray(x).dtype==bool for x in color)
def is_byte_color(color):
    return all(np.issubdtype(image.dtype,np.integer) for x in color)
def is_float_color(color):
    return all(np.issubdtype(image.dtype,np.floating) for x in color)
#TODO: Finish color conversions

#endregion

def running_in_ipython():
    try:
        #Can detect if we're in a jupyter notebook
        pip_import('IPython')
        from IPython import get_ipython
        return get_ipython() is not None
    except:
        return False#If we get an error when trying to import IPython...then..well, we're definately NOT running in iPython!
def running_in_google_colab():
    #Return true iff this function is called from google colab
    import sys
    return 'google.colab' in sys.modules


def split_tensor_into_regions(tensor,*counts,flat=True):
    #Return the tensor into multiple rectangular regions specified by th number of cuts we make on each dimension.
    #Uses: Splitting pictures that contain multiple entried of the mnist dataset into usable chunks of data
    # Let ‹a,b,c...› represent some numpy tensor with shape (a,b,c...)
    # EXAMPLES:
    #     split_tensor_into_regions(‹a,b,c›, x, y, flat=False)  ->  ‹x, y, a//x, b//y, c›  #Think of c as 3, and a and b the width of some RGB image
    #     split_tensor_into_regions(‹a,b,c›, x, y, flat=True )  ->  ‹x*y , a//x, b//y, c›  #Instead of addresing the regions by coordinates, we get a flat list of regions
    #     split_tensor_into_regions(‹a,b,c›, x, y, z, flat=True )  ->  ‹x*y*z  , a//x, b//y, c//z›
    #     split_tensor_into_regions(‹a,b,c›, x, y, z, flat=False)  ->  ‹x, y, z, a//x, b//y, c//z›
    #     split_tensor_into_regions(‹a,b,c,d›, x, y, z, flat=False)  ->  ‹x, y, z, a//x, b//y, c//z, d›
    #     split_tensor_into_regions(‹a,b,c,d›, x, flat=False)  ->  ‹x, a//x, b, c, d›
    #     split_tensor_into_regions(‹a,b,c,d›, x, flat=True )  ->  ‹x, a//x, b, c, d›      #Flattening doesnt make a difference when we only split on one dimension
    #     split_tensor_into_regions(‹a,b,c,d›)  ->  ‹a, b, c, d›      #Passing no arguments to 'counts' just returns the value of the original tensor. Of course, the flat argument doesnt make a difference here as there are no splitting dimensions to flat.
    #EXAMPLE APPLICATION:
    #   http://www.cs.unc.edu/~lazebnik/research/spring08/faces.jpg
    #   Look at that picture. You'll see an array of 10*10 faces. We need to pre-process this image to extract the individual faces.
    #   output=split_tensor_into_regions(‹that image›,10,10,flat=False)  (it doesn't matter if the image is RGB or not, it can handle either case)
    #   Then, output[0,0] is the upper left face, and output[0,1] is one-to-the-right of the top left image
    #   Also, output[1,:] is a list of all the faces on the second row ([face1,face2,face3...])
    #   But maybe we want to do PCA on all these images. We don't want to address these faces by coordinate anymore; we want to get rid of that information.
    #   We just want one big flattened list of faces. To do this, we would instead use
    #   output=split_tensor_into_regions(‹that image›,10,10,flat=True)
    #   This would give us a list of numpy arrays containing every face in the image, such that output[35] would exist (and, because it's a 10x10 faces image, give us the 5th face on the third row (taking into account starting at the 0th index))

    tensor=np.asarray(tensor)
    shape=tensor.shape
    new_shape=list(shape)

    assert len(counts)<=len(shape),'We can\'t split a tensor of shape '+str(shape)+' along '+str(len(counts))+' of its dimensions becuase it only has '+str(len(shape))+' dimensions'
    for index,count in reversed(list(enumerate(counts))):
        assert isinstance(count,int) and count>0,'All arguments to "counts" should be positive integers representing how many pieces we should slice the tensor in their respective dimension'
        assert shape[index]==new_shape[index],'Internal logical assertion. This should never fail.'
        assert not shape[index]%count,'All counts should evenly divide their respective dimension in the tensor, but '+str(shape[index])+'%'+str(count)+'!=0'
        new_shape[index]//=count
        new_shape.insert(index,count)

    def f(n,m):
        #This is a small helper function to create transpose_axes
        #EXAMPLES:
        # * Note: The | in the outputs is just for visual purposes to help you see the pattern faster
        # f(0,0)   -->   []
        # f(2,0)   -->   [0 2|1 3]
        # f(3,0)   -->   [0 2 4|1 3 5]
        # f(4,0)   -->   [0 2 4 6|1 3 5 7]
        # f(4,1)   -->   [0 2 4 6|1 3 5 7|8]
        # f(4,2)   -->   [0 2 4 6|1 3 5 7|8 9]
        # f(4,3)   -->   [0 2 4 6|1 3 5 7|8 9 10]
        # f(3,3)   -->   [0 2 4|1 3 5|6 7 8]
        # f(2,3)   -->   [0 2|1 3|4 5 6]
        # f(1,3)   -->   [0|1|2 3 4]
        # f(0,3)   -->   [0 1 2]
        o=list(range(2*n+m))
        a=o[0:2*n+0:2]
        b=o[1:2*n+1:2]
        o[0*n:1*n]=a
        o[1*n:2*n]=b
        return o
    transpose_axes=f(len(counts),len(shape)-len(counts))

    out=tensor.reshape(new_shape).transpose(transpose_axes)

    if flat:
        out=out.reshape(*(np.product(out.shape[:len(counts)]),*out.shape[len(counts):]))

    return out

def bordered_image_solid_color(image,color=(1.,1.,1.,1.),thickness=1,width=None,height=None,top=None,bottom=None,left=None,right=None):
    #Add a pixel border of color around the image with a solid color
    #Currently converts the input image into floating-point rgba
    #You can specify the border by thickness (controls top,bottom,left and right all at once)
    #You can override that thickness by setting width or height to some values (height overrides top and bottom if they're None and width overrides left and right if they're None)
    #You can override top, bottom, left and right manually (if these are set, they override anything set by width or height etc)
    assert len(color)==4,'Color must be rgba floats'

    #Inheritance options (better than having to specify top, bottom, left and right all manually if that would be redundant)
    width =thickness if width  is None else width
    height=thickness if height is None else height
    top   =height    if top    is None else top
    bottom=height    if bottom is None else bottom
    left  =width     if left   is None else left
    right =width     if right  is None else right
    assert thickness>=0,'Cannot have a negative border thickenss (measured in pixels)'
    assert height>=0 and width>=0,'Cannot have a negative border height or width (measured in pixels)'
    assert top>=0 and bottom>=0 and left>=0 and right>=0,'Cannot have a negative border thickness top, bottom, left or right (measured in pixels)'

    #We convert the image into rgba-floating point format (with colors between 0 and 1)
    image=np.asarray(image)
    image=as_rgba_image(image)
    image=as_float_image(image)

    colorize = lambda x: x*0+[[list(color)]]
    image=np.concatenate((colorize(image[:top   ]),image,colorize(image[:bottom ])),axis=0)#Add top and bottom borders
    image=np.concatenate((colorize(image[:,:left]),image,colorize(image[:,:right])),axis=1)#Add left and right borders
    return image

def get_principle_components(tensors,number_of_components=None):
    #Returns orthogonal, normalized, sorted-by-eigenvalue-in-descending-order principle components (retaining the shape of the original tensors, to make eigenfaces easy to extract for example)
    #For example, if we feed get_principle_components a list of images, we expect to return a list of images (not a list of vectors, like most PCA implementations require). This is for the sake of convenience.
    #NOTE: This function also works on RGB images just like it does grayscale images (like in the demo)
    #EXAMPLE:
    #   def demo(image_path,rows,cols):
    #       image=load_image(image_path,from_cache=True)
    #       faces=split_tensor_into_regions(image,rows,cols,flat=True)
    #       eigenfaces=get_principle_components(faces,number_of_components=20)
    #       print('Displaying principle components...')
    #       for face in eigenfaces:#Note how they get progressively more noisy the further down the components we go
    #           display_image(full_range(face))
    #           sleep(.5)
    #       print('Showing a few reconstructions...')
    #       for face in shuffled(faces)[:20]:
    #           face=face-face.mean()
    #           face=normalized(face)
    #           coeffs=(face*eigenfaces).sum(1).sum(1)
    #           reconstructed_face=np.sum(eigenfaces*np.expand_dims(np.expand_dims(coeffs,1),1),0)
    #           display_image(horizontally_concatenated_images(full_range(face),full_range(reconstructed_face)))
    #           sleep(.5)
    #   print("Eigenfaces demo:")
    #   demo("http://www.cs.unc.edu/~lazebnik/research/spring08/faces.jpg",10,10)
    #   print("Fashion MNIST demo:")
    #   demo("https://github.com/zalandoresearch/fashion-mnist/raw/master/doc/img/fashion-mnist-sprite.png",30,30)
    cv2=pip_import('cv2')

    tensors=np.asarray(tensors)
    number_of_tensors=len(tensors)
    tensor_shape=tensors[0].shape
    assert len(tensor_shape)>=1,'This is a bug. I dont know why this breaks opencv, but your tensor must have more dimensions. Maybe I can build a workaround that inserts dimensions temporarily, but I\'ll leave that for another day'
    if number_of_components is None:
        #Warning: this is the max possible value, and can be quite slow
        number_of_components=min(number_of_tensors,100)#This cap at 100 is for safety's sake. The opencv code can't be cancelled with a KeyboardInterrupt, so if you give it too much to calculate you're stuck rebooting rp
    number_of_components=min(number_of_tensors,number_of_components)
    vectorized_tensors=tensors.reshape(number_of_tensors,np.prod(tensor_shape))
    mean, eigenvectors=cv2.PCACompute(vectorized_tensors, mean=None, maxComponents=number_of_components)#Why mean=None? See https://stackoverflow.com/questions/47016617/how-to-use-the-pcacompute-function-from-python-in-opencv-3
    principle_components=eigenvectors.reshape(number_of_components,*tensor_shape)
    principle_components=np.asarray(list(map(normalized,principle_components)))#Each principle component is almost, but not quite perfectly normalized by opencv (one had a magnitude of 1.0000377) but we're going to normalize them again for even more precision. Side-note: it's ok to use a python-loop here because there shouldn't be many principle_components to begin with (that's very slow)
    assert len(principle_components)==len(eigenvectors)==number_of_components,'This is an internal assertion that should never fail'
    return principle_components

def cv_box_blur(image,diameter=3,width=None,height=None):
    cv2=pip_import('cv2')
    image=np.asarray(image)
    width =diameter if width  is None else width
    height=diameter if height is None else height
    assert width>=0 and height>=0
    if not width or not height:
        return image.copy()
    return cv2.blur(image,(width,height))

def rinsp_search(root,query,depth=10):
    #THIS IS A WORK IN PROGRESS
    #example: trying to find the conv function in torch? Maybe it's nested in some modules...wouldn't it be nice to automatically search the whole tree of a, a.b, a.c, a.d, b, b.a, b.a.c, etc... this does that
    #example:
    #TODO: Allow searching the docs etc more than just searching the name
    #TODO: Allow fuzzy search, better queries (fuzzy find for example with nice printed outputs)
    #TODO: Make this breadth-first instead of depth first
    def match(name):
        assert isinstance(query,str)
        assert isinstance(name,str)
        return query.lower() in name.lower()

    def keys(root):
        out=set()
        try:out.update(dir(root))
        except:pass
        try:out.update(root.__dict__)
        except:pass
        return sorted(out)

    def get(root,key):
        try:return getattr(root,key)
        except:pass
        try:return root.__dict__[key]
        except:pass
        try:return eval('root.'+key)
        except:pass
        raise

    searched=set()
    def helper(root=root,depth=depth,path=[]):
        if not depth or id(root) in searched:
            return
        searched.add(id(root))
        for name in keys(root):
            if match(name):yield path+[name]
            try:yield from helper(get(root,name),depth-1,path+[name])
            except:pass

    def highlighted(string,query):
        #Case insensitive fansi-highlighting of a query in a string
        #Example: print(highlighted('Hello, world wORld hello woRld!','world'))#All the 'world','wORld', etc's are printed green and bold
        i=string.lower().find(query.lower())
        if i==-1:return string#No matches -> no highlighting.
        s =string[:i]
        j=i+len(query)
        s+=fansi(string[i:j],'green','bold')
        s+=highlighted(string[j:],query)
        return s

    out=[]
    for result in helper():
        print(highlighted('.'.join(result),query))
        out+=result
    return out

def as_numpy_array(x):
    #Will convert x into type np.ndarray
    #This should convert anything that can be converted into a numpy array
    #Should work for torch tensors, python lists of numbers, etc.
    #Will necessarily make a copy of x so you dont have to worry about mutations etc
    try:return np.asarray(x)#For numpy arrays and python lists (and anything else that work with np.asarray)
    except:pass
    try:return x.detach().cpu().numpy()#For pytorch. We're not doing an isinstance check of type pytorch tensor becuse that involves importing pytorch, which might be slow. Try catch is faster here.
    except:pass
    assert False,'as_numpy_array: Error: Could not convert x into a numpy array. type(x)='+repr(type(x))+' and x='+repr(x)

def input_conditional(question,condition=lambda answer:True,on_fail=lambda answer: print('Please try again. Invalid input: '+repr(answer)),prompt=' > '):
    #Keeps asking the user for a console input until they satisfy the condition with their answer.
    #Example: ans=input_conditional('Please enter yes or no.', lambda x: x.lower() in {'yes','no'},)
    assert isinstance(question,str),'The "question" should be a string'
    assert callable(condition),'"condition" should be a boolean function of the users input'
    assert callable(on_fail),'"on_fail" should be a void function of the users input'
    assert isinstance(prompt,str),'The "prompt" should be a string'

    print(question)
    while True:
        answer=input(prompt)
        if condition(answer):
            return answer
        on_fail(answer)

def input_yes_no(question):
    #A boolean function of the user's console input
    #The user must say y, ye, yes, n or no to continue
    #Example: input_yes_no('Are you feeling well today?')
    return 'yes'.startswith(input_conditional(question+'\nPlease enter yes or no.', lambda x: x.lower() in {'y','ye','yes','n','no'}).lower())

def input_select(question='Please select an option:',options=[],stringify=repr):
    #Allow the user to choose from a list of numbered options
    #stringify is how we turn options into strings (options dont have to be strings)
    #Example: Try running 'input_select_option(options=['Hello','Goodbye','Bonjour'])'

    assert len(options),'input_select: Invalid input: Cannot select from 0 options.'

    number_of_options=len(options)
    max_number_of_digits=len(str(number_of_options))

    for i,e in enumerate(options):
        question+='\n'+str(i).rjust(max_number_of_digits)+': '+stringify(e)

    def condition(input):
        try:
            i=int(input)
            if i!=float(input):#No fractions
                return False
            return 0<=i<number_of_options
        except ValueError:#ERROR: ValueError: invalid literal for int() with base 10: 'aosijd
            return False

    user_input=input_conditional(question+'\nPlease enter an integer between 0 and '+str(number_of_options-1)+' (inclusive).',condition)

    return options[int(user_input)]


@memoized
def download_youtube_video(url,path='./'):
    #TODO: Implement a fallback method using 'you_get' (you_get is a pypy package. where pytube gets 403 permission errors donwloading lindsey stirling videos, you_get succeedes)
    pip_import('pytube')
    import pytube
    yt = pytube.YouTube(url)
    stream = yt.streams.first()
    stream.download(path)
    return os.path.join(path,stream.default_filename)

# def make_video(outvid, images=None, fps=30, size=None,is_color=True, format="FMP4"):
#     #WARNING: THIS DEFINITION IS GONIG TO CHANGE LATER TO MAKE IT SIMPLER
#     #CODE FROM https://www.dlology.com/blog/how-to-run-object-detection-and-segmentation-on-video-fast-for-free/
#     """
#     Create a video from a list of images.

#     @param      outvid      output video
#     @param      images      list of images to use in the video
#     @param      fps         frame per second
#     @param      size        size of each frame
#     @param      is_color    color
#     @param      format      see http://www.fourcc.org/codecs.php
#     @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
#     """
#     from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
#     fourcc = VideoWriter_fourcc(*format)
#     vid = None
#     for image in images:
#         if not os.path.exists(image):
#             raise FileNotFoundError(image)
#         img = imread(image)
#         if vid is None:
#             if size is None:
#                 size = img.shape[1], img.shape[0]
#             vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
#         if size[0] != img.shape[1] and size[1] != img.shape[0]:
#             img = resize(img, size)
#         vid.write(img)
#     vid.release()
#     return vid


def _get_video_file_duration_via_moviepy(path):
    #https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
    #pip install moviepy
    pip_import('moviepy')
    from moviepy.editor import VideoFileClip
    return VideoFileClip(path).duration

_get_video_file_duration_cache={}
def get_video_file_duration(path,from_cache=True):
    #Returns a float, representing the total video length in seconds
    if from_cache and path in _get_video_file_duration_cache:
        return _get_video_file_duration_cache[path]
    out=_get_video_file_duration_via_moviepy(path)
    _get_video_file_duration_cache[path]=out
    return out

def load_video_stream(path):
    #Much faster than load_video, which loads all the frames into a numpy array. This means load_video has to iterate through all the frames before you can even use the first frame.
    #load_video_stream is a generator, meaning to get the next frame you use python's builtin 'next' function
    #Returns a generator that iterates through the frame images
    #EXAMPLE:
    #    for frame in load_video_stream("/Users/Ryan/Desktop/media.io_Silicon Valley - Gavin - Animals Compilation copy.mp4"):display_image(frame)
    #EXAMPLE:
    #    for frame in load_video_stream(download_youtube_video('https://www.youtube.com/watch?v=cAy4zULKFDU')):display_image(frame)  #Monty python clip
    cv2=pip_import('cv2')
    assert file_exists(path),'load_video error: path '+repr(path)+' does not point to a file that exists'#Opencv will silently fail if this breaks
    cv_stream=cv2.VideoCapture(path)
    while True:
        not_done,frame=cv_stream.read()
        if not not_done:
            return
        yield cv_bgr_rgb_swap(frame)

_load_video_cache={}
def load_video(path,*,show_progress=True,from_cache=False):
    #This function does not take into account framerates or audio. It just returns a numpy array full of images.
    #It's slower than load_video_stream, but it can be cached using from_cache (which would actually make it faster, if applicable)
    progress_prefix="\rload_video: path="+repr(path)+": "
    if from_cache and path in _load_video_cache:
        return _load_video_cache[path]
    stream=load_video_stream(path)
    out=[]
    for i,frame in enumerate(stream):
        if show_progress:print(end=progress_prefix+"Loaded frame "+str(i)+"...")
        out.append(frame)
    if show_progress:print(end=progress_prefix+'done loading frames, creating numpy array...')
    out=np.asarray(out)
    if show_progress:print(end='done.\r\n')
    _load_video_cache[path]=out
    return out

def save_video(images,path):
    #TODO: add options for sound and framerate. Possibly quality options but probably not (that should be delegated to a function meant for a specific format)
    #Save a series of images into a video.
    #Note that the file extension used in path decides the kind of video that will be exported.
    #For example, save_video(images,'video.mp4') saves an mp4 file whilst save_video(images,'video.avi') saves an avi file
    pip_import('skvideo.io','sk-video')
    import skvideo.io#pip install sk-video:
    #NOTE: Quicktime on my mac can't play these. Idk why. But the video outputs are NOT broken. VLC video player CAN play them without error.
    skvideo.io.vwrite(path,images)

def directory_exists(path):
    return os.path.isdir(path)
folder_exists=directory_exists
is_a_folder=is_a_directory=directory_exists#Synonyms, you might want one more than another depending o nthe context. Sometimes we might want to know if it exists, and others we might allready know the path exists and want to see what kind of path it is. It's just to make it more readable, that's all. Less need for comments like these lol.

def file_exists(path):
    return os.path.isfile(path)
is_a_file=file_exists

def path_exists(path):
    return file_exists(path) or directory_exists(path)
# is_a_path=path_exists #Can be confused with complex vector paths etc, and also this isn't that descriptive...don't want code to be dependent on this synonym...

def rename_path(path,new_name):
    #EXAMPLE:
    #   rename_path("apple/bananna/cherry.jpg","coconut.png")
    #       is equivalent to (in bash)
    #   mv .apple/bananna/cherry.jpg apple/bananna/coconut.png
    os.rename(path,os.path.join(get_path_parent(path),new_name))
rename_file=rename_path#Synonyms that might make more sense to read in their context than rename_path
rename_folder=rename_path
rename_directory=rename_path

def move_path(path,directory):
    #Move a folder or file into a given directory
    assert directory_exists(directory)
    os.rename(path,os.path.join(directory,path))
move_file=move_diectory=move_folder=move_path#Synonyms that might make more sense to read in their context than rename_path

def delete_path(path,*,permanent=False):
    #TODO: Let delete_path delete folders recursively permanently.
    # permanent exists for safety reasons. It's False by default in case you make a stupid mistake like deleting this file. When false, it will send your files to the trash bin on your system (Mac,Windows,Linux, etc)
    # http://stackoverflow.com/questions/3628517/how-can-i-move-file-into-recycle-bin-trash-on-different-platforms-using-pyqt4
    # https://pypi.python.org/pypi/Send2Trash
    # pip3 install Send2Trash
    import os
    assert os.path.exists(path),"r.delete_path: There is no file to delete. The path you specified, '" + path + "', does not exist!"  # This is to avoid the otherwise cryptic errors you would get later on with this method
    if permanent:
        os.remove(path)
    else:
        pip_import('send2trash')
        import send2trash  # This is much safer. By default, we move files to the trash bin. That way we can't accidentally delete our whole directory for good ;)
        send2trash.send2trash(path)  # This is MUCH safer than when delete_permanently is turned on. This will have the same effect as deleting it in finder/explorer: it will send your file to the trash bin instead of immediately deleting it forever.
delete_file=delete_path#Synonyms that might make more sense to read in their context than rename_path

def delete_paths(*paths,permanent=False):
    #EXAMPLE:  delete_paths( 'a.jpg','b.jpg' )
    #EXAMPLE:  delete_paths(['a.jpg','b.jpg'])
    #EXAMPLE:  delete_paths(('a.jpg','b.jpg'))
    paths=detuple(delist(paths))
    for path in paths:
        if isinstance(path,str):
            delete_path(path,permanent=permanent)
delete_files=delete_paths

def copy_path(from_path,to_path,*,extract=False):
    #Chooses between copy_directory and copy_file, whichever makes more sense.
    #If extract is True, it will copy only the contents of the folder to the destination, as opposed to copying the actual folder itself.
    #Works with both files and directories. If given a directory, it will be copied recursively.
    assert path_exists(from_path),'Cannot copy from from_path='+repr(from_path)+' because that path does not exist'
    if is_a_directory(from_path):
        copy_directory(from_path,to_path,extract=extract)
    else:
        copy_file(from_path,to_path)

def copy_to_folder(from_path,to_path):
    #Copy a file or directory to a folder, keeping the same file name
    #For example, copy_to_folder('/docs/text.txt','some/folder/path') will create a new file whose path is 'some/folder/path/text.txt'
    #This can be nicer than copy_path, because then we don't have to rewrite the file name twice.
    #This function also works with folders, and copies them recursively.
    assert is_a_folder(to_path),'to_path must be a folder, but '+repr(to_path)+' either does not exist or is not a folder'
    dest=path_join(to_path,get_path_name(from_path))
    copy_path(from_path,dest)
copy_to_directory=copy_to_folder


def copy_directory(from_path,to_path,*,extract=False):
    #Recursively copy a directory.
    #If extract is True, it will copy only the contents of the folder to the destination, as opposed to copying the actual folder itself.
    #Note: the default extract=False must not change. Future versions of rp must respect this.
    assert path_exists     (from_path),'rp.copy_directory error: Cant copy from path '+repr(from_path)+' because that path does not exist'
    assert is_a_directory  (from_path),'rp.copy_directory error: from_path='+repr(from_path)+' is not a directory, and this function is specifically meant to copy directories.'
    assert not file_exists (to_path  ),'rp.copy_directory error: Cant copy a directory into a file. from_path='+repr(from_path)+' is a directory and to_path='+repr(to_path)+' is a file.'
    if not directory_exists(to_path  ):make_directory(to_path)#Make sure the destination path can exist...
    assert directory_exists(to_path  ),'rp.copy_directory error: Internal logical assertion. If this fails, then copy_directory is broken. make_directory should either be successful or throw an error.'
    if not extract:to_path=make_directory(path_join(to_path,get_directory_name(from_path)))
    from importlib import reload
    import distutils.dir_util
    reload(distutils.dir_util)#I don't know why, but when I copied a folder, deleted it, then told it to copy again, it broke with "ERROR: distutils.errors.DistutilsFileError: could not create 'TestJam/Wampo/prompt_toolkit/filters/.DS_Store': No such file or directory" and reloading the module appeared to fix it. This reloading doesn't appear to damage performance, I clocked it at 0.0003399848937988281 seconds
    distutils.dir_util.copy_tree(from_path,to_path)#Copy the directory's contents recursively...

def copy_file(from_path,to_path):
    #Copy a single file from from_path to to_path, where to_path is either a folder or a file that will be overridden
    assert file_exists(from_path),'copy_file copies a file from from_path to to_path, but from_path='+repr(from_path)+' is not a file'
    assert path_exists(to_path),'to_path must be either a directory or a file that will be overwritten, but to_path='+repr(to_path)+' does not exist'
    import shutil
    if is_a_directory(to_path):
        to_path=path_join(to_path,get_file_name(from_path))
    shutil.copyfile(from_path,to_path)

def get_path_parent(path):
    #Works for directories and files
    #EXAMPLES:
    #   ⮤ get_path_parent('oaijsd/odjf/aoijf/sdojif.ojf')
    #  ans = oaijsd/odjf/aoijf
    #   ⮤ get_path_parent('/')
    #  ans = /
    #   ⮤ get_path_parent('/apsokd')
    #  ans = /
    #   ⮤ get_path_parent('/apsokd.asd')
    #  ans = /
    #   ⮤ get_path_parent('/aps/asda/sokd.asd')
    #  ans = /aps/asda
    import pathlib
    return str(pathlib.Path(path).parent)
get_file_folder=get_path_parent#Synonyms that might make more sense to read in their context than get_path_parent
get_file_directory=get_path_parent
get_parent_directory=get_parent_folder=get_path_parent

def make_directory(path):
    #Will make a directory if it doesn't allready exist. If it does already exist, it won't throw an error.
    #However, it will throw an error if the specified path is impossible to make without deleting some file.
    #Can make nested paths that don't exist yet. You don't have to manually create every level.
    #For example, let's say you don't have Jumble, Fizz, or Buzz on your computer. make_directory('Jumble/Fizz/Buzz') will create three directories nested inside of each other
    try:
        if not directory_exists(path):
            os.mkdir(path)
        return path
    except OSError:
        from pathlib import Path
        cursor=Path(path)
        need_to_make=[]#Parent directories we would need to make in order to make the full path specified
        while not cursor.exists():
            need_to_make.append(cursor)
            cursor=cursor.parent
        while cursor != cursor.parent:
            assert cursor.is_dir(),'make_directory: failed to make directory at path '+repr(path)+' because '+repr(cursor)+' is the path of an existing file that is not a directory'
            cursor=cursor.parent
        for directory in reversed(need_to_make):
            directory.mkdir()
        return str(path)
make_folder=make_directory

def delete_all_files_in_directory(directory,*,permanent=False):
    assert directory_exists(directory)
    delete_paths(get_file_paths(directory),permanent=permanent)
delete_all_files_in_folder=delete_all_files_in_directory

path_join=joined_paths=os.path.join#Synonyms for whatever comes into my head at the moment when using the rp terminal



_get_cutscene_frame_numbers_cache={}
def get_cutscene_frame_numbers(video_path,*,from_cache=False):
    #Returns a list of ints containing all the framenumers of the cutscenes in a video
    #Confirmed to work with mp4 files
    #Note: Right now this only supports reading from a video file, as opposed to reading from a numpy array containing
    #pip install scenedetect
    #Code from https://pyscenedetect-manual.readthedocs.io/en/latest/api/scene_manager.html#scenemanager-example
    #EXAMPLE:
    #    video_path=download_youtube_video('https://www.youtube.com/watch?v=K5qACexzwOI')
    #    cutscene_frames_numbers=get_cutscene_frame_numbers(video_path)
    #    for i,frame in enumerate(load_video_stream(video_path)):
    #        if i in cutscene_frames_numbers:
    #            input('Hit enter to continue')
    #        cv_imshow(frame)
    #        sleep(1/30)
    pip_import('cv2')#Needed for scenedetect
    pip_import('scenedetect')

    if video_path in _get_cutscene_frame_numbers_cache:
        return _get_cutscene_frame_numbers_cache[video_path]

    # Standard PySceneDetect imports:
    from scenedetect.video_manager import VideoManager
    from scenedetect.scene_manager import SceneManager
    # For caching detection metrics and saving/loading to a stats file
    from scenedetect.stats_manager import StatsManager

    # For content-aware scene detection:
    from scenedetect.detectors.content_detector import ContentDetector

    # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    # We save our stats file to {VIDEO_PATH}.stats.csv.

    scene_list = []

    try:
        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list(base_timecode)
        # Each scene is a tuple of (start, end) FrameTimecodes.

    finally:
        video_manager.release()

    output = [x[1].frame_num for x in scene_list]
    _get_cutscene_frame_numbers_cache[video_path]=output
    return output

def send_text_message(message,number):
    #number is a phone number. Can be an int or a string
    #Once this no longer works (which it eventually won't, because it's running on a free trial), replace the credentials with your own twilio trial account
    #OR create a fallback that doesnt use twilio
    #EXAMPLE:
    #    send_text_message('Hello, World!',15436781234)
    #CODE FROM: https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library
    account_sid = 'AC35ef9db2c1104ea2764964cf0ddb7ebb'
    auth_token  = '0543decd5b2eb41e82393e8015c92f48'
    from_number = '16313052383'
    pip_import('twilio')
    from twilio.rest import Client
    number=str(number)
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body=message,
                     from_='+'+str(from_number),
                     to='+'+number
                 )

def crop_image_zeros(image):
    #Given some big image that is surrounded by black, or 0-alpha transparency, crop out that excess region
    #TODO: Give examples
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'
    if is_grayscale_image(image):
        points=np.argwhere(image)#Crop out the black regions
    elif is_rgb_image(image):
        points=np.argwhere(np.any(image,axis=2))#Crop out the black regions
    elif is_rgba_image(image):
        points=np.argwhere(image[:,:,3])#Crop to where there's alpha
    else:
        assert False,'crop_image_zeros cannot handle this image type and this function needs to be updated'
    top,left=np.min(points,axis=0)
    bottom,right=np.max(points,axis=0)+1
    cropped=image[top:bottom,left:right]
    print(top,bottom,left,right)
    return cropped

def cv_contour_to_segment(contour):
    #TODO: provide a visual example
    #The way OpenCV extracts single-pixel-wide non-looping contours is to treat those contours as loops, where the second half of the points are just the first-half of the points mirrored
    #If we want to find the start/end points of a segment, we need to find the two points of symmetry (which are visually obvious, but its not a given that they exist such as if we have a T-junction)
    #We do this by autocorrelating the contour with it's mirrored self (AKA the reverse of the contour) to find the shift of the reverse that best matches the original contour. This is equivalent to auto-convolving the contour with itself. We will get two minima, but we only need one. The second symmetry point should be exactly half-way down that contour.
    #For example: a contour created by opencv's find contours might look like [[1,1],[[2,2]],[[3,3]],[[4,4]],[[3,3]],[[2,2]]] but obviously we just want [[[1,1]],[[2,2]],[[3,3]],[[4,4]]] and to discard the duplicates. That's what cv_contour_to_segment does.
    #This function can be used to get the starting and end points of the segment, which is a bit of a tricky problem.
    #The output of a contour given to this function should have half the original length.
    #WARNING: This function doesn't check to see if the contour you gave it is actually a segment; be careful! You can usually check to see if a contour is a segment (if using cv_find_contours) by seeing if contour.is_solid_white is True (AKA if the contour doesn't enclose any non-white,area)
    contour=as_complex_vector(contour)
    if len(contour)<=3:
        return contour.copy()
    similarities=circ_conv(contour,contour.conj()).real
    i=np.argmax(similarities)
    return np.roll(contour,(len(contour)-i)//2)[:len(contour)//2]

def whiten_points_covariance(points):
    #Whiten the covariance matrix of a list of n-dimensional points, and return a list of new points.
    #Also works with 2d-contours represented as indicated by is_points_array, is_complex_vector, and is_cv_contour
    #EXAMPLE CODE:
    #    points=np.random.randn(1000,2)
    #    points[:,0]*=10#Stretch the distribution along the y-axis
    #    points=apply_affine(points,rotation_affine_2d(70))#Rotate the stretched distrubition
    #    ans=input("Displaying points before whitening...(press enter to continue)")
    #    scatter_plot(points)
    #    whitened=whiten_points_covariance(points)
    #    print('Displaying points after whitening (note how it looks like a unit normal distribution now)')
    #    scatter_plot(whitened)
    pip_import('sklearn')
    from sklearn.decomposition import PCA
    contour=as_numpy_array(points)
    if is_complex_vector(points) or is_cv_contour(points):
        points=as_points_array(points)#Support for making contours invariant to stretching in a given direction by normalizing their covariance (idea from Zebra 2019 internship).
    assert len(points.shape)==2,'Input should be a matrix, aka a list of points. But your input has shape '+str(points.shape)
    pca = PCA(whiten=True)
    whitened = pca.fit_transform(points)
    return whitened

def visible_string_ljust(string,width,fillchar=' '):
    #Trying to be as much like str.ljust as possible, with a small tweak:
    #str.ljust doesn't ignore ansi escape sequences, nor does it take into account unicode character widths.
    #The small tweak is that this function does (as best as it can).
    #This function works with fansi well, but str.ljust does not.
    delta_width=max(0,width-visible_string_length(string))
    return string+fillchar*delta_width

def visible_string_rjust(string,width,fillchar=' '):
    #Trying to be as much like str.rjust as possible, with a small tweak:
    #str.rjust doesn't ignore ansi escape sequences, nor does it take into account unicode character widths.
    #The small tweak is that this function does (as best as it can).
    #This function works with fansi well, but str.rjust does not.
    delta_width=max(0,width-visible_string_length(string))
    return fillchar*delta_width+string

def visible_string_center(string,width,fillchar=' '):
    #Trying to be as much like str.center as possible, with a small tweak:
    #str.center doesn't ignore ansi escape sequences, nor does it take into account unicode character widths.
    #The small tweak is that this function does (as best as it can).
    #This function works with fansi well, but str.center does not.
    #NOTE (NOT an example): Justification for why I round torwards the left when centering:
    #     ⮤ 'a'.center(1,'+')
    #    ans = a
    #     ⮤ 'a'.center(2,'+')
    #    ans = a+
    #     ⮤ 'a'.center(3,'+')
    #    ans = +a+
    #     ⮤ 'a'.center(4,'+')
    #    ans = +a++
    #     ⮤ 'a'.center(5,'+')
    #    ans = ++a++
    delta_width=max(0,width-visible_string_length(string))
    delta_left =delta_width//2
    delta_right=delta_width-delta_left
    return fillchar*delta_left+string+fillchar*delta_right


def make_string_rectangular(string,align='left',fillchar=' '):
    #EXAMPLES:
    # ⮤ s='The mathematician\nPlotting his past relations\n"ex" and "why" axis'
    # ⮤ make_string_rectangular(s,'right',fillchar='-')
    #   ...MAKES...
    #     ----------The mathematician
    #     Plotting his past relations
    #     --------"ex" and "why" axis
    # ⮤ make_string_rectangular(s,'left',fillchar='-')
    #   ...MAKES...
    #     The mathematician----------
    #     Plotting his past relations
    #     "ex" and "why" axis--------
    # ⮤ make_string_rectangular(s,'center',fillchar='-')
    #   ...MAKES...
    #     ans = -----The mathematician-----
    #     Plotting his past relations
    #     ----"ex" and "why" axis----
    align_methods={'left':visible_string_ljust,
                  'right':visible_string_rjust,
                 'center':visible_string_center}
    assert len(fillchar)==1,'fillchar should be a length 1 string, but got fillchar='+repr(fillchar)
    assert align in align_methods,'String alignment must be left, right or center, but got align='+repr(align)
    align_method=align_methods[align]
    lines=line_split(string)
    width=string_width(string)
    return line_join(align_method(line,width,fillchar) for line in lines)
def string_is_rectangular(string):
    #Returns true if all lines of the string have the same length
    lines=line_split(string)
    max_line_length=string_width(string)
    return all(len(line)==max_line_length for line in lines)

def horizontally_concatenated_strings(*strings,rectangularize=False,fillchar=' '):
    #The fillchar parameter only matters if rectangularize is True
    #EXAMPLE:
    # ⮤ horizontally_concatenated_strings('Why\nHello\nThere!','My\nName\nIs\nBob','Pleased\nTo\nMeet\nYou!',rectangularize=False)
    #   ...MAKES...
    #      WhyMyPleased
    #      HelloNameTo
    #      There!IsMeet
    #      BobYou!
    #EXAMPLE:
    # ⮤ print(horizontally_concatenated_strings('Why\nHello\nThere!','My\nName\nIs\nBob','Pleased\nTo\nMeet\nYou!',rectangularize=True))
    # Why   My  Pleased
    # Hello NameTo
    # There!Is  Meet
    # Bob       You!
    #EXAMPLE:
    # ⮤ print(horizontally_concatenated_strings('a','b\nb','c\nc\nc',rectangularize=True))
    # abc
    #  bc
    #   c
    strings=delist(detuple(strings))
    for string in strings:
        assert isinstance(string,str),'Type '+repr(type(string))+' is not a string, and cannot be concatenated with this function'
    if rectangularize and strings:
        return string_transpose(vertically_concatenated_strings(*map(string_transpose,strings)))
    lines=[]
    for string in strings:
        for index,line in enumerate(line_split(string)):
            if index==len(lines):
                lines.append(line)
            else:
                lines[index]+=line
        if rectangularize:
            lines=line_split(make_string_rectangular(line_join(lines),align='left',fillchar=fillchar))
    return line_join(lines)
def vertically_concatenated_strings(*strings):
    #Pretty obvious what this does tbh, I dont see good reason for documenation here
    strings=delist(detuple(strings))
    return line_join(strings)

def wrap_string_to_width(string,width):
    #TODO: Make this work with visible_string_length so that unicode chars/ansi codes are supported
    #EXAMPLE:
    # ⮤ wrap_string_to_width('Hello\nWorld!',2)
    #    ans = He
    #    ll
    #    o
    #    Wo
    #    rl
    #    d!
    assert width>=0,'Cannot have negative width'
    lines=[]
    for line in line_split(string):
        lines+=split_into_sublists(line,width,strict=False,keep_remainder=True)
    return line_join(''.join(line)for line in lines)

def bordered_string(string,*,
                    weight=1,width     =None,     height=None,     left=None,     right=None,     bottom=None,     top=None,
                    fill=' ',width_fill=None,height_fill=None,left_fill=None,right_fill=None,bottom_fill=None,top_fill=None,
                    bottom_right_fill=None,bottom_left_fill=None,top_right_fill=None,top_left_fill=None):
        #NOTE: 99% of the time you should be using a rectangular string, as you can tell with string_is_rectangular
        #These examples showcase the usage of a NON-rectangular string to show why, but the rest is hopefully intuitive
        #EXAMPLES:
        # ⮤ bordered_string('Hello\nWorld!',fill='-',weight=3)
        #ans = -----------
        #-----------
        #-----------
        #---Hello---
        #---World!---
        #------------
        #------------
        #------------
        #⮤ bordered_string('Hello\nWorld!',fill='-',weight=3,top=0)
        #ans = ---Hello---
        #---World!---
        #------------
        #------------
        #------------
        #⮤ bordered_string('Hello\nWorld!',fill='-',weight=3,right=3)
        #ans = -----------
        #-----------
        #-----------
        #---Hello---
        #---World!---
        #------------
        #------------
        #------------
        #⮤ bordered_string('Hello\nWorld!',fill='-',weight=3,right=1)
        #ans = ---------
        #---------
        #---------
        #---Hello-
        #---World!-
        #----------
        #----------
        #----------
        #⮤ bordered_string('Hello\nWorld!',fill='-',bottom_fill='+',weight=3,right=1)
        #ans = ---------
        #---------
        #---------
        #---Hello-
        #---World!-
        #++++++++++
        #++++++++++
        #++++++++++
        #⮤ bordered_string('Hello\nWorld!',fill='-',bottom_fill='+',weight=3,right=1,bottom_right_fill='O')
        #ans = ---------
        #---------
        #---------
        #---Hello-
        #---World!-
        #+++++++++O
        #+++++++++O
        #+++++++++O
        #⮤ print(bordered_string('Hello\nWorld!',width_fill='│',height_fill='─',top_right_fill='┐',top_left_fill='┌',bottom_left_fill='└',bottom_right_fill='┘'))
        #┌─────┐
        #│Hello│
        #│World!│
        #└──────┘
        #⮤ print(bordered_string(make_string_rectangular('Hello\nWorld!'),width_fill='│',height_fill='─',top_right_fill='┐',top_left_fill='┌',bottom_left_fill='└',bottom_right_fill='┘'))
        #┌──────┐
        #│Hello │
        #│World!│
        #└──────┘
    width =weight if width  is None else width
    height=weight if height is None else height
    top   =height if top    is None else top
    bottom=height if bottom is None else bottom
    left  =width  if left   is None else left
    right =width  if right  is None else right
    #
    width_fill =fill        if width_fill  is None else width_fill
    height_fill=fill        if height_fill is None else height_fill
    top_fill   =height_fill if top_fill    is None else top_fill
    bottom_fill=height_fill if bottom_fill is None else bottom_fill
    left_fill  =width_fill  if left_fill   is None else left_fill
    right_fill =width_fill  if right_fill  is None else right_fill
    #
    bottom_right_fill = bottom_right_fill if bottom_right_fill is not None else bottom_fill
    bottom_left_fill  = bottom_left_fill  if bottom_left_fill  is not None else bottom_fill
    top_right_fill    = top_right_fill    if top_right_fill    is not None else top_fill
    top_left_fill     = top_left_fill     if top_left_fill     is not None else top_fill
    #
    lines=line_split(string)

    lines =[top_fill   *string_width(lines[ 0])]*top+lines
    lines+=[bottom_fill*string_width(lines[-1])]*bottom

    for index,line in list(enumerate(lines))[top:-bottom]:
        lines[index]=left_fill*left+line+right_fill*right

    #Corner fills:
    for index in range(top   ):                         lines[index]=top_left_fill   *left + lines[index] + top_right_fill   *right
    for index in range(bottom):index=len(lines)-index-1;lines[index]=bottom_left_fill*left + lines[index] + bottom_right_fill*right

    return line_join(lines)

def simple_boxed_string(string,align='center',chars='│─┐┌└┘'):
    #EXAMPLE:
    #⮤ s="I don't have any kids\n\nBut I like making dad jokes\n\nI am a faux pa"
    #⮤ print(simple_boxed_string(s,'center'))
    #┌───────────────────────────┐
    #│   I don't have any kids   │
    #│                           │
    #│But I like making dad jokes│
    #│                           │
    #│       I am a faux pa      │
    #└───────────────────────────┘
    #EXAMPLE That demonstrates not only this function but several other console-string functions in rp at once:
    #    def griddify(string_lists):
    #        def uniform_boxify(strings,height,width):
    #            strings=list(map(str                    ,strings))
    #            strings=list(map(make_string_rectangular,strings))
    #            strings=[pad_string_to_dims(string,height=height,width=width)for string in strings]
    #            return strings
    #        strings=list_pop(string_lists)
    #        widths =list(map(string_width ,strings))
    #        heights=list(map(string_height,strings))
    #        max_height=max(heights)
    #        max_width =max(widths )
    #        string_lists=[uniform_boxify(string_list,max_height,max_width) for string_list in string_lists]
    #        rows=[horizontally_concatenated_strings(string_list)for string_list in string_lists]
    #        grid=vertically_concatenated_strings(rows)
    #        return grid
    #    strings=[[fansi(wrap_string_to_width(random_namespace_hash(randint(10,30)),5),random_element(['green','blue','yellow','red','magenta','gray','cyan']),per_line=True)for _ in range(5)]for _ in range(10)]
    #    print(simple_boxed_string(griddify(strings)))
    return bordered_string(make_string_rectangular(string,align=align),
        width_fill       =chars[0],
        height_fill      =chars[1],
        top_right_fill   =chars[2],
        top_left_fill    =chars[3],
        bottom_left_fill =chars[4],
        bottom_right_fill=chars[5])

try:
    import re
    _strip_ansi_escapes=re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
except:pass
def strip_ansi_escapes(string):
    #Undoes anything fansi might do to a string
    #Code from https://www.tutorialspoint.com/How-can-I-remove-the-ANSI-escape-sequences-from-a-string-in-python#targetText=You%20can%20use%20regexes%20to,%5B%40-~%5D'.
    try:
        return _strip_ansi_escapes.sub('',string)
    except NameError:
        assert False,"Failed to import re upon booting rp"



def visible_string_length(string):
    #Give the visible string length when printed into a terminal.
    #Ignores ansi escape seqences and zero-width characters
    try:string=strip_ansi_escapes(string)
    except AssertionError:pass
    try:
        from wcwidth import wcswidth
        out=string.count('\n')
        for line in line_split(string):
            visible_line_length=wcswidth(line)
            assert visible_line_length!=-1#It means something went wrong
            out+=visible_line_length
        return out
    except (ImportError,AssertionError):
        return len(line)#A fallback in-case wcswidth doesn't work. This will give the wrong answer on things like fansi-output, but it's probably better than crashing because not all code needs fansi

def string_width(string):
    return max(map(visible_string_length,line_split(string)),default=0)
def string_height(string):
    return len(line_split(string))

def pad_string_to_dims(string,*,height,width,fill=' '):
    assert string_width (string)<=width
    assert string_height(string)<=height
    delta_width =width -string_width (string)
    delta_height=height-string_height(string)
    top   =delta_height//2
    left  =delta_width //2
    bottom=delta_height-top
    right =delta_width -left
    return bordered_string(string,fill=fill,left=left,right=right,top=top,bottom=bottom)

def prime_number_generator():
    #TODO: Add caching and optional starting points. Add an is_prime function
    p=[]
    try:
        #The fast, numba-accelerated version
        import numba
        @numba.jit()
        def primes():
            i=2
            while True:
                f=True
                for x in p:
                    if not i%x:
                        f=False
                        break
                if f:
                    p.append(i)
                    yield i
                i+=1
    except ImportError:
        #The slower, pure-python version
        def primes():
            p=[]
            i=2
            while True:
                if all(i%x for x in p):
                    yield i
                i+=1
    return primes()

def edit_distance(string_from, string_to):
    #There are faster implementations. I just took this from stackoverflow. This might be improved (use libraries that implement this in c) in the future if I feel the need for better performance
    #CODE FROM:  https://stackoverflow.com/questions/2460177/edit-distance-in-python
    s1,s2=string_from,string_to
    m=len(s1)+1
    n=len(s2)+1
    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
    return tbl[i,j]
levenshtein_distance=edit_distance#Synonyms, for now...

class Timeout:  
    #TODO: Make this work on windows (I won't think it will work on anything but UNIX because of the signal handling)
    # https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
    # Use this function to prevent a block of code from taking too long to run, else throw a TimeoutError
    #EXAMPLE:
    #   with timeout(seconds=3):
    #       time.sleep(4)
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        import signal
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):                                                                                  
        import signal                                                                                                            
        signal.alarm(0)
                                                                                                                                 
class TimeoutError(Exception):
    pass
def timeout(*timeout_args,**timeout_kwargs):
    #A timeout decorator that uses the Timeout class
    #To see documentation for this function's arguments, see the Timeout class's documentation

    #region Argument Validation
    assert not (len(timeout_args)==1 and callable(timeout_args[0])),'\'timeout\' is a decorator function. To use it as a decorator you must first pass it arguments.\nExample:\n\tGood:\n\t\t@timeout(1)\n\t\tdef f():pass\n\tBad:\n\t\t@timeout\n\t\tdef f():pass'
    try:
        with Timeout(*timeout_args,**timeout_kwargs):
            pass#This is just here to throw errors ahead of time in-case the user passes invalid arguments to the Timeout constructor
    except TypeError:
        assert False,'Bad arguments given to timeout, which were then passed to the Timeout class and gave a TypeError. Please see \'Timeout\'s arguments for more details, and use those same arguments in this decorator.'
    #endregion

    def wrapper(function):
        def wrapped(*args,**kwargs):
            with Timeout(*timeout_args,**timeout_kwargs):
                return function(*args,**kwargs)
        return wrapped
    return wrapper

#region English stuff (like plural to singular vice versa / words to numbers and vice versa etc etc)

_inflect_engine=None
def _get_inflect_engine():
    #Documentation: https://pypi.org/project/inflect/
    pip_import('inflect')
    import inflect
    global _inflect_engine
    if _inflect_engine is None:
        _inflect_engine=inflect.engine()
        _inflect_engine.classical()#Makes the difference between 'indexes' and 'indices'
    return _inflect_engine

def is_plural_noun(noun):
    #Return True if the given noun is in plural form, and False otherwise
    return not is_singular_noun(noun)

def is_singular_noun(noun):
    #Return True if the given noun is in singular form, and False otherwise
    return not bool(_get_inflect_engine().singular_noun(noun))#When a noun is singular already, and we pass it into the inflect library's singular_noun function, it returns False

def is_singular_noun_of(singular_word,plural_word):
    #Returns true if singular_word is the signular-form of plural_word
    return _get_inflect_engine().compare_nouns(singular_word,plural_word) and is_singular_noun(singular_word)

def is_plural_noun_of(plural_word,singular_word):
    #Returns true if plural_word is the plural-form of singular_word
    #
    return _get_inflect_engine().compare_nouns(plural_word,singular_word) and is_plural_noun(plural_word)

def plural_noun(noun,force=False):
    #Returns the plural form of a singular word
    #If force is true, it will not check to see if this noun is allready plural.
    #If force is true, we guarentee that the result is different from the  orignal
    #Right now this function uses a library called 'inflect'. "pip install inflect"
    #EXAMPLE:
    #    plural_noun("house")              -> "houses"
    #    plural_noun("houses",force=False) -> "houses"
    #    plural_noun("houses",force=True)  -> "housess"
    #    plural_noun("mouse")              -> "mice"
    #    plural_noun("die")                -> "dice"
    #    plural_noun("goose")              -> "geese"
    #    plural_noun("sheep")              -> "sheep"
    #    plural_noun("doggy")              -> "doggies"
    #    plural_noun("qwerty")             -> "qwerties" #Even works for made-up words
    #    plural_noun("spinach")            -> "spinaches"
    #    plural_noun("person")             -> "people"
    #    plural_noun("the_thing")          -> "the_things"
    #    plural_noun('wrq_qijjz_puppy')    -> "wrq_qijjz_puppies" #it's robust enough to handle conjoined variable names with multiple words in them'
    #    plural_noun("index")              -> "indices" #Actually, indices and indexes are both gramattically correct. This is controlled by the line with '.classical()' in _get_inflect_engine
    #    plural_noun("octopus")            -> "octopuses"  #lol not "octoputties", which is the TECHNICALLY CORRECT name...
    #
    #
    #EXAMPLE:
    #    #The 'force' option defaults to False to prevent this from happening:
    #    plural_noun("houses",force=True)  -> "housess"
    #    #If force is True, it can keep growing the word indefinately if we keep applying this function to it
    if not force and is_plural_noun(noun):
        return noun
    return _get_inflect_engine().plural_noun(noun)

def singular_noun(noun):
    #Returns the singular form of a plural word
    #EXAMPLE:
    #    singular_noun('houses')            -> 'house'
    #    singular_noun('mice')              -> 'mouse'
    #    singular_noun('sheep')             -> 'sheep'
    #    singular_noun('dice')              -> 'die'
    #    singular_noun('doggies')           -> 'doggy'
    #    singular_noun('qwerties')          -> 'qwerty'
    #    singular_noun('spinaches')         -> 'spinach'
    #    singular_noun('the_things')        -> 'the_thing'
    #    singular_noun('wrq_qijjz_puppies') -> 'wrq_qijjz_puppy'
    #    singular_noun('indexes')           -> 'index'
    #    singular_noun('octopuses')         -> 'octopus'
    #    singular_noun('houseses')          -> 'housese'
    #    singular_noun('geese')             -> 'goose'
    #    singular_noun('people')            -> 'person'
    return _get_inflect_engine().singular_noun(noun) or noun#If the noun is allready singular; leave it alone. If noun is allready singular, inflect will return "False" because it fails to turn your noun into singular form, causing this function to return the orignal word instead.

def number_to_words(number):
    #Returns the english representation of a number (can be an integer, negative, or even floating point. But can NOT be a complex number right now, because it will mess that up)
    #    number_to_words(0)           -> 'zero'
    #    number_to_words(1)           -> 'one'
    #    number_to_words(2)           -> 'two'
    #    number_to_words(3)           -> 'three'
    #    number_to_words(4)           -> 'four'
    #    number_to_words(5)           -> 'five'
    #    number_to_words(10)          -> 'ten'
    #    number_to_words(15)          -> 'fifteen'
    #    number_to_words(20)          -> 'twenty'
    #    number_to_words(25)          -> 'twenty-five'
    #    number_to_words(50)          -> 'fifty'
    #    number_to_words(78)          -> 'seventy-eight'
    #    number_to_words(92)          -> 'ninety-two'
    #    number_to_words(101)         -> 'one hundred and one'
    #    number_to_words(1000)        -> 'one thousand'
    #    number_to_words(1238)        -> 'one thousand, two hundred and thirty-eight'
    #    number_to_words(3498)        -> 'three thousand, four hundred and ninety-eight'
    #    number_to_words(12398)       -> 'twelve thousand, three hundred and ninety-eight'
    #    number_to_words(12938123)    -> 'twelve million, nine hundred and thirty-eight thousand, one hundred and twenty-three'
    #    number_to_words(-1)          -> 'negative one'
    #    number_to_words(-2)          -> 'negative two'
    #    number_to_words(-3)          -> 'negative three'
    #    number_to_words(-4)          -> 'negative four'
    #    number_to_words(-5)          -> 'negative five'
    #    number_to_words(-123)        -> 'negative one hundred and twenty-three'
    #    number_to_words(-123.4)      -> 'negative one hundred and twenty-three point four'
    #    number_to_words(1.1)         -> 'one point one'
    #    number_to_words(0.2)         -> 'zero point two'
    #    number_to_words(0.333333333) -> 'zero point three three three three three three three three three'
    #    number_to_words(0.25)        -> 'zero point two five'
    return _get_inflect_engine().number_to_words(number).replace('minus','negative')

def words_to_number(string):
    #I did my best to make this the inverse of number_to_words, and it works for most cases
    #Returns either an int or a float, depending on the context
    #Can handle decimal points and negative numbers, but NOT complex numbers
    #EXAMPLES:
    #    words_to_number("sixty-five"                                     ) = 65
    #    words_to_number("negative twenty-one"                            ) = -21
    #    words_to_number("thirty-eight"                                   ) = 38
    #    words_to_number("negative thirty-five"                           ) = -35
    #    words_to_number("five hundred and ninety-three"                  ) = 593
    #    words_to_number("negative thirty-six"                            ) = -36
    #    words_to_number("twenty-nine"                                    ) = 29
    #    words_to_number("six hundred and five"                           ) = 605
    #    words_to_number("two hundred and thirty-four"                    ) = 234
    #    words_to_number("negative twenty-six"                            ) = -26
    #    words_to_number("thirty"                                         ) = 30
    #    words_to_number("one thousand and seven"                         ) = 1007
    #    words_to_number("one thousand, two hundred and six"              ) = 1206
    #    words_to_number("one thousand, seven hundred and twenty-seven"   ) = 1727
    #    words_to_number("ninety-eight"                                   ) = 98
    #    words_to_number("zero point six one"                             ) = 0.61
    #    words_to_number("point 5"                                        ) = 0.5
    #    words_to_number("zero point five"                                ) = 0.5
    #    words_to_number("one over 2"                                     ) = 0.5
    #    words_to_number("one out of 2"                                   ) = 0.5
    #    words_to_number("one of two"                                     ) = 0.5
    #    words_to_number("1 / 2"                                          ) = 0.5
    #    words_to_number("zero point zero five"                           ) = 0.5
    #    words_to_number("zero point five one"                            ) = 0.51
    #    words_to_number("five point 4"                                   ) = 5.4
    #    words_to_number("five point six three"                           ) = 5.63
    #    words_to_number("0.6"                                            ) = 0.6
    #    words_to_number("0.6234"                                         ) = 0.6234
    #    words_to_number("five point six two"                             ) = 5.62
    #    words_to_number("negative 4"                                     ) = -4
    #    words_to_number("negative 4 point 4"                             ) = -4.4
    #    words_to_number("negative zero point 4"                          ) = -0.4
    #    words_to_number("negative zero point 4 five 6"                   ) = -0.456
    #    words_to_number("one . 2 3 4 5"                                  ) = 1.2345
    #    words_to_number("negative one . 2 3 4 five"                      ) = -1.2345
    #    words_to_number("negative 2 one . 2 3 4 five"                    ) = -1.2345
    #    words_to_number("negative 2 four one . 2 3 4 five"               ) = -5.2345
    #    words_to_number("negative four one  . 2 3 4 five"                ) = -5.2345
    #    words_to_number("negative four one one . 2 3 4 five"             ) = -5.2345
    #    words_to_number("negative twelve . 2 3 4 five"                   ) = -12.2345
    #    words_to_number("negative          2     one   . 2 34   five    ") = -1.2345
    #    words_to_number("negative 2 one . 2 3 4 five"                    ) = -1.2345
    #    words_to_number("543 point 2 2 2"                                ) = 543.222
    #    words_to_number("  minus 543 point 2 2 2"                        ) = -543.222
    #    words_to_number(" minus point 5"                                 ) = -0.5
    #    words_to_number("   minus     zero out      of 10   "            ) = 0
    #    words_to_number("   negative  zero out      of 10   "            ) = 0
    #    words_to_number("      -      zero out      of 10   "            ) = 0
    #    words_to_number("324.234"                                        ) = 324.234
    #    words_to_number("-23.234"                                        ) = -23.234
    #    words_to_number("235"                                            ) = 235
    #    words_to_number("-1"                                             ) = -1
    #    words_to_number("-.0"                                            ) = -0.0
    #    words_to_number("-0.1"                                           ) = -0.1
    from word2number import w2n #pip install word2number

    assert isinstance(string,str),'word2number error: please input a string. You gave me a '+repr(type(string))

    negative=False
    string=string.strip()
    string=string.replace('minus ','-')
    string=string.replace('negative ','-')
    if string.startswith('-'):
        #This word2number library can't natively handle 'negative 5' without crashing
        negative=True
        string=string[1:].strip()

    string=string.replace('/'           ,' over ')
    string=string.replace(' out of '    ,' over ')#For the next few lines that handle fractions...
    string=string.replace(' of '        ,' over ')
    string=string.replace(' divided by ',' over ')
    if ' over ' in string:
        assert string.count(' over ')==1,'word2number error: Cant have a fraction with two denominators, but was given '+repr(string)
        numerator,denominator=string.split(' over ')
        out = words_to_number(numerator)/words_to_number(denominator)
        if int(out)==out:
            return int(out)#'five out of 1' should return an integer, not a float
        return out if not negative else -out

    string=string.replace('.','point ')#Because words_to_number('234.324') should also work for the next few lines...
    if 'point ' in string:
        assert string.count('point ')==1,'word2number error: Cant have more than one decimal point in a number but string said \'point\' twice in '+repr(string)
        before_decimal,after_decimal=string.split('point ')
        before_decimal='0' if not before_decimal.strip() else before_decimal#In case we get 'point five' -> .5
        after_decimal=''.join(str(words_to_number(x)) for x in after_decimal.split()).strip()#after_decimal looks like "five one six two"...space separated digits
        out = float(str(words_to_number(before_decimal))+'.'+str(words_to_number(after_decimal)))
        return out if not negative else -out

    string=string.replace(',',' ')#Because without this, 'one thousand, one hundred and fifty five' returns the wrong answer
    out=w2n.word_to_num(string)

    return out if not negative else -out

#endregion



def connected_to_internet():
    #Return True if we're online, else False
    #Code from: https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python/21460844
    import socket
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def _string_pager_via_pypager(string):
    #Uses prompt-toolkit. But this can break if you have the wrong prompt toolkit version.
    pip_import('pypager')
    string=str(string)
    from pypager.source import StringSource
    from pypager.pager import Pager
    p = Pager()
    p.add_source(StringSource(text=string,lexer=None))
    p.run()

def _string_pager_via_click(string):
    click=pip_import('click')
    click.echo_via_pager(string)


def string_pager(string):
    #Uses a python-based pager, similar to the program 'less', where you can scroll and search through things
    #What is a pager? See: https://en.wikipedia.org/wiki/Terminal_pager
    #Useful for displaying gigantic outputs without printing the whole thing

    _string_pager_via_click(string)
    # _string_pager_via_pypager(string)#We're not using this one right now, because it uses prompt toolkit and might break if we have the wrong version installed


#region Mouse functions

#TODO: Build full keylogger functionality with pynput, including the ability to record entire mouse position/mouse click/keypress sequences and play them back again (for easy, full automation)

_pynput_mouse_controller=None
def _get_pynput_mouse_controller():
    global _pynput_mouse_controller
    if not _pynput_mouse_controller:
        pynput=pip_import('pynput')
        _pynput_mouse_controller=pynput.mouse.Controller()
    return _pynput_mouse_controller
def get_mouse_position():
    #Return (x,y) coordinates representing the position of the mouse cursor. (0,0) is the top left corner of the screen.
    #x is horizontal movement, y is vertical movement. More y is further down, more x is further right.
    #EXAMPLE: while True:print(get_mouse_position()) #Move your mouse around and watch the numbers change
    return _get_pynput_mouse_controller().position
def set_mouse_position(*position):
    #EXAMPLES:
    #    set_mouse_position( 23,40 ) #you can specify the coordinates as separate x,y arguments
    #    set_mouse_position(*get_mouse_position())
    #
    #    set_mouse_position((23,40)) #you can also specify the coordinates as a single tuple
    #    set_mouse_position( get_mouse_position())
    position=detuple(position)
    assert len(position)==2 and all(map(is_number,position)),'Invalid input: expected (x,y) pair but got position='+repr(position)
    x,y=position#I'm being explicit here for readability
    _get_pynput_mouse_controller().position=x,y
def record_mouse_positions(duration=1,rate=60):
    """
    #Record the mouse position for (duration) seconds, taking (rate) samples per second
    """
    assert rate>0
    assert duration>=0
    out=[]
    for _ in range(int(duration*rate)):
        out.append(get_mouse_position())
        sleep(1/rate)
    return out
def playback_mouse_positions(positions,rate=60):
    """
    #Play back a list of mouse positions at (rate) positions per second
    #EXAMPLE: playback_mouse_positions(record_mouse_positions(10)) #Move the mouse around for 10 seconds, then watch it play back again
    """
    assert is_iterable(positions)
    assert rate>0
    for position in positions:
        set_mouse_position(position)
        sleep(1/rate)

def mouse_left_click():
    """
    #Trigger the mouse's left click button
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().click(pynput.mouse.Button.left)
def mouse_right_click():
    """
    #Trigger the mouse's right click button
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().click(pynput.mouse.Button.right)
def mouse_middle_click():
    """
    #Trigger the mouse's middle click button
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().click(pynput.mouse.Button.middle)

def mouse_left_press():
    """
    #Press the mouse's left button
    #EXAMPLE: mouse_left_press();sleep(1);mouse_left_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().press(pynput.mouse.Button.left)
def mouse_right_press():
    """
    #Press the mouse's right button
    #EXAMPLE: mouse_right_press();sleep(1);mouse_right_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().press(pynput.mouse.Button.right)
def mouse_middle_press():
    """
    #Press the mouse's middle button
    #EXAMPLE: mouse_middle_press();sleep(1);mouse_middle_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().press(pynput.mouse.Button.middle)

def mouse_left_release():
    """
    #Release the mouse's left button
    #EXAMPLE: mouse_left_release();sleep(1);mouse_left_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().release(pynput.mouse.Button.left)
def mouse_right_release():
    """
    #Release the mouse's right button
    #EXAMPLE: mouse_right_release();sleep(1);mouse_right_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().release(pynput.mouse.Button.right)
def mouse_middle_release():
    """
    #Release the mouse's middle button
    #EXAMPLE: mouse_middle_release();sleep(1);mouse_middle_release()
    """
    pynput=pip_import('pynput')
    _get_pynput_mouse_controller().release(pynput.mouse.Button.middle)

#endregion

# def captured_stdout_as_string(callable):
#THIS IS COMMENTED OUT. IT WORKS TECHNICALLY, BUT ITS WAY TOO MESSY. It would be better to make it into a generator that yields each character then returns the output of callable.
#     #Takes a callable, returns a string containing the stdout of that callable
#     #EXAMPLE: captured_stdout_as_string(lambda:print("Hello, World!"))  --->  'Hello, World!\n'
#     from contextlib import redirect_stdout
#     import io
#     f = io.StringIO()
#     with redirect_stdout(f):
#         callable()
#     s = f.getvalue()
#     return s

def unicode_loading_bar(n,chars='▏▎▍▌▋▊▉█'):
    """
    #EXAMPLE 1: for _ in range(200):print(end='\r'+unicode_loading_bar(_));sleep(.05)
    #EXAMPLE 2:
    #    for _ in range(1500):
    #        sleep(1/30)#30fps
    #        x=_/1000#_ is between 0 and 1
    #        x**=2#Frequency increases over time
    #        x*=tau
    #        x*=10
    #        x=np.sin(x)
    #        x+=1#Make it all positive
    #        x*=20
    #        x*=8
    #        print(unicode_loading_bar(x))
    #THE ABOVE EXAMPLE PRINTS SOMETHING LIKE THIS:
    # ▊
    # █▊
    # ███▏
    # ████▌
    # ██████▏
    # ███████▊
    # █████████▍
    # ██████████▋
    # ███████████▋
    # ████████████▎
    # ████████████▌
    # ████████████▍
    # ███████████▊
    # ██████████▊
    # █████████▍
    # ███████▉
    # ██████▏
    # ████▋
    # ███
    # █▊
    # ▊
    # ▎
    # ▏
    # ▍
    # █
    # ██
    # ███▎
    """

    assert is_number(n),'Input assumption'
    assert n>=0,'Input assumption'
    assert isinstance(chars,str),'Input assumption'
    assert len(chars)>=1,'Input assumption'
    n=int(n)
    n=max(0,n)#Clip off negative numbers
    size=len(chars)
    output =n//size*chars[-1]
    output+=chars[n%size]
    return output

def get_scope(level=0,scope='locals'):
    """
    #Get the scope of n levels up from the current stack frame
    #Useful as a substitute for using globals(), locals() etc: you can specify exactly how many functions up you want to go
    #This function lets you do pretty crazy things that seem totally illegal to python scoping rules...
    #EXAMPLE:
    #   | --> hello='bonjour'
    #   |   2 def f():
    #   |   3     hello='hola'
    #   |   4     def g():
    #   |   5         hello='world'
    #   |   6         print(get_scope(0)['hello'])
    #   |   7         print(get_scope(1)['hello'])
    #   |   8         print(get_scope(2)['hello'])
    #   |   9     g()
    #   |  10 f()
    #   |world
    #   |hola
    #   |bonjour
    #A useful application of this function is for letting pseudo_terminal infer the locals() and globals() when embedding it without having to pass them manually through arguments. I got this idea from iPython's embed implementation, and thought it was pretty genius.
    """
    assert level>=0,'level cannot be negative'
    assert isinstance(level,int),'level must be an integer (fractions dont make any sense; you cant go up a fractional number of frames)'
    assert scope in {'locals','globals'},"scope must be either 'locals' or 'globals', but you gave scope="+repr(scope)
    import inspect
    frame=inspect.currentframe()
    frame=frame.f_back#Don't ever return the scope for this function; that's totally useless
    for _ in range(level):
        frame=frame.f_back
    return {'locals':frame.f_locals, 'globals':frame.f_globals}[scope]

_all_module_names=set()
def get_all_importable_module_names(from_cache=True):
    """
    #Returns a set of all names that you can use 'import <name>' on
    """
    if from_cache and _all_module_names:
        return _all_module_names
    import pkgutil
    for _,name,_ in pkgutil.iter_modules():
        _all_module_names.add(name)
    for name in sys.builtin_module_names:
        _all_module_names.add(name)
    return _all_module_names

def get_module_path_from_name(module_name):
    #Gets the file path of a module without importing it, given the module's name
    #EXAMPLES:
    #    ⮤ get_module_path_from_name('rp')
    #   ans = /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/rp/__init__.py
    #    ⮤ get_module_path_from_name('prompt_toolkit')
    #   ans = /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/prompt_toolkit/__init__.py
    #    ⮤ get_module_path_from_name('numpy')
    #   ans = /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/numpy/__init__.py
    #    ⮤ get_module_path_from_name('six')
    #   ans = /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/six.py
    #FROM: https://stackoverflow.com/questions/4693608/find-path-of-module-without-importing-in-python
    import importlib
    return importlib.util.find_spec(module_name).origin


def get_current_date():
    """
    #This is annoying to type...so I added this function as a bit of sugar.
    """
    import datetime
    return datetime.datetime.now()
def string_to_date(string):
    """
    # Given a date represented as a string, turn it into a datetime object and return it
    # https://stackoverflow.com/questions/466345/converting-string-into-datetime
    """
    timestring=pip_import('timestring')
    return timestring.Date(string).date

def open_file_with_default_application(path):
    """
    #Open a file or folder with the OS's default application
    #EXAMPLE: open_file_with_default_application('.') #Should open up a file browser with the current directory
    #Currently works on Mac, Windows, and Linux.
    #https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
    """
    import subprocess, os, platform
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', path))

def indent(text:str,indent:str='    '):
    return line_join(indent+line for line in line_split(text))



def mean(*x):
    """
    #EXAMPLES:
    # ⮤ mean(1,2,3)
    # ⮤ mean(1,2,3)
    #ans = 2.0
    # ⮤ mean(123)
    #ans = 123.0
    # ⮤ mean([1,5,2,4])
    #ans = 3.0
    """
    x=detuple(x)
    try:
        from numpy import mean
        return mean(x)
    except:
        from statistics import mean
        return mean(x)

def median(*x):
    """
    #EXAMPLES:
    # ⮤ median(1,1,1,5,9,9,9)
    #ans = 5
    # ⮤ median([1,1,1,5,9,9,9])
    #ans = 5
    # ⮤ median(['a','b','c','d','e'])
    #ans = c
    """
    x=detuple(x)
    from statistics import median
    return median(x)

def norm_cdf(x,mean=0,std=1):
    #normal cumulative distribution function
    #Given a value x, calculate the z-score and return the cumulative normal distribution of that z score
    #Note: this function can also take numpy vector inputs and return vector outputs!
    #EXAMPLE: bar_graph(norm_pdf(np.linspace(-3,3)))
    z=(x-mean)/std#Calculate the z-score
    pip_import('scipy')
    from scipy.stats import norm
    return norm.cdf(z)

def norm_pdf(x,mean=0,std=1):
    #normal probability density function
    #Given a value x, calculate the z-score and return the normal distribution density of that z score
    #Note: this function can also take numpy vector inputs and return vector outputs!
    #EXAMPLE: bar_graph(norm_pdf(np.linspace(-3,3)))
    z=(x-mean)/std#Calculate the z-score
    pip_import('scipy')
    from scipy.stats import norm
    return norm.pdf(z)

def inverse_norm_cdf(p,mean=0,std=1):
    #inverse normal cumulative distribution function
    #The inverse of the norm_pdf function (given a probability, find the x-value that made it)
    #Note: this function can also take numpy vector inputs and return vector outputs!
    #EXAMPLE: bar_graph(inverse_norm_cdf(np.linspace(0,1,1000)))
    pip_import('scipy')
    from scipy.stats import norm
    z=norm.ppf(p)#The z-score. https://bytes.com/topic/python/answers/478142-scipy-numpy-inverse-cumulative-normal
    x=z*std+mean
    return x

def download_url(url,path=None):
    #Download a file from a url and return the path it downloaded to. It no path is specified, it will choose one for you and return it (as a string)
    #EXAMPLE: open_file_with_default_application(download_url('https://i.imgur.com/qSmVyCo.jpg'))#Show a picture of a cat
    import requests
    assert isinstance(url,str),'url should be a string, but got type '+repr(type(url))
    if path is None:
        path=get_file_name(url)
    response = requests.get(url)
    open(path,'wb').write(response.content)
    return path

def debug(level=0):
    #Launch a debugger at 'level' frames up from the frame where you call this function.
    #Try to launch rp_ptpdb, but if we can't for whatever reason fallback to regular ol' pdb.
    #This doesn't use pudb, because pudb doesn't work on windows. Meanwhile, ptpdb runs on anything that can run prompt toolkit...making it a clear winner here.
    try:
        from rp.rp_ptpdb import set_trace_shallow
        # text_to_speech("CHUGGA CHUGGA MUGGA WUGGA")
        return set_trace_shallow(level=1+level)
    except:
        raise
        from pdb import set_trace
        # text_to_speech("OK AND THE OLD ONE")
        return set_trace()

try:from icecream import ic#This is a nice library...I reccomend it for debugging. It's really simple to use, too. EXAMPLE: a=1;b=2;ic(a,b)
except:pass

def is_a_matrix(matrix):
    matrix=as_numpy_array(matrix)
    return len(matrix.shape)==2

def is_a_square_matrix(matrix):
    matrix=as_numpy_array(matrix)
    return is_a_matrix(matrix) and matrix.shape[0]==matrix.shape[1]

def square_matrix_size(matrix):
    #Square matrices are of shape (N,N) where N is some integer
    #This function returns N
    #Lets you not have to choose between matrix.shape[0] and matrix.shape[1], which are both equivalent.
    matrix=as_numpy_array(matrix)
    assert is_a_square_matrix(matrix)
    return matrix.shape[0]

_prime_factors_cache={}
def prime_factors(number):
    #EXAMPLES:
    #     >>> prime_factors(23)
    #    ans = [23]
    #     >>> prime_factors(24)
    #    ans = [2, 2, 2, 3]
    #     >>> prime_factors(12)
    #    ans = [2, 2, 3]
    #     >>> prime_factors(720)
    #    ans = [2, 2, 2, 2, 3, 3, 5]
    #     >>> prime_factors(10)
    #    ans = [2, 5]
    #     >>> prime_factors(11)
    #    ans = [11]
    assert number>=1,'number must be a positive integer'
    assert int(number)==number,'number must be a positive integer'
    if number in _prime_factors_cache:
        return _prime_factors_cache[number]
    original_number=number
    out=[]
    try:
        pip_import('sympy')
        from sympy import primefactors
        primes=primefactors(number)#Much faster if available
    except:
        primes=prime_number_generator()#Still works, but this algorithm is slower than sympy's
    for prime in primes:
        while not number%prime:
            number//=prime
            out.append(prime)
        if prime>number:
            _prime_factors_cache[original_number]=out
            return out

def set_os_volume(percent):
    #Set your operating system's volume
    assert is_number(percent),'Volume percent should be a number, but got type '+repr(type(volume))
    assert 0<=percent<=100,'Volume percent should be between 0 and 100, but got volume = '+repr(volume)
    if currently_running_mac():
        pip_import('osascript').osascript('set volume output volume '+str(int(percent)))
    else:
        assert False,'Sorry, currently only MacOS is supported for setting the volume. This might change in the future.'

def fuzzy_string_match(string,target,*,case_sensitive=True):
    # >>> fuzzy_string_match('apha','alpha')
    #ans = True
    # >>> fuzzy_string_match('alpha','alpha')
    #ans = True
    # >>> fuzzy_string_match('aa','alpha')
    #ans = True
    # >>> fuzzy_string_match('aqa','alpha')
    #ans = False
    # >>> fuzzy_string_match('e','alpha')
    #ans = False
    # >>> fuzzy_string_match('h','alpha')
    #ans = False
    if not case_sensitive:
        string=string.lower()
        target=target.lower()

    import re
    pattern='.*'.join(re.escape(char) for char in string)
    pattern='.*'+pattern+'.*'
    return bool(re.fullmatch(pattern,target))

def get_source_code(object):
    #EXAMPLE:
    # >>> get_source_code(get_source_code)
    # ans = def get_source_code(object):
    #     import inspect
    #     return inspect.getsource(object)
    import inspect
    return inspect.getsource(object)


def get_english_synonyms_via_nltk(word):
    #This thing is really crappy...but also really funny xD
    #This thing belongs in death of the mind honestly...
    #Try get_bad_english_synonyms('spade') and it won't list shovel...
    #Try get_bad_english_synonyms('cat') and it lists 'vomit', 'spew'...
    #Try get_bad_english_synonyms('cheese') and it lists 'vomit', {'cheeseflower', 'Malva_sylvestris', 'cheese', 'tall_mallow', 'high_mallow'}
    #https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
    pip_import('nltk')
    from nltk.corpus import wordnet 
    synsets = wordnet.synsets(word)
    if not synsets:
        return set()
    synonym_sets = [{y.name() for y in x.lemmas()} for x in synsets]#Sets of synonyms for different definitions. This function ignores that. For example, given word=='dog', 'hot-dog' and 'canine' would be in different synonym_sets. But for the sake of simplicity, this function will return them all as one big set. If you want something more sophisticated, just use the nltk library or modify this function
    synonyms = set.union(*synonym_sets)
    return synonyms


@memoized
def _datamuse_words_request(query,word):
    #Uses https://www.datamuse.com/api/
    import requests,json
    response=requests.get('https://api.datamuse.com/words?'+query+'='+word)
    content=response.content.decode()
    content=json.loads(content)
    return [x['word'] for x in content]


def get_english_synonyms_via_datamuse(word):
    #EXAMPLE: get_english_synonyms_via_datamuse('food')
    #Uses https://www.datamuse.com/api/
    return _datamuse_words_request('rel_syn',word)

def get_english_related_words_via_datamuse(word):
    #EXAMPLE: get_english_synonyms_via_datamuse('food')
    #Uses https://www.datamuse.com/api/
    return _datamuse_words_request('ml',word)

def get_english_antonyms_via_datamuse(word):
    #EXAMPLE: get_english_synonyms_via_datamuse('good')
    #Uses https://www.datamuse.com/api/
    return _datamuse_words_request('rel_ant',word)

def get_english_rhymes_via_datamuse(word):
    #EXAMPLE: get_english_synonyms_via_datamuse('breath')#poppy: what rhymes with breath?
    #Uses https://www.datamuse.com/api/
    return _datamuse_words_request('rel_rhy',word)

def get_english_synonyms(word):
    try:
        return get_english_synonyms_via_datamuse(word)
    except:
        return get_english_synonyms_via_nltk(word)

from .tracetraptest import * #A few experimental debugging features. These things mostly need to be renamed.

@memoized
def fibonacci(n):
    assert n>=0
    if n<71:
        #Although this method is beautiful, it's not accurate past n=70 (due to floating point precision)
        #www.desmos.com/calculator/6q1csqqoqo
        #Calculate fibbonacci in constant time
        φ=.5+.5*5**.5#The golden ratio
        return round((φ**n-φ**(-n)*(-1)**n)/5**.5)
    else:
        #The less cool, but more accurate way
        #This method takes O(n) time (but it doesn't really matter for almost all realistic cases)
        a=0
        b=1
        for _ in range(n):
            a,b=b,a+b
        return a
@memoized
def inverse_fibonacci(n):
    #Runs in constant time
    #inverse_fibonacci(fibonacci(3415))==3415
    #inverse_fibonacci(fibonacci(1234))==1234
    #inverse_fibonacci(fibonacci(9471))==9471
    #inverse_fibonacci(fibonacci(  x ))==x for all non-negative integer x
    #https://stackoverflow.com/questions/5162780/an-inverse-fibonacci-algorithm
    #TODO: Make accurate past n=70, similar to how def fibonacci(n) was made (split into two cases)
    φ=.5+.5*5**.5#The golden ratio
    from math import log as ln
    return int(ln(n*5**.5+.5)/ln(φ))



if __name__ == "__main__":
    print(end='\r')
    pterm()

# endregion

# TODO: Mini-Terminal, Stereo audio recording/only initialize stream if using audio, Plot over images, error stack-printing extract from pseudo_terminal,
# TODO: See 'pseudolambdaidea' file
# TODO: Git auto-commit: see 'ryan_autogitter.py' file
# TODO: A more detailed pseudo_terminal history
# TODO: Make pseudo_temrinal open source!!!!
# TODO: Make a command for pseudo_terminal to kill the current command's execution. Make it so that we try to run all commands as a thread, but we kill those threads if we type "CANCEL" or "ABORT" or something so we dont need to close pseudo_terminal to cancel the process.
#
#
# class blank:# Just a placeholder for call_non_blank_parameters
#     pass
# def call_non_blank_parameters(f,*args,**kwargs):#will be used to streamline my use of te Đ
#     assert callable(f)
#     Đ_args=f.
#     args=[args]
