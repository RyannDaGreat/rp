from __future__ import unicode_literals

from rp.prompt_toolkit.completion import Completer, Completion
from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.contrib.completers import PathCompleter
from rp.prompt_toolkit.contrib.regular_languages.compiler import compile as compile_grammar
from rp.prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter

from rp.rp_ptpython.utils import get_jedi_script_from_document
# from rp import printed,fansi_print
import re

__all__ = (
    'PythonCompleter',
)
non_completable_keywords={'class','finally','is','return','continue','for','lambda','try','def','from','nonlocal','while','and','del','global','not','with','as','elif','if','or','yield','assert','else','import','pass','break','except','in','raise'}

import sys
_all_module_names=set(sys.builtin_module_names)
def get_all_importable_module_names():
    #Returns a set of all names that you can use 'import <name>' on
    import pkgutil
    if _all_module_names:
        def update_thread():
            #Every time we call this fuction, make a new thread that will update the _all_module_names for us (without blocking)
            #That way we can respond to new packages being added, or changes in directory etc without having to block completions for them
            for _,name,_ in pkgutil.iter_modules():
                _all_module_names.add(name)
        from threading import Thread
        Thread(target=update_thread).start()
        return _all_module_names
    for _,name,_ in pkgutil.iter_modules():
        _all_module_names.add(name)
    return _all_module_names

from threading import Thread
Thread(target=get_all_importable_module_names).start()
Thread(target=lambda: __import__('rp').r._get_cached_system_commands).start()


MAX_SORTING_PRIORITY=999999999
sorting_priorities={}
    

_get_apt_completions_cache=None
def get_apt_completions():
    #Gets all installable apt packages. Perhaps migrate this to rp?
    global _get_apt_completions_cache
    if _get_apt_completions_cache is not None:
        return _get_apt_completions_cache.copy()
    else:
        import subprocess
        # Update package lists with 'sudo apt update'
        # subprocess.run(['sudo', 'apt', 'update'], stdout=subprocess.PIPE)
        
        try:
            # Get the list of all available packages
            result = subprocess.run(['apt-cache', 'dumpavail'], stdout=subprocess.PIPE, text=True)
            
            # Decode the byte string into a string, split by newline
            package_list = result.stdout.split('\n')
            
            # Extract package names
            packages = set()
            for line in package_list:
                if line.startswith('Package: '):
                    package_name = line.split(' ')[1]
                    packages.add(package_name)
            
            _get_apt_completions_cache= packages
        except Exception:
            _get_apt_completions_cache=[]

        return _get_apt_completions_cache

class PythonCompleter(Completer):
    """
    Completer for Python code.
    """
    def __init__(self, get_globals, get_locals):
        super(PythonCompleter, self).__init__()

        self.get_globals = get_globals
        self.get_locals = get_locals

        self._path_completer_cache = None
        self._path_completer_grammar_cache = None

    @property
    def _path_completer(self):
        if self._path_completer_cache is None:
            self._path_completer_cache = GrammarCompleter(
                self._path_completer_grammar, {
                    'var1': PathCompleter(expanduser=True),
                    'var2': PathCompleter(expanduser=True),
                })
        return self._path_completer_cache

    @property
    def _path_completer_grammar(self):
        """
        Return the grammar for matching paths inside strings inside Python
        code.
        """
        # We make this lazy, because it delays startup time a little bit.
        # This way, the grammar is build during the first completion.
        if self._path_completer_grammar_cache is None:
            self._path_completer_grammar_cache = self._create_path_completer_grammar()
        return self._path_completer_grammar_cache

    def _create_path_completer_grammar(self):
        def unwrapper(text):
            return re.sub(r'\\(.)', r'\1', text)

        def single_quoted_wrapper(text):
            return text.replace('\\', '\\\\').replace("'", "\\'")

        def double_quoted_wrapper(text):
            return text.replace('\\', '\\\\').replace('"', '\\"')

        grammar = r"""
                # Text before the current string.
                (
                    [^'"#]                                  |  # Not quoted characters.
                    '''  ([^'\\]|'(?!')|''(?!')|\\.])*  ''' |  # Inside single quoted triple strings
                    "" " ([^"\\]|"(?!")|""(?!^)|\\.])* "" " |  # Inside double quoted triple strings

                    \#[^\n]*(\n|$)           |  # Comment.
                    "(?!"") ([^"\\]|\\.)*"   |  # Inside double quoted strings.
                    '(?!'') ([^'\\]|\\.)*'      # Inside single quoted strings.

                        # Warning: The negative lookahead in the above two
                        #          statements is important. If we drop that,
                        #          then the regex will try to interpret every
                        #          triple quoted string also as a single quoted
                        #          string, making this exponentially expensive to
                        #          execute!
                )*
                # The current string that we're completing.
                (
                    ' (?P<var1>([^\n'\\]|\\.)*) |  # Inside a single quoted string.
                    " (?P<var2>([^\n"\\]|\\.)*)    # Inside a double quoted string.
                )
        """

        return compile_grammar(
            grammar,
            escape_funcs={
                'var1': single_quoted_wrapper,
                'var2': double_quoted_wrapper,
            },
            unescape_funcs={
                'var1': unwrapper,
                'var2': unwrapper,
            })

    def _complete_path_while_typing(self, document):
        char_before_cursor = document.char_before_cursor
        return document.text and (
            char_before_cursor.isalnum() or char_before_cursor in '/.~')

    def _complete_python_while_typing(self, document):
        char_before_cursor = document.char_before_cursor
        return document.text and (
            char_before_cursor.isalnum() or char_before_cursor in '_.')

    def _get_completions(self, document, complete_event,force=False):# When force is true it acts like the original ptpython autocomplete
      sorting_priorities.clear()
      import warnings
      with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        force=True
        global old_origin,candidates
        origin=document.get_word_before_cursor()

        def yield_from_candidates(candidates:list,priority=None,displays=None):
            candidates=list(candidates)
            if priority is None:
                priority=[MAX_SORTING_PRIORITY]*len(candidates)
            if displays is None:
                displays=candidates
            for c,p,d in zip(candidates,priority,displays):
                #TODO: RIGHT NOW displays IS IGNORED BY get_completions WHICH USES THIS FUNCTION. ANNOYING!
                completion=Completion(text=c,start_position=-len(origin),display=d);
                sorting_priorities[c]=p
                # print(c,p)
                yield completion
        import rp.r_iterm_comm as ric
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        after=document.text_after_cursor
        before=document.text_before_cursor


        import re
        from rp import ring_terminal_bell
        # ring_terminal_bell()
        if re.fullmatch(r' *(from|import) +\w*',before_line):
            #Speed up 'import ___|' completions. Note that this is going to skip modules that have been pip_installed during runtime, but this is a small price to pay for this kind of crazy fast autocompletion speed.
            #This kinda completion is particularly useful because the spacebar triggers the autocpmpletion of module names like tab does
            yield from yield_from_candidates(get_all_importable_module_names())
            return
        # if re.fullmatch(r'.*[^\w\.]',before_line):
        #     yield from yield_from_candidates(list(ric.globa))
        #     # from rp import play_tone
        #     # play_tone(880,seconds=.03)  
        #     return
        if not '\n' in document.text and re.fullmatch(r' *((if|with|while|assert|yield|yield from|elif) )? *\w*',before_line):
            # ring_terminal_bell()
            yield from yield_from_candidates(list(ric.globa))
            return
        blr=before_line[::-1]#blr=before_line reversed
        if '.' in blr:#This is a hack to make completions to namespaces like np.* not need to use jedi (which takes about 1 second to make a script which is super slow). This is a hack but it makes completions that would otherwise have to use jedi over 20x faster.
            found=re.match(r'(\.\w*[a-zA-Z_])+',blr[blr.find('.'):])
            if not found:
                pass#Something went wrong whatever
            elif found.string:
                found=found.string
                assert found,'wat? found='+repr(found.match)
                prefix=found[1:][::-1]
                try:
                    def keys(root):
                        out=set()
                        try:out.update(dir(root))
                        except:pass
                        try:out.update(root.__dict__)
                        except:pass
                        return sorted(out)
                    def evall():
                        parts=prefix.split('.')
                        cursor=ric.globa[parts[0]]
                        for part in parts[1:]:
                            cursor=getattr(cursor,part)
                        return cursor
                    yield from yield_from_candidates(keys(evall()))
                    # yield from yield_from_candidates(keys(eval(prefix,ric.globa)))
                    # from rp import play_tone
                    # play_tone(seconds=.03)
                    # print("HI"+repr(prefix)+"BYE")
                    return
                except Exception as E:
                    # from rp import print_stack_trace
                    # print_stack_trace(E)
                    #This type of error is perfectly normal and is to be expected.
                    #  ⮤ adsfpor.print_stack_trace: ERROR: Traceback (most recent call last):
                    #   File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/rp/rp_ptpython/completer.py", line 136, in _get_completions                                                                                     
                    #     yield from yield_from_candidates(keys(eval(prefix,ric.globa)))                                  
                    #   File "<string>", line 1, in <module>                                                              
                    # NameError: name 'adsfpo' is not defined  
                    pass#Oh well whatevs we'll do it with jedi, it will just be a bit slower

        import re
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        after=document.text_after_cursor
        before=document.text_before_cursor
        in_global_or_nonlocal_declaration=(re.fullmatch(r'\s*(del|global|nonlocal)\s+[\w\s\,]*',before_line))
        # if in_global_or_nonlocal_declaration:
        #     print("GOOGOO")
            #Make @memoized complete faster:
            #If we set the mode to 'fast' instead of 'good':
            #after 'if |' or 'while |' etc, you might want to use fast autocompletions instead of good autocompletions, because I can't think of a situation where it would miss any completions (though it might rip some out of strings and comments). This gives a speed boost.
        # if re.fullmatch(r'\s*def\s+\w+\s*\((\s*\w+\s*(\=\s*[^\s].*)?\s*\,\s*)*\w*',before_line) and after_line.strip()=='):':
        #     return#Don't autocomplete function paramater names

        from rp import starts_with_any

        def pathmod(entry):
            if isinstance(entry,str):
                if path_before_cursor is not None:
                    #For completing CD and TAKE etc
                    entry=entry[len(path_before_cursor):]
                elif entry.startswith('./'): 
                    #For completing in strings primarily
                    #This is just bloat
                    entry =entry[len('./'):]
                return entry
            out = entry.path
            if entry.is_dir():
                out+='/'
            assert isinstance(out,str)
            return pathmod(out)

        def pathsmod(entries,priority=lambda x:MAX_SORTING_PRIORITY):
            mods=[]
            pris=[]
            for x in entries:
                mods.append(pathmod(x))
                pris.append(priority(x))
            return mods,pris

        path_before_cursor=None
        def get_path_before_cursor():
            nonlocal path_before_cursor #Cache this

            #Assume we're like 'TAKE /path'  or  'CAT ./path' etc - we have a space after the first word
            assert ' ' in before_line
            first_word=before_line.split()[0]
            line=before_line
            line=line[len(first_word):]
            line=line.lstrip()
            if not line:
                path= '.'
            elif line.endswith('/'):
                path= line
            elif '/' in line:
                path= '/'.join(line.split('/')[:-1])
            else:
                path= line

            import rp
            if rp.path_exists(path):
                path_before_cursor = path
            else:
                #Don't crash, hack here. No reason to return '.', really, other than that. Cant pass bad path to scandir.
                path_before_cursor = '.'

            return path_before_cursor


                
        if starts_with_any(before_line,'CDH ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            import rp

            updirs = rp.r._get_cdh_back_names()
                
            # yield from yield_from_candidates(updirs)
            yield from yield_from_candidates(updirs,displays=updirs,priority=list(range(len(updirs))))
            return 
        if starts_with_any(before_line,'CD ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import rp
            import os
            from rp import is_a_directory
            yield from yield_from_candidates(*pathsmod(x for x in os.scandir(get_path_before_cursor()) if x.is_dir()))
            return 
        if starts_with_any(before_line,'TAKE ','MKDIR ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            from rp import is_a_directory
            yield from yield_from_candidates(*pathsmod(os.scandir(get_path_before_cursor()), priority= lambda x:not x.is_dir()))
            return 
        if starts_with_any(before_line,'PYM ','APYM ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            def get_module_names():
                import pkgutil
                for _, module_name, _ in pkgutil.iter_modules():
                    yield module_name
            yield from yield_from_candidates(get_module_names())
            return 
        if starts_with_any(before_line,'CDU ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            import rp

            pwd=rp.get_current_directory()
            cwd=pwd
            displays=[]
            updirs=[]
            priorities=[]
            for _ in range(len(rp.path_split(pwd))):
                cwd=rp.get_parent_directory(cwd)
                if rp.get_folder_name(cwd):
                    priorities.append(-len(cwd))
                    upname=rp.get_folder_name(cwd)
                    displays.append(upname)
                    updirs.append(upname)
                    # updirs.append('/'+cwd)

                
            yield from yield_from_candidates(updirs,displays=displays,priority=priorities)
            return 
        if starts_with_any(before_line,'RN ','RM ','VIM ','OPEN ','FD ','WANS ','MV ','PIP ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            yield from yield_from_candidates(*pathsmod(os.scandir(get_path_before_cursor())))
            return 
        if re.fullmatch(r'(CAT |NCAT |CCAT |OPEN |ACAT |TAB |RUN |PY |APY |PYM |APYM |LSS |LSR ).*',before) and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            from rp import is_a_file
            import rp
            yield from yield_from_candidates(*pathsmod(os.scandir(get_path_before_cursor()), priority= lambda x: x.is_dir())) #Put directories last but do include them
            return 
        if re.fullmatch(r'.*\`\w*',before_line)\
            or (before_line.startswith('RUN ') and not ('\n' in before) and not after):#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            yield from yield_from_candidates([x for x in os.listdir() if any(x.endswith(e) for e in '.py .rpy'.split())])
            return 
        if (before_line.startswith('!') or before_line.startswith('ARG ')) and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
            import os
            bls=before_line.split()
            if before_line.startswith('!sudo apt install'):
                yield from yield_from_candidates(get_apt_completions())
                return
            if before_line.startswith("!") and not (
                    before_line[1:].startswith("/") or before_line[1:].startswith(".")
                ) and (
                    len(bls) == 1
                    and (before_line.strip() == before_line or bls[0]=='!sudo')
                    or len(bls) == 2
                    and bls[0] == "!sudo"
                    and (not bls[1].startswith(".") or bls[1].startswith("/"))
                    and before_line==before_line.strip()
                ):
                    import rp
                    yield from yield_from_candidates(rp.r._get_cached_system_commands())
            else:
                yield from yield_from_candidates([x for x in os.listdir()])
            return 

        import re

        # if re.fullmatch(r'(.*\W)?',before_line)


        if  in_global_or_nonlocal_declaration     or\
            (not after and re.fullmatch(r'\@\w*',before_line)) or\
            (re.fullmatch(r'\s*(if|while|(for\s+(\w\s\,)+\s+in)|assert|with|return|yield|(yield from)|elif|)\s+\w*',before_line)) or \
            (ric.completion_style and ric.completion_style[0]=='fast'): #fast but bad completion mode
            tokens=re.findall(r'[a-zA-Z_]\w*',document.text)#all possible tokens in the current buffer
            yield from yield_from_candidates((set(tokens)|set(ric.globa))-non_completable_keywords)
            return


        ##################### JEDI SECTION. THIS IS A SLOW AREA  ##############

        # ric.current_candidates.clear()
        # if not origin:
        #     return
        if old_origin not in origin or force:# Make things faster when we're just adding on to a previous autocomplete thing by reusing our previous autocomplete data

            """
            Get Python completions.
            """
            # Do Path completions
            if complete_event.completion_requested or self._complete_path_while_typing(document):
                for c in self._path_completer.get_completions(document, complete_event):
                    # ric.current_candidates.append(c)
                    yield c

            # If we are inside a string, Don't do Jedi completion.
            import rp
            if self._path_completer_grammar.match(document.text_before_cursor):
                rp.r_iterm_comm.writing_in_string=True
                return
            rp.r_iterm_comm.writing_in_string=False

            # Do Jedi Python completions.
            if complete_event.completion_requested or self._complete_python_while_typing(document):
                
                cursor_position=document.cursor_position

                if not '/' in origin:
                    #If we're completing a path, don't modify this.
                    #Otherwise, please grab as many completions as we can so we can efficiently backtrack through them
                    cursor_position-=(origin[::-1].find(".") if "." in origin else len(origin))   #NOT SURE WHAT THIS WAS FOR (april 19 2024) --- Disabling it seems to do nothing?? OH wait...I think I know what this is for...its to make sure we get ALL the completions so our code can handle getting subsets faster. Re-enabling.

                doc = Document(
                    document.text,
                    cursor_position,
                    document.selection,
                )

                script = get_jedi_script_from_document(doc, self.get_locals(), self.get_globals())
                # print(script)
                pos=document.cursor_position-len(origin)+1
                if script and not isinstance(script,Exception):
                    try:completions = script.completions()
                    except Exception as e:
                        import rp
                        # rp.print_verbose_stack_trace(e)
                        pass#The original ptpython has a whole string of specific error types, and it looks like visual clutter. I got rid of it to see my code more easily. I dont think im missing much.
                    else:
                        # fff=1
                        for c in completions:
                            # if fff:
                                # from rp import ring_terminal_bell
                                # ring_terminal_bell()
                                # fff=0
                            thingy=Completion(c.name_with_symbols, len(c.complete) - len(c.name_with_symbols),display=c.name_with_symbols)
                            yield thingy
                        # else:
                            # from rp import ring_terminal_bell
                        return
                        candidates={c.name_with_symbols for c in completions}
                else:
                    def update_parso_grammars():
                        #Get all the latest grammar files but don't update parso as a whole
                        #This will make rp's autocomplete features happy
                        import rp
                        old_dir=rp.get_current_directory()
                        rp.set_current_directory(rp.get_parent_directory(rp.get_module_path_from_name('rp.libs.parso.python')))
                        ans=['https://raw.githubusercontent.com/davidhalter/parso/master/parso/python/grammar%s.txt'%v for v in '38 39 310 311 312 313 314 315 316 317 318 319 320'.split()]
                        for x in ans:
                            import os
                            os.system('wget -N '+x)
                        print('\n\nSaved some new files to %s'%rp.get_current_directory())
                        rp.set_current_directory(old_dir)
                        print('\n\n\n'+'Done! You may continue using rp without this error (hopefully).')
                        
                    print("ATTENTION: Please update the parso definitions! This message came from %s, and script="%__file__+repr(script))
                    if rp.input_yes_no("rp's autocomplete functionality is broken because it doesn't recognize this version of Python's grammar. Is it ok if we try and fix this by downloading some up-to-date files from https://github.com/davidhalter/parso?"):
                        update_parso_grammars()
                    else:
                        print("OK...I'm assuming you said NO because you tried this and it didn't fix the problem, so here's a big stack trace to help you debug it. If this is annoying you could comment it out in %s, but note that autocomplete won't work fully if you do that. Here's the stack trace:"%__file__)
                        if True: #Set this to False to disable the stack trace during errors
                            import rp
                            if isinstance(script,Exception):
                                rp.print_verbose_stack_trace(script)
                            print('doc='+str(doc),'\n\nscript='+repr(script),len(self.get_locals()))
                candidates=set(candidates)
                # if not force:
                #     candidates|=set(self.get_globals())|set(self.get_locals())# The namespace we search for completions in
        candidates =ryan_completion_matches(origin,tuple(candidates))    # Now its a list, and we've ordered our search.
        for c in candidates:
            # ric.current_candidates.append(c);
            yield Completion(text=c,start_position=-len(origin),display=c);
        else:
            from rp import is_namespaceable
            if not force and (not is_namespaceable(origin) or not origin):
                for x in self.get_completions(Document(document.text,document.cursor_position-len(origin)+(1 and len(origin)),),complete_event,force=True):
                    # ric.current_candidates.append(x);
                    yield x;# For when we want autocompletins for 'np.' or 'rinsp.' or 'rp.' etc, as opposed to 'pr' to print or 'lis' to list
        # if not force and not ric.current_candidates or origin not in old_origin and origin!=old_origin:old_origin=origin;return self.get_completions(document, complete_event,force=True)

        old_origin=origin
    def get_completions(self, document, complete_event,force=False):
      import warnings
      with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        global completion_cache_pre_origin_doc
        from rp import tic,toc,ptoctic,ptoc 
        # tic()
        origin=document.get_word_before_cursor()
        import rp.r_iterm_comm as ric
        pre_origin_doc=document.text[:document.cursor_position-(origin[::-1].find('.') if '.' in origin else len(origin))]
        from rp import ring_terminal_bell
        # if pre_origin_doc.endswith('.'):
            # ring_terminal_bell()
        # print()
        # print(pre_origin_doc)
        # print()
        # document=buffer.document

        before_line=document.current_line_before_cursor
        current_line=document.current_line
        after_line=document.current_line_after_cursor
        after=document.text_after_cursor
        before=document.text_before_cursor

        if not after_line and set(before_line)==set('u'):#not after and not '\n' in before and re.fullmatch(before_line):
            #Complete uuuuuu --> CDU that dir   (lets us see where we're going in the completions! No need to count)
            import os
            import rp

            cwd=rp.get_current_directory()
            for _ in range(len(before_line)):
                cwd=rp.get_parent_directory(cwd)

            # updir='CDU '+rp.get_folder_name(cwd)
            updir='CD '+cwd

                
            yield Completion(text=updir, start_position=-10000, display='^'+rp.get_folder_name(cwd))

        if not before_line.strip() and not force:
           return

        ##This paragraph: CD path completion. This should probably be in _get_completions for efficieny with large dicts, but for now this works.
        #before=document.text_before_cursor
        #after=document.text_after_cursor
        #def cd_path_completion_yield_from_candidates(candidates:list):
        #    for c in candidates:
        #        yield Completion(text=c,start_position=-len(origin),display=c[1:]);
        #from rp import get_path_parent
        #def path_complete(path):
        #    path=path.strip()
        #    if path.endswith('/'):
        #        return os.listdir(path)
        #    else:
        #        return os.listdir(get_path_parent(path))
        #if before_line.startswith('CD ') and not ('\n' in before) and not after:#not after and not '\n' in before and re.fullmatch(before_line):
        #    import os
        #    from rp import is_a_directory
        #    paths=before_line[len('CD '):]
        #    paths=path_complete(paths)
        #    yield from cd_path_completion_yield_from_candidates([x for x in paths if is_a_directory(x)])
        #    return 

        ##This paragraph: Dictionary key completion. This should probably be in _get_completions for efficieny with large dicts, but for now this works.
        ##This completes keys in a dictionary iff the dict is a global variable, and it's the first thing you've typed in the buffer
        ##(it's pretty limited - and only does stuff if all the keys are python literals)
        ##For example, if d=={'Hello':'World','Goodbye':'Sam'} then we get completions like this:
        ##     >>> d[|]
        ##         'Hello'
        ##         'Goodbye'
        #def dict_completion_yield_from_candidates(candidates:list):
        #    for c in candidates:
        #        yield Completion(text=c,start_position=-len(origin),display=c[1:]);
        #after_line=document.current_line_after_cursor
        #def is_any_instance(x,*types):
        #    for t in types:
        #        if isinstance(x,t):
        #            return True
        #    return False
        #from collections import OrderedDict
        #if before_line.endswith('[') and after_line==']':
        #    if before_line[:-1] in ric.globa:
        #        if is_any_instance(ric.globa[before_line[:-1]],dict, OrderedDict):
        #           if all(is_any_instance(x,str,int,float,bool) for x in ric.globa[before_line[:-1]]):
        #            # assert False
        #            dict_completion_candidates=[]
        #            for x in ric.globa[before_line[:-1]]:
        #                dict_completion_candidates.append('['+repr(x))
        #            ric.current_candidates[:]=dict_completion_candidates
        #            yield from dict_completion_yield_from_candidates(candidates)
        #            return

        flag=False
        while True:
            if pre_origin_doc not in completion_cache_pre_origin_doc or flag:
                ric.current_candidates=[]
                from rp import tic,ptoctic
                # tic()
                for c in self._get_completions(document, complete_event,force=False):
                    # print(c.text)
                    # print(c.text)
                    ric.current_candidates.append(str(c.text))
                # ptoctic()
                completion_cache_pre_origin_doc[pre_origin_doc]=tuple(ric.current_candidates)
                break
            else:
                ric.current_candidates=list(completion_cache_pre_origin_doc[pre_origin_doc])
                if not ric.current_candidates:
                    from rp import ring_terminal_bell
                    flag=True
                    # ring_terminal_bell()
                    continue

                else:
                    break
        # print("TIME1:",end='')
        # ptoc()
        # print()
        # print(ric.current_candidates)
        post_period_origin=origin if '.' not in origin else origin[origin.find('.')+1:]
        ric.current_candidates=ryan_completion_matches(post_period_origin,tuple(ric.current_candidates))
        # if '.' in origin:
            # ric.current_candidates==ric.current_candidates[::-1]

        user_created_var_names = set(ric.rp_pt_user_created_var_names)

        
        def sorting_key(x):
            # Assigns a sort key based on prefix rules:
            # 1. Items starting with '.' come last.
            # 2. Items starting with '_' come next.
            # 3. Other items come first.
            orig = x
            if x.startswith('.'):
                if origin.startswith('.'):
                    #If explicitly looking for hidden file paths, put it first
                    output = -1
                else:
                    #If not explicitly looking for that, put it last
                    output = 1
            elif x.startswith('_'):
                if origin.startswith('_'):
                    #If explicitly looking for privates, put it first
                    output = -1
                else:
                    #If not explicitly looking for that, put it last
                    output = 1
            else:
                output = 0  # Lowest sort value for other items

            #Put user-made vars first - that means not putting rp things first
            user_created_priority = 0 if x in user_created_var_names else 1

            output = (output, user_created_priority)
            output = (output, sorting_priorities.get(orig,MAX_SORTING_PRIORITY))

            return output

        out_completions=[]

        # print(sorting_priorities)

        # Single loop processing all candidates, sorted by the custom key
        for x in sorted(ric.current_candidates, key=sorting_key):
            if x.endswith("'") or x.endswith('"'): x=x[:-1] #Autocompleted paths in strings are a bit buggy right now

            #When completing 'System/|' origin is just '/'

            def unhidden_path(x):
                o=x
                x=x.strip()
                while x[0] in '/':
                    x=x[1:]
                if x.startswith('.'):
                    return x[1:]
                return o

            #TODO: THis was edited on MACX to give path completion for CD etc on April 19 2024. It's very sloppy and full of bugs and really ugly, done in los angeles. TODO: Undo this commit and make it prettier! 
            if x.startswith('/') and (not '/' in before_line or before_line.endswith('/')):
                x=x[1:]
                
            text=x
            display=x

            if x.strip().endswith('/'):
                #Its annoying when folders are completed with /'s because then when we type tab it goes away
                #But if we type / we get folder// instead.
                #Let the user type the /
                text=text.strip()[:-1]
                if '/' in origin:
                    #Make sure dividers are right
                    text = "/" + text

            if '.' in x and before_line.endswith('.'):
                #Don't complete .g to ..git   or   'rp/.' to 'rp/..git' make it 'rp/.git' instead
                text=unhidden_path(text)

            # display=origin #For debugging


            out_completions.append(Completion(text=text, start_position=-len(post_period_origin), display=display))

        yield from out_completions

        #OLD VERSION BEFORE SORTING_KEY
        # for x in ric.current_candidates:
        #     if not x.startswith('_') and not x.startswith('.'):#Make sure things starting with '_' come last...
        #         yield Completion(text=x,start_position=-len(post_period_origin),display=x)
        # for x in ric.current_candidates:
        #     if     x.startswith('_'):
        #         yield Completion(text=x,start_position=-len(post_period_origin),display=x)
        # for x in ric.current_candidates:
        #     if     x.startswith('.'): #Private files, such as .backup_.py should be displayed last
        #         yield Completion(text=x,start_position=-len(post_period_origin),display=x)

        # print("TIME2:",end='')
        # ptoc()
        # print()

        # return ric.current_candidates

completion_cache_pre_origin_doc={}#Using a bit of dynamic programming to speed up autocompletion by A FACTOR OF 7!! (I measured it with the commented tics/tocs)
#region Time for some super-speedy optimization tricks...
old_origin=''
candidates=set()

from functools import lru_cache

_ryan_completion_matches_cache={}#Note: over time this might cause a memory leakage....idk if that will be a problem....
def ryan_completion_matches(origin:str,candidates:list):
    import rp
    #This function accomplishes one of the few **beautiful** things in rp.pseudo_terminal: my string matching algorithm, specifically made for python namespace elements
    # Better autocompletions
    # candidates origin is string
    # candidates is list of strings
    # def is_match(origin:str,candidate:str):
    #     origin   =list(origin   )# So we can pop chars
    #     candidate=list(candidate)
    #     while origin and candidate:
    #         if origin[0]==candidate.pop(0):
    #             origin.pop(0)
    #     return not origin
    h=hash(origin),hash(candidates)
    if h in _ryan_completion_matches_cache:
        # print(end="HAHA");rp.ptoc()

        return _ryan_completion_matches_cache[h]

    candidates=list(candidates)

    def match(origin:str,candidate:str)->int:
        # from rp import regex_match
        # if not candidate.strip():
            # return None
        # try:
        # import regex
        # if origin and not :#Optimization to quickly weed out most candidates
            # return None
        # except:
            # print("ERROR AT origin",candidate)

        temp=candidate
        origin   =list(origin   )# So we can pop chars
        candidate=list(candidate)
        out=.001
        count=0# higher count means worse match
        def match_char(a:str,b:str):
            return a.upper()==b.upper()
        while origin and candidate:
            pop=candidate.pop(0)
            if match_char(origin[0],pop):
                org=origin.pop(0)
                if org!=pop:
                    count+=.0001# small penalty for wrong char case. still keep it but dont give it ordering priority
                out+=count
                count=0
            elif pop in '_':
                count=0
                out+=.1# penalty because 'ab' is closer to 'a_bz' than 'az_b'
            else:
                count+=1
        import rp.r_iterm_comm
        # rp.tic()
        try:
            temp=(''.join(rp.r_iterm_comm.successful_commands)).count(temp)
            if temp:
                out/=temp# Doesn't have to be division; this is arbitrary. Basically, if we used this before successfully give it more weight and likelyness we want to use it again
        except AttributeError:pass# AttributeError: module 'rp.r_iterm_comm' has no attribute 'successful_commands'
        except TypeError:pass# TypeError: unsupported operand type(s) for /=: 'float' and 'str'
        # rp.ptoc()
        return None if origin else out
    c=candidates
    o=origin
    import rp
    # print('co',len(c),len(o))
    import re
    compiled=re.compile('.*'+'.*'.join(re.escape(x) for x in origin.lower())+'.*')#Using regex to weed out bad candidates sped this function up by an order of magnitude when we had 4000 candidates
    c=candidates=[c for c in candidates if compiled.fullmatch(c.lower())]#Speed things up and weed out bad candidates
    out=sorted([x[1] for x in sorted(x for x in zip([match(o,x)for x in c],c) if x[0] != None) if x[1] != 'mro'],key=lambda x:x==x.startswith('_')+(x.startswith('__') and x.endswith('__')))
    # rp.ptoc()
    _ryan_completion_matches_cache[h]=out
    return out
 
