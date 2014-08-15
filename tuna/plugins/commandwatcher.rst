The CommandWatcher Plugin
=========================

This plugin creates a :ref:`Composite <the-composite>` of :ref:`TheWatcher <the-watcher>` command to file watchers.



.. uml::

   CommandWatcher --|> BasePlugin
   CommandWatcher o-- HelpPage
   CommandWatcher o-- TheWatcher

.. _commandwatcher-api:

The API
-------

.. module:: tuna.plugins.commandwatcher
.. autosummary::
   :toctree: api

   CommandWatcher
   CommandWatcher.help
   CommandWatcher.product
   CommandWatcher.sections
   CommandWatcher.fetch_config
   
