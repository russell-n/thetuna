Testing The CSV Storage
=======================

This tests the csv-storage. It's assumed that the ``DictWriter`` will be the main interface, not the regular ``writer``.

.. '

.. currentmodule:: ape.parts.storage.tests.testcsvstorage
.. autosummary::
   :toctree: api

   TestCsvStorage.test_constructor
   TestCsvStorage.test_path_only
   TestCsvStorage.test_bad_constructor
   TestCsvStorage.test_writerow
   TestCsvStorage.test_open
   TestCsvStorage.test_writerows
   TestCsvStorage.test_writer

.. csv-table:: Parameter Tests
   :header: Path, Header, Storage, Expected Outcome

   None, None, None, ApeError
   None, None, storage, ApeError
   None, header, None, ApeError
   None, header, storage, header and rows written to storage
   path, None, None, ApeError
   path, None, storage, ApeError
   path, header, None, header and rows written to new storage
   path, header, storage, header and rows written to storage


