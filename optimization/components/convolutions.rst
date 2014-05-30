The Convolutions
================


These are convolutions to `tweak` the candidate solutions when optimizing.

.. currentmodule:: optimization.components.convolutions
.. autosummary::
   :toctree: api

   UniformConvolution
   UniformConvolution.__call__

It uses numpy's ``random.uniform`` function as well as it's ``clip`` method.

.. currentmodule:: numpy
.. autosummary::
   :toctree: api

   random.uniform

.. currentmodule:: numpy
.. autosummary::
   :toctree: api

   clip


   
Gaussian Convolution
--------------------

This samples from a normal distribution instead of a uniform one. It will tend to make very small changes but occasionally make very large ones _[EOM]. Most of what it does looks the same as the UniformConvolution except with different variable or function names but I thought that keeping them separate would make it easier to remember the parameters.

.. currentmodule:: optimization.components.convolutions
.. autosummary::
   :toctree: api

   GaussianConvolution
   GaussianConvolution.__call__

From numpy:

.. currentmodule:: numpy
.. autosummary::
   :toctree: api

   random.normal

