Exhaustive Search with Simulated Data
=====================================

.. _case-study-exhaustive-search-simulated:

Problem
-------

*How can we characterize the data as a whole to tune the parameters for the optimizers?*

In order to make the optimization work we need to know how to set the parameters that affect whether the optimizer will emphasize *exploration* or *exploitation* (will it jump around a lot or will it stick to looking around where it is?). We also need to know a reasonable stopping condition -- setting an ideal value would allow a short-circuit to end the optimization but runs the risk that we've chosen an incorrect ideal value, while setting a time-out runs the risk of either being too short and missing the optimal value or being too long and searching needlessly while delaying moving on to the next phase of the experiment.

.. '

What we'll do here is use data collected by exhaustively sweeping a table to see how to do an exhaustive grid search.

.. '

The Simulation Data
-------------------

Alex created the data-set (:download:`download <data/data_step50.csv>`) by stepping through the table coordinates (with a step-size of 50) while the table was inside a Faraday cage and measuring throughput using iperf (I don't know what the scale of 50 means in human terms, but the annealer doesn't need to know either). The file is a csv with the row-indices assumed to be the y-values and the column-indices assumed to the be the x-values (both scaled by the step-size of 50). The values are the iperf bandwidth measurements for the location on the table (the traffic was run downstream for 5 seconds with the TCP window set to 256 K).

Data Plots
~~~~~~~~~~

.. figure:: figures/data_profile.png
   :scale: 75%


   *Side View* (0,0) is at rear-left, (3000,3000) at front right, z-axis is Mbits/second.


.. figure:: figures/data_angled.png
   :scale: 75%

.. figure:: figures/contoured.png
   :scale: 75%

   Max-throughput (72.7 Mb/s) at (350, 2550) indicated by intersection of red lines. Min-throughput (0.22 Mb/s) at (1200, 2950) indicated by intersection of blue lines.


 

Summary Statistics
~~~~~~~~~~~~~~~~~~

.. csv-table:: Summary Table
   :header: Statistic, Value

   count,3721
   mean,46.0563
   std,16.8165
   min,0.22
   25%,36.8
   50%,49.5
   75%,59
   max,72.7




Pseudocode for the Grid Search
------------------------------

   1. Get the first candidate solution
   2. Make the candidate solution the best solution
   3. While the candidate is less or equal to the maximum position:
   
      3.1. If the candidate is better than the best solution, make the candidate the best solution
      3.2. Increment the candidate position

   4. Return the best solution


Sample Configuration File
-------------------------

This is a sample configuration file for running this test.

.. literalinclude:: data/exhaustive_search.ini
   :language: ini

TUNA Section
~~~~~~~~~~~~

The ``[TUNA]`` section is a place to list what the plugin sections will be. In this case we're telling the `tuna` that there will only be one plugin and the information to configure it will be in a section named ``[GridSearch]``.

.. '

DEFAULT Section
~~~~~~~~~~~~~~~

We're going to repeat the simulation once and store the data in a folder named `grid_search_full_table` next to the configuration file.

.. '

MODULES Section
~~~~~~~~~~~~~~~

In this case we're simulating the use of Cameron's XYTable so we need to tell the `tuna` which module contains the plugin to fake the table's operation. This isn't really needed for the simulation but provides a way to check and see that the `tuna` is calling it the way we expect. The listed module will be imported so the ``xytable`` package has to have been installed for this to work.

GridSearch Section
~~~~~~~~~~~~~~~~~~

The ``plugin = GridSearch`` line tells the tuna to load the `GridSearch` class. 

The ``components = fake_table, table_data`` line tells the tuna to create components using the `fake_table` and `table_data` section in this configuration and give it to the Simulated Annealer (wrapped in a :ref:`composite <simple-composite>`). The components will be used to decide how good a location is. In this case we're substituting mocks for a table control object (fake_table) and an iperf object (table_data). `fake_table` will just log the calls made to it so we can check that the program is running like we think it should. The `table_data` object will lookup the data that Alex recorded using the table-coordinates it was given and give it back to the Simulated Annealer.

The ``observers = fake_table`` line tells the `tuna` to give the `GridSearch` a copy of the table-mock so that it will call it once it stops. This simulates moving the table to the best solution found at the end of an optimization run.

The ``minima = 0,0`` means that our miminum values for `x` and `y` are 0. The ``maxima = 60,60`` means that the maximum values for `x` and `y` are 60. ``increments = `` means that we'll be stepping through the grid 1 at a time (e.g. <0,0>, <1,0>, <2,0>... <60,60>). The ``datatype = int`` means that the `minima, maxima`, and `increments` will be cast to integers. 

.. '

The Outcome
-----------

Since it searches all the points the best-point will always be found and given to the FakeTable. The data has 3,721 cells so if we assume that it would take 15 seconds on average to measure each point (10 seconds for iperf, 5 seconds to move), we can estimate the total running time.

.. math::

   RunningTime &= (3721^2 \times 15)/3600\\
   &= \approx 15.5\\

So this would take about fifteen and a half hours to finish.   
