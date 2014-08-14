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

.. module:: tuna.infrastructure.arguments.runarguments
.. autosummary::
   :toctree: api

   Run
   Run.configfiles
   Run.function
   Run.reset



.. _tuna-interface-run-strategy:

The Run Strategy
----------------

This is the strategy for the `run` sub-command than runs the TUNA.

.. uml::

   BaseStrategy <|-- RunStrategy

.. autosummary::
   :toctree: api

   RunStrategy

