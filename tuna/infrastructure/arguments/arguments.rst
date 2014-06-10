The Arguments
=============
::

    """tuna (a metaheuristic maximizer)
    
    Usage: tuna -h | -v
           tuna [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Logging Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    Debugging Options:
    
        --pudb       Enable the `pudb` debugger (if installed)
        --pdb        Enable the `pdb` (python's default) debugger
    
    Positional Arguments:
    
        <command>      The name of a sub-command (see below)
        <argument>...  One or more options or arguments for the sub-command
        
    Available Sub-Commands:
    
        run    Run a plugin
        fetch  Fetch a sample configuration-file
        help   Display more help
        list   List known plugins
        check  Check a configuration
    
    To get help for a sub-command pass `-h` as the argument. e.g.:
    
        tuna run -h
    
    """     
    


.. currentmodule:: tuna.infrastructure.arguments


Contents:

   * :ref:`The Argument Constants <tuna-interface-arguments-argumentconstants>`
   * :ref:`The BaseArguments <tuna-interface-arguments-basearguments>`

   
.. _tuna-interface-arguments-argumentconstants:

The ArgumentConstants
---------------------

::

    class ArgumentsConstants(object):
        """
        Constants for the arguments
        """
        __slots__ = ()
        debug = "--debug"
        silent = '--silent'
        pudb = "--pudb"
        pdb = '--pdb'
        trace = '--trace'
        callgraph = '--callgraph'
        command = "<command>"
        argument = '<argument>'
    # end ArgumentConstants    
    
    



.. _tuna-interface-arguments-basearguments:

The BaseArguments
-----------------

.. currentmodule:: docopt
.. autosummary::
   :toctree: api

   docopt
   DocoptExit

.. uml::

   BaseClass <|-- BaseArguments
   BaseArguments o-- CheckArguments
   BaseArguments o-- RunArguments
   BaseArguments o-- FetchArguments
   BaseArguments o-- ListArguments
   BaseArguments o-- HelpArguments

.. currentmodule:: tuna.infrastructure.arguments.arguments
.. autosummary::
   :toctree: api

   BaseArguments
   BaseArguments.arguments
   BaseArguments.sub_arguments
   BaseArguments.debug
   BaseArguments.silent
   BaseArguments.pudb
   BaseArguments.pdb
   BaseArguments.trace
   BaseArguments.callgraph
   BaseArguments.reset

