The Steepest Ascent Hill Climber (With Replacement)
===================================================

*Steepest Ascent Hill-Climbing With Replacement* makes the search more aggresive than a regular hill-climber by sampling multiple times around the current candidate solution [EOM]_.

Contents:

   * :ref:`SteepestAscent Class <optimization-optimizers-steepestascent>`

For examples:
       
   * :ref:`Normal Distribution Example <optimization-optimizers-steepestascent-normalexample>`
   * :ref:`Needle in a Haystack Example <optimization-optimizers-steepestascent-needleinahaystack>`   
   * :ref:`Gaussian Convolution Noisy Example <optimization-optimizers-steepestascent-gaussianconvolution>`
   * :ref:`Gaussian Convolution Normal Example <optimization-optimizers-steepestascent-gaussianconvolution-normal>`



.. _optimization-optimizers-steepestascent:

SteepestAscent Class
--------------------

.. uml::

   BaseClimber <|-- SteepestAscent

.. currentmodule:: tuna.optimizers.baseclimber
.. autosummary::
   :toctree: api

   BaseClimber

.. currentmodule:: tuna.optimizers.steepestascent
.. autosummary::
   :toctree: api

   SteepestAscent
   SteepestAscent.__call__
   SteepestAscent.reset



This optimizer only has one real parameter to tune (``local_searches``) which decides how much it looks around each candidate. If this is small it will act more like a regular hill-climber (so the data has to have more information than noise) but if it is large it will be less likely to go off in the wrong direction. The Tweak used is what's responsible for most of the exploration this does. With GaussianConvolution, changing :math:`\sigma^2` to something larger will cause it to jump more often. If both the number of local searches and the spread are large, you end up with `evolutionary pressure <http://en.wikipedia.org/wiki/Evolutionary_pressure>`_ where there will be high mutation but the aggressive local searching will tend to weed out the bad variants.
