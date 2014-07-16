Feature: DummyClass logs calls made to it
=========================================



.. literalinclude:: ../dummy.feature
   :language: gherkin

Scenario: DummyClass set up to use debug logging
------------------------------------------------

::

    @given("the DummyClass is created with debug-level logging")
    def set_debug(context):
        context.dummy = DummyClass(level=DummyConstants.debug_level)
        return
    
    @when("the DummyClass is called")
    def call_dummy(context):
        return
    
    @then("it will log the arguments to the debug logger")
    def check_debug(context):
        expected = [call(CALLED.format(context.dummy.identifier))]
        return
    

