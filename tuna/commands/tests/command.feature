Feature: Command execution and data extraction

Background: A command is created 
    Given a command is created with a mocked connection

Scenario: Single data group
    Given the user identified one group in the data expression
    When the command is executed
    Then the call will return a single data-value

Scenario: Multiple data groups
    Given the user identified multiple groups in the data expression
    When the command is executed
    Then the call will return all the groups as data

Scenario: No matches are found
    Given the user creates a data_expression that doesn't match any output
    When the command is executed
    Then the call will return not_available
    And the logger will warn the user

Scenario: Matches are found but no groups 
    Given the user's data_expression doesn't have any groups that match output
    When the command is executed and checked with the output
    Then a TunaError is raised
