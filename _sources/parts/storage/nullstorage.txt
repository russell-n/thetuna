Null Storage
============

.. _null-storage-module::

Since I'm re-using a bunch of parts that think their main role is to collect data and save it to disk I'm creating a NullStorage class that discards strings instead of writing to disk to put in the place of a file storage.




.. _file-storage-api:

NullStorage API
---------------

.. currentmodule:: tuna.parts.storage.nullstorage
.. autosummary::
   :toctree: api

   NullStorage
   NullStorage.path
   NullStorage.safe_name
   NullStorage.open
   NullStorage.close
   NullStorage.write
   NullStorage.writeline
   NullStorage.writelines


