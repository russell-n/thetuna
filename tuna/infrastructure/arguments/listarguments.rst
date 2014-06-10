The List Sub-Command Arguments
==============================
::

    """list subcommand
    
    usage: tuna list -h
           tuna list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    """
    



See the :ref:`developer documentation <docopt-reproducingtuna-list-sub-command>` for more information.

Contents:

    * :ref:`The List Arguments Constants <tuna-interface-arguments-list-arguments-constants>`
    * :ref:`The List Arguments Class <tuna-interface-arguments-list-arguments-class>`
    * :ref:`The List Strategy <tuna-interface-arguments-list-strategy>`



.. _tuna-interface-arguments-list-arguments-constants:

The ListArguments Constants
---------------------------

::

    class ListArgumentsConstants(object):
        """
        Constants for the list sub-command arguments
        """
        __slots__ = ()
        # arguments
        modules = "<module>"
    
    



.. _tuna-interface-arguments-list-arguments-class:

The List Class
--------------

.. uml::

   BaseArguments <|-- List

.. currentmodule:: tuna.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   List
   List.modules
   List.reset
   List.function




.. _tuna-interface-arguments-list-strategy:

The List Strategy
-----------------

.. uml::

   BaseStrategy <|-- ListStrategy

.. currentmodule:: tuna.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   ListStrategy
   ListStrategy.function

