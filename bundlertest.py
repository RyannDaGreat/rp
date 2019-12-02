#TODO Fix that import ABC doesn't go to import Janky.ABC as ABC and instead goes to import Janky.ABC
#Will be used to systematically bundle other dependencies into RP so that it never ever breaks.....hopefully....
#TODO: We need a dependency graph....
def with_redirected_imports(code,prefix='rp.',module_names='prompt_toolkit'.split()):
    import re
    ans=code
    for _ in range(20):#Very overkill but its ok
        ans=re.sub(r'^(\s*import\s.*\,\s*)(%s)([^\w]|$)'%'|'.join(module_names),r'\1'+prefix+r'\2\3',ans,flags=re.MULTILINE)
    ans    =re.sub(r'^(\s*from\s+)(%s)([^\w]|$)'        %'|'.join(module_names),r'\1'+prefix+r'\2\3',ans,flags=re.MULTILINE)
    ans    =re.sub(r'^(\s*import\s+)(%s)([^\w]|$)'      %'|'.join(module_names),r'\1'+prefix+r'\2\3',ans,flags=re.MULTILINE)
    return ans
projectdir='Jenkins'
ans=make_directory(projectdir)
module_names=[]
def handle_module(module_name):
    import importlib as i
    m=i.import_module(module_name)
    module_names.append(module_name)
    module_folder=get_path_parent(m.__file__)
    if get_path_name(module_folder)!='site-packages':
        copy_directory(module_folder,projectdir)
    else:
        copy_file(m.__file__,projectdir)
def rewire():
    python_file_paths=get_file_paths(projectdir,recursive=True,file_extension_filter='py')
    for file_path in python_file_paths:  
        try:
            code=text_file_to_string(file_path)
            new_code=with_redirected_imports(code,projectdir+'.',module_names)
            if new_code!=code:
                fansi_print('CHANGED '+file_path,'blue')
            string_to_text_file(file_path,new_code)
            print('rewired '+file_path)
        except Exception as e:
            print_stack_trace(e)
    
rewire()
handle_module('six')
handle_module('pygments')
handle_module('prompt_toolkit')
handle_module('jupyter')
handle_module('IPython')
rewire()
