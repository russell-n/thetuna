The Components
==============

.. _the-components:

Contents:

    * :ref:`Introduction <components-introduction>`
    * :ref:`The BaseComponent Class <component-class>`

.. _components-introduction:

Introduction
------------

This is a module to hold classes that (loosely) implement the `Composite Pattern <http://en.wikipedia.org/wiki/Composite_pattern>`_. See the :ref:`Tuna Plugin <tuna-plugin>` for how the Composites are being used in the `tuna` (it is implemented in the `product` property).




.. _component-class:

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

