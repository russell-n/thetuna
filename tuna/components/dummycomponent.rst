The Dummy Component
===================



This is meant to be used as a placeholder for code that isn't implemented yet or, more likely, requires something outside of the system and so can't always be used.

The Dummy Component
-------------------

.. uml::

   BaseComponent <|-- DummyComponent
   DummyComponent o- DummyClass

.. currentmodule:: tuna.components.dummycomponent
.. autosummary::
   :toctree: api

   DummyComponent
   DummyComponent.__call__
   DummyComponent.check_rep
   DummyComponent.close
   DummyComponent.__getattr__
   DummyComponent.dummy

::

    CONFIGURATION = """
    [Dummy]
    # this follows the pattern for plugins --
    # the header has to match what's in the Optimizers `components` list
    # the component option has to be DummyComponent
    component = Dummy
    
    # Everything else is arbitrary
    """
    
    DESCRIPTION = """
    The DummyComponent is a placeholder for components that can't be run. It wi
    ll reflect (to stdout) the calls made to it.
    """
    
    




The DummyComponent Builder
--------------------------

A convenience class for building `DummyComponent` objects. It implements the plugin interface so the help and list sub-commands can use it.

.. uml::

   BasePlugin <|-- DummyComponentBuilder   

.. currentmodule:: tuna.components.dummycomponent
.. autosummary::
   :toctree: api

   Dummy
   Dummy.product
    
