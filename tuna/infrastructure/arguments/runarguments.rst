The Run Sub-Command Arguments
=============================
::

    """`run` sub-command
    
    Usage: tuna run -h
           tuna run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: tuna.ini
    ]
    
    Options;
    
        -h, --help  This help message.
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingoptimizer-run-sub-command>` for more information about this section.

Contents:

    * :ref:`Run Arguments Constants <tuna-interface-run-arguments-constants>`
    * :ref:`Run Arguments Class <tuna-interface-run-arguments-class>`
    * :ref:`Run Strategy <tuna-interface-run-strategy>`



.. _tuna-interface-run-arguments-constants:

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
        default_configfiles = ['tuna.ini']
    # RunArgumentsConstants    
    
    



.. _tuna-interface-run-arguments-class:

The RunArguments Class
----------------------

.. uml::

   BaseArguments <|-- RunArguments

.. currentmodule:: tuna.interface.arguments.runarguments
.. autosummary::
   :toctree: api

   RunArguments
   RunArguments.configfiles
   RunArguments.reset



.. _tuna-interface-run-strategy:

The Run Strategy
----------------

This is the strategy for the `run` sub-command than runs the TUNA.

.. uml::

   BaseStrategy <|-- RunStrategy

.. autosummary::
   :toctree: api

   RunStrategy

