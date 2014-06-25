
# this package
from base_storage import BaseStorage
#from tuna import BaseClass
from tuna import FILE_TIMESTAMP
from tuna import TunaError


class NullStorage(BaseStorage):
    """
    A class to store data to a file
    """
    def __init__(self, path=None, timestamp=FILE_TIMESTAMP,
                 name=None, overwrite=False, mode=None):
        """
        NullStorage constructor

        :param:

         - `path`: path to prepend to all files (default is current directory)
         - `timestamp`: strftime format to timestamp file-names
         - `name`: Filename to use
         - `overwrite`: If true, clobber existing file with same name
         - `mode`: file mode (e.g. 'a' for append)
        """
        super(NullStorage, self).__init__()
        self._path = None
        self.path = path
        self.timestamp = timestamp

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
        return True

    @property
    def file(self):
        return self
    
    @property
    def path(self):
        """
        The path to prepend to files (cwd if not set by client)
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path and creates the directory if needed
        """
        self._path = path
        return


    def open(self, name, overwrite=False, mode=None, return_copy=True):
        """
        :return: self
        """
        return self

    def close(self):
        """
        Does nothing
        """
        return

    def __enter__(self):
        """
        Support for the 'with' statement

        :return: self
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Does Nothing
        """
        return

    def reset(self):
        """
        Does nothing
        """

    def write(self, line):
        """
        Does nothing
        """
        return
# end class NullStorage    
