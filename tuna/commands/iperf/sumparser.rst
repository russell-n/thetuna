The SumParser
=============


The SumParser uses the summed lines instead of re-adding up the parallel threads. There seems to be a discrepancy between the added values and the sum-line at the end. My assumption is that the last line is the most 'accurate' but there's no indication of variance and there might be uses for both calculations.

.. '



The HumanExpressionSum
----------------------

.. currentmodule:: tuna.commands.iperf.sumparser
.. autosummary::
   :toctree: api

   HumanExpressionSum
   HumanExpressionSum.thread_column

This is meant to parse human-readable iperf output (as opposed to the csv format).



CsvExpressionSum
----------------

.. autosummary::
   :toctree: api

   CsvExpressionSum
   CsvExpressionSum.thread_column

This is meant to get the sum lines when the csv-format (`--reportstyle c`) is used.



SumParser
---------

.. uml::

   IperfParser <|-- SumParser

.. autosummary::
   :toctree: api

   SumParser
   SumParser.regex
   SumParser.__call__
   SumParser.pipe

The original idea that the iperf-parsers would be used with piped input (e.g. `cat iperfdata.txt | iperfparser`) but since I'm not adding the front end here (to the tuna) the `__call__` is probably the main interface.

.. '
   
