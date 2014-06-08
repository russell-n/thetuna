The Check Sub-Command Arguments
===============================
::

    """`check` sub-command
    
    usage: optimizer check -h
           optimizer check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='[
    'optimizer.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-optimizer module with plugins
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingoptimizer-check-sub-command>` for more information about this.

Contents:

   * :ref:`Check Arguments Constants <optimizer-interface-arguments-check-arguments-constants>`
   * :ref:`Check Arguments Class <optimizer-interface-arguments-check-arguments-class>`
   * :ref:`Check Strategy <optimizer-interface-arguments-check-strategy>`



.. _optimizer-interface-arguments-check-arguments-constants:

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
        default_configfilenames = ['optimizer.ini']
    
    



.. _optimizer-interface-arguments-check-arguments-class:

The Check Class
---------------

.. uml::

   BaseArguments <|-- Check

.. currentmodule:: optimizer.interface.arguments.checkarguments
.. autosummary::
   :toctree: api

   Check
   Check.configfiles
   Check.modules
   Check.reset
   Check.function



.. _optimizer-interface-arguments-check-strategy:

The Check Strategy
------------------

The Check strategy calls `check_rep` on the plugins.

.. uml::

   BaseStrategy <|-- CheckStrategy

.. autosummary::
   :toctree: api

   CheckStrategy
   CheckStrategy.function

