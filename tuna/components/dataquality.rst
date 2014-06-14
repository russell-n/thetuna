The Data Qualities
==================



These are classes meant to be dropped into place where `Quality` classes are called. They take csv-files, convert them to arrays and return matching output values based on indices of the arrays.

The XYData Quality
------------------

This class takes a filename and reads it in as an array. It takes a two-dimensional array and uses the values to look-up the data (the arguments have to be x,y indices for the array).

.. currentmodule:: tuna.qualities.dataquality
.. autosummary::
   :toctree: api

   XYData

