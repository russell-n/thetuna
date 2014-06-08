The Component
=============



The Component
-------------

The Component is the base unit for the Composite tree. The main interface will be a call method and a check-rep method.

.. uml::

   BaseClass <|-- Component
   Component : __call__
   Component : check_rep

.. currentmodule:: optimization.components.component
.. autosummary::
   :toctree: api

   Component
   Component.__call__
   Component.check_rep

The Component implemented here is an abstract base-class that raise an exception if the child-class is instantiated without defining both of those methods.



The Composite
-------------

The Composite extends the Component by adding a collection to hold other Components and methods to add and remove them.

.. uml::

   Component <|-- Composite
   Composite : add(Component)
   Composite: remove(Component)
   Composite: <list> components

.. autosummary::
   :toctree: api

   Composite
   Composite.add
   Composite.remove
   Composite.reset



.. note:: The Composite assumes that the components are run as-is and doesn't pass arguments in to them. To change this behavior override the __call__
