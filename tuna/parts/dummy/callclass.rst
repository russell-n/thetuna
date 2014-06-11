Call Class
==========

The call class is a primitive class for dummies to use in ``__getattr__`` to log un-implemented calls. Debugging use only.


CallClass
---------

.. uml::

   CallClass -|> BaseClass

.. autosummary::
   :toctree: api

   CallClass
   CallClass.__call__
   CallClass.__name__   

A class to fake calls and properties.

