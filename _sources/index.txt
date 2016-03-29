The Tuna
========

.. .. figure:: figures/blackfin_tuna_duane_raver_jr.jpg




.. _the-tuna:

*The Tuna* is an optimizer that seeks to find the optimal location for a device that is being tested. It was created to use a proprietary x-y table (table with two axes that could be placed anywhere within the square platform) but the controller for the table was created as an external plugin so it would need a plugin written for any controller's that are used to optimize the device's performance. The code is hosted on `github <https://github.com/russellnakamura/thetuna>`_.

To get an idea of the problem that this was trying to solve look at the `Random Restarts explanation <https://russellnakamura.github.io/thetuna/documentation/user/case_studies/random_restarts/random_restarts_full_table.html>`_. Although it is meant to explain how the optimizer works the data used was real data that was collected to see how well an exhaustive search might work (it took too long to be practical) and might give you some idea of why an optimizer was needed.

Written Documentation
---------------------

.. toctree::
   :maxdepth: 1
   
   Developer Documentation <documentation/developer/index>
   User Documentation <documentation/user/index>

Auto-Generated Documentation
----------------------------



.. toctree::
   :maxdepth: 1

   Log Setter <log_setter.rst>
   The Main Entry Point <main.rst>

.. toctree::
   :maxdepth: 1

   Client Connections <clients/index.rst>
   Commands <commands/index.rst>
   The Components <components/index.rst>
   Explorations <explorations/index.rst>
   Hosts <hosts/index.rst>
   The Infrastructure <infrastructure/index.rst>
   Optimizers <optimizers/index.rst>
   The Parts <parts/index.rst>
   The Tuna-Plugins <plugins/index.rst>
   Quality Modules <qualities/index.rst>
   Tweaks <tweaks/index.rst>




