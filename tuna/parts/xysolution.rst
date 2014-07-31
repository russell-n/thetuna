The XY Solution
===============



.. _optimization-components-xysolution-xysolution:    

The XYSolution
--------------

This is a Solution for the optimizations to use when mapping a collection of inputs (:math:`x_0, x_1, \ldots x_n`) to an output (`y`) with the goal of maximizing `y`.

.. uml::

   XYSolution : <narray> inputs
   XYSolution : <float> output

.. module:: tuna.parts.xysolution
.. autosummary::
   :toctree: api

   XYSolution
   XYSolution.copy
   XYSolution.__eq__
   XYSolution.__le__
   XYSolution.__ge__
   XYSolution.__lt__
   XYSolution.__add__
   XYSolution.__radd__
   XYSolution.__sub__
   XYSolution.__rsub__
   XYSolution.__mul__
   XYSolution.__rmul__
   XYSolution.__len__
   XYSolution.__getitem__
   XYSolution.__str__
   



.. _optimization-components-xysolution-xytweak:

The XYTweak
-----------

.. uml::

   XYTweak : <convolution> tweak
   XYTweak o- Convolution
   XYTweak : <XYSolution> __call__(vector)

.. autosummary::
   :toctree: api

   XYTweak
   XYTweak.__call__



.. _optimization-components-xysolution-generator:

XYSolution Generator
--------------------

A generator of XYSolution candidates.

Responsibility
~~~~~~~~~~~~~~

The XYSolutionGenerator generates XYSolution objects with random input values.

.. autosummary::
   :toctree: api

   XYSolutionGenerator
   XYSolutionGenerator.candidate
   XYSolutionGenerator.random_function
   XYSolutionGenerator.__iter__

Collaborators
~~~~~~~~~~~~~

.. currentmodule:: numpy.random
.. autosummary::
   :toctree: api

   uniform

.. currentmodule:: itertools
.. autosummary::
   :toctree: api

   repeat



Although this was created to generate XYSolution candidates, since the candidate property is public, it can be used to create initial candidates to start the optimizations as well.
