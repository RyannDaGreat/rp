This is a help document for using RP's pseudo_terminal.

SUMMARY
	This documention is for RP (aka RyanPython).
	It's not totally organized yet, but you can search through it to find what you want.
	It's not yet complete, but includes a lot of important information.
	It's an extension of the HELP command.
	If you have any questions, you can email sqrtryan@gmail.com (for Ryan Burgert, the author of this package)
	Note: The only reason this is a .py file and not a .txt file is to make it conveniently be included in my pypi package. It's not an actual python file. This might change in the future.

	Important Backslash Commands:
		\da \co \pa \vi \tbp \23p \ya \sw \tts \lo \sa \pu 

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
		Invariant to prompt_toolkit version. This should run anywhere fine. (Todo: Make it have 0 dependencies)
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
	⌥ X    delete the first character of every line
	⌥ v    edit current text in vim (equivalent to the \vi microcompletion)
	⌥ ␣    forcibly insert a space character, skipping any microcompletions
	⌥ ⌫    backspace a whole word
	⌥ ←    jump back one word
	⌥ →    jump forward one word
	⌥ ↓    jump down 10 lines
	⌥ ↑    jump up 10 lines
	⌥ !    run shell command
	⌥ #    comment out the entire buffer and run that comment (it will do nothing lol)
	⌥ n    executes 'NEXT', changing the value of 'ans' (useful in combination with \rpa and \an)
	⌥ p    executes 'PREV', changing the value of 'ans' (useful in combination with \rpa and \an)
	⌥ r    similar to \rpa, except it clears the buffer. Sets ans to the current buffer as a string
	⌃ a    insert str(ans)   Equivalent to \an
	⌥ ⌃ a  insert repr(str(ans))  Equivalent to \sa
	⌥ q    equivalent to \da: clears the current buffer
	⌥ (    insert ( at current position and ) at the end of the line without moving the cursor to the end of the line
	⌥ [    insert [ at current position and ] at the end of the line without moving the cursor to the end of the line
	⌥ )    insert ) at the end of the line without moving the cursor to the end of the line
	⌥ ]    insert ] at the end of the line without moving the cursor to the end of the line
	⌃ t    loads previous buffer in history regardless of where cursor is (stands for top). Faster than spamming the up arrow key
	⌃ b    loads next buffer in history regardless of where cursor is (stands for bottom). Faster than spamming the down arrow key
	LESS IMPORTANT AND MAYBE REMOVED IN FUTURE:
		//While these keyboard shortcuts are kind of silly, I do find myself using them quite often
		⌃ h    inserts 'HISTORY'
		⌃ p    inserts 'PREV' (then 'NEXT', if pressed again)
		⌥ m    inserts 'MORE' (then 'MMORE', if pressed again)
		⌥ s    inserts 'self'
		⌥ ⌃ v  edit current text in vim (equivalent to the \vi microcompletion)

MICROCOMPLETIONS:
	//This section covers only the microcompletions that take place in the context of a single line

	BACKSLASH COMMANDS:
		WITH ARGUMENTS:
			\sa   save file       (used like ‹`file.py\sa›. Saves the current buffer to 'file.py'. Will create a backup file if we overwrite something.)
			\wr   write file      (used like ‹`file.py\wr›. Saves the current buffer to 'file.py'. Not as safe as save file, because it will not create a backup file when overwriting.)
			\lo   load file       (used like ‹`file.py\lo›. Loads 'file.py' into the current buffer)
			\re   replace         (used like ‹`old`new\re›. It's a search-and-replace)
			\py   python          (used like ‹`repr\py›, ‹`str.upper\py›, or ‹`print_fix\py› etc. Replaces current buffer's text with function(currenttext))
			\go   goto            (used like ‹`10\go›. Bring the cursor to that line number.)
			\dtl  delete to line  (used like ‹`5\dtl›. Like d5G in vim.)
			\ca   cancel          (cancels any command you would have written and deletes the arguments. More civilized than spamming undo or backspace.)
			\?c   source code     (will enter the source code of any expression given in the first argument. Can also be used with no `s, where the entire buffer is the expression)
			\/c   source code     (is an alias for ?c)
		WITHOUT ARGUMENTS:
			\lo   load file               (loads a file just like `file.py\lo does, except it opens a dialog to let you choose the file so you dont have to type it manually)
			\db   debugger                (toggles the existence of 'debug()' on the top of your prompt without moving your cursor)
			\pu   pudb (other debugger)   (similar to \db, pudb is an alternative debugger, and this command also toggles a line on the top of the buffer. Whether you use this or \db is a matter of prefernece.)
			\vi   vim                     (opens up the current buffer in vim. Edit your code, then save the temp file and close vim. Your cursor's position will be shared between vim and rp.)
			\ed   editor                  (opens up the current buffer in some text editor; might be nano, might be vim. Depends on what you have. This command is an alternative to \vi)
			\ac   align char              (inserts ‹→›, aka the alignment character. Used before \al. See https://asciinema.org/a/KjFS2lT0shRyv4r82RtFENzlo)
			\al   align                   (aligns all alignment characters to the same column. Used after inserting \ac in multiple different places.)
			\co   copy                    (copies the current buffer to your clipboard)
			\pa   paste                   (equivalent to control+v)
			\spa  string paste            (pastes current clipboard as a python string literal)
			\3pa  commented paste         (pastes current clipboard, but commented out. Can also use this command with arguments: `    \3pa   makes comments with four spaces of indentation, for example.)
			\wco  web copy                (applies WCOPY to the current buffer's string. Use this to copy text between computers)
			\wpa  web paste               (inserts the output of WPASTE at your cursor position. Use this to paste text from another computer.)
			\wspa web string paste        (inserts the output of repr(WPASTE) at your cursor position. Use this to paste text from another computer.)
			\lco  local copy              (same as \wco  except it uses LCOPY  instead of WCOPY )
			\lpa  local paste             (same as \wpa  except it uses LPASTE instead of WPASTE)
			\lspa local string paste      (same as \wspa except it uses LCOPY  instead of WCOPY )
			\tco  tmux copy               (applies TCOPY to the current buffer's string. Use this to copy text to a tmux session)
			\tpa  tmux paste              (inserts the output of TPASTE at your cursor position. Use this to paste text from a tmux session. This is useful because often tmux will press the enter key when pasting a multiline string.)
			\tspa tmux string paste       (inserts the output of repr(TPASTE) at your cursor position. Use this to paste text from a tmux session. This is useful because often tmux will press the enter key when pasting a multiline string.)
			\t3pa tmux commented paste    (inserts the output of TPASTE, but commented out. See \3pa for more information.)
			\vco  vim copy                (applies VCOPY to the current buffer's string. Use this to copy text to vim's default register)
			\vpa  vim paste               (inserts the output of VPASTE at your cursor position. Use this to paste text vim's default register)
			\vspa vim string paste        (inserts the output of repr(VPASTE) at your cursor position. Use this to paste text vim's default register as an escaped string)
			\an   ans                     (inserts str(ans) at current cursor position)
			\3an  commented ans           (inserts str(ans), but commented out. See \3pa for more information.)
			\sa   string ans              (inserts repr(ans) at current cursor position)
			\da   delete all              (deletes all text in the current buffer)
			\sw   strip whitespace        (strips all trailing whitespace in the buffer)
			\sc   strip comments          (removes all #comments in the buffer)
			\d0l  delete empty lines      (removes empty lines in the buffer. d0l means there can be 0 consecutive empty lines)
			\rl   reverse lines           (reversed the order of all lines of text in the buffer)
			\sl   sort lines              (sorts all lines in the buffer in alphabetical order)
			\ya   yapf autoformatter      (autoformats your current code buffer using google's yapf library)
			\bla  black autoformatter     (autoformats your current code buffer using the 'black' library: pypi.org/project/black )
			\sim  sort imports            (sorts and organizes all imports in the current buffer, using the 'isort' library)
			\rms  remove star             (turns all 'from x import *' into explicit 'from x import y,z,...' etc)
			\fn   function name           (writes the name of the current function)
			\gg   go to top               (like gg in vim. bring cursor to the top of the buffer)
			\GG   go to bottom            (like G in vim. bring cursor to the bottom of the buffer)
			\vO   insert line above       (like O in vim. Inserts a new line above the current line.)
			\vo   insert line below       (like o in vim. Inserts a new line below the current line.)
			\mla  multi line arguments    (turns a lengthy def into a multi line def. See https://asciinema.org/a/RHuWRKsbwvkH3P28XZ81MnFYJ)
			\tbp  toggle big parenthesis  (enables/disables using big parenthesis on a given line https://asciinema.org/a/jhxmIcRogKp4yJy1gojIZBAem)
			\tts  tabs to spaces          (turns all tabs in the buffer into 4 spaces)
			\23p  python 2 to 3           (converts python2 code to python3 code: "print raw_input('>>>')") --> "print(input('>>>'))")
			\fo   for-loopify             (envelops the whole buffer into a for loop. Useful for when you have a command but just want to run it over without DITTO, which pollutes HISTORY)
			\wh   while-loopify           (envelops the whole buffer into a 'while True' loop. Useful for when you have a command but just want to loop it indefinitely)
			\de   functionify             (envelops the whole buffer into a function body)
			\lss  LS SEL                  (lets you select a file or folder and inserts the absolute path as a string)
			\lsr  (Relative) LS SEL       (lets you select a file or folder and inserts the relative path as a string)
			\rpr  repr                    (is equivalent to `repr\py  It will turn your buffer into a string literal)
			\fi   from import swap        (when you're on a line that goes like "from x import y", turns it into "import x". Vice versa.)
			\en   enumeratify             (Use when in a for-loop block header. Turns whatever it is into enumerated form. For example, ‹for x in y:› to ‹for |,x in enumerate(y):)
			\rpa  repr to ans             (sets ans to the current buffer's text)
			\lg   load gist               (treats the current buffer as a Github Gist URL, and tries to load it into the buffer. If it's a git.io shortened url, you only need to specify the title (for example, if using git.io/A3FC you can just use A3FC))
			\sg   save gist               (saves the current buffer as a Github Gist and sets 'ans' to the url of the gist)
			\dtb  delete to bottom        (deletes all lines below the cursor. Useful for getting lines after something like CHIST then \pa)
			\dtt  delete to top           (deletes all lines above the cursor. Useful for getting lines after something like CHIST then \pa)
			\dgx  deepgenx                (auto-completes your code using deepgenx. See https://deepgenx.com/. It's like GitHub Copilot, except open source and made with GPT-J. Needs internet.)
			\gpt  gpt3                    (auto-completes your code with gpt3. Needs internet. Mostly just for fun...but might have good uses.)
			\min  minify                  (Minifies your code - making it as small as possible. Uses https://github.com/dflook/python-minifier)

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
		CONTROL FLOW:shorturl.at/oIY16
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
		On ?:  print(x[thing¦]) –––> print(x[thing])?¦   //Don't have to move cursor to use inspection ?'s
		On \n: ans[5/¦] –––> ans[5]?\n¦
		On ‹-›: ‹def func(x,y,z)¦:›  –––>  ‹def func(x,y,z)->¦:›     // - goes to -> in functions
		On ‹-›: ‹def func(x,y,z)->¦:›  –––>  ‹def func(x,y,z)->¦:›   // nothing happens
		On ‹>›: ‹def func(x,y,z)->¦:›  –––>  ‹def func(x,y,z)->¦:›   // nothing happens

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
		 snt: x snt y  –––>  x is not y
		n:    x n y    –––>  x in y
		o:    x o y    –––>  x or y
		a:    x a y    –––>  x and y
		s:    x s y    –––>  x is y

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
			ARGUMENT TYPE HINTS:
				On ‹;›: ‹def f(x|):›  --->  ‹def f(x:|):›
			DICT LITERALS:
				On ‹;›: ‹{x|}›  --->  ‹x:|›

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
						‹1j›       –/–> ‹not j¦›  //1j is a valid literal
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
					‹def f(88kwargs):› –––> ‹def f(**kwargs):¦›
					‹def f(8args,88kwargs):› –––> ‹def f(*args,**kwargs):¦›
					‹def f(8args,8kwargs):› –––> ‹def f(*args,**kwargs):¦›  //TODO: Because we know that we can only have one *args in a function definition, the next * must be for kwargs, letting us save one keystroke   
					                                                        // (likewise, TODO: ‹def f(*args,*kwargs):› –––> ‹def f(*args,**kwargs):›)
				FUNCTION CALLS:
					‹print(8args)›           –––> ‹print(*args)¦›            //For function calls
					‹print(88kwargs)›        –––> ‹print(**kwargs)¦›
					‹print(x,y,88kwargs)›    –––> ‹print(x,y,**kwargs)¦›
					‹f(8args):›        –––> ‹f(*args¦)›
					‹f(88kwargs):›        –––> ‹f(**kwargs¦)›
					EDGE CASES:
						print(8)   –/–>  print(*)
						‹f(8j):›   –-–> ‹f(8j)›   // TODO
						‹f(8j):›   –/–> ‹f(*j)›   // TODO
						‹f(8jj):›  –-–> ‹f(*jj)›  // TODO (Since 8j is a valid literal, it should activate the *'s on the next character that breaks syntax...)
				SETS LISTS TUPLES:
					‹[8x]›    –––> ‹[*x]¦›                    //For data literals
					‹{88x}›   –––> ‹[**x]¦›
					‹{8x}›    –––> ‹[**x]¦› // TODO: Since we're in a dict literal, we know that a single * isn't an option; therefore it must be ** (saving one keystroke)  (likewise, TODO: ‹{*x}› –––> ‹[**x]¦›)
					‹(z,88x)› –––> ‹(z,**x)¦›
					‹z,88x›   –––> ‹(z,**x)¦›
					EDGE CASES:
						[x,8]  –/–>  [x,*]
						[x,88] –/–>  [x,**]
						{8}    –/–>  {*}
						[8j]   –-–> [8j]   // TODO
				LAMBDAS:
					‹lambda 8args:None›      –––> ‹lambda *args:None¦›       //For lambda declarations  //TODO
					‹lambda x,y,8args:None›  –––> ‹lambda x,y,*args:None¦›
					‹lambda 88kargs:None›    –––> ‹lambda **kwargs:None¦›

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
		ALL COMMANDS:
			<Input Modifier>        <Namespace History>    <Inspection>             <File System>
			MOD ON                  UNDO                   ?                        RM
			MOD OFF                 UNDO ON                ??                       RN
			MOD SET                 UNDO OFF               ???                      MV
			SMOD SET                UNDO CLEAR             ?.                       LS
			                        UNDO ALL               ?v                       LST
			<Stack Traces>                                 ?s                       CD
			MORE                    <Prompt Toolkit>       ?t                       CDP
			MMORE                   PT ON                  ?h (?/)                  CDA
			DMORE                   PT OFF                 ?e                       CDB
			AMORE                   PT                     ?p                       CDU
			GMORE                                          ?c                       CDH
			HMORE                   <RP Settings>          ?i                       CDZ
			VIMORE                  PT SAVE                ?r                       CDQ
			PIPMORE                 PT RESET                                        CAT
			IMPMORE                 SET TITLE              <Others>                 NCAT
			PREVMORE                SET STYLE              RETURN  (RET)            CCAT
			NEXTMORE                                       SUSPEND (SUS)            ACAT
			                        <Shell Commands>       WARN                     CATA
			<Command History>       !                      GPU                      NCATA
			HISTORY    (HIST)       !!                     TOP                      CCATA
			GHISTORY   (GHIST)      SRUNA                  TAB                      ACATA
			AHISTORY   (AHIST)      SSRUNA                 TABA                     RUN
			CHISTORY   (CHIST)                             MONITOR                  RUNA
			DHISTORY   (DHIST)      <Simple Timer>         UPDATE                   PWD
			VHISTORY   (VHIST)      TICTOC                 ANS PRINT ON   (APON)    CPWD
			ALLHISTORY (ALLHIST)    TICTOC ON              ANS PRINT OFF  (APOF)    APWD
			                        TICTOC OFF             ANS PRINT FAST (APFA)    TAKE
			<Clipboards>                                   SHELL (SH)               MKDIR
			COPY                    <Profiler>             LEVEL                    OPEN
			PASTE                   PROF                   DITTO                    OPENH
			EPASTE                  PROF ON                EDIT                     OPENA
			WCOPY                   PROF OFF               VARS                     DISK
			WPASTE                                         RANT                     DISKH
			TCOPY                   <Toggle Colors>        FORK                     TREE
			TPASTE                  FANSI ON               WANS                     TREE ALL
			LCOPY                   FANSI OFF              ARG                      TREE DIR
			LPASTE                                         VIM                      TREE ALL DIR
			VCOPY                   <Module Reloading>     VIMH                     FD
			VPASTE                  RELOAD ON              VIMA                     FDA
			FCOPY                   RELOAD OFF             AVIMA                    FDT
			FPASTE                                         GC OFF                   FD SEL (FDS)
			MLPASTE                 <Documentation>        GC ON                    LS SEL (LSS)
			                        HELP                   GC                       LS REL (LSR)
			<'ans' History>         HHELP                                           LS FZF (LSZ)
			NEXT                    SHORTCUTS              <Unimportant>            LS QUE (LSQ)
			PREV                                           NUM COM                  RANGER (RNG)
			PREV ON                 <Startup Files>        PROF DEEP
			PREV OFF                RPRC                   CDH CLEAN
			PREV CLEAR              VIMRC                  ALS
			PREV ALL                TMUXRC                 ALSD
			                        XONSHRC                ALSF
			                        RYAN RPRC
			                        RYAN VIMRC
			                        RYAN TMUXRC
			                        RYAN XONSHRC

	// NOTE: When a command here is listed like:
	//    SOME COMMAND (SMCMD)
	// It means SMCMD is an alias for SOME COMMAND, and is therefore a shorthand equivalent.
	//Also note that in SHORTCUTS, many of these command might have additional shorthands. They're listed here as well.

	// Any of these commands can also be typed in lower-case without spaces, for shorthand


	<Input Modifier>
		// In pseudo-terminal, modifiers are preprocessors for your code.
		// You can turn them on or off, or specify your own macro where | is the replacement
		MODIFIER ON  : Enables modifiers
		MODIFIER OFF : Disables any modifier
		MODIFIER SET : See https://asciinema.org/a/mb52gHyuFH92SXf32H6cuE4XR
		SMODIFIER SET: See https://asciinema.org/a/7SVhDzt4yho4hggja9Muh5ffV

	<Stack Traces>
		MORE  : Shows you a bigger stack trace. Always works.
			Shortcut: m
		MMORE : Shows you a more detailed stack trace with the values of every variable at every stack frame,
			along with big chunks of code, but requires an external library. It's extremely useful for debugging.
			Shortcut: mm
		DMORE : Lauches a post-mortem debugger on the last error. If you have pudb, it will launch that debugger
			instead of the defaut pdb library. It's useful when you want to get information that MMORE can't tell you.
			Shortcut: dm
		GMORE : Googles for your error in your default web browser
			Shortcut: gm
		AMORE : Stands for 'ans more'. Will set 'ans' to the latest error's exception, so you can perform custom tests on it.
			Shortcut: am
		HMORE : Almost exactly like MORE, except with syntax Highlighting
			Shortcut: hm
		VIMORE: Stands for 'vim more'. Used to edit the files you see in your stack trace with vim.
			Shortcut: vm
		PIPMORE: If you get an import error becuase a package isn't installed, simply use 'PIPMORE' to auto-install it
			Shortcut: pm
		IMPMORE: If you get an error like "NameError: name 'numpy' is not defined", this will automatically import numpy
			Shortcut: im
		PREVMORE: Goes to the previous error. It's kind of like the PREV command, but for errors.
			Shortcut: um
		NEXTMORE: The opposite of PREVMORE. It's kind of like the NEXT command, but for errors.
			Shortcut: nm

	<Command History>
		HISTORY : Prints a list of all commands that you've entered that didn't cause errors. All green commands were single-liners,
			and all yellow commands were multi-liners. Yellow commands alternate between bold and not-bold so you can visually distinguish
			one multiline command from the next.
			Shortcuts: hi, hist
		GHISTORY: Prints a list of all single-line commands that didn't have errors. GHISTORY stands for 'green history', because in HISTORY all
			single-liners are printed in green.
			Shortcuts: gh, ghi, ghist
		AHISTORY:
			Sets ans to str(HISTORY)
			Shortcuts: ah, ahi, ahist
		CHISTORY: Stands for 'Copy History'. Copies the output of HISTORY to your clipboard.
			Shortcuts: ch, chi, chist
		DHISTORY: Stands for 'def History'. Extracts all function definitions from HISTORY and shows one of each to you 
			(it's easier than sifting through HISTORY manually to pull your functions out)
			Shortcuts: dh, dhi, dhist
		VHISTORY: Every time you close RP, your HISTORY is saved to a file. VHISTORY opens up that file in VIM. You can use it to select code and paste it back into RP.
			Shortcuts: vh, vhi, vhist
		ALLHISTORY: Shows all commands you entered, including the ones that caused errors. In a terminal, you can also press F3 to get a similar result.

	<Clipboard>
		COPY  : Copies str(ans) to your clipboard. If you're using linux, please 'sudo apt install xclip'
			Shortcut: co
		PASTE: Sets ans to the string from your clipboard.
			Shortcut: pa
		EPASTE : Runs code from your clipboard. Stands for 'eval paste'
			Pro tip: Equivalent to PASTE followed by RUNA (aka 'pa ra' using shortcuts)
			Shortcuts: ep, epa
		WCOPY : Attempts to serialize ans into a bytestring, then sends it to be copied online. It's counterpart is WPASTE.
			Shortcuts: wc, wco
		WPASTE: Pastes from a world-wide clipboard that's hosted on the internet. Any instance of rp that uses WCOPY can copy to this clipboard, letting
			you copy and paste between computers easily. It supports many datatypes including numpy arrays, tensorflow tensors, lists, integers, floats and even lambdas and python
			functions (including builtins) - as well as many other datatypes. Anything that the 'dill'
			library supports is supported by WCOPY and WPASTE. The motivation behind this: Before, when writing code on things like the raspberry pi, it was annoying to bring code back 
			and fourth from my computer to the raspi. I had to use something 
			like email, etc, which meant leaving the terminal and using a GUI. But with this, you never even have to leave RP! Whatsmore, you can transfer more than just strings now :) 
			Shortcuts: wp, wpa
		TCOPY: Copies str(ans) to your tmux clipboard. If there is no tmux running, this won't do anything.
			Shortcuts: tc, tco
		TPASTE: Pastes the tmux clipboard as ans. That way, you can copy something in tmux and paste it directly into rp as a string.
			Pro tip: Follow TPASTE by COPY to copy your tmux clipboard to your system's clipboard, to paste tmux output into sublime or something.
			Shortcuts: tp, tpa
		VCOPY: Copies str(ans) into vim's clipboard. The next time you open vim, you can press 'p' to paste that string into vim.
			Shortcuts: vc, vco
		VPASTE: Paste's vim's clipboard contents into ans. Note that you have to yank something in vim, then exit vim, then this will work.
			Pro tip: If this causes an error, run the command 'VCL' then try again. This stands for 'vim clear'. This will clear certain corrupted vim files, letting it work again.
			Shortcuts: vp, vpa
		FCOPY: Will let you select a file (or folder) and copy it over the web. It can be pasted at any computer using FPASTE
			Shortcuts: fc, fco
			$FCA: File-copies ans, assuming ans is a string that is the path to a file or folder
			$FCH: File-copies current directory recursively
		FPASTE: Assumes somebody recently used FCOPY somewhere in the world. It will paste the file (or folder) in your current directory.
			Note: Behind the scenes, it uses WCOPY and WPASTE to do this. Large files, over a gigabyte, probably won't work well.
			Shortcuts: fp, fpa
		MLPASTE: When all else fails and we're in a nuclear apocalypse, this will still let you paste text into RP. Run this, then paste some content. When you're done, sent a KeyboardInterrupt by pressing Ctrl+C (or in Jupyter, by pressing 'stop')
			Shortcut: mlp

	<'ans' History>
		// See https://asciinema.org/a/TFf9OvoRj1vmRqMPYDhHEyDsV
		PREV      : reverts ans to its previous value
			Shortcut: pp
		NEXT      : The opposite of PREV. Undo is to PREV as redo is to NEXT.
			Shortcut: n
		PREV ON   : Enables tracking ans's history. This is the default.
		PREV OFF  : Disables tracking ans's history. This can save memory.
		PREV CLEAR: Deletes all ans history, which might save some memory. I rarely use it in practice.
		PREV ALL  : An alternative to typing PREV PREV PREV PREV PREV over and over again. This undoes ans as many times as it can.

	<Namespace History>
		//By default, undo-mode is turned off (aka UNDO OFF). This is to save memory.
		UNDO    : Reverts all visible variables to a previous state (TODO: show asciinema demo)
		UNDO ON : When undo-mode is turned on, all variables are recorded each time you enter a command.
		UNDO OFF: Opposite of UNDO ON

	<Prompt Toolkit>
		//TODO: Add video
		PT: Toggles between PT ON and PT OFF
		PT OFF: Disables prompt toolkit. This means using a simpler UI, with less features but also saving battery life.
		PT ON : Enables prompt toolkit, letting you have things like autocompletions and multi-line editing etc.

	<Saving Settings>
		//TODO: Add video
		PT SAVE  : Prompt-Toolkit Save saves all the settings in the menu you get when pressing F2, as well as any title made by SET TITLE.
			Shortcut: pts
		PT RESET : Resets all the options in the F2 menu to their defaults.
		SET TITLE: Lets you assign a title to this RP installation, displaying a tag on the bottom left.
			Shortcut: st
		SET STYLE: Lets you select a different prompt label (which is by default ' >>> ')

	<Shell Commands>
		//TODO: Add video
		! : Like in jupyter notebook, using an exclamation mark before a shell command runs that shell command. For example, '!ls | grep .py' will list all 
			python files in your current directory
		!!: Similar to the above single exclamation mark, having !! instead of ! will capture the standard output of your command to a string in 'ans', 
			instead of printing it to stdout. For example, '!!echo Hello World!' is the same as doing 'ans="Hello World!"'
			Pro tip: If you need to use sudo, or interact with the command somehow, its best use a single exclamation mark. Otherwise, if you want to keep the output, use !!.
		SRUNA : Equivalent to running "!*"  where * is replaced by str(ans). Stands for 'Shell-Run Ans'
			Shortcut: sa
		SSRUNA: Equivalent to running "!!*" where * is replaced by str(ans)
			Shortcut: ssa

	<Simple Timer>
		//TICTOC has nothing to do with TIKTOK - this came first - i promise lmao
		//rp.tic() and rp.toc() are timing functions that work the same way they do in MATLAB
		TICTOC: Toggles between TICTOC ON and TICTOC OFF
			Shortcut: tt
		TICTOC ON: When this is turned on, the time it takes to run each command will be displayed.
			Pro tip: If the command runs super fast, try doing '\fo 100' to edit the command to run 100 times, or alternatively do 'DITTO 100' to run the previosuly-run command 100 times
		TICTOC OFF: Turns that mode back off again.

	<Profiler>
		//TODO: Add video
		PROF: Toggles PROF ON with PROF OFF. Quick and dirty. What I almost always end up using lol.
			Shortcut: po
		PROF ON: Will turn on the profiler for your next commands, telling you which function takes how long to run in a tree diagram next time you run a python command.
		PROF OFF: Turns the profiler off.

	<Toggle Colors>
		FANSI ON: Enables terminal-based text coloring features of rp
			Shortcut: fon
		FANSI OFF: Disables terminal-based text coloring features of rp
			Pro tip: This can be less laggy, especially on Windows terminals
			Shortcuts: fof, foff
		// This enables/disables rp.fansi() and rp.fansi_print()

	<Module Reloading>
		RELOAD ON: Will automatically reload modules that have changed since the previous prompt
		RELOAD OFF: Disables that

	<Documentation>
		HELP: Lists commands
			Shortcut: h
		HHELP: Shows you this document
			Shortcut: hh
		SHORTCUTS: Shows you useful aliases
			// Ones with a + at the end of the line are defined elsewhere in this help document, in some line starting with a $ sign
			CLS aka CLEAR: Clears all terminal output. Equivalent to !clear
			RS aka RESET: resets the current tty. Equivalent to !reset
			RNA            +
			RMA            +
			CPAH aka CAH: (copy ans here) Copies the file specified by ans to the current directory (or if ans is a list of paths, copies all of them here)
			MVAH MAH       +
			FCA FCH        +
			GCLP: git-clones url from clipboard (git-clone paste)
			GCLA: git-clones ans
			GURL: github url (gets url of current repo)
			LN aka LNAH: Creates a symlink from the path specified by ans to here
			SG LG OG: save-gist, load-gist, old-gists (saves or loads a gist from ans, and old-gists shows old saved gists)
			SUH COH: sublime-here, code-here (opens sublime at . or vscode at .)
			SUA COA: sublime-ans, code-ans (opens sublime to edit the module or path specified by ans, or does that with vscode)
			IASM: import all sub-modules of ans (assuming ans is a module)
			DAPI: display all pypi packages' info
			LSM            +
			RF RD RE: Random-file, random-directory, random-element
			GP: equivalent to get_parent_directory(ans)
			NBC NBCA NBCH: notebook-clear (clears the outputs of a selected notebook), notebook-clear-ans (clears the notebook outputs of the notebook file speficied by ans), notebook-clear here (clears all ipynb outputs in current dir)
			NB: Takes a .ipynb file and returns python code that can be used in rp with the ^w key to execute individual cells
			Z BA S: zsh, bash, sh
			GOO: Googles str(ans)

	<Startup Files>
		RPRC: Edits your .rprc file. This file runs every time rp is launched via 'python3 -m rp'

	<Inspection>
		// All of these commands can be used like this:
		//     >>> some_object?
		// where some_object is the 'target'
		// Or like this:
		//     >>> ?
		// ...which is simply turned into:
		//     >>> ans?
		// where 'ans' is now the 'target'

		//Note that there is a microcompletion that will let you press '/' instead of '?' for most of these.

		//TODO: Add a video to this help section

		? : Just entering '?' by itself is equivalent to writing 'ans?'. 'some_value?' will give you more information about that value. 
			In ENTRIES, green items are callables (like functions and classes). Blue items are modules, and others are just plain colored.
			Some special cases:
				- If given a file or folder name, it will display information about it such as file size, number of files, etc
					- If given the path of a text file, will show the number of lines
					- If given an image file, will show it's resolution 
					- If given a video file, will show its duration
					- If given a symlink, will show its destination
				- If given a numpy array or torch tensor etc, will show its shape and dtype
				- If given a module, will show its source code path
				- If given a function, will show its arguments
				- If given something with length, will show it's len()
		??: Same as ?, but will also show the source code of the inspected object.
		???: Same as ?, but will also show details about every value in ENTRIES.
		?p: Will attempt to display the target in the terminal. Normally it will pretty-print it. Dicts, nested lists etc will be displayed nicely. Great for web api repsonses that looks like {{asd::f{}:::{asdf}a::sdf}}}asdf{}{a::sdf}{{asdf{}::{}{}{}}} etc
			Some special cases:
				- If target is an image (as defined by rp.is_image), it will be displayed in the terminal in full color (if your terminal supports true-color, which most do). When in Jupyter notebook, it will display an image in HTML instead of via text as it would in a terminal.
				- If the target is a string containing python code, it will print it with syntax highlighting
				- If the target is a valid url, it will try to display that webpage crudely in the terminal (you can view google search results etc with it)
		?h: Just entering '?/'' by itself is equivalent to writing 'help(ans)'. A command like 'some_expression?/' is turned into 'help(some_expression)'
		?/: Equivalent to ?h. Can be typed by pressing '/' twice.
		?.: Lets you search for attributes recursively, interactively. It uses fzf.
			You can also do "?.fourier" to search *non-interactively* for the query "fourier". Good for when you aren't running this in a terminal, or you want to record the output. Press control+c to cancel it prematurely.
			You can also do "?.1" or "?.2" to search interactively with a maximum recursion depth of 1 or 2 respectively (or 3, or 4 etc - whatever floats your boat)
		?v: Will attempt to edit the source code of the target in vim. Will position the cursor nicely for you in that file too.
		?s: Will print str(target).
		?t: Will let you interactively view a large numerical matrix or pandas table in a terminal. Equivalent to the TAB command.
		?e: Will display information about each attribute of the target. If there are functions with no arguments, it evaluates them (such as __len__ etc). It uses the 'peepdis' library to do this (its on pypi).
		?c: Gets source code. Will set ans to the source code of the target. Equivalent to "ans=rp.get_source_code(target)"
		?i: Will show pip information about a given module. Assumes the target is a module obtained from pip.
		?r: Will show nicely formatted colorful information about the target using the 'rich' library.
		?j: Will interactively display JSON-like structures, with collapsible dicts inside of lists inside of dicts etc. Works with other datatypes too, such as the OrderedDicts used in pytorch .pth files.

	<Others>
		RETURN: Exit the rp session, and return ans as the return value.
			Shortcut: ret, control+d
		SUSPEND: Suspends this python process. Usually ctrl+z does this, but in rp, ctrl+z means undo.
			Shortcut: sus
		CLEAR: Will clear the terminal screen. When in Jupyter lab or notebook and running rp.pterm(), it will clear the cell.
			Shortcut: cls
		WARN: Toggles all python warnings
		GPU: Shows GPU usage info
		TOP: Shows bpytop
		MONITOR: An alternative to TOP
			Shortcut: mon
		TAB: Asks you to select a csv file to be interactively viewed
		TABA: Lets you interactively view ans, where ans is either:
			- a file path to a csv or tsv file
			- a 2d numpy array
			- a pandas table
			- (other things might work too, try them out)
		UPDATE: Updates rp
			Shortcut: up
		ANS PRINT ON: enables printing str(ans) when it changes
			Shortcut: apon
		ANS PRINT OFF: disables that
			Pro tip: Use this when chaning ans spams the terminal (maybe ans is a long string or something)
			Shortcut: apof
		ANS PRINT FAST: enables printing str(ans) when it changes, but won't always get the color right (yellow vs green for changes vs unchanged).
			Pro tip: Use this if you still want to read the value of ans, but it's slow because it's a big tensor or something
			Shortcut: apfa
		SHELL: Launches xonsh. The directory you navigate to in xonsh will also change rp's current working directory after exiting xonsh.
			Shortcut: sh
		LEVEL: Displays information about your computer, runtime, python version, etc. The 'LEVEL' is how deeply your rp session is nested (when you call pseudo_terminal() inside a pseudo_terminal(), the LEVEL increases)
			Shortcut: l
		DITTO: Repeat the previous command
			Pro tip: 'DITTO 10' will repeat the previous command 10 times. Or any other number...
		EDIT: Use vim to enter a command, that will then be run.
		VARS: Return a set of all variable names created in this session
			Shortcut: vs
		RANT: Run-as-new-thread the stuff that comes after RANT.
			For example, 'RANT sleep(5);print("HELLO")' will print "HELLO" after 5 seconds.
		FORK: Will enter a forked process of this session. Good for experimenting with things you're not sure you'll break or not.
		WANS: Write-ans. Will write ans as a file. It will prompt you for the file name you want to use.
			Special cases:
				- If ans is a string, it will write a text file
				- If ans is an image, it will write an image
				- If ans is bytes, it will write a binary file
			Shortcut: wa
		ARG: Displays the current arguments given to this python process.
			Pro tip: 'ARG -a -b --thing stuff' is equivalent to sys.args[1:]='-a -b --thing stuff'.split()
		VIM: Selects a file with vim then opens it
			Pro tip: 'VIM ~/.vimrc' edits ~/.vimrc with vim
			Shortcut: vv
		VIMH: Equivalent to "!vim ."
			Shortcut: vih
		VIMA: Equivalent to ?v. Edits ans with vim, where ans is:
			- A file-path string
			- A module or function
			Shortcut: va
		AVIMA: Opens up vim with str(ans). Lets you modify it, then returns the result as ans.
			Shortcut: av, ava
		GC: Toggles between GC ON and GC OFF
		GC ON: Will run gc.collect() after every command
		GC OFF: Disables GC ON
	
	<Unimportant>  
		NUM COM: Lists all of these commands
		PROF DEEP: Like PROF ON, but shows more details.
		CDH CLEAN: Removes all red entries from CDH.
			Shortcut: cdc
		ALS: Returns the contents of LS as ans. 
			Shortcut: lsa
		ALSD: Returns the contents of LS as ans, but only dirs.
			Shortcut: lsad
		ALSFReturns the contents of LS as ans, but only files.
			Shortcut: lsaf


	<File System>
		RM: Removes a file that you select.
		$RMA : Removes ans. If ans is a file or folder, it will remove it. If ans is a list of files or folders, it will remove all of them.
		RN: Renames a file you select to a name you input
		$RNA: Renames the path specified by ans to a name you input
		MV: Moves a file you select into a destination you select
		$MVAH: Moves ans here. Moves the path specified by ans to the current directory.
		LS: Prints all files and directories
		LST: Prints all files and directories with timestamps and filesizes, sorted by time modified
		CD: Cd's into a directory you select, and adds it to sys.path so you can easily import python modules from it
			Pro tip: 'CD some/folder/path' will cd into that folder path
			Pro tip: Typing 'cd thing' will be microcompleted into 'CD thing'
		CDP: Cd's into the directory from your clipboard (cd paste)
		CDA: Cd's into ans, where ans is:
			- A directory string
			- A file string (it will cd into it's parent directory)
			- A module (will cd into the module's source code directory)
			- A function (will cd into the function's module's source code directory)
		CDB: Cd's back to the previous directory you visited
			Pro tip: You can use this as soon as you boot rp to go back to the directory of the previous session, to pick up where you left off
			Shortcut: b
		CDU: Cd's up. Equivalent to 'CD ..'
			Shortcut: u
		CDH: Cd history - keeps track of every directory rp's visited, and lets you select one of them to cd into.
			Pro tip: There are 3 colors for folders: yellow means it exists. Bold yellow means it's in sys.path, and red means it no longer exists
			Pro tip: Use CDH CLEAN to remove all red entries - good for when you've deleted folders
			Shortcut: hd
		CDZ: Cd's into a user-selected folder found via fuzzy-searching for it (cd fuzzy)
		CDQ: Cd's into a user-selected folder found via query-searching for it (cd query)
		CAT: Prints the contents of a file you select. If it's a python file, the contents will be syntax-highlighted.
			Pro tip: 'CAT filename.txt' will print the contents of filename.txt
		NCAT: (number-cat) Like CAT, but has line numbers
		CCAT: (copy-cat) Like CAT, but copies the contents of the file to your clipboard instead of printing them
		ACAT: (ans-cat) Like CAT, but copies the contents of the file to ans of printing them
			Special cases:
				- If the specified file is a text file, it will load the text as a string
				- If the specified file is an image file, it will load the image into a numpy array
				- If the specified file is a video, it will attempt to load the video into a numpy array
				- If the specified file is a sound file, it will load the audio into a numpy array
				- If the specified file is a .pt or .pth file, it will load the pytorch file into CPU using torch.load
				- If the specified file is a .npy, it will load the numpy array using np.load
				- If none of the above cases are met, it will simply load the file as raw bytes
			Shortcut: ac
		CATA: (cat ans) Like CAT, but instead of selecting a file, it cat's the file specified by ans (assumes ans is a file-name string)
			Shortcut: ca
		NCATA: Like CATA, except has line-numbers
		CCATA: Like CATA and CCAT combined (copies the contents of a file specified by ans into your clipboard)
		ACATA: Like CATA and ACAT combined (loads the contents of a file specified by ans into ans)
			Shortcut: aa, aca
		RUN: Runs a selected python file, as if it were copy-pasted into the console
			Pro-tip: 'RUN file.py' will run file.py
			Shortcut: ru
		RUNA: (run ans) Will run the contents of ans if ans is valid python code, or run the contents of a file if ans is a string pointing to a python file
			Shortcut: ra
		PWD: Shows the current working directory
			Shortcut: pw
		CPWD: Copies the current working directory to your clipboard
		APWD: Copies the current working directory to ans
			Shortcut: ap
		TAKE: Like the 'take' command in zsh; it will make a directory then cd into it.
			Shortcut: tk
		MKDIR: Makes a directory specified by the user
			Shortcut: mk
		OPEN: Opens a selected file or directory with the default application
			Shortcut: op
		OPENH: Open-here. Equivalent to 'OPEN .'
			Shortcut: oh
		OPENA: Open-ans. Opens the file or directory specified by ans with the defualt application.
			Shortcut: oa
		DISK: Displays a breakdown of the current directory's disk usage.
			Shortcut: dk
		DISKH: Displays a histogram of filetypes and how much storage they take recursively from the current directory.
			Shortcut: kh
		TREE: Displays a tree of files, and displays some information about each file and directory.
			Shortcut: tr
		TREE ALL: Like TREE, except it doesn't skip hidden files
			Shortcut: tra
		TREE DIR: Like TREE, except it only shows directories
			Shortcut: trd
		TREE ALL DIR: Like TREE ALL and TREE DIR combined
			Shortcut: trad
		FD: Recursively searches for a string to be contained in a file or folder name
		FDA: Like FD, but returns the result as a list in ans
		FDT: Interactively fuzzy-search for lines of text recursively in the current directory. Like recursive grep, but interactive...
		LS SEL (LSS): Select a file or folder path, and set ans to its absolute path.
		LS REL (LSR): Like LSS, except it does relative paths
		LS FZF (LSZ): Like LSS, except uses a fuzzy search recursively across directories
		LS QUE (LSQ): Like LSS, except uses a query search recursively across directories
		$LSM: Like LSS, but lets you select multiple files by pressing the tab key interactively in query search mode
		RANGER (RNG): Launches 'ranger', a python-based file manager. When you navigate in range, it will change rp's current working directory - you can use this to navigate quickly around a computer inside rp.













	?c  gets source code
	?p  prints either with pretty_print, or prints a python code string with syntax highlighting
	TOP vs MON: MON is simple, and always colored properly. TOP is not always colored properly depending on the terminal, but when it is it's very pretty. 
	?.  ans?.query   or   ans?.2  for fzf seach 2 layers deep+selection
	CDA will cd into a module's directory if ans is a module; into the source file's folder for an object (if possible, in same way that ?v works), or into the parent folder if ans is a path to a file
	CAT will work on URL's too, kind of like curl.
	CAT will syntax-highlight any python files
	ACAT also works on images, videos, and sounds - as well as any text file or url
	AVIMA will highlight a string using python syntax highlighting, if the string is valid python syntax
	OPENA will open a folder, file OR url in your web browser!
	LEVEL will print out the current pseudo_terminal level, as well as the current python version and computer name. Useful when running RP on multiple computers and you need to kno who's who.
CAT via LSS ACATA ?p










USING IN BLENDER (Or any other closed environment that has pip):
	#Copy-paste the following four lines into a blender console, and it will install rp
	import sys,subprocess
	subprocess.run(['sudo',sys.executable, "-m","pip","install",'rp','--upgrade'])
	from rp import pseudo_terminal
	pseudo_terminal()



#FZF Notes:
	Many functions in RP use FZF, a program that lets you search through things really fast in a terminal. Here's some useful info about it: 
	When in 'query' (as opposed to 'fuzzy') mode, you can *almost* do everything you can do in fuzzy mode by inserting spaces between every character
	The following searches for everything that contains 'jedi' but not 'rp.libs.jedi'
		jedi !rp.libs.jedi
	The following searches for every line containing 'from jedi'
		from\ jedi
	The following searches for every line containing both 'from' and 'import'
		from import
	The following is equivalent to the above because order doesnt matter:
		import from
	The following is equivalent to the above because it appears to only care about sets:
		import from import from import from from from import import import
	The following searches for a line starting with the letter H and ending with #
		^H $#
	The following searches for a line starting with the letter H and NOT ending with #
		^H !$#







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


#TODO: When x makes sense, y will happen when it makes sense (general ideas. )


When it makes sense, - will be turned into _.
	Examples:
		def f(-,) --> def f(_,)
                -=6  -->  _=6
		if -    if _



Here are some commands in the frequency that I've used them over the years:
(Here's the code used to make this list:  https://gist.github.com/SqrtRyan/b73080cf1e06c8dd2907d1143f77d66e)

			LS
			B
			U
			HD
			TR
			OH

			LSS
			CDA
			AA

			AV
			CO PA
			WC WP
			LC LP
			VC VP
			TC TP

			Z

			HI
			AH


			MM

			PP
			RET

			H

			?

LS 3147
PP 1091
B 1083
RET 925
U 922
? 719
HD 619
CDH 612
PASTE 560
AV 517
Z 503
MM 327
WC 321
PREV 316
ANS 301
MMORE 291
H 271
TR 258
CDA 240
RETURN 236
LP 236
VIMRC 230
LSS 230
PA 223
AA 214
PWD 212
CO 212
L 201
HISTORY 194
M 191
KH 181
PW 171
V 170
DK 166
LSA 162
HI 160
TP 160
TRD 153
VIH 153
FDQ 147
RM 145
APFA 141
WA 136
RF 136
VA 132
TOP 128
VP 127
OH 121
WP 113
FDT 112
VH 109
LC 108
S 107
LST 107
SC 103
N 102
DH 102
VM 102
COPY 96
HE 93
WCOPY 92
RA 88
PM 86
CPWD 85
OA 85
HELP 83
IASM 81
VV 78
CDU 78
LSR 78
MORE 77
RNG 72
LSQ 72
AC 69
NVT 69
DM 68
FP 66
AVIMA 65
CD 63
NEXT 61
GM 61
RMA 61
TK 59
TT 57
TAB 56
MK 56
IM 55
PO 54
LPASTE 54
LSZ 54
UP 54
RN 54
AP 53
ACATA 52
HM 51
UM 51
CDQ 51
TREE 50
MLP 49
LN 48
RS 48
TABA 48
PT 48
NB 48
VC 48
CH 47
AM 45
DISK 44
VIM 43
GPU 43
APOF 43
ACAT 43
AH 42
HH 42
SH 40
?. 39
CHI 39
CHIST 38
OG 38
P 37
UPDATE 36
VIMA 36
FD 36
DMORE 35
VS 35
RU 35
MVAH 35
TICTOC 34
?? 34
SG 34
RPRC 33
RV 33
CA 33
CAT 32
FC 32
LSM 32
WPASTE 31
CLS 30
DHIST 30
HIST 30
RUNA 30
FDA 30
OP 28
TMUXRC 28
TC 28
TPASTE 27
GOO 27
RUN 26
CDZ 26
CDC 26
CPAH 26
SA 25
LSAD 25
HHELP 24
VIMORE 24
RE 24
??? 23
VARS 23
CDB 23
MV 23
GCLA 23
GURL 22
RNA 22
CATA 22
APON 22
NN 22
NBC 22
LNAH 22
LSAF 21
CHISTORY 20
PROF 20
FDZ 20
NM 18
GC 17
DCI 17
LCOPY 16
?/ 15
OPEN 15
GHISTORY 14
CDP 14
HMORE 14
ACA 14
VCL 14
DAPI 14
ST 13
TCOPY 13
CCATA 13
MON 13
HC 12
MONITOR 12
SMI 12
ALS 12
LSF 12
FDS 12
FCA 11
LG 11
CLEAR 11
VHI 11
DITTO 10
GH 10
ARG 10
AMORE 10
GMORE 10
APWD 10
DHI 10
DA 10
VI 10
AW 10
ISA 10
RD 10
EDIT 9
SHELL 9
FORK 9
WANS 9
PREVMORE 9
LGA 8
TAKE 8
INS 8
WD 8
MAH 8
SRA 8
COH 8
UNDO 7
LEVEL 7
AHIST 7
SHORTCUTS 7
GHI 7
AHI 7
VCO 7
TA 7
GP 7
RT 7
CAA 7
DKH 7
WR 7
GCLP 7
SUSPEND 6
AHISTORY 6
NCATA 6
PF 6
DD 6
VIMH 6
SUS 6
ZSH 6
NBA 6
IMS 6
LSAG 6
DR 6
NBCH 6
PRINT 5
FANSI 5
WCO 5
PD 5
TRAD 5
ISM 5
BA 5
AFD 5
WGA 5
RANT 4
NCAT 4
CCAT 4
GHIST 4
LV 4
CAH 4
MPH 4
LPA 3
XONSHRC 3
TCO 3
LVL 3
WARN 3
RESET 2
DIR 2
SS 2
FCH 2
SUH 2
DO 2
ALL 2
SET 2
DISC 2
OPH 2
FOF 2
FON 2
OPA 2
ON 2
ALLHIST 2
RPA 2
EP 2
NEXTMORE 2
IMA 2
ALSF 2
ALSD 2
DT 2
CPH 2
NCA 2
MA 2
WN 2
RST 2
GOOP 2
DHISTORY 1
PIPMORE 1
PTS 1
WPA 1
FZF 1
OPENH 1
VHE 1
MKDIR 1
EPA 1
IMPMORE 1
CCL 1
SSA 1
REL 1
EA 1
RG 1
MVPH 1
FZM 1
CPPH 1
TRA 1
NBCA 1
SSRA 1
