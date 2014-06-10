The Components
==============

.. _the-components:

Contents:

    * :ref:`Introduction <components-introduction>`
    * :ref:`Component Module Diagram <component-module-diagram>`
    * :ref:`The Component Class <component-class>`
    * :ref:`The Composite Class <composite-class>`

.. _components-introduction:
Introduction
------------

This is a module to hold classes that (loosely) implement the `Composite Pattern <http://en.wikipedia.org/wiki/Composite_pattern>`_. See the :ref:`Tuna Plugin <tuna-plugin>` for how the Composites are being used in the `tuna` (it is implemented in the `product` property).




.. _component-class:

The Component Class
-------------------

This is the base-class which the other classes will inherit from. All :ref:`Plugin products <base-plugin-product>` should look like this (it doesn't do much but every method is called at some point by the Composites so all plugin products should implement it).

.. '

.. uml::

   Component -|> BaseClass
   Component : __call__()
   Component : check_rep()
   Component : close()

.. currentmodule:: tuna.components.component
.. autosummary::
   :toctree: api

   Component
   Component.__call__
   Component.check_rep
   Component.close





.. _composite-class:

The Composite
-------------

.. uml::

   Composite -|> Component

.. autosummary::
   :toctree: api

   Composite
   Composite.components
   Composite.add
   Composite.remove
   Composite.__call__
   Composite.__iter__
   Composite.__len__
   Composite.__getitem__
   Composite.one_call
   Composite.check_rep
   Composite.close
   Composite.time_remains

The `Composite` was created to be a generalization of the `Hortator`, `Operator` and `Operations`. By specifying the error that it will catch, the error message it will display if there is one, its components, and the component-category of its components, you specify what type of composite it is. It can also act as a regular composite to contain other parts, but this was the original use-case -- to create the infrastructure for the TUNA.

 * Each component call is wrapped by the :ref:`try_except decorator <try-except-decorator>` which catches the Exception in self.error

 * The default for ``self.time_remains`` is a :ref:`TimeTracker <tuna-parts-countdown-timetracker>` but can also be a :ref:`CountdownTimer <tuna-parts-countdown-countdowntimer>`

