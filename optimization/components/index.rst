The Components
=============



Components bundle parts for the Composite.

.. digraph:: Components

   rankdir="BT"
   component1 [label="Component"]
   component2 [label="Component"]
   part1 [label="Part"]
   part2 [label="Part"]
   part3 [label="Part"]
   part4 [label="Part"]
   part5 [label="Part"]
   component1 -> Composite
   component2 -> Composite
   part1 -> component2
   part2 -> component2
   part3 -> component1
   part4 -> component1
   part5 -> component1


.. toctree::
   :maxdepth: 1

   The Component <component.rst>

.. toctree::
   :maxdepth: 1

   Testing The Components <tests/index.rst>


