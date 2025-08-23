from rp import *


#This code is all sloppy; written in a few hours. Didn't debug. But it seems to work well...soo...its good 'nuff for me.
def get_name(metadata):
    if file_exists(metadata):
        metadata=text_file_to_string(metadata)
    lines=line_split(metadata)
    lines=[x for x in lines if x.startswith('Name:')]
    return lines
def get_site_packages_directory():
    import sysconfig
    out= sysconfig.get_paths()["purelib"]
    if folder_exists(out):
        return out
    # if not folder_exists(out):
    #     for _ in sys.path:
    #         if get_file_name(_)=='site-packages':
    #             return _
    import rp
    return get_parent_directory(get_parent_directory(get_module_path(rp)))#Should look like /home/ryan/.local/lib/python3.8/site-packages/rp/__init__.py then /home/ryan/.local/lib/python3.8/site-packages
                
def process(dist_info):
    assert folder_exists(dist_info)
    files=get_all_paths(dist_info,include_files=True,include_folders=False)
    file_names=[get_file_name(file) for file in files]
    assert 'METADATA' in file_names
    assert 'top_level.txt' in file_names
    modules=get_modules(dist_info)
    name=get_pypi_name(dist_info)
    info=get_pypi_info(dist_info)
    return info,modules
def get_pypi_name(dist_info_path):
    metadata=path_join(dist_info_path,'METADATA')
    if file_exists(metadata):
        metadata=text_file_to_string(metadata)
    else:
        raise FileNotFoundError(metadata)
    lines=line_split(metadata)
    lines=[x for x in lines if x.startswith('Name:')]
    assert len(lines)==1
    line=lines[0]
    name=line[len('Name:'):].strip()
    return name
def get_modules(dist_info_path):
    top_level_file = path_join(dist_info_path,'top_level.txt')
    
    if file_exists(top_level_file):
        # Standard case: read from top_level.txt
        top_level = text_file_to_string(top_level_file)
        top_level = line_split(top_level)
        return [m.strip() for m in top_level if m.strip()]
    else:
        # Fallback: infer module name from dist-info directory name
        # e.g., "numpy-1.26.4.dist-info" -> "numpy"
        dir_name = get_file_name(dist_info_path)  # Gets just the directory name
        if dir_name.endswith('.dist-info'):
            package_name = dir_name[:-len('.dist-info')]  # Remove .dist-info
            # Remove version info (everything after first hyphen)
            module_name = package_name.split('-')[0]
            return [module_name]
        return []
def get_dist_info_paths():        
    infos=[x for x in get_subdirectories(get_site_packages_directory()) if x.endswith('.dist-info')]
    return infos
def get_dist_infos():
    output=[]
    for path in get_dist_info_paths():
        try:
            processed=process(path)
            # fansi_print(processed[0],'cyan')
            output.append(processed)
        except Exception:
            pass
    out={}
    for o in output:
        for module in o[1]:
            out[module]=o[0]
    return out

def get_pypi_info(dist_info_path):

    output={}
    output['dist-info']=dist_info_path


    try:
        #EXAMPLE METADATA:
        #     Version: 1.7.0
        #     Name: torch
        #     Home-page: https://pytorch.org/
        #     Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
        #     Keywords: pytorch machine learning
        #     Requires-Python: >=3.6.1
        #     Author-email: packages@pytorch.org
        #     Requires-Dist: future
        #     Requires-Dist: numpy
        #     Requires-Dist: dataclasses
        metadata=path_join(dist_info_path,'METADATA')
        if file_exists(metadata):
            metadata=text_file_to_string(metadata)
        else:
            raise FileNotFoundError(metadata)
        lines=line_split(metadata)
        def get_field(prefix):
            return [x[len(prefix):].strip() for x in lines if x.startswith(prefix)]
        for prefix in 'Name Version Home-page Summary Keywords Requires-Python Author-email Requires-Dist'.split():
            fields=get_field(prefix+':')
            if len(fields)==0:
                continue
            if len(fields)==1:
                output[prefix]=fields[0]
            else:
                output[prefix]=fields
        
        if 'Requires-Dist' in output:
            #Turn stuff like  "prompt-toolkit ; extra == 'ptk'", into "prompt-toolkit"
            if isinstance(output['Requires-Dist'],list):
                output['Requires-Dist']=sorted(set([x.split()[0] for x in output['Requires-Dist']]))
            elif isinstance(output['Requires-Dist'],str):
                output['Requires-Dist']=[output['Requires-Dist'].split()[0]]#i changed my mind keep it as a list

        for from_name,to_name in [('Requires-Dist','Dependencies'),('Home-page','Homepage'),('Author-email',"Author Email"),('Requires-Python','Requires Python')]:
            if from_name in output:
                output[to_name]=output[from_name]
                del output[from_name]
            
    except Exception as e:
      #if 'cv' in output['Package Name']:
        print_verbose_stack_trace(e)
    

    try:
        entry_points=path_join(dist_info_path,'entry_points.txt')
        #entry_points=text_file_to_string(entry_points)
        #entry_points=entry_points.splitlines()
        #entry_points=[x.strip() for x in entry_points]
        #entry_points=[x for x in entry_points if x]
        scripts=get_console_scripts(entry_points)
        #if len(scripts)==1:
            #scripts=scripts[0]
            #output['Console Script']=scripts
        if scripts:
            output['Console Scripts']=scripts
    except Exception:pass

    try:
        output['Modules']=get_modules(dist_info_path)
    except Exception:pass
    return output
def get_console_scripts(entry_points):
    if path_exists(entry_points):
        entry_points=text_file_to_string(entry_points)
    entry_points=line_split(entry_points)
    output=[]
    flag=False
    for line in entry_points:
        line=line.strip()
        if line=='[console_scripts]':
            flag=True
            continue
        elif line.startswith('[') and line.endswith(']'):
            break
        if flag:
            if line:
                output.append(line)
    output=[x.split('=')[0].strip() for x in output]#Turn ['yapf = yapf:run_main'] into ['yapf']
    output=set(output)
    output=sorted(output)
    
    #ic(output)
    return output

def get_pypi_info_from_module(module):
    assert is_a_module(module)
    name=module.__name__
    name=name.split('.')[0]#rp.prompt_toolkit --> rp
    info=get_dist_infos()
    if name in info:
        return info[name]
    return None

def display_module_pypi_info(object,info=None):
    #assert is_a_module(module)
    #module_name=module.__name__
    module_name=get_module_name_from_object(object)
    fansi_print('PyPI package info for module '+module_name+':','blue','bold')
    info=info or get_pypi_info_from_module_name(module_name)
    indent='    '
    if info is None:
        fansi_print('Failed to find any package information for '+module_name+'. Maybe it didnt come from PyPI?','red','bold')
    else:
        for field in sorted(info):
            fansi_print(indent+field+': ','green','bold',new_line=False)
            data=info[field]
            if isinstance(data,list) and len(data)==1:
                data=data[0]
            if isinstance(data,list) and not data:
                continue
            if isinstance(data,str):
                print(data)
            else:
                print()
                print(indentify(line_join(data),indent=2*indent))

def display_all_pypi_info():
    iinfo=get_dist_infos()
    for name in sorted(iinfo):
        info=get_pypi_info_from_module_name(name,iinfo)
        display_module_pypi_info(name,info)
        print()

        
def get_module_from_object(o):
    if isinstance(o,str):
        pass

def get_module_name_from_object(o):
    if isinstance(o,str):
        return o
    if is_a_module(o):
        return o.__name__
    import inspect
    module=inspect.getmodule(o)
    if module is None:
        module=inspect.getmodule(type(o))
    # if is_a_module(module):
        # return module.__name__
    try:
        return module.__name__
    except Exception:
        pass
    raise TypeError('Failed to get the module name for the given object')

def _find_dist_info_for_module(module_name):
    """Find the specific dist-info directory for a module without scanning all packages"""
    name = module_name.split('.')[0]  # rp.prompt_toolkit --> rp
    site_packages = get_site_packages_directory()
    
    # Common patterns for dist-info naming
    possible_patterns = [
        f"{name}-*.dist-info",
        f"{name.replace('_', '-')}-*.dist-info", 
        f"{name.replace('-', '_')}-*.dist-info",
        f"{name.upper()}-*.dist-info",
        f"{name.lower()}-*.dist-info"
    ]
    
    import glob
    import os
    
    for pattern in possible_patterns:
        pattern_path = os.path.join(site_packages, pattern)
        matches = glob.glob(pattern_path)
        if matches:
            # Found a match - check if this dist-info contains our module
            for match in matches:
                try:
                    modules = get_modules(match)
                    if name in modules:
                        return match
                except Exception:
                    continue
    return None

def get_pypi_info_from_module_name(module_name, info=None):
    """Get PyPI info for a specific module"""
    if info is not None:
        # If full info dict is provided, use it directly
        name = module_name.split('.')[0]
        return info.get(name)
    
    # Try to find the specific dist-info directory first (much faster)
    dist_info_path = _find_dist_info_for_module(module_name)
    if dist_info_path:
        return get_pypi_info(dist_info_path)
    
    # Fallback to full scan only if direct lookup fails
    name = module_name.split('.')[0]
    info = get_dist_infos()
    return info.get(name)

def get_pypi_module_package_names():
    import rp.libs.pypi_inspection as p
    o=p.get_dist_infos()
    q={}
    for x in o:
        q[x]=o[x]['Name']
    q.update(r.known_pypi_module_package_names)
    q={x:y for x,y in q.items() if x}
    q={x:y for x,y in q.items() if x!=y}
    t={}
    for x in sorted(q):
        t[x]=q[x]
    return t
