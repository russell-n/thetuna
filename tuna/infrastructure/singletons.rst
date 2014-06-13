The Singletons
==============

This is a module to hold singletons. The (initial) problem it is trying to solve is the need for the plugins to be able to share a common composite without knowing about each other. In earlier incarnations if the APE I did something similar by having the *hortator* hold an object for others to share, but this ended up making the *hortator* large and complicated. The particular first-use will be for watchers which will be registered with a :ref:`Composite <composite-class>` :ref:`Singleton <ape-documentation-exploring-singletons>`.

Setting Up
----------

The first thing to create is the `singletons` dictionary. I originally thought that it would be a `name`: object mapping but I think now it should be a `name`:{`category`:object} mapping so that categories of objects can share the same singleton. I am also creating a `SingletonEnum` to hold the string names for the types of singleton (the `name` in the previous sentence) so that any code that needs to refer to them can do so using dot-notation.



.. currentmodule:: ape.commoncode.singletons
.. autosummary::
   :toctree: api

   SingletonEnum   

Get Composite
-------------

The Composite Singleton can be retrieved via the ``get_composite`` method. It takes a name to register the composite being retrieved so that multiple composites can be created (e.g. one composite for watchers, one for tests). Because I'm re-using the :ref:`Composite <composite-class>` meant to create the Ape's infrastructure the composite singleton's need to have an exception and error-message passed in. To avoid interfering with the infrastructure's error-handling I'm going to use a :ref:`DontCatchError <dont-catch-error>` by default so that the Composite will crash if any of its components crashes. In the case of threaded components, this won't work, of course, but we'll se how it goes.

.. '

.. currentmodule:: ape.commoncode.singletons
.. autosummary::
   :toctree: api

   get_composite
   


Get FileStorage
---------------

The ``get_filestorage`` function gets a :ref:`FileStorage <file-storage-module>` object. The intention is for each Operator Composite to set the path of the File Storage before creating its components, then each of the plugins can just open a file using the singleton. This creates a little bit of a different case from the composites in that if sub-groups are used they are going to need to copy the original file-storage and change its path (assuming the path will be different, which is the only case that I can think of where sub-groups might be useful).

.. currentmodule:: ape.commoncode.singletons
.. autosummary::
   :toctree: api

   get_filestorage
   


Refresh
-------

The ``refresh`` function clears the ``singletons`` dictionary. It is meant to be called whenever a new operation is created so that the objects from previous operations aren't still being held by the singletons. Since I don't have a use-case for selectively destroying singletons it clears all of them, but you could selectively delete types or categories::

    from ape.commoncode.singletons import singletons, SingletonEnum
    from ape.commoncode.singletons import refresh

    enum = SingletonEnum

    # delete a sub-category called 'test'

    del singletons[enum.composite]['test']

    # delete all the composites

    del singletons[enum.composite]

    # delete all the singletons

    refresh()

.. autosummary::
   :toctree: api

   refresh

