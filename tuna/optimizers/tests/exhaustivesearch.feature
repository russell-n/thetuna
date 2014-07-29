Feature: Exhaustive Search

    As a user
    I want to be able to exhaustively search a grid
    So that I can find the maximum value in it

Scenario: One Dimensional Grid

    Given a one-dimensional search space is set up
    When the user calls the ExhaustiveSearch
    Then it searches the space along one axis
    And returns the highest value

Scenario: Bounded one dimensional carries

    Given a one-dimensional search space is set up
    When the bounded flag is set
    And a candidate that's too big is passed to carry
    Then the candidate is set to the maximum 

Scenario: Unbounded one dimensional carries

    Given a one-dimensional search space is set up
    When the bounded flag is not set
    And a candidate that's too big is passed to carry
    Then the candidate is set to the minimum
