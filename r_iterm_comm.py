# Getting variables to be shared between modules can be difficult.
# This class exists so that modules from r.py can talk to modules in the rp_ptpython package.
# Essentially, this class is th middle-man. The other modules will both read and write to this module.
# This module is pretty hacky...but that's OK. It doesn't really respect nested pseudoterminals though, so if we were to make multiple async pseudoterminals this module couldn't exist.
globa={}
last_assignable_comm=None
pseudo_terminal_level=0
rp_evaluator=lambda x:None# Returns strings!! UNLESS the second argument is True
current_input_text=""
rp_pt_VARS=""
rp_pt_user_created_var_names=[]
python_input_buffers={}# str ⟶ str
rp_evaluator_mem=None
parenthesized_line=""
try_eval_mem_text=""
ans=None
clipboard_text=""#Should be in sync with pyperclip if its not broken
current_candidates=[]#Is overwritten in completer.py of rp_ptpython, and used in space-completion of callables
enable_space_autocompletions=[]#Make this list non-empty BY MUTATING IT to enable space completions (make bool(enable_space_autocompletions) True
dont_erase_buffer_on_enter=[]#as opposed to [True], which is truthy
completion_style=['good']#should be either ['good'] or ['fast']
debug_height=20#The height of the debugger toolbar
successful_commands=[]
options={
	'top_space':0,
	'min_bot_space':15,
}
