#PLANS:
	#Pretty much all future plans are here purely to make it clean, and to increase adoptability...
	#Maybe put this in my apple Notes app later...so as not to clutter the help document lol.
	#Ultimate terminal IDE plans:
	#	Probably won't get around to multi-cursors, realistically. Vim can handle that anyway.
	#	Alt+up that correctly expands and decreases selection region
	#	In editor: Right click items OR some keyboard shortcut for context menus, that include:
	#		Viewing documentation for a function/class etc
	#		Copying it
	#		Renaming it
	#		Extracting selection to a variable
	#		Finding usages (don't know how we would show results yet tho)
	#	Better syntax highlighting: 
	#		Highlight callables differently. We can use JEDI for this.
	#	GUI menus for everything. 
	#	Multiple tabs for the buffer; where we can open files and save files without having to type them out every time.
	#	Sync breakpoints with PUDB in the gutter of the editor. Remember that the buffer is refreshed every time, so this might be difficult...
	#	


##################CSE526 PLANS

	* Keep valid syntax as much as possible. New way to write def:
	* Need to somehow have more memory than just the visible text in order for this to work well...
	* Temporary text created in this way should be highlighted differently (temporary text, that might "solidify" if we move the cursor away)

	*Utilizes concrete syntax trees and differentiable syntax errors

	EXAMPLE (of how things could be done differently)

	On ‹ ›: ‹d¦›   --->   ‹def _¦():
	                           pass›

	Then, On ‹f›:  ‹def _¦():   --->   ‹def f¦():
	                    pass›               pass›

	Or,   On ‹_›:  ‹def _¦():   --->   ‹def _¦():   // This is because, although you can't see it in this document, that _ changed colors. It used to be a temp token, but now it's solidified. All state is still visible in the terminal (by color); this might be accomplished by also having state in the text there (with special unicode syntax + a postprocessor so that you don't see it + special syntax highlighting. Maybe an invisible no-space character before another character changes its color?)
	                    pass›               pass›

	Then, On ‹↵›:  ‹def f¦():   --->   ‹def f():
	                    pass›               ¦
	                                        pass›

	Then, On ‹p›:  ‹def f():   --->   ‹def f():
	                    ¦                  p¦›
	                    pass›               

	Or,   On ‹↵›:  ‹def f():   --->   ‹def f():
	                    ¦                  pass
	                    pass›          ¦›

	ANOTHER EXAMPLE:

	On ‹ ›: ‹if¦›   --->   ‹if ¦:

	#Play around with this to see how we can separate the syntax-error region from the rest of the code
	#For example, while entering some python code keep pressing ^e over and over to see how the syntax errors evolve over time
	#	For example, enter [x for x in y|] then press ^e then type ' if' to get [x for x in y if|] then press ^e again to see how ' if' is reddened
	#This will let us use a concrete syntax tree to analyze python even when there are syntax errors.
	#	For example, this will let alt+up progressively select text more easily.
	#TODO: Pull request changes to PromptToolkit: Mouse events, faster regions, color filters - to have highlightable menus when moused over
	def threeway_split(old_text,new_text):
		#EXAMPLES:
		#     >>> threeway_split('Hello World','Hello Fair World')
		#    ans = ('Hello ', 'Fair ', 'World')
		#     >>> threeway_split('Hello World','HelloWorld')
		#    ans = ('Hello', '', 'World')
		#     >>> threeway_split('Hello World','HelWorld')
		#    ans = ('Hel', '', 'World')
		#     >>> threeway_split('Hello World','Hel oi World')
		prefix=longest_common_prefix(old_text,new_text)
		old_text=old_text[len(prefix):]
		new_text=new_text[len(prefix):]
		suffix=longest_common_suffix(old_text,new_text)
		old_text=old_text[:-len(suffix)]
		new_text=new_text[:-len(suffix)]
		middle=new_text
		return prefix,middle,suffix
	class DifferentialPython:
		def __init__(self):
			self.valid_text=""
		def update(self,new_text):
			if is_valid_python_syntax(new_text):
				self.valid_text=new_text
				print(fansi(new_text,'green'))
			else:
				prefix,middle,suffix=threeway_split(self.valid_text,new_text)
				if is_valid_python_syntax(prefix+suffix):
					self.valid_text=prefix+suffix
					print(fansi(prefix,'green')+fansi(middle,'red','underlined')+fansi(suffix,'green'))
				else:
	d=DifferentialPython()
	SMODIFIER SET d.update(|)



