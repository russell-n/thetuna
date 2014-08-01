
class StorageAdapter(object):
    """
    An adapter to add an 'append' method
    """
    def __init__(self, storage, filename, format_string='{0}\n'):
        """
        StorageAdapter constructor

        :param:

         - `storage`: a built storage object
         - `filename`: name for the output (used if `reset` is called)
         - `format_string`: string to cast the item to write to the file to a string
        """
        self.storage = storage
        self.format_string = format_string
        self.filename = filename
        return

    def append(self, item):
        """
        writes the item to the storage

        :param:

         - `item`: data to cast to a string and write to storage
        """
        self.storage.write(self.format_string.format(item))
        return

    def open(self, filename=None):
        """
        Opens the file, sets the self.storage attribute

        :param:

         - `filename`: Name to use instead of self.filename

        :postcondition: self.storage is an opened file-ish object
        """
        if filename is None:
            filename = self.filename
        self.storage = self.storage.open(filename)
        return

    def reset(self):
        """
        Closes the old file, opens a new one
        """
        self.storage.close()
        self.open(self.filename)
        return

    def __getattr__(self, attribute):
        """
        A pass-through to the storage
        """
        return getattr(self.storage, attribute)
