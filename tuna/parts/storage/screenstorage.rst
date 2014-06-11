Screen Storage
==============

This is an adapter for stdout so that it can be used interchangeably with the other storages. This almost isn't needed, but it turns out things go badly if you try to close stdout.

.. superfluous '

.. uml::

   ScreenStorage -|> BaseStorage

.. autosummary::
   :toctree: api

   ScreenStorage


