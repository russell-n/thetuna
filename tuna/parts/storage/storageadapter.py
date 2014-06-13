
class StorageAdapter(object):
    """
    An adapter to add an 'append' method
    """
    def __init__(self, storage, format_string='{0}\n'):
        """
        StorageAdapter constructor

        :param:

         - `storage`: a built storage object
         - `format_string`: string to cast the item to write to the file to a string
        """
        self.storage = storage
        self.format_string = format_string
        return

    def append(self, item):
        """
        writes the item to the storage

        :param:

         - `item`: data to cast to a string and write to storage
        """
        self.storage.write(self.format_string.format(item))
        return

    def __getattr__(self, attribute):
        """
        A pass-through to the storage
        """
        return getattr(self.storage, attribute)
