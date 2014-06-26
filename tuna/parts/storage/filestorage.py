
# The MIT License (MIT)
# 
# Copyright (c) 2013 Russell Nakamura
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# python standard library
import os
import shutil
import datetime
import re
import copy

# this package
from base_storage import BaseStorage
#from tuna import BaseClass
from tuna import FILE_TIMESTAMP
from tuna import TunaError


WRITEABLE = 'w'
APPENDABLE = 'a'
DIGIT = r'\d'
ONE_OR_MORE = '+'
UNDERSCORE = '_'
FILENAME_SUFFIX = UNDERSCORE + DIGIT + ONE_OR_MORE
IN_PWEAVE = __name__ == '__builtin__'
AMBIGUOUS = "Ambiguous call: 'overwrite' True and mode 'a'"


if IN_PWEAVE:
    example_path = 'aoeu/snth'
    example_file = 'umma.gumma'
    
    
    # this is the part that should be part of the path property
    if not os.path.isdir(example_path):
        os.makedirs(example_path)
    for name in os.listdir('aoeu'):
        print name
    
    # this will be run multiple times, remove the example so it gets started fresh
    if os.path.isdir(example_path):
        shutil.rmtree(example_path)    


if IN_PWEAVE:
    name = "test_{timestamp}.csv"
    print name.format(timestamp=datetime.datetime.now().strftime(FILE_TIMESTAMP))


if IN_PWEAVE:
    # what's here?
    for name in (name for name in os.listdir(os.getcwd()) if name.endswith('txt')):
        print name
    
    name = "innagaddadavida.txt"
    path = os.getcwd()
    full_name = os.path.join(path, name)
    if os.path.exists(full_name):
        base, extension = os.path.splitext(name)
    
        digit = r'\d'
        one_or_more = '+'
        underscore = '_'
    
        suffix = underscore + digit + one_or_more
        expression = r"{b}{s}{e}".format(b=base,
                                          s=suffix,
                                            e=extension)
        regex = re.compile(expression)
        count = sum(1 for name in os.listdir(path) if regex.match(name))
        count = str(count + 1).zfill(4)
        name = "{b}_{c}{e}".format(b=base, c=count, e=extension)
    
    print name            


class FileStorage(BaseStorage):
    """
    A class to store data to a file
    """
    def __init__(self, path=None, timestamp=FILE_TIMESTAMP,
                 name=None, overwrite=False, mode=WRITEABLE):
        """
        FileStorage constructor

        :param:

         - `path`: path to prepend to all files (default is current directory)
         - `timestamp`: strftime format to timestamp file-names
         - `name`: Filename to use
         - `overwrite`: If true, clobber existing file with same name
         - `mode`: file mode (e.g. 'a' for append)
        """
        super(FileStorage, self).__init__()
        self._path = None
        self.path = path
        self.timestamp = timestamp

        # these are to support the `with` statement
        self.name = name
        self.overwrite = overwrite
        self.mode = mode
        self.closed = True
        return

    @property
    def writeable(self):
        """
        checks if the file is open for writing
        """
        return not self.closed and self.mode.startswith('w')        

    @property
    def file(self):
        return self._file
    
    @property
    def path(self):
        """
        The path to prepend to files (cwd if not set by client)
        """
        if self._path is None:
            self._path = os.getcwd()
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path and creates the directory if needed
        """
        
        if path is not None and not os.path.isdir(path):
            os.makedirs(path)
        self._path = path
        return

    def safe_name(self, name, overwrite=False):
        """
        Adds a timestamp if formatted for it, increments if already exists

        :param:

         - `name`: name for file (without path added)
         - `overwrite`: if True, don't mangle the name

        :return: unique name with full path
        """
        name = name.format(timestamp=datetime.datetime.now().strftime(self.timestamp))
        full_name = os.path.join(self.path, name)
        
        if overwrite:
            return full_name
        
        if os.path.exists(full_name):
            base, extension = os.path.splitext(name)


            expression = r"{b}{s}{e}".format(b=base,
                                             s=FILENAME_SUFFIX,
                                             e=extension)
            regex = re.compile(expression)
            count = sum(1 for name in os.listdir(self.path) if regex.match(name))
            count = str(count + 1).zfill(4)
            name = "{b}_{c}{e}".format(b=base, c=count, e=extension)
            full_name = os.path.join(self.path, name)
        return full_name

    def open(self, name, overwrite=False, mode=WRITEABLE, return_copy=True):
        """
        Opens a file for writing

        :param:

         - `name`: a basename (no path) for the file
         - `overwrite`: If True, clobber existing files with the same name
         - `mode`: file-mode (e.g. 'w' or 'a')
         - `return_copy`: If True, return a copy of self, otherwise return self

        :return: copy of self with file as open file and closed set to False
        """
        if overwrite and mode == APPENDABLE:
            self.logger.warning(AMBIGUOUS)
        name = self.safe_name(name, overwrite=overwrite or mode==APPENDABLE)
        self.logger.debug("Opening {0} for writing".format(name))
        if return_copy:
            opened = copy.copy(self)
        else:
            opened = self
        opened.name = name
        opened._file = open(name, mode)
        opened.mode = 'w'
        opened.closed = False
        return opened

    def close(self):
        """
        Closes self.file if it exists, sets self.closed to True
        """
        if self.file is not None:
            self.logger.debug("Closing the File")
            self.file.close()
            self.closed = True
        else:
            self.logger.debug("File is None")
        return

    def __enter__(self):
        """
        Support for the 'with' statement
        This doesn't work exactly right since I'm trying to emulate open()        

        :raise: TunaError if self.name not set
        :return: self (assumes this was called with open())
        """
        if self.name is None:
            raise TunaError("self.name not set, can't open file")
        return self

    def __exit__(self, type, value, traceback):        
        """
        Closes the object
        """
        self.logger.debug("Closing the file")
        self.close()
        return        
