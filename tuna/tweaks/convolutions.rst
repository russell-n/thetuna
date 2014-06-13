The Convolutions
================


These are convolutions to `tweak` the candidate solutions when optimizing.

Contents:

    * :ref:`Uniform Convolution <optimization-tweaks-uniform>`
    * :ref:`Gaussian Convolution <optimization-tweaks-gaussian>`

.. _optimization-tweaks-uniform:

Uniform Convolution
-------------------

.. currentmodule:: optimization.tweaks.convolutions
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




.. _optimization-tweaks-gaussian:

Gaussian Convolution
--------------------

This samples from a normal distribution instead of a uniform one. It will tend to make very small changes but occasionally make very large ones _[EOM]. Most of what it does looks the same as the UniformConvolution except with different variable or function names but I thought that keeping them separate would make it easier to remember the parameters.

.. currentmodule:: optimization.tweaks.convolutions
.. autosummary::
   :toctree: api

   GaussianConvolution
   GaussianConvolution.__call__

From numpy:

.. currentmodule:: numpy
.. autosummary::
   :toctree: api

   random.normal




A Gaussian Convolution Builder
------------------------------

This is a class to build a GaussianConvolution from a configuration map.



.. autosummary::
   :toctree: api

   GaussianConvolutionBuilder
   GaussianConvolutionBuilder.product

::

    if __name__ == '__builtin__':
        gaussian = GaussianConvolution(lower_bound=-100,
                                       upper_bound=100)
        candidate = numpy.array([5,6])
        print gaussian(candidate)
        
        # change the candidate, move the mean up, widen the distribution
        gaussian.scale = 20
        gaussian.location = 5
        candidate = numpy.array([0, 1, 2])
        gaussian.number_type = int
        print gaussian(candidate)
        
        # clip the values so it's right-skewed
        gaussian.lower_bound = 5
        gaussian.upper_bound = 100
        print gaussian(candidate)
    

::

    [ 5.20361999  4.59882791]
    [-16  26  -7]
    [25  5  5]
    

