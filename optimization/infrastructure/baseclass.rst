BaseClass
=========

This is a module to hold base-classes for others to sub-class. 

API
---

.. currentmodule:: optimization.infrastructure.baseclass

.. autosummary::
   :toctree: api

   BaseClass
   BaseClass.logger
   BaseClass.log_error
   BaseThreadClass

.. currentmodule:: logging
.. autosummary:
   :toctree: api

   Logger

.. currentmodule:: threading
.. autosummary::
   :toctree: Thread   



.. _ape-baseclass-baseclass:

Class BaseClass
---------------

This is the primary base-class. Sub-classes inherit a `logger` attribute so that they can send operational logging messages to a file.

.. uml::

   BaseClass : logger
   BaseClass o-- logging.Logger



BaseThreadClass
---------------

This is an extension to the `BaseClass` that adds a `run_thread` method that logs tracebacks in the event that an exception is raised. Classes that sub-class it need to implement a `run` method for the `run_thread` method to call and a method to put run_thread into a thread. Has a default ``thread`` attribute that contains a ``threading.Thread`` instance with ``run_thread`` as the target and ``daemon`` set to True.

.. uml::

   BaseThreadClass <|- BaseClass
   BaseThreadClass : run_thread()
   BaseThreadClass : run()
   BaseThreadClass o-- logging.Logger
   BaseThreadClass o-- traceback
   BaseThreadClass o-- threading.Thread
   BaseThreadClass : thread
   
This will raise a ``TypeError`` if the child class doesn't implement run and it gets instantiated.

.. '

.. currentmodule::: optimization.infrastructure.baseclass
.. autosummary::
   :toctree: api

   BaseThreadClass
   BaseThreadClass.thread
   BaseThreadClass.run_thread
   BaseThreadClass.run
   BaseThreadClass.reset
   
