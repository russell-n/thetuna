The Dummy
=========

This module holds classes to help test the running of the infrastructure.

Contents:

   * :ref:`The Dummy <dummy-class>`
   * :ref:`The Crash Dummy <crash-dummy>`
   * :ref:`The Hanging Dummy <hanging-dummy>`
   * :ref:`Example Use <dummy-example>`



.. _dummy-class::

The Dummy Class
---------------

.. currentmodule:: tuna.parts.dummy.dummy
.. _dummy-class:

The Dummy module holds dummy classes that do nothing. They is primarily used to test implementations of infrastructure components.

.. uml::

   DummyClass -|> BaseClass
   DummyClass o- CallClass

.. autosummary::
   :toctree: api

   DummyClass
   DummyClass.__call__
   DummyClass.__str__
   DummyClass.__getattr__

The Dummy Class logs (at the `info`) level when it is created and when it is called.



.. _crash-dummy:

A Crash Dummy
-------------

This is a Dummy that raises an error when called.

.. uml::

   CrashDummy -|> DummyClass

.. autosummary::
   :toctree: api

   CrashDummy
   CrashDummy.check_rep
   CrashDummy.close
   CrashDummy.__getattr__

.. note:: check_rep and close don't need to be implemented to crash, but the Composite is checking if it has the attributes before calling them so they have to be implemented to crash them

.. '   



.. _hanging-dummy:

The Hanging Dummy
-----------------

This is a Dummy that will block forever.

.. uml::

   HangingDummy -|> DummyClass

.. autosummary::
   :toctree: api

   HangingDummy
   HangingDummy.__call__
   




.. dummy-example::

An Example
----------

As an example we can create an operator and make some fake calls to it (I do not think the logging will get captured by Pweave, though).

::

    if output_documentation:
        class FakeLogger(object):
            def info(self, output):
                print output
                
        class KingKong(DummyClass):
            def __init__(self, *args, **kwargs):
                super(KingKong, self).__init__(*args, **kwargs)
                self._logger = FakeLogger()
                return
        
    
        kongs = (KingKong(index, name) for index,name in enumerate('Kong MightyJoe'.split()))
        for kong in kongs:
            kong.rampage()
            kong('fay wray')
    

::

    '[34mrampage[0;0m' attribute called on [31mKingKong[0;0m
    [31mKingKong[0;0m Called
    [1mArgs:[0;0m ('fay wray',)
    [1mKwargs:[0;0m {}
    '[34mrampage[0;0m' attribute called on [31mKingKong[0;0m
    [31mKingKong[0;0m Called
    [1mArgs:[0;0m ('fay wray',)
    [1mKwargs:[0;0m {}
    



I had to add a fake logger because pweave does not capture logging output. If you run this module::

    python dummy.py

You should see what is being sent to the logger in full color (without the extra ANSI codes).

