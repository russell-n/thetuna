Feature: A SummaryQuery runs commnads multiple times and saves a summary statistic for each command

Scenario: A single command is run once and its output is converted to a float
    Given a SummaryQuery has been built with a single command
    When the query is called without arguments
    Then it will store the statistic for the single command

