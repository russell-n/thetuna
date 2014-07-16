Feature: CallClass logs calls made to it

Scenario: CallClass logs to the debug log
   Given the logging level was set to 'debug'
   When the CallClass is called
   Then CallClass will send the arguments to the debug log

Scenario: CallClass logs to the info log
   Given the logging level was set to 'info'
   When the CallClass is called
   Then CallClass will send the arguments to the info log
