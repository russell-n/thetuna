Call Class
==========

The call class is a primitive class for dummies to use in ``__getattr__`` to log un-implemented calls. Debugging use only.



CallClassConstants
------------------

::

    class CallClassConstants(object):
        """
        Some constants so the expected strings are explicitly defined somewhere
    
        """
        __slots__ = ()
        debug_level = 'debug'
        info_level = 'info'
    
    



CallClass
---------

.. uml::

   CallClass -|> BaseClass

.. module:: tuna.parts.dummy.callclass   
.. autosummary::
   :toctree: api

   CallClass
   CallClass.__call__
   CallClass.__name__   

A class to fake calls and properties.

