#TODO: When x makes sense, y will happen when it makes sense (general ideas. )


When it makes sense, - will be turned into _.
	Examples:
		-=6  -->  _=6
		def f(-,) --> def f(_,)
		if -    if _





SUMMARY
	This documention is for RP (aka RyanPython).
	It's not yet complete, but includes a lot of important information.
	It's an extension of the HELP command.
	If you have any questions, you can email sqrtryan@gmail.com (for Ryan Burgert, the author of this package)
	Note: The only reason this is a .py file and not a .txt file is to make it conveniently be included in my pypi package. It's not an actual python file. This might change in the future.

SOME FEATURES OF RP:
	NORMAL FEATURE LIST:
		A profiler
		Debugger
		Better stack traces
		Code autoformatter
		Super fast Autocompletion
		Syntax highlighting
		Multi-line editing
		Linecaching (useful for debugger and stack traces)
		Xonsh shell (cross-platform)
		Auto re-import modules
		Embeddable pseudo_terminal()
		Runs with or without tty
		Persistent history and settings (even when updating rp)
	SPECIAL FEATURE LIST:
		Introspection tools ? ?. etc
		Big matlab-like library
		Microcompletions
		ans, PREV, UNDO, etc
		Tons of pretty themes
	COOL THINGS TO NOTICE:
		Invariant to prompt_toolkit version. This should run anywhere fine.
		rp includes a lot of tools made by different people. But the thing is, mine works out-of-the-box, no setup required. It makes these tools easy and accessible, as simple as 'pip install rp'.

KEY KEY:
	// In this documentation, you might see non-ascii symbols such as ↵ or ⌥. These symbols represent keys that can't otherwise be represented with a signle character.
	// This section is a key to tell you which symbol corresponds to which key, which will be useful for later sections of this documentation.
	// https://apple.stackexchange.com/questions/55727/where-can-i-find-the-unicode-symbols-for-mac-functional-keys-command-shift-e/55729
	↵ = '\n' aka the enter key
	¦ = the cursor
	⌫ = backspace
	⌦ = delete
	⇧ = shift
	⌥ = alt/option (assumed to be an escape prefix)
	⌘ = command
	⌃ = control
	⇥ = tab
	← = left arrow key
	→ = right arrow key
	↓ = down arrow
	↑ = up arrow
	␣ = spacebar
	⎋ = escape

KEYBOARD SHORTCUTS:
	⌃ c    copy
	⌃ v    paste
	⌃ d    duplicate current line
	⌃ e    execute current cell and keep buffer
	⌃ w    run current cell and keep buffer
	⌃ q    cancel current buffer
	⌃ l    clear and redraw the current screen (this is also useful when the gui looks all messed up, like if something printed over the gui for whatever reason)
	⌃ ⌦    delete current line
	⇧ →    move cursor to far right of line or shift line down
	⇧ ←    move cursor to far left of line or shift line up
	⌥ ↵    run current cell and clear buffer no-matter where you cursor is
	⇧ ⇥    unindent current line or cycle through completions
	⌃ ␣    toggle comment on current line and move cursor to next line
	⌥ ␣    forcibly insert a space character, skipping any microcompletions
	⌥ ⌫    backspace a whole word
	⌥ ←    jump back one word
	⌥ →    jump forward one word
	⌥ ↓    jump down several lines
	⌥ ↑    jump up several lines
	⌥ !    run shell command
	⌥ #    comment out the entire buffer and execute it
	⌃ t    previous buffer in history regardless of where cursor is (stands for top)
	⌃ b    next buffer in history regardless of where cursor is (stands for bottom)
	LESS IMPORTANT AND MAYBE REMOVED IN FUTURE:
		//While these keyboard shortcuts are kind of silly, I do find myself using them quite often
		⌃ h    inserts 'HISTORY'
		⌃ p    inserts 'PREV' then 'NEXT'
		⌥ m    inserts 'MORE' then 'MMORE'
		⌥ s    inserts 'self'
		⌥ )    insert ) at the end of the line without moving the cursor to the end of the line
		⌥ ]    insert ] at the end of the line without moving the cursor to the end of the line

MICROCOMPLETIONS:
	//This section covers only the microcompletions that take place in the context of a single line

	BACKSLASH COMMANDS:
		WITH ARGUMENTS:
			\sa  save file       (used like ‹`file.py\sa›. Saves the current buffer to 'file.py'. Will create a backup file if we overwrite something.)
			\wr  write file      (used like ‹`file.py\wr›. Saves the current buffer to 'file.py'. Not as safe as save file, and will not create a backup file.)
			\lo  load file       (used like ‹`file.py\lo›. Loads 'file.py' into the current buffer)
			\re  replace         (used like ‹`old`new\re›. It's a search-and-replace)
			\py  python          (used like ‹`repr\py›, or ‹`print_fix\py› etc. Replaces current buffer's text with function(currenttext))
			\go  goto            (used like ‹`10\go›. Bring the cursor to that line number.)
			\ca  cancel          (cancels any command you would have written and deletes the arguments. More civilized than spamming undo or backspace.)
			\dtl delete to line  (used like ‹`5\dtl›. Like d5G in vim.)
		WITHOUT ARGUMENTS:
			\de  debugger                (toggles the existence of 'debug()' on the top of your prompt without moving your cursor)
			\pu  pudb (other debugger)   (similar to \de, pudb is an alternative debugger, and this command also toggles a line on the top of the buffer. Whether you use this or \de is a matter of prefernece.)
			\ed  editor                  (opens up the current buffer in vim)
			\ac  align char              (inserts ‹→›, aka the alignment character. Used before \al. See https://asciinema.org/a/KjFS2lT0shRyv4r82RtFENzlo)
			\al  align                   (aligns all alignment characters to the same column. Used after inserting \ac in multiple different places.)
			\sw  strip whitespace        (strips all trailing whitespace in the buffer)
			\co  copy                    (copies the current buffer to your clipboard)
			\da  delete all              (deletes all text in the current buffer)
			\pa  paste                   (equivalent to control+v)
			\ya  yapf autoformatter      (autoformats your current code buffer using google's yapf library)
			\gg  go to top               (like gg in vim. bring cursor to the top of the buffer)
			\GG  go to bottom            (like G in vim. bring cursor to the bottom of the buffer)
			\vO  insert line above       (like O in vim. Inserts a new line above the current line.)
			\vo  insert line below       (like o in vim. Inserts a new line below the current line.)
			\mla multi line arguments    (turns a lengthy def into a multi line def. See https://asciinema.org/a/RHuWRKsbwvkH3P28XZ81MnFYJ)
			\tts tabs to spaces          (turns all tabs in the buffer into 4 spaces)

	FOR LOOPS:
		COMPREHENSION:
			IF: [f ff f ff] –––> [f for f in f if f]
			IF: [f ff f if] –––> [f for f in f if f]
			‹[x fx y]›  ––>  ‹[x for x in y]›
		CONTROL FLOW:
		‹fo ,› ––> ‹for i,e in enumerate()› //, to enumerate
		‹fo 5›  –––>  ‹for _ in range(5)› // 5 to range   <––– these are shared in different places
		‹for hello-world›  –––>  ‹for hello_world in :›// - to _ immediately
		‹fo -e a› ––> ‹for _ in enumerate(a)›
		‹fo -r a› ––> ‹for _ in range(a)›
		‹fo -l a› ––> ‹for _ in range(len(a))›
		‹fo -z a› ––> ‹for _ in zip(a)›
		‹fo x  ›  ––> ‹for x in ans›
		space to english plurality
		space to context variable
	KEYWORD COMPLETIONS:
		IF ELSE:
			x=y fz q
			EDGE CASES:
				[f ff f if] –/–> [f for f in f if f else]
		LETTER TO OPERATOR:
			in or and if/else,...
		AUTO SPACES:
			in, is, as
		CONTROL FLOW:
			ON ENTER:
				try,else,elif,def,...
				try: except as: pass
				with: as:
			ON SPACE:
				try,else,elif,def,...
		ASSERTIONS:
		PRINT: Not technically a keyword but kinda sorta is...it was in py2
	DECORATORS:
		‹2memoized› –––> ‹@memoized›
		‹2memoized↵df›–––>  ‹@memoized↵def f():›
		‹2memoized↵cf›–––>  ‹@memoized↵class f:›
	FUNCTIONS:
		everything from args to the pass
	CLASSES:
		‹c Name›  –––>  ‹class Name¦:›
		‹c Name object›  –––>  ‹class Name(object¦):›
		‹c Name object int›  –––>  ‹class Name(object,int¦):›
	QUICK KEYWORDS:
		‹c↵›  –––>  ‹class _:
		                 ¦›    //Only if we're not directly in a for/while loop

		‹c ›  –––>  ‹class ¦:›

		‹c↵›  –––>  ‹continue↵›  //Only if we are directly in a for/while loop

		‹b ›  –––>  ‹break ›
		‹b↵›  –––>  ‹break↵›

		‹c ›  –––>  ‹class ¦:›

		‹a ›  –––>  ‹assert ¦:›

		‹g ›  –––>  ‹global ¦›
		‹n ›  –––>  ‹nonlocal ¦›

		‹r ›  –––>  ‹return ¦› //Only if we're inside a function
		‹ra › –––>  ‹raise ¦›

		‹r↵›  –––>  ‹return↵¦› //Only if we're inside a function

		‹y↵›  –––>  ‹yield↵¦› //Only if we're inside a function

		‹y ›  –––>  ‹yield ¦› //Only if we're inside a function

		‹y  › –––>  ‹yield from ¦› //Only if we're inside a function

		‹p ›  –––>  ‹print(¦)› //Even though print isn't a keyword in python 3, it was in python 2. This is also a completion.

		‹p↵›  –––>  ‹pass↵›

		‹i↵›  –––>  ‹if True:
		                 ¦›

		‹i ›  –––>  ‹if ¦:› //Only if we're not on the first line (we're more likely to import as a command than start our buffer with an 'if' branch)

		‹i ›  –––>  ‹import ¦› //Only if we are on the first line

		‹if › –––>  ‹if ¦:›

		‹im › –––>  ‹import ¦›

		‹l › –––>  ‹lambda ¦:›

		‹w↵›  –––>  ‹while True:
		                 ¦›

		‹w ›  –––>  ‹while ¦:›

		‹wi › –––>  ‹with ¦:›

		‹wi x › –––>  ‹with x as ¦:›

		‹f↵›  –––>  ‹for _ in ans:
		                 ¦›

		‹f ›  –––>  ‹for ¦ in :› //Only if we're not on the first line

		‹f ›  –––>  ‹from ¦ import›  //Only if we are on the first line, otherwise f makes a for loop

		‹fo › –––>  ‹for ¦ in :› //This works regardless of the line we're on

		‹fr › –––>  ‹from ¦ import›  //This works regardless of the line we're on

		‹d↵›  –––>  ‹def ans():
		                 ¦›              //Only if we're not inside a class

		‹d ›       –––> ‹def ¦():›       //Only if we're not inside a class

		‹d↵›  –––>  ‹def __init__(self):
		                 ¦›              //Only if we are inside a class

		‹d ›       –––> ‹def ¦(self):›   //Only if we are inside a class

		‹t ›  –––>  ‹try:¦›
		‹t↵›  –––>  ‹try:
		                 ¦›


		‹ex ›  –––>  ‹except ¦:›

		On ‹↵›:  ‹try:       –––\    ‹try:
		              pass       \        pass
		              e¦›        /    except:
		                     –––/         ¦›

		On ‹ ›:  ‹try:               ‹if x:
		              pass     –––>       pass
		          ex¦›                except ¦:›

		//Each transition arrow is another successive press of the spacebar
		On ‹ ›:  ‹try:              ‹try:               ‹try:               ‹try:
		              pass    –––>       pass    –––>       pass    –––>       pass
		          ex¦                except:¦›           except:¦›           except:pass¦›


		On ‹↵›:  ‹if x:    –––\    ‹if x:
		              y        \        y
		              e¦›      /    else:     //enter to else
		                   –––/         ¦›

		On ‹ ›:  ‹if x:            ‹if x:            ‹if x:
		              y     –––>        y     –––>        y    //space to elif to else
		              e¦›           elif ¦:›          else:¦›
	FUNCTION DEFINITIONS:

		‹d ›       –––> ‹def ¦():›     //Only if we're not inside a class
		‹d f x›    –––> ‹def f(x¦):›   //Only if we're not inside a class
		‹d f x y›  –––> ‹def f(x,y¦):› //Only if we're not inside a class
		‹d  ›      –––> ‹def ans(¦):›  //Only if we're on the first line
		‹d  ›      –––> ‹def _(¦):›    //Only if we're not on the first line and not inside a class

		‹d ›       –––> ‹def ¦(self):›      //Only if we are inside a class
		‹d f ›     –––> ‹def f(self,¦):›    //Only if we are inside a class
		‹d f x y›  –––> ‹def f(self,x,y¦):› //Only if we are inside a class

	CLASS DEFINITIONS:
		‹c x ›     –––>  ‹class x(¦):›
		‹c x y z›  –––>  ‹class x(y,z¦):›

	ANS:
		. to ans.
		space to ans() or ans[] or ans
		for x in space --> for x in ans (duplicate entry)
		space-function f(ans,ans,ans,ans) (duplicate entry)
		x+  --> x+ans
		*5   –––> ans*5
	MISC:
		''''. –––>  ''.join(|)
		;\n –––> new line

	MATRIX LITERALS:
		[[1,2,3],[4,5,6],[7,8,9]]
	INDEXING:
		ASSIGNMENT SHORTCUT:
			x[1=y]  –––>  x[1]=y
		SPACE INSTEAD OF RIGHT ARROW KEY:
			x[y ,z] –––>  x[y],z
		SPACE
			x[1 2 3]–––>x[1][2][3]
		DOTS
			x..y  –––>  x['y']
			x.3   –––>  x[3]
	SPACE FUNCTIONS:
		f(f(f(f())))
		list map int  ans
		f(ans,ans,ans,ans,ans,ans) (duplocate)
		space-function option in r.py that comlpetes without tab

	LAMBDAS:
		‹lambda  1›        –––>  ‹lambda:1¦›
		‹l  1›             –––>  ‹lambda:1¦›
		‹l   ›             –––>  ‹lambda:None¦›
		‹l x  x+1›         –––>  ‹lambda x:x+1¦›
		‹l x y  x+y›       –––>  ‹lambda x,y:x+y¦›
		‹lambda x y  x+y›  –––>  ‹lambda x,y:x+y¦›

	REORDERING:
		//Use < and > to swap the order of comma-separated values.
		//Use in function declarations, lists, tuples – you name it!
		//Right now the implementation isn't perfect, but it's usually good enough
		//It works because [x,<y] is invalid syntax
		LEFT:
			On ‹<›: ‹[alpha,beta,¦gamma]›  –––>  ‹[alpha,¦gamma,beta]› //This hopefully makes intuitive sense
			On ‹<›: ‹[alpha,¦gamma,beta]›  –––>  ‹[gamma,¦alpha,beta]› //The position of the cursor doesn't change because it should remain next to a comma, and there are no more commas to the left
			On ‹<›: ‹def f(bob,sam,¦ann,tim):›  –––>  ‹def f(bob,¦ann,sam,tim):›
		RIGHT:
			//You should get the idea by now... < goes left and > goes right...
			On ‹>›: ‹[alpha,¦beta,gamma]›  –––>  ‹[alpha,gamma,¦beta]›

	IMPORTS:
		FROM:
			On ‹ ›: ‹f¦›                                   –––>  ‹from ¦ import› //True iff single-line command
			On ‹ ›: ‹fr¦›                                  –––>  ‹from ¦ import› //f, fr, and fro are all microcompleted into from
			On ‹ ›: ‹from¦›                                –––>  ‹from ¦ import›
			On ‹ ›: ‹from npy¦ import›                     –––>  ‹from numpy import ¦› //npy was autocompleted to numpy. Of course, whether this works depends on the context of your completion menu.
			On ‹ ›: ‹from numpy¦ import›                   –––>  ‹from numpy import ¦›
			On ‹ ›: ‹from numpy import ¦›                  –––>  ‹from numpy import *¦› //Import all
			On ‹ ›: ‹from numpy import *¦›                 –––>  ‹from numpy import ¦›
			On ‹ ›: ‹from numpy import ndarray¦›           –––>  ‹from numpy import ndarray as¦›
			On ‹ ›: ‹from numpy import ndarray as array¦›  –––>  ‹from numpy import ndarray as array, ¦›
			On ‹⌫›: ‹from ¦ import› –––>  ‹¦› // Delete it as quickly as you created in-case you didn't mean to import anything afterall
			‹f a b c d e f g›       –––>  ‹from a import b as c, d as e, f as g¦›  //This doesn't take into account autocompletions, but you get the general idea...
		IMPORT:
			On ‹ ›: ‹i¦›  –––>  ‹import ¦› //True iff single-line command
			On ‹ ›: ‹im¦› –––>  ‹import ¦› //i, im, imp, impo, and impor are all microcompleted into import upon pressing space
			On ‹ ›: ‹import npy¦›                –––>  ‹import numpy as ¦›
			On ‹ ›: ‹import numpy¦›              –––>  ‹import numpy as ¦›
			On ‹ ›: ‹import numpy as np¦›        –––>  ‹import numpy as np, ¦›
			On ‹ ›: ‹import numpy as np¦›        –––>  ‹import numpy as np, ¦›
			On ‹ ›: ‹import numpy as np, time¦›  –––>  ‹import numpy as np, time as ¦›
			On ‹↵›: ‹import numpy as¦›           –––>  ‹import numpy↵¦›  //'import numpy as' is invalid syntax for a line of code

	IMAGINARY OPERATORS:
		--:   x--  –––>  x-=1
		++:   x++  –––>  x+=1

		..:   x..y..z –––> x['y']['z']
		.:    x.1.2   –––> x[1][2]

		[=:   x[=y –––> x=x[y]
		(=:   x(=y –––> x=x(y)
		]=:   x]=y –––> x=y[x]
		)=:   x)=y –––> x=y(x)

		.=:   x.=y   –––>  x=x.y
		=.x:  x=.y   –––>  x.y=y
		..=:  x..=y  –––>  x.y=x
		=..:  x=..y  –––>  x=y.x

		nin:  x nin y  –––>  x not in
		isnt: x isnt y –––>  x is not y
		n:    x n y    –––>  x in y
		o:    x o y    –––>  x or y
		a:    x a y    –––>  x and y

			EDGE CASES:
				for x nin y:   –/–> for x not in y:
		=]:(Not implemented)

	COMPARATORS:
		DRAGGING:
			On ‹=›: ‹f(x==¦)› –––> ‹f(x)==¦›
			f(x>==)   --->  f(x)>=
			f(x<==)   --->  f(x)<=
			f(x===)   --->  f(x)==
			f(x!==)   --->  f(x)!=
			f(x>>)    --->  f(x)>
			f(x<<)    --->  f(x)<
		EQUALITY:
			//Instead of =, insert ==
			On ‹=›: ‹if x¦:› –––> ‹if x==¦:›
			On ‹=›: ‹assert x¦:› –––> ‹if x==¦:›
			EDGE CASES:
				On ‹=›: ‹x=y¦› –/–> ‹x=y==¦:›
				On ‹=›: ‹x=y¦› –––> ‹x=y=¦:›           //x=y=z is valid, commonly used syntax
				On ‹=›: ‹if f(x¦):› –/–> ‹if f(x==¦):›
				On ‹=›: ‹if f(x¦):› –––> ‹if f(x=¦):›  //Keyword arguments, like f(x=1), use a single == instead of a double ==
		INEQUALITY:
			//(See INEQUALITIES under SHIFT SAVERS)

	SHIFT SAVERS:
		//When possible, avoid having to press the shift key
		INEQUALITIES:
			//Where possible, turn .= to >= and ,= to <=
			//This saves you the bother of pressing the shift key
			On ‹=›: ‹if x,¦:›    –––> ‹if x<=¦:›     //Note that although ‹if x,=y:› is valid syntax, it's weird to compare a tuple to y in this way, and most of the time we're probably better off turning x,= into x<=
			On ‹=›: ‹if x.¦:›    –––> ‹if x>=¦:›     //Note that even though we talked about the imaginary '.=' operator, it doesn't make sense in this context, so it's ok to run .= into >=
			On ‹=›: ‹print(x,¦)› –––> ‹print(x<=¦)›
			On ‹=›: ‹print(x.¦)› –––> ‹print(x>=¦)›
			EDGE CASES:
				‹x.=y›  –––>  ‹x=x.y¦›
				‹x.=y›  –/–>  ‹x>=y¦›

		COLON:
			//When possible, turn ';' into ':'.
			SLICING:
				//In particular, you will often want to use ; to : when writing things like x[:5] or x[::-1].
				‹x[;]›       –––>  ‹x[:]›
				‹x[1;]›      –––>  ‹x[1:]›
				‹x[i;]›      –––>  ‹x[i:]›
				‹x[;;-1]›    –––>  ‹x[::-1]›
				‹x[1;2;3]›   –––>  ‹x[1:2:3]›
				‹x[a;b;c]›   –––>  ‹x[a:b:c]›
				‹x[1;2,3;4]› –––>  ‹x[1:2,3:4]›

		UNDERSCORE:
			//When possible, turn - into _. This is a recurring motif in other completions as well.
			FOR:
				On ‹-›: ‹for ¦ in:›  –––>  ‹for _ in ¦:›  //Although ‹for ¦ in:› seems like a strange starting point, note that other completions can take you there
				On ‹-›: ‹[for ¦ in]› –––>  ‹[for _ in ¦]›

			FUNCTION CALL ARGUMENT:
				On ‹↵›: ‹print(-)›   –––>  ‹print(_)›
				On ‹↵›: ‹print(x,-)› –––>  ‹print(x,_)›
				On ‹)›: ‹print(-¦›   –––>  ‹print(_)¦›  //TODO
				On ‹,›: ‹print(-¦)›  –––>  ‹print(_,¦)›
				On ‹ ›: ‹print(-¦)›  –––>  ‹print(_,¦)›

			DECLARATION:
				‹var-name-with-underscores=5›          –––>  ‹var_name_with_underscores=5›
				‹def -func-name-(arg-1,-arg-2,-,--):›  –––>  ‹def _func_name_(arg_1,_arg_2,_,__):›
				‹lambda -x,y-:None›                    –––>  ‹lambda _x,y_:None› //TODO
				On ‹-›: ‹def f():     –––\   ‹def f():
				             var¦›    –––/        var_¦›   //Why would you start a line in a function with an expression like x-y? That seems fairly useless, almost all the time. Instead, turn - into _ without having to double-tap
				EDGE CASES:
					‹x--›  –/–> ‹x__›  //This is because of a different microcompletion: the -- operator, which makes ‹x--› –––> ‹x-=1¦›

			GLOBAL NONLOCAL DEL IMPORT:
				//A - is a syntax-braking character inside del, import, global or nonlocal. Turn it into an underscore.
				‹del      x-,-y,-›  –––>  ‹del      x_,_y,_¦›
				‹global   x-,-y,-›  –––>  ‹global   x_,_y,_¦›
				‹nonlocal x-,-y,-›  –––>  ‹nonlocal x_,_y,_¦›
				‹import   x-,-y,-›  –––>  ‹import   x_,_y,_¦›
				‹from - import -›   –––>  ‹from _ import _¦›

			DOUBLE TAP:
				//Instead of pressing shift and - to get _, you can often just press - twice
				On ‹-›: ‹f(-¦)›  –––>  ‹f(_¦)›
				‹print(----)›  –––>  ‹print(__¦)›

			SPACEBAR:
				‹if - in l:›         –––> ‹if _ in l:¦›
				‹while - in l:›      –––> ‹while _ in l:¦›
				‹x and - ›           –––> ‹x and _ ¦›
				On ‹ ›: ‹if -¦:›     –––> ‹if _ ¦:›
				On ‹ ›: ‹while -¦:›  –––> ‹while _ ¦:›
				On ‹ ›: ‹x and -¦:›  –––> ‹x and _ ¦:›
				On ‹ ›:‹[-|]› --> ‹[_ |]›
				EDGE CASES:
					‹x- ›    –/–>  ‹x_ ¦›
					‹x- ›    –/–>  ‹x_ ¦›
					‹f()- ›  –/–>  ‹f()_ ¦›
				COMBOS:
					On ‹ ›: ‹print(-¦)›  –––> ‹print(_,¦)›
					On ‹ ›: ‹if -¦ else› –––> ‹if _ else ¦›

			OPERATORS:
				//-*2 is invalid syntax, but _*2 is
				‹-*›    –––>  ‹_*¦›
				‹-+›    –––>  ‹_+¦›
				‹-[0]›  –––>  ‹_[0]¦›


			(MORE TO COME: There are definitely more places we should put this type of completion that have neither been implemented nor listed here)

		NUMBERS TO CHARACTERS:
			1:
				//When possible, treat ‹1› as either ‹!› or ‹not›
				!=:
					//Here, we treat ‹1› like ‹!› when using ‹=› to get ‹!=›
					‹x 1=›      –––> ‹x !=¦›
					‹if x 1= y› –––> ‹if x != y¦›
					‹f()1=›     –––> ‹f()!=¦›
					‹[a 1= 2]›  –––> ‹[a != 2]¦›
					EDGE CASES:
						//When turning ‹1› into ‹!=› would break syntax, don't do it
						‹x and 1=› –/–> ‹x and !=¦›  //Don't do it after a keyword...
						‹if 1=›    –/–> ‹if !=¦›
						‹a=1==2›   –/–> ‹a=!=2¦›
						‹[1==2]›   –/–> ‹[!=2]¦›
						‹(1==2)›   –/–> ‹(!=2)¦›
						‹{1==2}›   –/–> ‹{!=2}¦›
				not:
					//Because we sometimes treat ‹1› like ‹!›,
					//    and we sometimes treat ‹!› like ‹not›,
					//    when possible, treat ‹1› as ‹not›
					‹if 1y:›      –––> ‹if not y:¦›
					‹x and 1y›    –––> ‹x and not y›
					‹x and 1[]›   –––> ‹x and not [¦]›
					‹[x,1y]›      –––> ‹[x,not y]¦›
					‹f(1y)›       –––> ‹f(not y)¦›
					‹while 1f():› –––> ‹while not f():¦›
					EDGE CASES:
						‹while 1:›   –––> ‹while 1:¦›
						‹while 1:›   –/–> ‹while not :¦›

						‹while 12:›  –––> ‹while 12:¦›
						‹while 12:›  –/–> ‹while not 2:¦›

						‹while 1.:›  –––> ‹while 1.:¦›
						‹while 1.:›  –/–> ‹while not .:¦›

						‹while 1+2:› –/–> ‹while not +2:¦›

						‹[x,1]›      –––> ‹[x,1]¦›
						‹[x,1]›      –/–> ‹[x,not ]¦›
				! and !!:
					//Because pseudo-terminal treats ‹!echo hello› as a shell command, we treat 1 as ! and 11 as !! so that we don’t need to press the shift key.
					//Note that this completion only occurs if the 1's are the first characters in the entire text buffer (! and !! have no effect anywhere else)
					‹11pwd›        –––> ‹!!pwd¦›
					‹1pwd›         –––> ‹!pwd¦›
					‹1echo hello›  –––> ‹!echo hello›
					‹11echo hello› –––> ‹!!echo hello›
					EDGE CASES:
						‹1›   –/–> ‹!¦›
						‹11›  –/–> ‹!!¦›
						‹111› –––> ‹111¦›
						‹111› –/–> ‹!11¦›
						‹111› –/–> ‹!!1¦›

			2:
				//When applicable, treat ‹2› as ‹@› in the context of a function or class decorator
				//To trigger, the ‹2› must be at the start of a line, ignoring whitespace. The pressed key must be a letter or underscore (a character capable of starting a variable name).
				‹2memoized›    –––>  ‹@memoized¦›
				‹  2memoized›  –––>  ‹  @memoized¦›
				EDGE CASES:
					‹2›            –/–>   ‹@¦›
					‹22memoized›   –/–>   ‹@2memoized¦›
					‹§2memoized›   –/–>   ‹§@memoized¦›  where ‹§› is any character other than ‹ ›

			3:
				//When possible, treat ‹3› as ‹#› to insert a comment at the end of a line
				//This pretty much only happens directly after ‹)›, ‹]›, ‹}› when there is nothing on the same line after the cursor
				‹print()3›        –––> ‹print()#¦›
				‹print()  3›      –––> ‹print()  #¦›
				‹  print()  3›    –––> ‹  print()  #¦›
				‹print()3comment› –––> ‹print()#comment¦›
				‹[]3›             –––> ‹[]#¦›
				‹[x,y]3›          –––> ‹[x,y]#¦›
				‹x={}3›           –––> ‹x={}#¦›
				‹x={}3comment›    –––> ‹x={}#comment¦›
				‹x={}  3comment›  –––> ‹x={}  #comment¦›
				EDGE CASES:
					‹print([]3)› –/–> ‹print([]#)¦›
					‹[3]›        –/–> ‹[3#]¦›

			5:
				//When applicable, treat ‹5› as if it were ‹%›, or ‹55› as if it were ‹%%›
				//This is used for iPython magics, which are always at the start of a line (ignoreing whitespace) and prefixed by % or %%
				‹5magic›   –––> ‹%magic¦›
				‹55magic›  –––> ‹%%magic¦›
				‹  5magic› –––> ‹  %magic¦›
				EDGE CASES:
					‹5m›       –––> ‹%m¦›
					‹5›        –/–> ‹%¦›
					‹55›       –/–> ‹%%¦›
					‹55m›      –––> ‹%%m¦›
					‹555magic› –/–> ‹%%%magic¦›
					‹x5magic›  –/–> ‹x%magic¦›

			8:
				//When calling or declaring arguments, or making elements in lists tuples or dict literals,
				//‹8› can be used as the vararg ‹*› and ‹88› can be used as the kwarg ‹**›
				FUNCTION DECLARATIONS:
					‹def f(8args):›          –––> ‹def f(*args):¦›          //For function definitions
					‹def f(8args,88kwargs):› –––> ‹def f(*args,**kwargs):¦›
					‹def f(x,y,8,z):›        –––> ‹def f(x,y,*,z):¦›
				SETS LISTS TUPLES:
					‹[8x]›    –––> ‹[*x]¦›                    //For data literals
					‹{88x}›   –––> ‹[**x]¦›
					‹(z,88x)› –––> ‹(z,**x)¦›
					‹z,88x›   –––> ‹(z,**x)¦›
					EDGE CASES:
						[x,8]  –/–>  [x,*]
						[x,88] –/–>  [x,**]
						{8}    –/–>  {*}
				LAMBDAS:
					‹lambda 8args:None›      –––> ‹lambda *args:None¦›       //For lambda declarations  //TODO
					‹lambda x,y,8args:None›  –––> ‹lambda x,y,*args:None¦›
					‹lambda 88kargs:None›    –––> ‹lambda **kwargs:None¦›
				FUNCTION CALLS:
					‹print(8args)›           –––> ‹print(*args)¦›            //For function calls
					‹print(88kwargs)›        –––> ‹print(**kwargs)¦›
					‹print(x,y,88kwargs)›    –––> ‹print(x,y,**kwargs)¦›
					EDGE CASES:
						print(8)  –/–>  print(*)

			9:
				//If next character breaks syntax that () would fix, treat ‹9› as if it were originally ‹(›
				//Note that normally ‹(› –––> ‹(¦)› from another completion, which is why we surround the cursor instead of simply inserting ‹(›
				‹9hello› –––> ‹(hello¦)›
				‹9x›     –––> ‹(x¦)›
				‹9jello› –––> ‹(jello¦)›
				EDGE CASES:
					‹9j›  –––> ‹9j¦›   //9j is a valid token...
					‹9jj› –––> ‹(jj¦)› //...but 9jj is not

PSEUDO TERMINAL COMMANDS:
	SUMMARY:
	    <Input Modifier>     <Namespace History>    <Simple Timer>     <File System>         
	    MODIFIER ON          UNDO                   TICTOC             CD                    
	    MODIFIER OFF         UNDO ON                TICTOC ON          LS                    
	    MODIFIER SET         UNDO OFF               TICTOC OFF         PWD                   
	    SMODIFIER SET        UNDO CLEAR                                CAT                   
	                         UNDO ALL               <Profiler>         RUN                   
	    <Stack Traces>                              PROF               CDP                   
	    MORE                 <Prompt Toolkit>       PROF ON            CPWD                  
	    MMORE                PT ON                  PROF OFF           NCAT                  
	    DMORE                PT OFF                 PROF DEEP          CCAT                  
	                                                                   OPEN                  
	    <Command History>    <Saving Settings>      <Toggle Colors>                          
	    HISTORY              PT SAVE                FANSI ON           <Documentation>       
	    AHISTORY             PT RESET               FANSI OFF          HELP                  
	    GHISTORY             SET STYLE                                 HHELP                 
	    CHISTORY                                    <Others>                                 
	                         <Shell Commands>       SUSPEND            <Module Reloading>    
	    <Clipboard>          !                      SHELL              RELOAD ON             
	    COPY                 !!                     LEVEL              RELOAD OFF            
	    PASTE                                       DITTO                                    
	    SPASTE               <Inspection>           EDIT               <Deprecated>          
	                         ?/                     VARS               IPYTHON               
	    <'ans' History>      ?.                     RANT               IPYTHON ON            
	    NEXT                 ?                      FORK               IPYTHON OFF           
	    PREV                 ??                     ARG                RETURN NOW            
	    PREV ON              ???                                       GC OFF                
	    PREV OFF             ????                                      GC ON                 
	    PREV CLEAR           ?????                                                           
	    PREV ALL                                                                             

	<Input Modifier>
		// In pseudo-terminal, modifiers are preprocessors for your code.
		// You can turn them on or off, or specify your own macro where | is the replacement
		MODIFIER ON  : Enables modifiers
		MODIFIER OFF : Disables any modifier
		MODIFIER SET : See https://asciinema.org/a/mb52gHyuFH92SXf32H6cuE4XR
		SMODIFIER SET: See https://asciinema.org/a/7SVhDzt4yho4hggja9Muh5ffV

	<Stack Traces>
		MORE : Shows you a bigger stack trace. Always works.
		MMORE: Shows you a more detailed stack trace with the values of every variable at every stack frame,
			along with big chunks of code, but requires an external library. It's extremely useful for debugging.
		DMORE: Lauches a post-mortem debugger on the last error. If you have pudb, it will launch that debugger
			instead of the defaut pdb library. It's useful when you want to get information that MMORE can't tell you.

	<Command History>
		HISTORY : Prints a list of all commands that you've entered that didn't cause errors. All green commands were single-liners,
			and all yellow commands were multi-liners. Yellow commands alternate between bold and not-bold so you can visually distinguish
			one multiline command from the next.
		AHISTORY: Stands for 'All History'. Prints all history entries from the current session, including ones that made errors while running. 
			Useful for getting numbers to plug into EDIT.
		GHISTORY: Prints a list of all single-line commands that didn't have errors. GHISTORY stands for 'green history', because in HISTORY all
			single-liners are printed in green.
		CHISTORY: Stands for 'Copy History'. Copies the output of HISTORY to your clipboard.

	<Clipboard>
		COPY  : Copies str(ans) to your clipboard.
		PASTE : Runs code from your clipboard.
		SPASTE: Sets ans to the string from your clipboard.

	<'ans' History>
		// See https://asciinema.org/a/TFf9OvoRj1vmRqMPYDhHEyDsV
		PREV      : revert's ans to it's previous value
		NEXT      : The opposite of PREV. Undo is to PREV as redo is to NEXT.
		PREV ON   : Enables tracking ans's history. This is the default.
		PREV OFF  : Disables tracking ans's history. This can save memory.
		PREV CLEAR: Deletes all ans history, which might save some memory. I rarely use it in practice.
		PREV ALL  : An alternative to typing PREV PREV PREV PREV PREV over and over again. This undoes ans as many times as it can.













#Guidelines for this document (for ryan to read this section):
	- ‹ and › are used instead of quotes because ' and " might be characters in a given completion
	- All completions shown should minimize the use of other irrelevant completions, because it makes things more confusing. Try using –/–> if that solves your issue.
	- Contextual completions as well as global completions (the difference between conetxteual: "On ‹x›: ‹y=¦›  –––>  ‹y=x¦›" vs global aka "‹y=x› –––> ‹y=x¦›). Contextual
		has an "on keypress", and the left ‹› and right ‹› both have cursor positoins. The global ones have
		no cursor in the left ‹› as it implicitly starts at the last character, and all chacters shwn in tat ‹› are pressed to get the ‹› on the right.
	- Ignore completions that are super common, like ( --> () and preserving indents when pressing enter key etc
	- Definition of breaking syntax and how it's used to make microcompletions fundamentally different from other kinds of completions (no selecting from a menu of options)
	- Don't need cursor on end of line to hit enter (no need to escape those functoin-call parenthesis)
	- Things marked 'TODO' have not yet been implemented but will eventually be
	- Not listing all the billions of completions which we need to counteract bad sideffects (like . –––> ans.  –––>  .1)
	– One man's bloat is another man's treasure

Tips and tricks:
	Debugging:
		Debuggers:
			- Uses both pudb and ptpdb. Will probably only use one later on, perhaps pudb (as it's being actively maintained, is agnostic to prompt toolkit version, has post-mortem debugging)
			- From the debugger, launch pseudo_terminal. Yeah, that's a power-move.
			- Using continue instead of quit in the debugger leaves the debugger running, and will trigger the breakpoint next time you use that function in pseudo_terminal.
			- Because exiting the debugger throws an error, it also prevents the rest of the code in your buffer (after the debugger) from running. Often this is desirable,
				actually. Of course, if you don't want this, just use continue instead
		ic():
			This function uses the icecream library to make monitoring values easy. Try ‹hello='HELLO';ic(hello)›

	Control+E:
		It even works with pseudo_terminal() and REUTRN, going up and down levels. Now THAT'S tenacity.


Todo:
	Debugger:
		- I want it to terminate once it reaches the top of the stack we put it on....because...
		- ...Conceptual issue: If you run into an error when debugging, or just continue off the edge, pseudo_terminal now runs in the debugger and for some reason you can't quit it.
		- I want a DMORE (post-mortem debugger). Honestly when the debugger crashes it's fuckin' useless (it never actually crashes beause pseudo-terminal catches the error. Which is a conceptual flaw I don't know how to work around.)