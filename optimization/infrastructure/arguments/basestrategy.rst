The BaseStrategy
================

.. currentmodule:: optimization.infrastructure.arguments.basestrategy

Contents:

    * :ref:`Introduction <optimization-infrastructure-arguments-base-strategy>`
    * :ref:`Class Model <optimization-infrastructure-arguments-basestrategy-class-model>`
    * :ref:`Error Explanations <optimization-infrastructure-arguments-basestrategy-errors>`
    * :ref:`UbootKommandant API <ubootkommandant-api>`



.. _optimization-infrastructure-arguments-base-strategy:

The BaseStrategy
----------------

This is a holder of sub-commands for the arguments. Its main purpose is to  provide the QuarterMaster and Optimization-plugin, since one or both is being used by various sub-commands.

.. _optimization-infrastructure-arguments-basestrategy-class-model:

Class Model
-----------

.. uml::

   BaseStrategy o- QuarterMaster
   BaseStrategy o- TheOptimizer
   BaseStrategy --|> BaseClass



.. _optimization-infrastructure-arguments-basestrategy-errors:

The Errors
----------

There are two kinds of exceptions caught which produce two error-messages:

.. csv-table:: Error Messages
   :header: Exception, Message, Meaning
   :delim: ;

   Exception; Oops, I Crapped My Pants; Something unexpected happened -- this indicates a problem with the code
   KeyboardInterrupt; Oh, I am slain; User killed the runtime for some reason -- clean-up and then close

