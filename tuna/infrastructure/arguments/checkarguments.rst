The Check Sub-Command Arguments
===============================
::

    """`check` sub-command
    
    usage: tuna check -h
           tuna check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='[
    'tuna.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-tuna module with plugins
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingtuna-check-sub-command>` for more information about this.



.. _tuna-interface-arguments-check-arguments-constants:

The CheckArgumentsConstants
---------------------------

::

    class CheckArgumentsConstants(object):
        """
        A holder of constants for the Check Sub-Command Arguments
        """
        __slots__ = ()
        # options and arguments
        configfilenames = "<config-file-name>"
        modules = "--module"
    
        #defaults
        default_configfilenames = ['tuna.ini']
    
    



.. _tuna-interface-arguments-check-arguments-class:

The Check Class
---------------

.. uml::

   BaseArguments <|-- Check

.. currentmodule:: tuna.infrastructure.arguments.checkarguments

.. autosummary::
   :toctree: api

   Check
   Check.configfiles
   Check.modules
   Check.reset
   Check.function



.. _tuna-interface-arguments-check-strategy:

The Check Strategy
------------------

The Check strategy calls `check_rep` on the plugins.

.. uml::

   BaseStrategy <|-- CheckStrategy

.. autosummary::
   :toctree: api

   CheckStrategy
   CheckStrategy.function

