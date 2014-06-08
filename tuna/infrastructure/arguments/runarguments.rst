The Run Sub-Command Arguments
=============================
::

    """`run` sub-command
    
    Usage: optimizer run -h
           optimizer run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: optimize
    r.ini]
    
    Options;
    
        -h, --help  This help message.
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingoptimizer-run-sub-command>` for more information about this section.

Contents:

    * :ref:`Run Arguments Constants <optimizer-interface-run-arguments-constants>`
    * :ref:`Run Arguments Class <optimizer-interface-run-arguments-class>`
    * :ref:`Run Strategy <optimizer-interface-run-strategy>`



.. _optimizer-interface-run-arguments-constants:

The RunArguments Constants
--------------------------

::

    class RunArgumentsConstants(object):
        """
        Constants for the Run Arguments
        """
        __slots__ = ()
        configfiles = '<configuration>'
        
        # defaults
        default_configfiles = ['optimizer.ini']
    # RunArgumentsConstants    
    
    



.. _optimizer-interface-run-arguments-class:

The RunArguments Class
----------------------

.. uml::

   BaseArguments <|-- RunArguments

.. currentmodule:: optimizer.interface.arguments.runarguments
.. autosummary::
   :toctree: api

   RunArguments
   RunArguments.configfiles
   RunArguments.reset



.. _optimizer-interface-run-strategy:

The Run Strategy
----------------

This is the strategy for the `run` sub-command than runs the OPTIMIZER.

.. uml::

   BaseStrategy <|-- RunStrategy

.. autosummary::
   :toctree: api

   RunStrategy

