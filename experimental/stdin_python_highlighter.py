from fileinput import filelineno
import sys

#We reimplement things from r.py here because then we don't have to import rp, decreasing the delay of the output from running this file.
#This script is called from iterfzf inside of r.py, and might be called tens of times a second


def line_number_prefix_generator( line_number,num_digits):
    return (('%%%ii| ')%num_digits)%line_number 

def line_highlighter(text):
    return fansi((text),'black','bold','yellow')

def preview_line_highlighter(text):
    return fansi((text),'black','bold','green')

def prefix_highlighter(prefix):
    return fansi(prefix,'cyan','bold','black')

def preview_prefix_highlighter(prefix):
    return fansi(prefix,'green','bold','black')

digit_remover=str.maketrans('0123456789', '          ')


def fansi_syntax_highlighting(code: str,
                              namespace=(),
                              style_overrides:dict={},
                              line_wrap_width:int=None,
                              show_line_numbers:bool=False,
                              lazy:bool=False,
                              highlighted_line_numbers=[], #This is not in rp. It's not useful for rp generically, but is very useful for fzf result highlighting...
                              squelch=False,#Supress errors?
                              ):
    #TODO: Because of the way it was programmed, it now included an extraneous new empty line on the top of the output. Feel free to remove that later brutishly lol (just lob it off the final output)
    #If lazy==True, this function returns a generator of strings that should be printed sequentially without new lines
    #If line_wrap_width is an int, it will wrap the whole output to that width - this is suprisingly tricky to do because of the ansi escape codes
    #show_line_numbers, if true, will also display a line number gutter on the side
    #
    #EXAMPLE USING LAZY:
    #    #Lazy can make syntax highlighting of things like rp start instantly
    #    code=get_source_code(r)
    #    for chunk in fansi_syntax_highlighting(code,lazy=True,show_line_numbers=True,line_wrap_width=get_terminal_width()):
    #        print(end=chunk)
    #    print()
    #The result is that it has a shorter delay to start ; but it also might take longer in total
    #
    #EXAMPLE:
    #    print(fansi_syntax_highlighting(get_source_code(load_image),line_wrap_width=30,show_line_numbers=False))
    #
    # PLEASE NOTE THAT I DID NOT WRITE SOME OF THIS CODE!!! IT CAME FROM https://github.com/akheron/cpython/blob/master/Tools/scripts/highlight.py
    # Assumes code was written in python.
    # Method mainly intended for rinsp.
    # I put it in the r class for convenience.
    # Works when I paste methods in but doesn't seem to play nicely with rinsp. I don't know why yet.
    # See the highlight_sourse_in_ansi module for more stuff including HTML highlighting etc.

    highlighted_line_numbers=[x-1 for x in highlighted_line_numbers] #Convert lines 1,2,3 etc to line indices 0,1,2 etc

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
            try:
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
            except Exception as e:
                #Probably a syntax error
                # yield from (('',x) for x in readline)
                import traceback
                if not squelch:
                    traceback.print_exception(e)
                pass
            line_upto_token,written=combine_range(lines,written,(erow,ecol))
            yield '',line_upto_token
        def ansi_highlight(classified_text,colors=default_ansi):
            'Add syntax highlighting to source code using ANSI escape sequences'
            # http://en.wikipedia.org/wiki/ANSI_escape_code

            nonlocal line_wrap_width, show_line_numbers

            if line_wrap_width is None:
                line_wrap_width = 9999999
            
            num_code_lines = code.count('\n')+1
            num_digits = len(str(num_code_lines)) #Max number of digits in the line numbers
            num_digits = max(3,num_digits) #Don't jitter around as much in qprp

            max_width = line_wrap_width
            if show_line_numbers:
                #Should always return strings of the same width if done correctly
                #TODO: Make this customizable through the args

                line_prefix_length = len(line_number_prefix_generator(num_code_lines,num_digits))

                if line_wrap_width >= line_prefix_length:
                    max_width = line_wrap_width-line_prefix_length
                else:
                    #We have to not show line numbers, or else we'd be showing literally nothing but them!
                    show_line_numbers=False
                    

            def wrapped_line_tokens(tokens,max_width):
                #Wrap the string, respecting token boundaries when possible
                #Tokens is a list of [(kind,text), (kind,text), ... ] tuples
                #Output is a generator of [(kind,text,line_number) ... ] tuples
                #EXAMPLE TEST:
                #   
                #    >>> list(wrapped_line_tokens([(11,'Hello\nWorld!\n123\nab\nc'),(22,'d'),(33,'e'),(44,'f')],2))
                #    [
                #        (11  , 'He', 0),
                #        (None, '\n', 1),
                #        (11  , 'll', 1),
                #        (None, '\n', 2),
                #        (11  , 'o' , 2),
                #        (None, '\n', 3),
                #        (11  , 'Wo', 3),
                #        (None, '\n', 4),
                #        (11  , 'rl', 4),
                #        (None, '\n', 5),
                #        (11  , 'd!', 5),
                #        (None, '\n', 6),
                #        (11  , '12', 6),
                #        (None, '\n', 7),
                #        (11  , '3' , 7),
                #        (None, '\n', 8),
                #        (11  , 'ab', 8),
                #        (None, '\n', 9),
                #        (11  , 'c' , 9),
                #        (22  , 'd' , 9),
                #        (33  , ''  , 9),
                #        (None, '\n', 10),
                #        (33  , 'e' , 10),
                #        (44  , 'f' , 10)
                #    ]
                #
                line_length=0
                line_number=0
                line_skip=0
                for kind,text in tokens:
                    subtokens=split_including_delimiters(text,'\n')
                    subtokens=subtokens[::-1]
                    while subtokens:
                        assert max_width>=line_length
                        subtoken=subtokens.pop()
                        if subtoken=='\n':
                            if line_number in highlighted_line_numbers:
                                yield 'HIGHLIGHT',' '*1000,line_number #Since FZF doesn't have line wrapping this will go off the edge, highlighting the whole terminal line (assuming the terminal isn't 1000 chars wide lol)
                                # yield 'HIGHLIGHT',' '*(max_width-line_length),line_number 
                            if not line_skip:
                                line_number+=1
                            line_skip=max(0,line_skip-1)
                            line_length=0
                            #Probably can eliminate typehere....
                            yield None,subtoken,line_number
                        elif line_length+len(subtoken)>max_width:
                            index=max_width-line_length
                            token_right=subtoken[index:]
                            subtoken   =subtoken[:index]
                            line_length=0
                            subtokens.append(token_right)
                            subtokens.append('\n')
                            yield kind,subtoken,line_number
                            line_skip+=1
                        else:
                            line_length+=len(subtoken)
                            yield kind,subtoken,line_number
            

            prev_line_number=None
            from itertools import chain
            for kind,text,line_number in chain([[None,'\n',0]],wrapped_line_tokens(classified_text,max_width=max_width)):
                assert isinstance(text,str),'text is not str, is '+str(type(text))
                opener,closer=colors.get(kind,('',''))
                if show_line_numbers and text.endswith('\n'):
                    prefix=line_number_prefix_generator(line_number+1,num_digits)
                    prefix=prefix_highlighter(prefix)
                    # prefix=fansi(prefix,'cyan','bold')#,'black')
                    # prefix='\u001b[1m\u001b[36m'+prefix #cyan bold
                    if line_number==prev_line_number:
                        #https://stackoverflow.com/questions/19084443/replacing-digits-with-str-replace
                        prefix=strip_ansi_escapes(prefix)
                        prefix=prefix.translate(digit_remover)
                        prefix=prefix_highlighter(prefix)
                    if line_number in highlighted_line_numbers:
                        prefix=strip_ansi_escapes(prefix)
                        prefix=line_highlighter(prefix)
                    text=text+prefix
                if line_number in highlighted_line_numbers:
                    yield from line_highlighter(text)
                else:
                    yield from [opener,text,closer]
                prev_line_number=line_number
        output=(ansi_highlight(analyze_python(code)))
        if lazy:
            return output
        else:
            return ''.join(output)
    
    except Exception:
        #To be honest, when the tokenizer throws a hissy fit idk what to do...haven't thought about it too much.
        #It cuts off some of the text in the preview, so that's not good...
        #TODO: figure this out. i dont' have time rn lol.
        #To reproduce this, try doing FDT through a bunch of files - eventually some error will pop up in the preview like "tokenize.TokenError: ('EOF in multi-line statement', (129, 0)) " which refers to the code being parsed
        if not squelch:
            print(code)
            raise
        # return code  # Failed to highlight code, presumably because of an import error.

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


def fansi(text_string,text_color=None,style=None,background_color=None,*,per_line=False,include_end=True):
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
        lines=(text_string).splitlines()
        lines=[fansi(line,text_color,style,background_color,per_line=False) for line in lines]
        return '\n'.join(lines)
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

    if include_end:
        return "\x1b[%sm%s\x1b[0m" % (';'.join(format),str(text_string))  # returns a string with the appropriate formatting applied
    else:
        #Don't end the style...
        return "\x1b[%sm%s" % (';'.join(format),str(text_string))  # returns a string with the appropriate formatting applied



def split_including_delimiters(input: str, delimiter: str):
    """
    Splits an input string, while including the delimiters in the output
    
    Unlike str.split, we can use an empty string as a delimiter
    Unlike str.split, the output will not have any extra empty strings
    Conequently, len(''.split(delimiter))== 0 for all delimiters,
       whereas len(input.split(delimiter))>0 for all inputs and delimiters
    
    INPUTS:
        input: Can be any string
        delimiter: Can be any string

    EXAMPLES:
         >>> split_and_keep_delimiter('Hello World  ! ',' ')
        ans = ['Hello ', 'World ', ' ', '! ', ' ']
         >>> split_and_keep_delimiter("Hello**World**!***", "**")
        ans = ['Hello', '**', 'World', '**', '!', '**', '*']
    EXAMPLES:
        assert split_and_keep_delimiter('-xx-xx-','xx') == ['-', 'xx', '-', 'xx', '-'] # length 5
        assert split_and_keep_delimiter('xx-xx-' ,'xx') == ['xx', '-', 'xx', '-']      # length 4
        assert split_and_keep_delimiter('-xx-xx' ,'xx') == ['-', 'xx', '-', 'xx']      # length 4
        assert split_and_keep_delimiter('xx-xx'  ,'xx') == ['xx', '-', 'xx']           # length 3
        assert split_and_keep_delimiter('xxxx'   ,'xx') == ['xx', 'xx']                # length 2
        assert split_and_keep_delimiter('xxx'    ,'xx') == ['xx', 'x']                 # length 2
        assert split_and_keep_delimiter('x'      ,'xx') == ['x']                       # length 1
        assert split_and_keep_delimiter(''       ,'xx') == []                          # length 0
        assert split_and_keep_delimiter('aaa'    ,'xx') == ['aaa']                     # length 1
        assert split_and_keep_delimiter('aa'     ,'xx') == ['aa']                      # length 1
        assert split_and_keep_delimiter('a'      ,'xx') == ['a']                       # length 1
        assert split_and_keep_delimiter(''       ,''  ) == []                          # length 0
        assert split_and_keep_delimiter('a'      ,''  ) == ['a']                       # length 1
        assert split_and_keep_delimiter('aa'     ,''  ) == ['a', '', 'a']              # length 3
        assert split_and_keep_delimiter('aaa'    ,''  ) == ['a', '', 'a', '', 'a']     # length 5
    """

    # I made this question an answer at https://stackoverflow.com/questions/2136556/in-python-how-do-i-split-a-string-and-keep-the-separators/73562313#73562313

    # Input assertions
    assert isinstance(input,str), "input must be a string but got "+str(input)
    assert isinstance(delimiter,str), "delimiter must be a string but got "+str(input)

    if delimiter:
        # These tokens do not include the delimiter, but are computed quickly
        tokens = input.split(delimiter)
    else:
        # Edge case: if the delimiter is the empty string, split between the characters
        tokens = list(input)
        
    # The following assertions are always true for any string input and delimiter
    # For speed's sake, we disable this assertion
    # assert delimiter.join(tokens) == input

    output = tokens[:1]

    for token in tokens[1:]:
        output.append(delimiter)
        if token:
            output.append(token)
    
    # Don't let the first element be an empty string
    if output[:1]==['']:
        del output[0]
        
    # The only case where we should have an empty string in the output is if it is our delimiter
    # For speed's sake, we disable this assertion
    # assert delimiter=='' or '' not in output
        
    # The resulting strings should be combinable back into the original string
    # For speed's sake, we disable this assertion
    # assert ''.join(output) == input

    return output

# def get_terminal_size():  # In (ↈcolumns，ↈrows) tuple form
#     # From http://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python/14422538#14422538
#     import os
#     env=os.environ
#     def ioctl_GWINSZ(fd):
#         try:
#             import fcntl,termios,struct,os
#             cr=struct.unpack('hh',fcntl.ioctl(fd,termios.TIOCGWINSZ,
#                                               '1234'))
#         except Exception:
#             return
#         return cr
#     cr=ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
#     if not cr:
#         try:
#             fd=os.open(os.ctermid(),os.O_RDONLY)
#             cr=ioctl_GWINSZ(fd)
#             os.close(fd)
#         except Exception:
#             pass
#     if not cr:
#         cr=(env.get('LINES',24),env.get('COLUMNS',80))

#         ### Use get(key[, default]) instead of a try/catch
#         # try:
#         #    cr = (env['LINES'], env['COLUMNS'])
#         # except Exception:
#         #    cr = (25, 80)
#     return int(cr[1]),int(cr[0])

# def get_terminal_width():
#     return get_terminal_size()[0]

# def _line_numbered_string(string,foreground='cyan',style='bold',background='blue'):
#     lines=line_split(string)
#     nlines=len(lines)
#     numwidth=len(str(nlines))
#     newlines=[fansi(str(i+1).rjust(numwidth)+' '*0,foreground,style,background)+e for i,e in enumerate(lines)]
#     return line_join(newlines)

# def wrap_string_to_width(string,width):
#     #TODO: Make this work with visible_string_length so that unicode chars/ansi codes are supported
#     #EXAMPLE:
#     # ⮤ wrap_string_to_width('Hello\nWorld!',2)
#     #    ans = He
#     #    ll
#     #    o
#     #    Wo
#     #    rl
#     #    d!
#     assert width>=0,'Cannot have negative width'
#     lines=[]
#     for line in line_split(string):
#         lines+=split_into_sublists(line,width,strict=False,keep_remainder=True)
#     return line_join(''.join(line)for line in lines)

def split_into_sublists(l,sublist_len:int,strict=False,keep_remainder=True):
    # If strict: sublist_len MUST evenly divide len(l)
    # It will return a list of tuples, unless l is a string, in which case it will return a list of strings
    # keep_remainder is not applicable if strict
    # if not keep_remainder and sublist_len DOES NOT evenly divide len(l), we can be sure that all tuples in the output are of len sublist_len, even though the total number of elements in the output is less than in l.
    # EXAMPLES:
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,3 ,0)   -> [(1,2,3),(4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,0)   -> [(1,2,3,4),(5,6,7,8),(9,)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,5 ,0)   -> [(1,2,3,4,5),(6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,6 ,0)   -> [(1,2,3,4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0)   -> [(1,2,3,4,5,6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0,1) -> [(1,2,3,4,5,6,7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,66,0,0) -> []
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,5 ,0,0) -> [(1,2,3,4,5)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,0,0) -> [(1,2,3,4),(5,6,7,8)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,3 ,0,0) -> [(1,2,3),(4,5,6),(7,8,9)]
    # ⮤ split_into_sublists([1,2,3,4,5,6,7,8,9］,4 ,1,0) -> ERROR: ¬ 4 | 9

    assert is_number(sublist_len),'sublist_len should be an integer, but got type '+repr(type(sublist_len))
    if strict:
        assert not len(l)%sublist_len,'len(l)=='+str(len(l))+' and sublist_len=='+str(sublist_len)+': strict mode is turned on but the sublist size doesnt divide the list input evenly. len(l)%sublist_len=='+str(len(l)%sublist_len)+'!=0'
    n=sublist_len

    #This line is rather dense, but it makes sense.
    output=list(zip(*(iter(l),) * n))+([tuple(l[len(l)-len(l)%n:])] if len(l)%n and keep_remainder else [])
    
    if isinstance(l,str):
        output=[''.join(substring) for substring in output]

    return output


def get_absolute_path(path,*,physical=True):
    import os
    #Given a relative path, return its absolute path
    #If physical, expand all symlinks in the path
    path=os.path.expanduser(path)#In case the path has a '~' in it
    if physical:
        path=os.path.realpath(path)#Get rid of any symlinks in the path
    return os.path.abspath(path)

def number_of_lines_in_file(filename):
    #Quickly count the nubmer of lines in a given file.
    #It's 5-10x faster than text_file_to_string(filename).count('\n')
    #It also appears to take constant memory; my memory usage didn't flinch even when I threw a 2gb file at it.
    #Note that it doesn't care if it's a text file or not; it just counts the number of \n bytes in the file!
    #   For example, number_of_lines_in_file('picture.jpg')==280 is a possibility.
    #https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    from itertools import takewhile,repeat
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )+1

def file_line_iterator(file_name):
    #Opens a file and iterates through its lines
    #Needs a better name
    file=open(file_name)
    while True:
        line=file.readline()
        if not line:
            return
        #I DONT KNOW WHY THIS ASSERTION DOESN'T ALWAYS WORK BUT SOMETIMES IT FAILS...
        if line.endswith('\n'):
            yield line[:-1]
        else:
            yield line

bytes_per_megabyte=2**20


def total_disc_bytes(path):

    #NOTE: 2**20 bytes is one megabyte

    # path can be either a folder or a file; it will detect that for you. Implemented recursively (checks subfolders)
    # returns total size in bytes
    import os
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

def line_join(x):
    return '\n'.join(x)

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

import difflib
from typing import Optional

class LineDiffHunk:
    def __init__(self,old_line_number:int,new_line_number:int,type:str):
        assert type in ' -+' and len(type)==1
        self.type=type
        self.lines=[]
        self.old_line_number=old_line_number
        self.new_line_number=new_line_number
    
    @property
    def color(self):    
        return {'+':'green','-':'red',' ':None}[self.type]
    
    def numbered_line(self,line:str,old_line_number:int,new_line_number:int):
        prefix_start=fansi(self.type+' ',self.color,'bold')        
        old_prefix='%4i'%old_line_number
        divider='│'
        new_prefix='%4i'%new_line_number
        prefix_end='│'+prefix_start
        
        if self.type=='+':old_prefix=' '*len(old_prefix)
        if self.type=='-':new_prefix=' '*len(old_prefix)
        
        if self.type!=' ':
            old_prefix=fansi(old_prefix,self.color,'bold')
            new_prefix=fansi(new_prefix,self.color,'bold')
            def fansi_with_underlined_trailing_whitespace(line):
                whitespace_amount=len(line)-len(line.rstrip())
                if whitespace_amount==0:
                    return fansi(line,self.color)
                    
                whitespace=line[-whitespace_amount:]
                return fansi(line[:-whitespace_amount],self.color)+fansi(whitespace,None,None,'yellow')
            line=fansi_with_underlined_trailing_whitespace(line)#,'underlined')
        
        return old_prefix+divider+new_prefix+prefix_end+line

    def __iter__(self):            
        old_line_number=self.old_line_number
        new_line_number=self.new_line_number
        for line in self.lines:
            old_line_number+=1
            new_line_number+=1
            yield self.numbered_line(line,old_line_number,new_line_number)
    
    def __str__(self):
        return line_join(self)
            
    def summary_string(self,max_context=5):#,is_first_hunk=False,is_last_hunk=False):
        cut_line='\n • • • • ( %i lines ) • • • • \n'
        cut_line=fansi(cut_line,'blue')
        
        lines=list(self)
        if len(lines)>2*max_context+1 :#and self.type==' ':
            num_lines_cut=len(lines)-2*max_context
            
            if num_lines_cut>=10:
                #Don't report we just cut one damn line lol...
                output=[]
                output+=lines[:max_context]
                output+=[cut_line%num_lines_cut]
                output+=lines[-max_context:]
                
                lines=output
            
        return line_join(lines)
            

def diff(old: str, new: str):#->list[LineDiffHunk]:

    old = old.splitlines()
    new = new.splitlines()

    line_types = {' ': None, '-': 'red', '+': 'green', '?': 'magenta'}

    old_line_number=0
    new_line_number=0
    

    current_hunk=LineDiffHunk(
        old_line_number,
        new_line_number,
        type=' ',
    )
    
    hunks=[]

    for line in difflib.Differ().compare(old, new):
        
        type=line[0]
        line=line[2:]

        assert type in ' -+?'

        if type=='?':
            # Skip this. See difflib.Differ.__doc__ to see what ? does.
            # It shows where in the line things changed, with an extra line.
            continue
        
        if not current_hunk.lines or type==current_hunk.type:
            current_hunk.type=type
            current_hunk.lines.append(line)
        else:
            assert type!=current_hunk.type
            hunks.append(current_hunk)
            current_hunk=LineDiffHunk(old_line_number,new_line_number,type)
            current_hunk.lines.append(line)

        if type==' ':
            new_line_number+=1
            old_line_number+=1
        elif type=='+':
            new_line_number+=1
        elif type=='-':
            old_line_number+=1
        else:
            assert False,'Unreachable code'
            
        
    hunks.append(current_hunk)
    
    return hunks
            
    
def diff_display_string(a:str,b:str)->str:
    #    #EXAMPLE:
    #        a="# 2022-09-08 00:16:07.547366\nimport difflib\nfrom typing import Optional\n\nclass LineDiffHunk:\n    def __init__(self,old_line_number:int,new_line_number:int,type:str):\n        assert type in ' -+' and len(type)==1\n        self.type=type\n        self.lines=[]\n        self.old_line_number=old_line_number\n        self.new_line_number=new_line_number\n    \n    @property\n    def color(self):    \n        return {'+':'green','-':'red',' ':None}[self.type]\n    \n    def numbered_line(self,line:str,old_line_number:int,new_line_number:int):\n        prefix_start=fansi(self.type+' ',self.color)        \n        old_prefix='%4i'%old_line_number\n        divider=', '\n        new_prefix='%4i'%new_line_number\n        prefix_end='│ '\n        \n        if self.type=='+':old_prefix=' '*len(old_prefix)\n        if self.type=='-':new_prefix=' '*len(old_prefix)\n        \n        new_prefix=fansi(new_prefix,self.color,'bold')\n        old_prefix=fansi(old_prefix,self.color,'bold')\n        \n        return old_prefix+divider+new_prefix+prefix_end+line\n\n    def __iter__(self):            \n        old_line_number=self.old_line_number\n        new_line_number=self.new_line_number\n        for line in self.lines:\n            old_line_number+=1\n            new_line_number+=1\n            yield self.numbered_line(line,old_line_number,new_line_number)\n    \n    def __str__(self):\n        return line_join(self)\n            \n    def summary_string(self,max_context=5,is_first_hunk=False,is_last_hunk=False):\n        cut_line=' • • • • ( %i lines ) • • • • '\n        \n        lines=list(self)\n        if self.type==' ' and len(lines)>2*max_context+1:\n            num_lines_cut=len(lines)-2*max_context\n            self.lines=self.lines[:max_context]+[cut_line%num_lines_cut]+self.lines[-max_context:]\n            \n        return line_join(lines)\n            \n\ndef diff(old: str, new: str)->list[LineDiffHunk]:\n\n    old = old.splitlines()\n    new = new.splitlines()\n\n    line_types = {' ': None, '-': 'red', '+': 'green', '?': 'magenta'}\n\n    old_line_number=0\n    new_line_number=0\n    \n\n    current_hunk=LineDiffHunk(\n        old_line_number,\n        new_line_number,\n        type=' ',\n    )\n    \n    hunks=[]\n\n    for line in difflib.Differ().compare(old, new):\n        \n        type=line[0]\n        line=line[1:]\n\n        assert type in ' -+?'\n        \n        if type==' ':\n            new_line_number+=1\n            old_line_number+=1\n        elif type=='+':\n            new_line_number+=1\n        elif type=='-':\n            old_line_number+=1\n        elif type=='?':\n            # Skip this. See difflib.Differ.__doc__ to see what ? does.\n            # It shows where in the line things changed, with an extra line.\n            continue\n        else:\n            assert False,'Unreachable code'\n            \n        if not current_hunk.lines or type==current_hunk.type:\n            current_hunk.type=type\n            current_hunk.lines.append(line)\n            current_hunk.new_line_number=new_line_number\n            current_hunk.old_line_number=old_line_number            \n        else:\n            assert type!=current_hunk.type\n            hunks.append(current_hunk)\n            current_hunk=LineDiffHunk(old_line_number,new_line_number,type)\n            current_hunk.lines.append(line)\n        \n    hunks.append(current_hunk)\n    \n    return hunks\n            \n    \ndef print_diff(a,b):\n    for hunk in diff(a,b):\n        print(hunk.summary_string())\n"
    #        b="import difflib\nfrom typing import Optional\n\nclass LineDiffHunk:\n    def __init__(self,old_line_number:int,new_line_number:int,type:str):\n        assert type in ' -+' and len(type)==1\n        self.type=type\n        self.lines=[]\n        self.old_line_number=old_line_number\n        self.new_line_number=new_line_number\n    \n    @property\n    def color(self):    \n        return {'+':'green','-':'red',' ':None}[self.type]\n    \n    def numbered_line(self,line:str,old_line_number:int,new_line_number:int):\n        prefix_start=fansi(self.type+' ',self.color,'bold')        \n        old_prefix='%4i'%old_line_number\n        divider='│'\n        new_prefix='%4i'%new_line_number\n        prefix_end='│'+prefix_start\n        \n        if self.type=='+':old_prefix=' '*len(old_prefix)\n        if self.type=='-':new_prefix=' '*len(old_prefix)\n        \n        if self.type!=' ':\n            old_prefix=fansi(old_prefix,self.color,'bold')\n            new_prefix=fansi(new_prefix,self.color,'bold')\n            line=fansi(line,self.color,'underlined')\n        \n        return old_prefix+divider+new_prefix+prefix_end+line\n\n    def __iter__(self):            \n        old_line_number=self.old_line_number\n        new_line_number=self.new_line_number\n        for line in self.lines:\n            old_line_number+=1\n            new_line_number+=1\n            yield self.numbered_line(line,old_line_number,new_line_number)\n    \n    def __str__(self):\n        return line_join(self)\n            \n    def summary_string(self,max_context=5,is_first_hunk=False,is_last_hunk=False):\n        cut_line='\\n • • • • ( %i lines ) • • • • \\n\\n'\n        cut_line=fansi(cut_line,'blue')\n        \n        lines=list(self)\n        if self.type==' ' and len(lines)>2*max_context+1:\n            num_lines_cut=len(lines)-2*max_context\n            \n            output=[]\n            output+=lines[:max_context]\n            output+=[cut_line%num_lines_cut]\n            output+=lines[-max_context:]\n            \n            lines=output\n            \n        return line_join(lines)\n            \n\ndef diff(old: str, new: str)->list[LineDiffHunk]:\n\n    old = old.splitlines()\n    new = new.splitlines()\n\n    line_types = {' ': None, '-': 'red', '+': 'green', '?': 'magenta'}\n\n    old_line_number=0\n    new_line_number=0\n    \n\n    current_hunk=LineDiffHunk(\n        old_line_number,\n        new_line_number,\n        type=' ',\n    )\n    \n    hunks=[]\n\n    for line in difflib.Differ().compare(old, new):\n        \n        type=line[0]\n        line=line[2:]\n\n        assert type in ' -+?'\n\n        if type=='?':\n            # Skip this. See difflib.Differ.__doc__ to see what ? does.\n            # It shows where in the line things changed, with an extra line.\n            continue\n        \n        if not current_hunk.lines or type==current_hunk.type:\n            current_hunk.type=type\n            current_hunk.lines.append(line)\n        else:\n            assert type!=current_hunk.type\n            hunks.append(current_hunk)\n            current_hunk=LineDiffHunk(old_line_number,new_line_number,type)\n            current_hunk.lines.append(line)\n\n        if type==' ':\n            new_line_number+=1\n            old_line_number+=1\n        elif type=='+':\n            new_line_number+=1\n        elif type=='-':\n            old_line_number+=1\n        else:\n            assert False,'Unreachable code'\n            \n        \n    hunks.append(current_hunk)\n    \n    return hunks\n            \n    \ndef print_diff(a,b):\n    for hunk in diff(a,b):\n        print(hunk.summary_string())\n"
    #        print_diff(a,b)
    subs=0
    sames=0
    adds=0
    out=''
    for hunk in diff(a,b):
        if hunk.type==' ':
            sames+=len(hunk.lines)
        if hunk.type=='+':
            adds+=len(hunk.lines)
        if hunk.type=='-':
            subs+=len(hunk.lines)
        out+=(hunk.summary_string())+'\n'
    return subs,sames,adds,out

def split_python_tokens(code: str):
    #Should return a list of all the individual python tokens, INCLUDING whitespace and newlines etc
    #When summed together, the token-strings returned by this function should equal the original inputted string
    from pygments.lexers import Python3Lexer
    from pygments.lexer import Lexer

    def get_all_pygments_tokens(string:str,pygments_lexer:Lexer=Python3Lexer()):
        return pygments_lexer.get_tokens_unprocessed(string)

    def get_all_token_strings(string:str):
        #Returns all the string-value of all tokens parsed from the string, including whitespace and comments
        token_string_generator = (token[2] for token in get_all_pygments_tokens(string))
        return token_string_generator

    return list(get_all_token_strings(code))

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

def print_python_line_summary(code,linum):
    if not is_valid_python_syntax(code):
        return
    linum-=1
    lines=code.splitlines()
    lines=[line+' '*100 for line in lines] #Make sure we still get the path for empty lines with no indent
    def get_indent_level(q):return len(q)-len(q.lstrip())
    current_level=get_indent_level(lines[linum])
    lines=lines[:linum]
    linum=min(linum,len(lines)-1)

    def startswithany(x,things):
        things=things.split()
        x=x.lstrip()
        for y in things:
            if x.startswith(y+' '):
                return True
        return False
    lines=[x for x in lines if startswithany(x,'def class if while for with try except finally async elif else ')]
    levels=[get_indent_level(x) for x in lines]
    lines=lines[::-1]
    levels=levels[::-1]
    out=[]
    for line,level in zip(lines,levels):
        if current_level>level:
            out.append(line)
            current_level=level
            
    out=out[::-1]#Like ['class Rays:', '    def is_cuda(self) -> bool:']
    out=[split_python_tokens(x.strip()) for x in out]
    out=[x[0]+' '+x[2] for x in out]
    def colorize(x):
        if x.startswith('class '):
            return fansi(x,'yellow','bold','black')
        if x.startswith('def '):
            return fansi(x,'green','bold','black')
        return None
        assert False, 'should start with class or def'+ ' '+ x
    out=[colorize(x) for x in out]    
    out=[x for x in out if x is not None]
    out=fansi(' --> ',None,'bold','black').join(out)
    #Out is coloried like "class Rays --> def is_cuda"
    # if not out:
    #     return
    print(fansi('     ',None,None,'black')+out+fansi(' '*1000,None,None,'black'))
    return out

def start(text=None):

    # HARDCODED_WIDTH=None

    text=text or sys.stdin.read()
    width=int(sys.argv[1])

    text=text.replace('\\"','"')


    try:
        thingstoprint=None
        mode=None
        if len(sys.argv)>2:
            mode = sys.argv[2]

            if mode=='FDT':
                #Something like
                #w​e​b​_​e​v​a​l​u​a​t​o​r​.​p​y​:​1​4​4​:​     def evaluate(self,code:str='',**vars):
                file,line_number,line=text.split(':',maxsplit=2)
                file=file.replace('\u200b','')
                line_number=line_number.replace('\u200b','')
                line_number=int(line_number)
                file_size=total_disc_bytes(file)
                total_num_lines=number_of_lines_in_file(file)
                print(fansi('Line %4i / %i (%s):  '%(line_number,total_num_lines,human_readable_file_size(file_size)),'green','bold','black')+fansi(get_absolute_path(file),'green','underlined','black')+fansi(' '*1000,None,None,'black'))


                max_megabytes=1
                max_mini_preview_megabytes=256 #a wild guess how big is too big...feel free to calibrate these max bmegabyte numbers Based on your preferences
                max_highlightable_size=bytes_per_megabyte*max_megabytes
                max_minipreviewable_size=bytes_per_megabyte*max_mini_preview_megabytes

                def make_preview_window():
                    num_surrounding_lines=10 #How much context to give in the preview?

                    blank_line='·'*1000

                    def get_preview_line(linenum):
                        linenum+=1
                        prefix=line_number_prefix_generator(linenum+1,num_digits)
                        if 0<=linenum<len(file_lines):
                            line=file_lines[linenum]
                            if linenum==line_number-1:
                                line=preview_line_highlighter(line+' '*1000)
                            else:
                                try:
                                    line=fansi_syntax_highlighting(line,squelch=True)[1:]
                                except Exception as e:
                                    pass
                        else:
                            prefix=prefix.translate(digit_remover).replace('-',' ')
                            line=blank_line
                        if linenum!=line_number-1:
                            prefix=preview_prefix_highlighter(prefix)
                        else:
                            prefix=preview_line_highlighter(prefix)
                        line=prefix+line
                        return line

                    for i in range(line_number-num_surrounding_lines-2,line_number+num_surrounding_lines-1):

                        print(get_preview_line(i))

                    print(prefix_highlighter('    Full Source Code (scroll down):'+' '*1000))

                    line_number

                if file_size>max_highlightable_size:
                    print(fansi('  - NOTE: Syntax highlighting and line wrapping disabled because this file is larger than %i megabytes (it would be annoyingly slow)'%max_megabytes+' '*1000,'green',None,'black'))

                    line_iterator=file_line_iterator(file) #Worst case if its too damn big...


                    if file_size<max_minipreviewable_size:
                        file_text=open(file,'r').read()
                        file_lines=file_text.splitlines()
                        line_iterator=file_lines
                        num_digits=len(str(total_num_lines))
                        num_digits=max(num_digits,4)
                        make_preview_window()
                    else:
                        print(fansi('  - NOTE: Mini-preview disabled because this file is larger than %i megabytes'%max_mini_preview_megabytes+' '*1000,'green',None,'black'))

                    

                    for i,line in enumerate(line_iterator):
                        i+=1
                        num_digits=len(str(total_num_lines))
                        num_digits=max(num_digits,4)
                        prefix=line_number_prefix_generator(i,num_digits)
                        prefix=prefix_highlighter(prefix)
                        print(end=prefix)
                        if i==line_number:
                            line+=' '*1000
                            line=line_highlighter(line)
                        print(line)

                else:

                    num_digits=len(str(total_num_lines))
                    num_digits=max(num_digits,3)
                    file_text=open(file,'r').read()
                    file_lines=file_text.splitlines()
                    
                    try:
                        print_python_line_summary('\n'.join(file_lines),line_number)
                    except Exception:
                        pass
                    make_preview_window()

                    thingstoprint=fansi_syntax_highlighting(file_text,show_line_numbers=True,line_wrap_width=width,lazy=True,highlighted_line_numbers=[line_number])
                # from random import random
                # if random()>.99:
                    # while True:pass

            if mode=='diff_mode':
                import json
                # text=json.loads(text)
                old_code = sys.argv[3]
                old_code=json.loads(old_code)
                # old_code = old_code.replace('\\"','"')
                subs,sames,adds,diff_string=diff_display_string(old_code,text)
                print(fansi(' DIFF FROM SELECTED TO ORIGINAL: '+' '*10000,'cyan','bold','black'))

                print(end=fansi('   LINES: ','cyan','bold','black'))
                sames=fansi('%i untouched, '%sames,'gray','bold','black')
                subs=fansi('  -%i'%subs,'red' ,'bold','black')+fansi(' removed, ','red'  ,'bold','black')
                adds=fansi('  +%i'%adds,'green','bold','black')+fansi(' added','green','bold','black')
                print(sames+subs+adds+fansi(' '*10000,'cyan','bold','black'))
                if text==old_code:
                    print(fansi('          (They\'re identical!) '+' '*10000,'cyan','bold','black'))
                print(end=diff_string)
                

                # print(old_code)

                # text.replace('\\"','"')
                # print("DONE!!!")
                print()
                print(fansi(' SELECTED CODE:  %i line%s'%(text.count('\n')+1,'s' if text.count('\n')+1>1 else '')+' '*10000,'cyan','bold','black'))

                import itertools
                thingstoprint=itertools.chain(
                    fansi_syntax_highlighting(text,show_line_numbers=True,line_wrap_width=width,lazy=True),
                    [' \n'],
                    [' \n'],
                    [fansi(' ORIGINAL CODE:  %i line%s'%(old_code.count('\n')+1,'s' if old_code.count('\n')+1>1 else '')+' '*10000,'cyan','bold','black')],
                    fansi_syntax_highlighting(old_code,show_line_numbers=True,line_wrap_width=width,lazy=True),
                )


        else:
        # width=HARDCODED_WIDTH or 80
        # text=fansi_syntax_highlighting(text)
        # print(text)
        # text=_line_numbered_string(text)
            thingstoprint=fansi_syntax_highlighting(text,show_line_numbers=True,line_wrap_width=width,lazy=True)
        
        if thingstoprint is not None:
            thingstoprint=iter(thingstoprint)
            print(end=next(thingstoprint).replace('\n',''))#Get rid of the first newline - its junk. Maybe a newer version of rp.fansi_syntax_highlighting addresses this, but in this file it outputs an empty junk line at the begginnging.

            print(end=next(thingstoprint).replace('\n','',1))#Get rid of the first newline - its junk. Maybe a newer version of rp.fansi_syntax_highlighting addresses this, but in this file it outputs an empty junk line at the begginnging.
            flag=9#This is a janky hack to prevent it from printing junk on the first line when the first line is selected...idk why it works...
            for x in thingstoprint:
                if mode=='FDT' and flag and line_number==1:
                    flag-=1
                    x=x.replace('\n','')
                print(end=x)
            print()

        exit()
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        # print(e)


start()
