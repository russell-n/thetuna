Feature: Simulated Annealer calls observers.

   As a user 
   I want to be able to use the outcome of the Simulated Annealing optimization with other code
   So that changes to external systems can be made based on the 'optimal' solution.

Background: Setup Annealer
    Given the Simulated Annealer has been built

Scenario: Simulated Annealer without observers

   When we run the Annealear without observers
   Then it should be callable without observers

Scenario: Simulated Annealer with observers

   When the Annealer is run with observers
   Then it should pass the solution to the observers
