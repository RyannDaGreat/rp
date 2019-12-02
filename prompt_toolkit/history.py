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
        # from rp import sleep,tic,toc,ptoc,ptoctic,ring_terminal_bell,run_as_new_thread,text_to_speech
        from rp import run_as_new_thread
        # ring_terminal_bell()
        # tic()

        lines = []

        def add():
            if lines:
                # Join and drop trailing newline.
                string = ''.join(lines)[:-1]

                self.strings.append(string)

        def add_all_lines():
            nonlocal lines
            if os.path.exists(self.filename):
                with open(self.filename, 'rb') as f:
                    for line in f:
                        # print(line)
                        line = line.decode('utf-8')

                        if line.startswith('+'):
                            lines.append(line[1:])
                        else:
                            add()
                            lines = []
                    add()
            # text_to_speech("a")
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
        run_as_new_thread(add_all_lines)#Running this as a new thread will save .2 seconds with my 18000 items in history
        # ptoctic()
        # sleep(3)
        # ring_terminal_bell()

    def append(self, string):
        self.strings.append(string)

        # Save to file.
        with open(self.filename, 'ab') as f:
            def write(t):
                f.write(t.encode('utf-8'))
            
            write('\n# %s\n' % datetime.datetime.now())
            for line in string.split('\n'):
                write('+%s\n' % line)

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
