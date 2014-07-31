Exhaustive Search
=================

This is as exhaustive grid-search.



Exhaustive Search Constants
---------------------------

These are constants to make building the ExhaustiveSearch object less error-prone.

::

    class ExhaustiveSearchConstants(object):
        __slots__ = ()
        # configuration options
        minima_option = 'minima'
        maxima_option = 'maxima'
        increments_option = 'increments'
        datatype_option = 'datatype'
    
    



Exhaustive Search Implementation
--------------------------------

.. module:: tuna.optimizers.exhaustivesearch
.. autosummary::
   :toctree: api

   ExhaustiveSearch
   ExhaustiveSearch.check_rep
   ExhaustiveSearch.close
   ExhaustiveSearch.carry
   ExhaustiveSearch.__call__
   


The ExhaustiveSearchBuilder
---------------------------

This is a builder of exhaustive searches.

.. uml::

   ExhaustiveSearchBuilder o- ExhaustiveSearch
   ExhaustiveSearchBuilder o- ConfigurationMap
   ExhaustiveSearchBuilder.product

.. autosummary::
   :toctree: api

   ExhaustiveSearchBuilder
   ExhaustiveSearchBuilder.product
   
