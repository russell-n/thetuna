The StorageAdapter
==================

The optimizers were originally built to put data into a list, but I want them to write to a file so this is a light-weight adapter.

.. currentmodule:: tuna.optimizers.storage.storageadapter
.. autosummary::
   :toctree: api

   StorageAdapter
   StorageAdapter.append
   StorageAdapter.__getattr__

The StorageAdapter adds an `append` method that converts the item it is given to a string and writes it to storage. The default is to add a newline to the item before writing it. To change this change the `format_string` attribute to something else (but it still has to be a string or something with a `format` method).

