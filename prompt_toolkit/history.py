from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from .document import Document


import datetime
import os

__all__ = (
    'FileHistory',
    'History',
    'InMemoryHistory',
)


class History(with_metaclass(ABCMeta, object)):
    """
    Base ``History`` interface.
    """
    @abstractmethod
    def append(self, string):
        " Append string to history. "

    @abstractmethod
    def __getitem__(self, key):
        " Return one item of the history. It should be accessible like a `list`. "

    @abstractmethod
    def __iter__(self):
        " Iterate through all the items of the history. Cronologically. "

    @abstractmethod
    def __len__(self):
        " Return the length of the history.  "

    def __bool__(self):
        """
        Never evaluate to False, even when the history is empty.
        (Python calls __len__ if __bool__ is not implemented.)
        This is mainly to allow lazy evaluation::

            x = history or InMemoryHistory()
        """
        return True

    __nonzero__ = __bool__  # For Python 2.

suppress_history_errors=False
_tasks=[]
_loop_started=False
def run_task(task):
    """ This function is also used by the r.py history functions! Such as cd history """ 
    global _loop_started, _tasks
    _tasks.append(task)
    import rp
    if not _loop_started:
        _loop_started=True
        @rp.run_as_new_thread
        def history_task_thread():
            while True:
                import time
                time.sleep(.1)
                while _tasks:
                    task = _tasks.pop(0)
                    try:
                        task()
                    except Exception as e:
                        if not suppress_history_errors:
                            import rp
                            rp.fansi_print('rp.prompt_toolkit.history.run_task: Running '+str(task)+': ERROR: '+str(e)+'\n    - Run rp.prompt_toolkit.history.suppress_history_errors=True to suppress this','red','bold')


class InMemoryHistory(History):
    """
    :class:`.History` class that keeps a list of all strings in memory.
    """
    def __init__(self):
        self.strings = []

    def append(self, string):
        self.strings.append(string)

    def __getitem__(self, key):
        return self.strings[key]

    def __iter__(self):
        return iter(self.strings)

    def __len__(self):
        return len(self.strings)

    def append_with_metadata(self,buffer):
        pass#TODO: Implement this


class FileHistory(History):
    """
    :class:`.History` class that stores all strings in a file.
    """
    def __init__(self, filename):
        self.strings = []
        self.filename = filename
        self.meta_filename=filename+'.meta'#For storing metadata about the history entries
        self._load()

    def _load(self):
        #took .2 seconds with 18000 items in history; 
        from rp import run_as_new_thread

        def load_history():
            if not os.path.exists(self.filename):
                return
            
            # Phase 1: Load last _fast_pterm_history_size for immediate access  
            # (This two-phase system which first loads a few history lines then loads them all was written by Claude in Aug 2025. It resulted in a massive speed boost allowing us to get history with the up arrow key immediately after booting rp. This only became noticeable after other improvements to boot time made RP boot faster than it could read the whole history file.)
            try:
                import rp
                fast_size = rp.r._fast_pterm_history_size
                with open(self.filename, 'rb') as f:
                    f.seek(0, 2)  # Go to end
                    file_size = f.tell()
                    start_pos = max(0, file_size - fast_size)
                    f.seek(start_pos)
                    data = f.read().decode('utf-8', errors='ignore')
                
                # Parse the tail data quickly
                lines = []
                temp_strings = []
                
                for line in data.split('\n'):
                    if line.startswith('+'):
                        lines.append(line[1:] + '\n')
                    else:
                        if lines:
                            string = ''.join(lines)[:-1]
                            temp_strings.append(string)
                        lines = []
                if lines:
                    string = ''.join(lines)[:-1]
                    temp_strings.append(string)
                
                # Set partial results immediately
                self.strings = temp_strings
            except Exception:
                pass
            
            # Phase 2: Load complete file (overwrites partial results)
            try:
                with open(self.filename, 'rb') as f:
                    lines = []
                    complete_strings = []
                    
                    for line in f:
                        line = line.decode('utf-8')
                        if line.startswith('+'):
                            lines.append(line[1:])
                        else:
                            if lines:
                                string = ''.join(lines)[:-1]
                                complete_strings.append(string)
                            lines = []
                    if lines:
                        string = ''.join(lines)[:-1]
                        complete_strings.append(string)
                
                # Replace with complete results
                self.strings = complete_strings
                
                # Notify that full loading is complete
                import rp
                rp.r._on_history_load_complete(self)
            except Exception:
                pass
        # if os.path.exists(self.filename):
        #     with open(self.filename, 'rb') as f:
        #         for line in f:
        #             line = line.decode('utf-8')

        #             if line.startswith('+'):
        #                 lines.append(line[1:])
        #             else:
        #                 add()
        #                 lines = []
        #         add()

        #FIRST ATTEMPT AT GOING REVERSE ORDER. BUT ITS SLOWER AND LAGS A BIT...ALSO WE GOTTA DO PROCESSING CORRECTLY...
        # def prepend():
        #     if lines:
        #         # Join and drop trailing newline.
        #         string = '\n'.join(lines)
        #
        #         self.strings.insert(0,string) #Meh it's fast enough even though it's technically O(n^2) right?
        #
        # def add_all_lines():
        #     import rp
        #     nonlocal lines
        #     if os.path.exists(self.filename):
        #         # with open(self.filename, 'rb') as f:
        #         #     for line in f:
        #             for line in rp.file_line_iterator(self.filename, reverse=True):
        #                 # print(line)
        #                 # line = line.decode('utf-8')
        #
        #                 if line.startswith('+'):
        #                     lines.append(line[1:])
        #                 else:
        #                     prepend()
        #                     lines = []
        #             prepend()
        #     rp.text_to_speech("b")
                    
        run_as_new_thread(load_history)  # Single thread with two-phase loading

    def append(self, string):
        self.strings.append(string)

        def task():
            # Save to file.
            with open(self.filename, 'ab') as f:
                def write(t):
                    f.write(t.encode('utf-8'))
                
                write('\n# %s\n' % datetime.datetime.now())
                for line in string.split('\n'):
                    write('+%s\n' % line)
        run_task(task)

    def get_all_metadata(self):
        #Get all history metadata fresh from the file
        import json
        try:
            with open(self.meta_filename,'r') as json_file:
                meta_data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            meta_data = {}
        except FileNotFoundError:
            meta_data = {}
        return meta_data

    def update_metadata(self,index,data):
        import json

        #Update an entry in the history's metadata file
        meta_data=self.get_all_metadata()

        #Apply a delta to metadata...
        if index in meta_data:
            assert isinstance(index[meta_data],dict),'rp.pseudo_terminal internal error: history meta_data has invalid schema...you must have tampered with '+repr(self.meta_filename)+' somehow, try deleting it if it continues to cause problems.'
            meta_data.update(data)
        else:
            meta_data[index]=data

        with open(self.meta_filename,'w') as json_file:
            json.dump(meta_data,json_file,indent=4)

    def get_metadata_entry(self,key):
        return self.get_all_metadata([key])

    def get_parent_document(self,buffer):
        return
        working_index=buffer.working_index+1#The index we started writing from originally. This is the 'parent' history entry.
        try:
            metadata_entry=get_metadata_entry()
            return Document(text=getme)
        except:
            return buffer.document



    def append_with_metadata(self,buffer):
        return
        #TODO: Right now this has two problems. One is that it re-reads the meta file every time, and this is slow. At the same time, 
        # it also suffers from index collision problems with two rp instances are running at once. How do we solve this problem? 
        import json,time
        meta_filename=self.filename+'.meta'
        working_index=buffer.working_index+1#The index we started writing from originally. This is the 'parent' history entry.
        current_index=len(self.strings)

        entry={
            'parent_index':working_index,
            'index':current_index,
            'time' :time.time(),
            'cursor_position':buffer.cursor_position,
            'text' :buffer.document.text
        }
        self.update_metadata(current_index,entry)



    def __getitem__(self, key):
        return self.strings[key]

    def __iter__(self):
        return iter(self.strings)

    def __len__(self):
        return len(self.strings)
