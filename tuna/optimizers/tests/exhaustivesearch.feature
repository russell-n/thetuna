Feature: Exhaustive Search

    As a user
    I want to be able to exhaustively search a grid
    So that I can find the maximum value in it

Scenario: ExhaustiveSearch creation
    Given an ExhaustiveSearch configuration
    When the ExhaustiveSearch is created
    Then the ExhaustiveSearch implements the Component interface

Scenario: ExhaustiveSearch mis-configuration
    Given an invalid ExhaustiveSearch configuration
    When the ExhaustiveSearch.check_rep is called
    Then the ExhaustiveSearch raises a ConfigurationError

Scenario: One Dimensional Grid

    Given a one-dimensional search space is set up
    When the user calls the ExhaustiveSearch
    Then it searches the space along one axis
    And returns the highest value

Scenario: Unbounded one dimensional carries

    Given a one-dimensional search space is set up
    When the bounded flag is not set
    And a candidate that's too big is passed to carry
    Then the candidate is set to the minimum

Scenario: Two-Dimensional Grid Search

    Given a two-dimensional search space is set up
    When the user calls the ExhaustiveSearch
    Then it searches the entire 2D space
    And returns the highest value
    

