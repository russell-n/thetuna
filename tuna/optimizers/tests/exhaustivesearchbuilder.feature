Feature: A builder of ExhaustiveSearch objects
    As a developer
    I want a builder of ExhaustiveSearch objects
    So that I can build a plugin that uses it

Background: Configuration setup
    Given a configuration with ExhaustiveSearch options

Scenario: A configuration file is used to build an ExhaustiveSearch
    When the ExhaustiveSearchBuilder product is retrieved
    Then the ExhaustiveSearchBuilder product is an ExhaustiveSearch

Scenario: A single increment is given with multiple minima and maxima 

    Given a configuration with one increment and multiple minima and maxima
    When the ExhaustiveSearchBuilder product is retrieved
    Then the ExhaustiveSearch has an increment of the same size as the minima and maxima

Scenario: Mismatched minima and maxima sizes are given

    Given a configuration with minima and maxima of different sizes
    When the ExhaustiveSearchBuilder product is retrieved
    Then a ConfigurationError is raised
