Crash Handler
=============

This is a module to help with catching exceptions.



.. _optimization-infrastructure-try-except-decorator:

The try-except Decorator
------------------------

This decorator allows exceptions to be caught and logged, rather than having the interpreter dump the stack-trace to standard-error (it still logs the stack-trace and displays some of the output).

.. currentmodule:: optimization.infrastructure.crash_handler
.. autosummary::
   :toctree: api

   try_except   

This wraps methods, not functions (it uses `self`). `self` must have access to `self.error` (the exception to trap), `self.error_message` a string to put in the title of the error message and `self.logger` a logging instance to send error messages to. Since it is catching exceptions, any method wrapped with this won't raise an error if the exception in self.error is raised by code it is running.

.. superfluous '

I have now added a call to a  `self.close` method after an exception is caught so users of this decorator should have that implemented as well (but it checks to see if the method exists so it won't try and call it if it wasn't implemented).



.. _ape-commoncode-crash-handler-log-error:

The log_error Function
----------------------

.. currentmodule:: optimization.infrastructure.crash_handler
.. autosummary::
   :toctree: api

   log_error

The `log_error` function was created to log the traceback and error messages. It was broken out from the `try_except` decorator so that when the `clean_up` is called the class using the decorator can decide what the error message should be (based on the error that was raised) and call this function directly. If the class has no `clean_up` method, the `try_except` decorator will then log the error itself.   



print_traceback
---------------

This is a function that does pretty much what log_error does but uses print-statements and no formatting so that I can use it in pweave.

::

    import traceback
    import sys
    import os
    
    def print_traceback(error):
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_info = traceback.extract_tb(exc_tb)
        filename, linenum, funcname, source = tb_info[-1]
    
        error_message = "{0}: {1}".format(error.__class__.__name__,
                                                        error)
    
        print "Failed Line: '{0}'".format( source)
        print "In Function: {0}".format(funcname)
        print "In File: {0}".format(os.path.basename(filename))
        print "At Line: {0}".format(linenum)
    



.. autosummary::
   :toctree: api

   print_traceback

