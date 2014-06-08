The Help Sub-Command Arguments
==============================
::

    """`help` sub-command
    
    usage: optimizer help -h
           optimizer help [-w WIDTH] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                A specific plugin to inquire about [default: Optimizer].
    
    optional arguments:
        -h, --help            show this help message and exit
        -w , --width <width>  Number of characters to wide to format the page. [default: 80]
        -m, --module <module>     non-optimizer module with plugins
        
    """
    



Contents:

   * :ref:`Help Constants <optimizer-interface-arguments-help-constants>`
   * :ref:`Help Arguments Class <optimizer-interface-help-arguments-class>`
   * :ref:`Help Strategy <optimizer-interface-arguments-help-strategy>`



.. _optimizer-interface-arguments-help-constants:

The Help Arguments Constants
----------------------------

.. currentmodule:: optimizer.interface.arguments.helparguments
.. autosummary::
   :toctree: api

   HelpArgumentsConstants



.. _optimizer-interface-help-arguments-class:

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



.. _optimizer-interface-arguments-help-strategy:

The Help Strategy
-----------------

.. uml::

   BaseStrategy <|-- HelpStrategy

.. autosummary::
   :toctree: api

   HelpStrategy
   HelpStrategy.function

