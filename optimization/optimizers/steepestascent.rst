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

.. currentmodule:: optimization.optimizers.steepestascent
.. autosummary::
   :toctree: api

   SteepestAscent
   SteepestAscent.__call__

