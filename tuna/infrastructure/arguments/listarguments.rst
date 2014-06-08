The List Sub-Command Arguments
==============================
::

    """list subcommand
    
    usage: optimizer list -h
           optimizer list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    """
    



See the :ref:`developer documentation <docopt-reproducingoptimizer-list-sub-command>` for more information.

Contents:

    * :ref:`The List Arguments Constants <optimizer-interface-arguments-list-arguments-constants>`
    * :ref:`The List Arguments Class <optimizer-interface-arguments-list-arguments-class>`
    * :ref:`The List Strategy <optimizer-interface-arguments-list-strategy>`



.. _optimizer-interface-arguments-list-arguments-constants:

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
    
    



.. _optimizer-interface-arguments-list-arguments-class:

The List Class
--------------

.. uml::

   BaseArguments <|-- List

.. currentmodule:: optimizer.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   List
   List.modules
   List.reset
   List.function




.. _optimizer-interface-arguments-list-strategy:

The List Strategy
-----------------

.. uml::

   BaseStrategy <|-- ListStrategy

.. currentmodule:: optimizer.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   ListStrategy
   ListStrategy.function

