The Base Storage
================

.. _base-storage:

This is a module for an Abstract Base Class to create the minimal file-like interface for storage objects. Although the model for storage is ``file``, it behaves a little differently in that it stores any paths that need to be added (e.g. for sub-folders). 



The BaseStorage
---------------



.. currentmodule:: tuna.parts.storage.base_storage
.. autosummary::
   :toctree: api

   BaseStorage
   BaseStorage.file
   BaseStorage.close
   BaseStorage.open
   BaseStorage.write
   BaseStorage.writeline
   BaseStorage.writelines
