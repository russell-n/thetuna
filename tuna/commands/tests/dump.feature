Feature: The output from a command sent to a device is dumped to a file.

Scenario: A non-blocking command is called and the output is sent to a file

    Given a TheDump object is created
    When TheDump object is called
    Then TheDump sends its command to its connection
    And TheDump redirects the command output to storage
