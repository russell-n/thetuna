The Normally Distributed Data
=============================



This creates data that is normally distributed.

.. currentmodule:: scipy.stats
.. autosummary::
   :toctree: api
      
   normal
   normal.pdf

.. uml::

   BaseSimulation <|-- NormalSimulation

.. currentmodule:: optimization.simulations.normalsimulation
.. autosummary::
   :toctree: api

   NormalSimulation
   NormalSimulation.ideal_solution



It is just a front-end for `scipy.stats`, and can be used to simulate various unimodal cases.

Normal Data Set
~~~~~~~~~~~~~~~

::

    if IN_PWEAVE:
        simulator = NormalSimulation(domain_start=-4, domain_end=4, domain_step
    =0.1)
    
    

.. figure:: figures/plot_normal.svg



Needle In a Haystack
~~~~~~~~~~~~~~~~~~~~

To create the needle in a haystack scenario, you can widen the domain to the point that it becomes rare to find the center.

::

    if IN_PWEAVE:
        simulator = NormalSimulation(domain_start=-100, domain_end=150, domain_
    step=0.1)    
    
    

.. figure:: figures/plot_needle_in_haystack.svg



Normal But Noisy
----------------

The `NormalSimulation` produces a unimodal distribution, to make a noisy distribution, values can be randomly chosen from the distribution and other functions added to the output (which is what we're doing here).

.. '

.. currentmodule:: scipy.stats
.. autosummary::
   :toctree: api

   norm.rvs

.. currentmodule:: optimization.simulations.normalsimulation
.. autosummary::
   :toctree: api

   NoisySimulation

::

    if IN_PWEAVE:
        squared = lambda x: scipy.power(x, 2)
        sine = lambda x: scipy.sin(x)
        noisy = NoisySimulation(domain_start=0, domain_end=100, domain_step=1,
                                functions=[squared, sine])
    
    

.. figure:: figures/noisy_data.svg



Local Optima
------------

The same idea that was used to alter the noisy data can also be used to alter the normal distribution to create something multimodal.

::

    if IN_PWEAVE:
        cosine_squared = lambda x: scipy.cos(x)**2
        sine = lambda x: -scipy.sin(x)
        simulator = NormalSimulation(domain_start=-4,
                                     domain_end=4.1,
                                     domain_step=0.1,
                                     functions=[cosine_squared, sine])
    
    

.. figure:: figures/plot_local_optima.svg

