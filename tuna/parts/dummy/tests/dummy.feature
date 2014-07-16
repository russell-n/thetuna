Feature: DummyClass logs calls made to it
    In order to get a better idea of what the code is doing
    As a developer of tuna-code
    I want a class that can be injected into the runtime to log calls to it

Scenario: DummyClass set up to use debug logging
    Given the DummyClass is created with debug-level logging
    When the DummyClass is called
    Then it will log the arguments to the debug logger


