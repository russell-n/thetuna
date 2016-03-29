The Base Components
===================

.. _the-components:

Introduction
------------

This is a module to hold the base class that (loosely) implements the `Composite Pattern <http://en.wikipedia.org/wiki/Composite_pattern>`_. See the :ref:`Tuna Plugin <tuna-plugin>` for how the Composites are being used in the `tuna` (it is implemented in the Tuna-plugin's `product` property).



.. _basecomponent-class:

The BaseComponent Class
-----------------------

This is the base-class which the other classes will inherit from. All :ref:`Plugin products <base-plugin-product>` should look like this (it doesn't do much but every method is called at some point by the Composites so all plugin products should implement it).

.. '

.. uml::

   BaseComponent -|> BaseClass
   BaseComponent : __call__()
   BaseComponent : check_rep()
   BaseComponent : close()

.. currentmodule:: tuna.components.component
.. autosummary::
   :toctree: api

   BaseComponent
   BaseComponent.__call__
   BaseComponent.check_rep
   BaseComponent.close

