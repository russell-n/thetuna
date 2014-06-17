The Help Sub-Command Arguments
==============================
::

    """`help` sub-command
    
    usage: tuna help -h
           tuna help [-w WIDTH] [-c] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                A specific plugin to inquire about [default: Tuna].
    
    optional arguments:
        -h, --help                show this help message and exit
        -m, --module <module>     non-tuna module with plugins or components
        -c, --components          If set, looks for `components` instead of `plugins`
        -w , --width <width>      Number of characters to wide to format the page. [default: 80]
    """
    



Contents:

   * :ref:`Help Constants <tuna-interface-arguments-help-constants>`
   * :ref:`Help Arguments Class <tuna-interface-help-arguments-class>`
   * :ref:`Help Strategy <tuna-interface-arguments-help-strategy>`



.. _tuna-interface-arguments-help-constants:

The Help Arguments Constants
----------------------------

.. currentmodule:: tuna.interface.arguments.helparguments
.. autosummary::
   :toctree: api

   HelpArgumentsConstants



.. _tuna-interface-help-arguments-class:

The Help Class
--------------

.. uml::

   BaseArguments <|-- Help

.. autosummary::
   :toctree: api

   Help
   Help.width
   Help.modules
   Help.reset
   Help.name
   Help.function
   Help.components



.. _tuna-interface-arguments-help-strategy:

The Help Strategy
-----------------

.. uml::

   BaseStrategy <|-- HelpStrategy

.. autosummary::
   :toctree: api

   HelpStrategy
   HelpStrategy.function

