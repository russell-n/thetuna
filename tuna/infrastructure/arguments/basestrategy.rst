The BaseStrategy
================

.. currentmodule:: tuna.infrastructure.arguments.basestrategy

Contents:

    * :ref:`Introduction <tuna-infrastructure-arguments-base-strategy>`
    * :ref:`Class Model <tuna-infrastructure-arguments-basestrategy-class-model>`
    * :ref:`Error Explanations <tuna-infrastructure-arguments-basestrategy-errors>`



.. _tuna-infrastructure-arguments-base-strategy:

The BaseStrategy
----------------

This is a holder of sub-commands for the arguments. Its main purpose is to  provide the QuarterMaster and Optimization-plugin, since one or both is being used by various sub-commands.

.. _tuna-infrastructure-arguments-basestrategy-class-model:

Class Model
-----------

.. uml::

   BaseStrategy o- QuarterMaster
   BaseStrategy o- Tuna
   BaseStrategy --|> BaseClass



.. _tuna-infrastructure-arguments-basestrategy-errors:

The Errors
----------

There are two kinds of exceptions caught which produce two error-messages:

.. csv-table:: Error Messages
   :header: Exception, Message, Meaning
   :delim: ;

   Exception; Oops, I Crapped My Pants; Something unexpected happened -- this indicates a problem with the code
   KeyboardInterrupt; Oh, I am slain; User killed the runtime for some reason -- clean-up and then close

