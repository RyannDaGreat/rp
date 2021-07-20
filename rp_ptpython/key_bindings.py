#TODO on space, if current name is not a function
#TODO fix autocomplete issues: backspace shouldn't erase everything, it should be faster, should highlight callables a different color, should let me immediately search in the middle of a word,3 shouldn't be persistent when I hit the enter key and the cursor is no longer on the keyword,
#TODO add a way to add a space without any of my autocomplete nonsense

#RULES:
    #Should follow normal typing even (such as import import --> import)
    #Should not use memory outisde current text (a few exceptions but they're exceptions not the rule)
    #Should be activated on the fringes of useless or invalid syntax

#TODO: Autocomplete "is" and "in" and "is not" and "and" and "or" (and any other alphabetic operators):
    #When NOT in a string: (WE NEED STRING AREA DETECTION):
        #On press 'a': "x |" ---> "x and |"
        #(because in no other situation would you need that space)
    #How to handle conflict: "in" vs "is":
        #Branch prediction: figure out how to predict which one the user uses more often.  #Let's say they use 'in' more often; more specifically, if the variable to the left has a __contains__ function:
            #On press i: "x |" ---> "x in |"
        #Let's say that the user actually wanted "is". Because of the rule that normal typing should be supported:
            #On press s: "x in |" ---> "x is |"
    #Shouldn't REALLY be limited to just spaces (should also allow ')',']','')

#Hold alt to make space act normal.


from __future__ import unicode_literals
import re
from rp.prompt_toolkit.document                    import Document
from rp.prompt_toolkit.enums                       import DEFAULT_BUFFER
from rp.prompt_toolkit.filters                     import HasSelection, IsMultiline, Filter, HasFocus, Condition, ViInsertMode, EmacsInsertMode
from rp.prompt_toolkit.key_binding.vi_state        import InputMode
from rp.prompt_toolkit.key_binding.registry        import Registry,_Binding
from rp.prompt_toolkit.keys                        import Keys,Key
from rp.prompt_toolkit.buffer                      import Buffer
from rp.prompt_toolkit.key_binding.input_processor import KeyPressEvent

def get_all_function_names(code:str):        
    #Return all the names of all functions defined in the given code, in the order that they appear
    from rp import lrstrip_all_lines,line_split
    lines=line_split(lrstrip_all_lines(code))
    import re
    defs=[line for line in lines if re.fullmatch(r'\s*def\s+\w+\s*\(.*',line)]
    func_names=[d[len('def '):d.find('(')].strip() for d in defs]
    return func_names

def run_code_without_destroying_buffer(event,put_in_history=True):
    #Run the code in the buffer without clearing it or destroying cursor position etc
    buffer=event.cli.current_buffer
    import rp.r_iterm_comm as ric
    ric.dont_erase_buffer_on_enter+=['DO IT']
    buffer.accept_action.validate_and_handle(event.cli, buffer,put_in_history=put_in_history)

def run_arbitrary_code_without_destroying_buffer(code,event,put_in_history=True):
    buffer=event.cli.current_buffer
    original_document=buffer.document
    buffer.document = Document(text=code)#Temporarily change the text in the buffer
        # cursor_position=len(''.join(lines_before + reshaped_text)))
    run_code_without_destroying_buffer(event,put_in_history=put_in_history)
    buffer.document=original_document#Put the old text/cursor pos/etc back. Dont mutate the buffer

def handle_run_cell(event):
    #Happens when we press control+w or alt+w
    #Run current cell between the boundary prefixes
    buffer=event.cli.current_buffer
    def main():
        text=buffer.document.text
        cursor_pos=buffer.cursor_position
        cell_code=get_cell_code(text,cursor_pos,cell_boundary_prefix)
        from rp import fansi_print
        # fansi_print("RUNNING CODE CELL:",'blue','bold')
        # fansi_print(cell_code,'blue')

        #When we do this, don't include that spam in our history...right? Maybe I'll change my mind in the future...I can't decide...like, it's annoying but it's truthful...
        run_arbitrary_code_without_destroying_buffer(cell_code,event,put_in_history=True)#To include or not to include...which one??
    main()

def edit_event_buffer_in_vim(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        text=buffer.document.text   
        from rp import text_file_to_string,temporary_file_path,string_to_text_file
        import subprocess

        path=temporary_file_path()+'.py'
        string_to_text_file(path,text)

        lineno=document.text_before_cursor.count('\n')
        colno=document.cursor_position_col

        #+=1 because vim's line/col numbers start at 1, not 0
        colno+=1
        lineno+=1

        try:
            try:
                subprocess.call(["vim",path,'+call cursor(%i,%i)'%(lineno,colno),'+normal zz'])#https://stackoverflow.com/questions/3313418/starting-vim-at-a-certain-position-line-and-column-of-a-file
            except:
                subprocess.call(["vi",path,'+call cursor(%i,%i)'%(lineno,colno),'+normal zz'])#If it doesn't work with vim, try vi. vi is installed on basically every computer by default (except windows)
        except FileNotFoundError as error:
            buffer.insert_text('#ERROR: Cant find vim. Are you sure its installed? '+str(error))
            return True

        text=text_file_to_string(path)

        from rp import delete_file
        delete_file(path)

        if text!='':
            #That means the user saved the file
            buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)

        event.cli.renderer.clear()#Refresh the screen

        try:
            #Attempt to restore the cursor position from vim and use it in rp
            #I'm still not 100% sure if this will always work; so for now I'm going to squelch any errors.
            import os
            def get_viminfo():return '\n'.join(open(os.path.expanduser('~/.viminfo'),errors='ignore').readlines())
            def get_last_cursor_row_in_vim():    return int(os.path.expanduser([line for line in get_viminfo().splitlines() if line.startswith("'0 ")].pop().split()[ 1]))
            def get_last_cursor_column_in_vim(): return int(os.path.expanduser([line for line in get_viminfo().splitlines() if line.startswith("'0 ")].pop().split()[ 2]))
            def get_last_path_edited_in_vim():   return     os.path.expanduser([line for line in get_viminfo().splitlines() if line.startswith("'0 ")].pop().split()[-1])
            from rp import get_file_name
            if get_file_name(get_last_path_edited_in_vim())==get_file_name(path):
                #We recently edited the file, and we should attempt to restore the cursor
                buffer.set_cursor_column(get_last_cursor_column_in_vim())
                buffer.set_cursor_row(get_last_cursor_row_in_vim()-1 )
        except:
            pass

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

def get_ans():
    import rp.r_iterm_comm as ric
    if 'ans' in ric.globa:
        return ric.globa['ans']
    else:
        return None


def do_vim_copy(string):
    import rp
    global _copied_string
    rp.vim_copy(string)
    # _copied_string=string

def do_local_copy(string):
    import rp
    global _copied_string
    rp.local_copy(string)
    # _copied_string=string

def do_tmux_copy(string):
    import rp
    global _copied_string
    rp.tmux_copy(string)
    # _copied_string=string

def do_vim_paste(buffer,repr_mode=False,commented=None):
    import rp
    try:
        if repr_mode:
            text=repr(rp.vim_paste())
        else:
            text=str(rp.vim_paste())

        if commented is not None:
            text=commented_string(buffer,text,spaces=commented)

        buffer.insert_text(text)
    except:
        pass

def do_tmux_paste(buffer,repr_mode=False,commented=None):
    import rp
    try:
        if repr_mode:
            text=repr(rp.tmux_paste())
        else:
            text=str(rp.tmux_paste())

        if commented is not None:
            text=commented_string(buffer,text,spaces=commented)

        buffer.insert_text(text)
    except:
        pass

def do_web_copy(string):
    import rp
    global _copied_string
    rp.web_copy(string)
    # _copied_string=string

def do_local_paste(buffer,repr_mode=False):
    import rp
    try:
        if repr_mode:
            buffer.insert_text(repr(str(rp.local_paste())))
        else:
            buffer.insert_text(str(rp.local_paste()))
    except:
        pass
def do_web_paste(buffer,repr_mode=False):
    import rp
    try:
        if repr_mode:
            buffer.insert_text(repr(str(rp.web_paste())))
        else:
            buffer.insert_text(str(rp.web_paste()))
    except:
        pass

_copied_string=""
def do_copy(string):
    import rp
    global _copied_string
    rp.string_to_clipboard(string)
    _copied_string=string

def commented_string(buffer,string,spaces=0):
    if isinstance(spaces,int):
        spaces=' '*spaces
    cursor_column=buffer.document.cursor_position_col
    string=string.split('\n')
    string=['#'+spaces+x for x in string]
    flag=False
    for index,line in enumerate(string):
        if flag:
            string[index]=' '*cursor_column+line
        flag=True
    string='\n'.join(string)
    return string

def do_paste(buffer,commented:int=None):
    import rp
    string=rp.string_from_clipboard()
    if commented is not None:string=commented_string(buffer,string,spaces=commented)
    buffer.insert_text(string)

def do_string_paste(buffer):
    import rp
    buffer.insert_text(repr(rp.string_from_clipboard()))
import rp.r_iterm_comm as ric
enable_space_autocompletions=ric.enable_space_autocompletions#This variable is a list that's mutated between being empty and being full, which toggles it's truth value. This feature isn't completely figured out yet...I suppose it's better to disable it for the time being...

from rp import *
__all__ = (
    'load_python_bindings',
    'load_sidebar_bindings',
    'load_confirm_exit_bindings',
)
from rp import *

def toggle_top_line_text(buffer,top_line='debug()\n'):
    text=buffer.document.text
    old_cursor_pos=buffer.document.cursor_position
    buffer.cursor_up(99999)
    buffer.cursor_left(99999)
    if text.startswith(top_line):
        #Delete 'debug()' from the top
        buffer.delete(len(top_line))
        buffer.document=Document(buffer.document.text,old_cursor_pos-len(top_line),buffer.document.selection)
    else:
        #Insert 'debug()' at the top
        buffer.insert_text(top_line)
        buffer.document=Document(buffer.document.text,old_cursor_pos+len(top_line),buffer.document.selection)
def toggle_bottom_line_text(buffer,bottom_line):
    def toggled_last_line(string,line):
        # print()
        # print("BEFORE:"+repr(string))
        lines=string.splitlines() or ['']
        if line==lines[-1]:
            del lines[-1]
        else:
            lines.append(line)
        out='\n'.join(lines)
        # print("AFTER:"+repr(out))
        # print()
        return out
    text=buffer.document.text
    old_cursor_pos=buffer.document.cursor_position
    new_text=toggled_last_line(text,bottom_line)
    buffer.document=Document(new_text,min(old_cursor_pos,len(new_text)-1),buffer.document.selection)

n_makes_in_and_s_makes_is=True#This is imperfect and got annoying
s_makes_is=True#This is imperfect and got annoying

def text_to_speech(words):
    try:
        from rp import text_to_speech
        text_to_speech(words)
    except:pass#Who cares if this doesn't work, it's just for debugging anyway...


# alt_updown_speed=
# def any_key_pressed_prefix(key,buffer):
#     #This function should include only things that happen during every keystroke. 
#     #If this function returns True, it cancels the rest of the execution. 
#     #This function happens before anything else.
#     alt_updown_speed=3
#     return False


#region code cells
#See https://asciinema.org/a/Hwj84iFknDtqIh5Tag2Eug6aj
cell_boundary_prefix='##'#SETTINGS
def separator_boundaries(code,separator_token):
    #Return cursor positions of the beginning of each boundary, including the start and end of the string
    #code="""@handle(Keys.ControlU)
#    def _(event):
#        +++
#        +
#            buffer=event.cli.current_buffer
#            buffer.insert_text('UNDO')
#            +++
#        @handle(Keys.ControlP)
#        def _(event):
#            +++  Hello
#            -
#            buffer=event.cli.current_buffer
#+++"""
    #separator_boundaries(code,'+++')  ->  [0, 40, 145, 214, 295, 299]
    #NOTE THE -1 and len()+1 at either side were originally 0 and len(), but for practicality (executing cells where the cursor is at the beginning or end of the text) I did this as a quick hack.
     # The examples are slightly different than the current code because of this.
    return [-1]+[x.span()[0] for x in re.finditer(r'((?<=(\n))|^) *'+re.escape(separator_token),code)]+[len(code)+1]
def above_and_below(value,L):
    #Examples:
    # ⮤ above_and_below(30,[2, 3, 13, 27, 28, 35, 35, 52, 90, 95])
    #ans = (28, 35)
    #
    # ⮤ above_and_below(4,[1,3,7,8,9])
    #ans = (3, 7)
    # ⮤ above_and_below(100,[1,3,7,8,9])
    #ans = (9, 100)
    # ⮤ above_and_below(0,[3,7,8,9])
    #ans = (0, 3)
    return max((x for x in L if x<=value),default=min(L)),min((x for x in L if x>=value),default=max(L))
def get_cell_code(text,cursor_pos,prefix=cell_boundary_prefix):
    #EXAMPLE:
    # ⮤ code
    #ans = @handle(Keys.ControlU)
    #    def _(event):
    #        ###
    #        +
    #            buffer=event.cli.current_buffer
    #            buffer.insert_text('UNDO')
    #            ###
    #        @handle(Keys.ControlP)
    #        def _(event):
    #            ###  Hello
    #            -
    #            buffer=event.cli.current_buffer
    ####
    # ⮤ separator_boundaries(code,'###')
    #ans = [0, 40, 145, 214, 295, 299]
    # ⮤ get_cell_code(code,30,'###')
    #ans = @handle(Keys.ControlU)
    #    def _(event):
    # ⮤ get_cell_code(code,41,'###')
    #ans = 
    #        ###
    #        +
    #            buffer=event.cli.current_buffer
    #            buffer.insert_text('UNDO')
    # ⮤ get_cell_code(code,67,'###')
    #ans = 
    #        ###
    #        +
    #            buffer=event.cli.current_buffer
    #            buffer.insert_text('UNDO')
    # ⮤ get_cell_code(code,213,'###')
    #ans = 
    #            ###
    #        @handle(Keys.ControlP)
    #        def _(event):
    # ⮤ get_cell_code(code,150,'###')
    #ans = 
    #            ###
    #        @handle(Keys.ControlP)
    #        def _(event):
    start,end=above_and_below(cursor_pos,separator_boundaries(text,prefix))
    return text[max(0,start):min(len(text),end)]
#endregion

def swap_from_import(line):
    try:
        #EXAMPLES:
        #     >>> swap_from_import('   import jugio as gi')
        #    ans =    from jugio import
        #     >>> swap_from_import('   from bugg.malo import bees')
        #    ans =    import bugg.malo
        whitespace=line[:len(line)-len(line.lstrip())]
        line=line[len(whitespace):]
        items=line.split()
        items=items[:2]
        if items[0]=='from':
            items[0]='import'
        elif items[0]=='import':
            items[0]='from'
            items.append('import ')        
        line=' '.join(items)
        return whitespace+line
    except Exception:
        return line

align_char='→'
def align_lines_to_char(string,char=align_char,space=' '):
    #EXAMPLE:
    #    SPASTE
    #    ans = from rp.prompt_toolkit.document →import Document
    #    from rp.prompt_toolkit.enums →import DEFAULT_BUFFER
    #    from rp.prompt_toolkit.filters →import HasSelection, IsMultiline, Filter, HasFocus, Condition, ViInsertMode, EmacsInsertMode
    #    from rp.prompt_toolkit.key_binding.vi_state →import InputMode
    #    from rp.prompt_toolkit.key_binding.registry →import Registry
    #    from rp.prompt_toolkit.keys →import Keys,Key
    #    from rp.prompt_toolkit.buffer →import Buffer
    #    ⮤ print(align(ans))
    #    from rp.prompt_toolkit.document             import Document
    #    from rp.prompt_toolkit.enums                import DEFAULT_BUFFER
    #    from rp.prompt_toolkit.filters              import HasSelection, IsMultiline, Filter, HasFocus, Condition, ViInsertMode, EmacsInsertMode
    #    from rp.prompt_toolkit.key_binding.vi_state import InputMode
    #    from rp.prompt_toolkit.key_binding.registry import Registry
    #    from rp.prompt_toolkit.keys                 import Keys,Key
    #    from rp.prompt_toolkit.buffer               import Buffer
    assert len(space)==1
    lines=string.splitlines()
    while any([char in x for x in lines]):
        alignto=0
        for i,line in enumerate(lines):
            if char in line:
                alignto=max(line.find(char),alignto)
        for i,line in enumerate(lines):
            if char in line:
                pos=line.find(char)
                line=line[:pos]+space*(alignto-pos)+(line[pos+1:] if len(line)-1!=pos else '')
                lines[i]=line
    out='\n'.join(lines)
    return out

def split_def_arguments_into_multiple_lines(single_line_def):    
    # print("GOT "+repr(single_line_def))
    #EXAMPLE:
    #INPUT:  'def play_chord(*semitones:list,t=1,block=True,sampler=triangle_tone_sampler):'
    #OUTPUT:
    #def play_chord(*semitones:list,
    #               t=1,
    #               block=True,
    #               sampler=triangle_tone_sampler):
    s=single_line_def
    try:
        import re
        assert re.fullmatch(r' *def .*: *(#.*)?',s)
        l=s.split(',')
        w=l[0].find('(')
        assert w!=-1
        o=[]
        o.append(l.pop(0)+',')
        for _ in range(len(l)):
            o.append(' '+' '*w+l.pop(0)+',')
        o='\n'.join(o)
        o=o[:-1]
        return o
    except Exception as E:
        return s
            
def keys(root):
    #Stolen from rinsp_search
    out=set()
    try:out.update(dir(root))
    except:pass
    try:out.update(root.__dict__)
    except:pass
    return sorted(out)
            
def find_all_substring_matches(string,substring):
    #Return a list of starting indices
    #https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
    #EXAMPLE:
    #    ⮤ find_all_substring_matches('jojo my jojo its jojo','jojo')
    #    ans = [0, 8, 17]
    return [m.start() for m in re.finditer(re.escape(substring), string)]
def token_exists(token_name):
    from rp import is_namespaceable
    if not is_namespaceable(token_name):
        return False#We don't want to run eval on anything except tokens...
    try:
        eval(token_name,ric.globa)
        return True
    except:
        return False#be on the safe side with space-function completions
def token_name_found_of_interest(before_line)->(str,object,bool):
    from rp import is_namespaceable
    token_of_interest=name_of_interest=None
    try:
        # fansi_print("\n\n"+split[-1]+"\n\n")

        string=''
        for char in reversed(before_line):
            if not (is_namespaceable(char) or char in '0987654321') and char not in '.':
                break
            string=char+string
        name_of_interest=string
        # print("HE")
        token_of_interest=eval(string,r_iterm_comm.globa)  # ≣token_of_interest=r_iterm_comm.rp_evaluator(string,True)# Should be just a name so there should be no side effects
        # print("HOO",token_of_interest)
        #
        # for char in string:
        #     if not char.isalnum() and char not in '.' and not is_namespaceable(char):
        #         string=string.replace(char,' ')
        # name_of_interest=string
        # token_of_interest=eval(string,r_iterm_comm.globa)# ≣token_of_interest=r_iterm_comm.rp_evaluator(string,True)# Should be just a name so there should be no side effects
    except:token_of_interest,name_of_interest,False#No variable called that was found
    return token_of_interest,name_of_interest,True
def starts_with_any(string,*prefixes):
    for p in prefixes:
        if string.startswith(p):
            return True
    return False

def cursor_on_string(text,cpos):
    #NOT accurate, dont put into the main RP library
    #EXAMPLE:
    # ⮤ def f(s):
    #2     print(s)
    #3     print(''.join([str(int(bool(cursor_on_string(s,i))))for i in  range(len(s))]))
    #4 
    #⮤ f('hello="Helo"+234')
    #hello="Helo"+234   <--- this works well because theresno whitespace between hello and = and "Helo"
    #0000001111110000
    import rp
    tokens=split_python_tokens(text)
    count=0
    for token in tokens:
        if count+len(token)>cpos:
            try:
                return isinstance(eval(token),str)
            except:
                return False
        count+=len(token)
    return False

def cursor_on_comment(text,cpos,tokens):
    #NOT accurate, dont put into the main RP library
    import rp
    tokens=split_python_tokens(text)
    count=0
    for token in tokens:
        if count+len(token)>cpos:
            try:
                return token.startswith('#')
            except:
                return False
        count+=len(token)
    return False

def current_token(text,cpos):
    #NOT accurate, dont put into the main RP library
    import rp
    tokens=split_python_tokens(text)
    count=0
    for token in tokens:
        if count+len(token)>cpos:
            return token
        count+=len(token)
    return ''

def true_get_if_in_string_or_comment(before_line,after_line,buffer):
    #This function IS not totally acurate, becauwe of a hack where I replace whitespace with other characters to trick the tokenizer into keeping cursor positoin relevant
    text=buffer.document.text#+' '#add space to prevent last char from returning false
    text=text.replace(' ','+').replace('\n','\n+')#Python tokenize gets rid of whitespace and newlines which we need to count but adding +'s still preserves whats  a string and whats a comment. its a quick cheap hack.'
    cpos=buffer.document.cursor_position-1
    token=current_token(text,cpos)
    out=False
    try:
        if isinstance(eval(token),str):
            out= True
    except:pass
    out=out or token.startswith('#')
    if out:
        # print("WAH")
        return True 
    return False

    # if cursor_on_string(text,cpos) or cursor_on_comment(text,cpos):
        # print("WAHH")
        # return True
    # return False
    # return '"' in before_line and after_line.count('"')==before_line.count('"') or \
                                       # "'" in before_line and after_line.count("'")==before_line.count("'") or \
                                       # '#' in before_line

_previous_after_line=None
_previous_before_line=None
_previous_result=False
def get_if_in_string_or_comment(before_line,after_line,buffer):
    if not '\n' in buffer.text:
        if re.fullmatch(r'((!|!!|CD |RUN |([A-Z]+ )).*)',before_line):#Things we want to turn microcompletions off for
            return True
    #This function attempts to make an nearly equivalent but faster version of true_get_if_in_string_or_comment
    global _previous_result,_previous_after_line,_previous_before_line
    if after_line!=_previous_after_line or\
          before_line.count('#')!=_previous_before_line.count('#') or\
          before_line.count("'")!=_previous_before_line.count("'") or\
          before_line.count('"')!=_previous_before_line.count('"'):
        _previous_result=true_get_if_in_string_or_comment(before_line,after_line,buffer)
    _previous_after_line =after_line
    _previous_before_line=before_line
    return _previous_result 


_meta_pressed=[]
def meta_pressed(clear=True):#This should only be called once per keystroke
    out=bool(_meta_pressed)
    if clear:
        _meta_pressed.clear()
    return out

def line_above(buffer):
    return line_above_document(buffer.document)

def line_above_document(document):
    before=document.text_before_cursor
    if not '\n' in before:
        return None
    before_lines=before.split("\n")
    return before_lines[-2]


def beginswithany(a,*b):
    for x in b:
        if a.startswith(x):
            return True
    return False

def ends_with_namespaceable(s):
    #      ⮤ ends_with_namespaceable('oaisjdoiasd')
    # ans = True
    #  ⮤ ends_with_namespaceable('oaisj[doiasd')
    # ans = True
    #  ⮤ ends_with_namespaceable('oaisj[4doiasd')
    # ans = False
    #  ⮤ ends_with_namespaceable('oaisj[4doi4asd')
    # ans = False
    #  ⮤ ends_with_namespaceable('oaisj[4doi4as5d')
    # ans = False
    #  ⮤ ends_with_namespaceable('oaisj[234234')
    # ans = False
    #  ⮤ ends_with_namespaceable('234,oaisj')
    from rp import is_namespaceable
    last_char=''
    for c in reversed(s):
        if not is_namespaceable(c) and not c.isnumeric():
            return not last_char.isnumeric()
        last_char=c
    return bool(last_char)
def ends_with_number(s):
    #  ⮤ ends_with_number('osdi[f[4')
    # ans = True
    #  ⮤ ends_with_number('osdi[f[d4')
    # ans = False
    #  ⮤ ends_with_number('osdiasdf4')
    # ans = False
    #  ⮤ ends_with_number('osdia34534sdf4')
    # ans = False
    #  ⮤ ends_with_number('osdia3asdfasd.4534sdf4')
    # ans = False
    #  ⮤ ends_with_number('osdia3asdfasd.4534sdf.4')
    # ans = True
    from rp import is_namespaceable
    last_char=''
    for c in reversed(s):
        if not c.isnumeric():
            return not is_namespaceable(c)
        last_char=c
    return bool(last_char)
def so_far(s):
    #EXAMPLES:
    # >> so_far('asod jasoidj a: soajdo is')
    #ans = 'soajdo is'
    # >> so_far('asod jasoidj a: soaasd ajdo is')
    #ans = 'soaasd ajdo is'
    # >> so_far('asod jasoidj a:retu')
    #ans = 'retu'
    i=s.rfind(':')
    s=s[i+1:]
    s=s.strip()
    return s
def splinterify(x):
    #For use in regex expression prefixes
    #EXAMPLES:
    # >> splinterify('hello')
    #ans = 'h|he|hel|hell'
    # >> splinterify('world')
    #ans = 'w|wo|wor|worl'
    out=[]
    for i in range(1,len(x)):
        out.append(x[:i])
    return '|'.join(out)
def indent_hiearchy(s:str):
    """
    Takes a str such as:
'''
def hiu(iub):
    ewq(ojhi)
    if h:
        apple
        hio
            iuy
              ioo'''
    And returns:
    ['              ioo',
     '            iuy',
     '        hio',
     '    if h:',
     'def hiu(iub):']
    """
    o=None
    for l in reversed(s.splitlines()):
        if o is None or not l.startswith(o):
            yield l
            o=get_indent(l)
            if not o:
                break
def find_header(code:str,*line_starts:str)->str:
    #(was originally just find_level, see it's purpose)
    #this function returns the entire line itself instead of just the number of indents
    #returns None if not in such a block
    for i,e in enumerate(indent_hiearchy(code)):
        if starts_with_any(e.lstrip(),*line_starts):
            return e
    return None
def find_level(code:str,*line_starts:str)->int:
    #return the unindents needed (assumed to be spaces) to reach block starting with any string from line_starts
    #returns None if not in such a block
    header=find_header(code,line_starts)
    if header is None:
        return None
    return len(get_indent(header))
def get_indent(line):
    #returns a string that just contains the line's indent
    return line[:len(line)-len(line.lstrip())]
def endswithany(a,*b):
    for x in b:
        if a.endswith(x):
            return True
    return False
def in_class_func_decl(buffer):#can be easily memoized but i wont bother unless its an issue; (prob got bigger probs tbh)
    document=buffer.document
    current_line=document.current_line
    before_line=document.current_line_before_cursor
    after_line=document.current_line_after_cursor
    before=document.text_before_cursor
    after= document.text_after_cursor
    lines=reversed(before.split('\n'))
    indent=get_indent(before_line)
    for line in lines:
        if not line.startswith(indent):
            return line.lstrip().startswith('class ')
    return False
class TabShouldInsertWhitespaceFilter(Filter):
    """
    When the 'tab' key is pressed with only whitespace character before the
    cursor, do autocompletion. Otherwise, insert indentation.

    Except for the first character at the first line. Then always do a
    completion. It doesn't make sense to start the first line with
    indentation.
    """
    def __call__(self, cli):
        b = cli.current_buffer
        before_cursor = b.document.current_line_before_cursor

        return bool(b.text and (not before_cursor or before_cursor.isspace()))

def has_selected_completion(buffer):# If we have a completion visibly selected on the menu
    return buffer.complete_state and buffer.complete_state.complete_index is not None
last_pressed_dash=False


class CommentedParenthesizerAutomator:
    def __init__(self,
        upper_marker='#',
        lower_marker='#',
        match_indent=True
        ):
    # def __init__(self,
    #     upper_marker='#╵',
    #     lower_marker='#╷',
    #     match_indent=True
    #     ):
        self.upper_marker=upper_marker
        self.lower_marker=lower_marker
        self.match_indent=match_indent#If true, indent the parnthesis comments along with the rest of the code. Otherwise, start the parenthesizer comments at the very beginning of the line

    def parenthezized_line(self,line:str)->str:
        assert '\n' not in line,'Input Assertion Error: line should be a single line, but its a multiline string. line='+repr(line)

        from rp import parenthesizer_automator

        original_line=line

        if self.match_indent:
            whitespace=line[:len(line)-len(line.lstrip())]
            assert line[len(whitespace):]==line.lstrip()
        else:
            whitespace=''

        middle_line  =line[len(whitespace):]
        parenth_lines=parenthesizer_automator(middle_line).splitlines()

        assert len(parenth_lines)==0 or len(parenth_lines)%2,'Internal logical assertion (this should never fail unless this function is broken) due to the nature of rp.parenthesizer_automator: rp.parenthesizer_automator should always return an odd number of lines, unless it returns 0 lines'
        if len(parenth_lines)<=1:
            return original_line

        upper_lines=parenth_lines[:len(parenth_lines)//2   ]
        lower_lines=parenth_lines[ len(parenth_lines)//2+1:]

        upper_lines=[(self.upper_marker+(upper_line[len(self.upper_marker):] if len(upper_line)>=len(self.upper_marker) else '')) for upper_line in upper_lines]
        lower_lines=[(self.lower_marker+(lower_line[len(self.lower_marker):] if len(lower_line)>=len(self.lower_marker) else '')) for lower_line in lower_lines]

        out_lines=[*upper_lines,middle_line,*lower_lines]
        out_lines=[whitespace+out_line for out_line in out_lines]

        out='\n'.join(out_lines)

        return out

    def is_upper_line(self,line:str)->bool:
        if not isinstance(line,str):return False#Can't be an upper line if it's not a line...
        assert '\n' not in line,'Input Assertion Error: line should be a single line, but its a multiline string. line='+repr(line)
        return line.lstrip().startswith(self.upper_marker) and set(line.strip())<=set(' #│┌┐') and set(line)&set('│└┘┌┐')

    def is_lower_line(self,line:str)->bool:
        if not isinstance(line,str):return False#Can't be a lower line if it's not a line...
        assert '\n' not in line,'Input Assertion Error: line should be a single line, but its a multiline string. line='+repr(line)
        return line.lstrip().startswith(self.lower_marker) and set(line.strip())<=set(' #│└┘') and set(line)&set('│└┘┌┐')

    def is_parenthesized_at_line(self,string:str,line_number:int)->bool:
        #Returns true if there are visible parenthesizer comments above and below the given linenumber in the given string
        #Check for comments with the right markers above and below that line
        #Used to determine whether this line is worth looking at (to see whether we must update its surroundings when using the editor)

        if line_number==0:
            return False #You can't have any upper parenthesis if we're on the first line

        lines=string.splitlines()
        try:
            line_above=lines[line_number-1]
            line_below=lines[line_number+1]
            return self.is_lower_line(line_below) and self.is_upper_line(line_above)
        except IndexError:
            return False

    def unparenthesized(self,string,line_number)->str:
        #Remove the parenthesizer comments around a given line number on the given string
        lines=string.splitlines()

        #Delete all lower lines
        while True:
            try:
                line_below_index=line_number+1
                line_below=lines[line_below_index]
                if self.is_lower_line(line_below):
                    del lines[line_below_index]
                else:
                    break
            except IndexError:
                break

        #Delete all upper lines
        line_above_index=line_number-1
        while line_above_index>=0:
            try:
                line_above=lines[line_above_index]
                if self.is_upper_line(line_above):
                    del lines[line_above_index]
                    line_above_index-=1
                else:
                    break
            except IndexError:
                break

        return '\n'.join(lines)


    def parenthesized_at_line(self,string,line_number)->str:
        #Insert parenthesizer comments around a given line in a string and return the result
        lines=string.splitlines()
        line =lines[ line_number]
        lines=lines[line_number:line_number+1]=self.parenthezized_line(line).splitlines()
        return '\n'.join(lines)
        
    def unparenthesize_buffer(self,buffer)->None:
        #Remove the parenthesizer comments around the cursor in the given buffer
        #Delete all lower lines
        while self.is_lower_line(buffer.document.current_line_below):
            from rp import random_chance
            buffer.delete_line_below_cursor()

        #Delete all upper lines
        while self.is_upper_line(buffer.document.current_line_above):
            buffer.delete_line_above_cursor()

    def parenthesize_buffer(self,buffer)->None:
        #Insert parenthesizer comments around the cursor in a given buffer
        current_line =buffer.document.current_line
        cursor_column=buffer.document.cursor_position_col
        buffer.cursor_right(999999)
        buffer.delete_before_cursor(len(current_line))
        new_text=self.parenthezized_line(current_line)
        buffer.insert_text(new_text)
        if '\n' in new_text:
            buffer.cursor_up(new_text.count('\n')//2)
        buffer.set_cursor_column(cursor_column)

    def buffer_is_parenthesized_at_cursor(self,buffer)->bool:
        #Returns true if there are visible parenthesizer comments above and below the buffer's cursor
        #Check for comments with the right markers above and below that line
        #Used to determine whether this line is worth looking at (to see whether we must update its surroundings when using the editor)
        return self.is_parenthesized_at_line(buffer.document.text,buffer.document.cursor_position_row)

    def buffer_refresh_parenthesization(self,buffer)->None:
        if self.buffer_is_parenthesized_at_cursor(buffer):
            #Refresh the parenthesization
            self.unparenthesize_buffer(buffer)
            self.parenthesize_buffer(buffer)
        else:
            pass

    def buffer_toggle_parenthesization(self,buffer)->None:
        if self.buffer_is_parenthesized_at_cursor(buffer):
            self.unparenthesize_buffer(buffer)
        else:
            self.parenthesize_buffer(buffer)


        
commented_parenthesizer_automator=CommentedParenthesizerAutomator()


_global_event=None
def post_handler(binding:_Binding,event:KeyPressEvent,old_document:Document):
    #This function should be very lightweight, as it's called once after EVERY keystroke in the editor (including ones like control+e which don't even modify the text)
    #I made sure that post_handler is called on every keystroke by modifying input_processor.py and replacing key_bindings.py's '@handle' with a lambda that also ensures this function is called
    #Get the pressed char
    char=event.data

    assert isinstance(char,str)

    #Get information about old_document
    old_text         = old_document.text
    old_current_line = old_document.current_line
    old_after_line   = old_document.current_line_after_cursor
    old_before_line  = old_document.current_line_before_cursor
    old_before       = old_document.text_before_cursor
    old_after        = old_document.text_after_cursor
    old_above_line   = line_above_document(old_document)

    #Get the buffer and related information
    buffer=event.cli.current_buffer
    text=document=current_line=after_line=before_line=before=after=above_line=None
    def refresh_strings_from_buffer():
        nonlocal text,document,current_line,after_line,before_line,before,after,above_line
        document     = buffer.document
        text         = buffer.document.text
        current_line = buffer.document.current_line
        after_line   = buffer.document.current_line_after_cursor
        before_line  = buffer.document.current_line_before_cursor
        before       = buffer.document.text_before_cursor
        after        = buffer.document.text_after_cursor
        above_line   = line_above(buffer)
    refresh_strings_from_buffer()

    if text!=old_text:
        commented_parenthesizer_automator.buffer_refresh_parenthesization(buffer)#This is optimized and only makes changes if nessecary


def handle_character(buffer,char,event=None):
    #This function should receive all VISIBLE keystrokes (such as 'a','b','c','1','2','3' but also ' ','\n','.','$' etc)
    #But it should NOT receive things like backspace, backtab, or other control keys that aren't actually part of the code
    #If this function returns true it overrides the other code that handles that specific char
    from rp import is_namespaceable
    global last_pressed_dash
    import rp.r_iterm_comm as ric
    import tokenize

    if False:#No microcompletions
        buffer.insert_text(char)
        return True

    text=current_line=after_line=before_line=before=after=above_line=before_tokens=after_tokens=before_line_ends_with_number=None
    def refresh_strings_from_buffer():
        nonlocal text,current_line,after_line,before_line,before,after,above_line,before_tokens,after_tokens,before_line_ends_with_number
        text                = buffer.document.text
        current_line        = buffer.document.current_line
        after_line          = buffer.document.current_line_after_cursor
        before_line         = buffer.document.current_line_before_cursor
        before              = buffer.document.text_before_cursor
        after               = buffer.document.text_after_cursor
        above_line          = line_above(buffer)

        after_tokens        = split_python_tokens(after_line ,True)
        before_tokens       = split_python_tokens(before_line,True)
        before_line_ends_with_number=before_tokens and before_tokens[-1].type==tokenize.NUMBER
    refresh_strings_from_buffer()

    if char=='\n' and after_line in ['"',"'"]:
        #Even if (especially if) we're in a string...
        #On \n:  ‹'|'›  -/->  ‹'\n|'›
        #On \n:  ‹'|'›  --->  ‹''\n|›
        buffer.cursor_right(100)

    if char==' ' and meta_pressed(clear=False):
        buffer.insert_text(' ')#This should always work
        meta_pressed(clear=True)
        return True

    if char=='v' and meta_pressed(clear=True):
        edit_event_buffer_in_vim(event)
        return True

    if char=='r' and meta_pressed(clear=True):
        run_arbitrary_code_without_destroying_buffer(repr(text),event,put_in_history=True)#To include or not to include...which one??
        buffer.document=Document('',0,buffer.document.selection)
        return True

    if char=='q' and meta_pressed(clear=True):
        #Delete all
        #Equivalent to \da
        buffer.document=Document('',0,buffer.document.selection)
        return True

    if char=='w' and meta_pressed(clear=True):
        handle_run_cell(event)
        return True

    in_string_or_comment=get_if_in_string_or_comment(before_line,after_line,buffer)
    if char not in '\n\'\"' and in_string_or_comment:
        buffer.insert_text(char)#Don't do anything but write the damn character lol
        return True

    if last_pressed_dash and char in '-=' and not in_string_or_comment and not after_line.strip() and re.fullmatch(r' *[a-zA-Z_0-9]+\_',before_line):
        buffer.delete_before_cursor()
        buffer.insert_text('-')#Trigger '--' or '-=' indirectly by replacing the '_' with a '-' where applicable (aka NOT if the user made the _ by typing _ with the shift key. This is one of the rare instances where stateful is OK)
    if char=='-':last_pressed_dash=True
    else:        last_pressed_dash=False

        
    if char in '/\n' and before_line.endswith('?/') and not after:
        #This rule is a HACK to preserve the functionality of ?/
        #Without this rule, pressing enter after ?/ will turn it into ??
        if char=='\n':
            return False
        #if char=='/':
        #    #Actually this rule isn't nessecary...pressing enter on // turns it into ??
        #    buffer.delete_before_cursor()
        #    buffer.insert_text('?')
        #    return True
    if char=='/' and before.endswith('???') and not after:
        return True
            



    if not in_string_or_comment:#This is just for visual purposes, so I can put the lines in a block of code and document ,after_line)it
      #region ..= and =.. in-place operators
        if char=='.' and before_line.endswith('=.') and not ' ' in before_line.strip() and before_line.count('=.')==1 and not before_line.endswith('==.') and not before_line.endswith('!=.'):
            #The '=..' in-place operator
            #On '.': right=.| --> right=|.right
            #`right=..cursor` —>  `right=cursor.right`
            varname=before_line[:-2]
            varname=varname.strip()
            buffer.insert_text(varname)
            buffer.cursor_left(len(varname)+1)
            return True
        if char=='=' and before_line.endswith('..'):
            #The '..=' in-place operator
            #On '=': cursor..| --> cursor.|=cursor
            #`cursor..=right` —>  `cursor.right=cursor`
            varname=before_line[:-2]
            varname=varname.strip()
            buffer.delete_before_cursor()
            buffer.insert_text(varname)
            buffer.cursor_left(len(varname))
            buffer.delete_before_cursor()
            buffer.insert_text('.=')
            buffer.cursor_left()
            return True
      #endregion

      #region pluralize list comprehension (must come before space stoppers)
        if char==' ' and (starts_with_any(after_line,']',':')) and re.fullmatch(r'((.* for)|(for)) [a-zA-Z_0-9]+ in ',before_line):
            #[thing(index) for index in |] --->  [thing(index) for index in indices|] #TO BE IMPROVED LATER. THIS IS JUST A PROOF OF CONCEPT RIGHT NOW.
            name=before_line.rstrip().split(' ')[-2]
            from rp import plural_noun,is_singular_noun_of,is_iterable,is_plural_noun,plural_noun
            refresh_strings_from_buffer()
            candidates=set(list(ric.globa)) | set(split_python_tokens(before+after))
            plural_name=plural_noun(name)
            if plural_name in candidates:#If this succeeds it makes the next loop a lot faster...
                buffer.insert_text(plural_name)
                return True
            for candidate in candidates:#Search all existing known names looking for a plural match to the iterator variable
                focus_name=name
                if not is_namespaceable(candidate) or candidate[:2]!=name[:2]:
                    continue#Speed things up
                if is_singular_noun_of(name,candidate) and is_plural_noun(candidate):
                    buffer.insert_text(plural_noun(candidate))
                    return True
            if '\n' not in text and after==']' and before.count('[')==1:
                #[x for x in |] --->  [x for x in ans|]
                buffer.insert_text('ans')
                return True
            # buffer.insert_text(plural_noun(name))#If we can't find a name that fits, and 'ans' isn't an option, just choose a plural name
            # return True 
        keywords={'async','await','with', 'nonlocal', 'while', 'None', 'global', 'as', 'is', 'and', 'else', 'yield', 'raise', 'del', 'break', 'in', 'not', 'False', 'assert', 'try', 'def', 'return', 'if', 'finally', 'lambda', 'for', 'from', 'True', 'pass', 'continue', 'elif', 'except', 'class', 'or', 'import'}
        from rp import is_namespaceable
        if char==' ' and (before_line=='for ' or before_line.endswith(' for ')) and starts_with_any(after_line,' in]','in)','in}',' in '):
            before_tokens=split_python_tokens(before_line)[:-1]#Get rid of the 'for'
            # dont_use_these_tokens=set(split_python_tokens(text))-set(before_tokens)
            for token in reversed(before_tokens):
                # if token=='[':#Technically correct but returns false negatives
                    # break#Welp..we failed to find a unique new variable...
                if is_namespaceable(token) and token not in keywords:
                    if token not in ric.globa:# and token not in dont_use_these_tokens:
                        buffer.insert_text(token)
                        buffer.cursor_right(len(' in'))
                        if not after_line.startswith(' in '):
                            buffer.insert_text(' ')
                        return True
        if char==' ' and re.fullmatch(r' *[a-zA-Z_0-9]+\(',before_line) and after_line==')':
            for line in before.splitlines()[::-1][1:]:
                if starts_with_any(line.lstrip(),*'for if while elif'.split()):
                    tokens=split_python_tokens(line.strip())
                    tokens=[token for token in tokens if is_namespaceable(token) and not token in keywords]
                    if tokens:
                        focus_name=tokens[0]
                        #ON SPACE:
                        #for focus_name in ans:
                        #   print(|)
                        #--->
                        #for focus_name in ans:
                        #   print(focus_name,)
                        buffer.insert_text(focus_name+',')
                        return True
      #endregion

      #region stopping double-spaces after 'or', 'and' etc

        if char==' ': 
            #TODO Possibly replace the below with something more useful than '_', such as the focus in the for loop or ans if there is no focus or perhaps 'True'
            if re.fullmatch(r' *for ',before_line) and re.fullmatch(r' in : *',after_line):
                #`    for | in :  `  --->  `    for _ in |:  `
                buffer.insert_text('_')
                buffer.cursor_right(len(' in '))
                refresh_strings_from_buffer()
            if re.fullmatch(r' *(if|while) ',before_line) and re.fullmatch(r': *',after_line):
                #`    if |:  `  --->  `    if _ |:  `   --->   `    if _:|  `
                #`    while |:  `  --->  `    while _ |:  `  --->  `    while _:|  `
                buffer.insert_text('_ ')
                refresh_strings_from_buffer()

        if char==' ':
            partial_correctables='or and not for if'.split(' ')
            if before_line.endswith(']') and after_line.startswith(']'):
                #  [[[]|]]  --->  [[[]]|]
                buffer.cursor_right()
                return True
            if before_line.endswith('[') and after_line.startswith('['):
                #  [[|[[]]]]  --->  [[[|[]]]]
                buffer.cursor_right()
                return True
            for c in partial_correctables:
                if before_line.strip().startswith(c+' '):
                    continue#We don't want `for f in y:` to be messed up
                if before_line.endswith(' '+c+' '+c[1:]):
                    #Leftovers from having 'a' --> 'and' or 'o'-->'or' if you just type out the whole thing
                    #AKA `a ob`-->`a or b` therefore `a or b`-->`a or rb` which is bad...this fixes that:
                    #  `a or r|` --> `a or |`
                    #  `a and nd|` --> `a and |`
                    buffer.delete_before_cursor(len(' '+c[1:]))
                    refresh_strings_from_buffer()
                    if c in 'for':
                        buffer.insert_text(' ')
                        return True#[x for or| in] --->  [x for | in]
                elif before_line.endswith(' '+c+' '):
                    return True#Do nothing
            full_correctables='return else or and not in'.split(' ')
            for c in full_correctables:
                if c=='in' and not starts_with_any(after_line,')','}',']'):
                    #This block is NOT used for list comprehension aka [x for x in in|]--->[x for x in |]
                    #It IS used for 'nin', which stands for 'not in'
                    if before_line.endswith(' '+c+' '+c):
                        if before_line.lstrip().startswith('for '):
                            buffer.delete_before_cursor(len('in'))
                            return True
                        else:
                            buffer.delete_before_cursor(len('in in'))
                            buffer.insert_text('not in ')
                            return True
                if before_line.endswith(' '+c+' '+c):
                    #`x if y else else|` ---> `x if y else |`
                    buffer.delete_before_cursor(len(' '+c))
                    refresh_strings_from_buffer()
                # elif before_line.endswith(' '+c+' '):
                    # return True#Do nothing
            if before_line.endswith(' if ') and starts_with_any(after_line,'}',')',']'):
                #[x for x in y if |] ---> [x for x in y if |]
                return True
            for keyword in 'or and not in is'.split():
                if before_line.endswith(' else '+keyword):
                    #`a=x ify and z w` ---> `a=x if y and z else w` 
                    buffer.delete_before_cursor(len(' '+keyword))
                    buffer.cursor_left(len(' else'))
                    buffer.insert_text(' '+keyword+' ')
                    return True
            for keyword in 'not in'.split():
                if before_line.endswith(keyword) and re.fullmatch(r' else(([^a-zA-Z0-9_].*)|())',after_line):
                    #a=x if not| else z   --->   a=x if not | else z
                    buffer.insert_text(' ')
                    return True
            if endswithany(before_line,' in ',' is '):
                #on space: `x in y |` --> `x in y |`
                #on space: `x is y |` --> `x is y |`
                if after_line==':':
                    buffer.insert_text('ans')
                return True
        if n_makes_in_and_s_makes_is and char=='t':
            if before_line.endswith(' in o'):
                #Because 'n' --> 'in', 'not'-->'in ot'
                #On t: ' in o|'-->' not '
                buffer.delete_before_cursor(4)
                buffer.insert_text('not ')
                return True
      #endregion

      #region spacebar to commas in lists
        #TODO: Make this much more general (beyond just lists and numbers) to move it out of the 'misc tweaks' section
        if char==' ':
            if after_line.startswith(']') and re.fullmatch(r' *[0-9]+\-? *(\, *[0-9]+\-? *)*\[ *(([^a-zA-Z\)\]].*)|())',before_line[::-1]):#If NOT used as an index but is a list of number literals)
                # if char==' ' and after_line.startswith(']') and re.fullmatch(r' *[0-9]+\-? *(\, *[0-9]+\-? *)*\[ *((nruter)|[\:\,\=]|(dleiy)|(ni )).*',before_line[::-1]):#<---- Possible alternative regex to the above
                #When creating list literals with numbers and hitting space, don't add a space; add a comma.
                #This helps when copying down lists of numbers from a piece of paper onto my mac (no numpad) without having to look up to put my fingers back on the right numbers (moving them back from the comma key, which I can't use my thumb for)
                buffer.insert_text(',')
                return True
            if after_line.startswith(']]'):
                if before_line.endswith(','):
                    #On space:  [[1,2,3,|]]  --->   [[1,2,3],[|]]
                    buffer.delete_before_cursor()
                    buffer.cursor_right()
                    buffer.insert_text(',[]')
                    buffer.cursor_left()
                    return True
                if after_line.startswith(']]]') and before_line.endswith(',['):
                    #On space: [[[1,2,3],[|]]]  --->   [[[1,2,3]],[[|]]]
                    #(and then by other completions...)   on space:  [[[1,2,3]],[[|]]] -->  [[[1,2,3]],[|]]
                    buffer.delete_before_cursor(2)
                    buffer.delete()
                    buffer.cursor_right()
                    # n=re.match(r'^\]*',after_line).span()[1]#How many ]'s does the after_line start with
                    n=re.match(r'^\[\,\]*',before_line[::-1]).span()[1]-1
                    # assert n>=3#Because in the 'if' condition, after_line.startswith(']]]')
                    # n-=1
                    buffer.insert_text(','+n*'['+']'*n)
                    buffer.cursor_left(n)
                    return True
        if char==' ' and before_line.endswith('[[') and after_line.startswith(']]'):
            #On space: [[[|]]]  -->  [[|]]
            buffer.delete_before_cursor()
            buffer.delete()
            return True
        if char in ' \n*.+[)},' and re.fullmatch(r'.*\[.* +',before_line) and after_line.startswith(']'):#All the valid characters that might commonly follow a list literal
            #On space or enter key: [1,2,3, |]      --->   [1,2,3]|
            #On space or enter key: [1,2,3,     |]  --->   [1,2,3]|
            #The space between the '3,' and the ']' is important
            #For all keys except the space key, proceed as usual (don't cancel further completions)
            number_of_spaces=len(before_line)-len(before_line.rstrip())
            buffer.delete_before_cursor(number_of_spaces)
            if before_line.rstrip().endswith(','):
                buffer.delete_before_cursor()#Delete the comma
            buffer.cursor_right()
            refresh_strings_from_buffer()
            if char==' ':return True#For all keys except the space key, proceed as usual (don't cancel further completions)

      #endregion

      #region
        if char=='-':
            if re.fullmatch(r'.* for [a-zA-Z_0-9]+',before_line):
                #[x for y| in]  --->  [x for y_| in]
                buffer.insert_text('_')
                return True
            if before_line.lstrip().startswith('def ') and after_line.strip()=='):':
                try:
                    if before_tokens[-2].string==',':
                        #ON -: def f(x,y|):  -->  def f(x,y_|):
                        buffer.insert_text('_')
                        return True
                    elif before_tokens[-1].string==',':
                        #ON -: def f(x,|):  -->  def f(x,_|):
                        buffer.insert_text('_')
                        return True
                    elif before_tokens[-3].string=='def':
                        #ON -: def f(|):  -->  def f(_|):
                        buffer.insert_text('_')
                        return True
                    elif before_tokens[-4].string=='def':
                        #ON -: def f(x|):  -->  def f(x,y_|):
                        buffer.insert_text('_')
                        return True
                except IndexError:
                    #Probably an error getting some index of before_tokens. This is perfectly ok...just ignore it.
                    pass
      #endregion

      #region
        # if ,before_line_ends_with_number:
        if char==' ' and before_line_ends_with_number and after_line.startswith(']') and len(before_tokens)>=2 and before_tokens[-2].string=='[':
            #ON Space:
            # a[0|]  --->  a[0][|]
            buffer.cursor_right()
            buffer.insert_text('[]')
            buffer.cursor_left()
            return True
        if before_line.endswith('[') and after_line.startswith(']'):
            if char in '+&^%@<>/,|' or char=='=' and not (len(before_tokens)>=2 and before_tokens[-2].type==tokenize.NAME):#This last part about '=' being special is so we can have the '[=' operator
                #Intentionally did not include any '*.!~-' as they can be unary operators that go before things. + is also technically a unary operator because '+5' is a valid int, but who even does that...
                #ON +:
                # a[0][|]  --->  a[0]+|
                buffer.delete()
                buffer.delete_before_cursor()
                buffer.insert_text(char)
                return True
      #endregion

      #region
        # EXAMPLES FOR THIS SECTION:
        # {a:5}..a\n   —>   {a:5}['a'] 
        # {a:5}..a..b..c\n   —>   {a:5}[‘a’][‘b’][‘c’]
        # {a:5}..a..b..c+5\n   —>   {a:5}[‘a’][‘b’][‘c’]+5
        # L..0\n   —>   L[0]\n
        # L.123+    —>  L[123]+
        # L..123+   —>  L['123']+
        # L.0.1.2\n   —>  L[0][1][2]
        # L.-1\n    —>   L[-1]\n
        # L.1;5\n  —>  L[1:5]\n
        # L.1;5.0\n   —>  L[1:5][0]\n
        # L.0;1.0;;1.-1.0;-1.0;;-1.1;\n   —>   L[1:1][0::1][-1][0:-1][0::-1][1:]   (first is len 26, second is len33  — so this saved 7 keystrokes)
        # L.;;3\n —>  L[::3]\n
        # image.;,;,0  —>  image[:,:,0]
        # “f f x  .y”  —>  f(f(x).y)
        # “f f x  .5”  —>  f(f(x),.5)
        # “L.4[5”   —>   L[4][5]
        # “f f x  .y.0.1..a”   —>  f(f(x).y[0][1][‘a’])
        # “f f x  .5”  —>   f(f(x),.5)   BUT    “f f x  .a”  —>   f(f(x).a)    AND NOT  “f f x  .a”  —>   f(f(x)[‘a’])
        # “d f a 8b 8c”   —>  def f(a,*b,**c):
        # “i.;.;.0”  —>  i[:,:,0]
        # “i.;,;,0”  —>  i[:,:,0]
        if before_line.endswith(').') and char.isnumeric():
            #On pressing 5: f(x().|)  --->  f(x(),.5|)  (To conuter a side-effect of one of the next blocks)
            #“f f x  .y”  —>  f(f(x).y)
            #“f f x  .5”  —>  f(f(x),.5)
            buffer.delete_before_cursor()
            buffer.insert_text(',.')
            refresh_strings_from_buffer()
        if '..' in before_line:
            i=before_line.rfind('..')
            key=before_line[i+2:]#If before_line is "aido.dsodifg..sdfgoj345.f.sdfg..abcd" then key is "abcd"
            if key and not key.isnumeric():
                do_number_key=key.isnumeric() and not char.isnumeric()#Do a    a..1   --->   a[1] completion  (no quotes)
                do_string_key=is_namespaceable(key) and key and not is_namespaceable(key+char)#Do a    a..b   --->   a['b'] completion (with quotes)
                assert not do_number_key or not do_string_key,'can only do one or the other. this is internal logic this should never break. key='+repr(key)
                if do_number_key or do_string_key:
                    #Javascript-like x.y ==== x['y'] notation by using '..' instead of '.'
                    #Example: On '+' (which isn't namespaceable):   ..stuff|   --->   ..['stuff']+|
                    q="'"*do_string_key
                    buffer.insert_text(q+"]")
                    l=len(before_line)-i#Amount we have to move left#Ignore the shift caused by adding "']" because of buffer.delete_before_cursor(2)
                    buffer.cursor_left(l-do_number_key)
                    buffer.delete_before_cursor(2)
                    buffer.insert_text("["+q)
                    buffer.cursor_right(l-do_number_key)
        if '.' in before_line and char not in ',:-':
            i=before_line.rfind('.')
            key=before_line[i+1:]#If before_line is "aido.dsodifg..sdfgoj345.f.sdfg..abcd" then key is "abcd"
            before_key=before_line[:i]
            #someList.5   --->   someList[5]
            numeric_key_candidate=key.replace(':','').replace(',','').replace('-','')
            do_number_key=numeric_key_candidate.isnumeric() and not (char.isnumeric() or (char=='-' and not (key and key[-1]=='-')))#Do a    a..1   --->   a[1] completion  (no quotes)
            if char==';' and (do_number_key or not numeric_key_candidate):
                buffer.insert_text(':')
                return True
            if char=='.' and key and not numeric_key_candidate:
                #Allow for "i.;.;.0"   --->   "i.;,;,0"  -->  "i[:,:,0]"  (have to worry about one less character (can forget about the comma in this particular case. The alternative is to give an invalid completion aka 'i.;.;.0'  -->  'i.:[:,0]'))
                buffer.insert_text(',')
                return True
            if do_number_key and numeric_key_candidate and not (not before_key or endswithany(before_key,',')) and not ends_with_number(before_key):
                buffer.insert_text("]")
                l=len(before_line)-i
                buffer.cursor_left(l)
                buffer.delete_before_cursor(1)
                buffer.insert_text("[")
                buffer.cursor_right(l)
            elif char in '.\n-+*&^%#/()[]{}@<>=':
                refresh_strings_from_buffer()
               #match=re.match(r'[0-9\,\:]+\-?\.[^= ]',before_line[::-1])
               #match=re.match(r'((([0-9]+\-?)|\:)(\,([0-9]+\-?)|\:)*)\-?\.[^= ]',before_line[::-1])
                match=re.match(r'(((([0-9]+\-?)|\:)*)(\,(([0-9]+\-?)|\:)*)*)\.[^= ]',before_line[::-1])
                bad_match=bool(re.match(r'[0-9]+\.[0-9]+'         ,before_line[::-1]))\
                  and not bool(re.match(r'[0-9]+\.[0-9]+\-?[a-zA-Z_\,]',before_line[::-1]))#Not part of a variale name but we still have before_line ending with something like 34234.32423
                bad_match=bad_match or\
                          bool(re.match(r'[0-9]+\.[0-9]*\-'       ,before_line[::-1]))
                bad_match=bad_match or before_line.endswith('.')
                if match and not bad_match and not re.fullmatch(r'.*[^\)\]a-zA-Z_\'\"][0-9]+',before_line) and\
                             not re.fullmatch(r'.*[0-9]+\,\w*',before_line):#To fix ‹[.5,.›  -/->  ‹[[.5,].|]›
                    double_dot=bool(re.match(r'[0123456789\,\:]+\.\.',before_line[::-1]))
                    start,end=match.span()#Number of digits
                    assert start==0
                    assert end>1
                    buffer.cursor_left(end)
                    buffer.delete_before_cursor()
                    if double_dot:buffer.delete_before_cursor()#;print('\n',end)# x.1.2..3.  -->  x[1][2]['3'].;
                    else:pass#x.1.2.3.4.5.   --->   x[1][2][3][4][5].
                    buffer.insert_text('[')
                    if double_dot:buffer.insert_text("'")
                    buffer.cursor_right(end)
                    if double_dot:buffer.insert_text("'")
                    buffer.insert_text(']')
                    refresh_strings_from_buffer()

        if char in '&^+/%|' and before_line.endswith(',') and not get_if_in_string_or_comment(before_line,after_line,buffer):#Not '-' because '-' can be a prefix for a number
            #Note: < and > purposely excluded because they're commands to swap arguments etc
            #On +: f(x,y,z,|)  --->  f(x,y,z+|)
            #“f f x  .y”  —>  f(f(x).y)
            #“f f x  .5”  —>  f(f(x),.5)
            buffer.delete_before_cursor()
            # return False#We should keep going if there are any other completions that could have been trigggered by this
        if char.isalpha() and before_line.endswith(',.'):
            #On y: f(x,.|)  --->  f(x.y|)
            buffer.cursor_left()
            buffer.delete_before_cursor()
            buffer.cursor_right()
        if char==',' and before_line.endswith('(') and after_line.startswith(')'):
            #Spacebar makes f(g(|)) --> f(g,)
            #So, on ',': f(g(|))  -->  f(g(),)
            buffer.cursor_right()
        if char.isalpha() and not after_line.strip() and before_line.lstrip()=='2':
            #Don't need to press shift to make the @ decorator symbol
            #Example:
            #'2memoized\ndf ' --->   '@memoized\ndef f():'
            buffer.delete_before_cursor()
            buffer.insert_text('@')
        if char.isalpha() and before_line.endswith('=.'):
            #fixed the i=.5 which autocompleted to i.5=5, which is not what we want because 5 is a numeric key
            # On press 'w' for example:
            # self=.|   --->   self.w|=  --->  self.w|=w   (and then type foo to get self.foo=foo)
            buffer.delete_before_cursor()
            buffer.cursor_left()
            buffer.insert_text('.')
            refresh_strings_from_buffer()

      #endregion

      #region async and await
        if char==' ' and before_line.lstrip in ('async','await') and not after_line.strip():
            buffer.insert_text(' ')
            return True
      #endregion


      #region misc tweaks

        if char=='\n' and not after_line and before_line.endswith(':'):
            buffer.insert_text('\n'+get_indent(before_line)+'    ')
            return True
        if char=='=' and before_line.endswith('.') and after_line.strip():
            #`if x.=5`   -->  `if x>=5|:`
            buffer.delete_before_cursor()
            buffer.insert_text('>')
            refresh_strings_from_buffer()
        if char=='=' and before_line.endswith(',') and after_line.strip():
            #NOTE This is a stylistic, heuristic choice. Technically, 'if x,=y:' is valid syntax. However, I find that I rarely ever do that. On the flip side, I do `if x<=y` much more often.
            #`if x,=5`   -->  `if x<=5|:`
            buffer.delete_before_cursor()
            buffer.insert_text('<')
            refresh_strings_from_buffer()

        if char=='\n':
            #A tweak meant to make ]= and )= operators betters
            if re.fullmatch(r'[^\=]+\=[^\=]+',before_line) and \
               after_line.startswith('(') or after_line.startswith('['):
              #We're on the right-hand-side of some assignment...  
                buffer.cursor_right(999999)#`i)=5\n`  -/->  `i=i\n|(5)` INSTEAD `i)=5\n`  --->  `i=i(5)\n|`
            refresh_strings_from_buffer()
        if char==' ' and re.fullmatch(r'.*[\,\(](and|or|not|nin|in|is)',before_line):
            #With function f: `f x and y` -/->  `f(x,and,y)
            #With function f: `f x and y` --->  `f(x and y)
            #Same goes for and,or,not,in,is,etc...
            for kw in 'and or not nin in is'.split():
                if before_line.endswith(kw):
                    if kw != 'not':
                        buffer.cursor_left(len(kw))
                        refresh_strings_from_buffer()
                        if not before_line.endswith('('):
                            buffer.delete_before_cursor()
                            buffer.insert_text(' ')
                        buffer.cursor_right(len(kw))
                    buffer.insert_text(' ')
                    if kw=='nin':
                        buffer.delete_before_cursor(len('nin '))
                        buffer.insert_text('not in ')
                    if kw=='isnt':
                        buffer.delete_before_cursor(len('isnt '))
                        buffer.insert_text('is not ')
                    return True
        if char==' ' and re.fullmatch(r'.*[^\w]is nt',before_line):
            #isn't ---> is not 
            #`x isnt y`  -->  `x is not y|`
            buffer.delete_before_cursor(len('is nt'))
            buffer.insert_text('is not ')
            return True
        if char in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_':
            if not after:
                if before=='5':
                    #`5edit` --->  `%edit` #For ipython magics, turn 5 into % if at the beginning of a line
                    buffer.delete_before_cursor()
                    buffer.insert_text('%')
                elif before=='55':
                    #`55edit` --->  `%%edit` #For ipython magics, turn 5 into % if at the beginning of a line
                    buffer.delete_before_cursor(2)
                    buffer.insert_text('%%')
        if char in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[({_' and re.fullmatch(r'.*[^a-zA-Z_0-9]1',before_line):
            if char!='j':#1j is a valid literal. Don't destroy it.
                #Interperet ! or 1 as 'not '
                #`x f1y z` --->  `x if not y else z`
                buffer.delete_before_cursor()
                buffer.insert_text('not ')
        if char in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_({[\'"':
            #8 to * in function calls and lists etc
            if re.fullmatch(r'.*[\(\[\{\,] *8',before_line):
                buffer.delete_before_cursor()
                buffer.insert_text('*')
                refresh_strings_from_buffer()
            elif re.fullmatch(r'.*[\(\[\{\,] *88',before_line):
                buffer.delete_before_cursor(2)
                buffer.insert_text('**')
                refresh_strings_from_buffer()
        if char in '"\'' and re.fullmatch(r'.*\*',before_line) and re.fullmatch(r'[\]\}\)]',after_line):
            #auto Double quotes. Dont know where the other part in this code is and I'll make this more coherent later.
            buffer.insert_text(char)
            buffer.cursor_left()
            buffer.insert_text(char)
            return True
        if char=='-':
            if re.fullmatch(r'( )*for [a-zA-Z_]+',before_line):
                #`   for abc|`  --->   `   for abc_|`
                buffer.insert_text('_')
                return True
            if re.fullmatch(r' *(from |import ).*',before_line):
                #import thingy-5 as stuff-6   --->  import thingy_5 as stuff_6
                buffer.insert_text('_')#`from itertools import product as cartesian-` should do _ instead of -
                return True
        if char=='\n' and '\n' not in before and '\n' in after:
            #Fixing a bug in a hacky way: Don't enter commands if our cursor is on the first character and we're multi-line
            buffer.insert_text('\n')
            return True
        if char=='\n' and text=='ans[]' and after_line==']':
            #THIS IS BROKEN
            #TODO: Why does this never get triggered?
            #Space -->  ans[|]  -->  ans\n   (when we just want to see the answer but hitting space tries to index an array)
            buffer.delete()
            buffer.delete_before_cursor()
        if char in '.\n' and re.fullmatch(r'[a-zA-Z_]+\=(\/)+',current_line) and after_line=='':
            #On hitting enter, `torch=/`  -->  `torch?`
            #On hitting enter, `torch=//`  -->  `torch??`
            #On hitting enter, `torch=///`  -->  `torch???`
            #On hitting enter, `torch=////`  -->  `torch????`
            #Because `import torch\n=/\n` shows help for torch
            # print("AOSD")
            I=0
            for c in reversed(before_line):
                if c!='/':
                    break
                I+=1

            buffer.delete_before_cursor(len('=')+I)
            buffer.insert_text('?'*I)
        if char=='\n' and after=='' and before_line.endswith(';'):
            #Insert a new line if we end with ';' to make life easier
            #on '\n': `single_line_stuff();|`  --->  `single_line_stuff()\n|`
            buffer.delete_before_cursor()
            buffer.insert_text('\n')
            return True
        if (char!='=' and re.fullmatch(r'.*\=',before_line) and not re.fullmatch(r'.*\=\=',before_line) and starts_with_any(after_line,']') and not (len(after_line.strip())==2 and after_line.strip()[1]==':')) and not endswithany(before_line,'==','1=','!='):
            #On a letter or number 'q':  i[w=|]  -->  i[w]=q
            if before_line.endswith('>=') or before_line.endswith('<='):
                buffer.insert_text(char)
                return
            buffer.delete_before_cursor()
            buffer.cursor_right()
            buffer.insert_text('=')
        any_keyword_regex=r'False|class|finally|is|return|None|continue|for|lambda|try|True|def|from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|else|import|pass|break|except|in|raise'
        if char=='=' and     re.fullmatch(r'.*([^\+\-\(\[\,\/\@\%\^\&\*\~\<\>\=]|(([a-zA-Z_0-9]*) +))1',before_line) \
                     and not re.fullmatch(r'.*('+any_keyword_regex+r') +1',before_line)\
                     and not re.fullmatch(r'\s*\w+',before_line):#we don't want h1=5 to turn into h!=5
            #`x 1=y` -->  'x !=y'
            #TODO: Check to make sure that variable x1 is not in the text, nor is it in globa scope. Then we can be sure we meant to use != instead of ==, and that it is not just a number literal (we don't want 21=  to 2!=)
            buffer.delete_before_cursor()
            buffer.insert_text('!=')
            return True
        if char==' ' and re.fullmatch(r' *(from |import ).*',before_line) and after_line.strip().startswith('#'):
            buffer.insert_text(' ')#FIX: on space: `import x as y#Comment|` —> `import x as y#Comment|, ` 
            return True
        for kw in 'return break yield continue assert'.split():
            if char==' ' and not after_line.strip() and re.fullmatch(r" *(for|while|if|with|try|def|elif|else|except|finally)(( .*\:)|( *\:)) *("+splinterify(kw)+")",before_line):
                assert so_far(before_line) in kw,'Internal logical assertion should never fail'
                buffer.insert_text(kw[len(so_far(before_line)):])
                refresh_strings_from_buffer()
                #on space: `if x:re`         -->  `if x:return|`  -->  `if x:return |`
                #on space: `if x:y`          -->  `if x:yield|`   -->  `if x:yield |`
                #on space: `with x as y:con  -->  `if x:return|`  -->  `if x:continue |`
        if char==' ' and re.fullmatch(r'.*[\(\[\, ]\-',before_line):
            #if -|:   --->   if _ |:
            #print(-|)   --->   print(_,|)
            #print(_,-|)   --->   print(_,_|)
            buffer.delete_before_cursor()
            buffer.insert_text('_')
            refresh_strings_from_buffer()
        if char=='\n' \
             and before_line.endswith('-')\
             and (re.fullmatch(r' *[^\w\(\{].*',after_line) or not after_line.strip())\
             and re.fullmatch(r'(\s*)|(.*[^\w\s]\s*\-)',before_line):
            #On \n:   `[_ and -|]`  --->  `[_ and _]\n
            #On \n:   `x and -`  --->  `x and _
            #On \n:   `x+-`  --->  `x+-`
            buffer.delete_before_cursor()
            buffer.insert_text('_')
            refresh_strings_from_buffer()
        if char==' ' and re.fullmatch(' *for len',before_line) and re.fullmatch(' in : *',after_line):
            #`   for len| in :`  --->  `   for _ in range(len(|)):`
            buffer.delete_before_cursor(len('len'))
            buffer.insert_text('_')
            buffer.cursor_right(len(' in '))
            buffer.insert_text('range(len())')
            buffer.cursor_left(len('))'))
            return True
        if char in 'p' and meta_pressed(clear=True):
            run_arbitrary_code_without_destroying_buffer('PREV',event,put_in_history=True)
            return True
        if char in 'n' and meta_pressed(clear=True):
            run_arbitrary_code_without_destroying_buffer('NEXT',event,put_in_history=True)
            return True
        if char in '{([])}' and meta_pressed(clear=False):
            #When holding alt, add a ) or ] or } to the end of the line, instead of autocompleting it where it is currently
            #TODO: Add example
            if char in '{([':
                buffer.insert_text(char)
                char={'(':')','[':']','{':'}'}[char]
            meta_pressed(clear=True)
            # l=after_line.find(':')#In the event that we're in "for x in func(|thing:" we want "for x in func(|thing):" and not "for x in func(|thing:)"
            l=len(after_line)-1 if after_line.endswith(':') else len(after_line)
            buffer.cursor_right(l)
            buffer.insert_text(char)
            buffer.cursor_left(l+1)
            return True
        if char=='=' and re.fullmatch(r' *[\-][\)\]\.\+\*\&\%\@\>\<\/\[\(]',before_line):
            #  `-+=x`  --->     `_+=x|`
            #`  -)=f`  --->   `  _=f(_|)`
            # ` -.=x`  --->    ` _=_.x|`
            buffer.cursor_left()
            buffer.delete_before_cursor()
            buffer.insert_text('_')
            buffer.cursor_right()
        if char=='=' and re.fullmatch(r' +[\-]',before_line):
            #`if _:\n\t-=5`  --->   `if _:\n\t_=5|`
            buffer.delete_before_cursor()
            buffer.insert_text('_')
        if char=='=' and re.fullmatch(r' *\w+\(',before_line) and after_line==')':
            #Fixing the (= operator
            #`f(=x`   --->   `f=f(x|)`
            buffer.delete_before_cursor()
            buffer.delete()
            buffer.insert_text('=')
            buffer.insert_text(before_line[:-1].strip())
            buffer.insert_text('()')
            buffer.cursor_left()
            return True
        if char=='=' and before_line.endswith('-') and after_line.strip().endswith(':'):
            #   `if -=5`  --->  `if _=5:`  --->  `if _==5|:`
            buffer.delete_before_cursor()
            buffer.insert_text('_')
        if char in '<>/%^&@+[,*' and before_line.endswith('-'):
            #- is treated like _ when an syntax-breaking operator comes after it
            #`-*5` --->  `_*5`
            buffer.delete_before_cursor()
            buffer.insert_text('_')

        if char=='=' and not endswithany(before_line,'=','>','<') and after_line.strip().endswith(':') and not starts_with_any(before_line.strip(),'def '):
            if before_line.endswith('(') and after_line.startswith(')'):
                #On '=': `if f(|):` --->  `if f()==|:`
                buffer.cursor_right()
            if before_line.endswith(',') and starts_with_any(after_line,*'])}'):
                #On '=': `if f(x,|):` --->  `if f(x)==|:`
                #On '=': `if l[i,|]:` --->  `if l[i]==|:`
                buffer.delete_before_cursor()
                buffer.cursor_right()
            buffer.insert_text('==')
            return True
        if char=='=' and endswithany(before_line,'<=','>=','!='):
            #Drag the >= or <= or !=
            #`if f(x>==y`  --->  `if f(x)>=y`
            ending=before_line[-2:]
            buffer.delete_before_cursor(2)
            buffer.cursor_right()
            buffer.insert_text(ending)
            return True
        if char in '<>' and before_line.endswith(char):
            #Drag > and <
            #`if f(x>>y`  --->  `if f(x)>y`
            buffer.delete_before_cursor()
            buffer.cursor_right()
            buffer.insert_text(char)
            return True
        if char=='\n' and after_line=='):' and before_line.endswith(',') and before_line.strip().startswith('def '):
            #On enter, `def f(x,|):`  --->  `def f(x):\n\t|`
            buffer.delete_before_cursor()
        if char=='\n' and before_line.lstrip()=='d' and not after_line and in_class_func_decl(buffer):
            buffer.delete_before_cursor()
            if not '__init__' in before:
                buffer.insert_text('def __init__(self):')
            else:
                buffer.insert_text('def _(self):')
        if char=='\n' and re.fullmatch(r'\s*(from|import)\s.* as ',before_line):
            buffer.delete_before_cursor(len(' as '))
        if char.isnumeric() and before_line.endswith(' for ') and after_line.startswith(' in'):
            #[x f4  --->  [x for x in range(4|)]
            buffer.insert_text('_')
            buffer.cursor_right(len(' in'))
            buffer.insert_text(' range('+char+')')
            buffer.cursor_left()
            return True
        if char==' ' and before=='from ' and after==' import':
            #On space: `from | import`   --->   `for | in :`
            buffer.delete(len(after))
            buffer.delete_before_cursor(len(before))
            buffer.insert_text('for  in :')
            buffer.cursor_left(len(' in :'))
            return True
        if char==' ' and re.fullmatch(r'.*[^\w]not',before_line) and starts_with_any(after_line,*')]}'):
            #Patch: `print x is not y`  -/->  `print(x is not,y|)`
            #Patch: `print x is not y`  --->  `print(x is not y|)`
            buffer.insert_text(' ')
            return True
        if char==';' and after_line==')':
            #On ‹;›: ‹print(|)›  -->  ‹print();|›
            buffer.cursor_right(9999)
            buffer.insert_text(';')
            return True
        if char==' ' and before_line.lstrip()=='for ' and after_line==' in :':
            #`for | in :` --->  `for _| in :` --->  `for _ in |:`
            buffer.insert_text('_')
            buffer.cursor_right(len(' in '))
            return True
        if char in '- \n' and starts_with_any(before_line.lstrip(),'nonlocal ','global ','del '):
            #After nonlocal and global,
            if char=='-':
                #‹nonlocal -var-name› ---> ‹nonlocal _var_name›
                #  ‹global -var-name› --->   ‹global _var_name›
                buffer.insert_text('_')
                return True
            if char==' ':
                if re.fullmatch(r'.*\w',before_line):
                    # ‹nonlocal x y z› ---> ‹nonlocal x,y,z›
                    buffer.insert_text(',')
                    return True
            if char=='\n' and not after_line.strip():
                #On enter: ‹global x,y,  |›  --->  ‹global x,y\n|›
                if before_line.strip().endswith(','):
                    while before_line.strip().endswith(','):
                        buffer.delete_before_cursor()
                        refresh_strings_from_buffer()
        if char=='n' and before_line.endswith(',not i'):
            #On ‹n›: ‹print(x,not i|)›  --->  ‹print(x not in |)›
            buffer.cursor_left(len('not i'))
            buffer.delete_before_cursor()
            buffer.insert_text(' ')
            buffer.cursor_right(len('not i'))
            buffer.insert_text('n ')
            return True
        if before and char=='\n' and not after and 'print'.startswith(before) and not before in ric.globa:
            #If the variable doesn't exist and would cause an error,
            #Replace something like ‹pri› --->  ‹print(ans)›
            #Pseudo terminal does this by default without this microcompletion, but it's tidier to do it here
            buffer.delete_before_cursor(99999)
            buffer.insert_text('print(ans)')
        if (char.isalpha() or char=='_') and before in ['1','11']:
            #‹1ls› --> ‹!ls|›
            #‹11ls› --> ‹!!ls|›
            refresh_strings_from_buffer()
            buffer.delete_before_cursor(len(before))
            buffer.insert_text('!'*len(before))
        if char in '?/' and before_line.endswith('(') and after==')' and not '\n' in text:
            #On /: some_function(|) --> some_function?|
            #On ?: some_function(|) --> some_function?|
            buffer.delete_before_cursor()
            buffer.delete()
            buffer.insert_text('?')
            return True
        if char=='/' and endswithany(before_line,'??','?/','//') and not '\n' in text:
            #‹x///› ---> ‹x?/›
            #‹x////› ---> ‹x??›
            #‹x/////› ---> ‹x???›
            #‹x//////› ---> ‹x????›
            #‹x///////› ---> ‹x?????›
            if before_line.endswith('?/'):
                buffer.delete_before_cursor()
                buffer.insert_text('??')
            elif before_line.endswith('//'):
                buffer.delete_before_cursor(2)
                buffer.insert_text('?/')
            else:
                buffer.insert_text('?')
            return True
        if (char.isalpha() or char=='_') and not '\n' in text and not after and before.endswith('/.'):
            #On ‹c›: ‹np/.|›  --->  ‹np?.c|›
            #`np/.conv` --->  `np?.conv`
            buffer.delete_before_cursor(2)
            buffer.insert_text('?.')
        if char in '.([?+/*@&|\n' and before and not '\n' in before and not after and ric.current_candidates and re.fullmatch(r'[\w\.]*[\ws]+',before):
            #`np.lin.cho.geta.`  --->  `np.linalg.cholesky.__getattribute__.|`
            if not before_line.isnumeric():
                current=before_line.split('.')[-1]
                if (False or current not in ric.current_candidates) and (not char=='\n' or '.' in before_line):#If enter key, must have some . in the line to do anything
                    candidate=ric.current_candidates[0]#First autocompletion candidate
                    if not '.' in before:
                        buffer.delete_before_cursor(99999)
                    else:
                        while not before.endswith('.'):
                            buffer.delete_before_cursor()
                            refresh_strings_from_buffer()
                    buffer.insert_text(candidate)
        if char=='\n' and not '\n' in text and not after and before.endswith('/') and not before_line.endswith('?/'):
            #On \n: ‹thing/›     --->  ‹thing?\n›
            #On \n: ‹thing//›    --->  ‹thing??\n›
            #On \n: ‹thing///›   --->  ‹thing???\n›
            #On \n: ‹thing////›  --->  ‹thing????\n›
            i=0
            while before.endswith('/'):
                i+=1
                buffer.delete_before_cursor()
                refresh_strings_from_buffer()
            buffer.insert_text('?'*i)
        if char=='\n' and before_line.lstrip() in {'while ','if '} and after_line.strip()==':':
            buffer.insert_text('True')
        if char==';' and after_line.startswith('}'):
            #On ‹;›: ‹{x|}›  --->  ‹x:|›
            buffer.insert_text(':')
            return True
        if char==';' and after_line.startswith(')') and before_line.lstrip().startswith('def '):
            #On ‹;›: ‹def f(x|):›  --->  ‹def f(x:|):›
            buffer.insert_text(':')
            return True

        if char=='-' and before_line.lstrip().startswith('def ') and before_line.endswith(')') and after_line==':':
            buffer.insert_text('->')
            return True
        if (char=='-' or char=='>') and before_line.lstrip().startswith('def ') and before_line.endswith(')->') and after_line==':':
            #Do nothing
            return True

        if before=='cd' and not after and char==' ':
            #Allow 'cd thing' to be 'CD thing'
            buffer.delete_before_cursor(2)
            buffer.insert_text('CD ')
            return True

        if set(after)<=set('])}') and not '\n' in before:
            if char=='\n' and before.endswith('/'):
                # On enter:  ans[5/|]  --->  ans[5]?|
                buffer.delete_before_cursor()
                buffer.cursor_right(9999)
                buffer.insert_text('?')
                return False
            if char=='\n' and before.endswith('//'):
                # On enter:  ans[5//|]  --->  ans[5]??|
                buffer.delete_before_cursor(2)
                buffer.cursor_right(9999)
                buffer.insert_text('??')
                return False
            # if char=='/' and before.endswith('//'):
            #     # On /:  ans[5//|]  --->  ans[5]???|
            #     buffer.delete_before_cursor(2)
            #     buffer.cursor_right(9999)
            #     buffer.insert_text('???')
            #     return True
            if char=='?':
                # On ?:  ans[5|]  --->  ans[5]?|
                buffer.cursor_right(9999)
                return False
                
        
        import rp.r_iterm_comm as ric
        if char in './?=' and text=="" and ric.successful_commands:
            last_command=ric.successful_commands[-1]
            if not '\n' in last_command and not ';' in last_command:
                if last_command.startswith('from ') or last_command.startswith('import '):
                    #import numpy
                    #<on .>
                    #numpy.|
                    buffer.insert_text(last_command.split()[-1]+char)
                    if char=='=':
                        buffer.delete_before_cursor()
                    return True
                

        # if char==' ' and after_line.startswith(')') and endswithany(before_line,*'\'"'):
        #     #print('hello'|) ---> print('hello',|)
        #     #print('hello'|) -/-> print('hello' |)
        #     buffer.insert_text(',')
        #     return True




      #endregion
    return False


ans_dot_completion_string=None


def original_ptpython_load_python_bindings(python_input):
    #THIS IS NOT USED RIGHT NOW. But if this was used instead of load_python_bindings, there would be no microcompletions. Mayybe you want that? I certainly dont.
    """
    Custom key bindings.
    """
    registry = Registry()

    sidebar_visible = Condition(lambda cli: python_input.show_sidebar)
    handle = registry.add_binding
    handle = lambda *args,**kwargs:registry.add_binding(*args,post_handler=post_handler,**kwargs)
    # handle = lambda *args,**kwargs:registry.add_binding(*args,post_handler=post_handler,**kwargs)
    has_selection = HasSelection()
    vi_mode_enabled = Condition(lambda cli: python_input.vi_mode)

    @handle(Keys.ControlL)
    def _(event):
        """
        Clear whole screen and render again -- also when the sidebar is visible.
        """
        event.cli.renderer.clear()

    @handle(Keys.F2)
    def _(event):
        """
        Show/hide sidebar.
        """
        python_input.show_sidebar = not python_input.show_sidebar

    @handle(Keys.F3)
    def _(event):
        """
        Select from the history.
        """
        python_input.enter_history(event.cli)

    @handle(Keys.F4)
    def _(event):
        """
        Toggle between Vi and Emacs mode.
        """
        python_input.vi_mode = not python_input.vi_mode
        print(event.cli.vi_state)
        event.cli.vi_state.input_mode = 'vi-navigation'

    @handle(Keys.F6)
    def _(event):
        """
        Enable/Disable paste mode.
        """
        python_input.paste_mode = not python_input.paste_mode

    @handle(Keys.Tab, filter= ~sidebar_visible & ~has_selection & TabShouldInsertWhitespaceFilter())
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        event.cli.current_buffer.insert_text('    ')

    @handle(Keys.ControlJ, filter= ~sidebar_visible & ~has_selection &
            (ViInsertMode() | EmacsInsertMode()) &
            HasFocus(DEFAULT_BUFFER) & IsMultiline())
    def _(event):
        """
        Behaviour of the Enter key.

        Auto indent after newline/Enter.
        (When not in Vi navigaton mode, and when multiline is enabled.)
        """
        b = event.current_buffer
        empty_lines_required = python_input.accept_input_on_enter or 10000

        def at_the_end(b):
            """ we consider the cursor at the end when there is no text after
            the cursor, or only whitespace. """
            text = b.document.text_after_cursor
            return text == '' or (text.isspace() and not '\n' in text)

        if python_input.paste_mode:
            # In paste mode, always insert text.
            b.insert_text('\n')

        elif at_the_end(b) and b.document.text.replace(' ', '').endswith(
                    '\n' * (empty_lines_required - 1)):
            if b.validate():
                # When the cursor is at the end, and we have an empty line:
                # drop the empty lines, but return the value.
                b.document = Document(
                    text=b.text.rstrip(),
                    cursor_position=len(b.text.rstrip()))

                b.accept_action.validate_and_handle(event.cli, b)
        else:
            auto_newline(b)

    @handle(Keys.ControlD, filter=~sidebar_visible & Condition(lambda cli:
            # Only when the `confirm_exit` flag is set.
            python_input.confirm_exit and
            # And the current buffer is empty.
            cli.current_buffer_name == DEFAULT_BUFFER and
            not cli.current_buffer.text))
    def _(event):
        """
        Override Control-D exit, to ask for confirmation.
        """
        python_input.show_exit_confirmation = True

    return registry

def load_python_bindings(python_input):
    """
    Author: Ryan Burgert
    """
    registry = Registry()

    sidebar_visible = Condition(lambda cli: python_input.show_sidebar)
    # handle = registry.add_binding # <---- OLD CODE
    handle = lambda *args,**kwargs:registry.add_binding(*args,post_handler=post_handler,**kwargs)# <---- NEW CODE: Make sure post_handler is called after every keystroke
    has_selection = HasSelection()
    vi_mode_enabled = Condition(lambda cli: python_input.vi_mode)
    # microcompletions_enabled = Condition(lambda cli: True)
    microcompletions_enabled = Condition(lambda cli: getattr(python_input,'enable_microcompletions',False))

    #region Ryan Burgert Stuff
    from rp.prompt_toolkit.key_binding.input_processor import KeyPressEvent
    from rp.prompt_toolkit.document import Document
    #region Template
    def _(event):# Parenthesis completion
        #
        assert isinstance(event,KeyPressEvent)
        #
        from rp.prompt_toolkit.buffer import Buffer
        buffer=event.cli.current_buffer
        assert isinstance(buffer,Buffer)
        #
        document=buffer.document
        assert isinstance(document,Document)
        document.insert_after()
        #
        text=document.text_after_cursor
        assert isinstance(text,str)
        #
    # buffer.insert_text("(")
    # if not text or text[0] in " \t\n":
    #     buffer.insert_text(")")
    #     buffer.cursor_left(count=1)
#endregion
    for char in '''`~!@#$%^&*()-_=+[{]}\|;:'",<.>/?']''':
        def go(c):
            @handle(c,filter=~vi_mode_enabled&microcompletions_enabled)
            def _(event):
                buffer=event.cli.current_buffer
                if handle_character(buffer,c,event):return
                buffer.insert_text(c)
        go(char)
    for char in '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./':# Normal keyboard inputs
        def go(c):
            @handle(c,filter=has_selection & ~vi_mode_enabled)
            def _(event):
                buffer=event.cli.current_buffer
                if handle_character(buffer,c,event):return
                # buffer.on_text_changed+=lambda *x:buffer.save_to_undo_stack(clear_redo_stack=False)
                buffer.cut_selection()# Overwrite text if we have something selected
                buffer.insert_text(c)
        go(char)
    from rp import regex_match
    def self_dot_var_equals_var(buffer,char_to_insert=None):
        #(upon typing foo)
        #
        #class x:
        #   def __init__(foo):
        #       self.|=
        #
        #    --->
        #
        #class x:
        #   def __init__(foo):
        #       self.foo|=foo

        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        #Are we donig this shenanagin right now? (Where we do self.foo=foo, and self.bar=bar...etc)
        if not '.' in before_line:return False
        self=before_line.lstrip()[:before_line.lstrip().find('.')]
        if not (before_line.lstrip().startswith(self+'.') and after_line.lstrip().startswith('=')):
            return False

        before_var_name=before_line.lstrip()[len(self+'.'):]#might be blank, but that's OK
        after_var_name=after_line[1:].strip()
        # print("\nbefore_var_name="+before_var_name+', after_var_name='+after_var_name)
        out=before_var_name==after_var_name
        var_name=before_var_name#or after_name, makes no difference

        if out and char_to_insert is not None:
            if char_to_insert =='\b':
                if var_name.strip():
                    assert buffer is not None#internal logic of how you use this function
                    buffer.delete_before_cursor()
                    buffer.cursor_right(len('='+var_name))
                    buffer.delete_before_cursor()
                    buffer.cursor_left(len('='+var_name)-1)
            else:
                assert buffer is not None#internal logic of how you use this function
                buffer.insert_text(char_to_insert)
                buffer.cursor_right(len('='+var_name))
                buffer.insert_text(char_to_insert)
                buffer.cursor_left(len(char_to_insert))
                buffer.cursor_left(len('='+var_name))
        return out
    def setting_index(buffer,char):
        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        before=document.text_before_cursor
        after= document.text_after_cursor
        if regex_match(before_line,r'.*\[.*=') and after_line==']':
            #a[b=|]  --->  a[b]=|
            if before_line.endswith('=='):
                #But NOT this:
                #a[b==|]  --->  a[b=]=|
                return False
            buffer.delete_before_cursor()
            buffer.cursor_right()
            buffer.insert_text('='+char)
            return True
        return False
    @handle(';',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,';',event):return
        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        before=document.text_before_cursor
        after= document.text_after_cursor
        if after_line.startswith(']'):
            #We can avoid pressing the shift-key here:
            #L[|]  --->  L[:]
            buffer.insert_text(':')
        else:
            buffer.insert_text(';')
        return
    for char in 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_':#Letter inputs
            def go(char):
                @handle(char,filter=~vi_mode_enabled&microcompletions_enabled)
                def _(event):
                    buffer=event.cli.current_buffer
                    if handle_character(buffer,char,event):return
                    document=buffer.document
                    current_line=document.current_line
                    before_line=document.current_line_before_cursor
                    after_line=document.current_line_after_cursor
                    before=document.text_before_cursor
                    after= document.text_after_cursor
                    if self_dot_var_equals_var(buffer,char) or setting_index(buffer,char):
                        return
                    token,name,found=token_name_found_of_interest(before_line)
                    # print(token,repr(name),found)
                    if (found and name in ('9','9j','9J') or name=='') and endswithany(before_line,'j','J','9'):
                        if not (before_line.endswith('9') and char in 'jJ'):#9j is a legit imaginary literal. That's an edge case...
                            #Tokens can't start with a digit and end with a letter. 
                            #So, because of that, we can start a () region by using the 9 key without holding shift
                            #(Later we'd want to extend this to quotes, or any other breaking syntax)
                            #(on press x, for ex)    [9|]  --->   [(x|)]
                            buffer.delete_before_cursor()
                            if before_line.lower().endswith('j'):
                                buffer.delete_before_cursor()
                            buffer.insert_text('(')
                            if before_line.lower().endswith('j'):
                                buffer.insert_text(before_line[-1])
                            buffer.insert_text(char)
                            buffer.insert_text(')')
                            buffer.cursor_left()
                            return
                    def writing_namespace_breaks_syntax(before_line):
                        return endswithany(before_line,' ',#This is like [x |for] (space to the left of |)
                            ')',']','}',*'1234567890','"',"'")#All of these are breaking syntax...
                    might_be_in_string_or_comment='"' in before_line and after_line.count('"')==before_line.count('"') or \
                                       "'" in before_line and after_line.count("'")==before_line.count("'") or \
                                       '#' in before_line
                    keywords={'with', 'nonlocal', 'while', 'None', 'global', 'as', 'is', 'and', 'else', 'yield', 'raise', 'del', 'break', 'in', 'not', 'False', 'assert', 'try', 'def', 'return', 'if', 'finally', 'lambda', 'for', 'from', 'True', 'pass', 'continue', 'elif', 'except', 'class', 'or', 'import', 'async', 'await'}
                    if before_line.strip() and not might_be_in_string_or_comment:
                        if not starts_with_any(before_line.lstrip() , 'from ','import '):
                            i_triggers_ifelse=False
                            if True:
                                # if writing_namespace_breaks_syntax(before_line) and char=='i' and i_triggers_ifelse and not endswithany(before_line.rstrip(),'else',*(keywords-{'True','False'})):
                                #     buffer.insert_text('if  else')
                                #     buffer.cursor_left(len(' else'))
                                #     return
                                # if endswithany(before_line,']i',')i','}i','"i',"'i",' i') and char=='f' or char=='i':
                                if before_line.endswith('i') and writing_namespace_breaks_syntax(before_line[:-1]) and char=='f' and not (endswithany(before_line[:-1].rstrip(),*(keywords-{'True','False'}))) or \
                                           i_triggers_ifelse and writing_namespace_breaks_syntax(before_line     ) and char=='i' and not (endswithany(before_line     .rstrip(),*(keywords-{'True','False'}))):
                                    #Ternary completion
                                    # if writing_namespace_breaks_syntax(before_line[:-1]):
                                        flag=True
                                        if char=='i':
                                            buffer.insert_text('i')
                                        if char=='f':
                                            if not before_line[:-1].strip():
                                                #We don't want to complete 'if | else' on an empty line where we want 'if |:'
                                                flag=False
                                        if flag:
                                            buffer.insert_text('f ')
                                            if not (starts_with_any(after_line.strip(),']','}') and 'for' in before_line):#This is an imperfect, sloppy check to see if we're in a list comprehension and we want 'x for x in y if z' instead of 'x for x in y if z else'
                                                 buffer.insert_text(' else')
                                                 buffer.cursor_left(len(' else'))
                                            return
                                if before_line.endswith('i') and char=='n':
                                    #Add space after writing 'in'
                                    if before_line.strip()!='i':#A blank line starting with 'in' generally is bad
                                        if re.fullmatch(r'^.*[a-zA-Z_0-9\)\}\]\'\"] +i',before_line):
                                            if not (before_line.endswith(' i') and endswithany(before_line[:-2],*(set(keywords)-{'True','False','not'}))):
                                                if writing_namespace_breaks_syntax(before_line[:-1]):
                                                    buffer.insert_text('n ')
                                                    return

                                if before_line.endswith('i') and char=='s':
                                    #Add space after writing 'is'
                                    if before_line.strip()!='i':#A blank line starting with 'in' generally is bad
                                        if re.fullmatch(r'^.*[a-zA-Z_0-9\)\}\]\'\"] +i',before_line):
                                            if not (before_line.endswith(' i') and endswithany(before_line[:-2],*(set(keywords)-{'True','False'}))):
                                                if writing_namespace_breaks_syntax(before_line[:-1]):
                                                    buffer.insert_text('s ')
                                                    return
                                # if char=='f':
                                #     if writing_namespace_breaks_syntax(before_line) and starts_with_any(after_line,')','}',']') and not endswithany(before_line.rstrip(),' in','if'):
                                #         #Attempt Comprehension autocompletion
                                #         #[x |]  --->  [x for | in]
                                #         #[(a,b)|]  --->  [(a,b)for | in]
                                #         if re.fullmatch(r'^.*[a-zA-Z_\)\}\]\'\"] +',before_line):
                                #             if not endswithany(before_line.rstrip(),*(' '+x for x in keywords)):
                                #                 buffer.insert_text('for  in')
                                #                 buffer.cursor_left(len(' in'))
                                #                 return
                                if char in 'fi':
                                    if writing_namespace_breaks_syntax(before_line) and starts_with_any(after_line,')','}',']') and not endswithany(before_line.rstrip(),' in','if'):
                                        #Attempt Comprehension autocompletion
                                        #[x |]  --->  [x for | in]
                                        #[(a,b)|]  --->  [(a,b)for | in]
                                        if re.fullmatch(r'^.*(([a-zA-Z_0-9] +)|([\)\}\]\'\"] *))',before_line):
                                            if not endswithany(before_line.rstrip(),*(' '+x for x in keywords)):
                                                if not re.fullmatch(r'.*for [^\[\(\{]+ in [^\[\(\{]+ ',before_line):
                                                    if char=='f':
                                                        if not before_line.endswith(' '):
                                                            buffer.insert_text(' ')#For the sake of aesthetics, [[x] for x in y] looks better than [[x]for x in y]
                                                        buffer.insert_text('for  in')
                                                        buffer.cursor_left(len(' in'))
                                                        return
                                                else:
                                                    #On press i or f: [x for x in y |] ---> [x for x in y if |]
                                                    buffer.insert_text('if ')
                                                    # buffer.cursor_left(len(' else'))
                                                    return
                                if char=='f':
                                    #f-->if
                                    if re.fullmatch(r'^.*[a-zA-Z_0-9\)\}\]\'\"] +',before_line):
                                        #x=x f|   --->   x=x if | else
                                        if not endswithany(before_line.strip(),*keywords):
                                            if not before_line.endswith(' for ')and not after_line.endswith(' in'):
                                                if not re.match(r'\w.*',after_line):
                                                    buffer.insert_text('if  else')
                                                    buffer.cursor_left(len(' else'))
                                                    return



                            if  not endswithany(before_line.rstrip(),*(keywords-{'True','False','and','or','not'})) and writing_namespace_breaks_syntax(before_line):
                                if not endswithany(before_line.rstrip(),*(keywords-{'not','True','False'})):
                                    if  not endswithany(before_line.rstrip(),*(keywords-{'True','False'})):
                                        if re.fullmatch(r'^.*[a-zA-Z_0-9\)\}\]\'\"] +',before_line):
                                            if char=='o':
                                                buffer.insert_text('or ')
                                                return
                                            if char=='a':
                                                buffer.insert_text('and ')
                                                return
                                # if not endswithany(before_line.rstrip(),*(keywords-{'and','or'})):
                                #     if char=='t':
                                #         buffer.insert_text('not ')
                                #         return
                                # TODO CORRECTION: 't' --> 'not ' should NOT be handled here, this should be handled as a space completion instead. I'll do that later...
                                # n_makes_in_and_s_makes_is=True#This is imperfect and got annoying
                                if n_makes_in_and_s_makes_is:#This completion is a real trouble-maker for edge cases...
                                    if char=='n' or char=='s':
                                        if before_line.strip() and not (before_line.endswith(' ') and endswithany(before_line[:-1],*(set(keywords)-{'not','True','False'}))):
                                            if re.fullmatch(r'.*[\]\}\)\'\"a-zA-Z0-9_] *',before_line):
                                                if not re.fullmatch(r'.*[^a-zA-Z0-9_](if|and|or|not|while|with|else|elif|is|yield) ',before_line):#prevent: return x if not negative  ——> return x if not in egative| else
                                                    if not re.fullmatch(r'[0-9]+[a-zA-Z_].*',before_line[::-1]):#Prevent: nuts2nuts  —>  nuts2 in uts
                                                        buffer.insert_text('in ' if char=='n' else 'is ')
                                                        return

                    if char=='m' and meta_pressed(clear=True):
                        # ⌥ + m ---> MORE
                        # ⌥ + m twice ---> MMORE
                        if before_line=='MORE':
                            buffer.cursor_left(4)
                            buffer.insert_text('M')
                            buffer.cursor_right(4)
                            return
                        if before_line=='':
                            buffer.insert_text('MORE')
                            return
                        if before_line=='MMORE':
                            buffer.cursor_left(4)
                            buffer.delete_before_cursor()
                            buffer.cursor_right(4)
                            return
                    if True:#not '"' in after_line and not "'" in after_line:
                        #Jump cursor to headers with special commands following the '\' key
                        #(on press d)
                        #def f():
                        #   return\|
                        #   --->
                        #|def f():
                        #   return
                        def jump_cursor_to_beginning_of_header(command:str='\\db',header:str='def '):
                            if before_line.endswith(command):
                                blines=before.splitlines()[:-1]
                                if any(x.lstrip().startswith(header)for x in blines):
                                    cline=lambda:buffer.document.current_line
                                    buffer.cursor_up()
                                    while not cline().lstrip().startswith(header):
                                        buffer.cursor_up()
                                        buffer.cursor_left(99999)
                                    buffer.cursor_right(99999)
                                    buffer.cursor_right(len(get_indent(cline())))
                                    return
                        # header_jump_commands={
                        #                  '\\db':'def ',
                        #                  '\\cl':'class ',
                        #                  '\\if':'if ',#go ...etc
                        #                  '\\wh':'while ',
                        #                  '\\wi':'with ',
                        #                  '\\fo':'for ',#go f
                        #                  '\\el':'el'}#go e
                        header_arg_commands={
                                             '\\re':'replace',
                                             '\\py':'python',
                                             '\\dtl':'delete to line',
                                             '\\go':'goto',
                                             '\\lo':'load',
                                             '\\sa':'save',
                                             '\\wr':'write',
                                             '\\ca':'cancel',
                                             '\\t3pa':'tmux_comment_paste',
                                             '\\3tpa':'tmux_comment_paste',
                                             '\\3an':'comment_ans',
                                             '\\/c':'source_code',
                                             '\\?c':'source_code',
                                             }
                        header_commands={
                                         '\\sim':'sort_imports',
                                         '\\bla':'black',
                                         '\\sg':'save_gist',
                                         '\\lg':'load_gist',
                                         '\\co':'copy',
                                         '\\pa':'paste',
                                         '\\3pa':'comment_paste',
                                         '\\vpa':'vim_paste',
                                         '\\vspa':'vim_string_paste',
                                         '\\vco':'vim_copy',
                                         '\\tpa':'tmux_paste',
                                         '\\tspa':'tmux_string_paste',
                                         '\\tco':'tmux_copy',
                                         '\\lpa':'local_paste',
                                         '\\lspa':'local_string_paste',
                                         '\\wpa':'web_paste',
                                         '\\wspa':'web_string_paste',
                                         '\\rpr':'repr',
                                         '\\rpa':'repr ans',
                                         '\\wco':'web_copy',
                                         '\\ed':'editor',
                                         '\\vi':'vim',
                                         '\\al':'align_lines',
                                         '\\ac':'align_char',
                                         '\\sw':'strip_whitespace',
                                         '\\sc':'strip_comments',
                                         '\\mla':'multi line arguments',
                                         '\\fo':'for',
                                         '\\fi':'import_from_swap',
                                         '\\de':'def',
                                         '\\wh':'while',
                                         '\\da':'delete all',
                                         '\\lss':'LSS',
                                         '\\lsr':'Relative LSS',
                                         '\\an':'ans',
                                         '\\san':'string ans',
                                         '\\tbp':'toggle_big_parenthesis',
                                         '\\spa':'string_paste',
                                         '\\d0l':'delete_empty_lines',
                                         '\\dtt':'delete_to_top',
                                         '\\dtb':'delete_to_bottom',
                                         '\\sl':'sort_lines',
                                         '\\rl':'reverse_lines',
                                         '\\ya':'yapf autoformat',
                                         '\\gg':'go to top',
                                         '\\GG':'go to bottom',
                                         '\\vO':'vim open up',
                                         '\\vo':'vim open down',
                                         '\\fn':'function_name',
                                         '\\tts':'tabs to spaces',
                                         '\\23p':'python_2_to_3',
                                         '\\db':'debug',
                                         '\\pu':'pudb',
                                         '\\wi':'workingindex',
                                         '\\en':'enumerate',
                                         }
                        # header_commands.update(header_jump_commands)
                        header_commands.update(header_arg_commands)

                        for command,header in header_commands.items():
                            key=command[-1]
                            chopped_command=command[:-1]
                            if before_line.endswith(chopped_command) and char==key:
                                buffer.delete_before_cursor(len(chopped_command))
                                # if command in header_jump_commands:
                                #     jump_cursor_to_beginning_of_header(chopped_command,header)
                                if command in header_arg_commands and '`' in before_line:
                                    if header=='replace':
                                        #DEMO: Type
                                        #`foo`bar\r
                                        #into the buffer (with a whole bunch of foo's which will be turned into bar's')
                                        if before_line.count('`')==2:#dumb assumption im makin
                                            arg1=before_line.split('`')[1]
                                            arg2=before_line.split('`')[2].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg1+'`'+arg2+'`'))
                                            text=buffer.document.text.replace(arg1,arg2)
                                            buffer.document=Document(text,buffer.document.cursor_position,buffer.document.selection)
                                    if header=='cancel':
                                        #Cancel whatever command you've written and delete it. Beats having to delete it manually.
                                        if before_line.count('`')==2:#dumb assumption im makin
                                            arg1=before_line.split('`')[1]
                                            arg2=before_line.split('`')[2].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg1+'`'+arg2+'`'))
                                        if before_line.count('`')==1:#give a lambda that takes one argument
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                    if header=='python':
                                         #DEMO: Type        
                                         #`lambda x:x.replace('foo','bar')\p
                                         #into the buffer (with a whole bunch of foo's which will be turned into bar's')
                                        if before_line.count('`')==1:#give a lambda that takes one argument
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                            text=buffer.document.text
                                            try:
                                                modifier=eval(arg,r_iterm_comm.globa);text=modifier(text);buffer.document=Document(text,buffer.document.cursor_position,buffer.document.selection)
                                            except BaseException as E:
                                                buffer.insert_text("\nERROR: "+str(E)+"\n(Undo to make me go away)\n")
                                    if header=='load':
                                        #Load a file into the buffer
                                        from rp import text_file_to_string, string_to_text_file
                                        if before_line.count('`')==1:#give a lambda that takes one argument
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                            text=buffer.document.text
                                            try:
                                                new_text=text_file_to_string(arg)
                                                buffer.document=Document(new_text,buffer.document.cursor_position,buffer.document.selection)
                                            except BaseException as E:
                                                buffer.insert_text("\nERROR: "+str(E)+"\n(Undo to make me go away)\n")
                                    if header=='write':
                                        #Write a file from the buffer (without asking to overwrite)
                                        from rp import text_file_to_string, string_to_text_file
                                        if before_line.count('`')==1:#give a lambda that takes one argument
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                            text=buffer.document.text
                                            try:
                                                string_to_text_file(arg,text)
                                            except BaseException as E:
                                                buffer.insert_text("\nERROR: "+str(E)+"\n(Undo to make me go away)\n")
                                    if header=='save':
                                        #A safer alternative to write, which will create a backup file if we're overwriting it
                                        from rp import text_file_to_string  , \
                                                       string_to_text_file  , \
                                                       file_exists          , \
                                                       get_parent_directory , \
                                                       get_file_name        , \
                                                       path_join            , \
                                                       get_current_date
                                        if before_line.count('`')==1:#give a lambda that takes one argument
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            path=arg
                                            if file_exists(path):
                                                try:
                                                    file_name=get_file_name(path)
                                                    directory=get_parent_directory(path)
                                                    backup_path=path_join(directory,'.'+file_name+'.backup.'+str(get_current_date()).replace(' ','_')+'.py')
                                                    file_contents=text_file_to_string(path)
                                                    string_to_text_file(backup_path,file_contents)
                                                except BaseException as E:
                                                    buffer.insert_text('#Failed to backup file '+repr(path)+', aborting the save. (Undo to make me go away). Error: '+repr(E))
                                                    return
                                            buffer.delete_before_cursor(len(path+'`'))
                                            text=buffer.document.text
                                            try:
                                                string_to_text_file(path,text)
                                            except BaseException as E:
                                                buffer.insert_text("\nERROR: "+str(E)+"\n(Undo to make me go away)\n")
                                                
                                        header='aoisjdaosijdoiasjdaosijd' #Prevent string ans from triggering
                                        # else:
                                            # buffer.insert_text('\\sa')#For '\san' for string ans

                                    if header=='goto':
                                        if before_line.count('`')==1:
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                            text=buffer.document.text
                                            try:
                                                n=int(arg)
                                                go_to_line_number(n,buffer)
                                            except Exception as e:
                                                buffer.insert_text('\n#ERROR: '+str(e))
                                                pass
                                    if header=='delete to line':
                                        if before_line.count('`')==1:
                                            # buffer.insert_text('\n#we: ')
                                            arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(arg+'`'))
                                            text=buffer.document.text
                                            try:
                                                _i=current_line_index(buffer)+1
                                                _n=int(arg)
                                                if _n<_i:
                                                    go_to_line_number(_n,buffer)
                                                for _ in range(abs(_n-_i)+1):
                                                    delete_current_line(buffer)
                                            except Exception as e:
                                                buffer.insert_text('\n#ERROR: '+str(e))
                                                pass
                                    # if header=='delete':
                                    #     if before_line.count('`')==1:
                                    #         arg=before_line.split('`')[1].split('\\')[0]
                                    #         buffer.delete_before_cursor(len(arg+'`'))
                                    #         text=buffer.document.text
                                    #         try:
                                    #             _i=current_line_index(buffer)
                                    #             _n=int(arg)
                                    #             if n<i:
                                    #                 go_to_line_number(_n,buffer)
                                    #             for _ in range(abs(_n-_i)+1):
                                    #                 delete_current_line(buffer)
                                    #         except Exception as e:
                                    #             buffer.insert_text('\n#ERROR: '+str(e))
                                    #             pass
                                
                                if header=='load' and not '`' in before_line:
                                    from rp import text_file_to_string, string_to_text_file, input_select_file
                                    try:
                                        print(end='\033[999B\n\033[999D\n')#Move the cursor to the bottom left of the screenhttps://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
                                        arg=input_select_file(message='Please select a python file to load into the buffer')
                                        new_text=text_file_to_string(arg)
                                        buffer.document=Document(new_text,buffer.document.cursor_position,buffer.document.selection)
                                    except BaseException as E:
                                        buffer.insert_text("\nERROR: "+str(E)+"\n(Undo to make me go away)\n")
                                    event.cli.renderer.clear()#Refresh the screen
                                    event.cli.renderer.clear()#Refresh the screen
                                    event.cli.renderer.clear()#Refresh the screen
                                    
                                if header=='LSS':
                                    #LSS refers to the command 'LSS' aka 'LS SEL' in rp's pseudo_terminal.
                                    try:
                                        import rp
                                        rp.clear_terminal_screen()
                                        buffer.insert_text(repr(rp.input_select_path()))
                                    except:pass
                                    event.cli.renderer.clear()#Refresh the screen
                                    
                                if header=='Relative LSS':
                                    #LSS refers to the command 'LSS' aka 'LS SEL' in rp's pseudo_terminal.
                                    try:
                                        import rp
                                        rp.clear_terminal_screen()
                                        buffer.insert_text(repr(rp.get_relative_path(rp.input_select_path())))
                                    except:pass
                                    event.cli.renderer.clear()#Refresh the screen
                                        
                                if header=='workingindex':
                                    buffer.insert_text('#'+str(buffer.working_index))

                                if header=='debug':
                                    toggle_top_line_text(buffer,"from rp import debug;debug()\n")
                                    # toggle_bottom_line_text(buffer,"pip_import('sys').settrace(None)#Exit the debugger")#Use the default exit-the-debugger#Commented this out. THis functionality is not handled, in a better way, in patch_linecache.py
                                if header=='pudb':
                                    line="from rp import pip_import;pip_import('pudb').set_trace()"
                                    import rp
                                    if rp.currently_running_windows():
                                        line+='#WARNING: pudb crashes on windows; it\'s unix-only'
                                    line+='\n'
                                    toggle_top_line_text(buffer,line)
                                    # toggle_bottom_line_text(buffer,"pip_import('sys').settrace(None)#Exit the debugger")#Use the default exit-the-debugger#Commented this out. THis functionality is not handled, in a better way, in patch_linecache.py
                                if header=='align_lines':
                                    #Insert the alignment char that cant normally be typed on a keyboard in this app
                                    text=buffer.document.text
                                    text=align_lines_to_char(text)
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='align_char':
                                    buffer.insert_text(align_char)
                                    buffer.cursor_left()
                                if header=='strip_whitespace':
                                    text=buffer.document.text
                                    text='\n'.join(line.rstrip() for line in text.split('\n'))
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='import_from_swap':
                                    before_line=buffer.document.current_line_before_cursor
                                    after_line=buffer.document.current_line_after_cursor
                                    current_line=buffer.document.current_line
                                    buffer.delete_before_cursor(len(before_line))
                                    buffer.delete(len(after_line))
                                    buffer.insert_text(swap_from_import(current_line))
                                if header=='enumerate':
                                    def uses_enumerate(line):
                                        ans=line
                                        ans=ans.split(' in ')
                                        ans=ans[1]
                                        ans=ans.strip()
                                        ans=ans.startswith('enumerate')
                                        return ans

                                    def transform_var(line):
                                        ans=line
                                        ans=ans.split(' in ')
                                        l=ans
                                        ans=ans[0]
                                        ans=ans.strip()
                                        ans=ans[len('for '):]
                                        oldvar=ans
                                        if not ans.isalnum():
                                            ans='('+ans+')'
                                        ans=','+ans
                                        var=ans
                                        return line.replace(oldvar,var,1)
                                    def enumeratify(line):
                                        ans=line.rstrip()
                                        ans=ans[:ans.find(' in ')+len(' in ')]+'enumerate('+ans[ans.find(' in ')+len(' in '):-1]+'):'
                                        return ans
                                    before_line=buffer.document.current_line_before_cursor
                                    after_line=buffer.document.current_line_after_cursor
                                    current_line=buffer.document.current_line
                                    buffer.delete_before_cursor(len(before_line))
                                    buffer.delete(len(after_line))
                                    buffer.insert_text(swap_from_import(current_line))
                                    leading_whitespace=current_line[:len(current_line)-len(current_line.lstrip())]
                                    buffer.cursor_right(9999)
                                    buffer.delete_before_cursor(len(current_line))
                                    new_line=transform_var(enumeratify(current_line))
                                    buffer.insert_text(leading_whitespace+new_line)
                                    buffer.cursor_left(9999)
                                    buffer.cursor_right(len(leading_whitespace+'for '))

                                if header=='toggle_big_parenthesis':
                                    if not '\n' in before+after:
                                        #If has a single line, add a new line to avoid a glitch where we get too many parenthesis
                                        text=buffer.document.text
                                        buffer.document=Document(buffer.document.text+'\n',min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                    commented_parenthesizer_automator.buffer_toggle_parenthesization(buffer)
                                if header=='delete_to_top':
                                    text=buffer.document.text
                                    lineno=document.text_before_cursor.count('\n')
                                    colno=document.cursor_position_col
                                    text=text.splitlines()[lineno:]
                                    text='\n'.join(text)
                                    buffer.document=Document(text,colno-len(r'\dt'),buffer.document.selection)
                                    # buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='delete_to_bottom':
                                    text=buffer.document.text
                                    lineno=document.text_before_cursor.count('\n')
                                    colno=document.cursor_position_col
                                    text=text.splitlines()[:lineno+1]
                                    text='\n'.join(text)
                                    buffer.document=Document(text,text.rfind('\n')+colno-len(r'\dt'),buffer.document.selection)
                                    # buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='delete_empty_lines':
                                    text=buffer.document.text
                                    text='\n'.join(line for line in text.split('\n') if line.strip())
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='sort_lines':
                                    text=buffer.document.text
                                    text='\n'.join(sorted(text.split('\n')))
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='reverse_lines':
                                    text=buffer.document.text
                                    text='\n'.join(reversed(text.split('\n')))
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='strip_comments':
                                    from rp import strip_python_comments
                                    text=buffer.document.text
                                    text=strip_python_comments(text)
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='repr':
                                    #A shortcut to `repr\py
                                    text=buffer.document.text
                                    buffer.document=Document(repr(text),min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='black':
                                    from rp import pip_import
                                    try:
                                        pip_import('black')
                                        import black
                                        text=buffer.document.text
                                        text=black.format_str(text,mode=black.Mode())
                                        buffer.document=Document((text),min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                    except BaseException as e:
                                        buffer.insert_text('#sort_imports: Error: '+str(e).replace('\n',' ; '))
                                if header=='sort_imports':
                                    from rp import pip_import
                                    try:
                                        pip_import('isort')
                                        import isort
                                        text=buffer.document.text
                                        text=isort.code(text)
                                        buffer.document=Document((text),min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                    except BaseException as e:
                                        buffer.insert_text('#sort_imports: Error: '+str(e).replace('\n',' ; '))
                                if header=='source_code':
                                    #Sets ans=rp.get_source_code(current buffer)
                                    indent=''
                                    if before_line.count('`')==1:
                                        commented_arg=before_line.split('`')[1].split('\\')[0]
                                        buffer.delete_before_cursor(len(commented_arg+'`'))
                                        before_line=buffer.document.current_line_before_cursor
                                        indent=' '*(len(before_line)-len(before_line.lstrip()))
                                        text=commented_arg
                                    else:
                                        text=buffer.document.text
                                        buffer.delete_before_cursor(99999999)
                                        buffer.delete(99999999)
                                    try:
                                        item=eval(text,r_iterm_comm.globa)
                                        from rp import get_source_code
                                        code=get_source_code(item)
                                        code=code.splitlines()
                                        code=code[::-1]
                                        code[:-1]=[indent+line for line in code[:-1]] 
                                        code=code[::-1]
                                        code='\n'.join(code)
                                        # buffer.document=Document(code,min(len(code),buffer.document.cursor_position),buffer.document.selection)
                                        buffer.insert_text(code)
                                    except BaseException as e:
                                        buffer.insert_text('#get_source_code: Error: '+str(e).replace('\n',' ; '))
                                if header=='save_gist':
                                    #Sets ans=str(current buffer)
                                    text=buffer.document.text
                                    text=repr(text)
                                    text='from rp import save_gist;ans=save_gist(%s)'%text
                                    run_arbitrary_code_without_destroying_buffer(text,event,put_in_history=True)#To include or not to include...which one??
                                if header=='load_gist':
                                    from rp import load_gist
                                    text=buffer.document.text
                                    try:
                                        try:
                                            text=load_gist(text)
                                        except Exception:
                                            text='git.io/'+text
                                            text=load_gist(text)
                                    except Exception:
                                        text='#Failed to load gist at specified url'
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='repr ans':
                                    #Sets ans=str(current buffer)
                                    text=buffer.document.text
                                    text=repr(text)
                                    run_arbitrary_code_without_destroying_buffer(text,event,put_in_history=True)#To include or not to include...which one??
                                if header=='tabs to spaces':
                                    text=buffer.document.text
                                    text=text.replace('\t','    ')
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='function_name':
                                    #Insert the current function's name
                                    func_names=get_all_function_names(buffer.document.text_before_cursor)
                                    buffer.insert_text(func_names[-1] if func_names else '')
                                if header=='python_2_to_3':
                                    text=buffer.document.text
                                    from rp import python_2_to_3
                                    text=python_2_to_3(text)
                                    buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                if header=='while':
                                    text=buffer.document.text
                                    text='while True:\n'+'\n'.join(['    '+line for line in text.split('\n')])
                                    buffer.document=Document(text,10,buffer.document.selection)
                                if header=='for':
                                    text=buffer.document.text
                                    text='for  in :\n'+'\n'.join(['    '+line for line in text.split('\n')])
                                    buffer.document=Document(text,4,buffer.document.selection)
                                if header=='def':
                                    text=buffer.document.text
                                    text='def ():\n'+'\n'.join(['    '+line for line in text.split('\n')])
                                    buffer.document=Document(text,4,buffer.document.selection)
                                if header=='go to top':
                                    buffer.cursor_up(1000000)
                                if header=='go to bottom':
                                    buffer.cursor_down(1000000)
                                if header=='vim open down':
                                    buffer.delete_before_cursor()
                                    buffer.cursor_up()
                                    buffer.cursor_right(1000000)
                                    buffer.insert_text('\n'+get_indent(current_line))
                                if header=='vim open up':
                                    buffer.delete_before_cursor()
                                    buffer.cursor_left(1000000)
                                    buffer.insert_text('\n')
                                    buffer.cursor_up()
                                    buffer.insert_text(get_indent(current_line))
                                if header=='multi line arguments':
                                    #Meant to split a def(x,y,z,w,asd,as,das,d,asd,aoisdaiosdiasidasd,as,d,asd,a,sd,as,da,sd,as,da,sd,asd,): onto multiple lines to make it more readable. see split_def_arguments_into_multiple_lines's documentation for an example.
                                    before_line=before_line[:-3]#get rid of the \ml
                                    buffer.delete_before_cursor(len(before_line))
                                    buffer.delete(len(after_line))
                                    # print("\n\n\n"+before_line+after_line+'\n\n\n')
                                    new_def=split_def_arguments_into_multiple_lines(before_line+after_line)
                                    # print("THEN")
                                    # print("\n\n\n"+new_def+'\n\n\n')
                                    # print("END")
                                    # print(new_def)
                                    buffer.insert_text(new_def)
                                if header=='local_copy':
                                    import rp
                                    do_local_copy(buffer.document.text)
                                if header=='vim_copy':
                                    import rp
                                    do_vim_copy(buffer.document.text)
                                if header=='tmux_copy':
                                    import rp
                                    do_tmux_copy(buffer.document.text)
                                if header=='web_copy':
                                    import rp
                                    do_web_copy(buffer.document.text)
                                if header=='copy':
                                    import rp
                                    do_copy(buffer.document.text)
                                if header=='editor':
                                    text=buffer.document.text   
                                    try:
                                        from rp import pip_import
                                        editor=pip_import('editor')
                                        text=editor.edit(contents=text,use_tty=True,suffix='.py').decode()
                                        buffer.document=Document(text,min(len(text),buffer.document.cursor_position),buffer.document.selection)
                                        event.cli.renderer.clear()#Refresh the screen
                                    except ImportError:
                                        buffer.insert_text("#ERROR: Cannot import 'editor'. Try pip install python-editor")
                                if header=='vim':
                                    edit_event_buffer_in_vim(event)
                                if header=='save' or header=='string ans':#header=='save' because of the conflict of \sa in the dict
                                    buffer.insert_text(repr(str(get_ans())))
                                if header=='ans':
                                    buffer.insert_text(str(get_ans()))

                                if header=='web_string_paste'   : do_web_paste(buffer,repr_mode=True)
                                if header=='tmux_string_paste'  : do_tmux_paste(buffer,repr_mode=True)
                                if header=='vim_string_paste'  : do_vim_paste(buffer,repr_mode=True)
                                if header=='local_string_paste' : do_local_paste(buffer,repr_mode=True)

                                if header=='web_paste'          : do_web_paste(buffer,repr_mode=False)
                                if header=='tmux_paste'         : do_tmux_paste(buffer,repr_mode=False)
                                if header=='vim_paste'         : do_vim_paste(buffer,repr_mode=False)
                                if header=='local_paste'        : do_local_paste(buffer,repr_mode=False)

                                if 'comment_paste' in header or 'comment_ans'==header:
                                    commented_arg=''
                                    if before_line.count('`')==1:
                                            commented_arg=before_line.split('`')[1].split('\\')[0]
                                            buffer.delete_before_cursor(len(commented_arg+'`'))
                                    
                                    if header=='tmux_comment_paste' : do_tmux_paste(buffer,repr_mode=False,commented=commented_arg)
                                    if header=='comment_paste'      : do_paste(buffer,commented=commented_arg)
                                    if header=='comment_ans'      : 

                                        ans=str(get_ans())
                                        ans=commented_string(buffer,ans,spaces=commented_arg)
                                        buffer.insert_text(ans)

                                if header=='paste'              : do_paste(buffer)
                                if header=='string_paste'       : do_string_paste(buffer)

                                if header=='delete all':
                                    buffer.document=Document('',0,buffer.document.selection)
                                if header=='yapf autoformat':
                                    try:
                                        from rp import pip_import
                                        yapf=pip_import('yapf')
                                    except:
                                        fansi_print("ERROR: To use yapf's autoformat, you must first install yapf. 'pip install yapf' is an option. See https://github.com/google/yapf",'red','bold')
                                        return
                                    try:
                                        # buffer.delete_before_cursor(len('\\ya'))
                                        buffer.document=Document(yapf.yapf_api.FormatCode(buffer.document.text)[0],buffer.document.cursor_position,buffer.document.selection)
                                    except Exception as e:
                                        from rp import fansi_print 
                                        buffer.insert_text("\n#ERROR Using yapf autoformatter: "+str(e))
                                return

                    if char in {'d','c'} and not before_line.strip():
                        above=line_above(buffer)#returns None if there are no above lines
                        if above is not None and get_indent(above)==get_indent(before_line):
                            if above.strip().startswith('@'):#we have a decorator on our hands...
                                #when we're below a decorator and we press d or c, the only valid syntax is to create a 'def' or a 'class' keyword 
                                if char=='d':
                                    if in_class_func_decl(buffer):
                                        #class c:
                                        #   @decorator
                                        #   |
                                        #
                                        #   --->
                                        # 
                                        #class c:
                                        #   @decorator
                                        #   def |(self):
                                        buffer.insert_text('def (self):')
                                        buffer.cursor_left(7)
                                        return
                                    else:
                                        #@decorator
                                        #|
                                        #
                                        #--->
                                        # 
                                        #@decorator
                                        #def |():
                                        buffer.insert_text('def ():')
                                        buffer.cursor_left(3)
                                        return
                                if char=='c':
                                        #@decorator
                                        #|
                                        #
                                        #--->
                                        # 
                                        #@decorator
                                        #class |:
                                        buffer.insert_text('class :')
                                        buffer.cursor_left(1)
                                        return
                    if char=='s':
                            # cl=find_level("class ")#class level
                            # dl=find_level("def ")#def level
                            # dh=find_header("def ")#def header
                            # if cl is not None and dl is not None and dl>cl:
                            #     if '(self' in dh:
                            if meta_pressed(clear=True):
                                buffer.insert_text('self')
                                return 
                    # if char=='e':
                            # buffer.insert_text('trans')
                            # if meta_pressed(clear=False):
                                # buffer.accept_action.run_in_terminal(render_cli_done=True)
                                # buffer.accept_action.validate_and_handle(event.cli, buffer)
                                # buffer.insert_text('elf')
                                # buffer.insert_text('self')
                                # return 
                    if regex_match(before_line,r'\s*for _ in range\(\d+'):
                        #(let's say we press Y)
                        #for _ in range(123|):  --->  for _ in range(Y|):
                        buffer.delete_before_cursor(len(before_line.lstrip())-len('for _ in range('))
                        buffer.insert_text(char)
                        return
                    buffer.insert_text(char) 
            go(char)
            meta_pressed(clear=True)#Reset: we don't want to keep the esc key pressed (this should go after every keystroke. Period. But it doesnt yet cause ima be a lazy...)
    for char in '1234567890':#Digit inputs
        def go(c):
            @handle(c,filter=~vi_mode_enabled&microcompletions_enabled)
            def _(event):
                buffer=event.cli.current_buffer
                if handle_character(buffer,c,event):return
                if self_dot_var_equals_var(buffer,c) or setting_index(buffer,c):
                    return
                document=buffer.document
                current_line=document.current_line
                before_line=document.current_line_before_cursor
                after_line=document.current_line_after_cursor
                before=document.text_before_cursor
                after= document.text_after_cursor
                above_line=line_above(buffer)
                single_line=above_line is None
                #
                if c=='3':
                    if before_line.endswith(':') and not after_line and starts_with_any(before_line.lstrip(),'def ','for ','if ','while ','except ','try:'):
                        #Adding comments to the end of function declarations...what meaningful function would start with '3'?
                        buffer.insert_text('#')
                        return
                    if not single_line and not before_line.strip():
                        #Why reach for the shift key?
                        #What meaningful text could you write on a line starting with 3....on multi lines....
                        buffer.insert_text('#')
                        return
                    if meta_pressed():
                        buffer.cursor_right(123123)
                        buffer.insert_text('#')
                        return
                    if endswithany(before_line,')',']') and after_line=='':
                        #If inserting '3' would be break syntax and '#' would not, insert '#'
                        #This saves a shift-key stroke
                        buffer.insert_text('#')
                        return
                if before == 'from ' and after == ' import':
                    #Lets us do 'f 5' to get a for loop in the first line, instead of trying to import something
                    #from | import    --->   for _ in range(4|):
                    buffer.delete_before_cursor(999)
                    buffer.delete(999)
                    buffer.insert_text('for _ in range('+c+'):')
                    buffer.cursor_left(2)
                    return
                if regex_match(before_line,r'\s*for\s+\w+\s+in\s+') and after_line.strip()==':':
                    #(let's say c=3...)
                    #for x in |: --> for x in range(3|):
                    buffer.insert_text('range('+c+')')
                    buffer.cursor_left()
                    return
                if before_line.endswith('for ') and endswithany(after_line,' in]',' in)',' in}'):
                    #[x for | in]  --->  [x for _ in range(9|)]
                    buffer.insert_text('_')
                    buffer.cursor_right(3)
                    buffer.insert_text(' range()')
                    buffer.cursor_left()
                    buffer.insert_text(c)
                    return
                if before_line.endswith(' in ') and endswithany(after_line,']',')','}'):
                    #[x for y in |]  --->  [x for y in range(9)]
                    buffer.insert_text('range()')
                    buffer.cursor_left()
                    buffer.insert_text(c)
                    return
                if before_line.lstrip()=='for ' and after_line.rstrip()==' in :':
                    #(let's say c=3...)
                    #for | in : --> for _ in range(3|):
                    buffer.insert_text('_')
                    buffer.cursor_right(len(' in '))
                    buffer.insert_text('range('+c+')')
                    buffer.cursor_left()
                    return
                if c=='8' and before_line.lstrip().startswith('def ') and after_line.endswith('):') and before_line.count('(')==1 and endswithany(before_line,'(',',','*'):
                    #Why use the shift key to make kwargs?
                    #(on pressing 8)
                    #def f(|)   --->   def f(*|)
                    #def f(a,b,*|)   --->   def f(a,b,**|)
                    buffer.insert_text('*')
                    return
                if before_line.lstrip()=='def 'and after_line in ['():',':']:
                    #8 is the key that makes the * chracter. We can't start function names with numbers, so let's make this the default...
                    #On press 8:
                    #def |:   --->   def _(*args,**kwargs):|
                    buffer.delete(len(before_line))
                    buffer.insert_text('_(*args,**kwargs):')
                    return
                if before=='ans.' and not after:
                    if ans_dot_completion_string:
                        # Let's say c=3...
                        # (middle 'ans.|' is current state)
                        #   ans(|)   -->   ans.|   -->   ans(.3|)
                        #                   AND
                        #   ans[|]   -->   ans.|   -->   ans[.3|]
                        buffer.delete_before_cursor()
                        buffer.insert_text(ans_dot_completion_string)
                        buffer.cursor_left()
                        buffer.insert_text('.')
                    else:
                        # Let's say c=3...
                        #   ans.|   -->  .3|
                        # This lets use the 'ans.' completion from just typing '.', without sacrificing the ability to type '.4'
                        buffer.delete_before_cursor(len(before))
                        buffer.insert_text('.')
                buffer.insert_text(c)
        go(char)


    # @handle('Ω')
    # def _(event):
    #     import rp.prompt_toolkit.key_binding.bindings.vi as vi 
    #     try:
    #         vi.ryan_go_to_vim_navigation_mode(event)
    #     except:pass
    #
    @handle(Keys.ShiftLeft)
    def _(event):
        """
        Select from the history.
        """
        buffer=event.cli.current_buffer
        before_line=buffer.document.current_line_before_cursor
        if before_line.lstrip():
            #····blah|   --->   ····|blah
            buffer.cursor_left(len(before_line.lstrip()))
        elif before_line:
            #····|blah   --->   |····blah
            buffer.cursor_left(1000000)
        elif buffer.cursor_position:
            after=buffer.document.text_after_cursor
            if after.count('\n'):
                buffer.cursor_up()
                move_line_down(buffer)
                buffer.cursor_up()
            else:
                move_line_down(buffer)
            buffer.cursor_left(1000000)

#     @handle(Keys.ControlBackslash)
#     def _(event):
#         buffer=event.cli.current_buffer
#         pseudo_terminal(merge_dicts(r_iterm_comm.globa,{ans:buffer.document.text}))

    @handle(Keys.ShiftRight)
    def _(event):
        buffer=event.cli.current_buffer
        after_line=buffer.document.current_line_after_cursor
        before_line=buffer.document.current_line_before_cursor    
        if after_line and before_line.strip() or after_line and after_line==after_line.lstrip():
            #····|blah   --->   ····blah|
            buffer.cursor_right(1000000)
        elif after_line:
            #|····blah   --->   ····|blah
            buffer.cursor_right(len(after_line)-len(after_line.lstrip()))
        else:
            after=buffer.document.text_after_cursor
            if after.count('\n')==0:
                return#We're on the bottom
            elif after.count('\n')==1:
                buffer.cursor_down()
                move_line_down(buffer)
                buffer.cursor_down()
            else:
                move_line_down(buffer)
    def move_line_down(buffer,up=False):
        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        buffer.cursor_left(1000000)
        if not buffer.cursor_position:
            buffer.delete(2)
        buffer.cursor_right(1000000)
        # print("Ima doing/ it!")
        delete_current_line(buffer)
        buffer.cursor_right(10000)
        buffer.cursor_down(1)
        buffer.cursor_left(10000)
        #region Adaptive indentation: Currently not implemented. Sticking to simplicity.
        if False:
            buffer.insert_line_above(copy_margin=not up)
            buffer.insert_text(current_line.lstrip() if not up else current_line)
            text=buffer.document.text
            lstrip=text.lstrip()
        else:
            buffer.insert_line_above(copy_margin=False)
            buffer.insert_text(current_line)
            lstrip=text=buffer.document.text

        # buffer.cursor_down(1)
        # buffer.cursor_right(1000000)
        buffer.document=Document(lstrip,buffer.document.cursor_position+(len(lstrip)-len(text)),buffer.document.selection)

    #These keys don't respond on the mac terminal
    # @handle(Keys.ShiftUp)
    # def _(event):
    #     print(324982308974078923)
    #     event.cli.current_buffer.cursor_right(1000000)
    #
    # @handle(Keys.ShiftDown)
    # def _(event):
    #     print(324982308974078923)
    #     buffer=event.cli.current_buffer
    #     document=buffer.document
    #     current_line=document.current_line

    @handle(Keys.ControlD)# Duplicate current line Only applies when there's text, else it will trigger the exit
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        buffer.cursor_right(10000)
        current_line=document.current_line
        # buffer.insert_line_below()
        buffer.insert_text("\n"+current_line)
    def current_line_index(buffer):
        #returns current line number, starting from 0
        return buffer.document.text_before_cursor.count('\n')
    def go_to_line_number(n,buffer):
        i=current_line_index(buffer)
        delta=i-n
        if delta<0:
            buffer.cursor_down(abs(delta))
        else:
            buffer.cursor_up(abs(delta))
        buffer.cursor_up()
    def delete_current_line(buffer):
        buffer.delete_line_at_cursor()
        # document=buffer.document
        # current_line=document.current_line
        # buffer.cursor_left(10000)
        # firstline=buffer.cursor_position==0
        # buffer.delete(len(current_line))
        # buffer.delete_before_cursor()
        # if firstline:
        #     buffer.delete()
        # else:
        #     buffer.cursor_down()

    #region Bracket Match Writers
    function_comma_flag=False# Used to keep track of when we are writing arguments to fucntions that were initially parenthesized with the spacebar
    can_take_no_args=False# Doesn't practically matter right now if function_comma_flag is false


    @handle(Keys.ControlDelete)# Delete current line
    def _(event):
        buffer=event.cli.current_buffer
        delete_current_line(buffer)

    #region Bracket Match Writers
    function_comma_flag=False# Used to keep track of when we are writing arguments to fucntions that were initially parenthesized with the spacebar
    can_take_no_args=False# Doesn't practically matter right now if function_comma_flag is false

    @handle('.',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):# period '.' event handler function thingy
        buffer=event.cli.current_buffer
        if handle_character(buffer,'.',event):return
        if self_dot_var_equals_var(buffer,'.'):
            #self.foo|=foo   --->   self.foo.|=self.foo.
            return
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor



        # if before_line.endswith('=') and not before_line.endswith('=='):
            #Moved this functionality elsewhere to fix the i=.5 which autocompleted to i.5=5, which is not what we want because 5 is a numeric key
            #self=|   --->   self.|=   (and then type foo to get self.foo=foo)
            # buffer.cursor_left()
            # buffer.insert_text('.')
            # return
        if not before and not after:
            buffer.insert_text('ans.')
            return
        import rp.r_iterm_comm
        var=rp.r_iterm_comm.last_assignable_comm
        # if before.endswith('=') and before[:-1]==var:
            #THIS COMLPETION IS COMMENTED OUT EVEN THOUGH IT WORKS. IT GOT ANNOYING FOR TETING THE =.. OPERATOR, WHICH I THINK MIGHT BE MORE IMPORTANT FOR DEMOING RPTERM
            #var=|  -->  var.|
            #You can use a sequence like:
            #  (What you type)   (What rp types)
            #   i numpy np          import numpy as np
            #   =.array?            np.array?
            # buffer.delete_before_cursor()
        if before_line.endswith("''") and not before_line.endswith("'''") and after_line.startswith("''") and not after_line.startswith("'''") or\
           before_line.endswith('""') and not before_line.endswith('"""') and after_line.startswith('""') and not after_line.startswith('"""'):
           # “''.['“   —>  ''.join([''])
            buffer.insert_text('.join()')
            buffer.delete(2)
            buffer.cursor_left()
            return
        if before_line.endswith("''.join(") and after_line.startswith(')'):
            # “''..[“        —>     ''.join(map(str,[]))
            # “''.[''“       —>     ''.join([''])
            buffer.insert_text('map(str,)')
            buffer.cursor_left()
            return
        if before+after in {'ans[]','ans()'} and after in {']',')'}:
            #ans[|]  -->  ans.|
            #       AND
            #ans(|)  -->  ans.|
            #
            #For space-completing 'ans' then wanting to use a '.', but can't 
            #
            #Edge case: when we want to write ans(.25) where ans is a float-function
            #   This is handled like so:
            #       ans(|)  -->  ans.|  -->  ans(.25)  
            #   Basically, the parenthesis are put back because the character following the '.' is a digit
            #   (This is handled in the digit handler, search for "ans_dot_completion_string")
            buffer.delete()
            buffer.delete_before_cursor()
            global ans_dot_completion_string
            ans_dot_completion_string=before[-1]+after[0]# is either () or []
        buffer.insert_text('.')


    @handle(Keys.Escape,filter=~vi_mode_enabled)#microcompletions_enabled)
    def _(event):
        _meta_pressed.append(True)#This is meant to be flipped to false immediately after anything reads it, with meta_pressed(). We're using a list to easily keep track of this after this method is @'d outta this file somewhere else idk where

    @handle(' ',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):# Spacebar event handle spacebar
        buffer=event.cli.current_buffer
        if handle_character(buffer,' ',event):return
        single_line = line_above(buffer) is None
        if meta_pressed():#No shenanagins -- just give me a space.
            buffer.insert_text(' ')
            return
        nonlocal function_comma_flag# ,can_take_no_args
        # from rp import mini_terminal
        # exec(mini_terminal)
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor

        if document.text=='':# What else would we possibly want the spacebar for on an empty input? Spacebar invokes functions, and the default variable is ans.
            import rp.r_iterm_comm as ric
            if callable(ric.ans):
                buffer.insert_text('ans()')
                buffer.cursor_left()
                function_comma_flag=True
            elif hasattr(ric.ans,'__getitem__'):#if we can do ans[0], ans[1] etc
                buffer.insert_text('ans[]')#we cant call it...might want to iterate through it though!
                buffer.cursor_left()
                function_comma_flag=True
            else:
                buffer.insert_text('ans')#Bleh it's boring
            return


        if before.startswith('!'):# Don't do anything special
            buffer.insert_text(' ')
            return
        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor
        if before_line.endswith(' in len') and starts_with_any(after_line,*'}])'):
                #[x for x in len|]  --->  [x for x in range(len(|))]
                buffer.delete_before_cursor(3)
                buffer.insert_text('range(len())')
                buffer.cursor_left(2)
                return
        if before_line.lstrip().startswith('class ') and after_line.startswith(':'):
            #class c|:   --->   class c(|):
            buffer.insert_text('()')
            buffer.cursor_left()
            return
        if before_line.lstrip().startswith('class ') and after_line.startswith('):'):
            if before_line.endswith(','):
                #class c(x,|):   --->   class c(x):|
                buffer.delete_before_cursor()
                buffer.cursor_right(2)
                return
            if before_line.endswith('('):
                #class c(|):   --->   class c:|
                buffer.delete_before_cursor()
                buffer.delete()
                buffer.cursor_right()
                return
        if before_line.lstrip().startswith('def '): 
            if before_line.endswith('def __') and after_line.startswith('__(self):'):
                #class x:
                #   def __|__(self):
                # 
                #   --->
                # 
                #class x:
                #   def __init__(self,|):
                buffer.insert_text('init')
                buffer.cursor_right(7)
                buffer.insert_text(',')
                return
            if before_line.strip()=='def' and after_line.startswith('(self):'):
                #class x:
                #   def |(self):
                # 
                #   --->
                # 
                #class x:
                #   def __|__(self):
                buffer.insert_text('____')
                buffer.cursor_left(2)
                return
            if after_line.startswith('__(self):'):
                #class x:
                #   def __eq|__(self):
                # 
                #   --->
                # 
                #class x:
                #   def __eq__(self|):
                if before_line.endswith('__'):
                    #autocomplete might have messed things up, this is a sloppy hack to fix that...
                    #def __eq__|__(self):   --->   #def __eq__(self|): 
                    buffer.delete_before_cursor(2)
                buffer.cursor_right(7)
                return
            if after_line.startswith('(self):'):
                #def f|(self):   --->   def f(self,|):
                buffer.cursor_right(5)
                buffer.insert_text(',')
                return
            if before_line.endswith(':') and not after_line.strip():
                #def f(x):|   --->   def f(x):return |
                buffer.insert_text('return ')
                return
            if before_line.strip()=='def __' and after_line.startswith('__(self):'):
                #class x:
                #   def __|__(self):
                # 
                #   --->
                # 
                #class x:
                #   def __init__(self|):
                buffer.insert_text('init')
                buffer.cursor_right(7)
                return
            if before_line.strip()=='def' and after_line.startswith('():'):
                def on_first_line():
                    return '\n' not in (before+after)
                function_title='ans' if on_first_line() else '_'
                #def |():   --->   def _(|):   (sometimes, when using decorators, you want an anonymous function)
                #def |():   --->   def ans(|): (if we're defining a function on the first line, perhaps we want to use it as our answer? I haven't actually used this yet; it's just an idea, I'll see how much I like it...)
                buffer.insert_text(function_title)
                buffer.cursor_right(1)
                return
        if before_line.strip()=='def' and not after_line.strip().endswith(':'):
            buffer.insert_text(' :')
            buffer.cursor_left()
            return
        if before_line.strip().startswith('def ') and endswithany(before_line.strip(),',','(') and after_line.strip()=='):':
            if before_line.endswith(','):
                buffer.delete_before_cursor()
            buffer.cursor_right(2)#If we want a one-line function
            return
        if self_dot_var_equals_var(buffer):
            #self.|foo=foo   --->   self.foo=foo|
            buffer.cursor_right(999999)
        from rp import is_namespaceable,space_split
        if before_line.strip().startswith('def ') and len(space_split(before_line.strip()))==2:
            if after_line.strip()==':' and is_namespaceable(before_line.split(' ')[-1]):
                buffer.insert_text('()')
                buffer.cursor_left()
                return
        if after_line=='):' and before_line.endswith(','):
            buffer.delete_before_cursor()
            if starts_with_any(before_line.strip(),*'if while'.split()):
                #if f(x,|):  --->  if f(x) |:
                buffer.cursor_right(1)
                buffer.insert_text(' ')#Lets us trigger things like a--->and
            else:
                #for x in range(5,|):   --->   for x in range(5):|
                buffer.cursor_right(2)
            return
        if before_line.endswith(' imoprt') or before_line.startswith("imoprt"):# This is a really common typo for me
            buffer.delete_before_cursor(6)
            buffer.insert_text('import ')
            return
        from rp import regex_match
        if regex_match(before_line.lstrip(),r'for\s+\w+\s+in\s+len'):
                #(Also implemented upon pressing '(')
                #for x in len|   -->  for x in range(len(|))
                buffer.delete_before_cursor(3)
                buffer.insert_text('range(len())')
                buffer.cursor_left(2)
                return
        if before_line.lstrip()=='if ' and after_line.rstrip()==':':
            #if |:   --->   import |
            buffer.delete_before_cursor(3)
            buffer.insert_text('import ')
            buffer.delete()
            return
        if before_line.lstrip()=='import ' and not after_line.rstrip():
            #import |   --->   if |:
            buffer.delete_before_cursor(len('import '))
            buffer.insert_text('if :')
            buffer.cursor_left()
            return
        # if before_line.lstrip()=='for ' and after_line==' in :':
        #     #"for | in :"  --->  "for _ in |:"
        #     buffer.insert_text('ans')
        #     return
        keywords={'async','await','with', 'nonlocal', 'while', 'None', 'global', 'as', 'is', 'and', 'else', 'yield', 'raise', 'del', 'break', 'in', 'not', 'False', 'assert', 'try', 'def', 'return', 'if', 'finally', 'lambda', 'for', 'from', 'True', 'pass', 'continue', 'elif', 'except', 'class', 'or', 'import'}

        if regex_match(before,r'\s*for\s+\w+\s+in\s+') and after.strip()==':':
            #"for x in |:"  --->  "for x in ans:"
            #(better alternative than "for x in |:" ---> "for x in:|", which is in the next block...)
            buffer.insert_text('ans')
            return
        elif starts_with_any(before_line.lstrip(),'if ','for ','while ') and before_line.endswith(' ') and after_line.rstrip()==':':# This is a really common typo for me
            #if x|:   --->   if x:|
            buffer.delete_before_cursor(1)
            buffer.cursor_right(2)
            return
        from rp import space_split,is_namespaceable
        import rp.r_iterm_comm as r_iterm_comm
        split=space_split(before_line)
        from rp import printed
        from_or_import_on_beginning_of_line=before_line.lstrip().startswith("import ") or before_line.lstrip().startswith("from ")
        def is_callable_token(token_name):
            try:
                return callable(eval(token_name,r_iterm_comm.globa))
            except:
                return False#be on the safe side with space-function completions
        try:
            function_comma_flag=function_comma_flag and( after_line.startswith(")") or after_line.startswith("'") or after_line.startswith('"') or after_line.startswith(']') or after_line.startswith(']') )
            token_of_interest,name_of_interest,found_token_of_interest=token_name_found_of_interest(before_line)
            from rp import regex_match
            def is_autocompletable_prefix(big,suffixes=[''],allow_single_liner=True,use_name_of_interest=False):
                #leave suffixes [] or None to allow any suffix
                if not allow_single_liner:
                    if '\n' not in before+after:
                        return False
                if use_name_of_interest:
                    name=name_of_interest
                else:
                    name=before_line.strip()
                return big.strip() != name and big.startswith(name) and before_line.strip() and (not suffixes or after_line in suffixes)#Shouldn't trigger when r is a function, because of where this is in the elif chain
            def autocomplete_prefix(big,left=1,remove_suffix=False):
                if remove_suffix:#used in 'except|:' --> 'except | as :', which is also 'except|' --> 'except | as :'
                    buffer.cursor_right(len(after_line))
                    buffer.delete_before_cursor(len(after_line))
                buffer.insert_text(big[len(name_of_interest):])
                buffer.cursor_left(left)
                try_to_autounindent(buffer)

            def try_autocompleting_functions(N,not_just_functions=False):
                from rp import ring_terminal_bell
                # if not_just_functions:
                    # ring_terminal_bell
                #TODO: right now not_just_functions doesn't do anything, it's supposed to let you space complete functions while importing
                nonlocal before_line,after_line,before,after

                #go through the top N current autocompletion results, and if one of them is callable, call it.
                # if before.count(' ')+before.count('\n')>1:
                    # return False #Don't autocomplete like this unless we are doing a one-liner
                bs=before_line.lstrip()#Before Strip  (bs)
                if not not_just_functions:
                    if not '\n' in before.strip() and before.strip().isupper() or beginswithany(bs,'import ','from ','def ') or 'lambda' in bs:#Basically, any place we're allowed to declare new variable names, we shouldn't be autocompleting them. lambda is bit tricky so I'm just sayig 'no space function completion on lines that contain lambda'.
                        return False#We might be typing something like 'UNDO ALL', in which case we do NOT want the 'UNDO' to be autocompleted
                import rp.r_iterm_comm as ric
                for candidate in ric.current_candidates:#Don't autocomplete if our current word to complete allready exists. For example, don't complete 'in' into 'inverse', etc.
                    try:
                        if hasattr(candidate,'text') and candidate.text==name_of_interest or candidate==name_of_interest:
                            return False
                    except:pass
                # ring_terminal_bell()
                # print(ric.current_candidates)
                if not_just_functions:
                    if not ric.current_candidates or  '.' in before_line:
                        return False#Problem avoided: Used to be 'import scipy.stats' -/-> 'import stats as |s'
                    buffer.delete_before_cursor(len(name_of_interest))#erase the current line
                    #space completions: 
                    #import num|   --->   import numpy as |
                    #(etc)
                    space_completion=ric.current_candidates[0]
                    if before_line.endswith(space_completion):
                        return False#Problem avoided: Used to be 'import cv2|' -/-> 'import cv2cv2 as |s'
                    #region Erase before and after so we don't do stupid things: Example, on autocompleting 'print', we want:
                    #   'pr|i'  --->  'print|'
                    #       and NOT
                    #   'pr|i'  --->  'prprint|i'
                    if is_namespaceable(space_completion):
                        #Allready taken care of in above line commented "erase the current line"
                        # while before_line and before_line[-1] in space_completion:
                        #     buffer.delete_before_cursor()
                        #     before_line=before_line[:-1]
                        #     before     =before     [:-1]
                        while after_line  and  after_line[ 0] in space_completion:
                            buffer.delete()
                            after_line =after_line [1: ]
                            after      =after      [1: ]
                    #endregion
                    buffer.insert_text(space_completion)
                    return True 
                for x in ric.current_candidates[:N]:
                    if is_callable_token(x) or not_just_functions and not (after_line.strip()=='():' and before_line.rstrip().startswith('def ')):
                        # if re.fullmatch(r'((.*[^a-zA-Z0-9_])|())for [a-zA-Z0-9_]',before_line):
                            buffer.delete_before_cursor(len(name_of_interest))#erase the current line
                            buffer.insert_text(x+('' if  not_just_functions else '()'))
                            buffer.cursor_left()
                            nonlocal function_comma_flag
                            function_comma_flag=True
                            return True
            if before_line.lstrip().startswith('def ') and before_line.endswith("=lambda")and after_line.startswith(')'):#When passing a lambda as an argument in a function definition default value (a nichey case, but important nevertheless), add a space so the rest of the program knows its a lambda (which it uses spaces to see)
                buffer.cursor_left(6)
                buffer.insert_text(' ')
                buffer.cursor_right(6)

            if not from_or_import_on_beginning_of_line \
                and not before_line.endswith(" ") \
                and callable(token_of_interest)  \
                and not (after_line.strip()=='():' and before_line.rstrip().startswith('def '))\
                and not re.fullmatch(r'((.*[^a-zA-Z0-9_])|())for [a-zA-Z0-9_]+',before_line)\
                and not re.fullmatch(r' *def [a-zA-Z0-9_]+\( *[a-zA-Z0-9_]+( *\, *[a-zA-Z0-9_]+ *)*',before_line)\
            :
                function_comma_flag=True
                import inspect
                #space-function implementation HERE
                #ON SPACE
                # callable_function|   --->   callable_function(|)
                #This is a big deal. I use this ALL THE TIME.

                # try:
                #     can_take_no_args=len(inspect.getfullargspec(token_of_interest).args)==0
                # except:# Probably a builtin function
                #     can_take_no_args=0 or token_of_interest is print
                if before_line.count('=')==1 and after_line=='('+before_line.split('=')[0].strip()+')':
                    #We came from using the )= operator. We want `matrix)=np.asarray float` --->  `matrix=np.asarray(matrix,float)` and not `matrix=np.asarray(float)(matrix)` (which would happen without this block)
                    buffer.cursor_right(99999)
                    buffer.cursor_left()
                    buffer.insert_text(',')
                else:
                    buffer.insert_text('()')
                    buffer.cursor_left(count=1)
            # region Brackets....they work but conceptually they're annoying.
            # elif not from_or_import_on_beginning_of_line and not before_line.endswith(" ") and hasattr(token_of_interest,'__getitem__'):
            #     buffer.insert_text('[]')
            #     buffer.cursor_left(count=1)
            #endregion

            elif regex_match(before_line.lstrip(),r'(from .*)|(import \w*)') and try_autocompleting_functions(N=1,not_just_functions=True):
                if(before_line.lstrip().startswith('from ')):
                    buffer.cursor_right(len(' import'))
                    buffer.insert_text(' ')
                elif(before_line.lstrip().startswith('import ')):
                    buffer.insert_text(' as ')#Without this, space would be redundant with respect to tab
            elif regex_match(before_line.lstrip(),r'from \w* import '):
                #'from rp import |'  -->  'from rp import *'
                buffer.insert_text('*')
            elif regex_match(before_line.lstrip(),r'from \w* import \*'):
                #'from rp import *|'  -->  'from rp import '
                buffer.delete_before_cursor()

            elif before_line.lstrip().startswith('with ') and after_line.startswith(':') and not before_line.endswith(' as '):
                buffer.insert_text(' as ')

            elif endswithany(before_line,' in len',' in le',' in l') and starts_with_any(after_line,':',']','}',')'):
                #Doesn't work if e is allready callable.
                #[x for x in l|]   --->   [x for x in range(len(|))]
                #for x in l|:      --->   for x in range(len(|)):
                buffer.delete_before_cursor(1 if before_line.endswith('l') else 2 if before_line.endswith('le') else 3)
                buffer.insert_text('range(len())')
                buffer.cursor_left(2)
                return
            elif name_of_interest in {'l','la','lam','lamb','lambd','lambda'} \
                and not 'import 'in before_line \
                and not before_line.lstrip() in {'for '+name_of_interest,'with '+name_of_interest} \
                and not re.fullmatch(r'( *def .*)|(.*[^a-zA-Z0-9_]lambda [^\:]*)|(.*[^a-zA-Z0-9_](for|in|as) (l|la|lam|lamb|lambd|lambda))',before_line) \
                :
                #Make a lambda from l
                #Shouldn't trigger when l is a function, because of where this is in the elif chain
                noil=len(name_of_interest)#noil stands for ((name of interest) length)
                if before_line.strip()!=name_of_interest:#don't do this at the beginning of an empty line
                    buffer.cursor_left(noil)
                    if not buffer.document.text_before_cursor.endswith(' '):
                        buffer.insert_text(' ')
                    buffer.cursor_right(noil)
                buffer.insert_text('lambda :'[noil:])
                buffer.cursor_left()
            elif regex_match(before_line.strip(),r'(for .* in in)') and after_line.strip()==':':
                buffer.delete_before_cursor(2)
            elif regex_match(before_line.strip(),r'(from \w* import import)') and after_line.strip()=='':
                buffer.delete_before_cursor(len('import'))
            elif before_line.endswith('lambda:'):
                #The default, most boring kind of lambda...
                #"lambda:|"   --->  "lambda:None|"
                buffer.insert_text('None')

            #None of the 'is_autocompletable_prefix's ahead should trigger when the prefix is a function, so as not to interfere with normal autocompletion in most cases
            elif is_autocompletable_prefix('def ():'):
                if in_class_func_decl(buffer):  autocomplete_prefix('def (self):',left=7)
                else:           autocomplete_prefix('def ():',left=3)
            elif before_line.lstrip().startswith('def ') and after_line.rstrip().endswith('):') and after_line.startswith('('):buffer.cursor_right()


            elif after_line.startswith(' in)'):
                #print(x for y| in)  -->  print(x for y in |)
                buffer.cursor_right(len(' in'))
                buffer.insert_text(' ')
            elif before_line.endswith(',for'):
                #print(x,for|)  -->  print(x for | in)
                buffer.delete_before_cursor(len(',for'))
                buffer.insert_text(' for  in')
                buffer.cursor_left(len(' in'))
            elif before_line.endswith(',if'):
                #Because when we're in functions, hitting space makes commas, we can still do 'for', 'if', etc
                #print(x,if)  -->  print(x for | in)
                buffer.delete_before_cursor(3)
                buffer.insert_text(' if  else')
                buffer.cursor_left(len(' else'))
            elif before_line.lstrip()=='else:'and not after_line.strip():
                #else:|   --->   elif |:
                buffer.delete_before_cursor(len('else:'))
                buffer.insert_text('elif :')
                buffer.cursor_left()
            elif before_line.lstrip()=='elif 'and after_line.rstrip()==':':
                #elif:|   --->   else:
                buffer.delete_before_cursor(len('elif '))
                buffer.insert_text('else')
                buffer.cursor_right()
            elif before_line.lstrip()=='f' and not after_line.strip() and single_line:
                #f|   --->   from | import         ONLY ON ONE-LINERS
                buffer.insert_text('rom  import')
                buffer.cursor_left(len(' import'))
            #Note that this was created after some other things in this file, and might even be redundant sometimes. For example, 'if'-->'if |:' is allready covered elsewhere in key_bindings.py
            elif is_autocompletable_prefix('return ',allow_single_liner=False):autocomplete_prefix('return ',left=0)
            elif is_autocompletable_prefix('while :'):autocomplete_prefix('while :')
            elif is_autocompletable_prefix('class :'):autocomplete_prefix('class :')
            elif is_autocompletable_prefix('for  in :'):autocomplete_prefix('for  in :',left=5)
            elif not (before=='i' and not after) and is_autocompletable_prefix('if :'):autocomplete_prefix('if :',left=1)#'i|' ---> 'if |:' ONLY IF we've typed something else in this buffer allready (often, I dedicate an input line to nothing but importing something)
            elif is_autocompletable_prefix('import '):autocomplete_prefix('import ',left=0)
            elif is_autocompletable_prefix('from  import'):autocomplete_prefix('from  import',left=7)
            elif is_autocompletable_prefix('elif :',allow_single_liner=False):autocomplete_prefix('elif :',left=1)
            elif is_autocompletable_prefix('else:',allow_single_liner=False):autocomplete_prefix('else:',left=0)
            elif is_autocompletable_prefix('try:'):autocomplete_prefix('try:',left=0)
            # elif is_autocompletable_prefix('True ',suffixes=[' ']):autocomplete_prefix('True ',left=0)
            # elif is_autocompletable_prefix('False ',suffixes=[' ']):autocomplete_prefix('False ',left=0)
            elif is_autocompletable_prefix('break',allow_single_liner=False):autocomplete_prefix('break',left=0)
            elif is_autocompletable_prefix('continue',allow_single_liner=False):autocomplete_prefix('continue',left=0)
            elif is_autocompletable_prefix('yield ',allow_single_liner=False):autocomplete_prefix('yield ',left=0)
            elif before_line.lstrip()!='yield' and is_autocompletable_prefix('yield from ',allow_single_liner=False):autocomplete_prefix('from ',left=0)
            # elif is_autocompletable_prefix('print()'):autocomplete_prefix('print()',left=1)#not a keyword, but used so frequently...
            elif is_autocompletable_prefix('assert '):autocomplete_prefix('assert ',left=0)
            elif is_autocompletable_prefix('nonlocal '):autocomplete_prefix('nonlocal ',left=0)
            elif is_autocompletable_prefix('global '):autocomplete_prefix('global ',left=0)
            elif is_autocompletable_prefix('raise '):autocomplete_prefix('raise ',left=0)
            elif is_autocompletable_prefix('async '):autocomplete_prefix('async ',left=0)
            # elif is_autocompletable_prefix('async def ():'):autocomplete_prefix('def ():',left=3)

            elif is_autocompletable_prefix('print()',allow_single_liner=True):autocomplete_prefix('print()',left=1);function_comma_flag=True
            elif is_autocompletable_prefix('pass',allow_single_liner=False):autocomplete_prefix('pass',left=0);function_comma_flag=True

            elif is_autocompletable_prefix('except :',allow_single_liner=False):autocomplete_prefix('except :',left=1)
            elif is_autocompletable_prefix('with :'):autocomplete_prefix('with :',left=1)
            elif ((not '\n' in before and not after and re.fullmatch(r'\w+',before_line) and not any(before_line.endswith(keyword) for keyword in keywords)) #space-completions are enabled if we're typing a function out as a comand, because then we know we don't have to worry about messy edge cases. space-functions are really convenient...\
                    or enable_space_autocompletions) \
                  and not regex_match(before_line.lstrip(),r'(def .*)|(for \w*)') \
                  and not name_of_interest.isdigit() \
                  and name_of_interest \
                  and try_autocompleting_functions(N=20):\
                    pass#"not name_of_interest.isdigit() and name_of_interest " because '5' --> 'display_color_255' without it, which is REALLY annoying
            # elif is_autocompletable_prefix('except :',[':','']):autocomplete_prefix('except :',left=1,remove_suffix=True)
            # elif is_autocompletable_prefix('except  as :',[':','']):autocomplete_prefix('except  as :',left=5,remove_suffix=True)
            elif before_line.lstrip()=='except ' and after_line.rstrip()==':':
                buffer.delete_before_cursor()
                buffer.cursor_right()
                return
            # elif before_line.endswith(' is '):
                #"x is |" --> "x is not |"
                # buffer.insert_text('not ')
                # return
            elif before_line.endswith(' is not '):
                #"x is not |" --> "x is |"
                buffer.delete_before_cursor(4)
                return
            elif before_line.lstrip()=='yield from ':
                #"yield from |" --> "yield |"
                buffer.delete_before_cursor(len('from '))
                return
            elif before_line.lstrip().startswith('except') and before_line.strip().endswith(":") and not after_line.rstrip():
                buffer.insert_text('pass')
                return
            elif starts_with_any(before_line.lstrip(),'except ','with ') and before_line.endswith(' as ') and after_line.strip()==':':
                #except A as |:   --->   except A:|
                buffer.delete_before_cursor(len(' as '))
                buffer.cursor_right()
            elif before_line.lstrip().startswith('except ') and not '(' in before_line:#not '(' in before_line because it won't properly complete functions for some reason inside the 'except' lines
                if before_line.lstrip()=='except ' and after_line.rstrip()==' as :':
                    #'except | as :' --> 'except|:'
                    buffer.cursor_right(len(' as '))#leave the ':' alone
                    buffer.delete_before_cursor(len(' as '))
                    buffer.delete_before_cursor()
                else:
                    if after_line==' as :':
                        #'except stuff | as :' --> 'except stuff as |:'
                        buffer.cursor_right(4)
                    elif after_line==':' and not ' as ' in before_line and not before_line.endswith('as'):
                        if before_line.endswith(' '):
                            buffer.delete_before_cursor()#when we have two spaces because of a function '()' --> ' '
                        if before_line.lstrip()=='except ':
                            buffer.delete_before_cursor()
                        else:
                            buffer.insert_text(' as ')
                        # buffer.cursor_right(0)
                    else:
                        buffer.insert_text(' ')
            elif before_line.lstrip().startswith('except ') and before_line.endswith('(') and after_line.startswith(')'):
                #except Exception()|:   -->   except Exception as |:
                buffer.cursor_right()
                buffer.delete_before_cursor(2)
                buffer.insert_text(' as ')
            elif before_line.lstrip().startswith('for ') and after_line.rstrip()==' in :':
                if before_line.lstrip()=='for ':#if we haven't given any variable name to iterate yet, switch to the 'from' shortcut instead because from and for both start with f
                    #Switch between 'for' and 'from'
                    buffer.cursor_right(len(' in :'))
                    buffer.delete_before_cursor(len('for '+' in :'))
                    buffer.insert_text('from  import')
                    buffer.cursor_left(len('import '))
                    return
                #Shouldn't trigger when r is a function, because of where this is in the elif chain
                buffer.cursor_right(4)
            elif before_line.endswith('lambda ')and after_line.startswith(':'):
                buffer.delete_before_cursor()
                buffer.cursor_right()
            elif endswithany(before_line,' -','[-','(-','{-'):
                #[-|] ---> [_ |]
                #[x and -|] ---> [x and _ |]
                #Posible imperfection: Maybe _ is a function. If it is, this current (sloppy) method of handling it won't call _, it will just add a space after it.
                buffer.delete_before_cursor()
                buffer.insert_text('_ ')
                return 
            elif starts_with_any(after_line,' in]',' in}','in )'):
                #A follow-up to a completion after pressing the f-key to create a comprehension
                #[x for x| in]   --->   [x for x in |]
                buffer.cursor_right(3)
                buffer.insert_text(' ')
                return
            elif single_line and before_line.endswith(' in ') and starts_with_any(after_line,']','}',')'):
                #List comprehension on single-liners
                #[x for x in |] --->  [x for x in ans]
                buffer.insert_text('ans')
                return                
            elif endswithany(before_line,' in e') and starts_with_any(after_line,':',']','}',')'):
                #Doesn't work if e is allready callable.
                #[x for x in e|]   --->   [x for x in enumerate(|)]
                #for x in e|:      --->   for x in enumerate(|):
                buffer.insert_text('numerate()')
                buffer.cursor_left()
                return
            elif endswithany(before_line,' in z') and starts_with_any(after_line,':',']','}',')'):
                #Doesn't work if e is allready callable.
                #[x for x in z|]   --->   [x for x in zip(|)]
                #for x in z|:      --->   for x in zip(|):
                buffer.insert_text('ip()')
                function_comma_flag=True
                buffer.cursor_left()
                return
            elif endswithany(before_line,' in r') and starts_with_any(after_line,':',']','}',')'):
                #Doesn't work if e is allready callable.
                #[x for x in r|]   --->   [x for x in range(|)]
                #for x in r|:      --->   for x in range(|):
                buffer.insert_text('ange()')
                buffer.cursor_left()
                return
            elif before_line.endswith('if ') and after_line.startswith(' else'):
                #Probably didn't mean to press the space-bar, out of habit...this works because of other completions
                #if | else    --->    if | else
                return
            elif (starts_with_any(after_line,' else]',
                                            ' else ',
                                            ' else)',
                                            ' else}',
                                            ' else,',
                                            ' else:') or after_line==' else') and not \
                                            endswithany(before_line,' if ',
                                                                    ']if ',
                                                                    ')if ',
                                                                    '}if ',
                                                                    '"if ',
                                                                    "'if ",
                                                                    ):
                #[x if y| else] ---> [x if y else |]
                buffer.cursor_right(len(' else'))
                buffer.insert_text(' ')
            elif before_line and after_line and before_line[-1]+after_line[0] in ['()','[]','{}']:
                if document.text in ['ans()','ans[]']:
                    buffer.delete()
                    buffer.delete_before_cursor(count=40000)
                    buffer.insert_text(' ')
                    return
                if '\n' not in before and after==')':
                    #'print()|' --> 'print(ans,|)'
                    #NOTE that upon hitting the enter key, the extra comma dissapears ('print(a,b,c,ans,|)'   --->   'print(a,b,c,ans)')
                    buffer.insert_text('ans,')
                    return
                buffer.cursor_right(count=1)
                buffer.delete_before_cursor(count=2)
                # if can_take_no_args:
                #     if function_comma_flag:
                #             buffer.insert_text(',')
                #     else:
                #             buffer.insert_text('(),')
                # else:
                #     if function_comma_flag:
                #         buffer.insert_text(',')
                #     else:
                #         buffer.insert_text(' ')
                if function_comma_flag and after_line.startswith("))"):
                    buffer.insert_text(',')
                else:
                    buffer.insert_text(' ')
            elif function_comma_flag and after_line.startswith(')'):
                if before_line.endswith(","):
                    if '\n' not in before and after==')':#(meant for one-liners, not multiliners. I wanted a convenient way to write ans into functions like this.)
                        #print(a,b,c,|) --> print(a,b,c,ans,|)
                        buffer.insert_text('ans,')
                        #NOTE that upon hitting the enter key, the extra comma dissapears ('print(a,b,c,ans,|)'   --->   'print(a,b,c,ans)\n|')
                    else:
                        #print(|) --> print
                        buffer.delete_before_cursor()
                        buffer.cursor_right()
                        if after_line.startswith("))"):
                            #print(f(|)) --> print(f(),|)
                            buffer.insert_text(',')
                elif before_line.endswith("lambda"):#special case to detect and space-autocomplete lambda syntax inside functions (normally, space in a function would make a comma; but we want print(lambda|) to go to print(lambda |:), not print(lambda,|))

                    buffer.cursor_left(count=6)
                    rev=document.text_before_cursor[::-1]
                    buffer.insert_text(' ')#This space is just an easy patch to let lambdas be easily put inside function arguments (before it was kinda annoying and didnt work well but not it does. yay. )
                    buffer.cursor_right(count=6)
                    buffer.insert_text(' :')
                    buffer.cursor_left(count=1)
                else:
                    buffer.insert_text(',')
            elif not after_line and all(is_namespaceable(x) for x in split) and len(split)==2 and split[0]=='def':
                buffer.insert_text('():')
                buffer.cursor_left(count=2)
            elif (before_line.lstrip() in['if','while','for','with','try','except'] or split and  name_of_interest=='lambda') and not after_line.strip().startswith(":"):
                buffer.insert_text(' :')
                buffer.cursor_left(count=1)
            elif before_line and after_line and before_line[-1]==','and after_line[0]==':':# for after lambda x,a,b,c,cursor:
                buffer.delete_before_cursor(count=1)
                buffer.cursor_right(count=1)
                buffer.insert_text(' ')

            elif len(split)>=2 and split[-2]=='lambda' and ':'not in name_of_interest or after_line=='):' and not before_line.rstrip().endswith(',') and before_line.lstrip().startswith('def '):# new argument in def
                #def f(x|): --> def f(x,):
                buffer.insert_text(',')
            elif before_line.lstrip()=='i':#Quick shortcut for importing. Type 'i' then press space. THis should only come after checking if i is a function, which should happen in some other if/else case above this line.
                #"i|" --> "import |"
                buffer.insert_text('mport ')
            elif before_line.lstrip()=='f':#Quick shortcut for 'from * import * style importing'. Type 'f' then press space.
                #"f|" --> "from | import"
                buffer.insert_text('rom  import')
                buffer.cursor_left(7)
            elif not after_line and (before_line.lstrip().startswith('import ') or before_line.lstrip().startswith('from ')):
                if before_line.endswith(' as'):
                    #for when the user doesn't know about or forgets about the 'as' autocompletion, so we don't end up with 'as as'
                    #'import x as as|'  -->  'import x as |'
                    buffer.delete_before_cursor(2)
                    buffer.insert_text('')#To trigger autocompletion
                    return
                if before_line.endswith(','):
                    #'import x,'  -->  'import x, |'
                    #Weird behavior if we don't do this an the user manually puts a comma without a space before this function would
                    buffer.insert_text(' ')
                    return
                #not after_line, so we're at the end of the line, which means we are done inputting the module name after 'from' or 'input'
                l=space_split(before_line)
                allready_end_with_an_as=len(l)>=2 and l[-2]=='as'
                if before_line.endswith(' as '):
                    #import x as | --> import x,|
                    buffer.delete_before_cursor(4)
                    buffer.insert_text(', ')
                elif before_line.rstrip().endswith(','):
                    #import x,| --> import x as |
                    buffer.delete_before_cursor(2)
                    # if allready_end_with_an_as:
                        # return
                    # buffer.insert_text(' as ')
                elif 'import ' in before_line:#to protect against "from x|" --> "from x as |" if we decide to type out the whole thing (naively)
                    #import x| --> import x as |
                    buffer.insert_text(', ' if allready_end_with_an_as else ' as ')#We default to the ' as ' instead of ',' because ' as ' starts with a space, which is the key we pressed. This is as opposed to functions, which default to using the comma on space by default.
                else:
                    buffer.insert_text(' ')
            elif before_line.lstrip().count(' ')==1 and before_line.lstrip().startswith('from ') and after_line==' import':#Quick shortcut for 'from * import * style importing'. Type 'f' then press space.
                # "from *| import" --> "from * import |"
                if before_line.lstrip()=='from ' and after_line.startswith(' import'):#we have no module name specified yet
                    #Switch between 'for' and 'from'
                    buffer.cursor_right(len(' import'))
                    buffer.delete_before_cursor(len('from '+' import'))
                    buffer.delete_before_cursor(13)
                    buffer.insert_text('for  in :')
                    buffer.cursor_left(len(' in :'))
                    return
                buffer.cursor_right(7)
                buffer.insert_text(' ')
            elif starts_with_any(before_line.lstrip(),'for ','except ') and after_line==':':#If we want a one-line if, elif, etc.
                if before_line.lstrip not in ['for ','except ']:#make sure it's not empty; we don't want to override completion etc
                    buffer.cursor_right(1)#Note that we exclude things we'd normally want to say, like "if x in y:"
                    buffer.insert_text('')#To trigger autocompletion
                    return
            else:
                buffer.insert_text(' ')
            buffer.insert_text('')#To trigger autocompletion

        except Exception as e:
            from rp import print_stack_trace
            print_stack_trace(e)

    @handle("?",filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,'?',event):return
        document=buffer.document
        before=document.text_before_cursor
        # after= document.text_after_cursor

        # before_line=before.split('\n')[-1]# all on same line, but before cursor
        # after_line=after.split('\n')[0]# ditto but after cursor
        if before.endswith('='):
            #x=| --> x?   (meant because I often want to use ? on something that I've just imported, and this is a small, stable way to do it)
            buffer.delete_before_cursor()
        buffer.insert_text('?')
    @handle("!",filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,'!',event):return
        document=buffer.document
        before=document.text_before_cursor
        if not before:
            buffer.insert_text('!')
            return

        # after= document.text_after_cursor

        before_line=before.split('\n')[-1]# all on same line, but before cursor
        # after_line=after.split('\n')[0]# ditto but after cursor
        if len(before)<3 and not (before_line.count("'")%2 or before_line.count('"')%2):#not in a string
            #if not in the beginning (for a ! or !! shell command) and not in string, the only time we'd want ! is for !=
            buffer.insert_text('!=')
            return
        buffer.insert_text('!')
    @handle(":",filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,':',event):return
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor

        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor
        if after_line==':':
            buffer.cursor_right(count=1)
        else:
            buffer.insert_text(':')
    @handle('=',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        import rp.r_iterm_comm as r_iterm_comm

        def buffer_insert(text):
            if(text=='=='):#text cannot be '=' because we still want to be able to use the '-=' augmented assignment
                if before_line.endswith('-'):
                    #An easy way to type '+' without the shift key: '-=', in places where that token would normally be invalid. Chosen because '-' and '=' are right next to each other.
                    buffer.delete_before_cursor()
                    buffer.insert_text('+')
                    return
            # if text in '==':
                # if before_line.endswith('=='):
                    # return
            buffer.insert_text(text)
        buffer=event.cli.current_buffer
        if handle_character(buffer,'=',event):return
        document=buffer.document
        #
        before=document.text_before_cursor
        after= document.text_after_cursor
        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor


        for l,r in {'()','[]'}:
            if (not ' ' in before_line.strip() and before_line.endswith(r) and before_line.count(l)<=before_line.count(r) and not after_line) \
                and before_line.count(l)<before_line.count(r):
                #The ')=' operator
                #The ']=' operator
                #alpha)|   --->   alpha=|(alpha)
                #foo(bar)[0])|   --->   foo(bar[0])=|(foo(bar[0]))
                buffer.delete_before_cursor()
                arg='='+l+before_line.lstrip()
                buffer.insert_text(arg)
                buffer.cursor_left(len(arg))
                buffer.cursor_right()
                return
            if endswithany(before_line,'==','<=','>=') and after_line.startswith(r):
                #i[0==|]  --->  i[0]==|
                #f(x==|)  --->  f(x)==|
                #f(x>=|)  --->  f(x)>=|
                #f(x<=|)  --->  f(x)<=|
                end=before_line[-2:]
                buffer.delete_before_cursor(2)
                buffer.cursor_right()
                buffer_insert(end)
                return

        if after_line.startswith(')'):
            if   before_line.endswith('('):
                #if f(|):   --->   if f()==|:
                buffer.cursor_right()
                buffer_insert('==')
                return
            elif before_line.endswith(','):
                #if f(x,|):  --->   if f(x)==|:
                buffer.delete_before_cursor()
                buffer.cursor_right()
                buffer_insert('==')
                return
        if starts_with_any(before_line.lstrip(),'elif','if','while'):
            # if x==y:
            #     blah
            # elif |: —> elif x==|:
            #
            # AND a cooler use-case: (because it only copies the variable from the same indent layer)
            #   if x==5:
            #       if y==6:
            #           pass
            #   elif x==7:
            #       if y==7:
            start=None
            starts={'elif','if','while'}
            for x in starts:
                if before_line.strip()==x:
                    indent=before_line[:before_line.find(x)]
                    start=x
            if start is not None:
                assert before_line.startswith(indent)
                i=-2
                try:
                    while True:
                        match=before.split('\n')[i]
                        # if match[:len(indent)].strip():#If wrong indentation level. This check is kinda rigid, maybe it would be nice to not have it...
                            # break
                        for match_start in starts:
                            if match.startswith(indent+match_start) and '==' in match:
                                match=match[match.find(match_start)+len(match_start):]
                                match=match[:match.find('==')]
                                match=match.strip()
                                if before_line[-1].strip():
                                    buffer_insert(' :')
                                    buffer.cursor_left()
                                buffer_insert(match+'==')
                                return
                        i-=1
                    return
                except:pass
        if (False or #'=' in before_line and not '==' in before_line or #We allready have some assignment operation on this line, therefore all other ='s must belong to =='s....ALMOST ALL THE TIME. There is the edge case where we say "a=b=c=d=e" etc.
            not function_comma_flag  and not after_line.startswith(')') and starts_with_any(before_line.lstrip(),'if ','elif ','while ','not ','assert ','return ','yield ','for ','lambda ','with ','not ')) and\
                not (before_line.count("'")%2 or before_line.count('"')%2):#not in a string
            #if x|:  -->  if x==|:
            #   and
            #if x==|:  -->  if x==|:
            if not re.fullmatch(r'.*(\>|\<)',before_line):
                from rp import text_to_speech as tts 
                # tts("r")
                if before_line.endswith('!'):
                    buffer_insert('=')
                    return
                if not before_line.endswith('==') or before_line.endswith('!='):
                    buffer_insert('==')
                return




        char_operators=['','+','-','*','/','%','//','**','&','|','^','>>','<<','~']
        letter_operators=['and','or','not','==','!=','>=','<=']
        var=r_iterm_comm.last_assignable_comm
        # the .=, (=, and [= operators:
        if endswithany(before_line.lstrip(),'.','(','[') and\
            (before_line.endswith('.') and not after_line.strip() or
             before_line.endswith('(') and after_line.strip() in ['',')'] or
             before_line.endswith('[') and after_line.strip() in ['',']']):
            if before_line.lstrip()=='ans.':
                #Prevent: '|' --> 'ans.|' --> 'ans=ans.'
                #Because last_assignable_comm is more useful in this case.
                buffer.delete_before_cursor(4)
                buffer.insert_text('.')
                document=buffer.document
                before_line=document.current_line_before_cursor
                before     =document.text_before_cursor
            #x.=y --> x=x.y
            #x.|  --> x=x.|
            #AND
            #x(|) --> x=x(|)
            #x[|] --> x=x[|]
            operator=before_line.lstrip()[-1]
            buffer.delete_before_cursor(count=1)
            assign_to=before_line.lstrip()
            if var and not assign_to[:-1]:
                #.|  -->  ans=ans.|
                buffer_insert(var+'='+var+operator)
                return
            buffer_insert("="+assign_to)
        elif before=='ans('and after==')':# Space + equals -> import torch;
            buffer.delete()
            buffer.delete_before_cursor(count=1000)
            buffer_insert("ans="+str(var))

        elif var and before==var+"=":
            buffer.delete_before_cursor(count=1000)
            # tts("t")
            buffer_insert("==")

        elif var and not after and before in letter_operators:# User hasn't typed anything in yet
            buffer.cursor_left(count=10000)
            buffer_insert(var)
            buffer_insert("=")
            buffer_insert(var)
            if before.isalpha():# and, or, not
                buffer_insert(" ")# We need a space
            buffer.cursor_right(count=10000)
        elif var and not after and before in char_operators:# User hasn't typed anything in yet
            buffer.cursor_left(count=10000)
            buffer_insert(var)
            buffer.cursor_right(count=10000)
            buffer_insert('=')
        else:
            buffer_insert('=')

    import os
    if os.name != 'nt':#If we are NOT running windows, which screws EVERYTHING up...
        # @handle(Keys.ControlC)
        # def _(event):
        #     buffer=event.cli.current_buffer
        #     # document=buffer.document
        #     # before=document.text_before_cursor
        #     # after= document.text_after_cursor
        #     buffer.insert_text('RETURN')


        @handle(Keys.ControlH,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):
            buffer=event.cli.current_buffer
            #On ubuntu, shift+backspace triggers this; and inserting 'HISTORY' is very annoying when we just want to backspace
            buffer.delete_before_cursor()
            # buffer.insert_text('HISTORY')
        @handle(Keys.ControlE)
        def _(event):
            #Run the buffer without erasing it or disturbing cursor position
            run_code_without_destroying_buffer(event)

        @handle(Keys.ControlW)
        def _(event):
            handle_run_cell(event)





        @handle(Keys.ControlU,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):
            buffer=event.cli.current_buffer
            buffer.insert_text('UNDO')
        @handle(Keys.ControlP,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):
            buffer=event.cli.current_buffer
            before_line=buffer.document.current_line_before_cursor
            after_line=buffer.document.current_line_after_cursor
            if before_line=='PREV' and not after_line:
                buffer.delete_before_cursor(4)
                buffer.insert_text('NEXT')
            elif before_line in ['','NEXT'] and not after_line:
                buffer.delete_before_cursor(4)
                buffer.insert_text('PREV')

    def move_arg(buffer,delta_positions:int):
        assert delta_positions in {1,-1}
        document=buffer.document
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor

        def chop_at_parenthesis_level(s:str,l:int):
            n=0
            for i,c in enumerate(s):
                if c in '([{':n+=1
                if c in '])}':n-=1
                if n==l:return s[:i]
            return s

        after_line=chop_at_parenthesis_level(after_line,-1)#Count and match parenthesis (we want 'A(B)(C)D)E' --> 'A(B)(C)D') (when we're dealing with after_line)
        before_line=before_line[::-1]
        before_line=chop_at_parenthesis_level(before_line,1)
        before_line=before_line[::-1]


        bargs=before_line.split(',')
        aargs=after_line.split(',')
        aarg=aargs[0]
        barg=bargs[-1]
        laarg=len(aarg)
        lbarg=len(barg)
        arg=barg+aarg
        larg=len(arg)

        def erase_arg():
            buffer.delete_before_cursor(lbarg)
            buffer.delete              (laarg)

        if delta_positions==1:
            if not ',' in after_line:return#Otherwise we glitch and delete the rest of it
            if len(aargs)==1:return
            erase_arg()
            buffer.delete()
            buffer.cursor_right(len(aargs[1]))#Shouldn't get index error if called properly (where cursor is AFTER a comma)
            buffer.insert_text(','+arg)
            buffer.cursor_left(larg)
        if delta_positions==-1:
            # if not ',' in after_line:return#Otherwise we glitch and delete the rest of it
            #     buffer.delete_before_cursor()
            #     buffer.delete(laarg)
            #     buffer.cursor_left(lbarg)
            #     buffer.insert_text(arg+',')
            erase_arg()
            buffer.delete_before_cursor()
            buffer.cursor_left(len(bargs[-2]))
            buffer.insert_text(arg+',')
            if len(bargs)>2:
                buffer.cursor_left(larg+1)




    @handle('<',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,'<',event):return
        document=buffer.document
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        if before_line.endswith(','):
            #Swap arguments around parenthesis! (Warning: Doesn't handle parenthesis inside strings as an edge case)
            #(apple,f(x),|['bananna'])   --->   (apple,|['bananna'],f(x))
            try:move_arg(buffer,-1)
            except:print("JAM")
            return
        buffer.insert_text('<')
    @handle('>',filter=~vi_mode_enabled&microcompletions_enabled)
    def _(event):
        buffer=event.cli.current_buffer
        if handle_character(buffer,'>',event):return
        document=buffer.document
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        if before_line.endswith(','):
            #Swap arguments around parenthesis! (Warning: Doesn't handle parenthesis inside strings as an edge case)
            #(apple,|f(x),['bananna'])   --->   (apple,['bananna'],f(x))
            try:move_arg(buffer,1)
            except:print("JAM")
            return
        buffer.insert_text('>')
    def do_backspace(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        if self_dot_var_equals_var(buffer,'\b') and after_line.strip()!='=':
            #self.foo|=foo   --->   self.fo|=fo
            return
        if before_line.endswith(' as '):
            #(I'm often trigger-happy with the space-bar on using imports, and try to correct it with backspace. This saves me some time...)
            #import osaidf as |   --->   import osaidf
            buffer.delete_before_cursor(len(' as '))
            return
        if before_line.endswith(', '):
            #import osaidf as c, |   --->   import osaidf as c|
            buffer.delete_before_cursor(len(', '))
            return
        selection_tuples=list(document.selection_ranges())
        if not selection_tuples:
            before=document.text_before_cursor
            after= document.text_after_cursor
            if not after and before =='ans.':
                buffer.delete_before_cursor(len(before))
                return
            if not before_line.strip():
                #(backspace entire indent when it's empty. example:)
                #def f(x):
                #····|return x
                #  --->
                #def f(x):return x
                buffer.delete_before_cursor(len(before_line))
            bl=before_line.lstrip()
            al=after_line.rstrip()
            if bl+'|'+al in {'from | import','for | in :','while |:','if |:','elif |:','except |:','lambda :','with |:'}|\
                            {'import |','return |','return|','pass|','else:|','yield |','assert |'}:
                            #Delete from both sides of the cursor on constructs we tend to make automatically (to make it less annoying)
                buffer.cursor_right(len(al))
                buffer.delete_before_cursor(len(bl+al))
                return
            if before and after:
                if after_line.strip()in {':','():'} and before_line.lstrip() in {'def ','while ','for ','class ','if ','elif ','else','except ','lambda ','with ','try'}:
                    #  '    def |:'   -->   '    |'
                    buffer.delete(len(after_line))
                    buffer.delete_before_cursor(len(before_line.lstrip()))
                    return
                pair=before[-1]+after[0]
                if pair in ['()','{}','[]',"''",'""']:
                    #  'f(|)'   -->   'f|'
                    buffer.cursor_right(count=1)
                    buffer.delete_before_cursor(count=2)
                    buffer.insert_text('')#trigger autocompletion
                    return
            buffer.delete_before_cursor(count=1)
        else:
            buffer.cut_selection()
        buffer.insert_text("")#Using this to trigger autocompletion on backspace
    def alt_backspace_char_class(event):
        #get char before cursor and distinguish between whitespace, alphanumerics, and other chars
        c=event.cli.current_buffer.document.text_before_cursor
        if not c:
            return None#no chars behind cursor
        c=c[-1]
        if c.isalnum():
            return 1
        elif not c.strip():
            return 2
        else:
            return 3

    @handle(Keys.Backspace,eager=True)
    def _(event):
        if meta_pressed():
            do_backspace(event)#We expect at least two characters to dissapear; so eat through one-char wide spaces (for example, "def |a()" --> "|a()", not "def|a()")
            c=alt_backspace_char_class(event)
            while c is not None and c==alt_backspace_char_class(event):
                do_backspace(event)
            return
        do_backspace(event)

    @handle(Keys.Right)
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        selection_tuples=list(document.selection_ranges())
        for t in selection_tuples:
            buffer._set_cursor_position(t[1])
            buffer.exit_selection()
        else:
            cpos=buffer.cursor_position
            buffer.cursor_right(1)
            if buffer.cursor_position==cpos:
                buffer=event.cli.current_buffer
                buffer._set_cursor_position(min(buffer.cursor_position + 1,len(buffer.document.text)))
            # buffer.cursor_right(0)# Gets stuck on ends of lines. Not as good as the new version

    @handle(Keys.Left)
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        selection_tuples=list(document.selection_ranges())
        for t in selection_tuples:# Handle arrow-keys on selection by putting the cursor on beginning or end of selection
            buffer._set_cursor_position(min(t[0]+1,len(buffer.document.text)))
            buffer.exit_selection()
        else:
            cpos=buffer.cursor_position
            buffer.cursor_left(1)
            if cpos==buffer.cursor_position:
                buffer=event.cli.current_buffer
                buffer._set_cursor_position(max(buffer.cursor_position - 1,0))

    @handle(Keys.Down)
    def _(event):
        buffer=event.cli.current_buffer
        if meta_pressed():
            buffer.cursor_down(10)
        else:
            buffer.auto_down(ryan_allow_completion_navigation=False)
        # document=buffer.document
        # assert isinstance(buffer,Buffer)
        # if not has_selected_comlpetion(buffer):
            
        # if has_selected_completion(buffer) or not '\n' in buffer.document.text:
            # buffer.auto_down()# Will select next completion
            # try:
            #     if not has_selected_completion(buffer) or not '\n' in buffer.document.text3:#
            #         buffer.auto_down()# So we don't get stuck when we come back around again
            # except:pass
        # else:
        #     temp=buffer.complete_state
        #     try:
        #         buffer.complete_state=False
        #         buffer.auto_down()# Will select next completion
        #     finally:
        #         buffer.complete_state=temp

    @handle(Keys.Up)
    def _(event):
        buffer=event.cli.current_buffer
        if meta_pressed():
            buffer.cursor_up(10)
        else:
            buffer.auto_up(ryan_allow_completion_navigation=False)
            return
            assert isinstance(buffer,Buffer)
            if has_selected_completion(buffer):#  Up is the only one that can initially select a history item
                buffer.auto_up()# Will select next completion
                if not has_selected_completion(buffer):
                    buffer.auto_up()# So we don't get stuck when we come back around again
            else:
                temp=buffer.complete_state
                try:
                    buffer.complete_state=False# So we don't select a completion
                    buffer.auto_up()# Will select next completion
                finally:
                    buffer.complete_state=temp





    @handle(Keys.ControlZ)
    def _(event):
        buffer=event.cli.current_buffer
        # print(buffer._redo_stack)
        buffer.undo()

    @handle(Keys.ControlY)
    def _(event):
        buffer=event.cli.current_buffer
        # print(buffer._redo_stack)
        buffer.redo()

    @handle(Keys.ControlQ)
    def _(event):
        #Abandon the current buffer. But still save it to history.

        buffer=event.cli.current_buffer
        buffer.append_to_history()
        event.cli.abort()
        # print(buffer._redo_stack)
        # buffer.redo()

    import rp.r_iterm_comm as r_iterm_comm
    @handle(Keys.ControlV)# On mac this is alt+z
    def _(event):
        if meta_pressed(clear=True):
            edit_event_buffer_in_vim(event)
        else:
            buffer=event.cli.current_buffer
            from rp import string_from_clipboard
            clip=r_iterm_comm.clipboard_text
            try:
                clip=string_from_clipboard()
                buffer.cut_selection()
                buffer.insert_text(clip)
            except:
                pass# Paste failed


    @handle(Keys.ControlC)# ,filter=has_selection)# On mac this is alt+z
    def _(event):
        buffer=event.cli.current_buffer
        selection_tuples=list(buffer.document.selection_ranges())

        #region
        if not selection_tuples:
            selection_tuples=[]
            line=buffer.document.current_line
            to_copy="\n" + line# ' ' * (len(line)-len(line.lstrip()))
            buffer.cursor_right(12323213)
        else:
            to_copy=""
            for t in selection_tuples:
                to_copy+=buffer.document.text[t[0]:t[1]+1]
        r_iterm_comm.clipboard_text=to_copy
        from rp import string_to_clipboard
        try:
            string_to_clipboard(to_copy)
        except:
            pass# Copy failed


    def inc_dec(inc_or_dec:str):# ++ ⟶ +=1
        #increment or decrement
        @handle(inc_or_dec,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):
            buffer=event.cli.current_buffer
            if handle_character(buffer,inc_or_dec,event):return
            document=buffer.document
            before=document.text_before_cursor
            before_line=document.current_line_before_cursor
            after_line=document.current_line_after_cursor
            after= document.text_after_cursor
            current_line= document.current_line
            above_line=    line_above(buffer)
            single_line=above_line is None
            # import r_iterm_comm
            # if not after and r_iterm_comm.last_assignable_comm and before[-1]==inc_or_dec:# So you can do ++ -> assignable ++= (because +=1 -> assignable+=1)
            #     buffer.cursor_left(count=1000)
            #     buffer.insert_text(r_iterm_comm.last_assignable_comm)
            #     buffer.cursor_right(count=1000)
            #     return
            # print('GAGAGAGA')

            from rp import is_namespaceable
            if inc_or_dec == '-' and all(is_namespaceable(x) for x in before_line if x not in ' ') and starts_with_any(before_line.lstrip(),'def ','class '):# When writing the title of a function, you don't have to use _ you can type - and it will turn it into _
                #(on -)
                #def |(): ---> def _|():
                #     AND
                #def f|(): ---> def _f_|():
                buffer.insert_text('_')
                return
            if inc_or_dec=='-' :
                if is_namespaceable(before_line.strip()) and before_line.rstrip()==before_line and not single_line:
                    #If multiline, and we're starting a line, and we're continuing some variable name, assume that we don't want to create an expression.
                    #Example:
                    #def f():
                    #   x|   ---->    x_
                    buffer.insert_text('_')
                    return

                if before_line.endswith('for ')and starts_with_any(after_line,' in)',' in}',' in]'):
                    buffer.insert_text('_')
                    buffer.cursor_right(3)
                    buffer.insert_text(' ')
                    return
                skip=False
                token,name,found=token_name_found_of_interest(before_line)
                if before_line=='from 'and after_line==' import':
                    buffer.cursor_right(1233)
                    buffer.delete_before_cursor(len('from  import'))
                elif found:
                    # print("NAME IS "+name)
                    if name=='f'==before_line.strip() and not callable(token):
                        buffer.delete_before_cursor()
                    else:
                        skip=True   
                if not skip:
                    buffer.insert_text('for _ in :')
                    buffer.cursor_left()
                    return 

            if (inc_or_dec=='+' or False) and (after_line.startswith('"') or after_line.startswith("'")):
                #(on + followed by +) (for combining strings more easily)
                #"Hello"|"World"  --->  "Hello"|+"World"  --->  "Hello"+|+"World"
                #       AND
                #'Hello'|'World'  --->  'Hello'|+'World'  --->  'Hello'+|+'World'
                buffer.insert_text('+')
                buffer.cursor_left()
                return
            # if (inc_or_dec=='-' or True) and (endswithany(before_line,'"',"'") and after_line.startswith("+")):
            #     #On pressing the '-' key, (because string literals don't implement the '-') operator
            #     #"Hello"|+"World"  --->  "Hello"+|+"World"
            #     buffer.insert_text('+')
            #     return

            if inc_or_dec=='-' and before_line.lstrip()=='for ' and after_line.rstrip()==' in :':
                #(on -)
                #for | in : --> for _ in |:
                buffer.insert_text('_')
                buffer.cursor_right(len(' in '))
                return
            if len(before_line.strip())>1 and before and before[-1]==inc_or_dec and is_namespaceable(before_line[:-1].lstrip()):
                #(on +) x+|  --->  x+=1
                #       AND
                #(on -) x-|  --->  x-=1
                if not after_line:
                    buffer.insert_text("=1")
                else:
                    buffer.insert_text(inc_or_dec)
                    buffer.cursor_left()
            elif inc_or_dec=='-' and before_line.endswith('-'):
                #becuase then we dont have to reach for the shify key (default blank vairable is _ in for loops)
                #print(-|) ---> print(_|)
                buffer.delete_before_cursor()
                buffer.insert_text('_')
            elif inc_or_dec=='-' and before_line.endswith('-=1'):
                #(when we wanted to make an underscore but got -=1, just press - again...)
                #x-=1| ---> x_| 
                buffer.delete_before_cursor(3)
                buffer.insert_text('_')
            else:
                buffer.insert_text(inc_or_dec)
            # if inc_or_dec=='+':
            #     print("ewfoijfdsijoijowfijofejio")
            #     if before.endswith('+') and after and after[0] in '\'"':
            #         buffer.cursor_left()
    inc_dec('+')
    inc_dec('-')

    # @handle("h")
    # def sploo(x):
    #     print("A")
    # @handle("h")
    # def sploo(x):
    #     print("B")


    bracket_pairs={"()","[]","{}"}
    def thing(begin,end):
        @handle(begin,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):# Parenthesis completion
            buffer=event.cli.current_buffer
            if handle_character(buffer,begin,event):return
            if(begin=='('):
                document=buffer.document
                before_line=document.current_line_before_cursor
                after_line =document.current_line_after_cursor
                if regex_match(before_line.lstrip(),r'for\s+\w+\s+in\s+len'):
                    #for x in len|   -->  for x in range(len(|))
                    buffer.delete_before_cursor(3)
                    buffer.insert_text('range(len())')
                    buffer.cursor_left(2)
                    return
                if before_line.rstrip().startswith('def ') and after_line.strip()=='():':
                    #def f|() --> def f(|):
                    buffer.cursor_right()
                    return
            if not surround(buffer,begin,end):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                buffer.insert_text(begin)
                if after.strip()==':' or not after or after[0].isspace() or before and before[-1]+after[0]in bracket_pairs or document.find_matching_bracket_position()!=0:
                    buffer.insert_text(end)
                    buffer.cursor_left(count=1)
        @handle(end,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event):# Parenthesis completion
            buffer=event.cli.current_buffer
            if handle_character(buffer,end,event):return
            if not surround(buffer,begin,end):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                if not after or after[0]!=end:#  or before.count(begin)>before.count(end):#Last part is checking for parenthesis matches. I know somewhere there's a way to do this already thats better and isnt confused by strings but idk where that is
                    buffer.insert_text(end)
                else:
                    buffer.cursor_right(count=1)
    for bracket_pair in bracket_pairs:
        thing(bracket_pair[0],bracket_pair[1])

    def surround(buffer,begin,end):
        from rp.prompt_toolkit.selection import SelectionState
        document=buffer.document
        text=document.text
        selection_tuples=list(document.selection_ranges())
        for range in selection_tuples:
            buffer.document=Document(text=text[:range[0]]+begin+text[range[0]:range[1]+1]+end +text[range[1]+1:],cursor_position=range[0]+1,selection=None)
            buffer.document._selection=SelectionState(original_cursor_position=range[1]+1,type=document.selection.type)
        # exec(mini_terminal)
        # from rp.rp_ptpython.utils import get_jedi_script_from_document
        # script=get_jedi_script_from_document(document,r_iterm_comm.globa,r_iterm_comm.globa)
        # script.call_signatures()
        return bool(selection_tuples)# Returns whether we have a selection
    def thing2(char):
        @handle(char,filter=~vi_mode_enabled&microcompletions_enabled)
        def _(event,filter=has_selection):# Parenthesis completion
            buffer=event.cli.current_buffer
            if handle_character(buffer,char,event):return
            if not surround(buffer,char,char):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                before_line=document.current_line_before_cursor
                after_line=document.current_line_after_cursor

                if after.startswith(char) and not before.endswith(char):
                    buffer.cursor_right()
                # else:
                #     buffer.insert_text(char)
                #     buffer.cursor_left()
                #     buffer.insert_text(char)

                elif (before and after and before[-1]+after[0] in {"[]","()","{}",",}",",)",",]",'+)','+,','+}','+]'}) or (not after_line or not before and not after or before and after and before[-1]in'(=!#%&*+,-./:;<>^|~' and after[0]in')=!#%&*+,-./ :;<>^|~' or before and after and before[-1]+after[0] in 2*char):
                    #| --> "|"
                    #| --> '|'
                    buffer.insert_text(char)
                    buffer.cursor_left()
                    buffer.insert_text(char)
                elif before.endswith(char):
                    #For splitting strings into two pieces
                    #(" pressed twice)
                    #"Hello|World!"  -->  "Hello"|World!"  -->  "Hello"|"World!"
                    buffer.insert_text(char)
                    buffer.cursor_left()
                else:
                    buffer.insert_text(char)

    for char in '"\'':
        thing2(char)
    @handle(',',filter=~vi_mode_enabled&microcompletions_enabled)  
    def _(event):
        #Comma event
        buffer=event.cli.current_buffer
        if handle_character(buffer,',',event):return
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        if before_line.lstrip()=='for ' and after_line.rstrip()==' in :':
            #for | in:  --->  for i,e in enumerate(|):
            buffer.insert_text('i,e')
            buffer.cursor_right(len(' in '))
            buffer.insert_text('enumerate()')
            buffer.cursor_left()
            return
        if before_line.endswith('for ') and starts_with_any(after_line,' in]',' in)',' in}'):
            #[x for | in]  --->  [x for i,e in enumerate(|)]
            buffer.insert_text('i,e')
            buffer.cursor_right(len(' in'))
            buffer.insert_text(' enumerate()')
            buffer.cursor_left()
            return
        if before_line.endswith(',') and after_line.startswith(','):
            #We prevent from accidently putting in more parenthesis than make sense
            #x,|,y  --->  x,|,y    (no change)...
            return
        if before_line.endswith(',') and \
            not before_line.endswith(',,'):#...however, we do allow ,,,,,,,:   x,,|y  --->  x,,,|y  
            #y,|x  -->  y,|,x
            buffer.insert_text(',')
            buffer.cursor_left()
            return
        if before_line.endswith('-'):
            #Turning the '-' into a '_' where a '-' would be syntactically invalid
            buffer.delete_before_cursor()
            buffer.insert_text('_')
            
        if after_line.startswith(','):
            #f(a,b,c|,)   --->   [a,b,c,|)
            #(don't waste commas)
            buffer.cursor_right()
            return
        if not (before_line.endswith(',') and after_line.startswith(']')):
            #[x,y|]  -->  [x,y,|]
            #       AND
            #[x,y,|]  -->  [x,y,|]
            #for when I spam the [12,3123,12,31,23,12,31,23,123,1,23,123,12,31,23] and don't want accidental ',,'s
            buffer.insert_text(',')
            return

    # @handle(',')
    # def thing3(char):
    #     @handle(char)
    #     def _(event,filter=~has_selection):# Parenthesis completion
    #         buffer=event.cli.current_buffer
    #         document=buffer.document
    #         before=document.text_before_cursor
    #         after= document.text_after_cursor
    #         if before.endswith('(') and after.startswith(')'):
    #             buffer.cursor_right()
    #         buffer.insert_text(char)
    # for char in '!#%&*,./:;<>^|~':# + and - allready taken
    #     thing3(char)

    @handle(Keys.Delete)
    def _(event):
        event.cli.current_buffer.delete()

    @handle(Keys.ControlSpace)# For commenting
    def _(event):  # Parenthesis completion
        # def toggle_comment_on_line(x):
        #     y=x.lstrip()
        #     if y.startswith("#"):# Line is commented out
        #         i=x.find('#')
        #         return x[:i]+x[i+1:]
        #     l=len(x)-len(y)
        #     return l*' ' +'#' + y

        buffer=event.cli.current_buffer
        # buffer.transform_current_line(toggle_comment_on_line)
        # buffer.insert_text("ⵁ")
        # buffer.delete_before_cursor
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        buffer.cursor_left(10000)
        lstrip=current_line.lstrip()
        w=len(current_line)-len(lstrip)
        buffer.cursor_right(w)
        if current_line.lstrip().startswith('#'):
            buffer.delete()
        else:
            buffer.insert_text('#')
        buffer.cursor_down()
    #endregion

    @handle(Keys.ControlT,eager=True)
    def _(event):
        """
        Cursor to top.
        """
        event.cli.current_buffer.history_backward()
    @handle(Keys.ControlB,eager=True)
    def _(event):
        """
        Cursor to top.
        """
        event.cli.current_buffer.history_forward()

    @handle(Keys.ControlL)
    def _(event):
        """
        Clear whole screen and render again -- also when the sidebar is visible.
        """
        event.cli.renderer.clear()
    @handle(Keys.F2)
    def _(event):
        """
        Show/hide sidebar.
        """
        python_input.show_sidebar = not python_input.show_sidebar

    @handle(Keys.F3)
    def _(event):
        """
        Select from the history.
        """
        python_input.enter_history(event.cli)

    @handle(Keys.F4)
    def _(event):
        """
        Toggle between Vi and Emacs mode.
        """
        event.cli.vi_state.input_mode = 'vi-navigation'
        python_input.vi_mode = not python_input.vi_mode#If we're switching out of RP-Emacs, its most likely because we want them good ol' vim bindings for manipulating text. 
        # print(event.cli.vi_state)
        # python_input.vi_mode = not python_input.vi_mode

    @handle(Keys.F6)
    def _(event):
        """
        Enable/Disable paste mode.
        """
        python_input.paste_mode = not python_input.paste_mode

    @handle(Keys.F1)
    def _(event):
        """
        Enable/Disable mouse mode.
        """
        python_input.enable_mouse_support = not python_input.enable_mouse_support

    @handle(Keys.F8)
    def _(event):
        """
        Enable/Disable microcopletions.
        """
        python_input.enable_microcompletions = not python_input.enable_microcompletions

    @handle(Keys.F7)
    def _(event):
        """
        Enable/Disable line wraps.
        """
        python_input.wrap_lines = not python_input.wrap_lines
        
    def number_of_leading_spaces(string):
        i=0
        for x in string:
            if x==' ':
                i+=1
            else:
                break
        return i
    @handle(Keys.Tab, filter= ~sidebar_visible & ~has_selection & TabShouldInsertWhitespaceFilter())
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        buffer=event.cli.current_buffer
        if handle_character(buffer,'\t',event):return
        buffer.insert_text('    ')
        after_line = buffer.document.current_line_after_cursor
        before_line = buffer.document.current_line_after_cursor
        # N=number_of_leading_spaces(before_line+after_line)
        # if not before_line.strip() and N%4:
            # buffer.insert_text(' '*(4-N%4))
            # return
        if after_line.lstrip():
            buffer.cursor_left(4)
    #region  Ryan Burgert Method

    @handle(Keys.BackTab,filter=IsMultiline())
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        # from r import mini_terminal
        buffer=event.cli.current_buffer
        after_line = buffer.document.current_line_after_cursor
        before_line = buffer.document.current_line_before_cursor
        # flag=before_line.strip() and before_line#has some whitespace characters on it
        N=min(4,number_of_leading_spaces(before_line+after_line))
        # i=0
        if not after_line.strip() and not before_line.strip():
            for i in range(4):
                if buffer.document.current_line_before_cursor:
                    buffer.delete_before_cursor(1)

            return
        for _ in range(N):
            try:
                if buffer.document.current_line.startswith(' ') or not has_selected_completion(buffer):
                    flag=False
                    if not buffer.document.current_line_after_cursor:#Otherwise it might jump to another line if we dont do this first
                        buffer.cursor_left()
                        flag=True
                    buffer.transform_current_line(lambda x:x[1:])
                    if not flag and buffer.document.current_line_before_cursor.strip():
                        buffer.cursor_left()
                # buffer.transform_current_line(lambda x:(x[1:]if x.startswith(' '*4)else x.lstrip()))
                # buffer.transform_current_line(lambda x:(x[4:]if x.startswith(' '*4)else x.lstrip()))
            except:
                pass# Error migght happen if cursor is in bad place. Not sure what to do about that; but its an edge case so I'm just gonna squelch it.
        #endregion
        # if flag:
            # buffer.cursor_right(i)
    from rp import ring_terminal_bell ,text_to_speech
    def try_to_unindent(buffer,*matching_prefixes):
        b=buffer
        current_line = b.document.current_line
        after_line = b.document.current_line_after_cursor
        before_line = b.document.current_line_before_cursor
        before=b.document.text_before_cursor
        after= b.document.text_after_cursor
        l=find_level(before,*matching_prefixes)
        if l is None:
            # ring_terminal_bell()
            # text_to_speech('a')
            return#We're at a bit of a loss on what to do here...
        i=get_indent(current_line)
        d=len(i)-l
        L=len(before_line.lstrip())
        # ring_terminal_bell()
        buffer.cursor_left(L)
        buffer.delete_before_cursor(d)
        buffer.cursor_right(L)
        # text_to_speech('b')
    indent_block_matches={
            'except':{'try','finally'},#cant add except for buggy reasons (it sees itself when trying to unindent and thus doesnt unindent)
            'finally':{'try','except','else'},
            'else':{'if','elif','for','while','except'},
            'elif':{'if'},#cant add elif for buggy reasons (it sees itself when trying to unindent and thus doesnt unindent)
            }
    def try_to_autounindent(buffer):
        b=buffer
        current_line = b.document.current_line
        after_line = b.document.current_line_after_cursor
        before_line = b.document.current_line_before_cursor
        before=b.document.text_before_cursor
        after= b.document.text_after_cursor
        if current_line.rstrip().endswith(':'):
            
            for m in indent_block_matches:
                if current_line.lstrip().startswith(m):
                    try_to_unindent(buffer,*indent_block_matches[m])
                    # text_to_speech('c')
                    return
        # text_to_speech('d')
        return



    @handle(Keys.ControlJ, filter= ~vi_mode_enabled & ~sidebar_visible & ~has_selection &( ViInsertMode() | EmacsInsertMode()) &HasFocus(DEFAULT_BUFFER) )#& IsMultiline())
    def _(event):
        """
        Behaviour of the Enter key. enter key

        Auto indent after newline/Enter.
        (When not in Vi navigaton mode, and when multiline is enabled.)
        """
        b = event.current_buffer
        buffer=b
        if handle_character(buffer,'\n',event):return
        empty_lines_required = python_input.accept_input_on_enter or 10000
        text=current_line=after_line=before_line=before=after=above_line=None
        def refresh_strings_from_buffer():
            nonlocal text,current_line,after_line,before_line,before,after,above_line
            text =         b.document.text_after_cursor
            current_line = b.document.current_line
            after_line =   b.document.current_line_after_cursor
            before_line =  b.document.current_line_before_cursor
            before=        b.document.text_before_cursor
            after=         b.document.text_after_cursor
            above_line=    line_above(b)
        refresh_strings_from_buffer()

        single_line = above_line is None
        def auto_pass():#try automatically adding a 'pass' keyword if it helps to avoid a syntax error; return True if we add a 'pass'
            if not single_line and not current_line.strip() and above_line.rstrip().endswith(':'):
                #Implicitly add 'pass' when hitting enter below an if/for/def block (which would otherwise be a syntax error because of the autounindent)
                buffer.insert_text('pass')
                refresh_strings_from_buffer()
                return True
            return False
        auto_pass()
        if before_line.endswith(' enumerate(') and after_line.startswith(')'):
            #for i,e in enumerate(|):   --->   for i,e in enumerate(ans):\n|
            buffer.insert_text('ans')
        elif before_line.lstrip()=='f,' and not 'f' in r_iterm_comm.globa:
            #f,|   --->   for i,e in enumerate(ans):\n|
            buffer.delete_before_cursor(2)
            buffer.insert_text('for i,e in enumerate(ans):')
        for end in ')]}':
            if current_line.endswith(','+end) and before_line.endswith(',') and after_line==end:
                #print(ans,|)   --->   print(ans|)
                #[1,2,3,|]      --->   [1,2,3|]
                #{1,2,3,|}      --->   {1,2,3|}
                buffer.delete_before_cursor()
                refresh_strings_from_buffer()
        # if endswithany(before_line,',-','(-','[-','{-'):
            #A BETTER VERSION OF THIS HAS BEEN MOVED TO MISC TWEAKS WITH A BUG FIX 
            #BUG IN THIS BLOCK: On \n: ‹(-|10)› –––>  ‹(_10)\n|›
            #Completing the '-' dash to the underscore variable '_' in one of many instances where it makes sense
            #print(-|) ---> print(_)\n|
            # buffer.delete_before_cursor()
            # buffer.insert_text('_')
            # refresh_strings_from_buffer()
        #a line with a sigle letter on it is useless, so let's make it useful.
        #TODO: Make it semantically aware: make 'e' write 'except' when in a try block, and 'else' when in an 'if' or after a 'for' block. Same logic SHOULD (but doesn't yet) apply to all of these (see below line)
        if before_line.lstrip()=='#':
            #'#|' ---> '|'  (so we can hit enter twice to break out of a comment)
            buffer.delete_before_cursor()
            return
        continue_comment=before_line.lstrip().startswith('#')
        if before_line=='from 'and after_line==' import':
            #With current completions, which come in the next few 'if' blocks, we get this:
            #from | import ---> for _ in ans:\n\t
            buffer.delete_before_cursor(len('from '))
            buffer.delete(len(' import'))
            buffer.insert_text('for  in :')
            buffer.cursor_left(len(' in :'))
            refresh_strings_from_buffer()

        if before_line.lstrip()=='for 'and after_line.rstrip()==' in :':
            #for | in :   --->   for _ in |:   (we don't stop here, it eventually goes to "for _ in ans": see the next 'if' block)
            buffer.insert_text('_')
            # buffer.insert_text('ans')
            # 
            refresh_strings_from_buffer()

        if after_line.rstrip()==' in :':
            buffer.cursor_right(len(' in '))
            # 
            refresh_strings_from_buffer()

        if after_line.rstrip()==':':
            #for spaoddsg in |:   --->   for spaoddsg in ans:
            spl=before_line.split()
            if len(spl)==3 and spl[0]=='for' and spl[2]=='in':
                buffer.insert_text('ans')
                # 
                refresh_strings_from_buffer()
        if not (single_line and token_exists(current_line.strip())):
            import rp.r_iterm_comm
            enter_completable_keywords=dict(fo='for _ in ans:',e='else:',t='try:',b='break',c='continue',f='finally:',p='pass',r='return',y='yield',d='def _():',w='while True:',i='if True:')#enter-completion of keywords that don't need to take arguments
            single_line_enabled_keywords={'fo','f','i','t','d','w'}-set(rp.r_iterm_comm.globa)
            keyword=current_line.lstrip()
            if single_line and before_line and 'class '.startswith(before_line) and not after_line:
                #c|   --->  class _:\n|
                #cla|   --->  class _:\n|
                buffer.delete_before_cursor(100)
                buffer.insert_text('class _:\n    ')
                return
            if (not single_line or keyword in single_line_enabled_keywords) and keyword in enter_completable_keywords:
                #Examples:
                #'e|' ---> 'else:\n    |'
                #'t|' ---> 'try:\n    |'
                #'r|' ---> 'return\n|'
                char=current_line.lstrip()
                replacement=enter_completable_keywords[char]
                level=lambda candidate:find_level(before,*indent_block_matches[candidate])
                if replacement=='else:':
                    exl=level('except')
                    ell=level('else')
                    if ell is None and exl is not None or exl is not None and exl>ell:
                        text_to_speech('q')
                        replacement='except:'
                if '_' in replacement:
                    if single_line:
                        replacement=replacement.replace('_','ans')
                if not 'try' in text and replacement=='finally:':
                    replacement='for _ in ans:'
                buffer.delete_before_cursor(len(char))
                refresh_strings_from_buffer()
                indent=current_line
                assert not current_line.strip()
                # if auto_pass():buffer.insert_text('\n'+indent)
                buffer.insert_text(replacement)
                try_to_autounindent(buffer)   
                refresh_strings_from_buffer()

            if not after and before.startswith('import ') and before.endswith(', '):
                #Sometimes when using my import microcompletions I hit the space key by accident, which causes this:
                #import w as x,y as z, |
                #Which is a syntax error. Autocorrect it to:
                #import w as x,y as z
                buffer.delete_before_cursor(2)
            if before_line.lstrip() in ('def ','class ') and current_line.strip() in ('def ():','def (self):','class :') :
                #def |():  --->  'def ans():\n|'  or 'def _():\n|' 
                #class |:  --->  class _:\n|
                if single_line:
                    buffer.insert_text('ans')
                else:
                    buffer.insert_text('_')
            #we might have made some changes; refreshing:
            refresh_strings_from_buffer()

        # if  (after_line.startswith('"""') and before_line.endswith ('"""')) or\
        #     (after_line.startswith("'''") and before_line.endswith ("'''")):
        #     print("ASOID")
        #     b.insert_text('\n')
        #     return
        def at_the_end(b):
            """ we consider the cursor at the end when there is no text after
            the cursor, or only whitespace. """
            assert isinstance(b,Buffer)
            refresh_strings_from_buffer()
            #region RYAN BURGERT STUFF
            text=after
            assert isinstance(text,str)
            if self_dot_var_equals_var(buffer) or (before_line.lstrip() and not beginswithany(before_line[::-1],' ',',',':',';','{','[','"""',"'''") and not '"""' in before_line and not "'''" in before_line and '(' in before_line or beginswithany(before_line.lstrip(),'for ','def ','lambda ','while ','with ','if ','except ','try ') or not text or text.split('\n')[0] in ["):",']',')','}',':']):# Presumably at the end of def( a,b,c,d,e^): where ^ is cursor
                event.cli.current_buffer.cursor_right(1000000)# Move cursor to end of line then proceed as normal
                text = b.document.text_after_cursor
            #endregion
            return text == '' or (text.isspace() and not '\n' in text)
        if single_line:#single-line commands are entered immediately.
            if not current_line.rstrip().endswith(':') \
            and not     endswithany(current_line.lstrip(),'@',"'''",'"""') \
            and not starts_with_any(current_line.lstrip(),'@',"'''",'"""'):
                b.accept_action.validate_and_handle(event.cli, b)
                # print("JI")
                # return
        # if at_the_end(b):# TODO Stuff here
            # print("""def a b c d e (enter)
# ->
# def a(b,c,d,e):
# """)
        if python_input.paste_mode:
            # In paste mode, always insert text.
            b.insert_text('\n')

        elif at_the_end(b) and b.document.text.replace(' ', '').endswith('\n' * (empty_lines_required - 1)):
            if b.validate():
                # When the cursor is at the end, and we have an empty line:
                # drop the empty lines, but return the value.
                b.document = Document(
                    text=b.text.rstrip(),
                    cursor_position=len(b.text.rstrip()))
                b.accept_action.validate_and_handle(event.cli, b)
        else:
            auto_newline(b)
            if continue_comment:
                #'#Foo|'-->'#Foo\n#|'
                buffer.insert_text('#')


    @handle(Keys.ControlD, filter=~sidebar_visible & Condition(lambda cli:
            # Only when the `confirm_exit` flag is set.
            python_input.confirm_exit and
            # And the current buffer is empty.
            cli.current_buffer_name == DEFAULT_BUFFER and
            not cli.current_buffer.text))
    def _(event):
        """
        Override Control-D exit, to ask for confirmation.
        """
        python_input.show_exit_confirmation = True




    @handle(Keys.F5, filter=Condition(lambda cli: python_input.show_sidebar))#Only activate when the sidebar is visible
    def _(event):
        from rp.prompt_toolkit.shortcuts import confirm
        from rp import input_yes_no,clear_terminal_screen

        import rp.rp_ptpython.python_input as rrpi

        clear_terminal_screen()
        if input_yes_no("Ryan Python\nPlease Confirm: Are you sure you want to this menu's settings (the F2 menu)?\nIf you choose yes, they'll be saved for the next time you boot rp.\nNote: You can also do this with the 'PT SAVE' command."):
            run_arbitrary_code_without_destroying_buffer("PT SAVE",event)
            print("Saved the F2 menu's current settings; you'll see them again when you reboot rp!")
        else:
            clear_terminal_screen()
            event.cli.renderer.clear()

    return registry


def load_sidebar_bindings(python_input):
    """
    Load bindings for the navigation in the sidebar.
    """
    registry = Registry()

    handle = registry.add_binding
    sidebar_visible = Condition(lambda cli: python_input.show_sidebar)

    @handle(Keys.Up, filter=sidebar_visible)
    @handle(Keys.ControlP, filter=sidebar_visible)
    @handle('k', filter=sidebar_visible)
    def _(event):
        " Go to previous option. "
        python_input.selected_option_index = (
            (python_input.selected_option_index - 1) % python_input.option_count)

    @handle(Keys.Down, filter=sidebar_visible)
    @handle(Keys.ControlN, filter=sidebar_visible)
    @handle('j', filter=sidebar_visible)
    def _(event):
        " Go to next option. "
        python_input.selected_option_index = (
            (python_input.selected_option_index + 1) % python_input.option_count)

    @handle(Keys.Right, filter=sidebar_visible)
    @handle('l', filter=sidebar_visible)
    @handle(' ', filter=sidebar_visible)
    def _(event):
        " Select next value for current option. "
        option = python_input.selected_option
        option.activate_next()

    @handle(Keys.Left, filter=sidebar_visible)
    @handle('h', filter=sidebar_visible)
    def _(event):
        " Select previous value for current option. "
        option = python_input.selected_option
        option.activate_previous()

    @handle(Keys.ControlC, filter=sidebar_visible)
    @handle(Keys.ControlG, filter=sidebar_visible)
    @handle(Keys.ControlD, filter=sidebar_visible)
    @handle(Keys.ControlJ, filter=sidebar_visible)
    @handle(Keys.Escape, filter=sidebar_visible)
    def _(event):
        " Hide sidebar. "
        python_input.show_sidebar = False

    return registry


def load_confirm_exit_bindings(python_input):
    """
    Handle yes/no key presses when the exit confirmation is shown.
    """
    registry = Registry()

    handle = registry.add_binding
    confirmation_visible = Condition(lambda cli: python_input.show_exit_confirmation)

    @handle('y', filter=confirmation_visible)
    @handle('Y', filter=confirmation_visible)
    @handle(Keys.ControlJ, filter=confirmation_visible)
    @handle(Keys.ControlD, filter=confirmation_visible)
    def _(event):
        """
        Really quit.
        """
        event.cli.exit()

    @handle("n", filter=confirmation_visible)
    # @handle("N", filter=confirmation_visible)
    @handle(Keys.Any, filter=confirmation_visible)
    def _(event):
        """
        Cancel exit.
        """
        python_input.show_exit_confirmation = False

    return registry
diddly=0

def auto_newline(buffer):
    r"""
    Insert \n at the cursor position. Also add necessary padding.
    """
    insert_text = buffer.insert_text

    if buffer.document.current_line_after_cursor:
        # When we are in the middle of a line. Always insert a newline.
        insert_text('\n')
    else:
        # Go to new line, but also add indentation.
        current_line = buffer.document.current_line_before_cursor.rstrip()
        insert_text('\n')

        # Unident if the last line ends with 'pass', remove four spaces.
        unindent = current_line.rstrip().endswith(' pass') or current_line.lstrip().startswith('return ') or current_line.lstrip().startswith('raise ')  or current_line.strip()==('break') or  current_line.strip()==('continue') or  current_line.strip()==('raise') or  current_line.strip()==('pass')or  current_line.strip()==('return')

        # Copy whitespace from current line
        current_line2 = current_line[4:] if unindent else current_line

        for c in current_line2:
            if c.isspace():
                insert_text(c)
            else:
                break

        # If the last line ends with a colon, add four extra spaces.
        if current_line[-1:] == ':':
            for x in range(4):
                insert_text(' ')

