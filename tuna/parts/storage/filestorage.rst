File Storage
============

.. _file-storage-module::

This is a module for classes that implement a file-like interface to disk-files but also add some extra features meant to make them easier to use within the TUNA.



.. _file-storage-model:

FileStorage Model
-----------------

Since the ultimate model for all storage classes is ``__builtin__.file`` (see: :ref:`exploring files <exploring-files>` for the API and some notes), this class will implement all the non-optional methods and attributes. In addition it will inherit from the :ref:`Composite <composite-class>` in order to allow non-homogeneous storage (e.g. stdout and disk -- the equivalent of the unix `tee`).

.. uml::

   FileStorage : FileStorage __init__(path, [,mode])
   FileStorage : open(name[, mode])
   FileStorage : close()
   FileStorage : flush()
   FileStorage : String read()
   FileStorage : String readline()
   FileStorage : List readlines()
   FileStorage : write(text)
   FileStorage : writeline(text)
   FileStorage : writelines(list)
   FileStorage : closed
   FileStorage : mode
   FileStorage : name
   FileStorage : path
   FileStorage : add(component)
   FileStorage : components
   FileStorage : __enter__
   FileStorage : __exit__
   FileStorage : __iter__

.. _file-storage-extras:

Extras
------

Although the built-in ``file`` is the model for the ``FileStorage``, it wouldn't make much sense to replicate it exactly. The main impetus for creating this (besides keeping an eye on non-disk output in the future) is to have something that can keep track of extra persistent data -- in particular:

   * Sub-folders 
   * Existing files with redundant names (and how to handle them)
   * Time-stamps
   * Locks

.. superfluous '   

.. _file-storage-sub-folders:

Sub-Folders
-----------

In order to help tame the explosion of files that can often happen from the repeated execution of code that collects data the FileStorage will accept a path which it will then prepend to any file-name when it is opened. If the sub-folder does not exist it will be created.

::

    if IN_PWEAVE:
        example_path = 'aoeu/snth'
        example_file = 'umma.gumma'
        
        
        # this is the part that should be part of the path property
        if not os.path.isdir(example_path):
            os.makedirs(example_path)
        for name in os.listdir('aoeu'):
            print name
        
        # this will be run multiple times, remove the example so it gets started fresh
        if os.path.isdir(example_path):
            shutil.rmtree(example_path)    
    

::

    snth
    



.. _file-storage-redundant-files:

Redundant Files
---------------

It often happens that data-collecting code will be run multiple times. The two ways proposed to avoid inadvertently overriding files are:

     * Appending count-numbers (e.g. a_0.txt, a_1.txt)
     * Adding Timestamps

The first scheme is more easily generalizable, while the second adds more useful information. It will therefore be assumed that both will be implemented and the increment scheme will only come into effect in the cases where the two files of the same name have been requested in too short a time-interval for the timestamps to differentiate them.

Adding Timestamps
~~~~~~~~~~~~~~~~~

The timestamp will be added using string formatting -- it will look for a `timestamp` keyword:

::

    if IN_PWEAVE:
        name = "test_{timestamp}.csv"
        print name.format(timestamp=datetime.datetime.now().strftime(FILE_TIMESTAMP))
    

::

    test_2014_07_31_01:33:49_PM.csv
    



Appending Increments
~~~~~~~~~~~~~~~~~~~~

In the event that no `timestamp` formatting was added or the files were created less than a second apart, the `FileStorage` will add a count to the end of the base file-name prefix.

Side Effects
~~~~~~~~~~~~

Because the name is being made to never match an existing file, the FileStorage can only write files, not read them. A separate file-reader needs to be built if that's something needed.

.. superfluous '

::

    if IN_PWEAVE:
        # what's here?
        for name in (name for name in os.listdir(os.getcwd()) if name.endswith('txt')):
            print name
        
        name = "innagaddadavida.txt"
        path = os.getcwd()
        full_name = os.path.join(path, name)
        if os.path.exists(full_name):
            base, extension = os.path.splitext(name)
        
            digit = r'\d'
            one_or_more = '+'
            underscore = '_'
        
            suffix = underscore + digit + one_or_more
            expression = r"{b}{s}{e}".format(b=base,
                                              s=suffix,
                                                e=extension)
            regex = re.compile(expression)
            count = sum(1 for name in os.listdir(path) if regex.match(name))
            count = str(count + 1).zfill(4)
            name = "{b}_{c}{e}".format(b=base, c=count, e=extension)
        
        print name            
    

::

    innagaddadavida.txt
    




.. _file-storage-api:

FileStorage API
---------------

.. module:: tuna.parts.storage.filestorage
.. autosummary::
   :toctree: api

   FileStorage
   FileStorage.path
   FileStorage.safe_name
   FileStorage.open
   FileStorage.close
   FileStorage.write
   FileStorage.writeline
   FileStorage.writelines

FileStorage Definition
----------------------

Constructor
~~~~~~~~~~~

The constructor takes two parameters:

   * path
   * timestamp

The ``path`` is the main reason for using the ``FileStorage`` -- by keeping it persistent it frees the users of the ``FileStorage`` from having to know about sub-folders. The ``timestamp`` is a `strftime` string-format. The default is stored in the global-space of this module as a constant called ``FILE_TIMESTAMP``.

The ``open`` Method
~~~~~~~~~~~~~~~~~~~

The ``open`` method is where things get kind of different from a regular file (and may not be a good idea if examined too closely). In order to preserve the path a copy of the ``FileStorage`` is created and a new opened-file is added to it before returning the copy.

Path:

   #. Append an integer if needed (or asked for) to requested filename to prevent over-writing an existing file with the same name
   #. Create a copy of the FileStorage
   #. Open a writeable file-object using the (possibly fixed) filename
   #. Set the FileStorage copy's ``file`` attribute to the opened file
   #. Set the mode for the FileStorage copy 
   #. Set the `closed` attribute of the copy to False
   #. Return the new FileStorage copy  

