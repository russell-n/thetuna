Feature: DummyClass logs calls made to it
    In order to get a better idea of what the code is doing
    As a developer of tuna-code
    I want a class that can be injected into the runtime to log calls to it

Scenario: DummyClass set up to use debug logging and called
    Given the DummyClass is created with "debug" level logging
    When the DummyClass is called
    Then it will log the call and arguments to the "debug" logger

Scenario: DummyClass set up to use debug logging and getattr called
    Given the DummyClass is created with "debug" level logging
    When the DummyClass getattr is called
    Then it will log the arguments to the "debug" logger


Scenario: DummyClass set up to use info logging and called
    Given the DummyClass is created with "info" level logging
    When the DummyClass is called
    Then it will log the call and arguments to the "info" logger

Scenario: DummyClass set up to use info logging and getattr called
    Given the DummyClass is created with "info" level logging
    When the DummyClass getattr is called
    Then it will log the arguments to the "info" logger



