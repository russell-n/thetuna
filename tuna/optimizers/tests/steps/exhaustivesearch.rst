Feature: Exhaustive Search
==========================



Scenario: One Dimensional Grid
-----------------------------

::

    @given("a one-dimensional search space is set up")
    def one_dimension(context):
        context.quality = MagicMock()
        context.minima = numpy.array([-3])
        context.maxima = numpy.array([10])
        context.increments = numpy.array([1])
        context.search = ExhaustiveSearch(minima=context.minima,
                                          maxima=context.maxima,
                                          increments=context.increments,
                                          quality=context.quality)
        assert_that(context.search.minima, equal_to(context.minima))
        assert_that(context.search.maxima, equal_to(context.maxima))
        assert_that(context.search.increments, equal_to(context.increments))
        assert_that(context.search.quality,
                    equal_to(context.quality))
        return
    
    @when("the user calls the ExhaustiveSearch")
    def search_call(context):
        context.quality.side_effect = lambda x: x[0]
        context.best = context.search()
        return
    
    @then("it searches the space along one axis")
    def one_axis_check(context):
        expected = []
        for coordinate in xrange(context.minima[0],
                                 context.maxima[0]):
            expected.append(call(coordinate+1))
            expected.append(call(coordinate))
            
        assert_that(expected, equal_to(context.quality.method_calls))
        return
    
    @then("returns the highest value")
    def return_maximum_check(context):
        assert_that(context.best, equal_to(context.maxima[-1]))
        return
    
    



Scenario: Bounded one dimensional carries
-----------------------------------------

::

    @when("the bounded flag is set")
    def set_bounded(context):
        context.search.bounded = True
        return
    
    @when("a candidate that's too big is passed to carry")
    def pass_candidate_to_carry(context):
        candidate = context.maxima + numpy.array([2])
        context.candidate = context.search.carry(candidate)
        return
    
    @then("the candidate is set to the maximum")
    def check_maximum(context):
        assert_that(context.candidate, equal_to(context.maxima))
        return
    
    



Scenario: Unbounded one dimensional carries
-------------------------------------------

::

    @when("the bounded flag is not set")
    def unset_flag(context):
        context.search.bounded = False
        return
    
    @then("the candidate is set to the minimum")
    def check_minimum(context):
        assert_that(context.candidate, equal_to(context.minima))
    
    

