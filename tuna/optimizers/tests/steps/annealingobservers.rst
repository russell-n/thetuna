Feature: Simulated Annealer calls observers
===========================================
.. literalinclude:: ../annealingobservers.feature
   :language: gherkin



Background: Setup Annealer
--------------------------

::

    @given("the Simulated Annealer has been built")
    def build_annealer(context):
        context.temperatures = MagicMock()
    
        context.tweak = MagicMock(name='tweak')
        context.quality = MagicMock(name='quality')
        context.candidate = MagicMock(name='candidate')
        context.stop_condition = MagicMock(name="stop")
        context.solution_storage = MagicMock(name='storage')
        context.stop_condition.__iter__ = [1]
        context.best = MagicMock('best')
    
        context.annealer = SimulatedAnnealer(temperatures=context.temperatures,
                                             tweak=context.tweak,
                                             quality=context.quality,
                                             candidate=context.candidate,
                                             stop_condition=context.stop_condition,
                                             solution_storage=context.solution_storage)
    



Scenario: Simulated Annealer without observers
----------------------------------------------

::

    @when("we run the Annealear without observers")
    def run_without_observers(context):
        context.annealer()
        return
    
    @then("it should be callable without observers")
    def call_without_observers(context):
        assert_that(context.annealer.solution, equal_to(context.candidate))
        return
    
    


 
Scenario: Simulated Annealer with observers
-------------------------------------------

::

    @when("the Annealer is run with observers")
    def run_with_observers(context):
        observers = MagicMock("observers")
        context.annealer.observers = observers
        context.annealer()
        return
    
    @then("it should pass the solution to the observers")
    def solution_check(context):
        context.annealer.observers.assert_called_with(target=context.candidate)
        return
    

