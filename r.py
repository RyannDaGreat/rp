# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
#THINGS TO DO BEFORE OFFICIAL RELEASE:
#   Rename "path" functions to "2d-somethings" idk what, but it conflicts with file-paths...
#   Rename "display" functions to "plot" functions. "display" functions should be very simple and library-agnostic, while plot can be matplotlib-based.
#   Remove useless functions, and categorize them. Probably should split into multiple files; but that's kinda messy...
#       These functions don't have to be removed from r.py, they just have to be deleted from rp.py (after using from r import *, use something like 'del useless_function')

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
import rp

# Places I want to access no matter where I launch r.py
# sys.path.append('/Users/Ryan/PycharmProjects/RyanBStandards_Python3.5')
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages')
# endregion
# region ［entuple， detuple］


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
    except Exception:
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
    except Exception:
        pass
    return x
# endregion
# region  rCode: ［itc‚ run‚ fog‚ scoop‚ seq_map‚ par_map‚ seq‚ par‚ rev‚ pam‚ identity，list_flatten，summation，product］
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
def run_func(f,*g,**kwg):  # Pop () ⟶ )(
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
    except Exception:
        try:
            scoop_value=copy(init_value)
        except Exception:
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
        except Exception:
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
# region ［list_flatten］
#FORMERLY CALLED list_pop (a bit of a misnomer; I know that now, after having taken CSE214.)
list_flatten=lambda list_2d:scoop(lambda old,new:list(old) + list(new),list_2d,[])
list_pop=list_flatten#Just because I'm used to list_pop, even though it doesn't make much sense lol. Thought of 'popping' the inner brackets of [[a,b],[c,d]] to [a,b,c,d] as if the inner brackets looked like bubbles to be popped. Has no relationship to popping an item off a stack or queue lol
# endregion
# region ［summation，product］
def product(x):
    # Useful because this literally uses the '*' operator over and over again instead of necessarily treating the elements as numbers.
    return scoop(lambda 𝓍,𝓎:𝓍 * 𝓎,x,x[0]) if len(x) else 1
    # assert is_iterable(x)
    # try:
    #     out=x[0]
    # except Exception:
    #     return 1# x has no indices
    # for y in x[1:]:
    #     out*=y
    # return out
def summation(x,start=None):
    # Useful because this literally uses the '+' operator over and over again instead of necessarily treating the elements as numbers.
    # list_flatten(l)≣summation(l)
    # sum(x,[])≣summation(x)
    # sum(x)≣summation(x)
    return scoop(lambda 𝓍,𝓎:𝓍 + 𝓎,x,start if start is not None else x[0]) if len(x) else start
    # assert is_iterable(x)
    # try:
    #     out=x[0]
    # except Exception:
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
    def reset_timer():
        nonlocal local_tic
        local_tic=time.time()
    local_toc.tic=reset_timer
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
    try:
        import os
        return os.getcwd()
    except FileNotFoundError as e:
        return '.' #A simple, but technically correct way to answer this question...will prevent errors in other places when the current directory is deleted...
        raise FileNotFoundError(str(e)+"\nPerhaps the directory you're working in no longer exists?")

def set_current_directory(path):
    import os
    os.chdir(path)

#THIS IS DEPRECATED IN FAVOR OF get_all_paths
# def get_all_file_names(file_name_ending: str = '',file_name_must_contain: str = '',folder_path: str = get_current_directory(),show_debug_narrative: bool = False):
#     # SUMMARY: This method returns a list of all file names files in 'folder_path' that meet the specifications set by 'file_name_ending' and 'file_name_must_contain'
#     # Leave file_name_ending blank to return all file names in the folder.
#     # To find all file names of a specific extension, make file_name_ending ﹦ '.jpg' or 'png' etc.
#     # Note: It does not matter if you have '.png' vs 'png'! It will return a list of all files whose name's ends…
#     #     …with file_name_ending (whether that comes from the file type extension or not). Note that you can use this to search…
#     #     …for specific types of file names that YOU made arbitrarily, like 'Apuppy.png','Bpuppy.png' ⟵ Can both be found with…
#     #     …file_name_ending ﹦ 'puppy.png'
#     # file_name_must_contain ⟶ all names in the output list must contain this character sequence
#     # show_debug_narrative ⟶ controls whether to print out details about what this function is doing that might help to debug something.
#     #     …By default this is disabled to avoid spamming the poor programmer who dares use this function.
#     # ;;::O(if)OOO
#     os.chdir(folder_path)
#     if show_debug_narrative:
#         print(get_all_file_names.__name__ + ": (Debug Narrative) Search Directory ﹦ " + folder_path)
#     output=[]
#     for file_name in glob.glob("*" + file_name_ending):
#         if file_name_must_contain in file_name:
#             output.append(file_name)  # I tried doing it with the '+' operator, but it returned a giant list of individual characters. This way works better.
#             if show_debug_narrative:
#                 print(get_all_file_names.__name__ + ": (Debug Narrative) Found '" + file_name + "'")
#     if show_debug_narrative:
#         print(get_all_file_names.__name__ + ' (Debug Narrative) Output ﹦ ' + str(output))
#     return output


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
        except Exception:
            return False
    return True
    # return sys.stdout.isatty()# There are probably more sophistacated, better ways to check, but I don't know them.
def terminal_supports_unicode():
    if currently_running_windows():# Try to enable unicode, but fail if we can't
        try:
            from win_unicode_console import enable
            enable()  # Trying to enable unicode characters on windows console
            return True
        except Exception:
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

def fansi(text_string,text_color=None,style=None,background_color=None,*,per_line=True):
    #TODO: Fix bug: PROBLEM is that '\n' not in fansi('Hello\n','gray')
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
    text_string=str(text_string)
    if per_line:
        lines=line_split(text_string)
        lines=[fansi(line,text_color,style,background_color,per_line=False) for line in lines]
        return line_join(lines)
    if _disable_fansi:
        return text_string#This is for terminals that dont support colors. I don't have a method wrapper for this yet, though.
    if not terminal_supports_ansi():# We cannot guarentee we have ANSI support; we might get ugly crap like '\[0Hello World\[0' or something ugly like that!
        return text_string# Don't format it; just leave it as-is
    if text_string=='':# Without this, print(fansi("",'blue')+'Hello World'
        return ''
    if isinstance(text_color,str):  # if text_color is a string, convert it into the correct integer and handle the associated exceptions
        text_colors={'black':0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'gray':7,'grey':7}
        try:
            text_color=text_colors[text_color.lower()]
        except Exception:
            print("ERROR: def fansi: input-error: text_color = '{0}' BUT '{0}' is not a valid key! Replacing text_color as None. Please choose from {1}".format(text_color,str(list(text_colors))))
            text_color=None
    if isinstance(style,str):  # if background_color is a string, convert it into the correct integer
        styles={'bold':1,'faded':2,'underlined':4,'blinking':5,'outlined':7}
        try:
            style=styles[style.lower()]  # I don't know what the other integers do.
        except Exception:
            print("ERROR: def fansi: input-error: style = '{0}' BUT '{0}' is not a valid key! Replacing style as None. Please choose from {1}".format(style,str(list(styles))))
            style=None
    if isinstance(background_color,str):  # if background_color is a string, convert it into the correct integer
        background_colors={'black':0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'gray':7,'grey':7}
        try:
            background_color=background_colors[background_color.lower()]
        except Exception:
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
    if currently_running_unix():
        print("ALSO PRINTING ALL 256 COLORS")
        #From https://superuser.com/questions/285381/how-does-the-tmux-color-palette-work/285400
        os.system('bash -c \'for i in {0..255}; do  printf "\\x1b[38;5;${i}mcolor%-5i\\x1b[0m" $i ; if ! (( ($i + 1 ) % 8 )); then echo ; fi ; done\'')
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
    except Exception:
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
            assert not (get_computer_name()=='glass' and running_in_ssh()) #This is a patch for Ryan Burgert's desktop computer, which doesn't like using the clipboard over ssh for some reason. 
            copy(string)
        except Exception:
            os.system("echo '%_s' | pbcopy" % string)
    except Exception:
        return
        fansi_print("string_to_clipboard: error: failed to copy a string to the clipboard",'red')

def string_from_clipboard():
    #Pastes the string from the clipboard and returns that value
    #First tries to paste the string from the system clipboard.
    #If that doesn't work, it falls back to reading your string from a local file called '.rp_local_clipboard'
    #If that doesn't work, it falls back to writing to a global variable called _local_clipboard_string
    try:
        from rp.Pyperclip import paste,copy
        assert not (get_computer_name()=='glass' and running_in_ssh()) #This is a patch for Ryan Burgert's desktop computer, which doesn't like using the clipboard over ssh for some reason. 
        return paste()
    except Exception:
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

#The following functions are very, very deprecated. Please don't use them.
# def width(image) -> int:
#     return len(image)
# def height(image) -> int:
#     return len(image[0])

def rgb_to_grayscale(image):  # A demonstrative implementation of this pair
    # Takes an image with multiple color channels
    # Takes a 3d tensor as an input (X,Y,RGB)
    # Outputs a matrix (X,Y ⋀ Grayscale value)
    # Calculated by taking the average of the three channels.
    try:
        image=as_numpy_array(image)
        return np.average(image,2).astype(image.dtype)  # Very fast if possible
    except Exception:
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
    def width(image) -> int:
        return len(image)
    def height(image) -> int:
        return len(image[0])
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
    :param image: a numpy array, preferably. But it can also handle pure-python list-of-lists if that fails.
    :param scale: can either be a scalar (get it? for SCALE? lol ok yeah that died quickly) or a tuple of integers to specify the new dimensions we want like (128,128)
    :param interp: ONLY APPLIES FOR numpy arrays! interp ∈ {'nearest','bilinear','bicubic','cubic'}
    :return: returns the resized image
    """
    assert interp in {'nearest','bilinear','bicubic'}
    if scale == 1:
        return image
    try:
        from scipy.misc import imresize
        return imresize(image,float(scale),interp)#We multiply scale by 100 because it's measured in percent
    except Exception:pass
    try:
        assert is_image(image)
        pip_import("skimage")
        from skimage.transform import resize
        if not isinstance(scale,tuple):
            height,width=image.shape[:2]
            height=int(height*scale)
            width =int(width *scale)
        else:
            height,width=scale

            if not height or not width:
                #If the user specifies (100,None) it means to rescale the image to a height of 100, and scale the width proportionally
                from math import ceil
                assert height or width
                if not height: height=ceil(get_image_height(image)/get_image_width (image)*width )
                if not width : width =ceil(get_image_width (image)/get_image_height(image)*height)
        # return resize(image,(height,width))
        order={'nearest':0,'bilinear':1,'bicubic':3}[interp]
        return resize(image,(height,width),order=order)
    except Exception:pass
    if is_number(scale):
        #Now we're in kinda bad janky territory...though it will still work...it will be slow because now its runnning in pure python...
        try:
            return cv_apply_affine_to_image(dog,scale_affine_2d(scale),output_resolution=scale)#Doesn't support 'interp'
        except Exception:pass
    return grid2d(int(len(image) * scale),int(len(image[0]) * scale),lambda x,y:image[int(x / scale)][int(y / scale)])#The slowest method of all...doesn't support 'interp'
# endregion
# region  xyrgb lists ⟷ image:［image_to_xyrgb_lists，xyrgb_lists_to_image，xyrgb_normalize，image_to_all_normalized_xy_rgb_training_pairs，extract_patches］     (Invertible Pair)

# try:from sklearn.feature_extraction.image import extract_patches
# except Exception:pass
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
    assert len(x) == len(y) == len(r) == len(g) == len(b),"An outside-noise assumption. If this assertion fails then there is something wrong with the input parameters --> this def is not to blame."
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
    if isinstance(x,set):
        x=list(x)
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
    except Exception:pass
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

def random_float_complex(exclusive_max: float = 1,inclusive_min=0) -> float:
    return random_float(exclusive_max=exclusive_max,inclusive_min=inclusive_min)+1j*random_float(exclusive_max=exclusive_max,inclusive_min=inclusive_min)

def random_floats(N,exclusive_max=1,inclusive_min=0):
    # Generate N uniformly distributed random floats
    # Example: random_floats(10)   ====   [0.547 0.516 0.421 0.698 0.732 0.885 0.947 0.668 0.857 0.237]
    # This function exists for convenience when using pseudo_terminal (wasn't really meant for use in long-term code, though it totally could be)
    assert N>=0 and N==int(N),'Cannot have a non-counting-number length: N='+repr(N)
    inclusive_min,exclusive_max=sorted([inclusive_min,exclusive_max])
    try:return (np.random.rand(N))*(exclusive_max-inclusive_min)+inclusive_min#Do this IFF we have numpy for convenience's sake
    except Exception:pass
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
    if isinstance(full_list,set):
        full_list=list(full_list)
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

def random_substring(string:str,length:int):
    assert len(string)>=length
    assert length>=0
    index=random_index(len(string)-length+1)
    return string[index:index+length]

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
    # print(parallel_batch(['a','b','c','d'],[1,2,3,4],batch_size=3)) --> [['c', 'b', 'd'], [3, 2, 4]]
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
def is_valid_url(url:str)->bool:
    #Return true iff the url string is syntactically valid
    from urllib.parse import urlparse
    if not isinstance(url,str):
        return False
    try:
        result=urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
# region  Saving/Loading Images: ［load_image，load_image_from_url，save_image，save_image_jpg］


_load_animated_gif_cache={}
def load_animated_gif(location,*,use_cache=True):
    #Location should be a url or a file path pointing to a GIF file
    #Loads an array of frames of an RGB animated GIF
    #Can load from a file or from a URL
    #EXAMPLE:
    #    while True:
    #       url = 'https://i.pinimg.com/originals/80/26/71/80267166501067a9da5e6b9412bdd9df.gif'
    #       for frame in load_animated_gif(url,use_cache=True):
    #           display_image(frame)
    #           sleep(1/20)
    if use_cache and location in _load_animated_gif_cache:
        return _load_animated_gif_cache[location]

    pip_import('PIL')
    from PIL import Image, ImageSequence

    if is_valid_url(location):
        try:
            from urllib.request import urlopen
            gif = Image.open(urlopen(location))
        except Exception as e:
            #Sometimes the above method doesn't work.
            #When it doesn't, often downloading the image and loading it from the hard drive will still work; so we'll try that before giving up.
            temp_file=temporary_file_path()
            try:
                download_url(location,temp_file)
                output=load_animated_gif(temp_file)
            finally:
                delete_file(temp_file)
            return output
    else:
        assert file_exists(location), 'No such file exists: ' + repr(location)
        gif = Image.open(location)

    frames = [as_numpy_array(frame.convert('RGB')) for frame in ImageSequence.Iterator(gif)]
    frames = as_numpy_array(frames)

    _load_animated_gif_cache[location]=frames

    return frames

_load_image_cache={}#TODO Test this and make sure it works. This is currently untested.



def load_image_from_clipboard():
    #Grab an image copied from your clipboard
    pip_import('PIL')
    from PIL import ImageGrab
    assert currently_running_windows() or currently_running_mac(),'load_image_from_clipboard() only works on Mac and Windows right now; sorry. This is because of PIL.'
    ans=ImageGrab.grabclipboard()
    path=temporary_file_path('.png')
    ans.save(path)
    ans=load_image(path)
    delete_file(path)
    return ans



def load_image(location,*,use_cache=False):
    #Automatically detect if location is a URL or a file path and try to smartly choose the appropriate function to load the image
    assert isinstance(location,str),'load_image error: location should be a string representing a URL or file path. However, location is not a string. type(location)=='+repr(type(location))+' and location=='+repr(location)
    if path_exists(location):
        location=get_absolute_path(location) #This is important for caching. ./image.jpg might mean different things when we're running in different directories.
    if use_cache and location in _load_image_cache and use_cache:
        return _load_image_cache[location].copy()
    if is_valid_url(location):
        out = load_image_from_url (location)
    else:
        out = load_image_from_file(location)
    if use_cache:
        #Only save to the cache if we're using use_cache, otherwise loading thousands of images with this method might run out of memory
        _load_image_cache[location]=out
    return out

def load_rgb_image(location,*,use_cache=False):
    #Like load_image, but makes sure there's no alpha channel
    #This function is really only here to save you from having to write it out every time
    return as_rgb_image(load_image(location,use_cache=use_cache))

class LazyLoadedImages:
    def __init__(self,image_paths:list,*args,**kwargs):
        self.image_paths=image_paths
        self.args=args
        self.kwargs=kwargs
    def __getitem__(self,i):
        image_path=self.image_paths[i]
        return load_image(image_path,*self.args,**self.kwargs)
    def __len__(self):
        return len(self.image_paths)

def load_images(*locations,use_cache=False,show_progress=False,strict=True):
    #Simply the plural form of load_image
    #This is much faster than using load_image sequentially because it's multithreaded. I've had performance boosts of up to 8x speed
    #This function will throw an error if any one of the images fails to load
    #If given a folder as the input path, will load all image files from that folder
    #The locations parameter:
    #    Can be a list    of images: load_images(['img1.png','img2.jpg','img3.bmp'])
    #    Can be a varargs of images: load_images( 'img1.png','img2.jpg','img3.bmp' )
    #    Can be a folder  of images: load_images( 'path/to/image/folder' )
    #The strict parameter controls what this function should do when an image fails to load. This is useful when loading a folder full of images, some of which might be corrupted.
    #    If strict==True, this function will throw an error if any one of the images fails to load
    #    If strict==False, this function will skip any images that fail to load (so you might not have as many images in the output as you did paths in the input)
    #    If strict==None, this function will replace any images that failed to load with 'None' instead of a numpy array. So the output might look like [image0. image1, image2, None, image4] where image1, image0 etc are numpy arrays

    assert strict in {True, False, None}, 'load_images: The \'strict\' parameter must be set to either True, False, or None. See the documentation for this function to see what that means.'

    if len(locations)==1:
        locations=locations[0]
    if isinstance(locations,str) and is_a_folder(locations):
        locations=get_all_paths(locations,include_files=True,include_folders=False)
        locations=[location for location in locations if is_image_file(location)]
        return load_images(locations,use_cache=use_cache,show_progress=show_progress,strict=strict)
    if isinstance(locations,str):
        locations=[locations]

    if show_progress:
        number_of_images_loaded=0
        show_time_remaining=eta(len(locations))
        start_time=gtoc()

    cancelled=False

    def _load_image(path):
        # print("PA",type(path),path)
        # assert isinstance(path,str)
        
        nonlocal cancelled
        if cancelled:
            if isinstance(cancelled,Exception):
                raise cancelled
            else:
                return None

        try:
            # print("JABBER",len(locations),flush=True)
            image=load_image(path,use_cache=use_cache)
            # print("JABBER",len(locations),flush=True)
        except Exception as e:
            if strict==True:
                cancelled=e
                raise
            else:
                image=None

        if cancelled:
            return image

        if show_progress:
            nonlocal number_of_images_loaded
            number_of_images_loaded+=1
            show_time_remaining(number_of_images_loaded)
        
        return image

    try:
        assert all(isinstance(x,str) for x in locations)
        images = par_map(_load_image,locations)#This is fast because it's multithreaded

        if strict is False:
            #When strict is False (as opposed to None), we skip any images that failed to load; meaning we exclude them from the output
            images = [image for image in images if image is not None]

    except KeyboardInterrupt:
        cancelled=True
        raise

    if show_progress:
        end_time=gtoc()
        elapsed_time=end_time-start_time
        sys.stdout.write('\033[2K\033[1G')#erase and go to beginning of line https://stackoverflow.com/questions/5290994/remove-and-replace-printed-items
        print('rp.load_images: Done! Loaded %i images in %.3f seconds'%(len(images),elapsed_time))#This is here because of the specifics of the eta function we're using to display progress

    return images


#     output=[]
#     for i,location in enumerate(locations):
#         image=load_image(location,use_cache=use_cache)
#         output.append(image)
#         if display_progress:
#             show_time_remaining(i)

#     return [load_image(location,use_cache=use_cache) for location in locations]

#def load_images_in_parallel(*locations,use_cache=False):
#    #This is like load_images, except it runs faster.
#    locations=delist(detuple(locations))
#    output=[]
#    show_time_remaining=eta(len(locations))

def load_image_from_file(file_name):
    #Can try opencv as a fallback if this ever breaks
    assert file_exists(file_name),'No such image file exists: '+repr(file_name)
    try               :return _load_image_from_file_via_imageio(file_name)#Imageio will not forget the alpha channel when loading png files
    except            :pass #Don't cry over spilled milk...if imageio didn't work we'll try the other libraries.
    try               :return _load_image_from_file_via_scipy  (file_name)#Expecting that scipy.misc.imread doesn't exist on the interpereter for whatever reason
    except ImportError:pass
    try               :return _load_image_from_file_via_opencv (file_name)#OpenCV is our last choice here, because when loading png files it forgets the alpha channel...
    except            :pass
    try               :return _load_image_from_file_via_PIL    (file_name)
    except            :raise
    # assert False,'rp.load_image_from_file: Failed to load image file: '+repr(file_name)

def _load_image_from_file_via_PIL(file_name):
    pip_import('PIL')
    from PIL import Image
    out = as_numpy_array(Image.open(file_name))
    assert is_image(out),'Sometimes when PIL fails to load an image it doesnt throw an exception, and returns a useless object. This might be one of those times.'
    return out

def _load_image_from_file_via_imageio(file_name):
    pip_import('imageio')
    from imageio import imread
    return imread(file_name)

def _load_image_from_file_via_scipy(file_name):
    from scipy.misc import imread
    return imread(file_name)

def _load_image_from_file_via_opencv(file_name):
    cv2=pip_import('cv2')
    image=cv2.imread(file_name, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    # image=cv2.imread(file_name) 
    if image is None:
        assert False,("OpenCV failed to load image file at the path: "+file_name)#By default, opencv doesn't raise an error when the file isn't found, and just returns None....which is dumb. It should act like scipy.misc.imread, which throws a FileNotFoundError when given an invalid path.
    return cv_bgr_rgb_swap(image)#OpenCV is really weird and doesn't use RGB: It uses BGR for some strange legacy reason. We have to swap the channels to make it useful.


def load_image_from_url(url: str):
    #Url should either be like http://website.com/image.png or like data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...
    #Returns a numpy image
    assert url.startswith('data:image') or is_valid_url(url),'load_image_from_url error: invalid url: '+repr(url)
    pip_import('PIL')
    from PIL import Image
    requests=pip_import('requests')
    from io import BytesIO
    response=requests.get(url)
    return np.add(Image.open(BytesIO(response.content)),0)  # Converts it to a numpy array by adding 0 to it.

def load_image_from_matplotlib(*,dpi:int=None,fig=None):
    #Return matplotlib's current display as an image
    #You can increase the DPI to get a higher resolution. Set it to something like 360 or higher.
    #Example:
    #    line_graph(random_ints(10))
    #    cv_imshow(load_image_from_matplotlib())
    import io
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    if fig is None: fig=plt.gcf()
    if dpi is None: dpi=fig.dpi
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def load_openexr_image(file_path:str):
    #Takes .exr image file with a depth map, and returns an RGBAZ image (where Z is depth, as opposed to an RGBA image.)
    #Because of the way .exr files work, the output of this function is not an image as defined by rp.is_image, because it has 5 channels (all floating point)
    #This function exists because load_image ignores the depth-map channel, which is important informatoin but is ignored by OpenCV's importer as well as Snowy's and all other libraries I've tried so far
    #This function requires a python package called 'openexr'. It can be annoying to install.
    pip_import('OpenEXR') # This package can be a bit of a pain-in-the-ass to get working; it requires apt-installs on Ubuntu and brew-installs on Mac. On ubuntu, try 'sudo apt install openexr ; sudo apt install libopenexr-dev' and if that fails try 'sudo apt remove libopenexr22' and try installing openexr and libopenexr-dev again
    
    assert file_exists(file_path),'File not found: '+file_path

    import OpenEXR, Imath, numpy
    
    #Below code adapted from: https://www.blender.org/forum/viewtopic.php?t=24549

    exrimage = OpenEXR.InputFile(file_path)

    dw = exrimage.header()['dataWindow']
    (width, height) = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    
    def fromstr(s):
      mat = numpy.fromstring(s, dtype=numpy.float16)
      mat = mat.reshape (height,width)
      return mat
    
    pt = Imath.PixelType(Imath.PixelType.HALF)
    (r, g, b, a, z) = [fromstr(s) for s in exrimage.channels('RGBAZ', pt)]
    return np.dstack((r,g,b,a,z)).astype(float)

_opencv_supported_image_formats='bmp dib exr hdr jp2 jpe jpeg jpg pbm pfm pgm pic png pnm ppm pxm ras sr tif tiff webp'.split()

def encode_image_to_bytes(image,filetype:str='.png',quality:int=100):
    #Returns the byte representation of an image file without actually saving it to your harddrive
    #TODO: Add PIL support too, in case cv2 fails. PIL can also do this.
    #TODO: Add image quality parameters for jpg 
    #Reference: https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
    #
    #EXAMPLE:
    #    ans='https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg'
    #    ans=load_image(ans)
    #    ans=encode_image_to_bytes(ans)
    #    ans=decode_image_from_bytes(ans)
    #    display_image(ans)


    filetype=filetype.lower() #Make filetype not case sensitive
    if not filetype.startswith('.'):
        #Allow filetype to be 'png' which gets turned into '.png'
        filetype='.'+filetype
    
    assert filetype[1:] in _opencv_supported_image_formats, 'Unsupported image format: '+repr(filetype)+', please choose from [.'+', .'.join(_opencv_supported_image_formats)+']'

    image=as_byte_image(image)
    image=as_rgb_image(image)
    image=cv_rgb_bgr_swap(image)
    
    pip_import('cv2')
    import cv2
    
    if filetype in 'jpg jpeg'.split():
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        success, encoded_image = cv2.imencode(filetype, image, encode_param)
    else:
        success, encoded_image = cv2.imencode(filetype, image)
    
    if not success:
        raise IOError('Failed to encode image to '+filetype+' bytes')

    return encoded_image.tobytes()

def decode_image_from_bytes(encoded_image:bytes):
    #Supports any filetype in r._opencv_supported_image_formats, including jpg, bmp, png, exr and tiff
    #TODO: Fix support for opencv, I suspect it will be faster.
    #
    #EXAMPLE:
    #    ans='https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg'
    #    ans=load_image(ans)
    #    ans=encode_image_to_bytes(ans)
    #    ans=decode_image_from_bytes(ans)
    #    display_image(ans)

    pip_import('PIL')

    from io import BytesIO
    from PIL import Image
    
    return np.array(Image.open(BytesIO(encoded_image)))

    # #TODO: Fix this if PIL is too slow
    #pip_import('cv2')
    #import cv2    
    #success, decoded_image = cv2.imdecode(encoded_image,cv2.IMREAD_ANYCOLOR)
    #if not success:
    #    raise IOError('Failed to decode image')
    #return decoded_image

def save_image(image,file_name=None,add_png_extension: bool = True):
    #Todo: Add support for imageio, which can also write images
    #Simply save a numpy image to a file.
    #The add_png_extension is annoying legacy stuff...sorry...it would break some of my other scripts to change that right now.
    #Provide several fallbacks to saving an image file
    if file_name==None:
        file_name=temporary_file_path('png')

    image=as_byte_image(image)#Suppress any warnings about losing data when coming from a float_image...that's a given, considering that png's only have one byte per color channel...

    if not folder_exists(get_parent_folder(file_name)):
        #If the specified path's folders don't exist, make them. Don't whine and throw errors.
        make_directory(get_parent_folder(file_name))

    try:
        from scipy.misc import imsave
    except Exception:
        try:
            from skimage.io import imsave
        except Exception:
            try:
                pip_import('cv2')
                from cv2 import imwrite
                imsave=lambda filename,data: imwrite(filename,cv_bgr_rgb_swap(as_rgba_image(as_byte_image(data))))
            except Exception:
                pass
    if file_name is None:
        file_name=str(millis()) + ".png"  # ⟵ Default image name
    if add_png_extension and not has_file_extension(file_name):#Save a png file by default
        file_name+=".png"
    imsave(file_name,image)
    return file_name

def save_images(images,paths:list=None,skip_overwrites=False,show_progress=False):
    #Save a list of images to a list of paths
    #If no paths are specified, the image names will be their hash values.
    #   In either case, this function returns a list of paths corresponsing to the image files that were saved
    #This function is faster than using save_image sequentially, as it uses multiple threads
    #If skip_overwrites is False, we won't overwrite any images that already have a given path name. This is especially useful when the image name is equal to it's hash code, as that can speed things up a lot (avoiding saving image files that don't need to be saved again saves you the time of having to write the same image file twice)
        
    if paths is None:
        paths=[None]*len(images)
        #if show_progress:
            #print("rp.save_images: No paths were specified for your %i images, so their names will be their hash values...calculating the image hash values...",end='',flush=True)
          #
        #paths=[str(handy_hash(image)) for image in images] #By defualt, give each image it's own unique name
#
        #if show_progress:
            #sys.stdout.write('\033[2K\033[1G')#erase and go to beginning of line https://stackoverflow.com/questions/5290994/remove-and-replace-printed-items

    if show_progress:
        number_of_images_saved=0
        show_time_remaining=eta(len(paths))
        start_time=gtoc()
    
    assert len(paths)==len(images),'Must have exactly one path to go with every image'
    assert all(map(is_image,images)),'All images must be images as defined by rp.is_image'
    assert all(isinstance(path,str) or path is None for path in paths),'All paths must be strings. They are where the images are saved to.'
    
    cancelled=False #This variable is used to make sure that all the other image-saving threads halt if the user of this function throws an exception, such as a KeyboardInterrupt (maybe it was taking too long and they got impatient...)

    def _save_image(image,path):

        if cancelled:
            return
        
        if path is None:
            path=str(handy_hash(image))+'.png'

        if skip_overwrites and path_exists(path):
            pass #We do nothing, we're skipping this image!
        else:    
            save_image(image,path)
        
        if cancelled:
            return

        if show_progress:
            nonlocal number_of_images_saved
            number_of_images_saved+=1
            show_time_remaining(number_of_images_saved)

        return path
        
    try:
        saved_paths = par_map(_save_image,images,paths)#This is fast because it's multithreaded
    except:
        cancelled=True
        raise

    if show_progress:
        end_time=gtoc()
        elapsed_time=end_time-start_time
        sys.stdout.write('\033[2K\033[1G')#erase and go to beginning of line https://stackoverflow.com/questions/5290994/remove-and-replace-printed-items
        print('rp.save_images: Done! Saved %i images in %.3f seconds'%(len(images),elapsed_time))#This is here because of the specifics of the eta function we're using to display progress

    return saved_paths

def temp_saved_image(image):
    #Return the path of an image, and return the path we saved it to
    #Originally used for google colab to display images nicely:
    #   from IPython.display import Image
    #   Image(temp_saved_image(‹some numpy image›,retina=True)) #<-- Displays image at FULL resolution, optimized for a retina monitor. 'retina=True' is totally optional, it  just looks really nice on my macbook.
    image_name="rp_temp_saved_image_"+random_namespace_hash(10)
    save_image(as_byte_image(as_rgba_image(as_float_image(image))),image_name)
    return image_name+'.png'

def save_image_to_imgur(image):
    #Takes an image, or an image path
    #Returns the url of the saved image
    #Note: This function can sometimes take up to 10 seconds, depending on the size of the input image
    assert is_image_file(image) or is_image(image),'The input image must either be a path to an image, or a numpy array representing an image'
    if isinstance(image,str):
        assert file_exists(image),'Cannot find a file at path '+repr(image)
        assert is_image_file(image),'There is a file, but its not an image: '+repr(path)
        image_path=image
        
        pip_import('imgurpython')
        from imgurpython import ImgurClient
        client=ImgurClient(client_id='e5b018ddc6db007',client_secret='2adb606c63637a04a55dfcbe7e929fb64f48b83d')#Please don't abuse this. There are limited uploads per month.
        response = client.upload_from_path(image_path, anon=True)
        return response['link']
    elif is_image(image):
        temp_image_path=temporary_file_path('.png')
        try:
            save_image(image,temp_image_path)
            return save_image_to_imgur(temp_image_path)
        finally:
            if file_exists(temp_image_path):
                delete_file(temp_image_path)
                
def save_image_jpg(image,path,*,quality=100,add_extension=True):
    #If add_extension is True, will add a '.jpg' or '.jpeg' extension to path IFF it doesn't allready end with such an extension (AKA 'a/b/c.jpg' -> 'a/b/c.jpg' BUT 'a/b/c.png' -> 'a/b/c.png.jpg')
    image=np.asarray(image)
    image=as_rgb_image(image)
    image=as_byte_image(image)
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
    (run_as_new_thread if run_as_thread else run_func)(fog(shell_command,("say -v " + voice + ((" -r " + str(rate_in_words_per_minute)) if rate_in_words_per_minute else"") + " " + text)))
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

_text_to_speech_via_google_sound_cache={}

#def text_to_sound(text):
#    #Takes a string, turns it into audio (a numpy vector with range [-1,1]) via google's text-to-speech api

def text_to_speech_via_google(text: str,voice='en',*,play_sound: bool = True,run_as_thread: bool = True):
    # This only works when online, and has a larger latency than the native OSX text-to-speech function
    # Favorite voices: da
    # region gTTS: My own version of https://github.com/pndurette/gTTS (I modified it so that it can actually play voices from other languages, which it couldn't do before. I put that functionality in a comment because I don't know how to use Github yet (Feb 2017))
    pip_import('requests')
    import re,requests
    pip_import('gtts_token')
    from gtts_token.gtts_token import Token
    mp3_file_path=temporary_file_path('mp3')
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

    if not (text,lang) in _text_to_speech_via_google_sound_cache:
        gTTS(text=text,lang=lang).save(mp3_file_path)  # gTTS is a class, and .save is a function of an instance of that class.
        _text_to_speech_via_google_sound_cache[text,lang]=load_sound_file(mp3_file_path,samplerate=True)
        
    samples,samplerate=_text_to_speech_via_google_sound_cache[text,lang]
    if play_sound:
        play_sound_from_samples(samples,samplerate)
    if file_exists(mp3_file_path):
        delete_file(mp3_file_path)

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
        if currently_running_mac():
            text_to_speech_via_apple(**kwargs)
        else:
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
        plt=get_plt()
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

def load_mp3_file(path):
    #Takes an mp3 file path, and returns a bunch of samples as a numpy array
    #Returns floating-point samples in the range [-1.0 , 1.0]
    pip_import('pydub')
    import pydub
    
    #A function I got from stackoverflow, minimally changed
    #https://stackoverflow.com/questions/53633177/how-to-read-a-mp3-audio-file-into-a-numpy-array-save-a-numpy-array-to-mp3
    #TODO: Use this same answer to create a save_mp3_file function
    def read(f, normalized=False):
        """MP3 to numpy array"""
        a = pydub.AudioSegment.from_mp3(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, a.channels))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y
    samplerate,samples= read(path,True)
    return samples,samplerate

def load_wav_file(path):
    #Takes a wav file path, and returns a bunch of samples as a numpy array
    #Returns floating-point samples in the range [-1.0 , 1.0]
    pip_import('scipy')
    import scipy.io.wavfile as wav
    samplerate,samples=wav.read(path)
    try:
        samples=np.ndarray.astype(samples,float) / np.iinfo(samples.dtype).max  # ⟶ All samples ∈ [-1,1]
    except Exception:
        pass
    return samples,samplerate

def adjust_samplerate(samples,original_samplerate:int,new_samplerate:int):
    #Used to change the samplerate of an audio clip (for example, from 9600hz to 44100hz)
    pip_install('scipy') 

    from scipy.signal import resample
    length_in_seconds=len(samples) / old_samplerate
    new_number_of_samples=int(length_in_seconds * new_samplerate)
    return resample(samples,num=new_number_of_samples)

def load_sound_file(file_path:str, samplerate:int=None):
    #Returns the contents of a sound file at file_path as a numpy array of floats in the range [-1, 1]
    #samplerate: either True, None or an int. If True, returns (samples, samplerate). If None, returns (samples at original samplerate). If int, returns (samples converted to samplerate).
    #TODO: Add conversion functions between stereo and mono, and add parameters to this function that use them

    #Make sure we support the requested file type
    assert isinstance(file_path,str),'r.load_sound_file: file_path must be a string, but you gave it a %s'%str(type(file_path))
    assert has_file_extension(file_path), 'r.load_sound_file: Your file doesnt have an extension, so I\'m not sure what to do with it. Your file path: %s. Supported filetypes include: %s'%(repr(file_path),', '.join(supported_filetypes))
    supported_filetypes=['mp3','wav']
    filetype=get_file_extension(file_path)
    assert filetype.lower() in supported_filetypes, 'r.load_sound_file: Sorry, but this function doesnt support %s files. It only supports the following filetypes: %s'%(filetype,', '.join(supported_filetypes))

    #Load the specific filetype
    if   filetype=='wav': samples, original_samplerate = load_wav_file(file_path)
    elif filetype=='mp3': samples, original_samplerate = load_mp3_file(file_path)

    #Handle the samplerate parameter
    if samplerate is True:
        return samples, original_samplerate
    elif samplerate is None:
        return samples
    elif is_number(samplerate):
        if samplerate!=original_samplerate:
            samples=adjust_samplerate(samples, original_samplerate, samplerate)
        return samples
    else:
        assert False,'r.load_sound_file: samplerate must either be True (which will return both the samples and the samplerate), None (which will return the audio at its original samplerate)elif , or an integer representing the desired samplerate.'

#def load_sound_file(file_path: str,samplerate_adjustment=False,override_extension: str = None) :
#    #TODO: Integrate this function with load_mp3_file
#    #TODO: Use the 'audioread' library to decode more than just .wav files, using more than just ffmpeg. This will make this function more robust. https://github.com/beetbox/audioread
#    # Opens sound files and turns them into numpy arrays! Unfortunately right now it only supports mp3 and wav files.
#    # Supports only .mp3 and .wav files.
#    # samplerate_adjustment:
#    # If true, your sound will be re-sampled to match the default_samplerate.
#    # If false, it will leave it as-is.
#    # If it'_s None, this function will output a tuple containing (the original sound, the original samplerate)
#    # Otherwise, it should be a number representing the desired samplerate it will re-sample your sound to match the given samplerate.
#    # Set override_extension to either 'mp3' or 'wav' to ignore the extension of the file name you gave it. For example, using override_extension='mp3' on 'music.wav' will force it to read music as an mp3 file instead.
#    if file_path.endswith(".mp3") or override_extension is not None and 'mp3' in override_extension:
#        return load_mp3_file(file_path)
#        file_path=mp3_to_wav(file_path)
#    else:
#        assert file_path.endswith(".wav") or 'wav' in override_extension,'sound_file_to_samples: ' + file_path + " appears to be neither an mp3 nor wav file." + " Try overriding the extension?" * (override_extension is None)
#    pip_import('scipy')
#    import scipy.io.wavfile as wav
#    samplerate,samples=wav.read(file_path)
#    try:
#        samples=np.ndarray.astype(samples,float) / np.iinfo(samples.dtype).max  # ⟶ All samples ∈ [-1,1]
#    except Exception:
#        pass

#    if samplerate_adjustment is False:
#        return samples
#    if samplerate_adjustment is None:
#        return samples,samplerate
#    new_samplerate=default_samplerate if samplerate_adjustment is True else samplerate_adjustment
#    if new_samplerate == samplerate:  # Don't waste time by performing unnecessary calculations.
#        return samples
#    from scipy.signal import resample
#    length_in_seconds=len(samples) / samplerate
#    new_number_of_samples=int(length_in_seconds * new_samplerate)
#    return resample(samples,num=new_number_of_samples)

def save_wav(samples,path,samplerate=None) -> None:  # Usually samples should be between -1 and 1
    pip_import('scipy')
    from scipy.io import wavfile
    if samples.dtype == np.float64:
        samples=samples.astype(np.float32)
    wavfile.write(path,samplerate or default_samplerate,samples)

default_samplerate=44100  # In (Hz ⨯ Sample). Used for all audio methods in the 'r' class.
def play_sound_from_samples(samples,samplerate=None,blocking=False,loop=False,**kwargs):
    # For stereo, use a np matrix
    # Example: psfs((x%100)/100 for x in range(100000))
    # Each sample should ∈ [-1,1] or else it will be clipped (if it wasn't clipped it would use modular arithmeti
    # c on the int16, which would be total garbage for sound)
    # Just like matlab'_s 'sound' method, except this one doesn't let you play sounds on top of one-another.
    try:
        pip_import('sounddevice')
    except OSError as error:
        if OSError.args==('PortAudio library not found',) and currently_running_linux:
            fansi_print("Error importing sounddevice; try running\n\tsudo apt-get install libportaudio2","red")
        raise
    if not running_in_ipython():
        import sounddevice
        wav_wave=np.array(np.minimum(2 ** 15 - 1,2 ** 15 * np.maximum(-1,np.minimum(1,np.matrix(list(samples)))).transpose()),dtype=np.int16)  # ⟵ Converts the samples into wav format. I tried int32 and above: None of them worked. 16-bit seems to be the highest resolution available.
        sounddevice.play(wav_wave,samplerate=samplerate or default_samplerate,blocking=blocking,loop=loop,**kwargs)
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
        if currently_running_linux():
            samples,samplerate=load_sound_file(path,samplerate=True)
            ic(samples,samplerate)
            play_sound_from_samples(samples,samplerate)

        elif currently_running_mac():
            play_sound_file_via_afplay(path)
            
        elif currently_running_windows():
            pip_import('playsound')
            from playsound import playsound
            playsound(path)# Worked on windows, but didn't work on my mac

    except Exception:
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
    return (run_as_new_thread if parallel else run_func)(shell_command,command)  # If parallel==True, returns the process so we can terminate it later.

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
    except Exception:
        pass
    # try:run_as_new_thread(shell_command,"killall com.apple.speech.speechsynthesisd")# ⟵ Works when I enter the command in terminal, but doesn't work when called from python! It'_s not very important atm though, so I'm not gonna waste time over it.
    # except Exception:pass
    try:
        import sounddevice
        sounddevice.stop()
    except Exception:
        pass
    try:
        import pygame
        pygame.mixer.stop()
    except Exception:
        pass

_default_wav_output_path='r.mp3_to_wav_temp.wav'  # Expect this file to be routinely overwritten.
def mp3_to_wav(mp3_file_path: str,wav_output_path: str = _default_wav_output_path,samplerate=None) -> str:
    # This is a audio file converter that converts mp3 files to wav files.
    # You must install 'lame' to use this function.
    # Saves a new wav file derived from the mp3 file you gave it.
    # shell_command('lame --decode '+mp3_file_path+" "+wav_output_path)# From https://gist.github.com/kscottz/5898352
    shell_command('lame ' + str(samplerate or default_samplerate) + ' -V 0 -h --decode ' + mp3_file_path + " " + wav_output_path)  # From https://gist.github.com/kscottz/5898352
    return wav_output_path
# endregionx
# region  Matplotlib: ［display_image，brutish_display_image，display_color_255，display_grayscale_image，line_graph，block，clf］

def _display_image_in_notebook_via_ipyplot(image):
    assert is_image(image)
    image=as_rgb_image(as_byte_image(image))
    image_width=get_image_width(image)
    pip_import('ipyplot').plot_images(images=[image],img_width=image_width,labels=[''])
    #pip_import('ipyplot').plot_images(images=[image],img_width=image_width,labels=[''],force_b64=True)#force_b64 is set to true so that ipyplot doesn't complain when we're in google colab: ' WARNING! Google Colab Environment detected!   If images are not displaying properly please try setting `base_64` param to `True`.' This has never been an issue, but the warning is annoying

def _display_image_in_notebook_via_ipython(image):
    import IPython
    return IPython.display.display_png(encode_image_to_bytes(image,'png'),raw=True)

def display_video(video,framerate=30):
    #Video can either be a string, or a video (aka a 4d tensor or iterable of images)
    if running_in_jupyter_notebook():
        display_video_in_notebook(video,framerate)
    else:
        #Todo: Add keyboard controls to play, pause, rewind, restart, next frame, prev frame, go to frame, adjust framerate
        #It would be much like display_image_slideshow (maybe even add functionality to display_image_slideshow and use that?)
        if isinstance(video,str):
            if not file_exists(video):
                raise FileNotFoundError(video)
            assert is_video_file(video),repr(video)+' is not a video file'
            video=load_video(video)
        for frame in video:
            display_image(frame)
            sleep(1/framerate) #Todo: Make this more accurate

def display_video_in_notebook(video,framerate=30):
    #Video can be either a string pointing to the path of a video, or the video itself. If it is the video itself, it will be embedded as a gif and displayed that way. 
    #This function can also display gif's and other video URL's we find on the web
    if isinstance(video,str):
        if file_exists(video) or is_valid_url(video):
            filetype=get_file_extension(video)

            video_filetypes='webm mp4 ogg'.split() #These are the only video filetypes officially supported by the HTML standard (see https://www.w3schools.com/html/html_media.asp)
            image_filetypes='gif'.split()

            assert filetype in video_filetypes+image_filetypes,'Invalid filetype: '+repr(video)+', video must be one of these types: '+str(video_filetypes+image_filetypes).replace("'",'')

            if filetype in video_filetypes:
                from IPython.display import Video,display_html
                if is_valid_url(video):
                    display_html(Video(url=video))
                else:
                    display_html(Video(data=video))
            else:
                assert filetype in image_filetypes
                from IPython.display import Image,display_html
                if is_valid_url(video):
                    display_html(Image(url=video))
                else:
                    display_html(Image(data=video))
        else:
            raise FileNotFoundError(video)
    else:
        display_embedded_video_in_notebook(video)

def display_embedded_video_in_notebook(video,framerate:int=30,filetype:str='gif'):
    #This will embed a video into the jupyter notebook you're using
    #Warning: This function is still experimental, and sometimes the videos are messed up a bit
    #Warning: This can make your notebooks very large, so please be careful to only use small videos with this function
    assert running_in_jupyter_notebook(),'display_embedded_video_in_notebook: This function only works in a jupyter notebook, such as Google Colab or Jupyter Lab'
    
    video_filetypes='webm mp4 ogg'.split() #These are the only video filetypes officially supported by the HTML standard (see https://www.w3schools.com/html/html_media.asp)
    image_filetypes='gif'.split()
    assert filetype in video_filetypes+image_filetypes,'Invalid filetype: '+repr(filetype)+', please choose from '+str(video_filetypes+image_filetypes).replace("'",'')
    
    from IPython.display import HTML, display_html
    from base64 import b64encode

    
    video_encoded = b64encode(encode_video_to_bytes(video,filetype,framerate=framerate)).decode()
    
    if filetype in video_filetypes:
        html = '<video controls alt="test" src="data:video/{0};base64,{1}">'.format(filetype, video_encoded)
    else:
        assert filetype in image_filetypes
        html = video_tag = '<img src="data:image/{0};base64,{1}" />'.format(filetype, video_encoded)
    
    display_html(html,raw=True)


def display_image_in_notebook(image):
    #Display an image at full resolution in a jupyter notebook

    #First method: Try to use iPython.display to do it directly. It's faster than ipyplot, and gives crisper images on my macbook.
    try: _display_image_in_notebook_via_ipython(image);return
    except Exception: pass

    #Second method: If that fails, try ipyplot. It gives good image displays as well.
    try: _display_image_in_notebook_via_ipyplot(image);return
    except Exception: raise

#def display_image_in_notebook(image):
#        #Display an image at full resolution in a jupyter notebook
#    assert is_image(image)
#    image=as_rgb_image(as_byte_image(image))
#    pip_import('ipyplot').plot_images([image],img_width=width(image))

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
        except Exception:pass
    if running_in_ipython():
        #Use the ipyplot library to display images at full resultion while in a jupyter notebook
        display_image_in_notebook(image)
        return
    elif module_exists('cv2'):
        try:
            #Personally, I think cv_imshow is better because it's faster.
            #If we have opencv installed, try to use that.
            #If not, then oh well - we'll just continue on and try matplotlib instead
            cv_imshow(image,wait=10 if not block else 10000000,label='rp.display_image()')
            return
        except Exception:#Only excepting exceptions because KeyboardInterrupt is a BaseException, and we want to be able to interrupt while True:display_image(load_image_from_webcam()) without tryiggering matplotlib
            pass #Oh well, we tried!
    global plt
    plt=get_plt()
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
    except Exception:
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

def display_image_slideshow(images='.',display=None,use_cache=True):
    #Enters an interactive image slideshow
    #Useful for exploring large folders/lists of images
    #images:
    #    images can be a path to a folder containing images
    #    images can be a list of images as defined by r.is_image()
    #    images can be a list of image file paths
    #display:
    #    if you set display=display_image_in_terminal, you can view the slideshow entirely over SSH
    #
    #EXAMPLE:
    #    display_image_slideshow(list(map(cv_text_to_image,'abcdefghijklmnopqrstuvwxyz')),display=display_image_in_terminal)
    #
    #EXAMPLE:
    #    images=line_split('''https://upload.wikimedia.org/wikipedia/commons/4/41/Left_side_of_Flying_Pigeon.jpg
    #    https://d17fnq9dkz9hgj.cloudfront.net/uploads/2020/04/shelter-dog-cropped-1.jpg
    #    https://i.pinimg.com/736x/4d/8e/cc/4d8ecc6967b4a3d475be5c4d881c4d9c.jpg
    #    https://www.dictionary.com/e/wp-content/uploads/2018/03/doge-300x300.jpg
    #    https://i.pinimg.com/originals/cb/e9/b4/cbe9b4280f390636e4d9432a02159528.jpg
    #    https://i.insider.com/5989fc4eefe3df1f008b48b9?width=1100&format=jpeg&auto=webp
    #    https://pyxis.nymag.com/v1/imgs/cd8/804/e0f612fa12d17e68e3d68ccf55f93cac4f-06-rick-morty.rsquare.w700.jpg
    #    https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iXusLDq1QUac/v1/1000x-1.jpg
    #    https://i0.wp.com/huskerchalktalk.com/wp-content/uploads/2016/09/chessboard.jpg?fit=698%2C400&ssl=1https://www.colorado.edu/mcdb/sites/default/files/styles/medium/public/article-image/logo-blm.png?itok=sbQ6vxqb''')
    #    display_image_slideshow(images,display_image_in_terminal)

    if display is None:
        if running_in_ssh() and currently_in_a_tty():
            display=display_image_in_terminal
        else:
            display=display_image

    if isinstance(images,str) and is_a_folder(images):
        images=get_all_paths(images,sort_by='number',include_files=True,include_folders=False)
        images=[path for path in images if is_image_file(path)]
    if len(images) and isinstance(images[0],str):
        assert all(isinstance(path,str) for path in images)
        images=[path for path in images if is_image_file(path) or is_valid_url(path)]
        #Todo: Make the images load lazily, but also somehow in parallel
        # images=load_images(images,use_cache=use_cache,strict=False)
        
    assert all(is_image(image) or is_image_file(image) for image in images)
    assert len(images)>0,'Must have at least one image to create a slideshow'

    index=0
    
    def display_help():
        print('r.image_slideshow: Displaying a slideshow of %i images'%len(images))
        print('    Use the following keymap:')
        print('        n: Go to the next image')
        print('        p: Go to the prev image')
        print('        r: Go to a random image')
        print('        +: Zoom In')
        print('        -: Zoom Out')
        print('        l: Pan Right')
        print('        k: Pan Up')
        print('        j: Pan Down')
        print('        h: Pan Left')
        print('        q: Quit the slideshow')
        print('        ?: Display this help text')
    
    display_help()

    skip_load=False
    origin_x=0
    origin_y=0
    scale=1
    scales={}

    def zoom_crop_origin(image):
        #TODO: Don't waste time when scale=1
        #TODO: Fix the issue where it resets if scale is too large (play aronud with zoom pan to see what I mean)
        if scale not in scales:
            #Do a bit of memoization to speed things up 
            if scale==1:
                scaled_image=image
            else:
                scaled_image=cv_resize_image(image,scale,interp='nearest')#Todo: Memoize this
            scales[scale]=scaled_image
        new_image=scales[scale]
        new_image=new_image[origin_y*scale:origin_y*scale+get_image_height(image), origin_x*scale:origin_x*scale+get_image_width(image)]
        return new_image
    
    while True:
        if not skip_load:
            index%=len(images)
            image=images[index]
            origin_x=0
            origin_y=0
            scale=1
            scales={}
        skip_load=False

        try:
            image_path=None
            if isinstance(image,str):
                image_path=image
                try:
                    image=load_image(image,use_cache=use_cache)
                except Exception:
                    print("Failed to load image: "+repr(image))
                    raise
            display(zoom_crop_origin(image))
            if scale!=1 or origin_x!=0 or origin_y!=0:
                print('Zoom Factor: %i   X: %i   Y:%i'%(scale,origin_x,origin_y))
            if image_path is not None:
                print("Image Location:",image_path)
            print('Displaying image #%i/%i, %ix%i'%(index+1,len(images),get_image_width(image),get_image_height(image)))
        except Exception as e:
            print('Failed to display image #%i/%i'%(index+1,len(images)))
            # print_stack_trace(e)
        
        if currently_in_a_tty():
            key=input_keypress()
        else:
            key=input('Enter a key: ')
            
        #Image Navigation
        if key=='n':
            index+=1
        elif key=='p':
            index-=1
        elif key=='r':
            index=random_index(images)

        #Panning and zooming
        elif key=='+':
            scale+=1
            scale=max(scale,1)
            skip_load=True
        elif key=='-':
            scale-=1
            scale=max(scale,1)
            skip_load=True
        elif key=='j':
            origin_y+=1
            origin_y+=int(max(1,get_image_height(image)/scale/10))
            origin_y=min(get_image_height(image)-1,max(origin_y,0))
            skip_load=True
        elif key=='k':
            origin_y-=1
            origin_y-=int(max(1,get_image_height(image)/scale/10))
            origin_y=min(get_image_height(image)-1,max(origin_y,0))
            skip_load=True
        elif key=='h':
            origin_x-=1
            origin_x-=int(max(1,get_image_width(image)/scale/10))
            origin_x=min(get_image_width(image)-1,max(origin_x,0))
            skip_load=True
        elif key=='l':
            origin_x+=1
            origin_x+=int(max(1,get_image_width(image)/scale/10))
            origin_x=min(get_image_width(image)-1,max(origin_x,0))
            skip_load=True

        #Exiting
        elif key=='q':
            break

        #Help
        elif key=='?':
            display_help()
    


def brutish_display_image(image):
    from copy import deepcopy
    global plt
    plt=get_plt()
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
    plt=get_plt()
    plt.imshow(matrix,cmap=plt.get_cmap('gray'),interpolation=pixel_interpolation_method_name)  # "cmap=plt.get_cmap('gray')" makes it show a black/white image instead of a color map.
    if refresh:
        plt.draw()
        plt.show(block=False)  # You can also use the r.block() method at any time if you want to make the plot usable.
        plt.pause(0.0001)  # This is nessecary, keep it here or it will crash. I don't know WHY its necessary, but empirically speaking it seems to be.

def bar_graph(values,*,width=.9,align='center',block=False,xlabel=None,ylabel=None,title=None,label_bars=False,**kwargs):
    #Create a bar graph with the given y-values
    #The 'values'     parameter is a list of bar heights. They should all be real numbers.
    #The 'width'      parameter sets the width of each bar
    #The 'align'      parameter sets whether the bars are to the center, right or left of each index
    #The 'label_bars' parameter, if true, will display numbers above each bar displaying their quantity. NOTE: This works best with integers, as opposed to floats!
    #EXAMPLE: bar_graph(randints(10))
    pip_import('matplotlib')
    plt=get_plt()

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
    plt.bar(x,values,width=width,align=align,**kwargs)

    if xlabel is not None: plt.xlabel(xlabel)
    if ylabel is not None: plt.ylabel(ylabel)
    if title  is not None: plt.title (title )
    
    if label_bars:
        for i in range(len(values)):
            plt.text(x=i,y=values[i]+1,s=str(values[i]),size=10,ha='center')
def line_graph_in_terminal(y):
    pip_import('plotille')
    import plotille
    print(plotille.plot(list(range(len(y))),y,bg=None,lc=None,width=get_terminal_width()-20,height=get_terminal_height()-13))

def line_graph(*y_values,
                show_dots: bool         = False,
                clf: bool               = True,
                ylabel: str             = None,
                xlabel: str             = None,
                use_dashed_lines: bool  = False,
                line_color: str         = None,
                title                   = None,
                block: bool             = False,
                background_image        = None,
                logx:float              = None,
                logy:float              = None) -> None:
    # This is mainly here as a simple reference for how to create a line-graph with matplotlib.pyplot.
    # There are plenty of options you can configure for it, such as the color of the line, label of the
    # axes etc. For more information on this, see http://matplotlib.org/users/pyplot_tutorial.html
    pip_import('matplotlib')
    global plt
    plt=get_plt()
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
    except Exception:  # y_values must have been an iterable of iterables, so we will graph each one on top of each other.
        # old_hold_value=plt.ishold() #This uses deprecated matplotlib stuff: https://github.com/matplotlib/matplotlib/issues/12337/
        # plt.hold(True)  # This lets us plot graphs on top of each other.
        for y in y_values:
            plot(y)
        # plt.hold(old_hold_value)

    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    if title:
        plt.title(title)

    if logy:
        if logy is True:
            logy=2
        plt.yscale('log',base=logy)

    if logx:
        if logx is True:
            logx=2
        plt.xscale('log',base=logx)

    plt.draw()
    display_update(block=block)
    plt.pause(.001)


def display_polygon(path,*,
                    filled    =True,
                    fill_color=None,
                    line_width=1,
                    line_style='solid',
                    line_color=None,
                    clear     =False,
                    block     =False,
                    alpha     =1):
    #Uses matplotlib
    #Parameters:
        #line_width: The width of the border around the polygon (set to 0 for no border)
        #line_style: Please see https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
        #line_color: The color of the outline aka border of the polygon (like (1,0,0) for red, etc)
        #
        #filled    : boolean whether we should fill the object or just use an outline
        #fill_color: The color of the area of the polygon (like (1,0,0) for red, etc)
        #
        #alpha     : The transparency value (1 is opaque, 0 is completely transparent)
        #
        #clear     : Whether we should clear the plot before drawing this polygon
        #block     : True for an interactive plot that blocks the current python code; False to display immediately and continue python code; None to just plot it and skip the displaying step (which is faster and useful if you want to plot a lot of polygons at once)
    #EXAMPLE: display_polygon(random_floats_complex(5),alpha=.5)
    pip_import('matplotlib')
    from matplotlib.patches import Polygon
    from matplotlib import pyplot as plt
    
    path=as_points_array(path)

    if fill_color is None: fill_color=random_rgb_float_color()
    
    if clear:    
        plt.clf()

    if len(path): #Prevent edge case errors
        #Setting up the polygon
        polygon=Polygon(path, True)
        
        polygon.set_fill     (filled    )
        polygon.set_alpha    (alpha     )
    if clear:    
        plt.clf()

    if len(path): #Prevent edge case errors
        #Setting up the polygon
        polygon=Polygon(path, True)
        
        polygon.set_fill     (filled    )
        polygon.set_alpha    (alpha     )
        #Setting up the polygon
        polygon=Polygon(path, True)
        
        polygon.set_fill     (filled    )
        polygon.set_alpha    (alpha     )
        polygon.set_facecolor(fill_color)
        polygon.set_linewidth(line_width)
        polygon.set_linestyle(line_style)
        polygon.set_edgecolor(line_color)
        
        plt.axes().add_patch(polygon)

        #Autoscaling
        bounding_points=np.row_stack((np.max(path,axis=0),np.min(path,axis=0)))#Get two points representing the bounding box of path
        plt.plot(*bounding_points,marker='o')[0].set_visible(False)#Plot two invisible points on this bounding box, so that matplotlib will automatically rescale to accomidate whatever path you gave it

    #Displaying
    if block is not None:
        plt.show(block=block)
        if not block:
            plt.pause(.01)

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

def display_update(block=False,time=.01):
    #This should be preferred over the older block() function shown above
    #Note: If time is too low, you can try setting it to a higher value
    pip_import('matplotlib')
    if block is None:
        return#A convention that if block is "None" for some display function, it means we don't actually want to display it right away (for speed purposes, mostly)
    import matplotlib.pyplot as plt
    if block:
        plt.show(block=block)
    else:
        plt.gcf().canvas.blit()
        plt.pause(time)
update_display=display_update#Synonyms

def display_clear():
    pip_import('matplotlib')
    import matplotlib.pyplot as plt
    plt.gcf().clf()
clear_display=display_clear#Synonyms

def clf():
    pip_import('matplotlib')
    plt.clf()
# endregion
# region Min/Max Indices/Elements:［min_valued_indices，max_valued_indices，min_valued_elements，max_valued_elements，max_valued_index，min_valued_index］
def _minmax_indices(l,f=None,key=None)->list:    
    if len(l) == 0:
        return [] # An empty list
    # A helper method for the min/max methods below. f is either 'min' or 'max'
    if isinstance(l,dict):
        return matching_keys(f(l.values(),key=key),l,key=key)
    else:
        return matching_indices(f(l,key=key),l,key=key)

def min_valued_indices(l,key=None)->list:
    # Returns the indices with the minimum-valued elements
    #TODO: Make this work properly with dicts, like max_valued_index does
    return _minmax_indices(l,min,key=key)
def max_valued_indices(l,key=None)->list:
    # Returns the indices with the maximum-valued elements
    #TODO: Make this work properly with dicts, like min_valued_index does
    #EXAMPLE:
    #     >>> max_valued_indices({'a':123,'b':23424})
    #    ans = ['b']
    return _minmax_indices(l,max,key=key)

def min_valued_elements(l,key=None):
    # Returns the elements with the smallest values
    return gather(l,min_valued_indices(l,key=key))
def max_valued_elements(l,key=None):
    # Returns the elements with the largest values
    return gather(l,max_valued_indices(l,key=key))

def max_valued_index(l,key=None):
    if isinstance(l,dict):
        #Let this function work with dictionaries, such that max_valued_index({'a':1,'b':3,'c':2})=='b'
        inverted_dict=invert_dict(l)
        return inverted_dict[max(inverted_dict,key=key)]

    return list(l).index(max(l))  # Gets the index of the maximum value in list 'l'. This is a useful def by rCode standards because it references 'l' twice.
def min_valued_index(l):
    if isinstance(l,dict):
        #Let this function work with dictionaries, such that max_valued_index({'a':1,'b':3,'c':2})=='b'
        inverted_dict=invert_dict(l)
        return inverted_dict[min(inverted_dict,key=key)]

    return list(l).index(min(l))  # Gets the index of the minimum value in list 'l'. This is a useful def by rCode standards because it references 'l' twice.
# endregion
# region  Blend≣Lerp/sign: ［blend，iblend，lerp，interp，linterp］
def blend(𝓍,𝓎,α):  # Also known as 'lerp'
    return (1 - α) * 𝓍 + α * 𝓎  # More α --> More 𝓎 ⋀ Less 𝓍
def iblend(z,𝓍,𝓎):  # iblend≣inverse blend. Solves for α， given 𝓏﹦blend(𝓍,𝓎,α)
    z-=𝓍
    z/=𝓎-𝓍
    return z
def interp(x,x0,x1,y0,y1):  # 2 point interpolation
    return (x - x0) / (x1 - x0) * (y1 - y0) + y0  # https://www.desmos.com/calculator/bqpv7tfvpy
def linterp(values:list,index:float,*,cyclic=False):# Where l is a list or vector etc
    #Linearly inerpolation between different values with fractional indices
    #This is written in pure python, so any values that implement addition, subtraction and multiplication will work
    #   (This includes floats, vectors, and even images)
    #Note that linterp(values,some_integer) == values[some_integer] for any valid integer some_integer
    #EXAMPLE: INTERPOLATING VECTORS
    #     ➤ as_numpy_array([ linterp( as_numpy_array([[0,1], [0,0], [1,0]]), index)   for   index   in   [0, .5, 1, 1.5, 2] ])
    #     ans = [[0.  1. ]
    #            [0.  0.5]
    #            [0.  0. ]
    #            [0.5 0. ]
    #            [1.  0. ]]
    #
    #EXAMPLE: INTERPOLATING IMAGES
    #    mountain=load_image('https://cdn.britannica.com/67/19367-050-885866B4/Valley-Taurus-Mountains-Turkey.jpg')
    #    chicago=load_image('https://pbs.twimg.com/media/EeqFCjvWkAI-rv_.jpg')
    #    doggy=load_image('https://s3-prod.dogtopia.com/wp-content/uploads/sites/142/2016/05/small-dog-at-doggy-daycare-birmingham-570x380.jpg')
    #    images=[resize_image(image,(256,256)) for image in [mountain,chicago,doggy]]
#Wit#h cyclic=True, it will loop through the images
    #    for index in np.linspace(0,10,num=100):
    #        frame=linterp(images,index,cyclic=True)
    #        display_image(frame)
    #        sleep(1/30)
#Wit#h cyclic=False, it will play the animation only once
    #    for index in np.linspace(0,2,num=100):
    #        frame=linterp(images,index,cyclic=False)
    #        display_image(frame)
    #        sleep(1/30)

    assert is_number(index),'The \'index\' parameter should be a single number (which can be a float, but doesnt have to be), but got type '+str(type(index))
    assert is_iterable(values),'The \'values\' parameter should be a list of values you\'d like to interpolate between, but type '+str(type(index))+' is not iterable and does not have numerical indices'
    l=values
    x=index
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
def matching_keys(x,d:dict,check=lambda x,y:x==y,key=None)->list:
    # Retuns a list [x0,x1,...] such that for all xi, d[xi]=x
    #EXAMPLE:
    #   matching_keys('a',{3:'c','q':'a',():'a'}) ==== ['q',()]
    assert isinstance(d,dict)
    if key is None:key=identity
    out=[]
    for key,value in d.items():
        if key(value)==key(x):
            out.append(key)
    return out
    
def matching_indices(x,l,check=lambda x,y:x == y,key=None)->list:
    # Retuns a list [x0,x1,...] such that for all xi, l[xi]=x
    #EXAMPLE:
    #   matching_indices('a',['a','b','c','a','t']) ==== [0,4]
    #   matching_indices('a','abcat') ==== [0,4]
    #   matching_indices('a',{3:'c','q':'a',():'a'}) ==== ['q',()]
    # Returns the matching indices of element 'x' in list 'l'

    if key is None:key=identity

    if isinstance(l,dict):
        #Let this function work for dicts too
        return matching_keys(x,l,check=check)

    out=[]
    for i,y in enumerate(l):
        if check(key(x),key(y)):
            out.append(i)
    return out
def gather(iterable,*indices):
    # indices ∈ list of integers
    indices=detuple(indices)
    indices=delist(indices)
    assert is_iterable(iterable),"The 'iterable' parameter you fed in is not an iterable!"
    assert is_iterable(indices),"You need to feed in a list of indices, not just a single index.  indices == " + str(indices)
    return [iterable[i] for i in indices]  # ≣list(map(lambda i:iterable[i],indices))
def pop_gather(x,*indices):
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
    indices=detuple(indices)
    out=gather(x,indices)
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
default_display_key_color=lambda x123:fansi(x123,'cyan')
default_display_arrow_color=lambda x123:fansi(x123,'green')
default_display_value_color=lambda x123:fansi(x123,'blue')
def display_dict(d: dict,
                 key_color      = default_display_key_color,
                 arrow_color    = default_display_arrow_color,
                 value_color    = default_display_value_color,
                 clip_width     = False,
                 post_processor = identity,
                 key_sorter     = sorted,
                 print_it       = True,
                 arrow          = " --> "
                 # arrow          = " ⟶  "
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
                 key_color   = default_display_key_color,
                 arrow_color = default_display_arrow_color,
                 value_color = default_display_value_color,
                 print_it    = True) -> None:
    # also works with tuples etc
    return display_dict(d=list_to_index_dict(l),key_color=key_color,arrow_color=arrow_color,value_color=value_color,print_it=print_it)
# endregion
# region  'youtube_dl'﹣dependent methods: ［rip_music，rip_info］
# noinspection SpellCheckingInspection

default_rip_music_output_filename="rip_music_temp"
def rip_music(URL: str,output_filename: str = default_rip_music_output_filename,desired_output_extension: str = 'wav',quiet=False):
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

    #This region is commented out because it's broken
            ## from rp.r_credentials import default_gmail_address   # ⟵ The email address we will send emails from and whose inbox we will check in the methods below.
            ## from rp.r_credentials import default_gmail_password  # ⟵ Please don't be an asshole: Don't steal this account! This is meant for free use!
            # default_gmail_address=''
            # default_gmail_password=''
            # default_max_ↈ_emails=100  # ≣ _default_max_number_of_emails to go through in the gmail_inbox_summary method.
            # def send_gmail_email(recipientⳆrecipients,subject: str = "",body: str = "",gmail_address: str = default_gmail_address,password: str = default_gmail_password,attachmentⳆattachments=None,shutup=False):
            #     # For attachmentⳆattachments, include either a single string or iterable of strings containing file paths that you'd like to upload and send.
            #     # param recipientⳆrecipients: Can be either a string or a list of strings: all the emails we will be sending this message to.
            #     # Heavily modified but originally from https://www.linkedin.com/pulse/python-script-send-email-attachment-using-your-gmail-account-singh
            #     from email.mime.text import MIMEText
            #     from email.mime.application import MIMEApplication
            #     from email.mime.multipart import MIMEMultipart
            #     import smtplib
            #     emaillist=[x.strip().split(',') for x in enlist(recipientⳆrecipients)]
            #     msg=MIMEMultipart()
            #     msg['Subject']=subject
            #     # msg['From']='presidentstanely@gmail.com'# ⟵       I couldn't find any visible effect from keeping this active, so I decided to remove it.
            #     # msg['Reply-to']='ryancentralorg@gmail.com' # ⟵    I couldn't find any visible effect from keeping this active, so I decided to remove it.
            #     # msg.preamble='Multipart massage mushrooms.\n' # ⟵ I couldn't find any visible effect from keeping this active, so I decided to remove it.
            #     msg.attach(MIMEText(body))
            #     if attachmentⳆattachments:
            #         for filename in enlist(attachmentⳆattachments):
            #             assert isinstance(filename,str)  # These should be file paths.
            #             part=MIMEApplication(open(filename,"rb").read())
            #             part.add_header('Content-Disposition','attachment',filename=filename)  # ⟵ I tested getting rid of this line. If you get rid of the line, it simply lists the attachment as a file on the bottom of the email, …
            #             # … and wouldn't show (for example) an image. With it, though, the image is displayed. Also, for files it really can't display (like .py files), it will simply act as if this line weren't here and won't cause any sort of error.
            #             msg.attach(part)
            #     try:
            #         with smtplib.SMTP("smtp.gmail.com:587") as server:
            #             server.ehlo()
            #             server.starttls()
            #             server.login(gmail_address,password)
            #             server.sendmail(gmail_address,emaillist,msg.as_string())
            #             server.close()
            #         if not shutup:
            #             print('r.send_gmail_email: successfully sent your email to ' + str(recipientⳆrecipients))
            #     except Exception as E:
            #         if not shutup:
            #             print('r.send_gmail_email: failed to send your email to ' + str(recipientⳆrecipients) + ". Error message: " + str(E))
# # region Old version of send_gmail_email (doesn't support attachments):
            # """def send_gmail_email(recipientⳆrecipients, subject:str="", body:str="",gmail_address:str=default_gmail_address,password:str=default_gmail_password,shutup=False):
            #     # param recipientⳆrecipients: Can be either a string or a list of strings: all the emails we will be sending this message to.
            #     import smtplib
            #     FROM = gmail_address
            #     TO = enlist(recipientⳆrecipients)# Original code: recipient if type(recipient) is list else [recipient]
            #     SUBJECT = subject
            #     TEXT = body

            #     # Prepare actual message
            #     message = "From: %s\nTo: %s\nSubject: %s\n\n%s\n" % (FROM, ", ".join(TO), SUBJECT, TEXT)
            #     try:
            #         server = smtplib.SMTP("smtp.gmail.com", 587)
            #         server.ehlo()
            #         server.starttls()
            #         server.login(gmail_address, password)
            #         server.sendmail(FROM, TO, message)
            #         server.close()
            #         if not shutup:
            #             print('r: send_gmail_email: successfully sent the mail')
            #     except:
            #         if not shutup:
            #             print( "r: send_gmail_email: failed to send mail")"""
# # endregion
            # def gmail_inbox_summary(gmail_address: str = default_gmail_address,password: str = default_gmail_password,max_ↈ_emails: int = default_max_ↈ_emails,just_unread_emails: bool = True):
            #     # Parameters captured in this summary include the fields (for the dicts in the output list) of
            #     # TODO［millis，sender，receiver，subject，sender_email，sender_name］  (Just using a TODO so that it's a different color in the code so it stands out more)  (all accessed as strings, of course)
            #     # returns a list of dictionaries. The length of this list ﹦ the number of emails in the inbox (both read and unread).
            #     # max_ↈ_emails ≣ max_number_of_emails --> caps the number of emails in the summary, starting with the most recent ones.
            #     '''Example output:
            #     [{'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484416777000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Computing Society] 10 games in 10 days. Today\'s game is "Purple...', 'receiver': 'Stony Brook Computing Society <sb.computing@groups.facebook.com>'},
            #     {'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484368779000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Game Developers (SBGD)] New link', 'receiver': '"Stony Brook Game Developers (SBGD)" <sbgamedev@groups.facebook.com>'},
            #     {'sender_email': 'no-reply@accounts.google.com', 'sender': 'Google <no-reply@accounts.google.com>', 'millis': 1484366367000, 'sender_name': 'Google', 'subject': 'New sign-in from Safari on iPhone', 'receiver': 'ryancentralorg@gmail.com'},
            #     {'sender_email': 'notification+kjdmmk_1v73_@facebookmail.com', 'sender': '"Richard McKenna" <notification+kjdmmk_1v73_@facebookmail.com>', 'millis': 1484271805000, 'sender_name': '"Richard McKenna"', 'subject': '[Stony Brook Computing Society] 10 games in 10 days. Today\'s game is "Jet LIfe"....', 'receiver': 'Stony Brook Computing Society <sb.computing@groups.facebook.com>'},
            #     {'sender_email': 'noreply@sendowl.com', 'sender': 'imitone sales <noreply@sendowl.com>', 'millis': 1484240836000, 'sender_name': 'imitone sales', 'subject': 'A new version of imitone is available!', 'receiver': 'ryancentralorg@gmail.com'}]'''
            #     # The following code I got of the web somewhere and modified a lot, I don't remember where though. Whatevs.
            #     import datetime
            #     import email
            #     import imaplib

            #     with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            #         # ptoc()
            #         mail.login(gmail_address,password)
            #         # ptoc()
            #         mail.list()
            #         # ptoc()
            #         mail.select('inbox')
            #         # ptoc()
            #         result,data=mail.uid('search',None,"UNSEEN" if just_unread_emails else "ALL")  # (ALL/UNSEEN)
            #         # ptoc()

            #         email_summaries=[]  # A list of dictionaries. Will be added to in the for loop shown below.
            #         ↈ_emails=len(data[0].split())
            #         for x in list(reversed(range(ↈ_emails)))[:min(ↈ_emails,max_ↈ_emails)]:
            #             latest_email_uid=data[0].split()[x]
            #             result,email_data=mail.uid('fetch',latest_email_uid,'(RFC822)')
            #             # result, email_data = conn.store(num,'-FLAGS','\\Seen')
            #             # this might work to set flag to seen, if it doesn't already
            #             raw_email=email_data[0][1]
            #             raw_email_string=raw_email.decode('utf-8')
            #             email_message=email.message_from_string(raw_email_string)

            #             # Header Details
            #             date_tuple=email.utils.parsedate_tz(email_message['Date'])
            #             if date_tuple:
            #                 local_date=datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            #                 # local_message_date=local_date.ctime()# formats the date in a nice readable way
            #                 local_message_date=local_date.timestamp()  # Gets seconds since 1970
            #                 local_message_date=int(1000 * local_message_date)  # millis since 1970
            #             email_from=str(email.header.make_header(email.header.decode_header(email_message['From'])))
            #             email_to=str(email.header.make_header(email.header.decode_header(email_message['To'])))
            #             subject=str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            #             # noinspection PyUnboundLocalVariable
            #             email_summaries.append(dict(millis=local_message_date,sender=email_from,receiver=email_to,subject=subject,sender_email=email_from[1 + email_from.find('<'):-1] if '<' in email_from else email_from,sender_name=email_from[:email_from.find('<') - 1]))
            #             # print('\n'.join(map(str,email_summaries)))//⟵Would display all email summaries in console
            #     return email_summaries
            # def _default_what_to_do_with_unread_emails(x):
            #     # An arbitrary default as an example example so that 'continuously_scan_gmail_inbox' can be run with no arguments
            #     # Example: continuously_scan_gmail_inbox()
            #     # By default, the continuous email scan will print out the emails and also read their subjects aloud via text-to-speech. (Assumes you're using a mac for that part).
            #     print(x)
            #     text_to_speech_via_apple(x['subject'],run_as_thread=False)
            #     send_gmail_email(x['sender_email'],'EMAIL RECEIVED: ' + x['subject'])
            # def continuously_scan_gmail_inbox(what_to_do_with_unread_emails: callable = _default_what_to_do_with_unread_emails,gmail_address: str = default_gmail_address,password: str = default_gmail_password,max_ↈ_emails: int = default_max_ↈ_emails,include_old_but_unread_emails: bool = False):
            #     # returns a new thread that is ran constantly unless you kill it. It will constantly scan the subjects of all emails received
            #     #  …AFTER the thread has been started. When it received a new email, it will run the summary of that email through the
            #     #  …'what_to_do_with_unread_emails' method, as a triggered event. It returns the thread it's running on so you can do stuff with it later on.
            #     #  …Unfortunately, I don't know how to make it stop though...
            #     # include_old_but_unread_emails: If this is false, we ignore any emails that were sent before this method was called. Otherwise, if include_old_but_unread_emails is true, …
            #     #  …we look at all emails in the inbox (note: this is only allowed to be used in this context because python marks emails as 'read' when it accesses them, …
            #     #  …and we hard-code just_unread_emails=True in this method so thfat we never read an email twice.)
            #     return run_as_new_thread(_continuously_scan_gmail_inbox,what_to_do_with_unread_emails,gmail_address,password,max_ↈ_emails,include_old_but_unread_emails)
            # def _continuously_scan_gmail_inbox(what_to_do_with_unread_emails,gmail_address,password,max_ↈ_emails,include_old_but_unread_emails):
            #     # This is a helper method because it loops infinitely and is therefore run on a new thread each time.
            #     exclusive_millis_min=millis()

            #     # times=[] # ⟵ For debugging. Look at the end of the while loop block to see more.
            #     while True:
            #         tic()
            #         # max_millis=exclusive_millis_min
            #         for x in gmail_inbox_summary(gmail_address,password,max_ↈ_emails):
            #             assert isinstance(x,dict)  # x's type is determined by gmail_inbox_summary, which is a blackbox that returns dicts. This assertion is for type-hinting.
            #             if x['millis'] > exclusive_millis_min or include_old_but_unread_emails:
            #                 #     if x['millis']>max_millis:
            #                 #         max_millis=x['millis']
            #                 what_to_do_with_unread_emails(x)
            #                 # exclusive_millis_min=max_millis

            #                 # times.append(toc())
            #                 # line_graph(times)
            #                 # ptoctic()# UPDATE: It's fine. Original (disproved) thought ﹦ (I don't know why, but the time here just keeps growing and growing...)
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

#def get_bytecode(obj):
#    #Commented this function out because it's broken, even though it's a good idea
#    import dis
#    return dis.Bytecode(lambda x:x + 1).dis()

def _format_datetime(date)->str:
    #EXAMPLE:
    #    ans = 2021-06-12 23:23:51.569487
    #     >>> ans.strftime('%b %d, %Y at %-I:%M:%S%p')
    #    ans = Jun 12, 2021 at 11:23:51PM
    import datetime
    assert isinstance(date,datetime.datetime)
    return date.strftime('%a %b %d, %Y at %-I:%M:%S%p')
    

_rinsp_temp_object=None
_builtin_print=print
def rinsp(object,search_or_show_documentation:bool=False,show_source_code:bool=False,show_summary: bool = False,max_str_lines: int = 5,*,fansi=fansi) -> None:  # r.inspect
    # This method is really uglily written (by Cthulu Himself, would ya believe!) because I made no attempt to refactor it. But it works and its really useful.
    # search_or_show_documentation: If this is a string, it won't show documentation UNLESS show_source_code ⋁ show_summary. BUT it will limit dir⋃dict to entries that contain search_or_show_documentation. Used for looking up that function name you forgot.


    printed_lines=[]
    def print(*x,end='\n',flush=False):
        out=' '.join(map(str,x))+end
        printed_lines.append(out)
        _builtin_print(end=out,flush=flush)

    """
    rinsp report (aka Ryan's Inspection):
        OBJECT: rinsp(object, show_source_code=False, max_str_lines:int=5)
        TYPE: class 'function'
        FILE: module '__main__' from '/Users/Ryan/PycharmProjects/RyanBStandards_Python3.5/r.py'
        STR: <function rinsp at 0x109eb10d0>"""
    search_filter=isinstance(search_or_show_documentation,str) and search_or_show_documentation or ''
    if search_filter:
        search_or_show_documentation=False or show_source_code or show_summary
    import inspect as i
    def linerino(x,prefix_length=0):
        max_string_length=max(0,max_str_lines*get_terminal_width()-prefix_length)
        number_of_lines=x.count("\n") + 1
        if len(x)<=max_string_length:
            new_x='\n'.join(x.split('\n')[:max_str_lines])
            continuation=fansi("\n" + tab + "\t………continues for " +str(number_of_lines -       max_str_lines) + " more lines and "+str(len(x)-       len(new_x)) + " more characters………",colour)
            return new_x + (continuation if (number_of_lines > max_str_lines + 1) else "")  # max_str_lines+1 instead of just max_str_lines so we dont get '………continues for 1 more lines………'
        else:
            new_x=x[:max_string_length]
            continuation=fansi("\n" + tab + "\t………continues for " +str(number_of_lines - new_x.count('\n')-1) + " more lines and "+str(len(x)-max_string_length) + " more characters………",colour)
            return new_x + continuation
    tab='   '
    colour='cyan'
    col=lambda x:fansi(x,colour,'bold')
    # _=col('rinsp report (aka Ryan\'s Inspection):')
    _=col('rinsp report (aka Ryan\'s Inspection):')
    print(_)
    if True:
        #Display ENTRIES
        temp=object
        try:  # noinspection PyStatementEffect
            object.__dict__
            print(col(tab + "ENTRIES: "),end="",flush=False)
            # print(col(tab + "DIR⋃DICT: "),end="",flush=False) # <---- ORIGINAL CODE
        except:
            temp=type(object)
            print(col(tab + "ENTRIES: "),end="",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
            # print(col(tab + "DIR⋃TYPE.DICT: "),end="",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.  # <---- ORIGINAL CODE
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
                    return ('red',None)
                if callable(attr):
                    return ('green', ) # Green if callable
                def is_module(x):
                    import types
                    return isinstance(x,types.ModuleType)
                if is_module(attr):
                    return ('blue',)
                return [None]  # Plain and boring if else
            dict_used_with_callables_highlighted_green=[fansi(x,*color(x)) for x in dict_used]
            print_string=(str(len(dict_used)) + ' things: [' + ', '.join(dict_used_with_callables_highlighted_green) + "]")  # Removes all quotes in the list so you can rad ) +" ⨀ ⨀ ⨀ "+str(dict_used).replace("\n","\\n"))
            print_string=print_string.replace('\x1b[0m','')#Make rendering large amounts of commas etc faster (switching between formats seems to make terminal rendering slow and even crashes windows)
            if currently_running_windows():
                print_string=strip_ansi_escapes(print_string)#This is to prevent really slowwww crashes on windows cause windows sucks lol
            print(end=print_string)
            print()
        else:
            print(end="\r")  # Erase the previous line (aka "DICT: " or "TYPE.DICT: ")

    str_on_top=True
    if str_on_top: #ENABLE THIS REGION TO PRINT 'STR:' on the TOP instead of the bottom
        try:
            # GETTING CHARACTER FOR TEMP
            def is_module(x):
                import types
                return isinstance(x,types.ModuleType)
            if not is_module(object):
                prefix=tab + "STR: "
                print((col(prefix) + linerino(str(object),len(prefix))))
        except:
            pass
        # try:
        #     # GETTING CHARACTER FOR TEMP
        #     def is_module(x):
        #         import types
        #         return isinstance(x,types.ModuleType)
        #     if not is_module(object):
        #         print(end=col(tab + "STR: ") + linerino(str(object)))
        #         print()
        # except Exception as e:
        #     # print_verbose_stack_trace(e)
        #     pass


    if False:
        pass
        # _=col(tab + 'OBJECT: ')
        # ⵁ_errored=False
        # try:
        #     _+=object.__name__
        # except Exception as e:
        #     _+='[cannot obtain object.__name__ without error: ' + str(e) + ']'
        #     ⵁ_errored=True
        # try:
        #     _+=str(i.signature(object))
        # except:
        #     pass
        # if not ⵁ_errored and _.strip():
        #     # print()
        #     print(end=_)
        #     print()
    try:
        temp=object
        from types import ModuleType
        neednewline=False
        try:
            print(col(tab+"LEN: ")+str(len(object)),end=' ')
            neednewline=True
        except Exception:pass
        if isinstance(object,str):
            print(col(tab + "LINES: ")+repr(number_of_lines(object)),flush=False,end='')
            
        if hasattr(object,'shape'):
            print(col(tab + "SHAPE: ")+repr(object.shape),flush=False,end='')
            neednewline=True
            if hasattr(object,'dtype'):
                print(col(tab + "DTYPE: ")+repr(object.dtype),flush=False,end='')
        if neednewline:
            print(flush=False)
        if isinstance(object,ModuleType):
            submodulenames=[x.split('.')[-1] for x in get_all_submodule_names(object)]
            if submodulenames:
                print(col(tab + "SUBMODULES: ")+(', '.join(submodulenames)),end="\n",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
            if hasattr(object,'__version__'):
                print(col(tab + "VERSION: ")+str(object.__version__),end="\n",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
        # try:  # noinspection PyStatementEffect
        #     object.__dict__
        #     print(col(tab + "ENTRIES: "),end="",flush=False)
        #     # print(col(tab + "DIR⋃DICT: "),end="",flush=False) # <---- ORIGINAL CODE
        # except:
        #     temp=type(object)
        #     print(col(tab + "ENTRIES: "),end="",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.
        #     # print(col(tab + "DIR⋃TYPE.DICT: "),end="",flush=False)  # If we can't get the dict of (let's say) a numpy array, we get the dict of it's type which gives all its parameters' names, albeit just their defgault values.  # <---- ORIGINAL CODE
        # dict_used=set(temp.__dict__)
        # dict_used=dict_used.union(set(dir(object)))
        # d=dict_used
        # if search_filter:
        #     print(fansi(tab + "FILTERED: ",'yellow','bold'),end="",flush=False)
        #     d={B for B in d if search_filter in B}
        # def sorty(d):
        #     A=sorted([x for x in d if x.startswith("__") and x.endswith("__")])  # Moving all built-ins and private variables to the end of the list
        #     B=sorted([x for x in d if x.startswith("_") and not x.startswith("__") and not x.endswith("__")])
        #     C=sorted(list(set(d) - set(A) - set(B)))
        #     return C + B + A
        # dict_used=sorty(d)
        # if len(dict_used) != 0:
        #     global _rinsp_temp_object
        #     _rinsp_temp_object=object
        #     attrs={}
        #     for attrname in dict_used:
        #         try:
        #             attrs[attrname]=(eval('_rinsp_temp_object.' + attrname))
        #         except:
        #             attrs[attrname]=(fansi("ERROR: Cannot evaluate",'red'))
        #     def color(attr):
        #         try:
        #             attr=eval('_rinsp_temp_object.' + attr)  # callable(object.__dir__.__get__(attr))
        #         except:
        #             return 'red',None
        #         if callable(attr):
        #             return 'green',  # Green if callable
        #         return [None]  # Plain and boring if else
        #     dict_used_with_callables_highlighted_green=[fansi(x,*color(x)) for x in dict_used]
        #     print_string=(str(len(dict_used)) + ' things: [' + ', '.join(dict_used_with_callables_highlighted_green) + "]")  # Removes all quotes in the list so you can rad ) +" ⨀ ⨀ ⨀ "+str(dict_used).replace("\n","\\n"))
        #     print_string=print_string.replace('\x1b[0m','')#Make rendering large amounts of commas etc faster (switching between formats seems to make terminal rendering slow and even crashes windows)
        #     if currently_running_windows():
        #         print_string=strip_ansi_escapes(print_string)#This is to prevent really slowwww crashes on windows cause windows sucks lol
        #     print(print_string)
        # else:
        #     print(end="\r")  # Erase the previous line (aka "DICT: " or "TYPE.DICT: ")
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
    def get_full_class_name(class_object):
        out=repr(class_object)
        if out.startswith('<class \'') and out.endswith("'>"):
            return out[len('<class \''):-len("'>")]
        return class_object.__name__
    def get_parent_hierarchy(object):
        from collections import OrderedDict
        # out=OrderedDict()
        out={}
        if not isinstance(object,type):
            object=object.__class__
        for parent in object.__bases__:
            # out[parent.__name__]=get_parent_hierarchy(parent)
            out[get_full_class_name(parent)]=get_parent_hierarchy(parent)
        return out

    def format_parent_hierarchy(hierarchy:dict,spaces=len('   ANCESTRY: ')):
        import pprint
        ans=pprint.pformat(hierarchy)
        ans=ans.replace("{'object': {}}",'object')
        ans=ans.replace("'",' ')
        ans=ans.splitlines()
        if len(ans)>1:
            ans[1:]=[' '*spaces+line for line in ans[1:]]
        ans=line_join(ans)
        return ans

    print(col(tab + 'ANCESTRY: ') + format_parent_hierarchy(get_parent_hierarchy(object)))#This is presenred in an ugly format right now and should eventually replace 'parent'. But this can be done later.

    print(col(tab + 'TYPE: ') + str(type(object))[1:-1]+parent_string)
    if i.getmodule(object) is not None:
        # print(col(tab + 'FILE: ') + str(i.getmodule(object))[1:-1])
        try:
            print(col(tab + 'FILE: ') + str(get_source_file(object)))
        except TypeError as e:
            print(col(tab + 'FILE: ') + str(e))


    if isinstance(object,str) and path_exists(object):
        stats=[]
        def append_stat(title,stat=''):
            stats.append(col(title+':')+str(stat))
        try:
            path=object
            if file_exists(path):
                append_stat('FILE STATS')
                append_stat('size',get_file_size(path))
                if is_image_file(path):
                    append_stat('resolution',str(get_image_file_dimensions(path)))
                if is_utf8_file(path):
                    append_stat('#lines',number_of_lines_in_file(path))    
                if is_video_file(path):
                    append_stat('duration',str(get_video_file_duration(path))+'s')
            else:
                append_stat('FOLDER STATS')
                append_stat('#files',len(get_all_files(path)))
                append_stat('#subfolders',len(get_all_folders(path)))
            append_stat('date_modified',str(_format_datetime(date_modified(path))))
        except Exception as e:
            print_stack_trace(e)
            pass
        print(col(tab + '     '.join(stats)))


    def errortext(x):
        return fansi(x,'red','underlined')

    # if not str_on_top:
    #     try:
    #         # GETTING CHARACTER FOR TEMP
    #         def is_module(x):
    #             import types
    #             return isinstance(x,types.ModuleType)
    #         if not is_module(object):
    #             prefix=tab + "STR: "
    #             print((col(prefix) + linerino(str(object),len(prefix))))
    #     except:
    #         pass
    # else:
    #     pass

    if True:
        _=col(tab + 'OBJECT: ')
        ⵁ_errored=False
        try:
            _+=object.__name__
        except Exception as e:
            _+='[cannot obtain object.__name__ without error: ' + str(e) + ']'
            ⵁ_errored=True
        try:
            def format_signature(item):
                assert callable(item)
                import inspect
                def autoformat_python_via_black(code:str):

                    if sys.version_info>(3,6):
                        pip_import('black')
                        import black
                        return black.format_str(code,mode=black.Mode())
                    #Python versions older than 3.6 don't support black
                    return code

                sig=inspect.signature(item)
                sig=item.__name__+str(sig)
                sig='def '+sig+':pass'
                sig=autoformat_python_via_black(sig)
                sig=sig[len('def '):]
                sig=sig.strip()
                sig=sig[:-len('pass')]
                sig=sig.strip()
                sig=sig[:-len(':')]
                return sig
            def indentify_all_but_first_line(string,indent):
                lines=line_split(string)
                if len(lines)<1:
                    return string
                lines[1:]=[indent+line for line in lines[1:]]
                return line_join(lines)
            try:
                signature=format_signature(object)
                # signature=signature[len(object.__name__):]
                signature=indentify_all_but_first_line(signature,' '*len('   SIGNATURE: '))
            except Exception:
                signature=object.__name__+i.signature(object)
            _=col(tab+'SIGNATURE: ')+fansi_syntax_highlighting(str(signature))
        except:
            pass
        if not ⵁ_errored and _.strip():
            # print()
            print(end=_)
            print()


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
        sourcecodeheader=tab + "SOURCE CODE:"
        print(col(sourcecodeheader) + fansi("―"*max(0,get_terminal_width()-len(sourcecodeheader)),'cyan','blinking'))
        _=code_string_with_comments=''
        _+=i.getcomments(object) or ''  # ≣i.getc omments(object) if i.getcomments(object) is not None else ''
        _=fansi_syntax_highlighting(_)
        try:
            try:
                _+=fansi_syntax_highlighting(str(i.getsource(object)))
            except:
                _+=fansi_syntax_highlighting(str(i.getsource(object.__class__)))
        except Exception as e:
            _+=2 * tab + errortext('[Cannot retrieve source code! Error: ' + linerino(str(e)) + "]")
        print(_)
    if search_or_show_documentation:
        print(col(tab + "DOCUMENTATION: "))
        try:
            if object.__doc__ and not object.__doc__ in _:
                print(fansi(str(object.__doc__),'gray'))
            else:
                if not object.__doc__:
                    print(2 * tab + errortext("[__doc__ is empty]"))
                else:  # ∴ object.__doc__ in _
                    print(2 * tab + errortext("[__doc__ can be found in source code, which has already been printed]"))
        except Exception as e:
            print(2 * tab + errortext("[Cannot retrieve __doc__! Error: " + str(e) + "]"))
    _maybe_display_string_in_pager(''.join(printed_lines),with_line_numbers=False)
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
default_audio_stream_chunk_size=1024  # chunk_size determines the resolution of time_in_seconds as the samplerate. Look in the code for more explanation idk how to describe it.
default_audio_mono_input_stream=None  # Initialized in the record_mono_audio function
def record_mono_audio(time_in_seconds,samplerate=default_samplerate,stream=None,chunk_size=default_audio_stream_chunk_size) :
    # You can count on this method having a delay (between when you call the method and when it actually starts recording) on the order of magnitude of 10⁻⁵ seconds
    # PLEASE NOTE: time_in_seconds is not interpreted precisely
    # EXAMPLE: play_sound_from_samples(record_mono_audio(2))
    pip_import('pyaudio')
    if stream is None:  # then use default_audio_mono_input_stream instead
        global default_audio_mono_input_stream
        if default_audio_mono_input_stream is None:  # Initialize it.
            import pyaudio  # You need this module to use this function. Download it if you don't have it.
            default_audio_mono_input_stream=pyaudio.PyAudio().open(format=pyaudio.paInt16,channels=1,rate=default_samplerate,input=True,frames_per_buffer=default_audio_stream_chunk_size)
        stream=default_audio_mono_input_stream
    number_of_chunks_needed=np.ceil(time_in_seconds * samplerate / chunk_size)  # Rounding up.
    out=np.hstack([np.fromstring(stream.read(num_frames=chunk_size,exception_on_overflow=False),dtype=np.int16) for _ in [None] * int(number_of_chunks_needed)])  # Record the audio
    out=np.ndarray.astype(out,float)  # Because by default it's an integer (not a floating point thing)
    out/=2 ** 15  # --> ∈［﹣1，1］ because we use pyaudio.paInt16. I confirmed this by banging on the speaker loudly and seeing 32743.0 as the max observed value.  ﹙# out/=max([max(out),-min(out)]) ⟵ originally this﹚
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
    return pickle.load(open(file_name,"rb"))
def save_pickled_value(file_name: str,*variables):
    # Filenames are relative to the current file path
    pickle.dump(detuple(variables),open(file_name,'wb'))
    # load_pickled_value=lambda file_name:pickle.load(open(file_name,"rb"))
# endregion
# region  .txt ⟷ str: ［string_to_text_file，text_file_to_string］
def string_to_text_file(file_path: str,string: str,) -> None:
    file_path=get_absolute_path(file_path)#Make sure it recognizes ~/.vimrc AKA with the ~ attached
    file=open(file_path,"w")
    try:
        file.write(string)
    except Exception:
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
    file_path=get_absolute_path(file_path)#Make sure it recognizes ~/.vimrc AKA with the ~ attached
    return open(file_path).read()

def append_line_to_file(line:str,file_path:str):
    #Adds a line to the end of a text file, or creates a new text file if none exists
    if not file_exists(file_path):
        string_to_text_file(file_path,line)
    else:
        file=open(file_path, 'a')
        try:
            file.write('\n'+line)
        finally:
            file.close()

def load_json(path):
    text=text_file_to_string(path)
    import json
    return json.loads(text)

def save_json(data,path):
    import json
    text=json.dumps(data)
    return text_file_to_string(path,text)

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
    session=pymatbridge.Matlab(executable=matlabroot,maxtime=60)  # maxtime=60-->Wait 1 minute to get a connection before timing out. I got this 'matlabroot' parameter by running "matlabroot" ﹙without quotes﹚in my Matlab IDE (and copy/pasting the output)
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
    pseudo_terminal("pseudo_terminal() --> Entering interactive MATLAB console! (Running inside of the 'r' module)",lambda x:"matlab('" + x + "')")
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
default_socket_port=13000
_socket_writers={}# A whole bunch of singletons
def socket_writer(targetIP: str,port: int = None):
    if (targetIP,port) in _socket_writers:
        return _socket_writers[(targetIP,port)]
    from socket import AF_INET,SOCK_DGRAM,socket
    # Message Sender
    host=targetIP  # IP address of target computer. Find yours with print_my_ip
    port=port or default_socket_port
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
    port=port or default_socket_port
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
def get_my_local_ip_address() -> str:
    import socket
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    try:
        return s.getsockname()[0]
    finally:
        s.close()
get_my_ip=get_my_local_ip_address #Legacy: Some of my old code might depend on this function. It's deprecated because it's a bad name
def get_my_mac_address()->str:
    #EXAMPLE:
    #     >> get_my_mac_address()
    #    ans = 28:cf:e9:17:d9:a5
    #
    if currently_running_linux():
        #If we're running linux, this solution works - and we don't have to pip install get-mac
        #    (pip install get-mac     also works, but this saves you the trouble of installing another package)
        #Returned as a string
        def get_default_iface_name_linux():
            #https://stackoverflow.com/questions/20908287/is-there-a-method-to-get-default-network-interface-on-local-using-python3
            route = "/proc/net/route"
            with open(route) as f:
                for line in f.readlines():
                    try:
                        iface, dest, _, flags, _, _, _, _, _, _, _, =  line.strip().split()
                        if dest != '00000000' or not int(flags, 16) & 2:
                            continue
                        return iface
                    except Exception:
                        continue
        def getmac(interface):
            #https://stackoverflow.com/questions/159137/getting-mac-address
            try:
                mac = open('/sys/class/net/' + interface + '/address').readline()
            except Exception:
                mac = "00:00:00:00:00:00"
            return mac[0:17]
        return getmac(get_default_iface_name_linux())
    else:
        pip_import('getmac','get-mac')
        import getmac
        return getmac.get_mac_address()
def get_my_public_ip_address():
    assert connected_to_internet(),'Cannot get our public IP address because we are not connected to the internet'
    from requests import get
    try:
        return get('https://icanhazip.com').text.strip()
        # return get('https://api.ipify.org').text
    except Exception:
        return get('http://ipgrab.io').text.strip()
# endregion
# region OSC≣'Open Sound Control' Output ［OSC_output］:
default_OSC_port=12345
try:default_OSC_ip=get_my_local_ip_address()
except Exception:pass
_OSC_client=None# This is a singleton
_OSC_values={}
def OSC_output(address,value):
    address=str(address)
    if not address[0]=='/':
        address='/'+address
    global default_OSC_ip
    default_OSC_ip=default_OSC_ip or get_my_local_ip_address()
    from rp.TestOSC import SimpleUDPClient
    global _OSC_client
    if not _OSC_client:
        _OSC_client=SimpleUDPClient(address=default_OSC_ip,port=default_OSC_port)
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
        except Exception:
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

def get_plt():
    pip_import('matplotlib')
    global plt
    import matplotlib.pyplot as plt
    locals()['plt']=plt
    return plt

def display_dot(x,y=None,color='red',size=3,shape='o',block=False):
    #Used to be called 'dot', in-case any of my old code breaks...
    #EXAMPLE: for theta in np.linspace(0,tau): display_dot(np.sin(theta),np.cos(theta));sleep(.1)
    if y is None:
        x,y=as_points_array([x])[0]
    plt=get_plt()
    plt.plot([x],[y],marker=shape,markersize=size,color=color)
    display_update(block=block)

def display_path(path,*,color=None,alpha=1,marker=None,linestyle=None,block=False,**kwargs):
    #If color is None, will plot as a different color every time
    x, y = as_points_array(path).T #Get the x, y values of the path as two lists
    import matplotlib.pyplot as plt
    plt.plot(x, y,color=color,alpha=alpha,marker=marker,linestyle=linestyle,**kwargs)
    update_display(block)

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
    assert is_valid(to_language) and is_valid(from_language),'Invalid language! Cannot translate. Valid languages: \n'+strip_ansi_escapes(indentify(display_dict(LANGUAGES,print_it=False,arrow=' --> ')))

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
    
def sync_shuffled(*lists):
    #Shuffles lists in sync with one another
    #EXAMPLE:
    # >>> sync_shuffled([1,2,3,4,5],'abcde')
    #ans = [(1, 3, 5, 2, 4), ('a', 'c', 'e', 'b', 'd')]
    lists=detuple(lists)
    return list(zip(*shuffled(list(zip(*lists)))))
    
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
    except Exception:
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
    T=T or default_tone_seconds
    samplerate=samplerate or default_samplerate
    ƒ=ƒ or default_tone_frequency
    ↈλ=ƒ * T  # ≣number of wavelengths
    return np.sin(np.linspace(0,τ * ↈλ,int(T * (samplerate or default_samplerate))))

def triangle_tone_sampler(ƒ=None,T=None,samplerate=None):
    return 2 / π * np.arcsin(sine_tone_sampler(ƒ,T,samplerate))

def sawtooth_tone_sampler(ƒ=None,T=None,samplerate=None):
    T=T or default_tone_seconds
    samplerate=samplerate or default_samplerate
    ƒ=ƒ or default_tone_frequency
    ↈλ=ƒ * T  # ≣number of wavelengths
    return (np.linspace(0,ↈλ,int(T * (samplerate or default_samplerate))) % 1) * 2 - 1

def square_tone_sampler(ƒ=None,T=None,samplerate=None):
    return np.sign(sawtooth_tone_sampler(ƒ,T,samplerate))

default_tone_frequency=440  # also known as note A4
default_tone_sampler=sine_tone_sampler
default_tone_seconds=1
def play_tone(hz=None,seconds=None,samplerate=None,tone_sampler=None,blocking=False):  # Plays a sine tone
    ƒ,T=hz or default_tone_frequency,seconds or default_tone_seconds  # Frequency, Time
    play_sound_from_samples((tone_sampler or default_tone_sampler)(ƒ,T),samplerate or default_samplerate,blocking=blocking)
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
        except Exception:
            return
        return cr
    cr=ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd=os.open(os.ctermid(),os.O_RDONLY)
            cr=ioctl_GWINSZ(fd)
            os.close(fd)
        except Exception:
            pass
    if not cr:
        cr=(env.get('LINES',24),env.get('COLUMNS',80))

        ### Use get(key[, default]) instead of a try/catch
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except Exception:
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
    except Exception:
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

def split_python_tokens(code: str):
    #Should return a list of all the individual python tokens, INCLUDING whitespace and newlines etc
    #When summed together, the token-strings returned by this function should equal the original inputted string
    pip_import('pygments')

    from pygments.lexers import Python3Lexer
    from pygments.lexer import Lexer

    def get_all_pygments_tokens(string:str,pygments_lexer:Lexer=Python3Lexer()):
        return pygments_lexer.get_tokens_unprocessed(string)

    def get_all_token_strings(string:str):
        #Returns all the string-value of all tokens parsed from the string, including whitespace and comments
        token_string_generator = (token[2] for token in get_all_pygments_tokens(string))
        return token_string_generator

    return list(get_all_token_strings(code))

def int_clamp(x: int,min_value: int,max_value: int) -> int:
    return min([max([min_value,x]),max_value])
def float_clamp(x: float,min_value: float,max_value: float) -> float:
    # noinspection PyTypeChecker
    return int_clamp(x,min_value,max_value)


def print_highlighed_stack_trace(error:BaseException):
    #Uses pygments to print a stack trace with syntax highlighting
    from traceback import format_exception
    from pygments import highlight
    from pygments.lexers import Python3TracebackLexer
    from pygments.formatters import TerminalTrueColorFormatter
    from pygments.formatters.terminal import TerminalFormatter
    error_string=''.join(format_exception(error.__class__,error,error.__traceback__))
    highlighted_error_string=highlight(error_string, Python3TracebackLexer(), TerminalFormatter())
    # highlighted_error_string=highlight(error_string, Python3TracebackLexer(), TerminalTrueColorFormatter())
    print(highlighted_error_string)    

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
    except ValueError as e:#ERROR: ValueError: Can't format KeyboardInterrupt(). Expected an exception instance, sys.exc_info() tuple,a frame or a thread object.
        fansi_print("Stackprinter failed to print your verbose stack trace using rp.print_verbose_stack_trace():",'magenta','underlined')
        print_stack_trace(e)
        fansi_print("Here's your error's traceback:",'magenta','underlined')
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
    return [ linterp(mono_audio,x) for x in np.linspace(0,len(mono_audio)-1,new_number_of_samples)]

def cartesian_to_polar(x, y, ϴ_unit=τ)->tuple:
    """Input conditions: x，y ∈ ℝ ⨁ x﹦［x₀，x₁，x₂……］⋀ y﹦［y₀，y₁，y₂……］
    returns: (r, ϴ) where r ≣ radius，ϴ ≣ angle and 0 ≤ ϴ < ϴ_unit. ϴ_unit﹦τ --> ϴ is in radians，ϴ_unit﹦360 --> ϴ is in degrees"""
    return np.hypot(x,y),np.arctan2(y,x)/τ%1*ϴ_unit  # Order of operations: % has same precedence as * and /
def complex_to_polar(complex,ϴ_unit=τ)->tuple:
    """returns: (r, ϴ) where r ≣ radius，ϴ ≣ angle and 0 ≤ ϴ < ϴ_unit. ϴ_unit﹦τ --> ϴ is in radians，ϴ_unit﹦360 --> ϴ is in degrees.
    Input conditions: c ≣ complex ⋀ c ∈ ℂ ⨁ c﹦［c₀，c₁，c₂……］
    Returns r and ϴ either as numbers OR as two lists: all the r's and then all the ϴ's"""
    return np.abs(complex),np.angle(complex)# np.abs is calculated per number, not vector etc
default_left_to_right_sum_ratio=0# By default, take a left hand sum
def riemann_sum(f,x0,x1,N,left_to_right_sum_ratio=None):# Verified ✔
    # Desmos: https://www.desmos.com/calculator/tgyr42ezjq
    # left_to_right_sum_ratio﹦0  --> left hand sum
    # left_to_right_sum_ratio﹦.5 --> midpoint hand sum
    # left_to_right_sum_ratio﹦1  --> right hand sum
    # The x1 bound MUST be exclusive as per definition of a left riemann sum
    c=left_to_right_sum_ratio or default_left_to_right_sum_ratio
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
    return list_flatten([[(r,c,m[r][c]) for c in range(len(m[r])) if filter(r,c,m[r,c])] for r in range(len(m))])# Creates list of coordinates, (x,y,value). WARNING: Can be very slow
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

def cluster_by_key(iterable,key)->list:
    #Iterable is a list of values
    #Key is a function that takes a value from iterable and returns a hashable
    assert callable(key)
    assert is_iterable(iterable)
    from collections import OrderedDict
    outputs=OrderedDict()
    for value in iterable:
        k=key(value)
        if k not in outputs:
            outputs[k]=[]
        outputs[k].append(value)
    return list(outputs.values())
    
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

#def encode_float_matrix_to_rgb_image(m):
#    # Encoded precision of values between 0 and 1 as r,g,b (in 8-bit color) values where r g and b are each digits, with b being the most precise and r being the least precise
#    #Formerly called 'rgb_encoded_matrix'
#    m=np.matrix(m)
#    assert len(m.shape)==2,"r.encode_float_matrix_to_rgb: Input should be a matrix of values between 0 and 1, which is not what you gave it! \n m.shape = \n"+str(m.shape)
#    r,g,b=proportion_to_digits(m,base=256,number_of_digits=3)
#    out=np.asarray([r,g,b])
#    out=np.transpose(out,[1,2,0])
#    out=out.astype(np.uint8)
#    return out

def encode_float_matrix_to_rgba_byte_image(float_matrix):
    #Can encode a 32-bit float into the 4 channels of an RGBA image
    #The values should be between 0 and 1
    #This output can be saved as a .png file
    #Formerly called 'rgb_encoded_matrix'
    #It's useful for reading and storing floating-point matrices in .png files
    m=float_matrix
    m=np.matrix(m)
    assert is_grayscale_image(m)
    assert is_a_matrix(m),'Please input a two-dimensional floating point matrix with values between 0 and 1. The input you gave is not a matrix.'
    assert len(m.shape)==2,"r.encode_float_matrix_to_rgb: Input should be a matrix of values between 0 and 1, which is not what you gave it! \n m.shape = \n"+str(m.shape)

    r,g,b,a=proportion_to_digits(m,base=256,number_of_digits=4)
    out=np.asarray([r,g,b,a])
    out=np.transpose(out,[1,2,0])
    out=out.astype(np.uint8)
    return out

def decode_float_matrix_from_rgba_byte_image(image):
    #This function is the inverse of encode_float_matrix_to_rgba_image
    #Takes an rgba byte-image (that was created with encode_float_matrix_to_rgba_image) and turns it back into a float image
    #It's useful for reading and storing floating-point matrices in .png files
    #Formerly called 'matrix_decoded_rgb'

    assert is_rgba_image(image)
    assert is_byte_image(image)
    # assert len(image.shape)==3 and image.shape[-1]==3,"r.encode_float_matrix_to_rgba_image: Input should be an rgb image (with 3 color channels), which is not what you gave it! \n m.shape = \n"+str(image.shape)
    r,g,b,a=image.transpose([2,0,1])
    return r/256**1 + g/256**2 + b/256**3 + a/256**4


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
    except Exception:
        return False

def indentify(s:str,indent='\t'):
    return '\n'.join(indent + x for x in s.split('\n'))

def lrstrip_all_lines(s:str):
    return '\n'.join([x.lstrip().rstrip()for x in s.split('\n')])

random_unicode_hash=lambda l:int_list_to_string([randint(0x110000-1)for x in range(l)])

def search_replace_simul(s:str,replacements:dict):
    #Attempts to make multiple simultaneous string .replace() at the same time
    #WARNING: This method is NOT perfect, and sometimes makes errors. TODO: Fix it for all input cases

    if not replacements:
        return s
    # search_replace_simul("Hello world",{"Hello":"world","world":"Hello"})
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

# def gist(gist_body="Body",gist_filename="File.file",gist_description="Description"):
#     # Older version:
#     # def gist(code:str,file_name:str='CodeGist.code',username='sqrtryan@gmail.com',password='d0gememesl0l'):
#     #     # Posts a gist with the given code and filename.
#     #     #  ⮤ gist("Hello, World!")
#     #     # ans = https://gist.github.com/b5b3e404c414f7974c4ccb12106c4fe7
#     #     import requests,json
#     #     r = requests.post('https://api.github.com/gists',json.dumps({'files':{file_name:{"content":code}}}),auth=requests.auth.HTTPBasicAuth(username, password))
#     #     try:
#     #         return r.json()['html_url']# Returns the URL
#     #     except KeyError as e:
#     #         fansi_print("r.gist ERROR:",'red','bold',new_line=False)
#     #         fansi_print(" "+str(e)+" AND r.json() = "+str(r.json()),'red')

#     from urllib.request import urlopen
#     import json
#     gist_post_data={'description':gist_description,
#                     'public':True,
#                     'files':{gist_filename:{'content':gist_body}}}

#     json_post_data=json.dumps(gist_post_data).encode('utf-8')

#     def upload_gist():
#         # print('sending')
#         url='https://api.github.com/gists'
#         json_to_parse=urlopen(url,data=json_post_data)

#         # print('received response from server')
#         found_json=(b'\n'.join(json_to_parse.readlines()))
#         return json.loads(found_json.decode())['html_url']
#     return upload_gist()

# sgist=lambda *x:seq([gist,printed,open_url,shorten_url],*x)# Open the url of a gist and print it

def unshorten_url(shortened_url):
    #Takes a shortened URL and returns the long one
    #EXAMPLE: unshorten_url('bit.ly/labinacube')  -->  'https://oneoverzero.pythonanywhere.com/'
    #https://stackoverflow.com/questions/3556266/how-can-i-get-the-final-redirect-url-when-using-urllib2-urlopen/3556287

    if not is_valid_url(shortened_url):
        shortened_url='https://'+shortened_url
    assert is_valid_url(shortened_url),'Please input a valid URL!'
    
    from urllib.request import urlopen
    return urlopen(shortened_url).url

def load_gist(gist_url:str):
    #Takes the URL of a gist, or the shortened url of a gist (by something like bit.ly), and returns the content inside that gist as a string
    #EXAMPLE:
    #     >>> save_gist('AOISJDIO')
    #    ans = https://git.io/JI2Ez
    #     >>> load_gist(ans)
    #     ans = AOISJDIO

    gist_url=unshorten_url(gist_url) #If we shortened the url, unshorten it first. Otherwise, this function will leave it alone.

    gist_id=[x for x in gist_url.split('/') if len(x)==32 and set(x)<=set('0123456789abcdef')] # A gist_id is like 162d6a7e7f0386208d323d35dd86a669 -- it has 40 characters
    assert len(gist_id)>0,'This is not a valid github GIST url'
    gist_id=gist_id[0] #Assume there's only one key in the url...
    gist_url='https://gist.githubusercontent.com/raw/'+gist_id

    gist_url+='/raw'

    import requests,json
    response=requests.get(gist_url)
    return response.content.decode()
    # response_json=json.loads(response.content)
    # file_name=list(response_json['files'])[0]
    # return response_json['files'][file_name]['content']
    
def shorten_github_url(url,title=None):
    #Uses git.io to shorten a url
    #This method specifically only works for Github URL's; it doesn't work for anything else
    #If title is specified, it will try to get you a particular name for your url (such as git.io/labinacube)
    if not is_valid_url(url):
        #Try to make it valid
        url='https://'+url
    assert is_valid_url(url)
    # print(url)
    import requests
    data = {'url': url, 'code':title}
    if not title: del data['code']
    r = requests.post('https://git.io/', data=data)
    out= r.headers.get('Location')
    # print(out)
    return out
#def post_gist(content:str,
#              file_name:str='',
#              description:str='',
#              api_token:str='d65866e83aac7fc09093220a795ca66a5f7cc18d'):
#    # Note: Please don't be a dick, this api_token is meant for everybody using this library to share. Don't abuse it.

#    # Example:          
#    #     >>> post_gist('Hello World!')                                          
#    #    ans = https://api.github.com/gists/92d158541ae4f3732267194b1f1ac14d     
#    #     >>> load_gist(ans)                                                     
#    #    ans = Hello World!                                                      

#    #You can't post the api_token in a gist on github. If you do, github will disable that api_token.
#    #To make sure that github doesn't revoke the api_token, we have to make sure it's not in the content string.
#    content=content.replace(api_token,api_token[::-1])#Let's just reverse it.


#    import urllib
#    import json
#    import datetime
#    import time

#    access_url = "https://api.github.com/gists"
    
#    data={
#            'description':description,
#            'public':True,
#            'files':{
#                file_name:
#                {
#                    'content':content
#                }
#            }
#        }
        
#    json_data=bytes(json.dumps(data),'UTF-8');
    
#    req = urllib.request.Request(access_url) #Request
#    req.add_header("Authorization", "token {}".format(api_token))
#    req.add_header("Content-Type", "application/json")
    
#    res = urllib.request.urlopen(req, data=json_data) #Response
#    res_json = json.loads(res.readline())
    
#    return res_json['url']

def save_gist(content:str,*,
              shorten_url=True,
              description:str='',
              filename:str='',
              token:str="5bbe2f80af7cd2c347664c2ff9f2616676918c70"):
    #This function takes an input string, posts it as a gist on Github, then returns the URL of the new gist
    #I've included a token that anybody using this library is allowed to use. Have fun, but please don't abuse it!
    #
    #EXAMPLE:
    #     >>> save_gist('AOISJDIO')
    #    ans = https://git.io/JI2Ez
    #     >>> load_gist(ans)
    #     ans = AOISJDIO
    #
    #You can't post the api_token in a gist on github. If you do, github will disable that api_token.
    #To make sure that github doesn't revoke the api_token, we have to make sure it's not in the content string.
    #NOTE: if you get a SSL Error that looks like
    #       URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)>
    #   Then try running rp.r._fix_CERTIFICATE_VERIFY_FAILED_errors()
    import urllib.request, urllib.error, urllib.parse
    import json
    import datetime
    import time
    
    access_url = "https://api.github.com/gists"
    
    data = {
      "description": description,
      "public": True,
      "files": {
        filename: {
          "content": content
        }
      }
    }
    
    json_data=json.dumps(data)
    assert token not in json_data,'You cannot put the github API token anywhere in your gist, or else the API token will be revoked!'
    
    req = urllib.request.Request(access_url)
    req.add_header("Authorization", "token {}".format(token))
    req.add_header("Content-Type", "application/json")
    response=urllib.request.urlopen(req, data=json_data.encode())
    response=json.loads(response.read())
    gist_url=response['html_url']

    if shorten_url:
        gist_url=shorten_github_url(gist_url)

    try:
        #Try to keep track of all the gists we've created, in case we ever want to go back for some reason
        try:
            old_gists=open(_old_gists_path,'a+')
            old_gists.write(gist_url+'\n')
        finally:
            old_gists.close()
    except Exception as e:
        print(e)
        #It's no big deal if we can't though
        raise
        pass

    return gist_url

def _fix_CERTIFICATE_VERIFY_FAILED_errors():
    #https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    import os
    import os.path
    import ssl
    import stat
    import subprocess
    import sys

    STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
                 | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
                 | stat.S_IROTH |                stat.S_IXOTH )


    def main():
        openssl_dir, openssl_cafile = os.path.split(
            ssl.get_default_verify_paths().openssl_cafile)

        print(" -- pip install --upgrade certifi")
        subprocess.check_call([sys.executable,
            "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"])

        import certifi

        # change working directory to the default SSL directory
        os.chdir(openssl_dir)
        relpath_to_certifi_cafile = os.path.relpath(certifi.where())
        print(" -- removing any existing file or link")
        try:
            os.remove(openssl_cafile)
        except FileNotFoundError:
            pass
        print(" -- creating symlink to certifi certificate bundle")
        os.symlink(relpath_to_certifi_cafile, openssl_cafile)
        print(" -- setting permissions")
        os.chmod(openssl_cafile, STAT_0o775)
        print(" -- update complete")

    if __name__ == '__main__':
        main()


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

def display_image_in_terminal(image,dither=True,auto_resize=True,bordered=False):
    #Uses unicode, and is black-and-white
    #EXAMPLE: while True: display_image_in_terminal(load_image_from_webcam())
    #
    #EXAMPLE: Starfield
    #     def stars(density=.001,size=256):
    #         return as_float_image(np.random.rand(size,size)<density)
    #     def zoom(image,factor):
    #         return (crop_image(cv_resize_image(image,factor),*get_image_dimensions(image),origin='center'))
    #     image=stars()
    #     for _ in range(10000):
    #         image=image+stars()
    #         image=zoom(image,1.05)
    #         image*=.99
    #         scene=image
    #         scene=as_binary_image(image,dither=True)
    #         scene=bordered_image_solid_color(scene)
    #         scene=as_binary_image(scene)
    #         display_image_in_terminal(image**1,bordered=True)
    #         display_image(image)
    #
    if isinstance(image,str):
        image=load_image(image)
    def width(image) -> int:
        return len(image)
    def height(image) -> int:
        return len(image[0])
    pip_import('drawille')
    from drawille import Canvas

    if get_image_width(image)>get_terminal_width()*2 and auto_resize==True:
        scale_factor=(max(1,get_terminal_width()*2))/get_image_width(image)
        image=resize_image(image,scale_factor,'nearest')

    i=as_binary_image(as_grayscale_image(image),dither=dither)
    if bordered:
        #This prevents drawille from cropping the image zeros
        i=bordered_image_solid_color(i)
        i=as_binary_image(as_grayscale_image(i))

        

    c=Canvas()
    for x in range(width(i)):
        for y in range(height(i)):
            if i[x,y]:
                c.set(y,x)
    print(c.frame())

def display_image_in_terminal_color(image):
    #Will attempt to draw a color image in the terminal
    #This is slower than display_image_in_terminal, and relies on both unicode and terminal colors
    #EXAMPLE:
    #    display_image_in_terminal_color(load_image('https://i.guim.co.uk/img/media/faf20d1b2a98cbca9f5eb2946254566527394e15/78_689_3334_1999/master/3334.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=69707184a1b38f36fc077f7cafba1130'))#Display Kim Petras in the terminal
    USE_OPENCV=True
    pip_import('timg')
    if file_exists(image) or is_valid_url(image):
        image=load_image(image)
    assert is_image(image)
    image=as_rgb_image(image)
    image=as_byte_image(image)
    temp_file=temporary_file_path('png')
    try:
        import subprocess
        width=min(get_terminal_width(),get_image_width(image))
        height=int(get_image_height(image)*width/get_image_width(image))
        if width!=get_image_width(image):
            image=(cv_resize_image if USE_OPENCV else resize_image)(image,(height,width))
        save_image(image,temp_file)
        subprocess.run([sys.executable,'-m','timg','-s',str(width),temp_file])
    finally:
        if file_exists(temp_file):
            delete_file(temp_file)


        
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
    except Exception:
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
def print_latex_image(latex: str):
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
    image=latex_image(latex)
    image=inverted_image(image)
    display_image_in_terminal(image,dither=False)
    


    #DisplayThin=   lambda latex:display_image_in_terminal(((resize_image(skeletonize(255 - latex_image(latex)[:,:,0]),scale) > threshold) * 1.0).squeeze(),dither=False)
    #DisplayRegular=lambda latex:display_image_in_terminal(((resize_image(           (255 - latex_image(latex)[:,:,0]),scale) > threshold) * 1.0).squeeze(),dither=False)
    ##@formatter:on
    #if thin:
    #    DisplayThin(latex)
    #else:
    #    DisplayRegular(latex)

# cd=os.chdir
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

# def is_valud_url(url: str) -> bool:
#     # PROBLEM:
#     #     ⮤ ivu("google.com")
#     # ans=False
#     # I DID NOT WRITE THIS WHOLE FUNCTION ∴ IT MIGHT NOT WORK PERFECTLY. THIS IS FROM: http://stackoverflow.com/questions/452104/is-it-worth-using-pythons-re-compile
#     import re
#     regex=re.compile(
#         r'^(?:http|ftp)s?://'  # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
#         r'localhost|'  # localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
#         r'(?::\d+)?'  # optional port
#         r'(?:/?|[/?]\S+)$',re.IGNORECASE).match(url)
#     return regex is not None and (lambda ans:ans.pos == 0 and ans.endpos == len(url))(g.fullmatch(url))

import rp.rp_ptpython.prompt_style as ps
ps.__all__+=("PseudoTerminalPrompt",)

_prompt_style_path=__file__+'.rp_prompt_style'
_get_prompt_style_cached=None
def _get_prompt_style():
    global _get_prompt_style_cached
    if _get_prompt_style_cached is None:
        try:
            out=text_file_to_string(_prompt_style_path)
        except Exception:
            out=' >>> '

        _get_prompt_style_cached=out
    return _get_prompt_style_cached


_cd_history_size_limit=100000#To avoid spamming the console when we use CDH, limit the number of recent directories to this amount #UPDATE: I decided to make this effectively limitless (100000 is very big lol). Why limit it?
_cd_history_path=__file__+'.rp_cd_history.txt'
def _get_cd_history():
    try:
        output = line_split(text_file_to_string(_cd_history_path))
        output = output[:_cd_history_size_limit]
        return output
    except Exception as e:
        # print_verbose_stack_trace(e)
        return []
def _add_to_cd_history(path:str):
    if path=='.':
        return
    def unique(l:list):
        o=[]
        for e in reversed(l):
            if e not in o:
                o.append(e)
        return o[::-1] 
    entries=_get_cd_history()
    entries.append(path)
    entries=unique(entries)
    string_to_text_file(_cd_history_path,line_join(entries))

def _update_cd_history():
    # print()
    # print("OLD HISTORY")
    # fansi_print(text_file_to_string(_cd_history_path),'magenta')
    # fansi_print(_get_cd_history(),'magenta')
    try:
        _add_to_cd_history(get_current_directory())
        from rp.rp_ptpython.completer import get_all_importable_module_names
        get_all_importable_module_names()#Refresh
    except FileNotFoundError:
        #This will happen if the folder we're currently working in is deleted. Just skip updating the history...
        pass
    # print("NEW HISTORY")
    # fansi_print(text_file_to_string(_cd_history_path),'magenta')
    # fansi_print(_get_cd_history(),'magenta')
    # print()
def _clean_cd_history():
    #Removes all nonexistant paths from CDH
    #It removes all the red entries
    entries=_get_cd_history()
    entries=[entry for entry in entries if path_exists(entry)]
    string_to_text_file(_cd_history_path,line_join(entries))

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
default_python_input_eventloop = None  # Singleton for python_input
# def python_input(namespace):
#     try:
#         from rp.prompt_toolkit.shortcuts import create_eventloop
#         from ptpython.python_input import PythonCommandLineInterface,PythonInput as Pyin
#         global default_python_input_eventloop
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
#         default_python_input_eventloop=default_python_input_eventloop or PythonCommandLineInterface(create_eventloop(),python_input=pyin)
#         #
#         # try:
#         code_obj = default_python_input_eventloop.run()
#         if code_obj.text is None:
#             print("THE SHARKMAN SCREAMS")
#         return code_obj.text
#     except Exception as E:
#         print_stack_trace(E)
#     # except BaseException as re:
#     # print_stack_trace(re)
#     # print("THE DEMON SCREAMS")
def split_into_sublists(l,sublist_len:int,strict=False,keep_remainder=True):
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
    assert is_number(sublist_len),'sublist_len should be an integer, but got type '+repr(type(sublist_len))
    if strict:
        assert not len(l)%sublist_len,'len(l)=='+str(len(l))+' and sublist_len=='+str(sublist_len)+': strict mode is turned on but the sublist size doesnt divide the list input evenly. len(l)%sublist_len=='+str(len(l)%sublist_len)+'!=0'
    n=sublist_len
    return list(zip(*(iter(l),) * n))+([tuple(l[len(l)-len(l)%n:])] if len(l)%n and keep_remainder else [])

def rotate_image(image, angle_in_degrees):
    #Returns a rotated image by angle_in_degrees, clockwise
    #The output image size is usually not the same as the input size, unless the angle is 180 (or in the case of a square image, 90, 180, or 270)
    #Usually, the output image size is larger than the input image size
    image=as_numpy_array(image)
    assert is_image(image)

    #Handle the edge cases: 0, 90, 180, 270, 360, etc - we don't need OpenCV for this
    if angle_in_degrees%360==0:
        return image.copy()
    if angle_in_degrees%360==180:
        return horizontally_flipped_image(vertically_flipped_image(image))
    if angle_in_degrees%90==0:
        if is_grayscale_image(image):
            if angle_in_degrees%360==270:
                return vertically_flipped_image(image.copy().T)
            else:
                assert angle_in_degrees%360==90
                return horizontally_flipped_image(image.copy().T)
        else:
            assert is_rgb_image(image) or is_rgba_image(image)
            if angle_in_degrees%360==270:
                return vertically_flipped_image(image.transpose(1,0,2))
            else:
                assert angle_in_degrees%360==90
                return horizontally_flipped_image(image.transpose(1,0,2))
        

    #ALTERNATIVE Implementation that doesn't use OpenCV and instead uses PILLOW (not used in this function):
    #    https://pythonexamples.org/python-pillow-rotate-image-90-180-270-degrees/#:~:text=You%20can%20rotate%20an%20image,to%20the%20size%20of%20output.
    # GOT CODE FROM URL: https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    #TODO: Make a cv_rotate_image version of this function that handles making the black pixels instead reflected images (there's an option for that in cv2.warp_affine). This is better for data augmentation purposes.
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

def open_url_in_web_browser(url:str):
    from webbrowser import open
    open(url)

def google_search_url(query:str)->None:
    #Returns the URL for google-searching the given query
    query=str(query)
    import urllib.parse
    url='https://www.google.com/search?q='+urllib.parse.quote(query)
    return url

def open_google_search_in_web_browser(query:str):
    #Opens up the web browser to a google search of a given query
    url=google_search_url(query)
    open_url_in_web_browser(url)
    return url

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
#         except Exception:
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
    getter=lambda x:inspect.getfile(inspect.getmodule(x))
    import inspect
    try:
        return getter(object)
    except TypeError:#ERROR: TypeError: None is not a module, class, method, function, traceback, frame, or code object
        return getter(type(object))


# region Editor Launchers
def edit(file_or_object,editor_command='atom'):
    if isinstance(file_or_object,str):
        return shell_command(editor_command +" " + repr(file_or_object),as_subprocess=True)# Idk if there's anything worth returning but maybe there is? run_as_subprocess is true so we can edit things in editors like vim, suplemon, emacs etc.
    else:
        return edit(get_source_file(object=file_or_object),editor_command=editor_command)
sublime=lambda x:edit(x,'sublime')
subl   =lambda x:edit(x,'subl'   )
vscode =lambda x:edit(x,'code'   )
gedit  =lambda x:edit(x,'gedit'  )
atom   =lambda x:edit(x,'atom'   )
# vim=lambda x:edit(x,'vim') # Later we define a special, custom function for vim

def _static_calldefs(modpath):
    pip_import('xdoctest')
    from xdoctest import static_analysis as static
    calldefs = dict(static.parse_calldefs(fpath=modpath))
    return calldefs

def _get_object_lineno(obj):
    #TODO: Make this still work even if the source file was changed (right now, if you use VIMORE and then edit the file then use VIMORE again, it will bring you to the wrong place the second time because of how python works)
    try:
        # functions just 
        lineno = obj.__code__.co_firstlineno
    except Exception:
        module_code=text_file_to_string(get_source_file(obj))
        obj_code=get_source_code(obj)
        first_line=obj_code.splitlines()[0]
        index=module_code.find(first_line)
        lineno=module_code[:index].count('\n')
        lineno+=1


    # except AttributeError:
    #     attrname = obj.__name__
    #     modpath = sys.modules[obj.__module__].__file__
    #     calldefs = _static_calldefs(modpath)
    #     ub.modpath_to_modname(modpath)
    #     calldef = calldefs[attrname]
    #     lineno = calldef.lineno

    return lineno

def vim(file_or_object=None,line_number=None):
    import subprocess
    args=['vim']

    assert currently_in_a_tty(),'Cannot start Vim because we are not running in a terminal' #In Jupyter Notebook, launching Vim might force you to restart the kernel...very annoying

    if isinstance(file_or_object,str):
        path=file_or_object
        path=get_absolute_path(path)
        args.append(path)
    elif file_or_object is None:
        path=None
        pass
    else:
        path=get_source_file(file_or_object)
        args.append(path)

        if line_number is None and not is_a_module(file_or_object):
            try:
                line_number=_get_object_lineno(file_or_object)
            except Exception:
                pass

    if line_number is not None:
        #https://stackoverflow.com/questions/3313418/starting-vim-at-a-certain-position-line-and-column-of-a-file
        column_number=0
        args+=['+call cursor(%i,%i)'%(line_number,column_number),'+normal zz']

    if is_a_folder(path):
        folder=path
    else:
        folder=get_parent_directory(path)
        
    original_directory=get_current_directory()

    try:
        set_current_directory(folder) # This step is just for convenience; it's completely optional (might be removed if I don't like it). When editing a file, set vim's pwd to it's folder
        subprocess.call(args) 
    finally:
        set_current_directory(original_directory)
    

# # initialize editor methods. Easier to understand when analyzing this code dynamically; static analysis might be really confusing
# __known_editors=['emacs','suplemon','atom','sublime','subl']# NONE of these names should intersect any methods or varables in the r module or else they will be overwritten!
# # for __editor in __known_editors:
#     exec("""
# def X(file_or_object):
#     _edit(file_or_object,editor_command='X')""".replace('X',__editor))
# del __known_editors,__editor# This is just a setup section to create methods for us, so get rid of the leftovers. __known_editors and __editor are assumed to be unused anywhere else in our current namespace!dz

def xo(file_or_object):
    # FYI: 'xo' stands for 'exofrills', a console editor. I haven't used it much though. I don't really use console based editors much…
    import xo
    try:
        if not isinstance(file_or_object,str):
            file_or_object=get_source_file(file_or_object)
        xo.main([file_or_object])
    except Exception:
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
    # except SyntaxError: #ValueError: source code string cannot contain null bytes
    except Exception:
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
            for k in d.copy():

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
            else:
                profiler.stop()#Something tells me its not a good idea to leave stray profilers running...

_PROF_DEEP=True

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

def run_until_complete(x):
    from asyncio import get_event_loop
    return get_event_loop().run_until_complete(x)

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
default_python_input_eventloop = None  # Singleton for python_input
default_ipython_shell = None  # Singleton for python_input
pyin=None# huge speed increase when using this as a singleton
_iPython=False
_printed_a_big_annoying_pseudo_terminal_error=False

# default_pseudo_terminal_settings_file=__file__+".pseudo_terinal_settings"
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
#     _pseudo_terminal_settings=eval(text_file_to_string(file or default_pseudo_terminal_settings_file))
#     return None
# def _save_pseudo_terminal_settings_to_file(file=None):
#     import ast
#     global _pseudo_terminal_settings
#     string_to_text_file(file or default_pseudo_terminal_settings_file,repr(_pseudo_terminal_settings))
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
            try:
                i=input(p if not ol else '')#input
            except ValueError:
                fansi_print("RP INPUT ERROR: Standard-Input file has been closed, which means you can't input any more text!","red","bold")
                raise BaseException("This exception is being raised to shut down RP so you don't get an infinite loop of spam. Please don't use quit() to exit rp, use control+d or the RETURN command")
                return ""
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
_current_ui_style_name='stars',
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
show_all_options=False,
show_last_assignable=False,
show_battery_life=False,
enable_microcompletions=True,
history_syntax_highlighting=False,
history_number_of_lines=2500,
min_bot_space=15,
top_space=0,
    )
_pyin_settings_file_path=__file__+'.rp_pyin_settings'
_globa_pyin=[None]
def _load_pyin_settings_file():
    # print("BOOTLEGER",pyin)
    _globa_pyin[0]=pyin
    try:
        settings=eval(text_file_to_string(_pyin_settings_file_path))
        for setting in _default_pyin_settings:
            assert setting in settings
    except Exception:
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
            global default_ipython_shell
            if default_ipython_shell is None:
                default_ipython_shell=InteractiveShellEmbed()
            if not pyin or _iPython!=iPython:
                pyin=Pyin(default_ipython_shell,get_globals=scope,history_filename=history_filename)
        else:
            if not pyin or _iPython!=iPython:
                # exec(mini_terminal)
                from rp.rp_ptpython.python_input import PythonCommandLineInterface,PythonInput as Pyin
                pyin=Pyin(get_globals=scope,history_filename=history_filename)
        _iPython=iPython
        global default_python_input_eventloop
        # global _pseudo_terminal_settings
        global _pt_pseudo_terminal_init_settings
        if not _pt_pseudo_terminal_init_settings:
            _load_pyin_settings_file()
            _pt_pseudo_terminal_init_settings=True

        pyin.all_prompt_styles['default']=ps.PseudoTerminalPrompt()
        if not currently_running_windows():
            pyin.prompt_style='default'
        # ps.PseudoTerminalPrompt=PseudoTerminalPrompt

        import warnings
        with warnings.catch_warnings():
            #I don't want anything printed to the console while we're typing...it's super annoying
            #Usually these warnings come from autocomplete stumbling upon some property of some library which is deprecated
            #I don't care about this, and it interrupts the typing experience
            default_python_input_eventloop=default_python_input_eventloop or PythonCommandLineInterface(create_eventloop(),python_input=pyin)
        #
        # try:

            code_obj = default_python_input_eventloop.run()
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
        fansi_print("Caught Control+D; preparing to exit rp.pseudo_terminal()  ",'blue','bold')# Presumably in ptpython when you use control+d and then select yes; AKA the exit prompt they built
        return "RETURN"
    except Exception as E:
        if not _printed_a_big_annoying_pseudo_terminal_error:

            if sys.stdout.isatty():#No reason to scare
                try:
                    print_verbose_stack_trace(E)
                except:
                    print_stack_trace(E)
                fansi_print("The prompt_toolkit version of pseudo_terminal crashed; reverting to the command-line version...",'cyan','bold')
            else:
                if running_in_google_colab():
                    reason="you're running in Google Colab, and not in a terminal."
                elif running_in_ipython():
                    reason="you're running in a Jupyter notebook, and not in a terminal."
                else:
                    reason="you're not running in a terminal"
                fansi_print("Defaulting to the command-line (aka PT OFF) version because "+reason,'cyan','bold')

            _printed_a_big_annoying_pseudo_terminal_error=True

        return input(header)
class pseudo_terminal_style:
    def __init__(self):
        self.message=lambda:"pseudo_terminal() --> Entering interactive session! "
        import datetime
        timestamp=lambda:datetime.datetime.now().strftime("%B %d, %Y at %I:%M:%S %p")
        import sys,platform
        version=platform.python_implementation()+' '+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
        self.message=lambda:"rp.pseudo_terminal() in %s: Welcome! "%version+timestamp()
"""
TODO:
    - Does NOT return anything
    - Can be used like MiniTerminal
    - But should be able to accept arguments for niche areas! Not sure how yet; should be modular though somehow...
    - History for every variable
    - Scope Hierarchy: [globals(),locals(),
    others()]:
        - Create new dict that's the composed of all the others then update them accordingly
    - HIST: Contains a list of dicts, whose differences can be seen

"""

def _dhistory_helper(history:str)->list:
    #Take some python code, rip out just the function definitions, and return them in a list
    def get_all_function_names(code:str):        
        #Return all the names of all functions defined in the given code, in the order that they appear
        from rp import line_split,lrstrip_all_lines
        lines=line_split(lrstrip_all_lines(code))
        import re
        defs=[line for line in lines if re.fullmatch(r'\s*def\s+\w+\s*\(.*',line)]
        func_names=[d[len('def '):d.find('(')].strip() for d in defs]
        return func_names

    def _get_function_name(code):
        all_func_names=get_all_function_names(code)
        if all_func_names:
            return all_func_names[0]
        return None

    from collections import OrderedDict
    defstate=True
    #defstate=False
    nondefchunks=[]
    defchunks=[]
    chunk=[]
    defs=OrderedDict()
    decorators=[]
    import re
    for line in line_split(history):
        if line.lstrip()==line and line:
            if defstate==True:
                defcode=line_join(decorators+chunk)
                defchunks.append(defcode)
                defname=_get_function_name(defcode)
                #assert defname is not None
                if defname is not None:
                    defs[defname]=defcode
                decorators=[]
                defstate=False
            if defstate==False:
                if line.startswith('@'):
                    # print(decorators)
                    decorators.append(line)
                else:
                    nondefchunks.append(line_join(chunk))
                    if line.strip() and not bool(re.fullmatch(r'def\s+\w+\s*\(.*',line)):
                        decorators=[]
            chunk=[]
            chunk.append(line)
            defstate = bool(re.fullmatch(r'def\s+\w+\s*\(.*',line))
        else:
            chunk.append(line)    
    if defstate and chunk:
        defcode=line_join(decorators+chunk)
        defchunks.append(defcode)
        defname=_get_function_name(defcode)
        #assert defname is not None
        if defname is not None:
            defs[defname]=defcode 
    
    return defs.values()
       
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

def launch_xonsh():
    #Launch the xonsh shell
    pip_import('xonsh')
    old_sys_argv=sys.argv.copy()
    try:
        sys.argv=old_sys_argv[:1]#Xonsh doesn't like it if we have custom arguments that don't fit xonsh, probably set by using ARG 
        import xonsh.main
        try:
            xonsh.main.main()
        except SystemExit as error:
            #This happens when we press control+d to exit the shell; we get "SystemExit: 0"
            pass
        sys.path.append(".")
    finally:
        #We definitely want to restore the old arguments
        sys.argv=old_sys_argv
    
def number_of_lines(string):
    return string.count('\n')+1 #This is probably more efficient than the line below this one...
    return len(line_split(string))

def number_of_lines_in_terminal(string):
    #Gets the number of lines a string would appear to have when printed in a terminal, assuming the terminal wraps strings
    #For example, the string '*'*1000 is technically only one line, but when printed print('*'*1000) might look like several lines in a terminal
    if not currently_in_a_tty():
        #Perhaps just return 1 if we're not in a TTY? Some places, like jupyter notebooks, don't wrap lines
        #For now, we'll ignore this edge case. In the future this block might return something different.
        pass
    lines=line_split(string)
    width=get_terminal_width()
    out=0
    for line in lines:
        out+=len(line)//width+1
    return out

def number_of_lines_in_file(filename):
    #Quickly count the nubmer of lines in a given file.
    #It's 5-10x faster than text_file_to_string(filename).count('\n')
    #It also appears to take constant memory; my memory usage didn't flinch even when I threw a 2gb file at it.
    #Note that it doesn't care if it's a text file or not; it just counts the number of \n bytes in the file!
    #   For example, number_of_lines_in_file('picture.jpg')==280 is a possibility.
    #https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    from itertools import (takewhile,repeat)
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )+1

def _all_files_listed_in_exception_traceback(exception:BaseException)->list:
    from traceback import format_exception,format_exception

    error=exception
    error_string=''.join(format_exception(error.__class__,error,error.__traceback__))
    ans=error_string
    import re
    ans=line_split(ans)
    ans=[line for line in ans if re.fullmatch(r'  File .*, line \d+.*',line)]
    #ans=[line for line in ans if re.fullmatch(r'  File .*, line \d+, in .*',line)]
    def process_line(line):
        #Usually a line will look like this:
        #    ans =   File "/home/ryan/anaconda3/lib/python3.7/copy.py", line 240, in _deepcopy_dict
        #     ➤ split_python_tokens(ans)
        #    ans = ['  ', 'File', ' ', '"', '/home/ryan/anaconda3/lib/python3.7/copy.py', '"', ',', ' ', 'line', ' ', '240', ',', ' ', 'in', ' ', '_deepcopy_dict']
        try:    
            tokens=split_python_tokens(line)
            path=tokens[4]
            assert path_exists(path)
            line=int(tokens[10])
            return path,line
        except Exception:
            return None
    ans=list(map(process_line,ans))
    ans=[x for x in ans if x is not None]
    return ans

    #Older version below (which sometimes missed a few files or got the linenumber wrong)
    tb=exception.__traceback__
    out=[]
    while hasattr(tb,'tb_next'):
        try:
            frame=tb.tb_frame
            code =frame.f_code
            tb=tb.tb_next
            #frame=frame.f_back
            # out.append((code.co_filename,code.co_firstlineno))
            out.append((code.co_filename,tb.tb_lineno))
        except Exception:
            pass
    return out

def is_symbolic_link(path:str):
    #Returns whether or not a given path is a symbolic link
    from pathlib import Path
    return Path(path).is_symlink()

def _guess_mimetype(file_path)->str:
    import mimetypes
    if not file_exists(file_path):
        return None
    mimetype=mimetypes.guess_type(file_path)[0] #mimetype should be something like 'image/jpeg'
    if mimetype is None:
        return None
    return mimetype.split('/')[0]

def is_image_file(file_path):
    return _guess_mimetype(file_path)=='image'

def is_video_file(file_path):
    return _guess_mimetype(file_path)=='video'

def is_sound_file(file_path):
    return _guess_mimetype(file_path)=='audio'

def is_utf8_file(path):
    #Returns True iff the file path is a UTF-8 file
    #Faster than trying to use text_file_to_string(path), because it doesn't need to read the whole file
    if not file_exists(path):
        return False
    import codecs
    try:
        f = codecs.open(path, encoding='utf-8', errors='strict')
        next(f)
        return True
    # except UnicodeDecodeError:
    except Exception:
        return False
# is_text_file=is_utf8_file #TODO: Not sure if this is the right way to do it
        
def display_file_tree(root=None,*,all=False,only_directories=False,traverse_symlinks=False):
    #This code was ripped off of somewhere online, I don't remember where. Search the body of this code on google and you should find it in some github repo that implements the tree command in multiple languages
    import os
    import sys

    printed_lines=[]
    
    def print_line(line):
        print(line)
        printed_lines.append(line)

    def get_stats_string(path):
        def is_hidden_file(file):
            return get_file_name(file).startswith('.')

        stats=[]
        color='blue'
        image_file_extensions='png jpg jpeg bmp gif tiff tga'.split()
        if is_a_folder(path):
            try:
                files=get_all_paths(path,include_files=True,include_folders=False,recursive=False)
            except PermissionError:
                #Skip directories we don't have access to, as opposed to crashing
                files=[]

            all_unhidden_file_extensions=([get_file_extension(file) for file in files if not is_hidden_file(file)])
            if len(set(all_unhidden_file_extensions))==1:
                extension=all_unhidden_file_extensions[0]
                if extension.strip():
                    stats.append('%i .%s file'%(len(all_unhidden_file_extensions),extension)+('s' if len(files)!=1 else ''))
                    if extension in image_file_extensions:
                        dims=None
                        try:
                            display_dims=True
                            for file in shuffled(files)[:15]:#Take only a random sample size of the image files for the sake of speed. Most likely it will be correct.
                                dim=get_image_file_dimensions(file)
                                if dims is None:
                                    dims=dim
                                if dims!=dim:
                                    display_dims=False
                                    break
                        except Exception:
                            display_dims=False
                        if display_dims:
                            stats.append('x'.join(map(str,dims)))
                        # else:
                        #     stats.append('(mixed sizes)')
                else:
                    stats.append('%i file'%(len(all_unhidden_file_extensions),)+('s' if len(files)!=1 else ''))
                    # stats.append('%i (no file extension) file'%(len(all_unhidden_file_extensions),)+('s' if len(files)!=1 else ''))
            else:
                if len(files)>0:
                    stats.append('%i file'%len(files)+('s' if len(files)!=1 else ''))#Number of files in the folder

            if is_symbolic_link(path):
                color='yellow'
                stats.append('is symlink')

        elif is_a_file(path):
            stats.append(get_file_size(path,human_readable=True))
            extension=get_file_extension(path)
            if extension in image_file_extensions:
                try:
                    stats.append('x'.join(map(str,get_image_file_dimensions(path))))
                except Exception:pass#Maybe it wasn't actually an image file...

            if get_file_size(path,human_readable=False) < 1024*1024*16 and is_utf8_file(path): #If the file is under 16 megabytes large (an arbitrary threshold I use to make sure it's not too slow)
                #TODO: Check to see if is a UTF-8 file
                # import codecs
                # codecs.open(filename, encoding='utf-8', errors='strict')
                #For small files, display the number of lines in the file (assume it's a text file)
                stats.append('%i lines'%number_of_lines_in_file(path))
            if is_utf8_file(path) and get_file_extension(path)=='csv':
                #If it's a CSV file, display the number of columns in that file
                try:
                    import csv
                    number_of_columns=len(next(csv.reader(open(path,'r'), delimiter=',')))
                    stats.append('%i cols'%number_of_columns)
                except Exception:
                    pass
            #Getting number of lines was too slow on large files;
            #else:
            #    try:
            #        #if it's a text file, say how many lines it has
            #        string=text_file_to_string(path)
            #        sum(1 for i in open(path, 'rb'))#https://stackoverflow.com/questions/9629179/python-counting-lines-in-a-huge-10gb-file-as-fast-as-possible

            #        # stats.append(str(number_of_lines(string))+' lines')
            #    except Exception:pass

        if stats:       
            return ' '*4 + '\t' + fansi('['+', '.join(stats)+']',color)
        else:
            return ''

    def highlight_child(child,absolute):
        if is_a_folder(absolute):
            return fansi(child,'blue','bold')
        else:
            return child

    class Tree:
        def __init__(self):
            self.dirCount = 0
            self.fileCount = 0

        def register(self, absolute):
            if os.path.isdir(absolute):
                self.dirCount += 1
            else:
                self.fileCount += 1

        def summary(self):
            return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

        def walk(self, directory, prefix = ""):
            if not is_a_folder(directory):
                return#??? This hack shouldn't be nessecary...
            try:
                filepaths = sorted([filepath for filepath in os.listdir(directory)])
                if only_directories:
                    # fansi_print("all filepaths:"+str(filepaths),'yellow')
                    filepaths=[filepath for filepath in filepaths if is_a_folder(path_join(directory,filepath))]
            except PermissionError:
                #Just in case we get some access-denied error
                filepaths = []
            for index in range(len(filepaths)):
                if not all and filepaths[index][0] == ".":
                    continue

                absolute = os.path.join(directory, filepaths[index])
                self.register(absolute)
    
                recurse=os.path.isdir(absolute) and traverse_symlinks or not is_symbolic_link(absolute)

                entry= highlight_child(filepaths[index],absolute)+get_stats_string(absolute)
                if index == len(filepaths) - 1:
                    print_line(prefix + "└── " + entry)
                    if recurse:
                        self.walk(absolute, prefix + "    ")
                else:
                    print_line(prefix + "├── " + entry)
                    if recurse:
                        self.walk(absolute, prefix + "│   ")

    try:
        directory = "." if root is None else root
        #if len(sys.argv) > 1:
            #directory = sys.argv[1]
        print_line(directory)

        tree = Tree()
        tree.walk(directory)
        print_line("\n" + tree.summary())

    except KeyboardInterrupt:
        #If the user gets tired of waiting and just wants the half-baked results, let them have it...
        print_line(fansi("...(incomplete due to a keyboard interrupt, probably because you pressed Control+C before we finished dipslaying the file tree)...",'red','underlined'))
    _maybe_display_string_in_pager(line_join(printed_lines))
    # if len(printed_lines)>get_terminal_height()*.75 and sys.stdout.isatty():
    #     display=(line_join(printed_lines))
    #     display=_line_numbered_string(display)
    #     display=(fansi("TREE: There were a lot of lines in the output (%i), so we're using rp.string_pager() to show them all. Press 'q' to exit, or press 'h' for more opttions."%len(printed_lines),'blue','bold'))+'\n'+displa
    #     string_pager(display)

def _line_numbered_string(string,foreground='cyan',style='bold',background='blue'):
    lines=line_split(string)
    nlines=len(lines)
    numwidth=len(str(nlines))
    newlines=[fansi(str(i+1).rjust(numwidth)+' '*0,foreground,style,background)+e for i,e in enumerate(lines)]
    return line_join(newlines)

                        

def _vimore(exception):
    try:
        files_and_line_numbers = _all_files_listed_in_exception_traceback(exception)
    except Exception as e:
        pass
    # print("JOLLY")
        # print_verbose_stack_trace(e)
    files_and_line_numbers = [(lineno,file) for file,lineno in files_and_line_numbers if file_exists(file)]

    if not files_and_line_numbers:
        fansi_print('   (There are no editable files in the error\'s traceback)','red')
    
    def localized_path(path):
        #Return either the global or the local path, whichever is more concise
        rel=get_relative_path(path)
        #if rel.startswith('..'):
        if rel.count('/')<path.count('/'):
            return rel
        else:
            return path
        
    colno=0 #I'm not sure how to tell which column number an error occured on
    lineno,path= input_select(
            question =fansi('Please choose a linenumber/file pair from the last traceback:',None,'bold') + '\n' + '    ' + \
                      fansi('pwd: ') + fansi(get_current_directory(),'yellow')
                ,
            options  =files_and_line_numbers,
            stringify=lambda item: fansi(str(item[0]).rjust(6),'cyan') +'  '+ localized_path(item[1])
            )
    
    import subprocess
    #https://stackoverflow.com/questions/3313418/starting-vim-at-a-certain-position-line-and-column-of-a-file
    #              ┌                                                              ┐
    #              │┌                                                            ┐│
    subprocess.call(["vim",path,'+call cursor(%i,%i)'%(lineno,colno),'+normal zz'])
    #              │└                                                            ┘│
    #              └                                                              ┘
    return path

def _load_text_from_file_or_url(location):
    if is_valid_url(location):
        import requests
        url=location
        response=requests.request('GET',url)
        text=response.text
    elif file_exists(location):
        text=text_file_to_string(location)
    else:
        assert False,"Neither a text file nor a url: "+repr(location)+"\nERROR: This is neither a valid url nor a text file"
    return text

_warning_ignore_filter=('ignore',None,Warning,None,0)
def _warnings_on():
    import warnings
    warnings.filters=[x for x in warnings.filters if x!=_warning_ignore_filter]
def _warnings_off():
    import warnings
    warnings.filters=[_warning_ignore_filter]+warnings.filters
def _warnings_are_off():
    import warnings
    return _warning_ignore_filter in warnings.filters

def _rma(ans):
    if not isinstance(ans,str):
        raise TypeError('RMA: ans should be a str pointing to a file path, but ans is a '+str(type(ans)))
    if not path_exists(ans):
        raise FileNotFoundError(ans)
    ans=get_absolute_path(ans)
    if input_yes_no("Are you sure you want to delete %s?"%ans):
        delete_path(ans)
        print('Deleted path: '+ans)
    else:
        print('Deletion cancelled.'+ans)

#def pudb_shell(_globals,_locals_):
#    #https://documen.tician.de/pudb/shells.html
#    pseudo_terminal(_globals,_locals)

_cd_history=[]
def pseudo_terminal(*dicts,get_user_input=python_input,modifier=None,style=pseudo_terminal_style(),enable_ptpython=True,eval=eval,exec=exec,rprc=''):
    try:
        import signal
        signal.signal(signal.SIGABRT,lambda:"rpy: pseudo terminal: sigabrt avoided!")
    except Exception as E:
        fansi_print("Warning: This pseudo_terminal is being started in a separate thread",'yellow')
        # print_stack_trace(E)
    import re
    
    import sys
    pwd=get_current_directory()
    if pwd not in sys.path:
        sys.path.append(pwd)

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
        fansi_print(style.message() +' '+ level_label(),'blue','bold')
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
        except Exception:pass

        def scope():
            return merged_dicts(*reversed(dicts))

        def equal(a,b):
            if a is b:
                return True

            try:
                #Uses the Dill library...
                if handy_hash(a)==handy_hash(b):
                    return True
                else:
                    return id(a)==id(b)
            except Exception as e:
                pass


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
            except Exception:pass
            return a is b # Will always return SOMETHING at least

        class UndoRedoStack():
            #TODO: This can be used for PREV, NEXT, CDB, UNDO, REDO, PREVMORE, NEXTMORE
            def __init__(self,clear_redo_on_do=True):
                self.undo_stack=[]
                self.redo_stack=[]
                self.clear_redo_on_do=clear_redo_on_do

            def can_undo(self):
                return len(self.undo_stack)!=0

            def can_redo(self):
                return len(self.redo_stack)!=0

            def undo(self):
                output=self.undo_stack.pop()
                self.redo_stack.insert(0,output)
                return output
                
            def redo(self):
                output=self.redo_stack.pop(0)
                self.undo_stack.append(output)
                return output
                
            def do(self,value):
                if self.clear_redo_on_do:
                    self.redo_stack.clear()
                self.undo_stack.append(value)

            def do_if_new(self,value):
                if self.undo_stack and self.undo_stack[-1]==value:
                    return
                self.do(value)

        error_stack=UndoRedoStack(clear_redo_on_do=False)

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
            import time
            start=time.time()
            if snapshots_enabled:
                snapshot_history.append(get_snapshot())
            if not gave_undo_warning and time.time()-start>.25:#.25 seconds is way too long to wait for a new prompt. We're delaying the prompt, and this can get annoying quickly...
                fansi_print("NOTE: ",'blue','bold',new_line=False)
                fansi_print("pseudo_terminal took "+str(start())[:5]+" seconds to save the UNDO snapshot, which might be because of a large namespace. If your prompts are lagging, this is probably why. You can fix this by using 'UNDO ALL', 'UNDO OFF'. This message will only show once.",'blue','bold')
                gave_undo_warning=True

        def get_ans():
            dupdate(dicts[0],'ans')
            return  dicts[0]['ans']# This should exist

        should_print_ans=True
        # A little python weridness demo: ⮤print(999 is 999)⟶True BUT ⮤a=999⮤print(a is 999)⟶False
        use_ans_history=True
        def set_ans(val,save_history=True,snapshot=True,force_green=False):
            try:    
                import rp.r_iterm_comm as ric
                ric.ans=val
                save_history&=use_ans_history
                dupdate(dicts[0],'ans')
                if snapshot:# default: save changes in a snapshot BEFORE making modifications to save current state! snapshot_history is independent of ans_history
                    take_snapshot()
                if save_history:
                    ans_history.append(val)
                dicts[0]['ans']=val
            except Exception as e:
                print_verbose_stack_trace(e)
                print("HA HA CAUGHT YOU LA SNEAKY LITTLE BUG! (Idk if this ever errors...but when it might...it's rare")

            if should_print_ans!=False:
                try:
                    #__str__ returned non-string (type NoneType)
                    val_str=str(val)
                except TypeError as error:
                    val_str='(Error when converting ans to string: %s)'%error
                try:
                    import numpy as np
                    set_numpy_print_options(linewidth=max(0,get_terminal_width()-len('ans = ')))#Make for prettier numpy printing, by dynamically adjusting the linewidth each time we enter a command

                    if type(val).__name__ in 'ndarray DataFrame Series Tensor'.split() and len(line_split(val_str))>1:#Recognize pandas dataframes, series, numpy Arrays, pytorch Tensors
                    # if isinstance(val,np.ndarray) and len(line_split(val_str))>1:
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
                except Exception:pass#print("Failed to set numpy width")# AttributeError: readonly attribute '__module__'
                fansi_print("ans = " + val_str,('green'if save_history or force_green else 'yellow')if use_ans_history else 'gray')

        def print_history(return_as_string_instead_of_printing=False):
            output=''
            output+=fansi("HISTORY --> Here is a list of all valid python commands you have entered so far (green means it is a single-line command, whilst yellow means it is a multi-lined command):",'blue','underlined')+'\n'
            flipflop=False
            def fansify(string,*args):
                return line_join([fansi(line,*args) for line in line_split(string)])
            for x in  successful_command_history:
                multiline='\n' in x
                if x.strip():#And x.strip() because we don't want to alternate bolding if it's invisible cause then it would look like we have two bold in a row
                    flipflop=not flipflop#Print every other yellow prompt in bold
                output+=fansify(x,'yellow' if multiline else'green','bold' if multiline and flipflop else None)+'\n'# Single line commands are green, and multi-line commands are yellow
            if return_as_string_instead_of_printing:
                return output
            else:
                print(end=output)
                _maybe_display_string_in_pager(output,with_line_numbers=False)

        def show_error(E):
            error_stack.do_if_new(E)
            nonlocal error,display_help_message_on_error,error_message_that_caused_exception
            if display_help_message_on_error:
                display_help_message_on_error=False
                fansi_print("""Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command aborted.
            Type 'HELP' for instructions on how to use pseudo_terminal in general.
            To see the full traceback of any error, type either 'MORE' or 'MMORE' (or alt+m as a shortcut).
            NOTE: This will be the last time you see this message, unless you enter 'HELP' without quotes.""",'red','bold')
            error_message_that_caused_exception=user_message# so we can print it in magenta if asked to by 'MORE'
            # print_verbose_stack_trace(E)
            print_stack_trace(E,False,'ERROR: ')
            error=E
        error_message_that_caused_exception=None
        display_help_message_on_error=True# A flag that will turn off the first time it displays "Sorry, but that command caused an error that pseudo_terminal couldn't fix! Command aborted. Type 'HELP' for instructions on pseudo_terminal. To see the full error traceback, type 'MORE'." so that we don't bombard the user with an unnessecary amount of stuff
        pwd_history=[]
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
        warned_about_ans_print_on=False
        do_garbage_collection_before_input=False#I'm going to see if this makes it faster when doing stuff with pytorch
        _reload=False#If this is true, call _reload_modules right before each exeval is called
        global _printed_a_big_annoying_pseudo_terminal_error
        # garbage_collector_timer=tic()

        def pterm_pretty_print(value,*args,**kwargs):
            #If it's a string with valid python code, highlight it
            #Otherwise, pretty_print it
            if isinstance(value,str) and is_valid_python_syntax(value):
                highlighted_code=fansi_syntax_highlighting(value)
                print(highlighted_code)
                _maybe_display_string_in_pager(highlighted_code)
            else:
                pretty_print(value,*args,**kwargs)
            return

            #from contextlib import redirect_stdout
            #import io


            #f = io.StringIO()
            #with redirect_stdout(f):
            #    pretty_print(value,*args,**kwargs)
            #    help(pow)
            #s = f.getvalue()

            #print(s)
            #_maybe_display_string_in_pager(s)
            #return s
        try:
            #TODO: For some reason psuedo_terminal doesnt capture the scope it was called in. IDK why. Fix that. The next few lines are a patch and should eventually not be nesecay once bugs are fixed.
            exeval("None",*dicts,exec=exec,eval=eval)#I don't know why this is necessary (and haven't really tried to debug it) but without running something before importing all from rp nothihng works....
            exeval(rprc,*dicts,exec=exec,eval=eval)#Try to import RP
        except BaseException as e:
            print("PSEUDO TERMINAL ERROR: FAILED TO IMPORT RP...THIS SHOULD BE IMPOSSIBLE...WAT")
            print_stack_trace(e)
        def add_to_successful_command_history(x):
            _write_to_pterm_hist(x)
            successful_command_history.append(x)
            import rp.r_iterm_comm
            rp.r_iterm_comm.successful_commands=successful_command_history.copy()
        help_commands_string="""
        <Input Modifier>
        MOD ON
        MOD OFF
        MOD SET
        SMOD SET

        <Stack Traces>
        MORE
        MMORE
        DMORE
        AMORE
        GMORE
        HMORE
        VIMORE
        PIPMORE
        IMPMORE
        PREVMORE
        NEXTMORE

        <Command History>
        HISTORY    (HIST)
        GHISTORY   (GHIST)
        AHISTORY   (AHIST)
        CHISTORY   (CHIST)
        DHISTORY   (DHIST)
        VHISTORY   (VHIST)
        ALLHISTORY (ALLHIST)

        <Clipboards>
        COPY
        PASTE
        EPASTE
        WCOPY
        WPASTE
        TCOPY
        TPASTE
        LCOPY
        LPASTE
        VCOPY
        VPASTE
        FCOPY
        FPASTE
        MLPASTE

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
        PT

        <RP Settings>
        PT SAVE
        PT RESET
        SET STYLE

        <Shell Commands>
        !
        !!

        <Simple Timer>
        TICTOC
        TICTOC ON
        TICTOC OFF

        <Profiler>
        PROF
        PROF ON
        PROF OFF

        <Toggle Colors>
        FANSI ON
        FANSI OFF

        <Module Reloading>
        RELOAD ON
        RELOAD OFF

        <Documentation>
        HELP
        HHELP
        SHORTCUTS

        <Startup Files>
        RPRC
        VIMRC
        TMUXRC
        XONSHRC
        RYAN RPRC
        RYAN VIMRC
        RYAN TMUXRC
        RYAN XONSHRC

        <Inspection>
        ?
        ??
        ???
        ?.
        ?v
        ?s
        ?t
        ?h (?/)
        ?e
        ?p
        ?c
        ?i

        <Others>
        RETURN  (RET)
        SUSPEND (SUS)
        WARN
        GPU
        TOP
        TAB
        TABA
        MONITOR
        UPDATE
        ANS PRINT ON   (APON)
        ANS PRINT OFF  (APOF)
        ANS PRINT FAST (APFA)
        SHELL (SH)
        LEVEL
        DITTO
        EDIT
        VARS
        RANT
        FORK
        WANS
        ARG
        VIM
        VIMH
        VIMA
        AVIMA
        GC OFF
        GC ON
        GC

        <Unimportant>
        NUM COM
        PROF DEEP
        CDH CLEAN
        ALS
        ALSD
        ALSF
        ?r

        <File System>
        RM
        LS
        LST
        FD
        CD
        CDP
        CDA
        CDB
        CDU
        CDH
        CDZ
        CDQ
        CAT
        NCAT
        CCAT
        ACAT
        CATA
        NCATA
        CCATA
        ACATA
        RUN
        RUNA
        SRUNA
        SSRUNA
        PWD
        CPWD
        APWD
        TAKE
        MKDIR
        OPEN
        OPENH
        OPENA
        DISK
        DISKH
        TREE    
        TREE ALL   
        TREE DIR
        TREE ALL DIR
        FD SEL (FDS)
        LS SEL (LSS)
        LS REL (LSR)
        LS FZF (LSZ)
        LS QUE (LSQ)
        RANGER (RNG)
        """
        # """
        # <Broken>
        # RYAN PUDBRC
        # IPYTHON
        # IPYTHON ON
        # IPYTHON OFF
        #
        # <Truly Unimportant>
        # IHISTORY (IHIST)
        # """

        help_commands=[]#All commands, so we can search through them and turn uncapitablized ones into capitalized ones
        for line in help_commands_string.splitlines():
            if '#' in line or  not line.strip() or not line.replace(' ','').replace('(','').replace(')','').isalpha():
                #Skip <Documentation>, ???, blank lines etc
                continue
            line=line.strip()
            if '(' in line:
                #LS SEL (LSS) --->  LS SEL   and    LSS
                first_help_command=line[:line.find('(')].strip()
                second_help_command=line[line.find('('):].strip()[1:-1].strip()
                help_commands.append(first_help_command)
                help_commands.append(second_help_command)
            else:
                help_command=line.strip()
                help_commands.append(help_command)
        help_commands_no_spaces_to_spaces={x.replace(' ',''):x for x in help_commands}
        # print(help_commands)#Should be like ['MOD ON', 'MOD OFF', 'MOD SET', 'SMOD SET.....


        #TODO: Make APOF, APON etc implemented HERE, not elsewhere.
        #TODO: Make these configurable in rprc
        #There are duplicate shortcuts. This is a good thing! They don't interfere with variables.
        #Example: H and HI. Maybe there's a variable called H. You can still use HI.
        rp_import="__import__('rp')."
        command_shortcuts_string='''
        M  MORE
        MM MMORE
        DM DMORE
        GM GMORE
        HM HMORE
        AM AMORE
        VM VIMORE
        PM PIPMORE
        IM IMPMORE
        UM PREVMORE
        NM NEXTMORE

        HI  HIST
        DH  DHIST
        DHI DHIST
        CH  CHIST
        CHI CHIST
        GH  GHIST
        GHI GHIST
        AH  AHIST
        AHI AHIST
        VH  VHIST
        VHI VHIST

        H HELP
        HE HELP
        HH HHELP
        SC SHORTCUTS

        CO  COPY
        WC  WCOPY
        WCO WCOPY
        LC  LCOPY
        LCO LCOPY
        TC  TCOPY
        TCO TCOPY
        VCO VCOPY
        VC  VCOPY

        EPA EPASTE
        EP  EPASTE
        PA  PASTE
        WP  WPASTE
        WPA WPASTE
        VP  VPASTE
        VPA VPASTE
        LP  LPASTE
        LPA LPASTE
        TP  TPASTE
        TPA TPASTE
        FP FPASTE
        FPA FPASTE
        FC FCOPY
        MLP MLPASTE
        RPA PASTE

        AA ACATA
        ACA ACATA
        AC ACAT
        CA CAT
        CAA CATA

        WN WARN
        WR WARN

        TT TICTOC

        TA TAKE
        TK TAKE
        MK MKDIR
        MA MKDIR

        PF PROF
        PO PROF

        N  NEXT
        P  PREV
        NN NEXT
        PP PREV
        
        UP UPDATE

        B CDB
        U CDU

        CDC cdhclean
        CCL cdhclean
        
        HC CDH
        HD CDH

        DA CDA

        RU RUN
        RN RUN
        SSRA SSRUNA
        SSA  SSRUNA
        SSR  SSRUNA
        SS   SSRUNA
        SRA   SRUNA
        SA    SRUNA
        SR    SRUNA
        RA RUNA
        EA RUNA

        V VIM
        VI VIM
        AV AVIMA
        AVA AVIMA
        VA VIMA
        VHE VIMH
        VIH VIMH

        GO GC

        MON MONITOR

        TRAD treealldir
        TRD treedir
        TR tree
        TRA treeall

        FON fansion
        FOF fansioff
        FOFF fansioff

        RRC ryanrprc
        RTC ryantmuxrc
        RVC ryanvimrc
        RXC ryanxonshrc
        RR  ryanrprc
        RT  ryantmuxrc
        RV  ryanvimrc
        RX  ryanxonshrc

        LSF LSQ
        FDZ LSZ
        FDQ LSQ

        RG RNG
        VS VARS

        OP OPEN
        OPH OPENH
        OH OPENH
        OPA OPENA
        OA OPENA

        LVL LEVEL
        LV LEVEL
        L LEVEL

        DK DISK
        DD DITTO
        DT DITTO
        DO DITTO

        PW PWD
        PD PWD
        WD PWD
        APW APWD
        AP  APWD
        AW  APWD

        WA WANS

        LSA ALS
        LSAD ALSD
        LSAF ALSF

        quit() RETURN
        exit() RETURN

        DKH DISKH
         KH DISKH
        GOO $open_google_search_in_web_browser(str(ans))
        ALSF $get_all_paths(get_current_directory(),include_files=True,include_folders=False,relative=True)
        SMI $os.system("nvidia-smi");
        NVT $os.system("nvtop");#sudo_apt_install_nvtop
        ZSH $os.system("zsh");
        BA   $os.system("bash");
        S   $os.system("sh");
        Z   $os.system("zsh");
        NB  $extract_code_from_ipynb()
        NBA  $extract_code_from_ipynb(ans)
        NBC  $r._clear_jupyter_notebook_outputs()
        NBCA $r._clear_jupyter_notebook_outputs(ans)
        NCA  $r._clear_jupyter_notebook_outputs(ans)
        INS $input_select("Select:",ans)
        ISA $input_select("Select:",ans)
        VCL $delete_file($get_absolute_path('~/.viminfo'))#VimClear_use_when_VCOPY_doesnt_work_properly
        IASM $import_all_submodules(ans,verbose=True);
        SUH $sublime('.')
        SUA $sublime(ans)
        COH $vscode('.')
        COA $vscode(ans)
        SG $save_gist(ans)
        LG $load_gist(input($fansi('URL:','blue','bold')))
        LGA $load_gist(ans)
        OG $load_gist($input_select(options=$line_split($text_file_to_string($path_join($get_parent_folder($get_module_path($rp)),'old_gists.txt')))))
        CAH  $copy_path(ans,'.')
        CPAH $copy_path(ans,'.')
        MAH  $move_path(ans,'.')
        MVAH $move_path(ans,'.')

        GCLP $git_clone($string_from_clipboard())
        GCLA $git_clone(ans)
        GURL $get_git_remote_url()

        RF    $random_element($get_all_files())
        RD    $random_element($get_all_directories())
        RE    $random_element(ans)

        DCI $display_image_in_terminal_color(ans)
        
        FCA $web_copy_path(ans)
        RMA $r._rma(ans)

        RST __import__('os').system('reset')
        RS  __import__('os').system('reset')

        DAPI __import__('rp.pypi_inspection').pypi_inspection.display_all_pypi_info()

        '''.replace('$',rp_import)
        # SA string_to_text_file(input("Filename:"),str(ans))#SaveAnsToFile
        # BB set_current_directory(r._get_cd_history()[-2]);fansi_print('BB-->CDH1-->'+get_current_directory(),'blue','bold')#Use_BB_instead_of_CDH_<enter>_1_<enter>_to_save_time_when_starting_rp
        #Note: \x20 is the space character
        command_shortcuts=line_split(command_shortcuts_string)
        command_shortcuts=list(map(str.strip,command_shortcuts))
        command_shortcuts=[x for x in command_shortcuts if x]
        command_shortcuts_pairs=list(map(str.split,command_shortcuts))
        command_shortcuts={x:y for x,y in command_shortcuts_pairs}
        for key in list(command_shortcuts):
            command_shortcuts[key.lower()]=command_shortcuts[key]#Make it case-insensitive

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
                        def try_eval(x,true=False):# If true==True, then we return the actual value, not a formatted string
                            # region Communicate with ptpython via r_iterm_comm
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





                        if get_current_directory()=='.':
                            fansi_print("WARNING: Current directory was deleted; moving to a new location",'yellow','bold')
                            set_current_directory('/')
                            fansi_print("PWD: "+get_current_directory(),"blue",'bold')

                        user_message=get_user_input(lambda:scope(),header=_get_prompt_style(),enable_ptpython=enable_ptpython)
                        try:set_numpy_print_options(linewidth=max(0,get_terminal_width()-len('ans = ')))#Make for prettier numpy printing, by dynamically adjusting the linewidth each time we enter a command
                        except Exception:pass#print("Failed to set numpy width")
                        if not user_message:
                            continue# A bit of optimization for aesthetic value when we hold down the enter key
                        allow_keyboard_interrupt_return=False
                    except (KeyboardInterrupt,EOFError):
                        if allow_keyboard_interrupt_return:
                            fansi_print("Caught repeated KeyboardInterrupt or EOFError --> RETURN",'cyan','bold')
                            while True:
                                try:
                                    if input_yes_no("Are you sure you want to RETURN?"):
                                        user_message="RETURN"
                                        break
                                    else:
                                        break
                                except:
                                    print("<KeyboardInterrupt>\nCaught another KeyboardInterrupt or EOFError...if you'd like to RETURN, please enter 'yes'")
                                    pass
                        else:
                            allow_keyboard_interrupt_return=True
                            raise
                    # endregion
                    user_created_var_names&=set(scope())# Make sure that the only variables in this list actually exist. For example, if we use 'del' in pseudo_terminal, ∄ code to remove it from this list (apart from this line of course)
                    # region Non-exevaluable Terminal Commands (Ignore user_message)
                    _update_cd_history()

                    import re
                    if not '\n' in user_message and '/' in user_message and not ' ' in user_message:
                        #Avoid the shift key when doing r?v by letting you do r/v (assuming v doesn't exist)
                        #When applicable, let thing/v --> thing?v  and  /v  -->  ?v
                        #Likewise, let /s --> ?s etc
                        #not ' ' in user_message is just a good heuristic
                        split=user_message.split('/')
                        left=''.join(split[:-1])
                        right=split[-1]
                        if right in 'p e s v t h c r i'.split():
                            #/p --> ?p   /e --> ?e   /t --> ?t   /s ---> ?s    /v --> ?v     /h --> ?h     /c --> ?c     /r --> ?r    /i --> ?i
                            if not right in scope():
                                user_message=left+'?'+right
                                fansi_print("Transformed input to "+repr(user_message)+' because variable '+repr(right)+' doesn\'t exist','magenta','bold')

                    # if 'PWD' in help_commands:
                    #     print("JAJAJA")
                    # if 'vim' in scope():
                    #     print("GLOO GLOO")
                        
                    if user_message in command_shortcuts and user_message not in scope():
                        original_user_message=user_message
                        user_message=command_shortcuts[user_message]
                        fansi_print("Transformed input to "+repr(user_message)+' because variable '+repr(original_user_message)+' doesn\'t exist but is a shortcut in SHORTCUTS','magenta','bold')

                    if user_message.strip().isalpha() and user_message.strip() and user_message.islower() and not user_message.strip() in scope() and user_message.upper().strip() in help_commands_no_spaces_to_spaces:
                        original_user_message=user_message
                        user_message=user_message.upper().strip()
                        user_message=help_commands_no_spaces_to_spaces[user_message]#Allow 'ptoff' --> 'PT OFF'
                        fansi_print("Transformed input to "+repr(user_message)+' because variable '+repr(original_user_message)+' doesn\'t exist but '+user_message+' is a command','magenta','bold')

                    if user_message == 'RETURN' or user_message =='RET':
                        try:
                            if get_ans() is None:
                                fansi_print("rp.pseudo_terminal(): Exiting session. No value returned.",'blue','bold')
                            else:
                                fansi_print("rp.pseudo_terminal(): Exiting session. Returning ans = " + str(get_ans()),'blue','bold')
                            return get_ans()
                        except Exception as e:
                            print_verbose_stack_trace(e)
                            fansi_print("rp.pseudo_terminal(): Exiting session. Failed to call get_ans() (this is a strange, rare error). Returning ans = None",'blue','bold')
                            return None#Sometimes, calling get_ans() fails

                    elif user_message=='SHORTCUTS':
                        lines=[]
                        lines.append(fansi("Showing all pseudo-terminal command shortcuts:\n    * NOTE: Shortcuts are not case sensitive!",'green','bold'))
                        
                        for x,y in command_shortcuts_pairs:
                            if x.isupper():
                                lines.append(fansi(x.ljust(4),'cyan','bold')+'  -->  '+fansi(y.replace(rp_import,''),'blue','bold'))
                        print(line_join(lines))
                        _maybe_display_string_in_pager(line_join(lines),False)


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
                            height=55#Total height of output
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
                        strings_input=help_commands_string
                        strings_input=lrstrip_all_lines(strings_input)
                        command_list=columnify_strings(strings_input)

                        display_help_message_on_error=True# Seems appropriate if they're looking for help
                        fansi_print("HELP --> Here are the instructions:",'blue','underlined')
                        fansi_print("""    For those of you unfamiliar, this will basically attempt to exec(input()) repeatedly.",'blue')
        For more documentation, type 'HHELP'
        NOTE: If you're using linux, please use 'sudo apt-get install xclip' to let rp access your system's clipboard
        Note that you must import any modules you want to access; this terminal runs inside a def.
            If the command you enter returns a value other than None, a variable called 'ans' will be assigned that value.
        If the command you enter returns an error, pseudo_terminal will try to fix it, and if it can't it will display a summary of the error.
        To set different prompt styles, use set_prompt_style(' >> ') or set_prompt_style(' ⮤ ') etc. This currently only works with PT ON. This setting will be saved between sessions.
        To launch the debugger, type debug() on the top of your code. HINT: Typing the microcompletion '\\de' will toggleååååå this for you.
        Enter 'HISTORY' without quotes to get a list of all valid python commands you have entered so far, so you can copy and paste them into your code.
        NOTE: 
        Enter 'EPASTE' without quotes to run what is copied to your clipboard, allowing you to run multiple lines at the same time
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
        Sometimes, you don't have to type a command in all caps. For example, 'pwd' acts like 'PWD' if there's no variable called 'pwd'. This saves you from having to reach to the shift key. Other examples: 'tictocon'-->'TICTOC ON', 'gcon'-->'GC ON'
        Sometimes, you can use "some_variable/v" in place of "some_variable?v" when variable v doesn't exist, to save you from having to reach for the shift key. This also works for "/s"-->"?s", "/p"-->"?e" etc.
        The ?. command has some variations. r?.image will print a list of results. But, just r?. alone will enter FZF. r?.3 will enter FZF with a max search depth of 3.
        ALL COMMANDS:\n"""*0+indentify(command_list,' '*4*0), "blue")
        # Other commands: 'MOD ON', 'MOD OFF', 'SMOD SET', 'MOD SET', 'VARS', 'MORE', 'MMORE', 'RETURN NOW', 'EDIT', 'AHISTORY', GHISTORY', 'COPY', 'PASTE', 'CHISTORY', 'DITTO', 'LEVEL', 'PREV', 'NEXT', 'UNDO', 'PT ON', 'PT OFF', 'RANT', '!', '!!', '?/', '?.', '?', '??', '???', '????', '?????','SHELL', 'IPYTHON', 'UNDO ALL', 'PREV ALL', 'UNDO ON', 'UNDO OFF', 'PREV ON', 'PREV OFF', 'PREV CLEAR', 'UNDO CLEAR', 'GC ON', 'GC OFF', 'SUSPEND', 'TICTOC ON', 'TICTOC OFF', 'TICTOC', 'FANSI ON', 'FANSI OFF', 'RUN', 'CD', 'PROF ON', 'PROF OFF', 'PROF', 'IPYTHON ON', 'IPYTHON OFF', 'PROF DEEP', 'SET STYLE', 'PT SAVE', 'PT RESET', 'RELOAD ON', 'RELOAD OFF', 'PWD', 'CPWD', 'LS', 'FORK'

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
                                fansi_print("...very well then. We won't reset your PT (PromptToolkit) settings file.", 'blue', 'underlined')
                        except Exception as e:
                            fansi_print("...failed to PT RESET!", 'red', 'underlined')
                            print_stack_trace(e)

                    elif user_message == 'SET STYLE':
                        set_prompt_style()

                    elif user_message=='ANS PRINT FAST' or user_message=='APFA':
                        fansi_print("ANS PRINT FAST --> Will still print the value of 'ans', but it won't check if it's the same value as before (which can make it much faster). It will still print the answer, but it won't always be highlighted yellow if 'ans' is unchanged (normally it's green if there's a new value of 'ans', and yellow if 'ans' hasn't changed)", 'blue', 'bold')
                        # print("TODO: This might be made the default option, in which case ANS PRINT FAST will be removed") #It's not fullproof. [0] twice is green twice, instead of green than yelloq
                        should_print_ans=''
                    elif user_message=='ANS PRINT OFF' or user_message=='APOF':
                        fansi_print("ANS PRINT OFF --> Will no longer automatically print the value of 'ans'. This is often useful when str(ans) is so large that printing 'ans' spams the console too much.", 'blue', 'bold')
                        should_print_ans=False
                    elif user_message=='ANS PRINT ON' or user_message=='APON':
                        fansi_print("ANS PRINT ON --> Will automatically print the value of 'ans'. Will print it in green if it's a new value, and in yellow if it's the same value as it was before.", 'blue', 'bold')
                        should_print_ans=True

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

                    elif user_message == 'WARN':
                        if _warnings_are_off():
                            fansi_print("WARN --> Toggles warnings --> Turning warnings back on", 'blue', 'bold')
                            _warnings_on()
                        else:
                            fansi_print("WARN --> Toggles warnings --> Turning all warnings off", 'blue', 'bold')
                            _warnings_off()
    
                    elif user_message == 'PROF ON':
                        # fansi_print("Turned PROFILER on. This will profile each command you run. To get more detailed profiles, use 'PROF DEEP'. Note: Commands that take under a millisecond to run will not be profiled, to maintain both accuracy and your sanity.", 'blue', 'underlined')
                        fansi_print("Turned PROFILER on. This will profile each command you run. Note: Commands that take under a millisecond to run will not be profiled, to maintain both accuracy and your sanity.", 'blue', 'underlined')
                        _profiler=True

                    elif user_message == 'PROF OFF':
                        fansi_print("Turned PROFILER off.", 'blue', 'underlined')
                        _profiler=False
                        
                    elif user_message == 'PROF':
                        _profiler=not _profiler
                        if _profiler:
                            # fansi_print("Turned PROFILER on. This will profile each command you run. To get more detailed profiles, use 'PROF DEEP'", 'blue', 'underlined')
                            fansi_print("Turned PROFILER on. This will profile each command you run.", 'blue', 'underlined')
                        else:
                            fansi_print("Turned PROFILER off.",'blue','underlined')

                    elif user_message=='MONITOR':
                        fansi_print("MONITOR -> Entering a system monitoring tool to show you cpu usage/memory etc of the current computer...", 'blue', 'bold',new_line=False)
                        pip_import('glances').main()
                        fansi_print('...done!','blue','bold')

                    elif user_message=='GPU':
                        try:
                            pip_import('gpustat').main()
                        except BaseException as e:
                            print_stack_trace(e)
                            pass

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
                            if currently_running_mac():
                                #This only seems to be a problem on MacOS, PT ON in FORK runs fine in Ubuntu..
                                fansi_print("Note: PT ON is not currently supported while forking yet on MacOS." ,'blue','underlined')#PT ON gives OSError: [Errno 9] Bad file descriptor
                                enable_ptpython=False
                            else:
                                fansi_print("...spawning child process. Also, please don't use control+c yet, that's not supported either, and if you send a keyboard interrupt during FORK this program will act very glitchy. To exit, use RETURN (or RET, for short).",'blue','underlined')#PT ON gives OSError: [Errno 9] Bad file descriptor
                            # child process
                            # os.system('ping -c 20 www.google.com >/tmp/ping.out')
                            # sys.exit(0)
                        else:
                            pid, status = os.waitpid(child_pid, 0)
                            fansi_print("FORK: resuming parent process...",'blue','underlined')

                    elif user_message=='RANGER' or user_message=='RNG':
                        fansi_print('RANGER --> Launching ranger, a curses-based file manager with vim bindings...','blue',new_line=True)
                        _launch_ranger()
                        fansi_print('...done!','blue',new_line=True)
                    elif user_message=='TOP':
                        fansi_print("TOP --> running 'bpytop'",'blue','bold')
                        if sys.version_info>(3,6):
                            pip_import('bpytop')
                            import subprocess
                            subprocess.run([sys.executable, "-m",'bpytop'])   
                        else:
                            fansi_print("Sorry, bpytop is not supported in python versions < 3.6",'red','bold')

                    elif user_message=='TREE ALL DIR':
                        display_file_tree(all=True,only_directories=True)
                    elif user_message=='TREE DIR':
                        display_file_tree(all=False,only_directories=True)
                    elif user_message=='TREE ALL':
                        display_file_tree(all=True)
                    elif user_message=='TREE':
                        display_file_tree(all=False)

                    elif user_message=='DISKH':
                        _display_filetype_size_histogram()

                    elif user_message=='DISK':
                        print(fansi("Showing disk usage tree for current directory: ",'blue','bold')+fansi(get_current_directory(),'yellow'))
                        pip_import('duviz').main()

                    elif user_message  in {'HISTORY','HIST'}:print_history()
                    elif user_message  in {'IHISTORY','IHIST'}:
                        #Because of the automatic _maybe_display_string_in_pager feature of HIST, this is no longer a nessecary command
                        #It's harmess though, so I'll leave it in anyway (maybe you don't want to spam the console for whatever reason)
                        fansi_print('IHISTORY --> Interactive History --> Displaying HISTORY interactively','blue','bold')
                        string_pager(print_history(True))

                    
                    elif user_message  in {'ALLHISTORY','ALLHIST'}:fansi_print("ALLHISTORY --> Displaying all history, including failures:",'blue','bold');display_list(all_command_history)

                    elif user_message == 'SUSPEND' or user_message=='SUS':
                        try:
                            psutil=pip_import('psutil')
                            fansi_print("Suspending this python session...",'blue','underlined')
                            import psutil,os
                            psutil.Process(os.getpid()).suspend()
                            fansi_print("...restored!",'blue','underlined')
                        except ImportError:
                            fansi_print("ERROR: psutil not installed. Try pip install psutil.",'red')

                    elif user_message  in {'DHISTORY','DHIST'}:
                        fansi_print("DHISTORY --> DEF HISTORY --> Here is a list of all your most recent function definitions in your HISTORY:",'blue','underlined')
                        dhistory=_dhistory_helper('\n'.join(successful_command_history))
                        set_ans('\n'.join(dhistory))
                        #set_ans('\n'+'\n'.join(dhistory))
                        # bold=False
                        # for defcode in :
                        #     fansi_print('\n'+defcode,'yellow','bold' if bold else None)
                    elif user_message in {'GHISTORY','GHIST'}:
                        fansi_print("GHISTORY --> GREEN HISTORY --> Here is a list of all valid single-lined python commands you have entered so far:",'blue','underlined')
                        for x in successful_command_history:
                            fansi_print(x if '\n' not in x else '','green')  # x if '\\n' not in x else '' ≣ '\\n' not in x and x or ''
                    elif user_message in {'CHISTORY','CHIST'}:
                        fansi_print("CHISTORY --> COPY HISTORY --> Copied history to clipboard!",'blue','underlined')
                        string_to_clipboard('\n'.join(successful_command_history))

                    elif user_message == "MORE":
                        fansi_print("The last command that caused an error is shown below in magenta:",'red','bold')
                        fansi_print(error_message_that_caused_exception,'magenta')
                        if error is None:# full_exception_with_traceback is None --> Last command did not cause an error
                            fansi_print( "(The last command did not cause an error)",'red')
                        else:
                            print_stack_trace(error,True,'')

                    elif user_message == "HMORE":
                        #HMORE is like MORE but with syntax highlighting. It's a tiny difference.
                        fansi_print("The last command that caused an error is shown below in magenta:",'red','bold')
                        fansi_print(error_message_that_caused_exception,'magenta')
                        if error is None:# full_exception_with_traceback is None --> Last command did not cause an error
                            fansi_print( "(The last command did not cause an error)",'red')
                        else:
                            try:
                                #By default, try to print a syntax-highlighted stack trace. Fall back to a regular one.
                                print_highlighed_stack_trace(error)   
                            except:
                                print_stack_trace(error,True,'')

                    elif user_message == "MMORE":
                        fansi_print("The last command that caused an error is shown below in magenta:",'red','bold')

                        fansi_print(error_message_that_caused_exception,'magenta')
                        fansi_print("A detailed stack trace is shown below:",'red','bold')
                        if error is None:# full_exception_with_traceback is None --> Last command did not cause an error
                            fansi_print( "(The last command did not cause an error)",'red')
                        else:
                            print_verbose_stack_trace(error)
                    elif user_message == "AMORE":
                        fansi_print("AMORE --> 'ans MORE' --> Setting 'ans' to the error",'red','bold')
                        set_ans(error)
                        # if error is None:# full_exception_with_traceback is None --> Last command did not cause an error
                            # fansi_print( "(The last command did not cause an error)",'red')
                        # else:
                            # print_verbose_stack_trace(error)

                    elif user_message == 'DMORE':
                        fansi_print("DMORE --> Entering a post-mortem debugger","blue")
                        pip_import('pudb').post_mortem(error.__traceback__)
                        # fansi_print("DMORE has not yet been implemented. It will be a post mortem debugger for your error using rp_ptpdb",'red','bold')

                    elif user_message.startswith('MOD SET'):
                        cursor='|'
                        if cursor in user_message:
                            def string_to_modifier(string):
                                #Treat the string as a template.
                                return lambda input:string.replace(cursor,input)
                            template_string=user_message[len('MOD SET'):].lstrip()
                            fansi_print("MOD SET: Setting template with cursor="+repr(cursor)+" string to "+repr(template_string),'blue','bold')
                            fansi_print(repr(cursor)+" will be replaced with user_message",'blue')
                            modifier=string_to_modifier(template_string)
                            if not use_modifier:
                                fansi_print("MOD ON --> use_modifier=True","blue")
                                use_modifier=True
                        else:
                            fansi_print("Failed to set modifier because you didn't use the cursor anywhere. You should use "+repr(cursor)+" somewhere in your modifier string.\nEXAMPLE:\nMOD SET print("+str(cursor)+")",'red','bold')

                    elif user_message.startswith('SMOD SET'):
                        cursor='|'
                        if cursor in user_message:
                            def repr_string_to_modifier(string):
                                #Treat the string as a template.
                                return lambda input:string.replace(cursor,repr(input))
                            template_string=user_message[len('SMOD SET'):].lstrip()
                            fansi_print("SMOD SET: (aka String-modifier set) Setting template with cursor="+repr(cursor)+" string to "+repr(template_string),'blue','bold')
                            fansi_print(repr(cursor)+" will be replaced with repr(user_message)",'blue')
                            modifier=repr_string_to_modifier(template_string)
                            if not use_modifier:
                                fansi_print("MOD ON --> use_modifier=True","blue")
                                use_modifier=True
                        else:
                            fansi_print("Failed to set string-modifier because you didn't use the cursor anywhere. You should use "+repr(cursor)+" somewhere in your modifier string.\nEXAMPLE:\nSMOD SET print("+str(cursor)+")",'red','bold')

                    elif user_message == "MOD OFF":
                        fansi_print("MOD OFF --> use_modifier=False","blue")
                        use_modifier=False
                    elif user_message == "MOD ON":
                        fansi_print("MOD ON --> use_modifier=True","blue")
                        use_modifier=True

                    elif user_message=='FANSI ON':
                        enable_fansi()
                        fansi_print("FANSI ON --> enable_fansi()","blue")
                    elif user_message=='FANSI OFF':
                        disable_fansi()
                        fansi_print("FANSI OFF --> disable_fansi()","blue")

                    elif user_message == "PT ON":
                        fansi_print("PROMPT TOOLKIT ON --> enable_ptpython=True","blue")
                        if _printed_a_big_annoying_pseudo_terminal_error:
                            fansi_print("Warning: PT ON crashed, so PT ON might not be available right now. This could be because PT ON crashed, or you're using a terminal that doesn't support it. Will attempt to PT ON anyway, though.","red")
                        _printed_a_big_annoying_pseudo_terminal_error=False
                        enable_ptpython=True

                    elif user_message == "PT OFF":
                        fansi_print("PROMPT TOOLKIT OFF --> enable_ptpython=False","blue")
                        enable_ptpython=False
                        use_modifier=True

                    elif user_message == "PT":
                        fansi_print("PT --> PROMPT TOOLKIT TOGGLE --> enable_ptpython=not enable_ptpython (Toggles between PT ON and PT OFF)","blue",'bold')
                        enable_ptpython=not enable_ptpython
                        use_modifier=True

                        if enable_ptpython:
                            if _printed_a_big_annoying_pseudo_terminal_error:
                                fansi_print("Warning: PT ON crashed, so PT ON might not be available right now. This could be because PT ON crashed, or you're using a terminal that doesn't support it. Will attempt to PT ON anyway, though.","red")
                            _printed_a_big_annoying_pseudo_terminal_error=False

                    elif user_message == "LEVEL":
                        #TODO: add more info:
                        #       - If we're in VM
                        #       - If we're in Anaconda
                        #       - rp version
                        #       - If we're in TMUX
                        #       - If we're in docker
                        #       - Current memory
                        #       - Available GPU's (and if they have CUDA)
                        name=get_computer_name()
                        name=fansi(name,'green','bold')
                        if running_in_ssh():
                            name=fansi('(SSH) ','green',)+name
                        if running_in_google_colab():
                            fansi_print("Google Colab",'yellow','bold')
                        elif running_in_jupyter_notebook():
                            fansi_print("Jupyter",'yellow','bold')
                        if currently_in_a_tty():
                            print("(Running in a terminal)")
                        else:
                            print("(NOT Running in a terminal)")
                        def cyan(text):return fansi(text,'cyan')
                        import platform,sys,getpass
                        version=platform.python_implementation()+' '+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
                        version=fansi(version,'magenta','bold')

                        platform_type=""
                        if currently_running_unix():platform_type='Unix'
                        if currently_running_linux():platform_type='Linux'
                        if currently_running_mac():platform_type='Mac'
                        if currently_running_windows():platform_type='Windows'

                        bullet='    - '

                        print('Python version: '+version)
                        print('Current time: '+_format_datetime(get_current_date()))
                        print('Computer details:')
                        print(bullet+'Operating system: '+fansi('('+platform_type+') ','red','bold')+fansi(platform.platform(),'red'))
                        print(bullet+'Computer name: '+name)
                        print(bullet+'User Name: '+cyan(getpass.getuser()))
                        print("Network:")
                        print(bullet+"MAC Address:",cyan(get_my_mac_address()))
                        if connected_to_internet():
                            print(bullet+"Local IP:",cyan(get_my_local_ip_address()))
                            #TODO: Cache the public IP, it can be slow...
                            print(bullet+"Public IP:",cyan(get_my_public_ip_address()))
                        else:
                            print(bullet+'(NOT Connected to internet)')

                        # def getCurrentMemoryUsage():
                        #THIS FUNCTION DOESNT WORK
                        #     # https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
                        #     ''' Memory usage in kB '''
                        #     with open('/proc/self/status') as f:
                        #         memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
                        #     return int(memusage.strip())

                        

                        print('Process:',fansi(get_process_id(),'yellow','bold'),fansi(get_process_title(),'yellow'))
                        # print(bullet+'Memory used: '+human_readable_file_size(getCurrentMemoryUsage()))
                        fansi_print("LEVEL --> "+level_label(-1),"blue")
                        use_modifier=True

                    elif user_message == "COPY":
                        from rp import string_to_clipboard as copy
                        fansi_print("COPY --> r.string_to_clipboard(str(ans))","blue")
                        copy(str(get_ans()))

                    elif user_message == "VARS":
                        fansi_print("VARS --> ans = user_created_variables (AKA all the names you created in this pseudo_terminal session):","blue")
                        fansi_print("  • NOTE: ∃ delete_vars(ans) and globalize_vars(ans)","blue")
                        set_ans(user_created_var_names,save_history=True)

                    elif user_message == "WCOPY":
                        from rp import string_to_clipboard as copy
                        fansi_print("WCOPY --> Web Copy --> rp.web_copy(ans) --> Copying ans to the internet","blue")
                        from time import time
                        start_time=time()
                        if callable(get_ans()):
                            fansi_print("        *Note: I noticed that ans is callable. If you're trying to copy a function, make sure you paste it in the same python version!",'blue')

                        fansi_print("    ...please wait, communicating with "+repr(_web_clipboard_url)+"...","blue",new_line=False)
                        web_copy(get_ans())
                        fansi_print("done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)
                        successful_command_history.append("#WCOPY rp.web_copy(ans)")

                    elif user_message=='TCOPY':
                        fansi_print("TCOPY --> tmux Copy --> Copying str(ans) to tmux's clipboard","blue",'bold')
                        tmux_copy(str(get_ans()))

                    elif user_message=='VCOPY':
                        fansi_print("VCOPY --> Vim Copy","blue",'bold')
                        vim_copy(str(get_ans()))


                    elif user_message == "WPASTE":
                        from rp import string_to_clipboard as copy
                        fansi_print("WPASTE --> Web Paste --> rp.web_paste(ans) --> Pasting ans from the internet","blue",'bold')
                        fansi_print("    ...please wait, communicating with "+repr(_web_clipboard_url)+"...","blue",new_line=False)
                        from time import time
                        start_time=time()
                        new_ans=web_paste()
                        fansi_print("done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)

                        if isinstance(new_ans,str):
                            successful_command_history.append("ans=%s#WPASTE"%repr(new_ans))
                        else:
                            successful_command_history.append("#WPASTE ans=rp.web_paste()")

                        set_ans(new_ans)

                    elif user_message == "LCOPY":
                        from rp import string_to_clipboard as copy
                        fansi_print("LCOPY --> Local Copy --> rp.local_copy(ans) --> Copying ans to a clipboard file on your computer (faster than WCOPY)","blue",'bold')
                        from time import time
                        start_time=time()
                        if callable(get_ans()):
                            fansi_print("        *Note: I noticed that ans is callable. If you're trying to copy a function, make sure you paste it in the same python version!",'blue')

                        local_copy(get_ans())
                        fansi_print("Done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)
                        successful_command_history.append("#LCOPY rp.local_copy(ans)")

                    elif user_message == "LPASTE":
                        from rp import string_to_clipboard as copy
                        fansi_print("LPASTE --> Local Paste --> rp.local_copy(ans) --> Pasting ans from a clipboard file on your computer (faster than WPASTE)","blue",'bold')
                        from time import time
                        start_time=time()
                        new_ans=local_paste()
                        fansi_print("Done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)

                        if isinstance(new_ans,str):
                            successful_command_history.append("ans=%s#LPASTE"%repr(new_ans))
                        else:
                            successful_command_history.append("#LPASTE ans=rp.local_paste()")

                        set_ans(new_ans)

                    elif user_message in {"#PREV","PREV"}:
                        fansi_print("PREV -->  ans = ‹the previous value of ans›:","blue",'bold')
                        if ans_history:
                            ans_redo_history.append(ans_history.pop())
                        if not ans_history:
                            fansi_print("    [Cannot get PREV ans because ans_history is empty]",'red')
                        else:
                            set_ans(ans_history[-1],save_history=False,force_green=True)#Because ans_history isn't updated when we know that we have a duplicate ans value, we can logically conclude that it should be green (and not yellow)
                            successful_command_history.append("#PREV")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"#NEXT","NEXT"}:
                        if not ans_redo_history:
                            fansi_print("    [Cannot get NEXT ans because ans_redo_history is empty. NEXT is to PREV as REDO is to UNDO. Try using PREV before using NEXT.]",'red')
                        else:
                            fansi_print("NEXT -->  ans = ‹the next value of ans› (PREV is to UNDO as NEXT is to REDO):","blue",'bold')
                            set_ans(ans_redo_history.pop(),save_history=True)
                            successful_command_history.append("#NEXT")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO","#UNDO"}:
                        fansi_print("UNDO --> UNDO:","blue")
                        if not snapshot_history:
                            fansi_print("    [Cannot UNDO anything right now because snapshot_history is empty"+(' becuase UNDO is OFF (enable it with UNDO ON)' if not snapshots_enabled else '')+"]",'red')
                        else:
                            while snapshot_history and not set_snapshot(snapshot_history.pop()):# Keep undoing until something changes
                                successful_command_history.append("#UNDO")# We put this here in case the user wants to analyze the history when brought back into normal python code
                            successful_command_history.append("#UNDO")# We put this here in case the user wants to analyze the history when brought back into normal python code
                            # set_snapshot([{},{},{}])
                    elif user_message in {"UNDO ALL","#UNDO ALL"}:
                        fansi_print("UNDO ALL --> snapshot_history=[] (Doing UNDO over and over again):\n\tCleared %i entries"%len(snapshot_history),"blue")
                        if snapshot_history:set_snapshot(snapshot_history[0])
                        else:fansi_print("\t(snapshot_history is allready empty, so no changes were made)",'blue')
                        snapshot_history=[]
                        successful_command_history.append("#UNDO ALL")
                    elif user_message in {"PREV ALL","#PREV ALL"}:
                        fansi_print("PREV ALL --> ans_history=[] (Doing PREV over and over again):\n\tCleared %i entries"%len(ans_history),"blue")
                        fansi
                        if ans_history:set_ans(ans_history[0])
                        else:fansi_print("\t(ans_history is allready empty, so no changes were made)",'blue')
                        ans_history=[]
                        successful_command_history.append("#PREV ALL")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO CLEAR","#UNDO CLEAR"}:
                        fansi_print("UNDO ALL --> snapshot_history=[] (Clearing the UNDO history):\n\tCleared %i entries"%len(snapshot_history),"blue")
                        snapshot_history=[]
                        successful_command_history.append("#UNDO CLEAR")
                    elif user_message in {"PREV CLEAR","#PREV CLEAR"}:
                        fansi_print("PREV CLEAR --> ans_history=[] (Clearing the PREV history):\n\tCleared %i entries"%len(ans_history),"blue")
                        ans_history=[]
                        successful_command_history.append("#PREV CLEAR")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"UNDO ON","#UNDO ON"}:
                        fansi_print("UNDO ON --> snapshots_enabled=True (Enables future UNDO history recording)","blue")
                        snapshots_enabled=True
                        successful_command_history.append("#UNDO ON")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"UNDO OFF","#UNDO OFF"}:
                        fansi_print("UNDO OFF --> snapshots_enabled=False (Disables future UNDO history recording)","blue")
                        snapshots_enabled=False
                        successful_command_history.append("#UNDO OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"PREV OFF","#PREV OFF"}:
                        fansi_print("PREV OFF --> use_ans_history=False (Disables future PREV history recording)","blue")
                        use_ans_history=False
                        successful_command_history.append("#PREV OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"PREV ON","#PREV ON"}:
                        fansi_print("PREV ON --> use_ans_history=True (Enables future PREV history recording)","blue")
                        use_ans_history=True
                        successful_command_history.append("#PREV ON")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    elif user_message in {"GC ON","#GC ON"}:
                        fansi_print("GC ON --> do_garbage_collection_before_input=True ('GC ON' Forcibly invokes the garbage collector upon each user prompt). This is is especially useful, for example, when python forgets to deallocate pytorch CUDA tensors in a timely fashion, which fills up vram and makes it unusable.","blue")
                        #This feature was added to avoid errors like """CUDA out of memory. Tried to allocate 76.00 MiB (GPU 0; 3.95 GiB total capacity; 1.72 GiB already allocated; 43.69 MiB free; 1.73 GiB reserved in total by PyTorch) """
                        do_garbage_collection_before_input=True
                        successful_command_history.append("#GC ON")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"GC OFF","#GC OFF"}:
                        fansi_print("GC OFF --> do_garbage_collection_before_input=False ('GC ON' Forcibly invokes tgarbage collector upon each user prompt)","blue")
                        do_garbage_collection_before_input=False
                        successful_command_history.append("#GC OFF")# We put this here in case the user wants to analyze the history when brought back into normal python code
                    elif user_message in {"GC","#GC"}:
                        fansi_print("GC --> toggles forced garbage collection between prompts --> toggles between GC ON and GC OFF.","blue",'bold')
                        do_garbage_collection_before_input=not do_garbage_collection_before_input
                        fansi_print('\tSet GC %s'%('ON' if do_garbage_collection_before_input else 'OFF'),'blue','bold')
                        successful_command_history.append("#GC")# We put this here in case the user wants to analyze the history when brought back into normal python code

                    # endregion
                    # region  Short-hand rinsp
                    elif user_message=='?v' or user_message=='VIMA':
                        if user_message=='VIMA':
                            fansi_print("VIMA (VIM ans) is an alias for ?v","blue",'bold',)
                        fansi_print("?v --> Running rp.vim(ans)...","blue",'bold',new_line=False)
                        vim(get_ans())
                        fansi_print("done!","blue",'bold')
                    elif user_message.endswith('?v') and not '\n' in user_message:
                        fansi_print("?v --> Running rp.vim(%s)..."%user_message,"blue",'bold',new_line=False)
                        user_message=user_message[:-2]
                        value=eval(user_message,scope())
                        fansi_print("done!","blue",'bold')
                        vim(value)
                    elif user_message=='?s':
                        fansi_print("?s --> string viewer --> shows str(ans)","blue",'bold')
                        string=str(get_ans())
                        print(string)
                        _maybe_display_string_in_pager(string)
                    elif user_message.endswith('?s') and not '\n' in user_message:
                        fansi_print("?s --> string viewer --> shows str(ans)","blue",'bold')
                        user_message=user_message[:-2]
                        value=eval(user_message,scope())
                        string=str(value)
                        print(string)
                        _maybe_display_string_in_pager(string)
                    elif user_message=='?t' or user_message=='TABA':
                        if user_message=='TABA':
                            fansi_print("TABA (TAB ans) is an alias for ?t","blue",'bold',)
                        fansi_print("?t --> Table Viewer --> Running view_table(ans):","blue",'bold')
                        view_table(get_ans())
                    elif user_message.endswith('?t') and not '\n' in user_message:
                        user_message=user_message[:-2]
                        fansi_print("t --> Table Viewer --> Running view_table(%s):"%user_message,"blue",'bold')
                        value=eval(user_message,scope())
                        view_table(value)
                    elif user_message=='?p':
                        fansi_print("?p --> Pretty Print --> Running pretty_print(ans,with_lines=False):","blue",'bold')
                        #pip_import('rich').print(get_ans())
                        pterm_pretty_print(get_ans(),with_lines=False)
                    elif user_message.endswith('?p') and not '\n' in user_message:
                        user_message=user_message[:-2]
                        fansi_print("?p --> Pretty Print --> Running pretty_print(%s,with_lines=False):"%user_message,"blue",'bold')
                        value=eval(user_message,scope())
                        pterm_pretty_print(value,with_lines=False)
                        #pip_import('rich').print(value)
                    elif user_message=='?i':
                        fansi_print("?i --> PyPI Package Inspection:","blue",'bold')
                        import rp.pypi_inspection as pi
                        pi.display_module_pypi_info(get_ans())
                    elif user_message.endswith('?i') and not '\n' in user_message:
                        user_message=user_message[:-2]
                        fansi_print("?i --> PyPI Package Inspection:","blue",'bold')
                        value=eval(user_message,scope())
                        import rp.pypi_inspection as pi
                        pi.display_module_pypi_info(value)

                    elif user_message=='?e':
                        fansi_print("Running peepdis.peep(ans):","blue",'bold')
                        pip_import('peepdis')
                        from peepdis import peep
                        peep(get_ans())
                    elif user_message.endswith('?e') and not '\n' in user_message:
                        user_message=user_message[:-2]
                        fansi_print("running peepdis.peep(%s):"%user_message,"blue",'bold')
                        pip_import('peepdis')
                        from peepdis import peep
                        value=eval(user_message,scope())
                        peep(value)
                    elif user_message == "?":
                        fansi_print("? --> rinsp(ans)","blue")
                        rinsp(get_ans())
                    elif user_message == "??":
                        fansi_print("?? --> rinsp(ans,1,1)","blue")
                        rinsp(get_ans(),1,1)
                        # fansi_print("?? --> rinsp(ans,1)","blue")
                        # rinsp(get_ans(),1)
                    elif user_message == "???":
                        fansi_print("??? --> rinsp(ans,1,0,1)","blue")
                        rinsp(get_ans(),1,0,1)
                        # fansi_print("??? --> rinsp(ans,1,1)","blue")
                        # rinsp(get_ans(),1,1)
                
                    ##### I decided to deprecate the old ??, and ????? because I found I never used them. But naturally, this means getting rid of ????? and ???? instead.

                    # elif user_message == "????":
                    #     fansi_print("???? --> rinsp(ans,1,0,1)","blue")
                    #     rinsp(get_ans(),1,0,1)
                    # elif user_message == "?????":
                    #     fansi_print("????? --> rinsp(ans,1,1,1)","blue")
                    #     rinsp(get_ans(),1,1,1)
                    elif user_message == "?/" or user_message=='?h':
                        fansi_print("?h --> help(ans)","blue")
                        # fansi_print("?/ --> help(ans)","blue")
                        help(get_ans())
                    elif user_message.endswith("?/") or user_message.endswith('?h'):
                        fansi_print("◊?h --> help(◊)","blue")
                        help(eval(user_message[:-2],scope()))
                    # elif user_message.endswith("?????"):
                    #     fansi_print("◊????? --> rinsp(◊,1,1,1)","blue")
                    #     rinsp(eval(user_message[:-5],scope()))
                    # elif user_message.endswith("????"):
                    #     fansi_print("◊???? --> rinsp(◊,1,0,1)","blue")
                    #     rinsp(eval(user_message[:-4],scope()),1,0,1)
                    elif user_message.endswith("???"):
                        fansi_print("◊??? --> rinsp(◊,1,0,1)","blue")
                        rinsp(eval(user_message[:-3],scope()),1,0,1)
                        # fansi_print("◊??? --> rinsp(◊,1,1)","blue")
                        # rinsp(eval(user_message[:-3],scope()),1,1)
                    elif user_message.endswith("??"):
                        fansi_print("◊?? --> rinsp(◊,1,1)","blue")
                        rinsp(eval(user_message[:-2],scope()),1,1)
                        # fansi_print("◊?? --> rinsp(◊,1)","blue")
                        # rinsp(eval(user_message[:-2],scope()),1)
                    elif user_message.endswith("?"):
                        fansi_print("◊? --> rinsp(◊)","blue")
                        rinsp(eval(user_message[:-1],scope()))

                    elif user_message=='PWD':
                        fansi_print("PWD: "+get_current_directory(),"blue",'bold')
                    elif user_message=='CPWD':
                        fansi_print("CPWD: Copied current directory to clipboard: "+get_current_directory(),"blue",'bold')
                        string_to_clipboard(get_current_directory())
                    elif user_message.startswith('CAT ') or user_message.startswith('NCAT ') or user_message in ['CAT','NCAT','CATA','NCATA']:

                        if user_message in ['CAT','NCAT']:
                            print("Please select the file you would like to display")
                            file_name=input_select_file()
                        elif user_message in ['CATA','NCATA']:
                            file_name=str(get_ans())
                        else:
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

                        contents=_load_text_from_file_or_url(file_name)

                        def print_code(code,highlight=False,line_numbers=False):
                            printed_lines=[]
                            def print_line(line):
                                print(line)
                                printed_lines.append(line)

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
                                print_line(num+line)

                            _maybe_display_string_in_pager(line_join(printed_lines),with_line_numbers=False)

                        print_code(contents,highlight,line_numbers)

                    elif user_message.startswith('CCAT ') or user_message=='CCAT' or user_message=='CCATA':
                        if user_message=='CCATA':
                            fansi_print('CCAT -->text_file_to_string Copy CAT ans --> Copies the contents of the file or url at \'ans\' to your clipboard','blue','bold')
                            user_message='CCAT '+str(get_ans())
                        elif user_message=='CCAT':
                            fansi_print('CCAT --> Copy CAT --> Copies a files contents to your clipboard --> Please select a file!','blue','bold')
                            user_message='CCAT '+input_select_file()

                        file_name=user_message[user_message.find(' '):].strip()
                        fansi_print("CCAT: Copying to your clipboard the contents of "+repr(file_name),"blue")
                        string_to_clipboard(_load_text_from_file_or_url(file_name))

                    elif user_message=='LS' or user_message=='LST':
                        import os

                        printed_lines=[]
                        def print_line(line):
                            printed_lines.append(line)

                        paths=sorted(sorted(os.listdir()),key=is_a_directory)

                        if user_message=='LST':
                            fansi_print("LST -> Printing all paths from LS sorted by Time (date_modified)",'blue','bold')
                            paths=[path for path in paths if path_exists(path)]
                            paths=sorted(paths,key=date_modified)
                            paths=sorted(paths,key=is_a_directory)

                        for item in paths:
                            if is_a_directory(item):
                                print_line(fansi(item,'cyan','bold'))
                            elif is_a_file(item):
                                print_line(fansi(item,'gray'))
                            else:
                                print_line(fansi(item,'red'))

                        text=line_join(printed_lines)

                        if user_message=='LST':
                            dates=[_format_datetime(date_modified(path)) for path in paths]
                            dates=[fansi(date,'blue',None) for date in dates]
                            dates=line_join(dates)
                            text=horizontally_concatenated_strings(text,'    ',dates,rectangularize=True)

                        try:
                            # ERROR: UnicodeEncodeError: 'utf-8' codec can't encode character '\udcd9' in position 10: surrogates not allowed
                            print(text)
                        except (UnicodeDecodeError,UnicodeEncodeError):
                            for line in line_split(text):
                                print(''.join(x for x in line if ord(x)<5000))

                        _maybe_display_string_in_pager(text)

                    elif user_message=='WANS':
                        fansi_print("WANS -> Write ans to a file (can be text, bytes, or an image)","blue",'bold')
                        path=input(fansi("(Enter blank path to select and overwrite an existing file)\nPath: ",'blue','bold'))
                        if not path:
                            path=input_select_file(message='WANS: Select a file to overwrite')
                        if path_exists(path):
                            if not input_yes_no("Are you sure you want to overwrite "+path+"?"):
                                path=None
                        if path is None:
                            fansi_print("WANS cancelled",'red')
                        else:
                            if is_image(get_ans()):
                                path=save_image(get_ans(),path)
                                fansi_print("WANS: Wrote image file to "+path,'blue','bold')
                            elif isinstance(get_ans(),bytes):
                                bytes_to_file(str(get_ans()),path)
                                fansi_print("WANS: Wrote binary file to "+path,'blue','bold')
                            else:
                                string_to_text_file(path,str(get_ans()))
                                fansi_print("WANS: Wrote text file to "+path,'blue','bold')
                            set_ans(path)



                    elif user_message=='UPDATE':
                        fansi_print("UPDATE -> Attempting to update this program...","blue",'bold')
                        update_rp()
                    elif user_message=='IPYTHON ON':
                        fansi_print("IPYTHON ON --> running all commands with an ipython interpereter. Run '%magic' to see help for all available iPython magics commands. (pro-tip: for line magics, you don't even need to use %, so just 'magic' works too)","blue",'underlined')
                        global _ipython_exeval
                        try:
                            if _ipython_exeval is None:
                                _ipython_exeval=_ipython_exeval_maker(dicts[0])#Right now this is global. This is seriously messy. But since pseudoterminal's namespace is allready F'd up right now, who cares...I'll fix this when I rewrite pseudoterminal
                            _use_ipython_exeval=True
                        except ImportError:
                            fansi_print("IPYTHON ON failed due to an import error",'red','bold')
                            _use_ipython_exeval=False
                    elif user_message=='IPYTHON OFF':
                        fansi_print("IPYTHON OFF --> running your inputs as regular ol' python again","blue")
                        _use_ipython_exeval=False
                    # endregion
                    else:

                        if user_message=='MLPASTE':
                            fansi_print("MLPASTE --> Multi-Line Paste","blue",'bold')
                            user_message=repr(input_multiline())

                        if user_message == 'NUM COM':
                            fansi_print("NUM COM --> listing all %i commands"%len(help_commands),"blue",'bold')
                            user_message=repr(help_commands)

                        if user_message == "SHELL" or user_message=='SH':
                            fansi_print("SHELL --> entering Xonsh shell","blue",'bold')
                            xonsh=pip_import('xonsh')
                            # xonsh.execer.Execer.__del__=lambda *x:None# This prevents it from unimportant error messages after we leave the shell
                            # xonsh.execer.print_exception=lambda *x:None# This prevents it from unimportant error messages after we leave the shell
                            
                            #The following line hasn't been a problem in a while, and the message is kinda a nuisance
                            # fansi_print('Will try to run Xonsh (a python-based alternative to bash). Note that its the same runtime as. If it fails to launch properly, try "pip3 install prompt-toolkit pygments --upgrade". If it\'s fine, ignore this message.','blue')
                            user_message='__import__("rp").launch_xonsh()'  # Import xonsh, run the shell, then update the directory

                        elif user_message=='AVIMA':
                            fansi_print("AVIMA --> Letting you edit ans in vim as a string","blue",'bold')
                            temp=temporary_file_path()
                            text=str(get_ans())
                            if is_valid_python_syntax(text):
                                #If we're editing a python-code string, let vim use syntax highlighting by indicating the correct file extension
                                temp+='.py'
                            try:
                                string_to_text_file(temp,str(get_ans()))
                                vim(temp)
                                user_message=repr(text_file_to_string(temp))
                            finally:
                                delete_file(temp)

                        elif user_message=='FCOPY':
                            fansi_print("FCOPY --> Web File Copy --> rp.web_copy_path() --> Copying a file or folder to the internet","blue",'bold')
                            path=input_select_path()
                            from time import time
                            start_time=time()
                            fansi_print("    ...please wait, communicating with "+repr(_web_clipboard_url)+"...","blue",new_line=False)
                            web_copy_path(path)
                            fansi_print("done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)
                            user_message=repr(path)

                        elif user_message=='?c':
                            fansi_print("?c --> Getting source code --> ans = rp.get_source_code(ans)...","blue",'bold')
                            try:
                                user_message=repr(get_source_code(get_ans()))
                            except TypeError:
                                user_message=repr(type(get_source_code(get_ans())))
                        elif user_message.endswith('?c') and not '\n' in user_message:
                            user_message=user_message[:-2]
                            fansi_print("?c --> Getting source code --> ans = rp.get_source_code(%s)..."%user_message,"blue",'bold')
                            value=eval(user_message,scope())
                            user_message=repr(get_source_code(value))

                        elif user_message=='?r':
                            fansi_print("?r --> rich.inspect(ans)","blue",'bold')
                            pip_import('rich').inspect(get_ans(),all=True,help=True,methods=True,private=True,dunder=True)
                            user_message=""

                        elif user_message.endswith('?r') and not '\n' in user_message:
                            user_message=user_message[:-2]
                            fansi_print("?r --> rich.inspect(%s)"%user_message,"blue",'bold')
                            value=eval(user_message,scope())
                            pip_import('rich').inspect(value,all=True,help=True,methods=True,private=True,dunder=True)
                            user_message=""


                        elif user_message=='FPASTE':
                            fansi_print("FPASTE --> Web File Paste --> rp.web_paste_path() --> Pasting a file or folder from the internet","blue",'bold')
                            fansi_print("    ...please wait, communicating with "+repr(_web_clipboard_url)+"...","blue",new_line=False)
                            from time import time
                            start_time=time()
                            path=web_paste_path()
                            fansi_print("done in "+str(time()-start_time)[:6]+' seconds!',"blue",new_line=True)
                            user_message=repr(path)

                        elif '\n' not in user_message and re.fullmatch(r'[a-zA-Z0-9_]*\.\?.*',user_message[::-1]) or (not '\n' in user_message and user_message.endswith('/.')):
                            def breakify(entry):
                                #Make '.asoij.woi.avoaap.thing' only contain 'thing' when using iterfzf to search for it
                                l=entry.split('.')
                                l[:-1]=['\u2060'.join(x) for x in l[:-1]]
                                return '.'.join(l)
                            if user_message.endswith('/.'):
                                #Turn 'thing/.' into 'thing?.' and '/.' into '?.'
                                user_message=user_message[:-2]+'?.'
                            if user_message.startswith('i.'):
                                user_message='ans'+user_message
                            qans=user_message.endswith('?.') or user_message in {'/.','?.'}
                            qans=user_message in 'ans?. ?. /. ans/.'.split()
                            if qans:
                                user_message='ans'+user_message



                            # if user_message and not user_message.isnumeric():
                            #     fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in ans:","blue",'bold')
                            #     rinsp_search(get_ans(),user_message)
                            #     user_message=''
                            # else:
                                depth = 5 
                                try:
                                    #Allow ?.5 to set depth of 5
                                    depth=int(user_message)
                                    assert depth>0
                                except Exception:pass
                                #If given no arguments, use FZF to select something as your new answer
                                results=('ans.'+'.'.join(result) for result in _rinsp_search_helper(get_ans(),'',depth=depth))
                                results=map(breakify,results)
                                result=_iterfzf(results,exact=True) #Exact to prevent fuzzy matching
                                result=result.replace('\u2060','')#Remove all no-space spaces
                                if result is not None:
                                    user_message=result
                                    fansi_print("Transformed command into: " + fansi_syntax_highlighting(user_message),'magenta')
                                    # set_ans(result)
                                    # successful_command_history.append()
                                else:
                                    user_message=''
                            # else:
                                    # fansi_print("You didn't give ?. a query. You must follow ?. by a query. For example, '?.print' when ans is rp","red")
                                #if user_message like 'some_value[0](x,y,z)?.query'
                            split=[x[::-1] for x in user_message[::-1].split('.?',1)][::-1]#Split on the last ?.
                            if not qans:
                                assert len(split)==2
                                value=eval(split[0],scope())
                                query=split[1]

                                if query and not query.isnumeric():
                                    fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in "+split[0]+":","blue",'bold')
                                    rinsp_search(value,query)
                                    user_message=''
                                else:
                                    # fansi_print("You didn't give some_value?. a query. You must follow some_value?. by a query. For example, 'thing?.print' is ok while 'thing?.' is not","red")
                                    depth = 5 #default depth of the rinsp search
                                    try:
                                        #Allow ?.5 to set depth of 5
                                        depth=int(query)
                                        query=''
                                        assert depth>0
                                    except Exception:pass

                                    #If given no arguments, use FZF to select something as your new answer
                                    results=('.'+'.'.join(result) for result in _rinsp_search_helper(value,'',depth=depth))

                                    
                                    results=map(breakify,results)
                                    result=_iterfzf(results,exact=True) #Exact to prevent fuzzy matching
                                    if result is None:
                                        raise KeyboardInterrupt #This is how that happens:wq
                                    result=result.replace('\u2060','')#Remove all no-space spaces
                                    if result is not None:
                                        result = split[0]+result
                                        user_message=result
                                        fansi_print("Transformed command into: " + fansi_syntax_highlighting(user_message),'magenta')
                                        # set_ans(result)
                                        # successful_command_history.append()
                                    else:
                                        user_message=''



                        # elif user_message.startswith('?.') or user_message in {'/.','?.'}:
                        #     user_message=user_message[2:]
                        #     if user_message and not user_message.isnumeric():
                        #         fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in ans:","blue",'bold')
                        #         rinsp_search(get_ans(),user_message)
                        #         user_message=''
                        #     else:
                        #         depth = 5 
                        #         try:
                        #             #Allow ?.5 to set depth of 5
                        #             depth=int(user_message)
                        #             assert depth>0
                        #         except Exception:pass
                        #         #If given no arguments, use FZF to select something as your new answer
                        #         results=('ans.'+'.'.join(result) for result in _rinsp_search_helper(get_ans(),'',depth=depth))
                        #         result=_iterfzf(results,exact=True) #Exact to prevent fuzzy matching
                        #         if result is not None:
                        #             user_message=result
                        #             fansi_print("Transformed command into: " + fansi_syntax_highlighting(user_message),'magenta')
                        #             # set_ans(result)
                        #             # successful_command_history.append()
                        #         else:
                        #             user_message=''

                        #         # fansi_print("You didn't give ?. a query. You must follow ?. by a query. For example, '?.print' when ans is rp","red")
                        # elif '\n' not in user_message and re.fullmatch(r'[a-zA-Z0-9_]*\.\?.*',user_message[::-1]):
                        #     #if user_message like 'some_value[0](x,y,z)?.query'
                        #     split=[x[::-1] for x in user_message[::-1].split('.?',1)][::-1]#Split on the last ?.
                        #     assert len(split)==2
                        #     value=eval(split[0],scope())
                        #     query=split[1]
                        #     if query:
                        #         fansi_print("Recursively rinsp_search searching for "+repr(user_message)+" in "+split[0]+":","blue",'bold')
                        #         rinsp_search(value,query)
                        #     else:
                        #         fansi_print("You didn't give some_value?. a query. You must follow some_value?. by a query. For example, 'thing?.print' is ok while 'thing?.' is not","red")
                        #     user_message=''


                        elif user_message in {'AHISTORY','AHIST'}:
                            fansi_print("AHISTORY --> ans HISTORY --> Set ans to HISTORY",'blue','underlined')
                            user_message=repr('\n'.join(successful_command_history))

                        elif user_message in ['VHIST','VHISTORY']:
                            fansi_print("VHISTORY --> VIM HISTORY --> Letting you browse all HISTORY's from previous rp.pseudo_terminal() sessions. Try yanking some entries from it, then pasting them into your buffer using \\vi mode",'blue','underlined')
                            vim(pterm_history_filename)
                            user_message=repr(pterm_history_filename)
                            # user_message=repr(pterm_history_filename)

                        elif user_message.startswith('ACAT ') or user_message=='ACAT' or user_message=='ACATA':
                            if user_message=='ACATA':
                                fansi_print('ACATA --> ans CAT ans --> Copies the contents of the file or url at \'ans\' to ans','blue','bold')
                                user_message='ACAT '+str(get_ans())
                                
                            if user_message=='ACAT':
                                fansi_print('ACAT --> ans CAT --> Copies a file\'s contents to ans --> Please select a file!','blue','bold')
                                user_message='CCAT '+input_select_file()

                            file_name=user_message[user_message.find(' '):].strip()
                            try:
                                fansi_print("ACAT: Copying to your ans the contents of "+repr(file_name),"blue",'bold')
                                user_message='ans='+repr(_load_text_from_file_or_url(file_name))
                            except UnicodeDecodeError:
                                if is_video_file(file_name):
                                    user_message='ans=__import__("rp").load_video(%s)'%repr(file_name)
                                elif is_image_file(file_name):
                                    user_message='ans=__import__("rp").load_image(%s)'%repr(file_name)
                                elif is_sound_file(file_name):
                                    user_message='ans=__import__("rp").load_sound_file(%s)'%repr(file_name)
                                else:
                                    user_message='ans=__import__("rp").file_to_bytes(%s)'%repr(file_name)
                                    # assert False,'Failed to read file '+repr(file_name)

                        elif user_message == "IPYTHON":
                            fansi_print("WARNING: Use 'IPYTHON ON' or 'IPYTHON OFF' for now on, 'IPYTHON' is broken until further notice. Will try to do it anyway, though.",'red','bold')
                            fansi_print("IPYTHON --> embedding iPython","blue")
                            # user_message='import IPython;IPython.embed()'
                            user_message='import rp.rp_ptpython.ipython;rp.rp_ptpython.ipython.embed()'

                        # region Alternate methods of user_input (PASTE/EDIT/DITTO etc)
                        elif user_message == 'RPRC':
                            print("Your .rprc is run each time you start rp. You can edit it (tip: use 'vim(ans)'). Your .rprc file is in the following path:")
                            print(rprc_file_path)
                            try:
                                vim(rprc_file_path)
                            except Exception:pass
                            user_message='ans = '+repr(rprc_file_path)

                        elif user_message == 'RYAN XONSHRC':
                            if input_yes_no('Would you like to use Ryan Burgert\'s settings in your ~/.xonshrc? (This is the settings file for the SHELL command, which uses the Xonsh shell)'):
                                _set_ryan_xonshrc()
                                user_message='ans = '+repr(xonshrc_path)

                        elif user_message=='APWD':
                            fansi_print("APWD: Set ans to current directory: "+get_current_directory(),"blue",'bold')
                            user_message=repr(get_current_directory())


                        elif user_message=='RYAN PUDBRC':
                            print("TODO: Make sure that the pudb pseudo-terminal is able to see the debugger's scope! This is currently broken.")
                            fansi_print("RYAN PUDBRC: Setting PUDB's shell to pseudo_terminal",'blue','bold')

                            pudb_config_file_path=get_absolute_path('~/.config/pudb/pudb.cfg')
                            make_directory(get_parent_folder(pudb_config_file_path))
                            if not file_exists(pudb_config_file_path):
                                pudb_config=line_join([
                                  '[pudb]',
                                  'custom_shell = /home/ryan/anaconda3/lib/python3.7/site-packages/rp/pudb_shell.py',
                                  'shell = /home/ryan/anaconda3/lib/python3.7/site-packages/rp/pudb_shell.py',
                                ])
                            else:
                                pudb_shell_path=get_module_path_from_name('rp.pudb_shell')#should be pudb_shell.py
                                assert file_exists(pudb_shell_path)
                                assert get_file_name(pudb_shell_path)=='pudb_shell.py'
                                pudb_config=text_file_to_string(pudb_config_file_path)

                                fansi_print("OLD PUDB CONFIG",'blue','underlined')
                                fansi_print(pudb_config,'yellow')

                                pudb_config=[line for line in line_split(pudb_config) if not line.startswith('shell = ') and not line.startswith('custom_shell = ')]
                                pudb_config.append('shell = '+pudb_shell_path)
                                pudb_config.append('custom_shell = '+pudb_shell_path)
                                pudb_config=line_join(pudb_config)

                                fansi_print("NEW PUDB CONFIG",'blue','underlined')
                                fansi_print(pudb_config,'yellow')

                            string_to_text_file(pudb_config_file_path,pudb_config)

                            user_message='ans = '+repr(pudb_config_file_path)

                        elif user_message=='RYAN TMUXRC':
                            _set_ryan_tmux_conf()
                            user_message='ans = '+repr(get_absolute_path('~/.tmux.conf'))


                        elif user_message=='RYAN VIMRC':
                            if input_yes_no('Would you like to add Ryan Burgert\'s vim settings to your ~/.vimrc?'):
                                _set_ryan_vimrc()
                                user_message='ans = '+repr(get_absolute_path('~/.vimrc'))
                            
                        elif user_message == 'XONSHRC':
                            fansi_print("XONSHRC --> editing your ~/.xonshrc file","blue",'bold')
                            vim(get_absolute_path('~/.xonshrc'))
                            user_message='ans = '+repr(get_absolute_path('~/.xonshrc'))

                        elif user_message == 'TMUXRC':
                            fansi_print("TMUXRC --> editing your ~/.tmux.conf file","blue",'bold')
                            vim(get_absolute_path('~/.tmux.conf'))
                            user_message='ans = '+repr(get_absolute_path('~/.tmux.conf'))

                        elif user_message == 'VIMRC':
                            fansi_print("VIMRC --> editing your ~/.vimrc file","blue",'bold')
                            vim(get_absolute_path('~/.vimrc'))
                            user_message='ans = '+repr(get_absolute_path('~/.vimrc'))

                        elif user_message == 'RYAN RPRC':
                            #This isn't in the help documentation, because it's something I made for myself. You can use it too though!
                            if input_yes_no('Would you like to add Ryan Burgert\'s default settings to your rprc?'):
                                _get_ryan_rprc_path()
                            user_message='from rp import *\nans='+repr(rprc_file_path)

                        elif user_message == 'GMORE':
                            fansi_print("GMORE --> 'google-search MORE' --> Searching the web for your error...","red",'bold')
                            if error is None:
                                fansi_print('    (Can\'t use GMORE because there haven\'t been any errors yet)','red')
                                user_message=''
                            else:
                                error_string=strip_ansi_escapes(print_stack_trace(error,full_traceback=False,header='',print_it=False))
                                print(fansi("    Searching for: ",'red','bold')+fansi(error_string,'yellow'))
                                url=google_search_url(error_string)
                                open_url_in_web_browser(url)
                                user_message=repr(url)

                        elif user_message == 'VIMORE':
                             fansi_print("VIMORE --> 'vim MORE' --> Edit some file in the last error's traceback",'red','bold')
                             if error is None:
                                fansi_print('    (Can\'t use VIMORE because there haven\'t been any errors yet)','red')
                                user_message=''
                             else:
                                 try:
                                      user_message=repr(_vimore(error))
                                 except KeyboardInterrupt:
                                      print('(Cancelled)')
                                      user_message=''
                                 except:
                                      user_message=''
                                      pass
                        elif user_message=='IMPMORE':
                            def get_name_from_name_error(error:NameError):
                                #EXAMPLE:
                                #    INPUT:
                                #        NameError: name 'thing' is not defined
                                #    OUTPUT:
                                #        'thing'
                                assert isinstance(error,NameError)
                                ans=error
                                ans=ans.args
                                ans=ans[0]
                                ans=ans.split()
                                ans=ans[1]
                                import ast
                                ans=ast.literal_eval(ans)
                                return ans
                            fansi_print("IMPMORE --> attempts to import a module resulting from a NameError",'red','bold')
                            if 'ModuleNotFoundError' not in vars():
                                ModuleNotFoundError=ImportError#Older versions of python, like python3.5
                            if not isinstance(error,NameError) and not isinstance(error,ModuleNotFoundError) and not isinstance(error,ImportError):
                                fansi_print("     (Current error is not a NameError, ImportError or ModuleNotFoundError but is instead a %s, so IMPMORE won't do anything)"%str(type(error)),'red','bold')
                                user_message=''
                            else:
                                if isinstance(error,NameError):
                                    user_message='import '+get_name_from_name_error(error)
                                elif isinstance(error,ModuleNotFoundError) or isinstance(error,ImportError):
                                    user_message='import '+str(error)[16:][1:-1]
                                print(fansi("Transformed command into: ",'magenta')+fansi_syntax_highlighting(user_message))

                        elif user_message=='NEXTMORE':
                            fansi_print("NEXTMORE --> sets the error to the next error in history",'red','bold')
                            if error_stack.can_redo():
                                error=error_stack.redo()
                                print(fansi('ERROR: ','red','bold')+fansi(error,'red'))
                            else:
                                fansi_print("     (Cannot go to the NEXT error: allready at the latest)",'red','bold')
                            user_message=''


                                
                        elif user_message=='PREVMORE':
                            fansi_print("NEXTMORE --> sets the error to the next error in history",'red','bold')
                            if error_stack.can_undo():
                                error=error_stack.undo()
                                print(fansi('ERROR: ','red','bold')+fansi(error,'red'))
                            else:
                                fansi_print("     (Cannot go to the PREV error: allready at the earliest error)",'red','bold')
                            user_message=''
                            


                        elif user_message=='PIPMORE':
                            fansi_print("PIPMORE --> 'pip_install MORE' --> Will try to install missing modules with pip",'red','bold')
                            #Used when you have something like ERROR: ModuleNotFoundError: No module named 'tensorflow'
                            #Will automatically install tensorflow  
                            if 'ModuleNotFoundError' not in vars():
                                ModuleNotFoundError=ImportError #Python3.5 doesn't have ModuleNotFoundError
                            if not isinstance(error,ModuleNotFoundError):
                                if error is None:
                                    fansi_print('    (Warning: PIPMORE cannot be used yet because you havent made any errors)','red','bold')
                                else:
                                    fansi_print('    (Warning: PIPMORE cannot be used on this error because its not a ModuleNotFoundError)','red','bold')
                            else:
                                missing_module_name=error
                                missing_module_name=str(missing_module_name)
                                missing_module_name=missing_module_name[len('No module named '):]
                                missing_module_name=eval(missing_module_name)
                                try:
                                    pip_import(missing_module_name)#pip_import instad of pip_install because it takes into account known_pypi_module_package_names
                                except Exception as e:
                                    raise
                            user_message=''


                        elif user_message == 'EPASTE':
                            fansi_print("EPASTE --> Exec/Eval PASTE --> Running code from your clipboard (printed below):",'blue','underlined')
                            user_message=string_from_clipboard()
                            # fansi_print(user_message,"yellow")
                            print(fansi_syntax_highlighting(user_message))
                        elif user_message.startswith("RANT ") or user_message.startswith("RANT\n"):
                            user_message="run_as_new_thread(exec,"+repr(user_message[5:].strip())+",globals(),locals())"
                        elif user_message.startswith("RANP "):
                            user_message="run_as_new_process(exec,"+repr(user_message[5:].strip())+",globals(),locals())"
                        elif user_message=='VPASTE':
                            fansi_print("VPASTE --> Vim Paste","blue",'bold')
                            tmux_clipboard=vim_paste()
                            user_message=repr(tmux_clipboard)
                        elif user_message=='TPASTE':
                            fansi_print("TPASTE --> tmux paste --> Setting ans to tmux's clipboard","blue",'bold')
                            tmux_clipboard=tmux_paste()
                            user_message=repr(tmux_clipboard)
                        elif user_message == 'PASTE':
                            fansi_print("PASTE --> ans=str(string_from_clipboard()):",'blue','underlined')
                            user_message=repr(string_from_clipboard())
                        elif user_message in 'ALS ALSF ALSD'.split():
                            if user_message in 'ALS' :
                                fansi_print("ALS --> ans LS --> Sets ans to the list of paths in the current directory",'blue','bold')
                                user_message = repr(get_all_paths(get_current_directory(),include_files=True,include_folders=True,relative=True,sort_by='name'))
                            if user_message in 'ALSD':
                                fansi_print("ALSD --> ans LS directories --> Sets ans to the list of directories in the current directory",'blue','bold')
                                user_message = repr(get_all_paths(get_current_directory(),include_files=False,include_folders=True,relative=True,sort_by='name'))
                            if user_message in 'LSAF ALSF':
                                fansi_print("ALSF --> ans LS files --> Sets ans to the list of files in the current directory",'blue','bold')
                                user_message = repr(get_all_paths(get_current_directory(),include_files=True,include_folders=False,relative=True,sort_by='name'))
                                
                        elif user_message.startswith('DITTO'):
                            ditto_arg=user_message[len('DITTO'):]
                            try: ditto_number=int(ditto_arg.strip())
                            except: ditto_number=1
                            if not successful_command_history:
                                fansi_print("DITTO --> Cannot use DITTO, the successful_command_history is empty!",'red')
                                user_message=""# Ignore it
                            else:
                                fansi_print("DITTO --> re-running last successful command "+str(ditto_number)+" times, shown below in yellow:",'blue','underlined')
                                user_message='\n'.join([successful_command_history[-1]]*ditto_number)
                                fansi_print(user_message,"yellow")
                        elif user_message=='LS SEL' or user_message=='LSS' or user_message in ['LS REL','LSR']:
                            rel = user_message in ['LS REL','LSR']
                            if rel:
                                fansi_print("LS REL aka LSR--> LS Select (Relative Path) --> Same as LSS, except uses relative path instead of global path--> Please select a file or folder",'blue','underlined')
                            else:
                                fansi_print("LS SEL aka LSS--> LS Select --> Please select a file or folder",'blue','underlined')
                            try:
                                path=input_select_path()
                                if rel:
                                    path=get_relative_path(path)
                                user_message='ans = '+repr(path)
                            except KeyboardInterrupt:
                                fansi_print("\t(LS SEL cancelled)",'blue')
                                user_message=''
                        elif user_message=='LS FZF' or user_message=='LSZ' or user_message=='LSQ' or user_message=='LS QUE':
                            #TODO: LSQ could be made obsolete if there was some way to sort the results of LSZ
                            #However, I don't know how to do this
                            #For this reason, I don't know if I'll made a CDQ soon, as you could just to LSQ then CDA. 
                            #Hopefully there's some way to sort the FZF results...
                            #Also, it would be nice if we didn't show irrelevant search results. For example, when searchig for a folder 'Thing', having 'Thing/Stuff' show up doesn't make sense when 'Thing' was already a result
                            if user_message in ['LSQ','LS QUE']:    
                                fansi_print("LS QUE aka LSQ --> LS Query --> Please select a file or folder (this is basically LS FZF, but requires an exact match)",'blue','underlined')
                                exact=True
                            else:
                                fansi_print("LS FZF aka LSZ --> LS Fuzzy-Select --> Please select a file or folder",'blue','underlined')
                                exact=False

                            try:
                                result=_iterfzf((line.replace('\n',' ').replace('\r',' ') for line in breadth_first_path_iterator('.')),exact=exact)
                            except:
                                result=None

                            if not result:
                                raise KeyboardInterrupt #This is the only way this could have happened; and it seems pretty natural. More so than seeing an error message.
                                # fansi_print("LS FZF (aka LSZ) cancelled: you didn't select a path",'red','underlined')
                                # user_message=''
                            else:
                                # result=get_absolute_path(result)
                                user_message=repr(result)


                        elif (user_message.startswith('FDS ') or user_message.startswith('FD ')) and not '\n' in user_message and ' ' in user_message.strip() or user_message=='FDS':
                            if user_message=='FDS':
                                user_message='FDS '+input(fansi("Please enter a search query: ",'blue','bold'))
                            if user_message.startswith('FDS '):
                                user_message='FD SEL '+user_message[len('FDS '):]
                            query=user_message[len('FD '):]
                            select=False
                            if query.startswith("SEL "):
                                select=True
                                query=query[len('SEL '):]

                            print(fansi("FD --> Searching recursively for a path name containing:","blue"), fansi(query,'yellow'))
                            results=_fd(query)
                            
                            if not results:
                                fansi_print("\t(There were no results matching your query)",'blue')
                            if select and results:
                                print()
                                print()
                                selected_result=input_select(fansi('Please select a path, or press control+c to cancel:','yellow','bold'),results,stringify=str)
                                selected_result=strip_ansi_escapes(selected_result)#get rid of highlighting...
                                user_message='ans = '+repr(selected_result)
                            else:
                                user_message=''
                        elif user_message in {'RUNA','SRUNA','SSRUNA'}:
                            cmd=user_message
                            user_message=str(get_ans())
                            if cmd=='SSRUNA':
                                fansi_print("SRUNA --> Shell-Run !!ans --> Run ans as a shell command and return result as string",'blue','bold')
                                user_message='ans=__import__("rp").shell_command('+repr(user_message)+')#SSRUNA'
                            if cmd=='SRUNA':
                                fansi_print("SRUNA --> Shell-Run !ans --> Run ans as a shell command",'blue','bold')
                                user_message='import os;os.system('+repr(user_message)+')#SRUNA'

                            fansi_print("RUNA --> Running the contents of 'ans' as a command",'blue','bold')
                            if not is_valid_python_syntax(user_message) and (file_exists(user_message) or is_valid_url(user_message)):
                                fansi_print("Loading code from "+user_message+"...",'blue','bold')
                                user_message=_load_text_from_file_or_url(user_message)

                            print(fansi("Transformed command into:",'magenta')+'\n' +fansi_syntax_highlighting(user_message))
                        elif user_message.startswith('RUN ') or user_message=='RUN':
                            import shlex
                            command=shlex.split(user_message[4:])#shlex handles quoted strings even if there are spaces in them. https://stackoverflow.com/questions/899276/python-how-to-parse-strings-to-look-like-sys-argv
                            if not command:
                                command=[input_select_file(message=fansi("RUN (without arguments) --> Please select a python file","blue",'bold'))]
                            script_path=command[0]
                            script_path=script_path.strip()
                            if not script_path:
                                fansi_print("RUN --> Error: Please specify a python script. Example: 'RUN test.py --args",'red')
                            else:
                                fansi_print("RUN --> Executing python script at file with args: "+script_path,'blue')
                                lines=line_split(text_file_to_string(script_path))
                                for i,line in enumerate(lines):
                                    if line.strip() and not line.startswith('from __future__'):#These must come first
                                        lines.insert(i,'import sys;_old_sys_argv=sys.argv;sys.argv='+repr(command)+" #RUN: Set the appropriate arguments")
                                        break
                                lines.append('sys.argv=_old_sys_argv #RUN: Restore the original arguments')
                                user_message=line_join(lines)
                                fansi_print("Printing script below: "+script_path,'blue')
                                print(fansi("Transformed command into:",'magenta')+'\n'+ fansi_syntax_highlighting(user_message))
                        # elif not is_valid_python_syntax(user_message) and re.fullmatch(,user_message):
                        elif user_message and 'print'.startswith(user_message) and not any(user_message in dict for dict in dicts):
                            fansi_print("Variable "+repr(user_message)+" does not exist, so parsed command into print(ans)",'magenta')
                            user_message='print(ans)'

                        elif user_message == 'VIM' or user_message.count('\n')==0 and user_message.startswith('VIM ') or user_message=='VIMH':
                            
                            if user_message=='VIMH':
                                fansi_print("VIMH --> VIM Here --> VIM .",'blue','bold')
                                user_message='VIM .'
                            fansi_print("VIM --> Launching the vim text editor",'blue','bold')
                            if user_message=='VIM':
                                path=input_select_path() 
                            else:
                                path=user_message[len('VIM '):]
                            vim(path)
                            user_message='ans = '+repr(path)+" # VIM"
                    
                        elif user_message == 'TAB' or user_message.count('\n')==0 and user_message.startswith('TAB '):
                            fansi_print("TAB --> Launching tabview (a tabular data viewer)",'blue','bold')
                            if user_message=='TAB':
                                path=input_select_path() 
                            else:
                                path=user_message[len('TAB '):]
                            pip_import('tabview')
                            import tabview
                            # tabview.tabview.view(path)
                            view_table(path)
                            # import sys
                            # command=sys.executable+' -m tabview '+path
                            # shell_command(command)
                            user_message='ans='+repr(path)+" # TAB"

                        elif user_message.startswith('RM ') or user_message=='RM':
                            fansi_print("RM --> Deletes a file or folder (actually, tries to move it to the trash bin if possible)",'blue','bold')
                            path=input_select_path()
                            # if user_message=='RM':
                            #     path=input_select_file()
                            # else:
                            #     path=user_message[len('RM '):]
                            user_message='__import__("rp").delete_path('+repr(path)+')# '+path
                            if is_a_folder(path) and not is_empty_folder(path):
                                if not input_yes_no(fansi("Warning: You selected a non-empty folder. Are you sure you want to delete it?",'red','underlined')):
                                    user_message=""#Cancelled

                            if user_message:
                                fansi_print("Deleting %s: "%('folder' if is_a_folder(path) else 'file')+repr(get_absolute_path(path)),'blue','bold')
                                
                            

                        elif user_message.startswith("TAKE ") or user_message =='TAKE' or user_message=='MKDIR' or user_message.startswith('MKDIR '):
                            make=user_message.startswith('MKDIR')
                            take=not make
                            if make:
                                fansi_print("MKDIR --> Makes a directory",'blue','bold')
                            elif take:
                                fansi_print("TAKE --> MKDIR then CD --> Makes a directory then cd's into it, inspired from zsh:",'blue','bold')

                            if user_message=='TAKE' or user_message=='MKDIR':
                                path=input(fansi("Enter the name of the new directory: ",'blue','bold'))
                                if path=='':
                                    fansi_print("(Given a blank input --> cancelled)",'blue','bold')
                                    user_message=''
                                    continue
                                else:
                                    user_message+=' '+path


                            if take:
                                new_dir=user_message[len('TAKE '):]
                            elif make:
                                new_dir=user_message[len('MKDIR '):]

                            make_directory(new_dir)

                            if take:
                                if directory_exists(new_dir):
                                    user_message='import sys,os;os.chdir('+repr(new_dir)+');sys.path.append(os.getcwd())# '+user_message
                                else:
                                    user_message='import sys,os;os.mkdir('+repr(new_dir)+');os.chdir('+repr(new_dir)+');sys.path.append(os.getcwd())# '+user_message
                                fansi_print("TAKE --> Current directory = "+get_absolute_path(new_dir),'blue')
                            elif make:
                                fansi_print("MKDIR --> Created new directory: "+new_dir,'blue')
                                # user_message="__import__('os').mkdir(%s)"%repr(new_dir)
                                user_message=''

                        elif user_message=='CDH':
                            fansi_print("CDH --> CD History --> Please select an entry to cd into!",'blue','bold')
                            hist=_get_cd_history()
                            if not hist:
                                fansi_print("    CDH: There are no history entries. Try going somwhere else; for example with 'CD ..'",'red')
                                user_message=''
                            else:
                                import sys
                                new_dir=input_select("Please choose a directory",_get_cd_history()[::-1], stringify=lambda x:fansi(x,'yellow' if folder_exists(x) else 'red','bold' if x in sys.path else None), reverse=True)
                                user_message='import sys,os;os.chdir('+repr(new_dir)+');sys.path.append(os.getcwd())# '+user_message

                                #The next two lines are duplicated code from the below 'CD' section!
                                if get_absolute_path(new_dir)!=get_absolute_path(get_current_directory()):
                                    from rp.rp_ptpython.completer import get_all_importable_module_names
                                    _cd_history.append(get_current_directory())

                                print(fansi("CDH: You chose:",'blue','bold'),fansi(new_dir,'yellow','bold'))
                        elif user_message=='CDH CLEAN':
                            if input_yes_no("Are you sure you want to clean CDH? This will permanently remove all red options (paths in your CD History that no longer exist)"):
                                _clean_cd_history()
                            user_message=''

                        elif not '\n' in user_message and (user_message=='CD' or user_message.startswith('CD ') or user_message=='CDP') or user_message=='CDB' or user_message=='CDU' or user_message=='CDA' or user_message in 'CDZ' or user_message=='CDQ':
                            if user_message=='CDU':
                                fansi_print("CDU (aka CD Up) is an alias for 'CD ..'",'blue')
                                user_message='CD ..'
                            if user_message=='CDA':
                                new_dir=str(get_ans())
                                if is_a_module(get_ans()):
                                    new_dir=get_module_path(get_ans())
                                elif not isinstance(get_ans(),str):
                                    try:
                                        new_dir=get_source_file(get_ans())
                                    except Exception:
                                        pass
                                if is_a_file(new_dir):
                                    new_dir=get_parent_directory(new_dir)
                                fansi_print("CDA (aka CD ans) is basically 'CD str(ans)' (or CD get_module_path(ans))",'blue')
                                if not directory_exists(new_dir):
                                    fansi_print("CDA (aka CD ans) aborted: ans is not a valid directory!",'red','underlined')
                                    cancel=True
                                    continue
                                else:
                                    user_message='CD '+new_dir
                            if user_message=='CDZ' or user_message=='CDQ':
                                if user_message=='CDQ':
                                    fansi_print("CDQ (aka CD Query) --> Letting you -search for a directory",'blue')
                                else:
                                    fansi_print("CDZ (aka CD FZF) --> Letting you fuzzy-search for a directory",'blue')
                                try:
                                    result=_iterfzf((line.replace('\n',' ').replace('\r',' ') for line in breadth_first_path_iterator('.') if is_a_folder(line)),exact=user_message=='CDQ')
                                except:
                                    result=None
                                if not result:
                                    fansi_print("CDZ (aka CD FZF) aborted: you didn't select a folder",'red','underlined')
                                    cancel=True
                                    continue
                                else:
                                    user_message='CD '+result
                            cancel=False
                            if user_message=='CDP':
                                new_dir=string_from_clipboard()
                                fansi_print("CDP --> CD Paste (CD to the string in your clipboard, aka "+repr(new_dir)+')','blue')
                                if not path_exists(new_dir):
                                    fansi_print("CDP (aka CD PASTE) aborted: Path Directory %s doesn't exist"%repr(new_dir),'red','underlined')
                                    continue
                            #This was disabled because I was too lazy to finish it properly. But it would be nice to implement this in the future
                            elif user_message=='CDB':
                                #Means CD Back
                                fansi_print("CDB --> CD Back (CD to the previous directory in your history)",'blue',)
                                #fansi_print("    Old Directory: "+get_current_directory(),'blue')
                                # if _cd_history:
                                #     _cd_history.pop()
                                cdh=_get_cd_history()
                                if _cd_history:
                                    new_dir=_cd_history[-1]
                                    _cd_history.pop()
                                elif len(cdh)>=2:
                                    fansi_print("    (Empty CD history for this session; going to previous CDH directory)",'blue')
                                    new_dir=cdh[-2]
                                else:
                                    fansi_print("    (Cannot CDB because the CD history is empty)",'red')
                                    cancel=True
                            else:
                                new_dir=user_message[2:].strip()
                            if cancel:
                                user_message=''
                            else:
                                if not new_dir:
                                    try:
                                        fansi_print("CD --> No directory was specified, please choose one!",'blue')
                                        new_dir=input_select_folder()
                                    except:
                                        fansi_print("CD --> Error: Please specify a directory. Example: 'CD /Users/Ryan'"+new_dir,'red')
                                if new_dir:
                                    _pwd=get_current_directory()
                                    # import posix
                                    # _pwd=posix.getcwd()
                                    if new_dir.startswith('~'):
                                        new_dir=get_absolute_path(new_dir)
                                    set_current_directory(new_dir)
                                    fansi_print("CD --> Current directory = "+(get_current_directory()),'blue','bold')
                                    set_current_directory(_pwd)
                                    if user_message!='CDB':
                                        if get_absolute_path(new_dir)!=get_absolute_path(get_current_directory()):
                                            _cd_history.append(get_current_directory())

                                new_dir=get_absolute_path(new_dir)
                                user_message='import sys,os;os.chdir('+repr(new_dir)+');sys.path.append(os.getcwd())# '+user_message
                            # fansi_print("Transformed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')
                        elif user_message == 'EDIT' or re.fullmatch(r'EDIT[0-9]+',user_message):
                            # pip install python-editor
                            start=''
                            give_up=False
                            if re.fullmatch(r'EDIT[0-9]+',user_message):
                                n=int(user_message[4:])
                                fansi_print("EDIT"+str(n)+" --> Editing your "+str(n)+'th last entry:','blue','underlined')
                                try:
                                    start=all_command_history[-(n+1)]
                                except IndexError:
                                    if not all_command_history:
                                        fansi_print("EDIT"+str(n)+" --> Error: Can't go back into ALLHISTORY, you haven't entered any commands yet.",'red','underlined')
                                    else:
                                        fansi_print("EDIT"+str(n)+" --> Error: Can't go back that far into ALLHISTORY; try a lower value of n",'red','underlined')
                                    give_up=True
                            if not give_up:
                                fansi_print("EDIT --> Replacing EDIT with your custom text, shown below in yellow:",'blue','underlined')
                                try:
                                    editor=pip_import('editor')
                                    temp_file=temporary_file_path()
                                    string_to_text_file(temp_file,start)
                                    vim(temp_file)
                                    user_message=text_file_to_string(temp_file)
                                    delete_file(temp_file)
                                    # user_message=editor.edit(contents=start,use_tty=True,suffix='.py').decode()
                                except ImportError:
                                    user_message=mini_editor(start,list(scope()))
                                fansi_print(user_message,'yellow')
                            else:
                                user_message=''

                        elif user_message.startswith('await ') and not '\n' in user_message:
                            user_message='__import__("rp").run_until_complete('+user_message[len('await '):]+')'
                            # user_message='from asyncio import get_event_loop\nans=get_event_loop().run_until_complete('+user_message[len('await '):]+')'
                            fansi_print("Transformed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')

                        elif user_message.startswith('ARG '):
                            import sys,shlex
                            args_string=user_message[len('ARG '):]
                            fansi_print('ARG: Old sys.argv: '+repr(sys.argv),'blue','bold')
                            sys.argv=command=[sys.argv[0]]+shlex.split(args_string)
                            fansi_print('ARG: New sys.argv: '+repr(sys.argv),'blue','bold')
                            user_message='sys.argv='+repr(sys.argv)

                        elif user_message=='ARG':
                            
                            fansi_print('ARG (dislpaying current ARG value):','blue','bold')
                            import sys
                            user_message='ans = '+repr(' '.join(sys.argv[1:]))


                        elif user_message.startswith('OPEN ') or user_message=='OPEN' or user_message=='OPENH' or user_message=='OPENA':
                            if user_message=='OPENH':
                                fansi_print("OPENH --> OPEN Here --> OPEN .",'blue','bold')
                                user_message='OPEN .'
                            if user_message=='OPENA':
                                fansi_print("OPENA --> OPEN ans --> OPENs the path or URL specified by ans",'blue','bold')
                                path=str(get_ans())
                                if not path_exists(path) and not is_valid_url(path):
                                    fansi_print("    (Error: path %s does not exist)"%repr(path[:1000]),'red','bold')
                                    continue
                                user_message='OPEN '+path
                            if user_message == 'OPEN':
                                print("Please select the file or folder you would like to open")
                                file_path=input_select_path()
                            else:
                                file_path=user_message[len('OPEN '):]

                            if path_exists(file_path):
                                user_message='open_file_with_default_application('+repr(file_path)+')'
                                user_message='__import__("rp"),'+user_message
                            elif is_valid_url(file_path):
                                user_message='__import__("rp").open_url_in_web_browser('+repr(file_path)+')'
                                
                            fansi_print("Transformed command into:\n" + fansi_syntax_highlighting(user_message),'magenta')
                

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
                        # if user_message in '/ // /// //// /////'.split():
                        #     user_message=user_message.replace('/','?')
                        #     fansi_print("Transformed command into " + repr(user_message),'magenta')
                        if not '\n' in user_message and user_message.startswith('..'):
                            user_message='ans[' + repr(user_message)+']'
                            fansi_print("Transformed command into " + repr(user_message),'magenta')
                        elif not '\n' in user_message and user_message.startswith('.') and len(user_message)>1 and user_message[1].isalpha():
                            user_message='ans.'+user_message
                            fansi_print("Transformed command into " + repr(user_message),'magenta')
                        elif current_var is not None and user_message in ['+','-','*','/','%','//','**','&','|','^','>>','<<']+['and','or','not','==','!=','>=','<=']+['>','<','~']:
                            user_message='ans ' + user_message +' ' + current_var
                            fansi_print("Transformed command into " + repr(user_message),'magenta')
                        else:
                            if user_message.startswith("!!"):# For shell commands
                                user_message="ans=__import__('rp').shell_command("+repr(user_message[2:])+")"
                                fansi_print("Transformed command into " + repr(user_message),'magenta')
                            elif user_message.startswith("!"):# For shell commands
                                # user_message="from rp import shell_command;ans=shell_command("+repr(user_message[1:])+",True)"#Disabled because we no longer guarentee that rp is imported
                                user_message="import os;os.system("+repr(user_message[1:])+")"
                                fansi_print("Transformed command into " + repr(user_message) ,'magenta')
                            if True and len(user_message.split("\n")) == 1 and not enable_ptpython:  # If we only have 1 line: no pasting BUT ONLY USE THIS IF WE DONT HAVE ptpython because sometimes this code is a bit glitchy and its unnessecary if we have ptpython
                                _thing=space_split(user_message)
                                if len(_thing) > 1:
                                    # from r import is_literal
                                    bracketeers=None
                                    try:
                                        if hasattr(eval(_thing[0]),'__getitem__'):
                                            bracketeers="[]"
                                    except:
                                        pass
                                    try:
                                        if callable(eval(_thing[0])):
                                            bracketeers="()"
                                    except Exception:pass
                                            
                                    if bracketeers is not None: 
                                        flaggy=False
                                        if all(map(is_literal,_thing)):  # If there are no ';' or ',' in the arguments; just 'rinsp' or 'ans' etc
                                            user_message=_thing[0] + bracketeers[0] + ','.join(_thing[1:]) + bracketeers[1]
                                            flaggy=True
                                        elif is_literal(_thing[0]):
                                            user_message=_thing[0] + bracketeers[0] + " " + repr(user_message[len(_thing[0]):]) + bracketeers[1]
                                            flaggy=True
                                        if flaggy:
                                            fansi_print("Transformed command into " + repr(user_message),'magenta')
                            if user_message.lstrip():
                                try:
                                    float(user_message)  # could be a negative number; we dont want Transformed command into 'ans -1324789'
                                except:
                                    arg_0=user_message.lstrip()
                                    if arg_0=='=' or last_assignable and (arg_0[0] == '=' and arg_0[1] != "=" or arg_0[0:2] in ['+=','-=','*=','/=','&=','|=','^=','%='] or arg_0[:3] in ['//=','**=','<<=','>>=']):
                                        if not last_assignable in assignable_history:
                                            assignable_history[last_assignable]=[]
                                        else:
                                            assignable_history[last_assignable].append(eval(last_assignable,scope()))
                                        user_message=last_assignable + user_message
                                        fansi_print("Transformed command into " + repr(user_message),'magenta')
                                    elif arg_0[0] in '.+/*^=><&|' or space_split(user_message.lstrip().rstrip())[0] in ['and','or','is']:
                                        if not user_message.startswith('.'):#This is a fix for: We don't want '.01+1' --> 'ans .01+1'
                                            #intentionally excluding '-' from this, as we want to be able to say -value 
                                            user_message='ans ' + user_message
                                            fansi_print("Transformed command into " + repr(user_message),'magenta')
                            if user_message.rstrip().endswith("="):
                                user_message=user_message + ' ans'
                                fansi_print("Transformed command into " + repr(user_message),'magenta')
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
                                    dupdate(dicts[0],'ans')
                                    if should_print_ans and fansi_is_enabled():
                                        from time import time
                                        pip_import('dill')#Don't count the import time
                                        start_time=time()
                                        save_history=not equal(result,dicts[0]['ans'])
                                        end_time=time()
                                        delta_time=end_time-start_time
                                        if delta_time>.25:
                                            if not warned_about_ans_print_on:
                                                fansi_print("pseudo_terminal took "+str(delta_time)[:5]+" seconds to display 'ans', which can happen when ans is a very large object in memory (and thus takes a long time to compare to the previous value of ans). If your prompts are lagging, this is probably why. You can fix this by using 'ANS PRINT FAST' (aka 'APFA'), 'ANS PRINT OFF' (aka 'APOF'), or 'FANSI OFF'. This message will only show once.",'blue','bold')
                                                warned_about_ans_print_on=True
                                    else:
                                        #Generally, the reason we turn should_print_ans off with ANS PRINT OFF, is because printing 'ans' is slow. When this is the case, we probably also don't want to wait to check if the current ans is the same as the previous ans: str(x) is generally slow iff object_to_bytes(x) is also slow, which is what handy_hash falls on. In other words, the equal() function used above is slow when we have a list of big images, for example; which is also when we would want to turn ANS PRINT OFF.
                                        save_history=result is not dicts[0]['ans']
                                    set_ans(result,save_history=save_history,snapshot=False)# snapshot=False beacause we've already taken a snapshot! Only saves history if ans changed, though. If it didn't, you'll see yellow text instead of green text
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
                                if use_modifier and modifier is not None and original_user_message is not None:# If we're using the modifier and we get a syntax error, perhaps it'_s because the user tried to input a regular command! Let them do that, meaning they have to use the 'MOD ON' and 'MOD OFF' keywords less than they did before.
                                    fansi_print("That command caused an error, but it might have been because of the modifier. Trying to run the original command (without the modifier) shown below in magenta:","red","bold")
                                    # noinspection PyUnboundLocalVariable
                                    fansi_print(user_message,"magenta")
                                    user_message=original_user_message # ⟵ We needn't original_user_message=None. This will literally never happen when use_modifier==True
                                    original_user_message=None# We turn original_user_message to None so that we don't get an infinite loop if we get a syntax error with use_modifier==True.
                                else:
                                    raise
                            # endregion
                    rp.r_iterm_comm.globa=scope()
                    
                    #Add the current directory to the cd history if its changed
                    try:
                        current_pwd=get_current_directory()
                        if not pwd_history or pwd_history[-1]!=current_pwd:
                            pwd_history.append(current_pwd)
                    except FileNotFoundError:
                        #When the folder we're working in is deleted, get_current_directory throws an error
                        #This is ok, just ignore it.
                        pass
                        
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
except Exception:pass
def get_process_title():
    try:
        import setproctitle
        return pip_import('setproctitle').getproctitle()
    except Exception:
        return pip_import('psutil').Process().name()
#@formatter:on


def parenthesizer_automator(string:str):
    def parenthesizer_automator(x:str):
        # Parenthesis automator for python
        #For best results, x should be one line.
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
            if x==y:
             return [x]#Prevent possible infinite recursion errors
            return [x] + p(y,False)
        return delete_empty_lines(strip_trailing_whitespace(p(x)))
    return '\n'.join(parenthesizer_automator(line) for line in string.splitlines())
    #I tried and failed to do this without recursion. I wonder what the time complexity of this function is? My failure is below
    # assert not '\n' in line,'Input must be a single line, not multiple lines'
    
    # from rp import string_transpose
    
    # inc='([{'
    # dec=')]}'
    
    # levels=[]
    # i=0
    # for char in line:
    #     if   char in inc:
    #         levels.append(i)
    #         i+=1
    #     elif char in dec:
    #         i-=1
    #         levels.append(i)
    #     else:
    #         levels.append(i)


    # if not levels:
    #     #If there are no parenthesis in the original input, don't change it
    #     return line
    
    # #Make sure that there are no negatives if we have unbalanced parenthesis like '(()))))'        
    # min_level=min(levels)
    # levels=[level-min_level for level in levels]
    
    # #Right now, the inner parenthesis' levels are higher than the outer ones. Flip that around, and make the middle levels small and the outer levels large (so that outer parenthesis are taller than inner parnethesis)
    # max_level=max(levels)
    # levels=[max_level-level for level in levels]
    
    # def render(char:str,level:str)->str:
    #     out=char
    #     if char in inc+dec:
    #         if char in inc:
    #             top='┌'
    #             mid='│'
    #             bot='└'
    #         else:
    #             assert char in dec
    #             top='┐'
    #             mid='│'
    #             bot='┘'
    #         out=top+(level-1)*mid+out+(level-1)*mid+bot
    #     out=out.center(max_level+1+max_level)
    #     return out
    
    # return string_transpose('\n'.join(render(char,level) for char,level in zip(line,levels)))

    # # ORIGINAL, LESS EFFICIENT CODE THAT HAD A FEW PROBLEMS (such as recursion that was too deep)


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
    except Exception:
        return 100#Don't crash pseudoterminal just because we don't have psutil installed....it's unnessecary. It's just nice, that's all. Perhaps we're not even on a laptop...so default to 100%.
def battery_plugged_in()->bool:
    try:
        import psutil
        return psutil.sensors_battery().power_plugged
    except Exception:
        return True
def battery_seconds_remaining():
    try:
        import psutil
        return psutil.sensors_battery().secsleft
    except Exception:
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

def human_readable_file_size(file_size:int):
    #Given a file size in bytes, return a string that represents how large it is in megabytes, gigabytes etc - whatever's easiest to interperet
    #EXAMPLES:
    #     >>> human_readable_file_size(0)
    #    ans = 0B
    #     >>> human_readable_file_size(100)
    #    ans = 100B
    #     >>> human_readable_file_size(1023)
    #    ans = 1023B
    #     >>> human_readable_file_size(1024)
    #    ans = 1KB
    #     >>> human_readable_file_size(1025)
    #    ans = 1.0KB
    #     >>> human_readable_file_size(1000000)
    #    ans = 976.6KB
    #     >>> human_readable_file_size(10000000)
    #    ans = 9.5MB
    #     >>> human_readable_file_size(1000000000)
    #    ans = 953.7MB
    #     >>> human_readable_file_size(10000000000)
    #    ans = 9.3GB
    
    for count in 'B KB MB GB TB PB EB ZB YB BB GB'.split():
        #Bytes Kilobytes Megabytes Gigabytes Terrabytes Petabytes Exobytes Zettabytes Yottabytes Brontobytes Geopbytes
        if file_size > -1024.0 and file_size < 1024.0:
            if int(file_size)==file_size:   
                return "%i%s" % (file_size, count)
            else:
                return "%3.1f%s" % (file_size, count)
        file_size /= 1024.0

def get_file_size(path:str, human_readable:bool=True):
    #Gets the filesize of the given path
    #Can also get the size of folders
    #If human_readable is True, it will return a string.
    #If human_readable is False, it will return an int specifying the number of bytes.
    
    assert path_exists(path),'The path you gave doesnt exist: '+repr(path)

    size=total_disc_bytes(path)

    if not human_readable:
        return size

    return human_readable_file_size(size)

get_path_size=get_folder_size=get_directory_size=get_file_size
    
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
    if not with_lines and sys.version_info>(3,6):
        try:
            pip_import('rich').print(d)
            return
        except Exception:
            pass    

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

def get_process_id():
    import os
    return os.getpid()

def regex_match(string,regex)->bool:
    #returns true if the regex describes the whole string
    import re
    return bool(re.fullmatch(regex,string))
def regex_replace(string,regex,replacement):
    #Regex replacement. Example: regex_replace('from abc import def','from .* import (.*)',r'\1') == 'def'
    import re
    return re.sub(regex,replacement,string)

def ring_terminal_bell():
    #Lets the terminal make a little noise. You've probably heard this sound at least once before on your OS...
    print(end=chr(7),flush=True)#This character should ring the TTY's bell, if that's possible.



def _pterm():
    #This is what gets run when we run rp from the command line
    try:
        pseudo_terminal(locals(),globals(),rprc=_get_ryan_rprc_path())
    finally:
        if _pterm_hist_file is not None:
            _pterm_hist_file.close()

def clear_terminal_screen():
    #Will clear the screen of a tty
    print(end="\033[0;0H\033[2J")#https://www.csie.ntu.edu.tw/~r92094/c++/VT100.html

def set_cursor_to_bar(blinking=False):
    #Modify the shape of the cursor in a vt100 terminal emulator
    #I'm not sure what the escape codes are for different terminals; tmux for example is a mystery.
    #To see what these do, I reccomend just running them in a unix terminal.
    if blinking:
        print(end="\033[5 q")
    else:
        print(end="\033[6 q")

def set_cursor_to_box(blinking=True):
    #Modify the shape of the cursor in a vt100 terminal emulator
    #I'm not sure what the escape codes are for different terminals; tmux for example is a mystery.
    #To see what these do, I reccomend just running them in a unix terminal.
    if blinking:
        print(end="\033[1 q")
    else:
        print(end="\033[2 q")

def set_cursor_to_underscore(blinking=True):
    #Modify the shape of the cursor in a vt100 terminal emulator
    #I'm not sure what the escape codes are for different terminals; tmux for example is a mystery.
    #To see what these do, I reccomend just running them in a unix terminal.
    if blinking:
        print(end="\033[3 q")
    else:
        print(end="\033[4 q")

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
    # except Exception:pass#Maybe we don't have torch.
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
    from rp.rp_ptpython.completer import get_all_importable_module_names
    get_all_importable_module_names()
    #DONT DELETE THIS COMMENT BLOCK: An alternative way to install things with pip:
    #    from pip.__main__ import _main as pip
    #    errored=pip(['install', package_name]+['--upgrade']*upgrade)
    #    if errored:
    #        assert False,'pip_install: installation of module '+repr(package_name)+' failed.'

def update_rp():
    if input_yes_no("Are you sure you'd like to try updating rp? (You will need to restart it to see any effects)"):
        pip_install("rp --upgrade --no-cache")

def module_exists(module_name):
    # https://www.tutorialspoint.com/How-to-check-if-a-python-module-exists-without-importing-it
    import imp
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

known_pypi_module_package_names={
    # To update this list, copy-paste the output of rp.pypi_inspection.get_pypi_module_package_names()
    # A list of some non-obvious pypi package names given their module names, used by pip_import
    # Let's make this dict as big as we can! More the merrier...
    'Crypto': 'pycrypto',
    'IPython': 'ipython',
    'OpenGL': 'PyOpenGL',
    'PIL': 'Pillow',
    'PyQt5': 'PyQt5-sip',
    'Xlib': 'python-xlib',
    '_ast27': 'typed-ast',
    '_ast3': 'typed-ast',
    '_bimpy': 'bimpy',
    '_black_version': 'black',
    '_dlib_pybind11': 'dlib',
    '_plotly_future_': 'plotly',
    '_plotly_utils': 'plotly',
    '_sentencepiece': 'sentencepiece',
    '_sounddevice': 'sounddevice',
    'absl': 'absl-py',
    'async_timeout': 'async-timeout',
    'atari_py': 'atari-py',
    'babel': 'Babel',
    'backports': 'configparser',
    'black_primer': 'black',
    'blackd': 'black',
    'blib2to3': 'black',
    'bs4': 'beautifulsoup4',
    'cached_property': 'cached-property',
    'caffe2': 'torch',
    'chart_studio': 'chart-studio',
    'clinical_trials': 'clinical-trials',
    'clinical_trials/api': 'clinical-trials',
    'clinical_trials/api/xml2dict': 'clinical-trials',
    'colors': 'ansicolors',
    'compose': 'docker-compose',
    'cv2': 'opencv-python',
    'cython': 'Cython',
    'deprecate': 'pyDeprecate',
    'diff_match_patch': 'diff-match-patch',
    'dns': 'dnspython',
    'dockerpycreds': 'docker-pycreds',
    'dot_parser': 'pydotz',
    'dotenv': 'python-dotenv',
    'dt_authentication': 'dt-authentication-daffy',
    'dt_data_api': 'dt-data-api-daffy',
    'dt_shell': 'duckietown-shell',
    'duckietown_docker_utils': 'duckietown-docker-utils-daffy',
    'easyprocess': 'EasyProcess',
    'editor': 'python-editor',
    'eglRenderer': 'pybullet',
    'examples': 'test-tube',
    'faiss': 'faiss-gpu',
    'getmac': 'get-mac',
    'git': 'GitPython',
    'github': 'PyGithub',
    'glances': 'Glances',
    'google': 'protobuf',
    'google_auth_oauthlib': 'google-auth-oauthlib',
    'gpt_2_simple': 'gpt-2-simple',
    'greptile': 'Greptile',
    'grpc': 'grpcio',
    'gtts_token': 'gTTS-token',
    'httpcore/_async': 'httpcore',
    'httpcore/_backends': 'httpcore',
    'httpcore/_sync': 'httpcore',
    'httpx/_transports': 'httpx',
    'integrations': 'torchmetrics',
    'ioc': 'python-ioc',
    'is_even_aast': 'iseven-aast',
    'jinja2_time': 'jinja2-time',
    'js2py': 'Js2Py',
    'jupyter_lsp': 'jupyter-lsp',
    'jupyterlab_git': 'jupyterlab-git',
    'jupyterlab_server': 'jupyterlab-server',
    'keras': 'keras-nightly',
    'keras_gym': 'keras-gym',
    'keras_preprocessing': 'Keras-Preprocessing',
    'lazy_object_proxy': 'lazy-object-proxy',
    'lib2to3': '2to3',
    'libarchive': 'libarchive-c',
    'libfuturize': 'future',
    'libpasteurize': 'future',
    'lpips_tf': 'lpips-tf',
    'mac_vendor_lookup': 'mac-vendor-lookup',
    'markdown': 'Markdown',
    'markdown_it': 'markdown-it-py',
    'matplotlib_inline': 'matplotlib-inline',
    'mpl_toolkits': 'matplotlib',
    'mplcairo': 'git+https://github.com/matplotlib/mplcairo',#Some features only available on master branch: https://stackoverflow.com/questions/26702176/is-it-possible-to-do-additive-blending-with-matplotlib
    'mypy_extensions': 'mypy-extensions',
    'neural_style': 'neural-style',
    'nmap3': 'python3-nmap',
    'notebook_as_pdf': 'notebook-as-pdf',
    'nvidia_smi': 'nvidia-ml-py3',
    'oembed': 'python-oembed',
    'ometa': 'Parsley',
    'opt_einsum': 'opt-einsum',
    'ot': 'POT',
    'paho': 'paho-mqtt',
    'pandocattributes': 'pandoc-attributes',
    'parsley': 'Parsley',
    'past': 'future',
    'pasta': 'google-pasta',
    'piglet': 'piglet-templates',
    'pl_bolts': 'pytorch-lightning-bolts',
    'pl_examples': 'pytorch-lightning',
    'plotlywidget': 'plotly',
    'prompt_toolkit': 'prompt-toolkit',
    'pyasn1_modules': 'pyasn1-modules',
    'pybullet_data': 'pybullet',
    'pybullet_envs': 'pybullet',
    'pybullet_robots': 'pybullet',
    'pybullet_utils': 'pybullet',
    'pydot': 'pydotz',
    'pyinstrument_cext': 'pyinstrument-cext',
    'pylab': 'matplotlib',
    'pyls': 'python-language-server',
    'pyls_black': 'pyls-black',
    'pyls_jsonrpc': 'python-jsonrpc-server',
    'pyls_spyder': 'pyls-spyder',
    'pynvml': 'nvidia-ml-py3',
    'pytorch_lightning': 'pytorch-lightning',
    'pyvirtualdisplay': 'PyVirtualDisplay',
    'pywt': 'PyWavelets',
    'pyximport': 'Cython',
    'qdarkstyle': 'QDarkStyle',
    'qtawesome': 'QtAwesome',
    'ranger': 'ranger-fm',
    'requests_oauthlib': 'requests-oauthlib',
    'requests_toolbelt': 'requests-toolbelt',
    'requirements': 'requirements-parser',
    'rich_traceback': 'rich-traceback',
    'rtmidi': 'python-rtmidi',
    'rtree': 'Rtree',
    'sentry_sdk': 'sentry-sdk',
    'serial': 'pyserial',#WARNING: there is a 'pip install serial' which ALSO creates a 'serial' module. This module is the WRONG SERIAL MODULE.
    'skimage': 'scikit-image',
    'sklearn': 'scikit-learn',
    'skvideo': 'sk-video',
    'skvideo.io': 'sk-video',
    'slugify': 'python-slugify',
    'smart_open': 'smart-open',
    'spacy_legacy': 'spacy-legacy',
    'sphinx': 'Sphinx',
    'sphinx_rtd_theme': 'sphinx-rtd-theme',
    'sphinxcontrib': 'sphinxcontrib-htmlhelp',
    'spyder_kernels': 'spyder-kernels',
    'tensorboard_data_server': 'tensorboard-data-server',
    'tensorboard_plugin_wit': 'tensorboard-plugin-wit',
    'tensorflow': 'tensorflow-gpu',
    'tensorflow_estimator': 'tensorflow-estimator',
    'terml': 'Parsley',
    'tesseract_ocr': 'tesseract-ocr',
    'test': 'pyinstrument',
    'test_tube': 'test-tube',
    'tests': 'torchmetrics',
    'text_unidecode': 'text-unidecode',
    'three_merge': 'three-merge',
    'timg/methods': 'timg',
    'typed_ast': 'typed-ast',
    'typing_extensions': 'typing-extensions',
    'websocket': 'websocket-client',
    'websockets/extensions': 'websockets',
    'werkzeug': 'Werkzeug',
    'wheel-platform-tag-is-broken-on-empty-wheels-see-issue-141': 'sklearn',
    'xontrib': 'xonsh',
    'yapftests': 'yapf',
    'zalgo_text': 'zalgo-text'
}
def pip_import(module_name,package_name=None):
    #Attempts to import a module, and if successful returns it.
    #If it's unsuccessful, it attempts to find it on pypi, and if
    #    it can, it asks you if you'd like to install it, and if
    #    you say 'yes', rp will attempt to install it for you.
    #Note: There are some cases where it won't ask you, and instead will just go ahead and install the packages needed
    #   - If you're in Google Colab, it won't ask before installing packages as needed
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
            if running_in_google_colab() or input_yes_no("Failed to import module "+repr(module_name)+'. You might be able to get this module by installing package '+repr(package_name)+' with pip. Would you like to try that?'):
                print("Attempting to install",package_name,'with pip...')
                pip_install(package_name)
                fansi_print("pip_import: successfully installed package "+repr(package_name)+"; attempting to import it...",'green',new_line=False)
                assert module_exists(module_name),'pip_import: error: Internal assertion failed (rp thought we successfully installed your package, but perhaps it didnt actually work, or maybe this package isn\'t compatiable with this version of python. Right now I dont know how to detect this).'# pip_import needs to be fixed if you see this message.'
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

# def delete_empty_lines(string):
#     return '\n'.join(line for line in string.splitlines() if line.strip())

#region OpenCV Helpers



def cv_text_to_image(text,*,scale=2,font=3,thickness=2,color=(255,255,255),tight_fit=False,background_color=(0,0,0)):
    lines=text.splitlines()
    images=[]
    for line in lines:
        images.append(_single_line_cv_text_to_image(line,scale=scale,font=font,thickness=thickness,color=color,tight_fit=tight_fit,background_color=background_color))
    return vertically_concatenated_images(images)
def _single_line_cv_text_to_image(text,*,scale,font,thickness,color,tight_fit,background_color):
    #EXAMPLE:
    #    display_image(cv_text_to_image('HELLO WORLD! '))
    #This is a helper function for cv_text_to_image, which can handle multi-line text
    assert isinstance(text,str)
    assert isinstance(font,int)
    cv2=pip_import('cv2')
    dims=cv2.getTextSize(text,font,scale,thickness)[0][::-1] #The dimensions of the output image
    #UPDATE: added the *2 in dims[0]*2 below to prevent the lowercase letter y's tail from being cut off
    temp=2 if tight_fit else 1
    from math import ceil
    image=np.zeros((ceil(dims[0]*1.333*temp+thickness//2+1),dims[1]*temp,3),np.uint8)
    image[:,:,0]+=background_color[0]
    image[:,:,1]+=background_color[1]
    image[:,:,2]+=background_color[2]
    image= cv2.putText(image,text,(0,dims[0]),font,scale,color,thickness)
    if tight_fit:
        image=crop_image_zeros(image)
    return image

def cv_bgr_rgb_swap(image_or_video):
    #Works for both images AND video
    #Opencv has an annoying feature: it uses BGR instead of RGB. Heckin' hipsters. This swaps RGB to BGR, vice-versa.
    image_or_video=np.asarray(image_or_video)
    image_or_video=image_or_video.copy()
    temp=image_or_video.copy()
    image_or_video[...,0],image_or_video[...,2]=temp[...,2],temp[...,0]
    return image_or_video
cv_rgb_bgr_swap=cv_bgr_rgb_swap#In-case you forgot what to type. It's all the same thing though.

_first_time_using_cv_imshow=True
def cv_imshow(img,label="cvImshow",*,
        img_is_rgb=True,#As opposed to BGR. If this is true, then the R and B channels are swapped before the image is displayed.
        wait=10,#Set to None to skip waiting all-together (will have to wait at some point or else the images won't display)
        on_mouse_down =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_mouse_move =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_mouse_up   =None, #Either set to None or some function like lambda x,y:print(x,y)
        on_key_press  =None  #Either set to None or some function like lambda key:print(key).
        # on_key_press will either be sent a character representing the key (such as pressing 'a' makes key='a') or else a multi-character string describing it. Examples: 'left','right','backspace','delete'
        ):

    if running_in_google_colab() or running_in_ipython():
        #Quick hack to make sure the notebook doesn't crash
        #It will crash if you try to use cv2.imshow in it
        display_image(img)
        return

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
        global _first_time_using_cv_imshow
        if _first_time_using_cv_imshow:
            #We try to display it twice the first time we display an image
            #This is because, for some reason, it usually just comes up blank the first time I display an image using cv2.imshow, and end up having to call cv_imshow twice. I don't want to have to do this, so I let this function handle that automatically
            cv2.imshow(label,img)
            sleep(.1)
            _first_time_using_cv_imshow=False
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
try:
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
except Exception:
    pass
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
    #EXAMPLE:
    #    cv_closest_contour_point([[1,1],[2,2],[3,3],[4,4],[5,5]],4.4,4.4)  -->  (4,4)
    cv2=pip_import('cv2')
    points=contour
    points=as_points_array(points)
    diffs=points-[x,y]
    squared_diffs=diffs**2
    squared_dists=np.sum(squared_diffs**2,1)
    index=np.argmin(squared_dists)
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

    if is_binary_image(image):
        image=as_float_image(image) #cv2.GaussianBlur can't handle binary images, just float_images and byte_images

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



def scatter_plot(x,y=None,*,block=False,clear=True,color=None,dot_size=1,ylabel=None,xlabel=None,title=None):
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
    plt=get_plt()
    if clear and plt:
        #Clear the plot (wipe it clean of any(previous drawings)
        plt.clf()
    plt.scatter(x,y,
        s=dot_size,#The size of the dots. Smaller value --> smaller dots. The default is too big for my taste.
        color=color)

    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    if title:
        plt.title(title)

    display_update(block=block)

def line_split(string):
    #I find myself often wishing this function exists for a few seconds before remembering String.splitlines exists
    #EXAMPLE: line_split('hello\nworld')==['hello','world']
    return string.splitlines()
def line_join(lines):
    #EXAMPLE: line_join(['hello','world'])=='hello\nworld'
    lines=[str(line) for line in lines]#Make sure all lines are strings. This lets line_join([1,2,3,4,5]) not crash
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
    ###NOTE we use float64 because float128 can cause problems with some libraries and is annoying to deal with...
    ###Note: We convert to np.complex256 for maximum accuracy across all datatypes
    return float(np.sum(np.abs((np.asarray(to_point,dtype=np.complex256)-np.asarray(from_point,dtype=np.complex256)))**2))

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
    if not len(x):return True#Vaccuous truth
    return len(x.shape)==1 and np.iscomplexobj(x)
def is_points_array(x):
    #Return True iff x is like [[1,2],[3,4],[5,6],...]
    x=np.asarray(x)
    if not len(x):return True#Vaccuous truth
    return len(x.shape)==2 and x.shape[1]==2
def is_cv_contour(x):
    #Return True iff x is like [[[1,2]],[[3,4]],[[5,6]],...] and dtype=np.int32
    x=np.asarray(x)#TODO this might cast it to a type other than np.int32 if given a list...though it wouldn't be WRONG to say it's not a cv contour in this case...idk should I change this or leave it be?
    if not len(x):return True#Vaccuous truth
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
    if isinstance(path,set) or isinstance(path,dict):path=list(path)
    if   is_complex_vector(path):return                        np.asarray(path.copy())
    elif is_points_array  (path):return   _points_array_to_complex_vector(path)
    elif is_cv_contour    (path):return     _cv_contour_to_complex_vector(path)
    else:assert False,'Cannot convert 2d path: path='+repr(path)
def as_points_array(path):
    #Automatically convert path data
    if isinstance(path,set) or isinstance(path,dict):path=list(path)
    if   is_complex_vector(path):return _complex_vector_to_points_array(path)
    elif is_points_array  (path):return                      np.asarray(path.copy())
    elif is_cv_contour    (path):return     _cv_contour_to_points_array(path)
    else:assert False,'Cannot convert 2d path: path='+repr(path)
def as_cv_contour(path):
    #Automatically convert path data
    if isinstance(path,set) or isinstance(path,dict):path=list(path)
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

def is_euclidean_affine_matrix(affine):
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
    assert is_euclidean_affine_matrix(affine),'The given affine is not a euclidean transform. affine=='+repr(affine)
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
        # fansi_print('Warning: fallback_hash was called on value where repr(value)=='+repr(value),'yellow') #This is annoying
        return id(value)
    fallback=fallback or default_fallback
    value_type=type(value)
    try:return hash(value)
    except Exception:pass#This is probably going to happen a lot in this function lol (that's kinda the whole point)
    try:return hash(('DILL HASH',object_to_bytes(value)))#The dill library is capable of hashing a great many things...including numpy arrays! This was added after my original implementation of handy_hash, as dill is able to handle a huuuggggeee amount of different types
    except Exception:pass
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
    except Exception:
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
    def memoized_function(*args,**kwargs):
        key=args_hash(function,*args,**kwargs)
        if not key in cache:
            cache[key]=function(*args,**kwargs)
        return cache[key]
    memoized_function.__name__+=function.__name__
    return memoized_function

def memoized_property(method):
    #This method is meant to be used as a substitute for @property
    #Often, when using @property you'll see a method like this:
    #
    #   @property
    #   def thing(self):
    #       try:
    #           return self._thing
    #       except Exception:
    #           self.thing=fancy_calculations()
    #           return self._thing
    #
    #This function takes the hassle of creating a private variable away, and automatically creates the self._thing
    #The completely equivalent function, using @memoized_property, is shown below
    #    
    #   @memoized_property
    #   def thing(self):
    #       return fancy_calculations()
    #
    assert callable(method)
    property_name='_'+method.__name__
    def memoized_property(self):
        if not hasattr(self,property_name):
            setattr(self,property_name,method(self))
        return getattr(self,property_name)
    memoized_property.__name__+=method.__name__
    memoized_property=property(memoized_property)
    return memoized_property
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

def with_file_extension(path:str,extension:str,*,replace=False):
    #Replaces or adds a file extension to a path
    #
    #EXAMPLES:
    #    >>> with_file_extension('doggy.png','jpg')
    #   ans = doggy.png.jpg
    #    >>> with_file_extension('doggy.png','.jpg')
    #   ans = doggy.png.jpg
    #    >>> with_file_extension('doggy.png','.jpg',replace=True)
    #   ans = doggy.jpg
    #    >>> with_file_extension('doggy.png','.png')
    #   ans = doggy.png
    #    >>> with_file_extension('doggy.png','..png')
    #   ans = doggy.png..png
    #    >>> with_file_extension('doggy.png','png')
    #   ans = doggy.png
    #    >>> with_file_extension('doggy','png')
    #   ans = doggy.png
    #    >>> with_file_extension('path/to/doggy','png')
    #   ans = path/to/doggy.png

    if extension.startswith('.'):
        extension=extension[1:]
    if not has_file_extension(path):
        return path+'.'+extension
    else:
        if get_file_extension(path)==extension:
            return path
        else:
            if replace:
                path=strip_file_extension(path)
            return path+'.'+extension

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
    path=os.path.expanduser(path)#In case the path has a '~' in it
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
    
def get_all_paths(*directory_path                   ,
                   sort_by                  = None  ,
                   file_extension_filter    = None  ,
                   recursive                = False ,
                   include_files            = True  ,
                   include_folders          = True  ,
                   just_file_names          = False ,
                   include_file_extensions  = True  ,
                   relative                 = False ,
                   ignore_permission_errors = False
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
    #    ⮤ get_all_paths('Tests/First','Inputs',sort_by='name')
    #    ans = ['Tests/First/Inputs/01.png',
    #           'Tests/First/Inputs/02.jpg',
    #           'Tests/First/Inputs/03.gif',
    #           'Tests/First/Inputs/04.bmp']
    #
    #    ⮤ get_all_paths('Tests/First','Inputs')                 #Without sort_by specified, the output could potentially be shuffled
    #    ans = ['Tests/First/Inputs/02.jpg',
    #           'Tests/First/Inputs/04.bmp',
    #           'Tests/First/Inputs/03.gif',
    #           'Tests/First/Inputs/01.png']
    #
    #    ⮤ get_all_paths('Tests/First','Inputs',sort_by='name',just_file_names=True)
    #    ans =  ['01.png', '02.jpg', '03.gif', '04.bmp']
    #
    #    ⮤ get_all_paths('Tests/First','Inputs',sort_by='name',just_file_names=True,include_file_extension=False)
    #    ans =  ['01', '02', '03', '04']
    #
    #    ⮤ get_all_paths('Tests/First','Inputs',sort_by='name',just_file_names=True,include_file_extension=False,file_extension_filter='bmp png')  #Filtering the extension type to just .bmp and .png images
    #    ans =  ['01', '04']
    #

    if sort_by is not None:
        sort_by=sort_by.lower()#Don't be case-sensitive. That's annoying. Reassign it here so we dont need to make it nonlocal.

    if directory_path==():#If the user didn't specify a path...
        directory_path=get_current_directory()#...default to the current directory
    else:
        directory_path=os.path.join(*directory_path)#Turn ('Ryan','Documents','Images') into 'Ryan/Documents/Images'

    def recursion_helper(directory_path):
        assert isinstance(directory_path,str),'This is an internal assertion that should never fail. If this assertion does fail, get_all_paths has a bug.'
        assert directory_exists(directory_path),'get_file_paths error: '+repr(directory_path)+' is not a directory'

        try:
            all_paths=[os.path.join(directory_path,name) for name in os.listdir(directory_path)]
        except PermissionError:
            if ignore_permission_errors:
                return []
            else:
                raise

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
            #Example: if not include_file_extensions, then 'Documents/Textures/texture.png'  --->  'texture.png' (see get_file_name for more details)
            output=list(map(get_file_name,output))

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

def get_all_files(*args,**kwargs):
    return get_all_paths(*args,**{'include_folders':False,'include_files':True,**kwargs})

def get_all_folders(*args,**kwargs):
    return get_all_paths(*args,**{'include_folders':True,'include_files':False,**kwargs})
get_all_directories=get_all_folders

def get_file_paths(*args,**kwargs):
    assert False,'This function is deprecated. Use get_all_files instead - its the same function with a new name.'

def get_subfolders(folder,*,relative=False,sort_by=None):
    #Take a folder, and return a list of all of its subfolders
    assert folder_exists(folder),'Folder '+repr(folder)+' doesnt exist!'
    return get_all_paths(folder,include_files=False,include_folders=True,recursive=False,relative=relative,sort_by=sort_by)
get_subdirectories=get_subfolders

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

def grid_concattenated_images(image_grid):  
    #Given a list of lists of images, like [[image1, image2],[image3,image4]], join them all together into one big image
    #Often, when given a list of images you want to put into a grid, 
    #   split_into_sublists(images, number_of_images_per_row) will be a good companion function!
    #   See the example functions...
    #It's a combination of vertically_concatenated_images and horizontally_concatenated_images simultaneously that maintains a gridlike structure
    #EXAMPLE:
    #    doggy=load_image('https://nationaltoday.com/wp-content/uploads/2020/02/doggy-date-night.jpg')
    #    imagechunks=[]
    #    imagechunks+=list(split_tensor_into_regions(doggy,4,2))
    #    imagechunks+=list(split_tensor_into_regions(doggy,2,4))
    #    imagechunks=[bordered_image_solid_color(image,thickness=5,color=(0,1,0,1)) for image in imagechunks]
    #    imagechunks=shuffled(imagechunks)
    #    ans=split_into_sublists(imagechunks,4)
    #    display_image(grid_concattenated_images(ans))
    #EXAMPLE:
    #    dog=load_image('https://nationaltoday.com/wp-content/uploads/2020/02/doggy-date-night.jpg')
    #    dog=resize_image(dog,.25)
    #    regions=split_tensor_into_regions(dog,3,5,flat=False)
    #    regions=grid2d_map(regions, lambda image: bordered_image_solid_color(image,color=(1,0,0,1),thickness=5))
    #    for angle in list(range(360)):
    #        display_image(grid_concattenated_images(grid2d_map(regions, lambda image: rotate_image(image,angle))))
    #EXAMPLE:
    #    ans='https://pbs.twimg.com/profile_images/945393898649665536/Ea5FkV5q.jpg'
    #    ans=load_image(ans)
    #    ans=split_tensor_into_regions(ans,10,10)
    #    ans=[bordered_image_solid_color(x,color=random_rgba_float_color(),thickness=5) for x in ans]
    #    ans=split_into_sublists(ans,10)
    #    ans=grid_concattenated_images(ans)
    #    display_image(ans)
    #EXAMPLE:
    #    ans='https://pbs.twimg.com/profile_images/945393898649665536/Ea5FkV5q.jpg'
    #    ans=load_image(ans)
    #    tiles=split_tensor_into_regions(ans,10,10)
    #    ans=[horizontally_concatenated_images(tile,resize_image(cv_text_to_image(str(i)),.25)) for i,tile in enumerate(tiles)]
    #    ans=[bordered_image_solid_color(an,color=(0,.5,1,1)) for an in ans]
    #    ans=split_into_sublists(ans,10)
    #    ans=grid_concattenated_images(ans)
    #    display_image(ans)

    image_grid=list(image_grid)
    max_image_widths=[0]*max(map(len,image_grid))

    for y,image_row in enumerate(image_grid):
        image_grid[y]=image_row=list(image_row)
        for x,image in enumerate(image_row):
            assert is_image(image),'All inputs must be images, but '+repr(image)+' is not an image as defined by rp.is_image()!'
            image_grid[y][x]=as_rgba_image(as_float_image(image))
            max_image_widths[x]=max(max_image_widths[x],get_image_width(image))

    for y,image_row in enumerate(image_grid):
        for x,image in enumerate(image_row):
            image_row[x]=crop_image(image,width=max_image_widths[x])#Cropping can also make the image larger by padding it with zeroes
        image_grid[y]=horizontally_concatenated_images(image_row)

    output_image=vertically_concatenated_images(image_grid)
    return output_image

def tiled_images(images,length=None,border_color=(.5,.5,.5,1),border_thickness=1):
    #EXAMPLE:
    #   display_image_in_terminal_color(tiled_images([load_image('https://i.pinimg.com/236x/36/69/39/36693999b6e24b1d06d0ee21c9ae320d--caged-nicolas-cage.jpg')]*25))
    #Sugar for what I often do with grid_concattenated_images
    images=list(images)
    if length is None:
        length=max(1,int(len(images)**.5))
    format_image=lambda image: bordered_image_solid_color(image,color=border_color,thickness=border_thickness,top=0,left=0)
    images=[format_image(image) for image in images]
    images=split_into_sublists(images,length)
    output=grid_concattenated_images(images)
    output=bordered_image_solid_color(output,color=border_color,thickness=border_thickness,bottom=0,right=0)
    return output

def vertically_flipped_image(image):
    #Flips (aka mirrors) an image vertically
    return image[::-1]

def horizontally_flipped_image(image):
    #Flips (aka mirrors) an image horizontally
    return image[:,::-1]
    
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

@memoized
def _get_byte_to_binary_grayscale_image_floyd_steinburg_dithering_function():
    #Code Originally from http://study.marearts.com/2018/10/dithering-python-opencv-source-code.html 
    #I optimized it to use numba, which yielded a speedup of over 1000
    
    pip_import('numba')#We're going to need numba to speed things up, or else this isn't practical
    import numba    

    @numba.jit
    def minmax(v):
        if v > 255:
            v = 255
        if v < 0:
            v = 0
        return v

    @numba.jit
    def dithering_gray(inMat, samplingF=1):
        #https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
        #https://www.youtube.com/watch?v=0L2n8Tg2FwI&t=0s&list=WL&index=151
        #input is supposed as color
        # grab the image dimensions
        h = inMat.shape[0]
        w = inMat.shape[1]
        global math
        # loop over the image
        for y in range(0, h-1):
            for x in range(1, w-1):
                # threshold the pixel
                old_p = inMat[y, x]
                new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
                inMat[y, x] = new_p
                
                quant_error_p = old_p - new_p
                
                # inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
                # inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
                # inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
                # inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)
                
                inMat[y  , x+1] = minmax(inMat[y  , x+1] + quant_error_p * 7 / 16.0)
                inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
                inMat[y+1, x  ] = minmax(inMat[y+1, x  ] + quant_error_p * 5 / 16.0)
                inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)


                #   quant_error  := oldpixel - newpixel
                #   pixel[x + 1][y    ] := pixel[x + 1][y    ] + quant_error * 7 / 16
                #   pixel[x - 1][y + 1] := pixel[x - 1][y + 1] + quant_error * 3 / 16
                #   pixel[x    ][y + 1] := pixel[x    ][y + 1] + quant_error * 5 / 16
                #   pixel[x + 1][y + 1] := pixel[x + 1][y + 1] + quant_error * 1 / 16

        # return the thresholded image
        return inMat
    
    return dithering_gray

def _binary_floyd_steinburg_dithering(image):
    #Takes an image and returns a dithered binary image
    #I chose not to expose this method right now outside of rp (aka the _ in _binary_flo...) because the name is ugly, but it will be going into as_binary_image.
    #Warning: Using the PROF with numba results in a seg-fault!
    assert is_image(image)

    if is_binary_image(image):
        #If it's already a binary image, dithering will have no effect
        return image.copy()

    pip_import('numba')
    dither=_get_byte_to_binary_grayscale_image_floyd_steinburg_dithering_function()
    image=as_byte_image(image)

    if is_grayscale_image(image):
        image=dither(image)
    else:
        for channel in range(image.shape[2]):
            image[:,:,channel]=dither(image[:,:,channel])

    return as_binary_image(image)

#region Image Channel Conversions
def is_image(image):
    #An image must be either grayscale, rgb, or rgba and have be either a bool, np.uint8, or floating point dtype
    image=as_numpy_array(image)
    return (is_grayscale_image(image) or is_rgb_image (image) or is_rgba_image  (image))  and\
           (is_float_image    (image) or is_byte_image(image) or is_binary_image(image))

def is_grayscale_image(image):
    #Basically,
    image=as_numpy_array(image)
    return len(image.shape)==2
def is_rgb_image(image):
    image=as_numpy_array(image)
    shape=image.shape
    if len(shape)!=3:return False
    number_of_channels=shape[2]
    return number_of_channels==3
def is_rgba_image(image):
    image=as_numpy_array(image)
    shape=image.shape
    if len(shape)!=3:return False
    number_of_channels=shape[2]
    return number_of_channels==4

def _grayscale_image_to_grayscale_image(image):return as_numpy_array(image).copy()
def _grayscale_image_to_rgb_image      (image):return grayscale_to_rgb(image)
def _grayscale_image_to_rgba_image     (image):return _rgb_image_to_rgba_image(_grayscale_image_to_rgb_image(image))

def _rgb_image_to_grayscale_image      (image):return rgb_to_grayscale(image)
def _rgb_image_to_rgb_image            (image):return as_numpy_array(image).copy()
def _rgb_image_to_rgba_image           (image):
    # assert False,'_rgb_image_to_rgba_image: Please fix me Im broken?!'
    if is_byte_image(image):
        #This is a dirty hack. Idk why this method can't handle byte images, and instead of looking deeper into it I'll just make do with this slightly slower version shown in the next line.
        return as_byte_image(_rgb_image_to_rgba_image(as_float_image(image)))
    assert not is_byte_image(image),'This function is currently broken for byte images! It adds too many dimensions to the shape'
    return np.concatenate((image,np.ones((*image.shape[:2],255 if is_byte_image(image) else 1),image.dtype)),2)#TODO TEST ME!!!

def _rgba_image_to_grayscale_image     (image):return _rgb_image_to_grayscale_image(_rgba_image_to_rgb_image(image))
def _rgba_image_to_rgb_image           (image):return as_numpy_array(image)[:,:,:3]
def _rgba_image_to_rgba_image          (image):return as_numpy_array(image).copy()

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

def _clamp_float_image(image):
    #Take some floating image and make sure that it has no negative numbers or numbers >1
    assert is_float_image(image)
    image=np.minimum(image,1)
    image=np.maximum(image,0)
    return image

def _float_image_to_float_image  (image):return image.copy()
def _float_image_to_byte_image   (image):return (np.asarray(_clamp_float_image(image),dtype=float)*255).astype(np.uint8)
def _float_image_to_binary_image (image):return np.round(_clamp_float_image(image)).astype(bool)
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

def as_binary_image(image,dither=False):
    # EXAMPLE of 'dither': while True: display_image(as_binary_image(load_image_from_webcam(),dither=True))
    assert is_image(image),'Error: input is not an image as defined by rp.is_image()'

    if dither:
        return _binary_floyd_steinburg_dithering(image)

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
    return all(np.asarray(x).dtype==bool for x in as_numpy_array(color))
def is_byte_color(color):
    return all(np.issubdtype(x.dtype,np.integer) for x in as_numpy_array(color))
def is_float_color(color):
    return all(np.issubdtype(x.dtype,np.floating) for x in as_numpy_array(color))

def get_color_hue(color):
    assert is_float_color(color),'For now, get_color_hue only works with float_colors and returns a float between 0 and 1'
    import colorsys
    hue=colorsys.rgb_to_hsv(*color)[0]
    return hue

def get_color_saturation(color):
    assert is_float_color(color),'For now, get_color_saturation only works with float_colors and returns a float between 0 and 1'
    import colorsys
    hue=colorsys.rgb_to_hsv(*color)[1]
    return hue

def get_color_brightness(color):
    assert is_float_color(color),'For now, get_color_brightness only works with float_colors and returns a float between 0 and 1'
    import colorsys
    hue=colorsys.rgb_to_hsv(*color)[2]
    return hue

def get_image_dimensions(image):
    #Return (height,width) of an image
    assert is_image(image)
    return get_image_height(image),get_image_width(image)

def get_image_height(image):
    #Return the image's height measured in pixels
    assert is_image(image)
    return image.shape[0]

def get_image_width(image):
    #Return the image's width measured in pixels
    assert is_image(image)
    return image.shape[1]

#TODO: Finish color conversions

#endregion

def running_in_ipython():
    try:
        #Can detect if we're in a jupyter notebook
        # pip_import('IPython') #nooo duhh, if we don't have this installed then obviously we're not running in it...
        from IPython import get_ipython
        return get_ipython() is not None
    except Exception:
        return False#If we get an error when trying to import IPython...then..well, we're definately NOT running in iPython!
running_in_jupyter_notebook=running_in_ipython

#Commented this out because ipynbname returned the wrong answer! Idk why but it returned a path to a notebook that didn't exist...see the example; it got the class wrong somehow...
#def get_current_notebook_path()->str:
#    #Returns the path of the current jupyter notebook
#    #Example:
#    #    get_current_notebook_path() --->  '/home/ryan/CleanCode/SBU/Classes/CSE512_Machine_Learning/project_guided/CSE527_HW5_fall20.ipynb'
#    #
#    assert running_in_jupyter_notebook(),'get_current_notebook_path() must be called from inside a Jupyter Notebook'    
#    pip_import('ipynbname')
#    import ipynbname
#    path=ipynbname.path()
#    path=str(path)
#    return path
#def get_current_notebook_folder()->str:
#    return get_parent_folder(get_current_notebook_path())
#get_current_notebook_directory=get_current_notebook_folder

def running_in_google_colab():
    #Return true iff this function is called from google colab
    import sys
    return 'google.colab' in sys.modules

def running_in_ssh():
    #Returns True iff this Python session was started over SSH
    #https://stackoverflow.com/questions/35352921/how-to-check-if-python-script-is-being-called-remotely-via-ssh
    return 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ or 'SSH_CONNECTION' in os.environ

def split_tensor_into_regions(tensor,*counts,flat=True,strict=False):
    #Return the tensor into multiple rectangular regions specified by th number of cuts we make on each dimension.
    #Uses: Splitting pictures that contain multiple entried of the mnist dataset into usable chunks of data
    # Let ‹a,b,c...› represent some numpy tensor with shape (a,b,c...)
    # If strict==True, then all of tensor.shape's dimensions must evenly divide counts. Otherwise, if strict==False, tensor will be automatically cropped to accomodate the given *counts
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

    assert len(counts)<=len(tensor.shape),'We can\'t split a tensor of shape '+str(shape)+' along '+str(len(counts))+' of its dimensions becuase it only has '+str(len(shape))+' dimensions'
        
    if not strict:
        #Try to crop the tensor to make sure it evenly divides counts
        slices=[]
        for size,count in zip(tensor.shape,counts):
            slices.append(slice(0,size//count*count))
        slices=tuple(slices)
        tensor=tensor[slices]

    shape=tensor.shape
    new_shape=list(shape)

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
    #       image=load_image(image_path,use_cache=True)
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

def _highlighted_query_results(string,query):
    #Case insensitive fansi-highlighting of a query in a string
    #Example: print(_highlighted_query_results('Hello, world wORld hello woRld!','world'))#All the 'world','wORld', etc's are printed green and bold
    i=string.lower().find(query.lower())
    if i==-1:return string#No matches -> no highlighting.
    s =string[:i]
    j=i+len(query)
    s+=fansi(string[i:j],'green','bold')
    s+=_highlighted_query_results(string[j:],query)
    return s

def _rinsp_search_helper(root,query,depth=10):

    def match(name):
        assert isinstance(query,str)
        assert isinstance(name,str)
        return query.lower() in name.lower()

    def keys(root):
        out=set()
        try:out.update(dir(root))
        except Exception:pass
        try:out.update(root.__dict__)
        except Exception:pass
        return sorted(out)

    def get(root,key):
        try:return getattr(root,key)
        except Exception:pass
        try:return root.__dict__[key]
        except Exception:pass
        try:return eval('root.'+key)
        except Exception:pass
        raise

    searched=set()
    def helper(root=root,depth=depth,path=[]):
        if not depth or id(root) in searched:
            return
        searched.add(id(root))
        for name in keys(root):
            if match(name):yield path+[name]
            try:yield from helper(get(root,name),depth-1,path+[name])
            except Exception:pass

    return helper()

def rinsp_search(root,query,depth=10):
    #THIS IS A WORK IN PROGRESS
    #example: trying to find the conv function in torch? Maybe it's nested in some modules...wouldn't it be nice to automatically search the whole tree of a, a.b, a.c, a.d, b, b.a, b.a.c, etc... this does that
    #example:
    #TODO: Allow searching the docs etc more than just searching the name
    #TODO: Allow fuzzy search, better queries (fuzzy find for example with nice printed outputs)
    #TODO: Make this breadth-first instead of depth first

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        printed_lines=[]
        def print_line(line):
            print(line)
            printed_lines.append(line)

        out=[]
        for result in _rinsp_search_helper(root,query,depth):
            print_line(_highlighted_query_results('.'.join(result),query))
            out+=result
            
        _maybe_display_string_in_pager(line_join(printed_lines))

        return out




# def rinsp_search(root,query,depth=10):
#     #THIS IS A WORK IN PROGRESS
#     #example: trying to find the conv function in torch? Maybe it's nested in some modules...wouldn't it be nice to automatically search the whole tree of a, a.b, a.c, a.d, b, b.a, b.a.c, etc... this does that
#     #example:
#     #TODO: Allow searching the docs etc more than just searching the name
#     #TODO: Allow fuzzy search, better queries (fuzzy find for example with nice printed outputs)
#     #TODO: Make this breadth-first instead of depth first
#     def match(name):
#         assert isinstance(query,str)
#         assert isinstance(name,str)
#         return query.lower() in name.lower()

#     def keys(root):
#         out=set()
#         try:out.update(dir(root))
#         except Exception:pass
#         try:out.update(root.__dict__)
#         except Exception:pass
#         return sorted(out)

#     def get(root,key):
#         try:return getattr(root,key)
#         except Exception:pass
#         try:return root.__dict__[key]
#         except Exception:pass
#         try:return eval('root.'+key)
#         except Exception:pass
#         raise

#     searched=set()
#     def helper(root=root,depth=depth,path=[]):
#         if not depth or id(root) in searched:
#             return
#         searched.add(id(root))
#         for name in keys(root):
#             if match(name):yield path+[name]
#             try:yield from helper(get(root,name),depth-1,path+[name])
#             except Exception:pass

#     printed_lines=[]
#     def print_line(line):
#         print(line)
#         printed_lines.append(line)

#     out=[]
#     for result in helper():
#         print_line(_highlighted_query_results('.'.join(result),query))
#         out+=result
        
#     _maybe_display_string_in_pager(line_join(printed_lines))

#     return out

def as_numpy_array(x):
    #Will convert x into type np.ndarray
    #This should convert anything that can be converted into a numpy array
    #Should work for torch tensors, python lists of numbers, etc.
    #In particular, this works even if a torch tensor is on a GPU
    #Will necessarily make a copy of x so you dont have to worry about mutations etc
    try:return np.asarray(x)#For numpy arrays and python lists (and anything else that work with np.asarray)
    except Exception:pass
    try:return x.detach().cpu().numpy()#For pytorch. We're not doing an isinstance check of type pytorch tensor becuse that involves importing pytorch, which might be slow. Try catch is faster here.
    except Exception:pass
    assert False,'as_numpy_array: Error: Could not convert x into a numpy array. type(x)='+repr(type(x))+' and x='+repr(x)

def input_multiline():
    fansi_print('Please enter text. It can be multiple lines long. When you\'re done, press control+c or control+d','blue','bold')
    lines=[]
    while True:
        try:
            lines+=[input()]
        except KeyboardInterrupt:
            break
    return line_join(lines)

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

def input_select(question='Please select an option:',options=[],stringify=repr,reverse=False):
    #Allow the user to choose from a list of numbered options
    #stringify is how we turn options into strings (options dont have to be strings)
    #Example: Try running 'input_select_option(options=['Hello','Goodbye','Bonjour'])'

    assert len(options),'input_select: Invalid input: Cannot select from 0 options.'

    if isinstance(options,set):
        options=list(options)

    number_of_options=len(options)
    max_number_of_digits=len(str(number_of_options))

    enumerated_options=list(enumerate(options))
    if reverse:
        enumerated_options=enumerated_options[::-1]
    
    question_option_lines=[]
    for i,e in enumerated_options:
        question_option_lines.append(str(i).rjust(max_number_of_digits)+': '+stringify(e))
    question+='\n'+line_join(question_option_lines)

    def condition(user_input):
        try:
            if user_input.startswith('/'):
                return True
            if user_input in {'?','p','z','q','c'}:
                return True
            i=int(user_input)
            if i!=float(user_input):#No fractions
                return False
            return 0<=i<number_of_options
        except ValueError:#ERROR: ValueError: invalid literal for int() with base 10: 'aosijd
            return False

    def display_more_options():
        string_pager("""More options:
        - Enter 'p' to use rp.string_pager() to view your choices (this is useful if all the options can't fit on your terminal's screen)")
        - Enter 'c', 'control + c' or 'control + d' to cancel this selection
        - Enter '/' followed by a search query to display all options matching that query
              For example, enter '/.png' to get a list of options that have '.png' in them
        - Enter 'q' to enter search-query mode (will let you select an option by interactively searching for it)
        - Enter 'z' to enter fuzzy search mode (will let you select an option by interactively fuzzy-searching for it)
        """)    

    def display_query_options(query):
        if not query:
            print("Entering / by itself doesn't search for anything. Try '/.png' or '/somefile' etc instead. Enter ? for more information.")
            return
        options=question
        options=strip_ansi_escapes(options)
        options=options.splitlines()
        options=[option for option in options if query.lower() in option.lower()]
        options=[_highlighted_query_results(option,query) for option in options]
        string=line_join(options)
        _maybe_display_string_in_pager(string,False)
        if not options:
            string='(No options matched your query: %s)'%repr(query)
        print(string)


    def display_options_with_pager():
        string_pager(question)

    show_question=True
    while True:
        user_input=input_conditional(show_question*(question+'\n')+'Please enter an integer between 0 and '+str(number_of_options-1)+' (inclusive), or \'?\' for more options.',condition)
        show_question=True

        if user_input=='c':
            print("(Entered 'c': cancelling selection with a KeyboardInterrupt)")
            raise KeyboardInterrupt
        if user_input=='?':
            display_more_options()
        elif user_input=='p':
            display_options_with_pager()
        elif user_input.startswith('/'):
            query=user_input[1:]
            display_query_options(query)
            show_question=False
        elif user_input=='z' or user_input=='q':
            try:
                if user_input=='z':
                    print('Using an interactive fuzzy-search to select an option:')
                elif user_input=='q':
                    print('Using an interactive search to select an option:')
                else:
                    assert False

                displayed_question_option_lines=[strip_ansi_escapes(line).replace('\n',' ').replace('\r',' ') for line in question_option_lines] # In fzf, multiline options are not allowed

                if reverse:
                    displayed_question_option_lines=displayed_question_option_lines[::-1]

                result=_iterfzf(displayed_question_option_lines,exact=user_input=='q')

                assert result!=None

                index=displayed_question_option_lines.index(result)
                option=options[index]
                print('Selected option %i:'%index,option)
                return option

            except:
                print('    (Cancelled searching through the options)')
                show_question=False
        else:
            return options[int(user_input)]

def input_select_multiple(question='Please select any number of options:',options=[],stringify=repr,reverse=True):
    #EXAMPLE:
    #   input_select_multiple("Please select some letters:",'abcdefg')
    add_text=fansi('++ ','green','bold')
    sub_text=fansi('-- ','red'  ,'bold')
    done_text=fansi('(DONE)','yellow','bold')
    
    #This code is a bit messy, but it can be refactored later
    #It's all about how we're selecting indices instead of the actual objects

    indices=list(range(len(options)))
    selected=list() #List of indices
    unselected=list(range(len(options))) #List of indices
    
    def _stringify(option):
        if option is None:
            return done_text
        
        output=stringify(options[option])
        if option in selected:
            output=sub_text+output
        elif option in unselected:
            output=add_text+output
        else:
            assert False,'This should be impossible'
        
        return output
    
    while True:
        option=input_select(question,options=[None]+selected+unselected,stringify=_stringify,reverse=reverse)
        if option is None:
            return [options[index] for index in selected]
        if option in selected:
            selected=[x for x in selected if x!=option]
        else:
            selected+=[option]
        
        unselected=[option for option in indices if option not in selected]
        
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
def get_video_file_duration(path,use_cache=True):
    #Returns a float, representing the total video length in seconds
    if use_cache and path in _get_video_file_duration_cache:
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
def load_video(path,*,show_progress=True,use_cache=False):
    #This function does not take into account framerates or audio. It just returns a numpy array full of images.
    #It's slower than load_video_stream, but it can be cached using use_cache (which would actually make it faster, if applicable)
    progress_prefix="\rload_video: path="+repr(path)+": "
    if use_cache and path in _load_video_cache:
        return _load_video_cache[path]
    stream=load_video_stream(path)
    out=[]
    for i,frame in enumerate(stream):
        if show_progress:print(end=progress_prefix+"Loaded frame "+str(i)+"...")
        out.append(frame)
    if show_progress:print(end=progress_prefix+'done loading frames, creating numpy array...')
    out=np.asarray(out)
    if show_progress:print(end='done.\r\n')
    if use_cache:
        _load_video_cache[path]=out
    return out

def save_video_avi(frames,path:str=None,framerate:int=30):
    #Saves the frames of the video to an .avi file

    pip_import('cv2')
    import cv2
    
    if path is None:
        path=temporary_file_path()
    if not has_file_extension(path) or get_file_extension(path).lower()!='avi':
        path+='.avi'
        
    frames=as_numpy_array(frames)
    
    height=get_image_height(frames[0])
    width =get_image_width (frames[0])
    
    out = cv2.VideoWriter(path,
                      cv2.VideoWriter_fourcc(*'XVID'),
                      framerate,
                      (width,height),
                      #isColor=True
                      )
                      
    for frame in frames:
        frame=as_rgb_image(frame)
        frame=as_byte_image(frame)
        frame=cv_bgr_rgb_swap(frame)
        out.write(frame)
        
    return path

def save_video(images,path,framerate=30):
    #TODO: add options for sound and framerate. Possibly quality options but probably not (that should be delegated to a function meant for a specific format)
    #Save a series of images into a video.
    #Note that the file extension used in path decides the kind of video that will be exported.
    #For example, save_video(images,'video.mp4') saves an mp4 file whilst save_video(images,'video.avi') saves an avi file
    if not has_file_extension(path):
        try:
            return save_video_avi(images,path,framerate=framerate)
        except Exception:
            pass #No big deal, we'll try sk-video. Although, that's more annoying because it means we need FFMPEG instead of just needing OpenCV

    #Make sure all frames have ranges between 0 and 255, and that they're RGB. Otherwise we might get weird results when we save the video
    images=[as_byte_image(as_rgb_image(frame)) for frame in images]

    pip_import('skvideo.io','sk-video')
    import skvideo.io#pip install sk-video:
    #NOTE: Quicktime on my mac can't play these. Idk why. But the video outputs are NOT broken. VLC video player CAN play them without error.
    skvideo.io.vwrite(path,images,inputdict={'-r':str(framerate)})
    return path


def encode_video_to_bytes(video,filetype:str='.avi',framerate=30):
    video_file=temporary_file_path(filetype)
    
    try:
        save_video(video,video_file,framerate=framerate)
        return file_to_bytes(video_file)
    except:
        raise
    finally:
        if file_exists(video_file):
            delete_file(video_file)
    
def directory_exists(path):
    if not isinstance(path,str): return False
    return os.path.isdir(path)
folder_exists=directory_exists
is_a_folder=is_a_directory=directory_exists#Synonyms, you might want one more than another depending o nthe context. Sometimes we might want to know if it exists, and others we might allready know the path exists and want to see what kind of path it is. It's just to make it more readable, that's all. Less need for comments like these lol.

def is_empty_folder(path:str):
    if not isinstance(path,str): return False
    return is_a_folder(path) and list(get_all_paths(path,include_folders=True,include_files=True,recursive=False))==[]
is_empty_directory=is_empty_folder
    

def file_exists(path):
    if not isinstance(path,str): return False
    return os.path.isfile(path)
is_a_file=file_exists

def path_exists(path):
    if not isinstance(path,str): return False
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

from rp import *
def move_path(from_path,to_path):
    #Like the 'mv' command
    #Move a folder or file into a given directory if to_path is a directory,
    #otherwise just rename the path
    
    make_directory(get_parent_directory(to_path))#Make sure it has somewhere to go. If the destination folder doesn't already exist, create it.
    if is_a_directory(to_path):
        new_path=path_join(to_path,get_file_name(from_path))
    else:
        new_path=to_path
    os.rename(from_path,new_path)
    return new_path

move_file=move_directory=move_folder=move_path#Synonyms that might make more sense to read in their context than rename_path

def delete_file(path,*,permanent=True):
    # Deletes a file at a given path
    # permanent exists for safety reasons. It can be False in case you make a stupid mistake like deleting this file. When false, it will send your files to the trash bin on your system (Mac,Windows,Linux, etc)
    # By default, though, permanent=True, becuase when it's not it can cause your hard-drive to fill up without you expecting it (you don't normally expect to keep files when calling a function called delete file, which doesn't actually free your hard-drive when permanent=False)
    # http://stackoverflow.com/questions/3628517/how-can-i-move-file-into-recycle-bin-trash-on-different-platforms-using-pyqt4
    # https://pypi.python.org/pypi/Send2Trash
    # pip3 install Send2Trash
    import os
    assert os.path.exists(path),"r.delete_file: There is no file to delete. The path you specified, '" + path + "', does not exist!"  # This is to avoid the otherwise cryptic errors you would get later on with this method
    assert file_exists(path),"r.delete_file: The path you selected exists, but is not a file: %s"%path
    if permanent:
        os.remove(path)
    else:
        pip_import('send2trash')
        import send2trash  # This is much safer. By default, we move files to the trash bin. That way we can't accidentally delete our whole directory for good ;)
        send2trash.send2trash(path)  # This is MUCH safer than when delete_permanently is turned on. This will have the same effect as deleting it in finder/explorer: it will send your file to the trash bin instead of immediately deleting it forever.

def delete_folder(path,*,recursive=True,permanent=True):
    #Will recursively delete a folder and all of its contents
    # permanent exists for safety reasons. It can be False in case you make a stupid mistake like deleting this file. When false, it will send your files to the trash bin on your system (Mac,Windows,Linux, etc)
    # By default, though, permanent=True, becuase when it's not it can cause your hard-drive to fill up without you expecting it (you don't normally expect to keep files when calling a function called delete file, which doesn't actually free your hard-drive when permanent=False)
    # http://stackoverflow.com/questions/3628517/how-can-i-move-file-into-recycle-bin-trash-on-different-platforms-using-pyqt4
    # https://pypi.python.org/pypi/Send2Trash
    # pip3 install Send2Trash
    import shutil
    assert os.path.exists(path),"r.delete_folder: There is no folder to delete. The path you specified, '" + path + "', does not exist!"  
    assert folder_exists(path),"r.delete_folder: The path you selected exists, but is not a folder: %s"%path
    if permanent:
        if not recursive:
            assert is_empty_folder(path),'delete_folder: Cannot delete folder because its not empty and recursive==False. Folder: '+repr(path)
        shutil.rmtree(path)
    else:
        pip_import('send2trash')
        import send2trash  
        send2trash.send2trash(path)  
delete_directory=delete_folder

def delete_path(path,*,permanent=True):
    # permanent exists for safety reasons. It can be False in case you make a stupid mistake like deleting this file. When false, it will send your files to the trash bin on your system (Mac,Windows,Linux, etc)
    # By default, though, permanent=True, becuase when it's not it can cause your hard-drive to fill up without you expecting it (you don't normally expect to keep files when calling a function called delete file, which doesn't actually free your hard-drive when permanent=False)
    # http://stackoverflow.com/questions/3628517/how-can-i-move-file-into-recycle-bin-trash-on-different-platforms-using-pyqt4
    # https://pypi.python.org/pypi/Send2Trash
    # pip3 install Send2Trash
    assert os.path.exists(path),"r.delete_path: There is no folder or file to delete. The path you specified, '" + path + "', does not exist!"  
    if is_a_file(path):
        delete_file(path,permanent=permanent)
    elif is_a_folder(path):
        delete_folder(path,permanent=permanent)
    else:
        assert False, "This should be impossible...it appears that path %s exists but is neither a file nor a folder."%path

def _delete_paths_helper(*paths,permanent=True,delete_function=delete_path):
    #EXAMPLE:  delete_paths( 'a.jpg','b.jpg' )
    #EXAMPLE:  delete_paths(['a.jpg','b.jpg'])
    #EXAMPLE:  delete_paths(('a.jpg','b.jpg'))
    paths=detuple(paths)
    if isinstance(paths,str):
        paths=[paths] #if we gave a single path as an argument, turn it into a list so we can iterate over it...
    for path in paths:
        if isinstance(path,str):
            delete_function(path,permanent=permanent)

def delete_paths(*paths,permanent=True):
    _delete_paths_helper(*paths,permanent=permanent,delete_function=delete_path)

def delete_files(*paths,permanent=True):
    _delete_paths_helper(*paths,permanent=permanent,delete_function=delete_file)

def delete_folders(*paths,permanent=True):
    _delete_paths_helper(*paths,permanent=permanent,delete_function=delete_folders)
delete_directories=delete_folders

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
copy_folder=copy_directory

def copy_file(from_path,to_path):
    #Copy a single file from from_path to to_path, where to_path is either a folder or a file that will be overridden
    assert file_exists(from_path),'copy_file copies a file from from_path to to_path, but from_path='+repr(from_path)+' is not a file'
    # assert path_exists(to_path),'to_path must be either a directory or a file that will be overwritten, but to_path='+repr(to_path)+' does not exist' # <--- This seems silly. If this assertion still seems silly in the year 2022...get rid of it forever lol
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

def delete_all_paths_in_directory(directory,*,permanent=True,include_files=True,include_folders=True,recursive=False):
    assert directory_exists(directory)
    delete_paths(get_all_paths(directory,include_folders=include_folders,include_files=include_files),permanent=permanent)
delete_all_paths_in_folder=delete_all_paths_in_directory

def delete_all_files_in_directory(directory,*,recursive=False,permanent=True):
    #Ignores all folders, just deletes files
    assert directory_exists(directory),'No such directory exists: '+repr(directory)
    delete_all_paths_in_directory(directory,permanent=permanent,recursive=recursive,include_folders=False,include_files=True)
delete_all_files_in_folder=delete_all_files_in_directory

path_join=joined_paths=os.path.join#Synonyms for whatever comes into my head at the moment when using the rp terminal

_old_gists_path=path_join(get_parent_folder(__file__),'old_gists.txt') #This has to come after path_join and get_parent_folder are defined

_get_cutscene_frame_numbers_cache={}
def get_cutscene_frame_numbers(video_path,*,use_cache=False):
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
    _get_cutscene_frame_numbers_cache[video_path]=output#The output of this is so small that it's probably ok to store it even if use_cache is False. It's unlikely our memory will run out because of this...
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

def crop_image(image, height: int = None, width: int = None, origin='top left'):
    #Returns a cropped image to the specified width and height
    #If either hieght or width aren't specified (and left as None), their size will be untouched
    #    (This means you can crop an image only by height, for example, without having to manually specify its width)
    #It crops the image, keeping the top left corner the same
    #If the specified width or height are larger than the original image,
    #this function will pad out the remainder with blank black pixels
    #
    #EXAMPLE:
    #    puppy=load_image('https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSwzqzyaeWqxfQiCnOqpnd1V27Wr8MOaZtfGQ&usqp=CAU')
    #    for _ in range(500):
    #        cv_imshow(crop_image(puppy,_,_))    
    #
    #EXAMPLE:
    #    ans=load_image('https://todaysveterinarypractice.com/wp-content/uploads/sites/4/2018/06/T1807F02Fig01.jpg')
    #    for _ in range(3):
    #        for theta in np.linspace(0,pi):
    #            display_image(crop_image(ans,100+1000*np.cos(theta)**2,100+1000*np.sin(theta)**2,'center'))
    #            sleep(1/60)


    assert is_image(image)
    image_width  = get_image_width (image)
    image_height = get_image_height(image)
    assert image_height, image_width == image.shape
    assert any(image.shape),'The image must have at least 1 pixel to be cropped'

    if height is None:height=image_height
    if width  is None:width =image_width 
    height=int(height)
    width =int(width)
    assert height>=0 and width>=0, 'Images can\'t have a negative height or width'

    origins=['top left','center','bottom right'] #TODO: Possibly add more origins
    assert origin in origins,'Invalid origin: %s. Please select from %s'%(repr(origin),repr(origins))

    if origin=='bottom right':
        out = image

        out = horizontally_flipped_image(out)
        out = vertically_flipped_image  (out)

        out = crop_image(out, height = height, width = width)

        out = horizontally_flipped_image(out)
        out = vertically_flipped_image  (out)

        return out

    if origin=='center':
        out = image
        out = crop_image(out, height = (height+image_height)//2, width = (width+image_width)//2 )
        out = crop_image(out, height = height, width = width, origin = 'bottom right')
        return out

    blank_pixel=np.zeros_like(image[0][0])
    out=blank_pixel
    out=np.expand_dims(out,0)
    out=np.repeat(out,width,0)
    out=np.expand_dims(out,0)
    out=np.repeat(out,height,0)
    
    common_width =min(width ,image_width )
    common_height=min(height,image_height)
    
    out[:common_height,:common_width]+=image[:common_height,:common_width]
    
    return out

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
    if not len(points):
        points=[[0,0],[0,0]]
    top,left=np.min(points,axis=0)
    bottom,right=np.max(points,axis=0)+1
    cropped=image[top:bottom,left:right]
    #print(top,bottom,left,right)
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
    #        strings=list_flatten(string_lists)
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
except Exception:pass
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
    #Returns a generator that returns the sequence of primes
    #If you have numba, it will run very very very fast
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

def _get_parts_of_speech_via_nltk(word):
    #Given a word, return the parts of speech (adjectives, nouns, verbs etc) that this word belongs to.
    #Code from: https://stackoverflow.com/questions/35462747/how-to-check-a-word-if-it-is-adjective-or-verb-using-python-nltk
    #EXAMPLES:
    #     >>> _get_parts_of_speech_via_nltk('dog')
    #    ans = {'n'}
    #     >>> _get_parts_of_speech_via_nltk('tail')
    #    ans = {'v', 'n'}
    #     >>> _get_parts_of_speech_via_nltk('run')
    #    ans = {'v', 'n'}
    #     >>> _get_parts_of_speech_via_nltk('pretty')
    #    ans = {'s'}
    #     >>> _get_parts_of_speech_via_nltk('the')
    #    ans = set()
    #     >>> _get_parts_of_speech_via_nltk('aosidfj')
    #    ans = set()

    pip_import('nltk')
    _make_sure_nltk_has_wordnet_installed()
    from nltk.corpus import wordnet as wn
    pos_l = set()
    for tmp in wn.synsets(word):
        if tmp.name().split('.')[0] == word:
            pos_l.add(tmp.pos())
    return pos_l

def _nltk_wordnet_is_installed()->bool:
    pip_import('nltk')
    import nltk
    try:
        nltk.data.find("corpora/wordnet")
        return True
    except LookupError:
        return False

def _make_sure_nltk_has_wordnet_installed():
    #If wordnet isn't installed, this function will install it. It avoids nltk's 'Resource wordnet not found.' error.
    pip_import('nltk')
    import nltk
    if not _nltk_wordnet_is_installed():
        fansi_print("rp: Detected that while you do have nltk installed, you do not have wordnet downloaded. Downloading wordnet...",'yellow','bold')
        nltk.download('wordnet')
        fansi_print("...done!",'yellow','bold')

def is_a_verb(word:str)->bool:
    #Returns true if the given word is an english verb, false otherwise
    return 'v' in _get_parts_of_speech_via_nltk(word)

def is_an_adjective(word:str)->bool:
    #Returns true if the given word is an english adjective, false otherwise
    return 's' in _get_parts_of_speech_via_nltk(word)

def is_a_noun(word:str)->bool:
    #Returns true if the given word is an english noun, false otherwise
    #Please note that this function is far from fool-proof. is_a_noun('poop')==False, for example (which is wrong), even though is_an_english_word('poop')==True
    #However, for most english words, this will work properly.
    return 'n' in _get_parts_of_speech_via_nltk(word)

@memoized
def get_all_english_words():
    #Apparently, both Linux and Mac have a file that contains every english word! 
    #See https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python/3789057
    #TODO: Possibly might make all of these words lower case, haven't decided yet...
    if currently_running_unix():
        return set(line_split(text_file_to_string("/usr/share/dict/words")))
    else:
        assert False,'Sorry, currently only unix supports rp.all_english_words()'

@memoized
def _get_all_english_words_lowercase():
    return line_join(get_all_english_words()).lower()

def is_an_english_word(word):
    #This function is not case sensitive
    return word.lower() in _get_all_english_words_lowercase()

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
    string=str(string)
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
def get_all_importable_module_names(use_cache=True):
    """
    #Returns a set of all names that you can use 'import <name>' on
    """
    if use_cache and _all_module_names:
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
    try:
        return importlib.util.find_spec(module_name).origin
    except AttributeError:
        assert module_exists(module_name),'r.get_module_path_from_name: module %s doesnt exist!'%repr(module_name)
        raise

def get_module_path(module):
    #Returns the file path of a given python module
    if isinstance(module,str):
        return get_module_path_from_name(module)
    import inspect
    assert inspect.ismodule(module),'get_module_path error: The input you gave is not a module type. You gave input of type '+repr(type(module))
    return inspect.getfile(module)

def is_a_module(object):
    import builtins
    return type(object)==type(builtins)

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

#DEPRECATED In favor of indentify
# def indent(text:str,indent:str='    '):
#     return line_join(indent+line for line in line_split(text))



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
    except Exception:
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
    except Exception:
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
    except Exception:
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

def graham_scan(path):
    #This function is intentionally unoptimized to match my personal intuition of the algorithm most closely
    #(Might change in the future if this is a bottleneck)

    #Complex numbers make math nicer
    points=as_complex_vector(path)

    #Empty set edge case
    if len(points)==0:
        return as_numpy_array([])

    #Remove any duplicate points
    points=np.unique(points)

    #Edge cases where we aren't able to make a polygon: the original set of points is either a point or a line
    if len(points)<=2:
        return points

    #Find point with lowest y coordinate. On ties, choose the leftmost point
    bottom_left_point=min(points,key=lambda point:(point.imag,point.real))

    #Make bottom_left_point the center. We'll undo this shift at the end by adding bottom_left_point to the hull
    points=points-bottom_left_point

    #Remove the center from the pointset (because it doesn't have an angle) and add it to the hull
    points=points[np.where(points!=0)]
    hull=[0+0j]

    #Sort the points by decreasing angle (decreasing angle because I'm used to it's visualization)
    #During ties, choose the closer point first
    points=sorted(points,key=lambda point:(-np.angle(point),np.abs(point)))

    #Add the first edge to the hull (now we have a line)
    hull.append(points.pop(0))

    #The meat of the graham scan algorithm
    while points:
        point=points.pop(0)
        while True:
            edge =hull[-2:]
            if not is_counter_clockwise([*edge,point]):
                hull.append(point)
                break
            else:
                hull.pop()

    #Un-shift the points on the hull
    hull=as_numpy_array(hull)+bottom_left_point

    return hull

    #TEST CODE (run repeatedly):
    #   points=randints_complex(20,10)
    #   scatter_plot(points,dot_size=10)
    #   convex_hull=graham_scan(points)
    #   display_polygon(convex_hull,alpha=.25)

def convex_hull(points):
    #Only 2d convex hulls are supported at the moment, sorry...
    return graham_scan(points)

def _point_on_edge(point,edge):
    #Return true if a point is on an edge, including the edge's endpoints
    point,=as_complex_vector([point])
    a,b=edge
    return loop_direction_2d([point,*edge])==0 and point.real==median([point.real,a.real,b.real]) and \
                                                   point.imag==median([point.imag,a.imag,b.imag])
def _edges_intersect(edge_a,edge_b):
    edge_a=as_complex_vector(edge_a)
    edge_b=as_complex_vector(edge_b)
    assert len(edge_a==2)
    assert len(edge_b==2)

    if _point_on_edge(edge_a[0],edge_b) or \
       _point_on_edge(edge_a[1],edge_b) or \
       _point_on_edge(edge_b[0],edge_a) or \
       _point_on_edge(edge_b[1],edge_a):
       return True

    return is_clockwise([edge_a[0],*edge_b])!= \
           is_clockwise([edge_a[1],*edge_b])and\
           is_clockwise([edge_b[0],*edge_a])!= \
           is_clockwise([edge_b[1],*edge_a])

    #TEST CODE (run this over and over again):
    #    while True:
    #        edge_a=randints_complex(2,4)
    #        edge_b=randints_complex(2,4)
    #        if not _edges_intersect(edge_a,edge_b):#Depending on whether you're looking for false positives or false negatives, negate this or don't negate this
    #            break
    #    print(_edges_intersect(edge_a,edge_b))
    #    plot_clear()
    #    plot_polygon(edge_a)
    #    plot_polygon(edge_b)
    #    plot_update()

def paths_intersect(path_a,path_b)->bool:

    #Does NOT assume the paths are loops
    #O(n^2) naive algorithm. Should be full-proof.

    #Make sure we have valid paths
    path_a=as_complex_vector(path_a)
    path_b=as_complex_vector(path_b)

    #If one of the paths has no points, there are no intersections
    if not len(path_a) or not len(path_b):
        return False

    #If a path only has one point, turn that into a segment with duplicate end-points to work nicely with the rest of the code
    if len(path_a)==1:path_a=[path_a[0]]*2
    if len(path_b)==1:path_b=[path_b[0]]*2

    #Check every edge in path_a to every edge in path_b for intersections
    edges_a=map(list,zip(path_a[:-1],path_a[1:]))
    edges_b=map(list,zip(path_b[:-1],path_b[1:]))
    for edge_a in edges_a:
        for edge_b in edges_b:
            if _edges_intersect(edge_a,edge_b):
                #We found an intersection
                return True

    #No intersections were found
    return False

def _edge_intersection_positions(edge_a,edge_b):
    #Will return a list of either 0, 1 or 2 points (2 points is a special edge case where one line shares part of its segment with another line collinearly)
    a0,a1=edge_a=as_complex_vector(edge_a)
    b0,b1=edge_b=as_complex_vector(edge_b)

    output=[]
    if _point_on_edge(a0,edge_b):output.append(a0)
    if _point_on_edge(a1,edge_b):output.append(a1)
    if _point_on_edge(b0,edge_a):output.append(b0)
    if _point_on_edge(b1,edge_a):output.append(b1)
    if not output and _edges_intersect(edge_a,edge_b):#If we already detected an intersection, we don't need to run these calculations (which might even divide by 0)
        # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
        px= ( (a0.real*a1.imag-a0.imag*a1.real)*(b0.real-b1.real)-(a0.real-a1.real)*(b0.real*b1.imag-b0.imag*b1.real) ) / ( (a0.real-a1.real)*(b0.imag-b1.imag)-(a0.imag-a1.imag)*(b0.real-b1.real) ) 
        py= ( (a0.real*a1.imag-a0.imag*a1.real)*(b0.imag-b1.imag)-(a0.imag-a1.imag)*(b0.real*b1.imag-b0.imag*b1.real) ) / ( (a0.real-a1.real)*(b0.imag-b1.imag)-(a0.imag-a1.imag)*(b0.real-b1.real) )
        output.append(px+py*1j)

    return np.unique(output)

    #TEST CODE (run repeatedly):
    #   while True:
    #       edge_a=randints_complex(2,4)
    #       edge_b=randints_complex(2,4)
    #       if _edges_intersect(edge_a,edge_b):#Depending on whether you're looking for false positives or false negatives, negate this or don't negate this
    #           break
    #   print(_edges_intersect(edge_a,edge_b))
    #   plot_clear()
    #   intersection=_edge_intersection_positions(edge_a,edge_b)
    #   plot_path(edge_a,color='blue' ,alpha=.5,linestyle='--')
    #   plot_path(edge_b,color='green',alpha=.5,linestyle='-')
    #   plot_path(intersection,marker='o',linestyle='dotted',color='black',alpha=.5)
    #   plot_update()

def path_intersections(path_a,path_b):
    #TODO: Let this function take varargs paths and return all intersections
    #Returns a list of points where the two paths intersect, including edge cases (the paths intersect tangentially at a vertex, or overlap etc - it handles all of those correctly)
    path_a=as_points_array(path_a)
    path_b=as_points_array(path_b)
    output=[]
    edges_a=list(map(list,zip(path_a[:-1],path_a[1:])))
    edges_b=list(map(list,zip(path_b[:-1],path_b[1:])))
    for edge_a in edges_a:
        for edge_b in edges_b:
            if _edges_intersect(edge_a,edge_b):
                output.extend(_edge_intersection_positions(edge_a,edge_b))
    output=as_complex_vector(output)
    return np.unique(output)

def path_intersects_point(path,point)->bool:
    return paths_intersect([point],path)

def longest_common_prefix(a,b):
    #Written by Ryan Burgert, 2020. Written for efficiency's sake.
    #Works for strings, lists and tuples (and possibly other datatypes, but not numpy arrays)
    #This implementation is two orders of magnitude faster than anything I could find on the web/stack overflow/etc, especially for strings
    #It has complexity O(len(output of this function)), and a very good time constant (because it doesn't directly iterate through every element in a python loop)
    #On my computer, this function was able to compare two strings of length 1,000,000 in 0.00454 second. Here's the test I used: string='a'*10**7;tic();longest_common_prefix(string,string);ptoc() [[[tic() starts a timer, ptoc() prints out the elapsed time]]]
    #
    #EXAMPLES:
    #   longest_common_prefix('abcderty','abcdefoaisjd')                --> abcde
    #   longest_common_prefix('abcderty','abcsdefoa')                   --> abc
    #   longest_common_prefix('abcderty','asbcsdefoa')                  --> a
    #   longest_common_prefix('abcderty','aasbcsdefoa')                 --> a
    #   longest_common_prefix('aaaabdcderty','aasbcsdefoa')             --> aa
    #   longest_common_prefix(list('aaaabdcderty'),list('aasbcsdefoa')) --> ['a', 'a']
    
    len_a=len(a)
    len_b=len(b)
    out_max=min(len_a,len_b)
    s=0#Start index
    i=1#Length of proposed additional match
    while s+i<out_max and a[s:s+i]==b[s:s+i]:
        s+=i
        i*=2
    while i:
        if a[s:s+i]==b[s:s+i]:
            s+=i
        i//=2
    assert a[:s]==b[:s]
    return a[:s]


def longest_common_suffix(a,b):
    #This funcion is analagous to longest_common_prefix. See it for more documentation.
    #EXAMPLES:
    #   longest_common_suffix('12345abcd','876323abcd')        --> abcd
    #   longest_common_suffix('adofoieabcd','29348psaabcd')    --> abcd
    #   longest_common_suffix('adofoieabcd','29348psaabqcd')   --> cd
    #   longest_common_suffix([1,2,3,4,5],[7,6,3,4,5])         --> [3, 4, 5]
    #   longest_common_suffix([1,2,3,4,5],[7,3,3,4,3,6,3,4,5]) --> [3, 4, 5]

    out=longest_common_prefix(a[::-1],b[::-1])[::-1]
    if isinstance(a,str) and not isinstance(b,str):
        out=''.join(out)
    return out

def input_keypress():#catch_keyboard_interrupt=False): <---- TODO: Implement catch_keyboard_interrupt correctly! right now it doesn't work...
    #If catch_keyboard_interrupt is True, when you press control+c, it will return the control+c character instead of throwing a KeyboardInterrupt
    #Blocks the code until you press some key on the keyboard
    #Returns the characters sent to a terminal after you press that key
    #Original code from https://stackoverflow.com/questions/983354/how-do-i-make-python-wait-for-a-pressed-key
    #Note that when arrow keys are pressed, for example, more than one character might be sent - and it might vary depending on your terminal.
    #EXAMPLE: for _ in range(10): print(repr(input_keypress()))
    #EXAMPLE: Piano:
    #    print("Press keys qwertyui to play music!")
    #    major_scale=[0,2,4,5,7,9,11,12]
    #    while True:
    #        index='qwertyui'.index(input_keypress())#Intentionally, this will break the loop if we press a wrong key
    #        print(index)
    #        play_chord(major_scale[index],t=.25)
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns a tuple of characters of the key that was pressed - on Linux, 
    pressing keys like up arrow results in a sequence of characters. Returns 
    ('\x03',) on KeyboardInterrupt which can happen when a signal gets
    handled.

    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        if catch_keyboard_interrupt:
            ret.append('\x03')
        else:
            raise
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ''.join(tuple(ret))

def input_select_path(root=None,
                      *,
                      sort_by='name',
                      reverse=True,
                      message:str=None,
                      include_folders=True,
                      include_files=True,
                      file_extension_filter:str=None)->str:
    #Asks the user to select a file or folder
    #If reverse. put option 0 on the bottom instead of the top (might make it easier to read)
    #If include_files=True, allows the user to select a file
    #If include_folders=True, allows the user to select a folder
    #'message', if not None, will be displayed above the prompt
    
    assert include_files or include_folders, 'Both include_files and include_folders are False, which means the user can\'t select anything!'

    assert root is None or is_a_folder(root)
    if root is None:
        root=get_current_directory()

    folders=get_all_paths(root,sort_by=sort_by,include_files=False,include_folders=True )
    files  =get_all_paths(root,sort_by=sort_by,include_files= True,include_folders=False)
    parent =get_parent_directory(root)
    paths  =[parent]+folders
    
    if include_folders:
        #Include the option to select a folder
        paths=[None]+paths
        
    if include_files:
        paths+=files
    
    def format_path(path:str):
        if path is None:
            return fansi(root,'green','bold')
        if is_a_folder(path):
            if path==parent:
                path='..'
            path=get_folder_name(path)
            return fansi(path,'cyan','bold')
        else:
            path=get_file_name(path)
            if not file_extension_filter or get_file_extension(path) in file_extension_filter.split():
                path=fansi(path,'yellow','bold')
            else:
                path=fansi(path,'red')
            return path

    header_lines=[]
    
    if message is not None:
        header_lines.append(message)
        
    print('Current Folder:',fansi(get_absolute_path(root),'green','bold'))
    
    if include_files and not include_folders:
        header_lines.append('Please select a %s:'%fansi('file','yellow','bold'))
    elif include_folders and not include_files:
        header_lines.append('Please select a %s to navigate into it, or %s to select the current folder:'%(fansi('folder','cyan','bold'),fansi('0','green','bold')))
    elif include_files and include_folders:
        header_lines.append('Please select a %s or %s to navigate into, or %s to select the current folder:'%(fansi('file','yellow','bold'),fansi('folder','cyan','bold'),fansi('0','green','bold')))

    header=line_join(header_lines)

    selected=input_select(header,options=paths,stringify=format_path,reverse=reverse)

    if selected is None:
        return root

    if is_a_folder(selected):
        try:
            return input_select_path(selected,sort_by=sort_by,reverse=reverse,message=message,include_files=include_files,include_folders=include_folders,file_extension_filter=file_extension_filter)
        except PermissionError as error:
            print(fansi('ERROR: ','red','bold')+fansi(error,'red'))
            return input_select_path(root    ,sort_by=sort_by,reverse=reverse)
            
    print('You selected the following file: '+fansi(selected,'cyan','bold')) 

    return selected

def input_select_folder(root=None,sort_by='name',reverse=True,message=None,file_extension_filter=None)->str:
    return input_select_path(root=root,sort_by=sort_by,reverse=reverse,include_folders=True,include_files=False,message=message,file_extension_filter=file_extension_filter)

def input_select_file(root=None,sort_by='name',reverse=True,message=None,file_extension_filter=None)->str:
    return input_select_path(root=root,sort_by=sort_by,reverse=reverse,include_folders=False,include_files=True,message=message,file_extension_filter=file_extension_filter)

#def input_select_folder(root=None,sort_by='name',reverse=True)->str:
#    #Asks the user to select a folder
#    #If reverse. put option 0 on the bottom instead of the top (might make it easier to read)
#    assert root is None or is_a_folder(root)
#    if root is None:
#        root=get_current_directory()
#    assert is_a_folder(root)
#    print('Current Folder:',fansi(get_absolute_path(root),'yellow','bold'))
#    folders=get_all_paths(root,include_files=False,include_folders=True,sort_by=sort_by)
#    parent=get_parent_directory(root)
#    select_button=None
#    paths=[select_button,parent]+folders
#    def format_path(path:str):
#        if path==select_button:
#            return fansi(root,'yellow','bold')
#        else:
#            if path==parent:
#                path='..'
#            else:
#                path=get_folder_name(path)
#            path=fansi(path,'cyan','bold')
#            return path
#    selected=input_select('Please select a folder to navigate into it, or select '+fansi('0','yellow','bold')+' to choose the current folder:',options=paths,stringify=format_path,reverse=reverse)
#    if selected==select_button:
#        selected=root
#        print('You selected the following folder: '+fansi(selected,'cyan','bold')) 
#        return selected
#    else:
#        try:
#            return input_select_folder(selected,sort_by=sort_by)
#        except PermissionError as error:
#            print(fansi('ERROR: ','red','bold')+fansi(error,'red'))
#            return input_select_folder(root    ,sort_by=sort_by)

#def input_select_file(root=None,sort_by='name',reverse=True)->str:
#    #Asks the user to select a file
#    #If reverse. put option 0 on the bottom instead of the top (might make it easier to read)
#    assert root is None or is_a_folder(root)
#    if root is None:
#        root=get_current_directory()
#    print('Current Folder:',fansi(get_absolute_path(root),'cyan','bold'))
#    folders=get_all_paths(root,sort_by=sort_by,include_files=False,include_folders=True)
#    files  =get_all_paths(root,sort_by=sort_by,include_files=True,include_folders=False)
#    parent=get_parent_directory(root)
#    paths=[parent]+folders+files
#    def format_path(path:str):
#        if is_a_folder(path):
#            if path==parent:
#                path='..'
#            path=get_folder_name(path)
#            return fansi(path,'cyan','bold')
#        else:
#            path=get_file_name(path)
#            path=fansi(path,'yellow','bold')
#            return path
#    selected=input_select('Please select a file:',options=paths,stringify=format_path,reverse=reverse)
#    if is_a_folder(selected):
#        try:
#            return input_select_file(selected,sort_by=sort_by,reverse=reverse)
#        except PermissionError as error:
#            print(fansi('ERROR: ','red','bold')+fansi(error,'red'))
#            return input_select_file(root    ,sort_by=sort_by,reverse=reverse)
#    print('You selected the following file: '+fansi(selected,'cyan','bold')) 
#    return selected

def input_select_serial_device_id(*defaults)->str:
    #I use this to select arduinos when I want to connect to one with a serial port
    #After this, I generally use serial.Serial(device_id,baudrate=9600).read() etc
    #EXAMPLES:
    #    print(input_select_serial_device_id())
    #    print(input_select_serial_device_id("/dev/cu.SLAB_USBtoUART")) #Won't prompt you if "/dev/cu.SLAB_USBtoUART" is a valid option

    pip_import('serial')#Required dependency
    import serial.tools.list_ports
    ports     =list(serial.tools.list_ports.comports())
    device_ids={port.device for port in ports}

    for default in defaults:
        #Allow us to automatically select a port again if we specify it when calling this function
        assert isinstance(default,str),'The default device ids should be strings, like "/dev/cu.SLAB_USBtoUART" or "/dev/cu.Bluetooth-Incoming-Port" etc'
        if default in device_ids:
            return default

    refresh_option='(Refresh Ports)'#Select this to refresh the port list

    def option_to_string(option):
        if isinstance(option,str):
            #the option is a string
            return fansi(option,'yellow')
        else:
            #the option is a port
            return fansi(option.device,'cyan')+'\t'+fansi("Description: "+repr(option.description),'blue')

    selected_option=input_select(question="Please choose a port:",options=[refresh_option,*ports],stringify=option_to_string)

    if selected_option is refresh_option:
        #the selected_option is a string
        return input_select_serial_device_id(*defaults)
    else:
        #the selected_option is a port
        return selected_option.device

def temporary_file_path(file_extension:str=''):
    #Returns the path of a temporary, writeable file
    #(No more pesky "don't have permission to write" errors)
    #https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
    import tempfile
    f = tempfile.NamedTemporaryFile(mode='w') # open file
    temp = f.name  
    if file_extension:
        if not file_extension.startswith('.'):
            file_extension='.'+file_extension
        temp += file_extension
    return temp

@memoized
def python_2_to_3(code:str)->str:
    #Turns python2 code into python3 code
    #EXAMPLE: python_2_to_3("print raw_input('>>>')") --> "print(input('>>>'))"
    pip_import('lib2to3','2to3')#Make sure this is installed
    assert isinstance(code,str),'code should be a string but got type '+repr(type(code))
    # from rp import r
    # temp_file_path=__file__+'.python_2_to_3_temp.py'
    temp_file_path=temporary_file_path()#get_absolute_path(temp_file_path)
    string_to_text_file(temp_file_path,code)
    import sys
    from subprocess import Popen, PIPE, STDOUT
    p = Popen([sys.executable,'-m','lib2to3','-w',temp_file_path], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=code.encode())[0]
    return text_file_to_string(temp_file_path)
    return (stdout_data.decode())

def strip_python_comments(code:str):
    #Takes a string, and returns a string
    #Removes all python #comments from code with a scalpel (not touching anything else)
    #Todo: Add an option to delete entire lines of comments (when a line is literally just a comment)
    #Todo: Add option to delete multiline strings that just serve as comments
    return ''.join(token for token in split_python_tokens(code) if not token.startswith('#'))

def strip_trailing_whitespace(string):
    #Takes a string, and returns a string
    #Returns a new string, with all trailing whitespace removed from the end of every line. Doesn't change the number of lines.
    #Useful for refactoring code to get rid of trailing whitespace.
    return '\n'.join([line.rstrip() for line in string.splitlines()])

def delete_empty_lines(string,strip_whitespace=False):
    #Takes a string, and returns a string
    #Removes all lines of length 0 from the string and returns the result
    #If strip_whitespace is True, it will also delete lines that have nothing but whitespace
    return '\n'.join([line for line in string.splitlines() if (line.strip() if strip_whitespace else line)])

____file=path_join(get_parent_directory(__file__),'.'+get_file_name(__file__))#/usr/local/lib/python3.7/site-packages/rp/.r.py
rprc_file_path=strip_file_extension(____file)+'.rprc.py'
rprc_file_path=path_join(get_parent_directory(__file__),'.rprc')
_default_rprc="""## %s
## This is the rprc file. Like .bashrc, or .vimrc, this file is run each time you boot rp from the command line.
## Even though the extension of this file is .rprc, and not .py, treat it as a python file.
## Feel free to commment/uncomment any of the lines here, or to add your own. This file is preserved when you update rp.

## Add the current directory to the path, letting us import any files in the directory we booted rp in
## For example, if we run 'rp' in a directory with 'thing.py', let us run 'import thing.py' by enabling the belowline
import os,sys;sys.path.append(os.getcwd());del os,sys;

## Import the rp library's whole namespace. It's not nessecary, but it exposes a lot of useful functions without
#from rp import *

## Set the terminal's cursor to the shape of a line, instead of a block. I personally prefer this, but I've commented out because I don't know if you'd like it.
#set_cursor_to_bar()

"""%rprc_file_path

def _get_ryan_rprc_path():
    if not file_exists(rprc_file_path):
        string_to_text_file(rprc_file_path,_default_rprc)
    return text_file_to_string(rprc_file_path)

def _set_ryan_rprc():
    rprc_file_path=_get_ryan_rprc_path()
    string_to_text_file(rprc_file_path,text_file_to_string(rprc_file_path)+'\n'+'from rp import *')
    print("Your rprc file has been modified.")
    

def _set_ryan_vimrc():
    vimrc=text_file_to_string(get_module_path_from_name('rp.ryan_vimrc'))
    string_to_text_file(get_absolute_path('~/.vimrc'),vimrc)
    shell_command('git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim')
    import os
    os.system('vim +PluginInstall +qall')
    print("Finished setting your ~/.vimrc vim settings. Give it a try! Enter 'ans?v' without quotes to see your new ~/.vimrc file")

def _set_ryan_xonshrc():
    xonshrc_path=get_absolute_path('~/.xonshrc')
    xonfig=text_file_to_string(xonshrc_path) if file_exists(xonshrc_path) else ''
    
    ryan_xonfig='''
$PROMPT = "{BOLD_CYAN} >> {BOLD_CYAN}{cwd_base}{branch_color}{curr_branch: {}}{NO_COLOR} "
$CASE_SENSITIVE_COMPLETIONS = False
'''
    string_to_text_file(xonshrc_path,xonfig+ryan_xonfig)
    print("Your ~/.xonshrc file has been modified. Use the SHELL command to try it out!")

def _set_ryan_tmux_conf():
    conf='''
#Ryan Burgert's Tmux config
#Main changes:
#   - You can use the mouse to move panes around
#   - The history limit is way higher than the default
#   - Vim-like bindings have been added:
#       - hjkl for pane navigation
#       - When in copy move (after ctrl+b then [), use 'v' to start a selection then 'y' to yank it
#           - When this selection is yanked, it's sent to your system clipboard, which means you can paste it again somewhere else (i.e. sublime text, for example). NOTE: On Linux, please install 'sudo apt install xclip' to make this work!)

set -g mouse on 
set -g history-limit 99999
# set-option -g prefix M-b


#Allow vim-like navigation: https://stackoverflow.com/questions/30719042/tmux-using-hjkl-to-navigate-panes
set -g status-keys vi
setw -g mode-keys vi
# smart pane switching with awareness of vim splits
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
bind-key -T copy-mode-vi 'v' send -X begin-selection     # Begin selection in copy mode.
bind-key -T copy-mode-vi 'C-v' send -X rectangle-toggle  # Begin selection in copy mode.

# Let tmux copy to the system clipboard.
# First, please run   git clone https://github.com/tmux-plugins/tmux-yank ~/clone/path
run-shell ~/clone/path/yank.tmux
set -g @yank_with_mouse on
set -g @yank_selection_mouse 'clipboard' # or 'primary' or 'secondary'

#Let tmux use 256 colors, instead of being limited to plain boring ascii colors
set -g default-terminal "screen-256color"
    '''
    conf_path=get_absolute_path("~/.tmux.conf")
    if not file_exists(conf_path) or input_yes_no("You already have a tmux config file ~/.tmux.conf, would you like to overwrite it?"):
        string_to_text_file(conf_path,conf)
        shell_command('git clone https://github.com/tmux-plugins/tmux-yank ~/clone/path')
        print("Succesfully configured your tmux! Please restart tmux to see the changes.")


def can_convert_object_to_bytes(x:object)->bool:
    #Returns true if we can run object_to_bytes on x without getting an error
    #See object_to_bytes for more documentation
    dill=pip_import('dill')
    return dill.pickles(x)#https://stackoverflow.com/questions/17872056/how-to-check-if-an-object-is-pickleable

def object_to_bytes(x:object)->bytes:
    #Try to somehow turn x into a bytestring. 
    #Right now, it supports numpy arrays, lambdas and functions, dicts lists and tuples and everything pickle can handle
    #Should be able to serialize things like numpy arrays, and pickleable objects
    #However it works is a black box, as long as it can be decoded by the bytes_to_object function
    # assert can_convert_object_to_bytes(x),'Sorry, but we cannot serialize this object to a bytestring'
    dill=pip_import('dill')
    return dill.dumps(x)

def bytes_to_object(x:bytes)->object:
    #Inverse of object_to_bytes, see object_to_bytes for more documentation
    dill=pip_import('dill')
    try:
        return dill.loads(x)
    except Exception:
        return x #bytestrings allready are objects. In the event that we have an error, it might make sense just to return the original bytestring

_web_clipboard_url = 'https://ryanpythonide.pythonanywhere.com'#By sqrtryan@gmail.com account
def web_copy(data:object)->None:
    #Send an object to RyanPython's server's clipboard
    assert connected_to_internet(),"Can't connect to the internet"
    # assert can_convert_object_to_bytes(data),'rp.web_copy error: Cannot turn the given object into a bytestring! Maybe this type isnt supported? See can_convert_object_to_bytes for more help. The type of object you gave: '+repr(type(data))
    import requests
    response=requests.post(_web_clipboard_url,data=object_to_bytes(data))
    assert response.status_code==200,'Got bad status code that wasnt 200: '+str(response.status_code)

def web_paste():
    #Get an object from RyanPython's server's clipboard
    assert connected_to_internet(),"Can't connect to the internet"
    import requests         
    response=requests.get(_web_clipboard_url) 
    assert response.status_code==200,'Got bad status code that wasnt 200: '+str(response.status_code)
    return bytes_to_object(response.content)

def tmux_copy(string:str):
    #Copies a string to tmux's clipboard, assuming tmux is running and installed
    assert isinstance(string,str),'You can only copy a string to the tmux clipboard'
    temp_file_path=temporary_file_path()
    try:
        string_to_text_file(temp_file_path,string)
        shell_command('tmux load-buffer '+temp_file_path)
    finally:
        delete_file(temp_file_path)

def tmux_paste():
    #Returns the string from tmux's current clipboard, assuming tmux is running and installed
    tmux_clipboard=shell_command('tmux show-buffer')
    return tmux_clipboard

_local_dill_clipboard_string_path=__file__+'.rp_local_dill_clipboard'
def local_copy(data:object):
    #Works just like web_copy, but is local to one's computer
    #This makes copying large python objects between processes practical
    file=open(_local_dill_clipboard_string_path,'wb')
    file.write(object_to_bytes(data))
    file.close()

def local_paste():
    #Works just like web_paste, but is local to one's computer
    #This makes copying large python objects between processes practical
    file=open(_local_dill_clipboard_string_path,'rb')
    return bytes_to_object(file.read())
    
    
    
def extract_code_from_ipynb(path:str=None):
    #This function isnt meant to be used in any code. Its just a utility for running ipynb files in rp, by extracting their code into cells that can be run individually
    import json
    if path is None:
        path=input_select_file(file_extension_filter='ipynb')
    assert path_exists(path),'Sorry, but '+repr(path)+' doesnt exist'
    path=text_file_to_string(path)
    notebook=json.loads(path)
    code_cells=[''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type']=='code'] 
    code_cells=[code_cell for code_cell in code_cells if code_cell.strip()]
    notebook_code='\n\n#################################\n\n'.join(code_cells)
    notebook_code=line_join((line if not (line.startswith('%') or line.startswith('!')) else '#'+line) for line in line_split(notebook_code))
    ans=notebook_code
    return ans

@memoized
def _get_facebook_client(email,password):
    #Cache this to make it faster when sending repeated messages etc
    assert False,'This function is currently broken and will fail to log into facebook because a dependency called fbchat is no longer maintained and no longer compatiable with facebook.com\'s api. TODO: Update this function'
    pip_import('fbchat')
    import fbchat
    return fbchat.Client(email,password)

def send_facebook_message(message:str=None,my_email:str=None,my_password:str=None):
    pip_import('fbchat')
    import fbchat as f
    e=my_email or input("Please enter your facebook account's email: ")
    p=my_password or input("Please enter your facebook account's password: ")
    me=_get_facebook_client(e,p)
    users=me.fetchAllUsers()
    users=sorted(users,key= lambda x: x.name)
    user=input_select('Please select the user you\'d like to message: ',users,stringify=lambda x:x.name)
    m=message or input("Please enter your message: ")
    user_id=user.uid
    return me.sendMessage(m,user_id)

def get_all_facebook_messages(my_email:str=None,my_password:str=None,my_name:str=None,max_number_of_messages:int=9999)->list:
    #Returns a list of all messages between you and one of your contacts on facebook
    #Uses a python package called 'fbchat' to do this
    #I used this to download all messages between me and one of my friends for safekeeping (facebook makes this difficult)
    #Todo: Let this import groupchat history and not just direct messages between you and someone else
    pip_import('fbchat')
    import fbchat as f
    e=my_email or input("Please enter your facebook account's email: ")
    p=my_password or input("Please enter your facebook account's password: ")
    my_name=input("Please enter your name: ")
    me=_get_facebook_client(e,p)
    users=me.fetchAllUsers()
    users=sorted(users,key= lambda x: x.name)
    user=input_select('Please select another facebook user:',users,stringify=lambda x:x.name)
    user_id=user.uid
    user_name=user.name
    messages=me.fetchThreadMessages(user_id,limit=max_number_of_messages)
    messages=messages[::-1]#Make the most recent message come last, not first. This is the way it shows it in facebook messenger
    def format(a,t):
        a=str(a)
        t=str(t)
        o=a
        o+='\n'
        o+=t
        return o
    message_tuples=[(user_name if m.author==user_id else my_name, m.text) for m in messages]
    message_strings=[format(*message_tuple) for message_tuple in message_tuples]
    output='\n\n'.join(message_strings)
    print(output)
    return message_tuples

def visualize_pytorch_model(model,*,input_shape=None, example_input=None):
    #TODO: integrate code better with _visualize_pytorch_model_via_torchviz: get rid of redundant code
    #Show a graph depicting some pytorch-based neural network
    # - model: should be some neural network model created in pytorch
    # - input_shape: should be the shape of a single input. For example, if MNIST is the input, input_shape should be [28, 28].
    #      We need input_shape in order to determine the size of each layer in the network.
    # - example_input: an alternative to using input_shape (particularly useful for networks that don't take torch.Tensor in their forward model)
    #See https://github.com/waleedka/hiddenlayer/blob/master/demos/pytorch_graph.ipynb for a demo
    #
    #EXAMPLE:
    #    import torchvision.models
    #    model = torchvision.models.vgg16()
    #    visualize_pytorch_model(model,[3,224,224])
        
    pip_import('hiddenlayer')  #This library is used to draw the neural network. See github.com/waleedka/hiddenlayer
    pip_import('torch'      )  #We obviously need pytorch installed to use this function
    pip_import('graphviz')
    import hiddenlayer, torch
    assert isinstance(model,torch.nn.Module)    

    assert example_input is None or input_shape is None,'Please only specify one, not both: either input_shape or example_input should be None'
    
    if input_shape is not None:
        input_shape=[1, *input_shape] #The first dimension refers to the number of samples. For simplicity's sake, we're going to use just one sample.
        model_input=torch.zeros(input_shape)
        model=model.cpu()
    else:
        model_input=example_input

    graph = hiddenlayer.build_graph(model=model, args=model_input)
    
    if running_in_ipython(): 
        #If we're in a jupyter notbook, display the graph inside it 
        from IPython.display import display
        display(graph)
    else:
        file_type = 'pdf'
        output_path = temporary_file_path(file_type)
        graph.save(path=output_path, format=file_type)
        # display_image(load_image(output_path),block=block) #We would use this line if we wanted to rasterize it. However, a PDF is probably the best option
        open_file_with_default_application(output_path)# If we're making a pdf, open it in some pdf viewer

#def _visualize_pytorch_model_via_torchviz(model,*,input_shape=None, example_input=None):
#    pip_import('torch'      )
#    pip_import('torchviz'   )
#    import torch
#    import torchviz
#    assert isinstance(model,torch.nn.Module)    

#    assert example_input is None or input_shape is None,'Please only specify one, not both: either input_shape or example_input should be None'
    
#    if input_shape is not None:
#        input_shape=[1, *input_shape] #The first dimension refers to the number of samples. For simplicity's sake, we're going to use just one sample.
#        model_input=torch.zeros(input_shape)
#        model=model.cpu()
#    else:
#        model_input=example_input

#    return torchviz.make_dot(model(model_input))


#def visualize_pytorch_model_via_torchviz(model,*,input_shape=None, example_input=None):
#    #TODO: integrate code better with _visualize_pytorch_model_via_torchviz: get rid of redundant code
#    #Show a graph depicting some pytorch-based neural network
#    # - model: should be some neural network model created in pytorch
#    # - input_shape: should be the shape of a single input. For example, if MNIST is the input, input_shape should be [28, 28].
#    #      We need input_shape in order to determine the size of each layer in the network.
#    # - example_input: an alternative to using input_shape (particularly useful for networks that don't take torch.Tensor in their forward model)
#    #See https://github.com/waleedka/hiddenlayer/blob/master/demos/pytorch_graph.ipynb for a demo
#    #
#    #EXAMPLE:
#    #    import torchvision.models
#    #    model = torchvision.models.vgg16()
#    #    visualize_pytorch_model(model,[3,224,224])
#    return _visualize_pytorch_model_via_hiddenlayer(model,input_shape=input_shape,example_input=example_input)
#    return _visualize_pytorch_model_via_torchviz(model,input_shape=input_shape,example_input=example_input)

def inverted_color(color):
    if   is_binary_color(color):
        return tuple(not x for x in color)
    elif is_byte_color(color):
        return tuple(255-x for x in color)
    elif is_float_color(color):
        return tuple(1-x for x in color)
    else:
        raise TypeError('Unknown color format')

def inverted_image(image,invert_alpha=False):
    #Inverts the colors of an image. By default, it doesn't touch the alpha channel (if one exists)
    assert is_image(image)
    image=image.copy()
    if is_rgba_image(image) and not invert_alpha:
        if is_byte_image(image):
            image[:,:,:3]=255-image[:,:,:3]
        elif is_float_image(image):
            image[:,:,:3]=1-image[:,:,:3]
        elif is_binary_image(image):
            image[:,:,:3]=~image[:,:,:3]
    else:
        if is_byte_image(image):
            image=255-image
        elif is_float_image(image):
            image=1-image
        elif is_binary_image(image):
            image=~image
    return image

def make_zip_file_from_folder(src_folder:str=None, dst_zip_file:str=None)->str:
    #Creates a .zip file on your hard drive.
    #Zip the contents of some src_folder and return the output zip file's path
    if src_folder is None:
        print("Please select a folder whose contents you'd like to zip:")
        src_folder=input_select_folder()
        
    temp_path=temporary_file_path()
    import shutil
    shutil.make_archive(temp_path, 'zip', src_folder)
    temp_path+='.zip'

    if dst_zip_file is None:
        dst_zip_file=temp_path
    else:
        move_file(temp_path,dst_zip_file)
        
    return dst_zip_file

def extract_zip_file(zip_file_path,folder_path=None):
    #Extracts a zip file to a given folder
    #If that folder doesn't exist, create it
    if folder_path==None:
        #By default, extract path/to/thing.zip to a new folder called path/to/thing
        folder_path=strip_file_extension(zip_file_path)
    assert isinstance(zip_file_path,str)
    assert isinstance(folder_path,str)
    make_directory(folder_path)
    assert folder_exists(folder_path)

    if get_file_extension(zip_file_path)=='zip':
        #If we're just unpacking a zip file, we don't need pyunpack (a pypi package that's used for .rar files, .7z files etc)
        import zipfile
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)
    else:
        #If it's not a zip file, don't give up. We can still unzip rar, jar, 7z, and other filetypes with the help of pyunpack
        _extract_archive_via_pyunpack(zip_file_path, folder_path)

    return folder_path
unzip_to_folder=extract_zip_file

def _extract_archive_via_pyunpack(archive_path, folder_path):
    #This function is used to unpack more than just .zip files.
    #It can unpack .rar files, .tar files, .7z files - etc!
    #On linux, you might have to apt-install a package to get this function to work
    #For example: 'apt install patool', 'apt install rar', etc
    #SUPPORTED FILETYPES:
    # 7z       (.7z)
    # ACE      (.ace)
    # ALZIP    (.alz)
    # AR       (.a)
    # ARC      (.arc)
    # ARJ      (.arj)
    # BZIP2    (.bz2)
    # CAB      (.cab)
    # compress (.Z)
    # CPIO     (.cpio)
    # DEB      (.deb)
    # DMS      (.dms)
    # GZIP     (.gz)
    # LRZIP    (.lrz)
    # LZH      (.lha .lzh)
    # LZIP     (.lz)
    # LZMA     (.lzma)
    # LZOP     (.lzo)
    # RPM      (.rpm)
    # RAR      (.rar)
    # RZIP     (.rz)
    # TAR      (.tar)
    # XZ       (.xz)
    # ZIP      (.zip .jar)
    # ZOO      (.zoo)

    pip_import('pyunpack')

    filetype=get_file_extension(archive_path)
    supported_filetypes='7z ace alz a arc arj bz2 cab Z cpio deb dms gz lrz lha lzh lz lzma lzo rpm rar rz tar xz zip jar zoo'.lower().split()
    assert filetype.lower() in supported_filetypes, 'Sorry, but I dont know how to unpack/extract/unzip etc the given filetype .'+filetype+'\n\tSupported filetypes: '+' '.join(supported_filetypes)
    
    from pyunpack import Archive
    Archive(archive_path).extractall(folder_path)

    return folder_path

def get_normal_map(bump_map):
    #Turn a bump map aka a height map, into a normal map
    #This is used for 3d graphics, such as in video games
    #EXAMPLE:
    #    ans=load_image('https://www.filterforge.com/filters/6422-bump.jpg')
    #    ans=get_normal_map(ans)
    #    display_image(full_range(ans))
    assert is_image(bump_map)
    pip_import('snowy')#A truly delightful little image processing library!
    import snowy
    bump_map=as_grayscale_image(as_float_image(bump_map))
    bump_map=np.expand_dims(bump_map,2)#Snowy needs to have a third axis for colors
    normal_map=snowy.compute_normals(bump_map)
    return normal_map

def sobel_edges(image):
    #Calculates sobel edges for edge detection
    #Computes it indivisually for each r,g,b channel
    #   - Because of this feature, this function is approximately 3x faster on grayscale images
    #EXAMPLE:
    #    ans=load_image('https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSwzqzyaeWqxfQiCnOqpnd1V27Wr8MOaZtfGQ&usqp=CAU'))
    #    ans=sobel_edges(ans)
    #    display_image(ans)
    assert is_image(image)
    pip_import('snowy')#A truly delightful little image processing library!
    import snowy

    image=as_float_image(image)
    if is_grayscale_image(image):
        image=np.expand_dims(image,2)
        output=snowy.compute_sobel(image)
        output=output.squeeze(2)
        return output

    else:
        image=as_rgb_image(image)

        red  =snowy.compute_sobel(np.expand_dims(image[:,:,0],2))
        green=snowy.compute_sobel(np.expand_dims(image[:,:,1],2))
        blue =snowy.compute_sobel(np.expand_dims(image[:,:,2],2))
    
        output=np.dstack((red,green,blue))
    return output

def currently_in_a_tty():
    #Returns True if we're in a TTY (aka a terminal that can run Prompt-Toolkit)
    #(As opposed to, for example, running inside a jupyter notebook)
    try:
        return sys.stdout.isatty()
    except Exception:
        #Perhaps the current stdout, maybe patched, breaks when we do this...
        return False


def _maybe_display_string_in_pager(string,with_line_numbers=True):
    #Display the string in the pager if it's too long
    if currently_in_a_tty():
        # if number_of_lines_in_terminal(string) > get_terminal_height()*.75:
        if number_of_lines_in_terminal(string) > get_terminal_height()-5:#This takes into account the prompt-toolkit prompt height, which I believe is hardcoded to 7 lines from the bottom of the terminal
            ring_terminal_bell()
            display_string=_line_numbered_string(string) if with_line_numbers else string
            string=fansi("There were %i lines with %i characters in the output, which would print out for many (%i) lines in your terminal. So, we're displaying them with rp.string_pager. Press 'q' to exit, -S to toggle line wrapping, and use arrow keys to navigate (or press 'h' for more help)"%(number_of_lines(string),len(string),number_of_lines_in_terminal(string)),'blue','bold')+'\n'+display_string
            string_pager(string)
    


def _fd(query,select=False):
    #Act like the 'fd' command 
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
    from glob import iglob, escape
    from itertools import chain
    glob_query='*'+escape(query)+'*'
    printed_lines=[]
    def print_line(line):
        print(line)
        printed_lines.append(line)
    query=query.lower()
    try:
        for result in glob.iglob('**',recursive=True):
        # for result in chain( iglob(glob_query), iglob('*/**/'+glob_query,recursive=True)):
            if query in get_path_name(result):  
                print_line(highlighted(result,query))
    except KeyboardInterrupt:
        pass
    _maybe_display_string_in_pager(line_join(printed_lines))
    return printed_lines
    # if sys.stdout.isatty() and len(printed_lines)>get_terminal_height()*.75:
    #     ring_terminal_bell()
    #     printed_lines.insert(0,fansi("FD: There were many (%i) results, so we're displaying them with rp.string_pager. Press 'q' to exit, and use arrow keys to navigate (or press 'h' for more help)"%len(printed_lines),'blue','bold'))
        
    #     string_pager(line_join(printed_lines))

def get_image_file_dimensions(image_file_path:str):
    #Takes the file path of an image, and returns the image's (height, width)
    #It does this without loading the entire image, so while 
    #   get_image_file_dimensions(image_file_path) == get_image_width,get_image_height (load_image(image_file_path))
    #This method can be up to 4000 times faster.
    #This method supports the following file types:
    #    png jpg gif tiff svg jpeg jpeg2000
    assert file_exists(image_file_path)
    pip_import('imagesize')
    import imagesize
    return imagesize.get(image_file_path)#Returns (width, height)

def rgb_to_hsv(image):
    #Takes an RGB image and returns an HSV image
    #Any alpha channels will be removed
    #EXAMPLE: Animating a rainbow doggy
    #    i=load_image('https://www.rover.com/blog/wp-content/uploads/2018/04/ThinkstockPhotos-485251240-960x540.jpg')
    #    for _ in range(100):
    #        i=rgb_to_hsv(i)
    #        i[:,:,0]+=.05
    #        i=hsv_to_rgb(i)
    #        display_image(i)
    assert is_image(image)
    image=as_float_image(image)
    image=as_rgb_image(image)
    pip_import('skimage')
    import skimage.color as color
    return color.rgb2hsv(image)

def hsv_to_rgb(image):
    #Takes an RGB image and returns an HSV image
    #Any alpha channels will be removed
    assert is_image(image)
    image=as_float_image(image)
    image=as_rgb_image(image)
    pip_import('skimage')
    import skimage.color as color
    return color.hsv2rgb(image)

def get_image_hue(image):
    assert is_image(image)
    return rgb_to_hsv(image)[:,:,0]

def get_image_saturation(image):
    assert is_image(image)
    return rgb_to_hsv(image)[:,:,1]

def get_image_value(image):
    assert is_image(image)
    return rgb_to_hsv(image)[:,:,2]

def apply_colormap_to_image(image,colormap_name='viridis'):
    # https://stackoverflow.com/questions/52498777/apply-matplotlib-or-custom-colormap-to-opencv-image/52626636
    # EXAMPLE:
    #    image=load_image('https://www.gaytimes.co.uk/wp-content/uploads/2018/05/Kim-Petras-Thom-Kerr-header.jpg')
    #    styles='Accent Accent_r Blues Blues_r BrBG BrBG_r BuGn BuGn_r BuPu BuPu_r CMRmap CMRmap_r Dark2 Dark2_r GnBu GnBu_r Greens Greens_r Greys Greys_r OrRd OrRd_r Oranges Oranges_r PRGn PRGn_r Paired Paired_r Pastel1 Pastel1_r Pastel2 Pastel2_r PiYG PiYG_r PuBu PuBuGn PuBuGn_r PuBu_r PuOr PuOr_r PuRd PuRd_r Purples Purples_r RdBu RdBu_r RdGy RdGy_r RdPu RdPu_r RdYlBu RdYlBu_r RdYlGn RdYlGn_r Reds Reds_r Set1 Set1_r Set2 Set2_r Set3 Set3_r Spectral Spectral_r Wistia Wistia_r YlGn YlGnBu YlGnBu_r YlGn_r YlOrBr YlOrBr_r YlOrRd YlOrRd_r afmhot afmhot_r autumn autumn_r binary binary_r bone bone_r brg brg_r bwr bwr_r cividis cividis_r cool cool_r coolwarm coolwarm_r copper copper_r cubehelix cubehelix_r flag flag_r gist_earth gist_earth_r gist_gray gist_gray_r gist_heat gist_heat_r gist_ncar gist_ncar_r gist_rainbow gist_rainbow_r gist_stern gist_stern_r gist_yarg gist_yarg_r gnuplot gnuplot2 gnuplot2_r gnuplot_r gray gray_r hot hot_r hsv hsv_r inferno inferno_r jet jet_r magma magma_r nipy_spectral nipy_spectral_r ocean ocean_r pink pink_r plasma plasma_r prism prism_r rainbow rainbow_r seismic seismic_r spring spring_r summer summer_r tab10 tab10_r tab20 tab20_r tab20b tab20b_r tab20c tab20c_r terrain terrain_r twilight twilight_r twilight_shifted twilight_shifted_r viridis viridis_r winter winter_r'.split()
    #    for style in styles:
    #        display_image(apply_colormap_to_image(image,style))
    #        input(style)
    pip_import('cmapy')
    pip_import('cv2')
    import cv2
    import cmapy
    image=as_rgb_image(image)
    image=as_byte_image(image)
    image_colorized = cv2.applyColorMap(image, cmapy.cmap(colormap_name))
    image_colorized = cv_rgb_bgr_swap(image_colorized)
    return image_colorized

def big_ascii_text(text:str,*,font='standard'):
    #Returns big ascii art text!
    #EXAMPLE:
    # ➤ big_ascii_text('Hello World!')
    #    ans =  
    #     _   _        _  _         __        __              _      _  _ 
    #    | | | |  ___ | || |  ___   \ \      / /  ___   _ __ | |  __| || |
    #    | |_| | / _ \| || | / _ \   \ \ /\ / /  / _ \ | '__|| | / _` || |
    #    |  _  ||  __/| || || (_) |   \ V  V /  | (_) || |   | || (_| ||_|
    #    |_| |_| \___||_||_| \___/     \_/\_/    \___/ |_|   |_| \__,_|(_)
    #Some of my favorite fonts:
    #    varsity
    #    sub-zero
    #    stop
    #    stforek
    #    starwars
    #    standard
    #    speed
    #    slant
    #    serifcap
    #    roman
    #    puffy
    #    poison
    #    nvscript
    #    fratkur
    #    doh
    #    cybermedium
    #    big
    #    alpha
    #    fancy92
    #    fancy89
    #    fancy57
    #    fancy61

    pip_import('art')
    import art
    assert font in art.FONT_NAMES,'Please choose from the following fonts:'+'\n'+repr(art.FONT_NAMES)
    big_text=art.text2art(text,font)
    return big_text

#class torch_utils:
#    #This class might later become a module.
#    #This class holds utility functions specific to pytorch
#    def as_torch_image(image):
#        import torch
#        if isinstance(image,torch.Tensor):
#            return image
#        else:
#            image=as_numpy_array(image)
#            assert is_image(image)
#            if is_grayscale_image(image):
#                image=np.expand_dims(image,2)
#            image=image.transpose(2,0,1)
#            image=torch.Tensor(image)
#            return image
#    def as_numpy_image(image):
#        import torch
#        if isinstance(image,torch.Tensor):
#            image=as_numpy_array(image)
#            image=image.transpose(1,2,0)
#            if image.shape[2]==1:
#                image=image.squeeze(2)
#            return image
#        else:
#            assert is_image(image)
#            return image
#    class ImageFolderDataset(torch.utils.data.Dataset):
#        # A pytorch image dataset which features image caching, making 10x or more times as fast
#        def __init__(self,folder:str):
#            self.recognized_file_types='apng bmp cur gif ico jfif jpeg jpg pjp pjpeg png svg tif tiff webp'
#            self.folder=folder
#            self.refresh_paths()
#        def refresh_paths(self):
#            self.paths=rp.get_all_paths(self.folder,file_extension_filter=self.recognized_file_types,include_files=True,include_folders=False)
#        def __len__(self):
#            return len(self.paths)
#        def __getitem__(self,index):
#            image_path=self.paths[index]
#            image=rp.load_image(image_path,use_cache=True)
#            image=as_torch_image(image)
#            return image

def bytes_to_file(data:bytes,path:str=None):
    assert isinstance(data,bytes)
    if path is None:
        path=temporary_file_path()
    try:
        out=open(path,'wb')
        out.write(data)
    finally:
        out.close()
    return path
    
def file_to_bytes(path:str):
    try:
        out=open(path,'rb')
        data=out.read()
    finally:
        out.close()
    return data

def file_to_object(path:str):
    return bytes_to_object(file_to_bytes(path))

def object_to_file(object,path:str):
    return bytes_to_file(object_to_bytes(object),path)



def _launch_ranger():
    #Ranger is a curses-based file manager with Vim keybindings
    #It's really useful for quickly/visually browsing through files and directories!
    #Whatsmore, is that we can launch it in this process - which is what we'll do.
    #Currently this method is private, as I can't think of a reason to use it outside of pseudo_terminal and I don't want to clutter rp's namespace more

    pip_import('ranger')
    import ranger
    old_os_environ_pwd=os.environ.get('PWD')#This is how ranger determines the current directory. We want to make sure it syncs up with RP's PWD, but also want to resore os.environ.get('PWD') afterwards in-case some other function needs it to work the way it originally did
    old_args=sys.argv
    try:
        sys.argv=sys.argv[:1]
        os.environ['PWD']=get_current_directory()
        out=ranger.main()
    finally:
        os.environ['PWD']=old_os_environ_pwd
        sys.argv=old_args
    return out

def curl(url:str)->str:
    #Meant to imitate the 'curl' command in linux
    #Sends a get request to the given URL and returns the result string
    import requests
    response=requests.request('GET',url)
    return response.text

def get_computer_name():
    #Returns the name of the current computer
    #https://stackoverflow.com/questions/799767/getting-name-of-windows-computer-running-python-script
    #There are apparently a few ways to do this (according to stackoverflow)
    import socket
    return socket.gethostname()

def cv_image_filter(image,kernel):
    #Convolves an image with a custom kernel matrix on a per-channel basis
    #
    #EXAMPLE:
    #   img=load_image('https://mcusercontent.com/1f7db88dcefeafdd417098188/images/78188951-5329-4a51-8808-f68231d17609.png')
    #   kernel=gaussian_kernel(40,40)
    #   kernel=resize_image(kernel,(80,5))
    #   kernel/=kernel.sum()
    #   for theta in range(180):
    #       display_image(cv_image_filter(img,rotate_image(kernel,theta)))
    #
    #Please note: I don't know if we have to ensure that the kernel 
    assert is_image(image ),'Input must be an image as defined by rp.is_image'
    assert is_image(kernel),'The kernel must also be an image as defined by rp.is_image'

    kernel=as_grayscale_image(kernel)
    kernel=as_float_image(kernel)

    if is_binary_image(kernel):
        kernel=as_byte_image(kernel)

    import cv2
    return cv2.filter2D(image,-1,kernel)

def random_rotation_matrix(dim=3):
    #Also known as a real orthonormal matrix
    #Every vector in the output matrix is orthogonal to every vector but itself
    #Every vector in the output matrix has magnitude 1
    #Source: https://stackoverflow.com/questions/38426349/how-to-create-random-orthonormal-matrix-in-python-numpy
    random_state = np.random
    H = np.eye(dim)
    D = np.ones((dim,))
    for n in range(1, dim):
        x = random_state.normal(size=(dim-n+1,))
        D[n-1] = np.sign(x[0])
        x[0] -= D[n-1]*np.sqrt((x*x).sum())
        # Householder transformation
        Hx = (np.eye(dim-n+1) - 2.*np.outer(x, x)/(x*x).sum())
        mat = np.eye(dim)
        mat[n-1:, n-1:] = Hx
        H = np.dot(H, mat)
        # Fix the last sign such that the determinant is 1
    D[-1] = (-1)**(1-(dim % 2))*D.prod()
    # Equivalent to np.dot(np.diag(D), H) but faster, apparently
    H = (D*H.T).T
    return H

def wordcloud_image(words,width=512,height=512,colormap='viridis',**kwargs):
    #EXAMPLE:
    #   display_image(wordcloud_image(get_source_code(r)))
    pip_import('wordcloud')
    
    if not isinstance(words,str):
        words='\n'.join(words)
    
    #NOTE: Two different wordcloud items might be 'Action Thriller' vs 'Action Drama', which might have two distinct colors (as opposed to three: 'Action','Thriller','Drama'        
    #If we have collocations=True, we want to randomly shuffle all of the words, otherwise we might get duplicates
    words=line_split(words)
    words=shuffled(words)
    words=line_join(words)
    
    from wordcloud import WordCloud
    #For collocations, see https://stackoverflow.com/questions/43954114/python-wordcloud-repetitve-words
    wordcloud = WordCloud(width=width,height=height,collocations=False,colormap=colormap,**kwargs)
    wordcloud.generate(words)
    return wordcloud.to_array()

def display_pandas_correlation_heatmap(dataframe,*,title=None,show_numbers=False,method='pearson',block=False):
    #This function is used for exploratory analysis with pandas dataframes. It lets you see which variables are correlated to which other variables, and by how much.
    #The dataframe argument should be a pandas.DataFrame object
    #show_numbers will, when True, show the correlation value as a number over each square in the grid. Typically, it only looks good if the squares on the grid are large (otherwise the numbers won't fit). Because of this, I turned it off by default - but if you enable it it can make your plot much more informative!
    #EXAMPLE:
    #   display_pandas_correlation_heatmap(show_numbers=True,dataframe=pip_import('pandas').read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'))
    pip_import('seaborn')
    pip_import('matplotlib')
    pip_import('pandas')
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    assert isinstance(dataframe,pd.DataFrame)

    f, ax = plt.subplots(figsize=(10, 8))
    corr = dataframe.corr(method=method)

    # Generate a custom diverging colormap
    # TODO: Possibly add an argument to change the colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(corr, square=True, ax=ax, annot=show_numbers,cmap=cmap)
    
    if title is not None:
        plt.title(title)

    update_display(block=block)

def _get_youtube_video_data_via_embeddify(url):
    #See https://pypi.org/project/embeddify/
    #Uses a specification called 'oembed', which lets us get info such as title/author etc without an api key (it's perfectly legal, and an intended use-case by google)
    #EXAMPLE:
    #     >>> _get_youtube_video_data_via_embeddify('https://www.youtube.com/watch?v=2wii8hfNkzE')
    #    ans = {'title': 'Day9] Daily #596   Rigged Games Funday Monday P1', 'width': 560, 'version': '1.0', 'type': 'video', 'height': 315, 'provider_url': 'https://www.youtube.com/', 'author_name': 'Day9TV', 'thumbnail_url': 'https://i.ytimg.com/vi/2wii8hfNkzE/hqdefault.jpg', 'author_url': 'https://www.youtube.com/user/day9tv', 'provider_name': 'YouTube', 'thumbnail_width': 480, 'thumbnail_height': 360, 'html': '<iframe width="560" height="315" src="https://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'}
    assert isinstance(url,str)
    assert is_valid_url(url)
    pip_import('embeddify')
    from embeddify import Embedder
    embedder = Embedder()
    result = embedder(url)
    return result.data
    
def get_youtube_video_title(url):
    return _get_youtube_video_data_via_embeddify(url)['title']

def view_table(data):
    #Launches a program that lets you view tabular data
    #Kinda like microsoft excel, but in a terminal
    #Can view numpy arrays
    #Can view pandas dataframes
    #Can view .csv files (given a filepath)
    #Can view .csv files (given the contents as a string)
    #Can view lists of lists such as view_table([[1,2,3],['a','b','c'],[[1,2,3],{'key':'value'},None]])
    #Can view multiline strings that look like tables, such as 'a b c\nd e f\nthings stuff things fourth thing six'


    pip_import('pandas')
    pip_import('tabview')
    import tabview
    import pandas as pd


    temp_file=temporary_file_path('csv')
    try:
        #This works for view_table([[1,2,3],[4,5,6]])
        tabview.view(data) 
    except Exception:
        #ERROR: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        if isinstance(data,str):

            if file_exists(data):
                #Perhaps the data is the path to a .csv file...
                tabview.view(data)
                return

            #If data is a string, perhaps it is the contents of some .csv file
            string_to_text_file(temp_file,data)

        else:
            dataframe=pd.DataFrame(data)
            dataframe.to_csv(temp_file,index=False)

        tabview.view(temp_file)
    finally:
        if file_exists(temp_file):
            delete_file(temp_file)

#Pseudo-terminal HISTORY files
# pterm_history_folder=path_join(get_parent_directory(__file__),'pterm_history')
# pterm_history_filename=path_join(pterm_history_folder,str(millis())+'.txt')
pterm_history_filename=path_join(get_parent_directory(__file__),'HISTORY')
_pterm_hist_file=None
def _write_to_pterm_hist(entry):
    assert isinstance(entry,str)
    global _pterm_hist_file
    if _pterm_hist_file is None:
        _pterm_hist_file = open(pterm_history_filename,'a+')
        _pterm_hist_file.write('\n\n')
        _pterm_hist_file.write('\n############################################################')
        _pterm_hist_file.write('\n########### BEGINNING OF PSEUDO TERMINAL SESSION ###########')
        _pterm_hist_file.write('\n###########%s###########'%_format_datetime(get_current_date()).center(86-48))
        _pterm_hist_file.write('\n############################################################')
    _pterm_hist_file.write('\n'+entry)
    
    
def cv_resize_image(image,size,interp='bilinear'):
    #This function is similar to r.resize_image (which uses scipy), except this uses OpenCV and is much faster
    #Valid sizes:
    #    - A single number: Will scale the entire image by that size
    #    - A tuple with integers in it: Will scale the image to those dimensions (height, width)
    #    - A tuple with None in it: A dimension with None will default to the image's dimension
    #Unlike r.resize_image, this function will not always return a floating point image. If given a byte image, the result will also be a byte image
    
    pip_import('cv2')
    import cv2  

    #Choose an interpolation method
    interp_methods={'bilinear':cv2.INTER_LINEAR,'cubic':cv2.INTER_CUBIC,'nearest':cv2.INTER_NEAREST}
    assert interp in interp_methods, 'cv_resize_image: Interp must be one of the following: %s'%str(list(interp_methods))
    interp_method=interp_methods[interp]

    assert is_image(image)
    
    if is_binary_image(image):
        #OpenCV's resize function doesn't support boolean images
        image=as_byte_image(image)

    if is_number(size):
        assert size>=0, 'Cannot resize an image by a negative factor' #Technically, I suppose this would mean flipping the image...maybe I'll implement that some other day
        height=np.ceil(get_image_height(image)*size)
        width =np.ceil(get_image_width (image)*size)
    else:
        height,width=size
        width =get_image_width(image) if width  is None else width
        height=get_image_width(image) if height is None else height
    
    height=int(height)
    width =int(width)
    
    out = cv2.resize(image,(width,height),interp_method)
    
    return out

def _iterfzf(*args,**kwargs):
    pip_import('iterfzf')
    from iterfzf import iterfzf
    return iterfzf(*args,**kwargs)

def breadth_first_path_iterator(root='.'):
    #As opposed to a depth-first path iterator, this goes through every file and directory from the root in a breadth-first manner
    #It returns a generator instead of a list, which makes computations more efficient (especially for FZF)
    #TODO: Add a depth-first path iterator
    #Original code: https://code.activestate.com/recipes/511456-breadth-first-file-iterator/
    #EXAMPLE:
    #    for path in breadth_first_path_iterator():
    #        print(path)
    import os
    dirs = [root]
    # while we has dirs to scan
    while len(dirs) :
        nextDirs = []
        for parent in dirs :
            # scan each dir
            try:
                for f in os.listdir( parent ) :
                    # if there is a dir, then save for next ittr
                    # if it  is a file then yield it (we'll return later)
                    ff = os.path.join( parent, f )
                    if os.path.isdir( ff ) :
                        yield ff
                        nextDirs.append( ff )
                    else :
                        yield ff
            except PermissionError:
                #If we encounter an error such as a PermissionError, skip the directory
                pass
        # once we've done all the current dirs then
        # we set up the next itter as the child dirs 
        # from the current itter.
        dirs = nextDirs

def gpt3(text:str):
    #Use GPT3 to write some text
    #https://deepai.org/machine-learning-model/text-generator
    import requests
    assert isinstance(text,str),'Text must be a string'
    assert len(text)>0,'Text cannot be empty'
    response = requests.post(
        #If in the future this API key no longer works, you can sign up for one -- its free. Or, if this site is broken, please replace this function with a working API.
        "https://api.deepai.org/api/text-generator",
        data={
            'text': text,
        },
        headers={'api-key': '68da3879-3ec4-4f51-905d-dd46a1a88405'}
    )
    data=response.json()
    return data['output']

def image_to_text(image)->str:
    #Takes an image, finds text on it, and returns the text as a string
    #(Optical character recognition)
    #It's kind of mind-blowing how this can be done in just 6 lines of code...
    #EXAMPLE:
    #    print(image_to_text(load_image('http)://www.morefamousquotes.com/images/topics/20170915/quotes-about-hitchhikers-guide-to-the-galaxy.jpg'))
    image=as_rgb_image(image)
    image=as_byte_image(image)
    pip_import('pytesseract')
    from pytesseract import image_to_string
    text=image_to_string(image)
    return text

def cv_equalize_histogram(image,by_value=True):
    #Equalizes the histogram of a given image
    #If by_balue is True, and image is RGB, equalize it's value in HSV space instead of applying equalization per RGB channel
    #EXAMPLE:
    #    ans=load_image('https://www.cdc.gov/healthypets/images/pets/cute-dog-headshot.jpg')
    #    ans=as_grayscale_image(ans)
    #
    #    display_image(ans)
    #    bar_graph(np.cumsum(np.histogram(ans.flatten(),256)[0]))
    #    input('Before');
    #
    #    ans=cv_equalize_histogram(ans)
    #    display_image(ans)
    #    bar_graph(np.cumsum(np.histogram(ans.flatten(),256)[0]))
    #    print('After')

    pip_import('cv2')
    import cv2
    
    assert is_image(image)
    image=as_byte_image(image)

    if is_grayscale_image(image):
        return cv2.equalizeHist(image)
    elif is_rgb_image(image):
        if by_value:
            h=get_image_hue(image)
            s=get_image_saturation(image)
            v=get_image_value(image)
            
            v=cv_equalize_histogram(v)
            v=as_float_image(v)
            
            hsv = np.stack((h,s,v),axis=2)
            rgb = hsv_to_rgb(hsv)
            
            return rgb
        else:
            r=image[:,:,0]
            g=image[:,:,1]
            b=image[:,:,2]
            r=cv_equalize_histogram(r)
            g=cv_equalize_histogram(g)
            b=cv_equalize_histogram(b)
            return np.concatenate((r,g,b),axis=2)
    else:
        #To the same thing we would for RGB, but don't change the alpha channel
        assert is_rgba_image(image)
        alpha=image[:,:,3]
        output=cv_equalize_histogram(as_rgb_image(image))
        output=np.concatenate((output,alpha),axis=2)
        return output



def compose_rgb_image(r,g,b):
    #Create an RGB image from three separate channels
    r=as_grayscale_image(r)
    g=as_grayscale_image(g)
    b=as_grayscale_image(b)
    assert is_grayscale_image(r),'Each channel must be a matrix, not a tensor'
    assert is_grayscale_image(g),'Each channel must be a matrix, not a tensor'
    assert is_grayscale_image(b),'Each channel must be a matrix, not a tensor'
    assert r.shape==g.shape==b.shape,'All channels must have the same shape'
    r=as_float_image(r)
    g=as_float_image(g)
    b=as_float_image(b)
    return np.stack((r,g,b),axis=2)

def compose_rgba_image(r,g,b,a):
    #Create an RGBA image from four separate channels
    r=as_grayscale_image(r)
    g=as_grayscale_image(g)
    b=as_grayscale_image(b)
    a=as_grayscale_image(a)
    assert is_grayscale_image(r),'Each channel must be a matrix, not a tensor'
    assert is_grayscale_image(g),'Each channel must be a matrix, not a tensor'
    assert is_grayscale_image(b),'Each channel must be a matrix, not a tensor'
    assert is_grayscale_image(a),'Each channel must be a matrix, not a tensor'
    assert r.shape==g.shape==b.shape==a.shape,'All channels must have the same shape'
    r=as_float_image(r)
    g=as_float_image(g)
    b=as_float_image(b)
    a=as_float_image(a)
    return np.stack((r,g,b,a),axis=2)

def compose_image_from_channels(*channels):
    #Create an RGB or RGBA image from three or four separate channels
    assert len(channels) in (3,4),'Cannot create an RGB or RGBA image from %i channels. We need 3 or 4 channels.'%len(channels)
    if len(channels)==3:
        return compose_rgb_image(*channels)
    else:
        return compose_rgba_image(*channels)

def extract_image_channels(image):
    #Given an RGB image of shape (height,width,3) return a tensor of (3,height,width)
    #This function is the inverse of compose_image_from_channels
    #Meant to be used like:
    #EXAMPLE:
    #   r,g,b  =extract_image_channels(image)
    #   r,g,b,a=extract_image_channels(image)
    assert is_rgb_image(image) or is_rgba_image(image)
    return np.transpose(image,(2,0,1))
extract_rgb_channels=extract_image_channels
extract_rgba_channels=extract_image_channels

def apply_image_function_per_channel(image,function):
    #Apply a grayscale funcion on every image channel individually
    assert is_image(image)
    if is_grayscale_image(image):
        return function(image)
    channels=extract_image_channels(image)
    return compose_image_from_channels(*(function(channel) for channel in channels))

pterm=pseudo_terminal#Just a shortcut. Not to be used in code; just Colab etc where I don't want to type pseudo_terminal. What?? Don't look at me like that - I'm lazy lol

#def rich_print(*args,**kwargs):
#    #This function exists because I want to be able to print fancy thing in google colab
#    #This function is 99% unnessecary lol it saves me basically one line of code...
#    return pip_import('rich').print(*args,**kwargs)

def play_the_matrix_animation():
    #Plays a super cool animation in your terminal that makes it look like you're hacking the matrix
    #(From the movie)
    #This code is from: https://github.com/gineer01/matrix-rain
    #!/usr/bin/env python3
    
    import random
    import curses
    import time
    
    # Sleep between frame after refresh so that user can see the frame. Value 0.01 or lower results in flickering because
    # the animation is too fast.
    SLEEP_BETWEEN_FRAME = 1/25#.04  # about 25 frames/s is good enough
    
    # How fast the rain should fall. In config, we change it according to screen.
    FALLING_SPEED = 2#2
    
    # The max number of falling rains. In config, we change it according to screen.
    MAX_RAIN_COUNT = 10
    
    # Color gradient for rain
    COLOR_STEP = 20
    NUMBER_OF_COLOR = 45  # The darkest color is 1000 - COLOR_STEP * NUMBER_OF_COLOR. This should be >= 0
    USE_GRADIENT = True
    START_COLOR_NUM = 128  # The starting number for color in gradient to avoid changing the first 16 basic colors
    
    # Different styles for rain head
    HEAD_STANDOUT = curses.COLOR_WHITE | curses.A_STANDOUT  # look better for small font
    HEAD_BOLD = curses.COLOR_WHITE | curses.A_BOLD  # look better for larger font

    
    # TODO This can be a namedtuple
    options = {
        'head': HEAD_BOLD,
        'speed': FALLING_SPEED,
        'count': MAX_RAIN_COUNT,
        'opening_title': " ".join("The Matrix".upper()),
        'end_title': " ".join("The Matrix. Goodbye!".upper()),
    }
    
    MAX_COLS=None
    
    # Reset the options value according to screen size
    def config(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
    
        init_colors()
    
        options['count'] = MAX_COLS // 2
        options['speed'] = 1 + curses.LINES // 25
    
    
    def init_colors():
        curses.start_color()
        nonlocal USE_GRADIENT
        USE_GRADIENT = curses.can_change_color()  # use xterm-256 if this is false
    
        if USE_GRADIENT:
            curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
            curses.init_color(curses.COLOR_BLACK, 0, 0, 0)  # make sure background is black
            for i in range(NUMBER_OF_COLOR + 1):
                green_value = (1000 - COLOR_STEP * NUMBER_OF_COLOR) + COLOR_STEP * i
                curses.init_color(START_COLOR_NUM + i, 0, green_value, 0)
                curses.init_pair(START_COLOR_NUM + i, START_COLOR_NUM + i, curses.COLOR_BLACK)
        else:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    
    def get_matrix_code_chars():
        l = [chr(i) for i in range(0x21, 0x7E)]
        # half-width katakana. See https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
        l.extend([chr(i) for i in range(0xFF66, 0xFF9D)])
        return l
    
    
    MATRIX_CODE_CHARS = get_matrix_code_chars()
    
    
    def random_char():
        return random.choice(MATRIX_CODE_CHARS)
    
    
    def random_rain_length():
        return random.randint(curses.LINES // 2, curses.LINES)
    
    
    def rain_forever(stdscr, pool):
        """
        Make rain forever by choosing a random column from pool and make rain at that column and repeat
        :param stdscr: curses's screen object
        :param pool: a list of int: a list of available columns to choose randomly from
        :return: None
        """
        while True:
            if pool:
                x = random.choice(pool)
                pool.remove(x)
            else:
                break
    
            # We want most of the rain start from 0, but some starts randomly
            begin = random.randint(-curses.LINES // 2, curses.LINES // 3)
            if begin < 0:
                begin = 0
    
            # We want most of the rain end at the bottom but some randomly end before reaching the bottom
            end = random.randint(curses.LINES // 2, 2 * curses.LINES)
            if end > curses.LINES:
                end = curses.LINES
    
            should_stop = yield from rain_once(stdscr, x, begin, end)
    
            if should_stop:
                break
            else:
                pool.append(x)
    
    
    def rain_once(stdscr, x, begin, end, last_char=None):
        """
        Make rain once at column x from line begin to line end
        :param stdscr: curses's screen object
        :param x: the column of this rain on the screen
        :param begin: the line to begin
        :param end: the line to end
        :param last_char: the last character to show
        :return: the value received from yield
        """
        max_length = random_rain_length()
        speed = random.randint(1, options['speed'])
        r = yield from animate_rain(stdscr, x, begin, end, max_length, speed, last_char)
        return r
    
    
    def animate_rain(stdscr, x, begin, end, max_length, speed=FALLING_SPEED, last_char=None):
        """
        A rain consists of 3 parts: head, body, and tail
        Head: the white leading rain drop
        Body: the fading trail
        Tail: empty space behind the rain trail
        :param stdscr: curses's screen object
        :param x: the column of this rain on the screen
        :param begin: the line to begin
        :param end: the line to end
        :param max_length: the length of this rain
        :param speed: how fast a rain should fall (the number of lines it jumps each animation frame)
        :param last_char: the last character to show
        :return: the value received from yield
        """
        head, tail = begin, begin
    
        head_style = options['head']
    
        def show_head():
            if head < end:
                stdscr.addstr(head, x, random_char(), head_style)
    
        def get_color(i):
            color_num = NUMBER_OF_COLOR - (head - i) + 1
            if color_num < 0:
                color_num = 0
            return curses.color_pair(START_COLOR_NUM + color_num)
    
        def show_body():
            if USE_GRADIENT:
                for i in range(tail, min(head, end)):
                    stdscr.addstr(i, x, random_char(), get_color(i))
            else:
                middle = head - max_length // 2
                if (middle < begin):
                    middle = begin
                for i in range(tail, min(middle, end)):
                    stdscr.addstr(i, x, random_char(), curses.color_pair(1))
                for i in range(middle, min(head, end)):
                    stdscr.addstr(i, x, random_char(), curses.color_pair(1) | curses.A_BOLD)
    
        def show_tail():
            for i in range(max(begin, tail - speed), min(tail, end)):
                stdscr.addstr(i, x, ' ', curses.color_pair(0))
    
        while tail < end:
            tail = head - max_length
            if tail < begin:
                tail = begin
            else:
                show_tail()
    
            show_body()
    
            show_head()
    
            head = head + speed
            r = yield
    
        if last_char:
            stdscr.addstr(end - 1, x, last_char, curses.color_pair(0))
    
        return r
    
    
    def update_style():
        """
        Cycle thru different styles
        :return: None
        """
        count = 0
    
        for i, s in enumerate(title):  # for each visible letter, add a rain drop
            col = x + i
            if col >= MAX_COLS:
                break
            pool.remove(col)
            if s != ' ':  # space is not visible
                rains.append(rain_once(stdscr, col, 0, y, s))
                count = count + 1
    
        for i in range(len(pool) // 3):
            rains.append(rain_forever(stdscr, pool))
    
        stdscr.clear()
        should_stop = None
        while True:
            for r in rains:
                try:
                    r.send(should_stop)
                except StopIteration:
                    rains.remove(r)
                    count = count - 1
    
            if count == 0:  # finish the title, wait for others to finish then exit
                should_stop = True
    
            ch = stdscr.getch()
            if ch != curses.ERR and ch != ord(' '):  # Use space to proceed animation if nodelay is False
                break  # exit
    
            if not rains:  # all the rains have stopped
                break
    
            time.sleep(SLEEP_BETWEEN_FRAME)
    
    
    def main(stdscr):
        # Do not use the last column due to curses limit
        # See https://docs.python.org/3/library/curses.html#curses.window.addstr
        #   Attempting to write to the lower right corner will cause an exception to be raised
        nonlocal MAX_COLS
        MAX_COLS = curses.COLS - 1
    
        stdscr.addstr(0, 0, "Press any key to start. Press any key (except SPACE) to stop.")
        stdscr.addstr(1, 0, "Press key 'h' to try a different style.")
        stdscr.addstr(curses.LINES // 3, MAX_COLS // 4, options["opening_title"])
        ch = stdscr.getch()  # Wait for user to press something before starting
        config(stdscr)
    
        rains = []
        pool = list(range(MAX_COLS))
    
        while True:
            add_rain(rains, stdscr, pool)
    
            for r in rains:
                next(r)
    
            ch = stdscr.getch()
            if ch != curses.ERR and ch != ord(' '):  # Use space to proceed animation if nodelay is False
                if ch == ord('h'):
                    update_style()
                else:
                    show_title(stdscr, curses.LINES // 2, MAX_COLS // 3, options["end_title"])
                    break  # exit
    
            time.sleep(SLEEP_BETWEEN_FRAME)
    
    
    def add_rain(rains, stdscr, pool):
        if (len(rains) < options['count']) and (len(pool) > 0):
            rains.append(rain_forever(stdscr, pool))
    
    
    curses.wrapper(main)
        
def view_string_diff(before:str,after:str):
    #This function asssumes you have git installed
    #Lets you view the diff between two strings interactively
    #TODO: Let you accept/reject changes between the diffs and return the result as a string
    
    pip_import('ydiff')
    import os,ydiff,subprocess
    
    original_dir=get_current_directory()
    temp_dir=temporary_file_path()
    make_directory(temp_dir)
    
    file_name='temp.py'
    commit_message='Changed '+file_name
    
    try:
        set_current_directory(temp_dir)
        os.system('git init')
        string_to_text_file(file_name,before)
        os.system('git add '+file_name)
        os.system('git commit -am '+repr(commit_message))
        string_to_text_file(file_name,after)
        os.system('ydiff -s '+file_name)
    finally:
        set_current_directory(original_dir)
        delete_directory(temp_dir)

def vim_string_diff(before:str,after:str):
    #Requires the program 'vimdiff'
    #Interactively diffs between two strings
    #Returns the result of the 'after' string after changes have been made
    #    (In other words, it returns the file you see on the right of the split in the vimdiff)
    #CONTROLS:
    #    def vim_string_diff(before:str,after:str):
    #    pip_import('ydiff')
    #    import os,ydiff
    #    
    #    original_dir=get_current_directory()
    #    temp_dir=temporary_file_path()
    #    make_directory(temp_dir)
    #    
    #    try:
    #        set_current_directory(temp_dir)
    #        string_to_text_file('before.py',before)
    #        string_to_text_file('after.py' ,after )
    #        os.system('vimdiff before.py after.py')
    #    finally:
    #        set_current_directory(original_dir)
    #        delete_directory(temp_dir)
    #https://vi.stackexchange.com/questions/625/how-do-i-use-vim-as-a-diff-tool
    
    import os
    original_dir=get_current_directory()
    temp_dir=temporary_file_path()
    make_directory(temp_dir)
    
    try:
        set_current_directory(temp_dir)
        string_to_text_file('before.py',before)
        string_to_text_file('after.py' ,after )
        os.system('vimdiff before.py after.py')
        return text_file_to_string('after.py')
    finally:
        set_current_directory(original_dir)
        delete_directory(temp_dir)

def vim_paste():
    #Gets the string in the 0th register of vim and returns it
    #Looking for a line like
    #    |3,1,0,1,7,0,1613593399,"Line1","Line2","Line3","Line4","Line5","Line6","Line7"
    #TODO: Make this code cleaner
    def is_valid_int(string):
        try:
            int(string)
            return True
        except Exception:
            return False
    def is_valid_line(line):
        original_line=line
        line=line.strip()
        if not line.startswith('|'):return False
        line=line[len('|'):]
        line=line.split(',')
        if not all(map(is_valid_int,line[:7])):return False
        #try:
            #get_lines(original_line) #This function includes some useful assertions
        #except AssertionError as e:
             #print_stack_trace(e)
             #print(e)
            #fansi_print('OIAJSOIDJOISDJ','red')
            #return False
        return True
    def get_lines(line):
        line=line.strip()
        line=line.split(',')
        line=line[7:]
        #stated_number_of_lines=int(line[4])
        #lines=[line[1:-1] for line in line] #"aosijd" --> aosijd
        line=','.join(line)+','
        import ast
        line=ast.literal_eval(line)
        lines=line
        #print(stated_number_of_lines)
        #assert len(lines)==stated_number_of_lines
        return lines
    def get_timestamp(line):
        #When using vim's put, it grabs the line in viminfo that has the latest timestamp
        try:
            line=line.split(',')
            timestamp=line[6]
            timestamp=int(timestamp)
            return timestamp
        except Exception:
            return 0 #By default, we'll return the worst timestamp in-case a line was formatted improperly
    viminfo=text_file_to_string('~/.viminfo')
    lines=viminfo.splitlines()
    prefix='|3,1,0,1'
    lines=[line for line in lines if line.startswith(prefix)]
    # print(lines)

    lines=[line for line in lines if is_valid_line(line)    ]
    # print(lines)
    lines=sorted(lines,key=get_timestamp,reverse=True)
    if not len(lines):
        return '' #If there is no current register 0 in ~/.viminfo, just return an empty string
    first_index=viminfo.splitlines().index(lines[0])
    vimlines=viminfo.splitlines()
    recorded_lines=[vimlines[first_index]]
    index=first_index+1
    while vimlines[index].startswith('|<'):
        recorded_lines.append(vimlines[index])
        index+=1
    def strip_braces(line):
        if line.startswith('|<'):
            line=line[2:]
        line=line[::-1]
        if line[0] in '01234567890':
            line=line[line.find('>')+1:]
        line=line[::-1]
        return line

    recorded_lines[:]=[strip_braces(line) for line in recorded_lines[:]]
    #global ans
    #ans=recorded_lines
    line=''.join(recorded_lines)
    # fansi_print(line,'green')

    return line_join(get_lines(line))


def vim_copy(string:str):
    #Gets the string in the 0th register of vim and returns it
    #Writing a line like
    #    |3,1,0,1,7,0,1613593399,"Line1","Line2","Line3","Line4","Line5","Line6","Line7"


    viminfo=text_file_to_string('~/.viminfo') if file_exists('~/.viminfo') else ''

    def get_timestamp(line):
        #When using vim's put, it grabs the line in viminfo that has the latest timestamp
        try:
            line=line.split(',')
            timestamp=line[6]
            timestamp=int(timestamp)
            return timestamp
        except Exception:
            return 0 #By default, we'll return the worst timestamp in-case a line was formatted improperly

    max_timestamp=max(get_timestamp(line) for line in viminfo.splitlines()) if viminfo.splitlines().__len__() else 0

    lines=string.splitlines()
    original_lines=string.splitlines()
    from json import dumps # Will be used instead of repr, because repr might use single quotes (we need double quotes). We use it to escape characters such as \ which might be in string
    lines=list(map(dumps,map(str,lines)))

    #new_line=','.join(['|3,1,0,1,%i,0,%i'%(len(lines),max_timestamp+1)]+lines)
    new_line='|3,1,0,1,%i,0,%i'%(len(lines),max_timestamp+1)
    if len(lines):
        #combined_lines=','.join(lines)
        combined_lines_undended='\n|<'.join([line for line in lines])
        combined_lines='\n|<'.join([(line)+(',>'+str(len(lines[i+1]))if (i<len(lines)-1) else'') for i,line in enumerate(lines)])
        #combined_lines='\n|<'.join([dumps(line)+',>'+str(len(line)+2) for index,line in enumerate(original_lines)])
        combined_lines=line_split(combined_lines)
        combined_lines_undended=line_split(combined_lines_undended)
        combined_lines[-1]=combined_lines_undended[-1]
        combined_lines=line_join(combined_lines)
        new_line+=','+combined_lines


    string_to_text_file('~/.viminfo',new_line+'\n'+viminfo)

def zip_folder_to_bytes(folder_path:str):
    #Similar to file_to_bytes
    #Takes a folder_path, zips it into a .zip file, then returns the bytes of that zip file
    assert path_exists(folder_path),'zip_folder_to_bytes error: Path does not exist: '+str(folder_path)
    assert is_a_folder(folder_path),'zip_folder_to_bytes error: Path exists but is not a folder: '+str(folder_path)
    temp_zip=temporary_file_path('.zip')
    try:
        make_zip_file_from_folder(folder_path,temp_zip)
        data=file_to_bytes(temp_zip)
    finally:
        if file_exists(temp_zip):
            delete_file(temp_zip)
    return data
    
class _BundledPath:
    #A class used internally by rp for web_copy_path and web_paste_path
    def __init__(self,is_file,data,path):
        self.is_file=is_file
        self.is_folder=not is_file
        self.data=data
        self.path=path

def web_paste_path(path=None,*,ask_to_replace=True):
    data=web_paste()
    try:
        data=bytes_to_object(data)
        assert isinstance(data,_BundledPath)
    except Exception:
        raise Exception('web_paste_path error: web_paste data was not created via web_copy_path')
    def request_replace(path)->bool:
        return input_yes_no(fansi("Replace "+get_file_name(path)+"?",'yellow'))
    if path is None and data.path=='.' and data.is_folder:
        temp_zip=temporary_file_path('.zip')
        temp_dir=temporary_file_path()
        try:
            bytes_to_file(data.data,temp_zip)
            unzip_to_folder(temp_zip,temp_dir)
            all_paths_here=get_all_paths(include_files=True,include_folders=True,relative=True)
            for new_path in get_all_paths(temp_dir,include_files=True,include_folders=True):
                if get_file_name(new_path) in all_paths_here and ask_to_replace:
                    if not request_replace(new_path):
                        continue
                move_path(path,'.')
        finally:
            if file_exists(temp_zip):
                delete_file(temp_zip)
            if folder_exists(temp_dir):
                delete_folder(temp_dir)
    else:
        if path is None:
            path=get_file_name(data.path)
        assert path is not None
        if data.is_file:
            if ask_to_replace and file_exists(path) and not request_replace(path): return
            bytes_to_file(data.data,path)
        elif data.is_folder:
            temp_zip=temporary_file_path('.zip')
            try:
                bytes_to_file(data.data,temp_zip)
                assert not is_a_file(path),'Path already exists as a file; cannot extract a zip file into it: '+path
                unzip_to_folder(temp_zip,path)
            finally:
                if file_exists(temp_zip):
                    delete_file(temp_zip)
    return path

def web_copy_path(path:str=None):
    if path is None:
        path=input_select_path(message='Select a file or folder for web_copy_path:')
        path=get_relative_path(path)
    assert path_exists(path),'Path does not exist: '+str(path)
    data=file_to_bytes(path) if is_a_file(path) else zip_folder_to_bytes(path)
    web_copy(object_to_bytes(_BundledPath(is_a_file(path),data,path)))
    return path

def get_all_local_ip_addresses():
    #Returns a list of all local ip addresses currently in use on your local network
    #Code from: https://stackoverflow.com/questions/207234/list-of-ip-addresses-hostnames-from-local-network-in-python
    #Can take up to 20 seconds to complete
    #EXAMPLE:
    #     >>> get_all_local_ip_addresses()
    #     ans = ['192.168.1.1', '192.168.1.21', '192.168.1.33', '192.168.1.32', '192.168.1.53', '192.168.1.105', '192.168.1.122', '192.168.1.136', '192.168.1.171', '192.168.1.190', '192.168.1.205', '192.168.1.235', '192.168.1.237', '192.168.1.175', '192.168.1.228', '192.168.1.249']
    #TODO: Condense this function into less lines. It's pretty big...
     
    import socket,multiprocessing,subprocess,os
    
    def pinger(job_q, results_q):
        """
        Do Ping
        :param job_q:
        :param results_q:
        :return:
        """
        DEVNULL = open(os.devnull, 'w')
        while True:
    
            ip = job_q.get()
    
            if ip is None:
                break
    
            try:
                subprocess.check_call(['ping', '-c1', ip],
                                      stdout=DEVNULL)
                results_q.put(ip)
            except Exception:
                pass
    
    
    def get_my_ip():
        """
        Find my IP address
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    
    def map_network(pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """
    
        ip_list = list()
    
        # get my IP and compose a base like 192.168.1.xxx
        ip_parts = get_my_ip().split('.')
        base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    
        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()
    
        pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]
    
        for p in pool:
            p.start()
    
        # cue hte ping processes
        for i in range(1, 255):
            jobs.put(base_ip + '{0}'.format(i))
    
        for p in pool:
            jobs.put(None)
    
        for p in pool:
            p.join()
    
        # collect he results
        while not results.empty():
            ip = results.get()
            ip_list.append(ip)
    
        return ip_list
    
    return map_network()

def ip_to_mac_address(address):
    #EXAMPLE:
    #     >>> [ip_to_mac_address(x) for x in get_all_local_ip_addresses()]
    #    ans = ['70:4d:7b:e4:c7:b8', '00:11:32:0e:90:6b', '30:5a:3a:7a:e4:a8', 'b0:83:fe:4c:d2:f8', '68:b5:99:a9:c8:a7', '8c:ae:4c:ee:66:28', '00:03:ea:0d:2c:fd', '10:ce:a9:1e:9b:c3', 'b0:a7:37:e6:af:c0']
    if address==get_my_local_ip_address():
        return get_my_mac_address()
    pip_import('getmac')
    import getmac
    return getmac.get_mac_address(ip=address)

def ip_to_host_name(address:str)->str:
    #Will attempt to get the name of the host computer with the given IP address
    #If no name is returned, this function returns None
    #EXAMPLE:
    #    >>> get_my_local_ip_address()
    #   ans = 192.168.1.33
    #    >>> ip_to_host_name(ans)
    #   ans = glass
    import socket
    try:
        out=socket.gethostbyaddr(address)
        return out[0]
    except socket.herror:
        return None

def get_mac_address_vendor(address:str)->str:
    #EXAMPLE:
    #    >>> get_my_mac_address()
    #   ans = 30:5a:3a:7a:e4:a8
    #    >>> get_mac_address_vendor(ans)
    #   ans = ASUSTek COMPUTER INC.
    pip_import('mac_vendor_lookup')
    from mac_vendor_lookup import MacLookup
    return MacLookup().lookup(address)

try:
    # import numpy as np
    def autoimportable_module(module_name):
        class LazyloadedModule(type(rp)):
            def __getattribute__(self,key):
                return getattr(pip_import(module_name),key)
        return LazyloadedModule(module_name)
    np=autoimportable_module('numpy')
    icecream=autoimportable_module('icecream')
except:
    print("Warning: Cannot import numpy. Please excuse any 'np is None' errors, or try rp.pip_install('numpy')")

def import_all_submodules(module,*,recursive=True,strict=False,verbose=False):
    #Useful when you're searching for some keyword in a library, but not every submodule has been imported
    #Background: Modules sometimes don't import everything all at once. When you import PIL, for example, PIL.Image doesn't exist until you use 'import PIL.image'
    #   This makes it impossible to search for a function, such as 'imsave' using autocompletion or rp's rinsp_search (aka the ?. operator).
    #If recursive is True, it will import all of the submodule's submodules etc
    #If strict is True, it will throw an error if any of the modules fail to import properly
    #If verbose is True, it will print out each module as it's imported (or failed to import)
    #The 'module' parameter can either be a string, or a python module
    #EXAMPLE: import_all_submodules('sklearn',verbose=True)
        
    assert is_a_module(module) or isinstance(module,str),'import_all_submodules: the "module" parameter should be either a string or a module, but got type '+repr(type(module))
    if isinstance(module,str):
        assert module_exists(module),'Module doesn\'t exist: '+repr(module)
        
    seen_modules=set()
    
    @memoized
    def try_import(module_name):
        try:
            from importlib import import_module
            output = import_module(module_name)
            seen_modules.add(output)
            if verbose:
                module_info=module_name.ljust(20)+'\t    '+fansi(get_module_path(output),'green')
                fansi_print('Imported: '+module_info,'green','bold')
            return output
        except ModuleNotFoundError:
            #If get_all_submodule_names returned a module that can't be imported, just ignore it
            pass
        except KeyboardInterrupt:
            #Let us cancel this via a keyboard interrupt, but don't let mischevious modules that call sys.exit() hinder this function
            raise
        except BaseException:
            if strict:
                #When strict is True, we want to make sure that none of the modules throw exceptions upon importing them
                raise
        if verbose:
            fansi_print('Not imported: '+module_name,'red','bold')
        
    if isinstance(module,str):
        module=__import__(module)

    def helper(module):
            
        if module in seen_modules or module is None:
            return
        
        for submodule_name in get_all_submodule_names(module):
            submodule=try_import(submodule_name)
            if recursive:
                helper(submodule)
    
    helper(module)
    return seen_modules-{None}
        
def dns_lookup(url:str)->str:
    #Takes a url, and returns a string with the ip that's found
    #EXAMPLE:
    #     >> dns_lookup('google.com')
    #    ans = 172.217.3.110
    assert connected_to_internet(),'Cannot use dns_lookup because we are not connected to the internet'
    import socket
    return socket.gethostbyname(url)

def unwarped_perspective_image(image, from_points, to_points=None, height:int=None, width:int=None):
    #Takes an image, and two corresponding lists of four points, and returns an unwarped image
    #If you don't specify the to_points, it will simply unwarp the source quadrangle to the resolution of the input image
    #If you specify to_points, it might be useful in-case you want to adjust the transform etc
    #Height and width can be manually specified as well, in case you want to capture parts of the perspectie transform that might have been cropped out
    #When to_points is not specified, we assume that the from_points start from the top left of the desired area, and progress clockwise
    #
    #EXAMPLE:
    #    while True:
    #        #Place the apriltags clockwise from 0 at the the topleft on your target area then run this program and look at them through your webcam
    #        image=load_image_from_webcam()
    #        tags={}
    #        for tag in detect_apriltags(image):
    #            tags[tag.id_number]=tag
    #            
    #        print("Detected apriltags:",sorted(tags))
    #        
    #        corners=[]
    #        for id_number in [0,1,2,3]:
    #            if id_number in tags:
    #                corners.append(tags[id_number].center)
    #        print(corners)
    #        
    #        if len(corners)>=4:
    #            display_clear()
    #            display_path(corners)
    #            image=unwarped_perspective_image(image,corners)
    #        
    #        display_image(image)    

    pip_import('cv2')
    import cv2
    
    image=as_rgb_image (image)
    image=as_byte_image(image)
    
    if width  is None:width =get_image_width (image)
    if height is None:height=get_image_height(image)
    
    if to_points is None:to_points=[[0,0],[width,0],[width,height],[0,height]]
    from_points=as_points_array(from_points).astype(np.float32)
    to_points  =as_points_array(to_points  ).astype(np.float32)
    assert len(from_points)==4,'unwarped_perspective_image needs four from_points, but got '+str(len(from_points))
    assert len(to_points  )==4,'unwarped_perspective_image needs four to_points, but got '  +str(len(to_points  ))

    #SOURCE: https://stackoverflow.com/questions/22656698/perspective-correction-in-opencv-using-python
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(from_points, to_points)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(image, M, (width, height), flags=cv2.INTER_LINEAR)
    return warped

@memoized
def _get_apriltag_detector(**kwargs):
    assert not currently_running_windows(),'The "apriltag" library doesnt currently work on Windows, sorry :( Try using Unix'
    pip_import('apriltag')
    import apriltag
    options = apriltag.DetectorOptions(**kwargs)
    detector = apriltag.Detector(options)
    return detector
class AprilTag:
    def __init__(self,corners,id_number:int,family:str):
        self.corners  =as_points_array(corners  )
        self.id_number=int            (id_number)
        self.family   =str            (family   )
    def __hash__(self):
        return hash(self.id_nubmer,tuple(map(tuple,self.corners)))
    def __eq__(self,x):
        return isinstance(x,AprilTag) and hash(self)==hash(x)
    @property
    def center(self):
        return np.mean(self.corners,axis=0)
    def __repr__(self):
        return 'AprilTag(corners=%s, id_number=%i, family=%s)'%(repr(self.corners.tolist()),self.id_number,self.family)
        
def detect_apriltags(image,family:str='tag36h11'):
    #Apriltags are a particular type of AR Marker, which looks like a QR Code
    #Apriltags are lower resolution than normal QR codes though
    #Each apriltag corresponds to a single number
    #Some apriltags to print out: https://www.dotproduct3d.com/uploads/8/5/1/1/85115558/apriltags_0-99.pdf
    #To test out a whole bunch at one time, try printing this out: https://dfimg.dfrobot.com/nobody/makelog/4cd2b76a8912dfe060413b7dece0dfdf.png
    #The apriltag's corners are specified clockwise from the top left corner of the apriltag
    #
    #EXAMPLE: (Try waving some of these apriltags around your webcam after printing them out)
    #    while True:
    #        image=load_image_from_webcam()
    #        results=detect_apriltags(image)
    #        print("[INFO] {} total AprilTags detected".format(len(results)))
    #        
    #        for r in results:
    #            # extract the bounding box (x, y)-coordinates for the AprilTag
    #            # and convert each of the (x, y)-coordinate pairs to integers
    #            import cv2
    #            (ptA, ptB, ptC, ptD) = r.corners
    #            ptB = (int(ptB[0]), int(ptB[1]))
    #            ptC = (int(ptC[0]), int(ptC[1]))
    #            ptD = (int(ptD[0]), int(ptD[1]))
    #            ptA = (int(ptA[0]), int(ptA[1]))
    #    
    #            # draw the bounding box of the AprilTag detection
    #            cv2.line(image, ptA, ptB, (0, 255, 0), 2)
    #            cv2.line(image, ptB, ptC, (0, 255, 0), 2)
    #            cv2.line(image, ptC, ptD, (0, 255, 0), 2)
    #            cv2.line(image, ptD, ptA, (0, 255, 0), 2)
    #    
    #            # draw the center (x, y)-coordinates of the AprilTag
    #            (cX, cY) = (int(r.center[0]), int(r.center[1]))
    #            cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
    #    
    #            # draw the tag family on the image
    #            tagFamily = r.family
    #            tagFamily = str(r.id_number)
    #            cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #            
    #            #Unwarp the image using the apriltag:
    #            #image=unwarped_perspective_image(image,r.corners)
    #    
    #        display_image(image)

    family=family.lower()    
    supported_families='tag25h9 tag36h11 tagCircle21h7 tagCircle49h12 tagCustom48h12 tagStandard41h12 tagStandard52h13'.split()
    assert family in supported_families,'detect_apriltags only supports the following apriltag families'+str(supported_families)
    
    image=as_grayscale_image(image)
    image=as_byte_image(image)
    
    results = _get_apriltag_detector(families=family).detect(image)
    results = [AprilTag(result.corners,result.tag_id,result.tag_family.decode("utf-8")) for result in results]
    return results

def _display_filetype_size_histogram(root='.'):
    assert is_a_folder(root)

    paths=get_all_paths(root,recursive=True,ignore_permission_errors=True,include_files=True,include_folders=False)

    paths=[path for path in paths if not is_symbolic_link(path)] #Don't include symlinks in the overall count for file sizes

    filetypes=set(get_file_extension(file) for file in paths)
    mem_hist={filetype:sum(get_file_size(file,human_readable=False) for file in paths if get_file_extension(file)==filetype) for filetype in filetypes}
        
    entries=[]
    for filetype in sorted(set(mem_hist),key=mem_hist.get):
        mem_percent=mem_hist[filetype]/sum(mem_hist.values())
        mem_percent*=100
        entries.append((filetype,'    ',human_readable_file_size(mem_hist[filetype]),'   %10.5f%%'%mem_percent))

    ans=horizontally_concatenated_strings(list(map(line_join,zip(*entries))),rectangularize=True)
        

    printed_lines=[]
    printed_lines.append(ans)
    printed_lines.append('')
    printed_lines.append('Root: '+get_current_directory())
    printed_lines.append('Total Size: '+human_readable_file_size(sum(mem_hist.values())))
    printed_lines=line_join(printed_lines)

    _maybe_display_string_in_pager(printed_lines)
    print(printed_lines)

def _clear_jupyter_notebook_outputs(path:str=None):
    #This clears all outputs of a jupyter notebook file
    #This is useful when the file gets so large it crashes the web browser (storing too many images in it etc)
    #Source: https://stackoverflow.com/questions/28908319/how-to-clear-an-ipython-notebooks-output-in-all-cells-from-the-linux-terminal
    if path is None:
        path=input_select_file(file_extension_filter='ipynb')
    path=get_absolute_path(path)

    assert get_file_extension(path)=='ipynb','clear_jupyter_notebook_outputs: You must select a .ipynb file'

    if input_yes_no('Are you sure you want to clear the outputs of '+path+'?'):
        pip_import('jupyter')
        command=sys.executable+' -m jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output '+path
        print('Original file size:',get_file_size(path))
        shell_command(command)
        print('New file size:',get_file_size(path))

    return path

def get_git_remote_url(repo='.'):
    assert folder_exists(repo)
    pip_import('git')
    import git
    ans=git.Remote.urls
    ans=git.Repo(repo)
    ans=ans.remotes
    ans=ans[0]
    ans=ans.urls
    ans=list(ans)
    ans=ans[0]
    return ans

def is_a_git_repo(folder='.'):
    if not is_a_folder(folder):
        return False
    pip_import('git')
    import git
    try:
        _ = git.Repo(folder).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

def git_clone(url,path=None):
    def get_repo_name_from_url(url):
        #Url should look like: https://github.com/gabrielloye/RNN-walkthrough/
        assert is_valid_url(url)
        url=url.strip()
        if url.endswith('/'):
            url=url[:-1]
        url=url.split('/')
        url=url[-1]
        return url
    if path is None:
        path=get_repo_name_from_url(url)
        path=get_absolute_path(path)
    pip_import('git')
    import git
    git.Repo.clone_from(url,path)
    return path

try:from icecream import ic#This is a nice library...I reccomend it for debugging. It's really simple to use, too. EXAMPLE: a=1;b=2;ic(a,b)
except Exception:pass

def _autoformat_python_code_via_black(code:str):
    pip_import('black')
    import black
    return black.format_str(code,mode=black.Mode())

def _is_numpy_array(x):
    try:
        import numpy
        return isinstance(x,numpy.ndarray)
    except Exception:
        return False

def _is_torch_tensor(x):
    try:
        import torch
        return isinstance(x,torch.Tensor)
    except Exception:
        return False

def as_numpy_images(images):
    if _is_numpy_array(images):
        return images.copy()
    elif _is_torch_tensor(images):
        import torch
        assert isinstance(images,torch.Tensor)
        assert len(images.shape)==4,'Should be 4d tensor: (batch size, num channels, height, width)'
        images=as_numpy_array(images)
        images=images.transpose(0,2,3,1)
        return images   
    else:
        raise TypeError('Unsupported image datatype: %s'%type(images))
    
def as_torch_images(images):
    if _is_numpy_array(images) or all(is_image(x) for x in images):
        assert len(images.shape)!=3,'Grayscale images are not yet supported'
        images=images.transpose(0,3,1,2)
        import torch
        images=torch.Tensor(images)
        return images
    elif _is_torch_tensor(images):
        #Not creating a copy. GPU tensors are expensive.
        return images
    else:
        raise TypeError('Unsupported image datatype: %s'%type(images))

if __name__ == "__main__":
    print(end='\r')
    _pterm()

del re

#TODO: Fix this. It can help extract function defs among other useful thins
#    def semantic_lines(python_code:str)->list:
#	#Gets every semantic python line.
#	#Meaning, literals that take up more than one line will be treated as one line (aka multiline strings, multiline defs, multiline lists etc)
#	tokens=split_python_tokens(python_code)#This fraks up because split_python_tokens is broken -- it sees '"hello"' as 3 tokens: ['"','hello','"']
#	output=[]
#	stack =[]
#	current_line=''
#	closes={'}':'{',')':'(',']':'['}
#	opens ={'{','(','['}
#	for token in tokens:
#	    current_line+=token
#	    if token in opens:
#		stack.append(token)
#	    elif token in closes and stack and stack[-1] == closes[token]:
#		stack.pop()
#	    elif token=='\n' and not stack:
#		output.append(current_line)
#		current_line=''
#	if current_line:
#	    output.append(current_line)
#	return output



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
#     default_args=f.
#     args=[args]








