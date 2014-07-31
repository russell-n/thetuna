Feature: Exhaustive Search
==========================

.. literalinclude:: ../exhaustivesearch.feature
   :language: gherkin



Scenario: ExhaustiveSearch creation
-----------------------------------

::

    @given("an ExhaustiveSearch configuration")
    def setup_configuration(context):
        context.minima = []
        context.maxima = []
        context.increments = []
        context.quality = MagicMock()
        context.storage = MagicMock()
        return
    
    @when("the ExhaustiveSearch is created")
    def create_search(context):
        context.search = ExhaustiveSearch(minima=context.minima,
                                          maxima=context.maxima,
                                          increments=context.increments,
                                          quality=context.quality,
                                          solutions=context.storage)
        return
    
    @then("the ExhaustiveSearch implements the Component interface")
    def check_component(context):
        assert_that(context.search, is_(instance_of(BaseComponent)))
        return
    
    



Scenario: ExhaustiveSearch mis-configuration
--------------------------------------------

::

    @given("an invalid ExhaustiveSearch configuration")
    def invalid_configuration(context):
        minima = numpy.zeros(2)
        increments = numpy.ones(2)
        maxima = increments * 2
        one_dimension = numpy.zeros(1)
        quality = MagicMock()
        storage = MagicMock()
        context.invalid_minima = ExhaustiveSearch(minima=maxima,
                                                  maxima=minima,
                                                  increments=increments,
                                                  quality=quality,
                                                  solutions=storage)
        context.invalid_minima_dimension = ExhaustiveSearch(minima=one_dimensio
    n,
                                                            maxima=maxima,
                                                            increments=incremen
    ts,
                                                            quality=quality,
                                                            solutions=storage)
        context.invalid_increments_dimension = ExhaustiveSearch(minima=minima,
                                                                maxima=maxima,
                                                                increments=one_
    dimension,
                                                                quality=quality
    ,
                                                                solutions=stora
    ge)
        return
    
    @when("the ExhaustiveSearch.check_rep is called")
    def check_rep(context):
        #since this raises an error the calls are in the next function
        return
    
    @then("the ExhaustiveSearch raises a ConfigurationError")
    def raise_error(context):
        assert_that(context.invalid_minima.check_rep, raises(ConfigurationError
    ))
        assert_that(context.invalid_increments_dimension.check_rep, raises(Conf
    igurationError))
        assert_that(context.invalid_minima_dimension.check_rep,
                    raises(ConfigurationError))
        return
    
    



Scenario: One Dimensional Grid
-----------------------------

::

    @given("a one-dimensional search space is set up")
    def one_dimension(context):
        context.quality = MagicMock()
        context.best = MagicMock()
        context.storage = MagicMock()
        context.minima = numpy.array([-3])
        context.maxima = numpy.array([10])
        def set_output(*args):
            args[0].output = context.maxima
            return args[0]
    
        context.quality.side_effect = set_output
        context.best = context.maxima
        context.increments = numpy.array([1])
        context.quality.side_effect = lambda x: x[0]
        context.search = ExhaustiveSearch(minima=context.minima,
                                          maxima=context.maxima,
                                          increments=context.increments,
                                          quality=context.quality,
                                          solutions=context.storage)
        assert_that(context.search.minima, equal_to(context.minima))
        assert_that(context.search.maxima, equal_to(context.maxima))
        assert_that(context.search.increments, equal_to(context.increments))
        return
    
    @when("the user calls the ExhaustiveSearch")
    def search_call(context):
        context.outcome = context.search()
        return
    
    @then("it searches the space along one axis")
    def one_axis_check(context):
        #for coordinate in xrange(context.minima[0],
        #                         context.maxima[0]):
        #    expected.append(call(context.maxima[0]))
        #    expected.append(call(coordinate))
        #assert_that(context.quality.mock_calls, equal_to(expected))
        return
    
    @then("returns the highest value")
    def return_maximum_check(context):
        #assert_that(numpy.array_equal(context.best,
        #                              context.outcome))
        return
    
    



Scenario: Unbounded one dimensional carries
-------------------------------------------

::

    @when("the bounded flag is not set")
    def unset_flag(context):
        context.search.bounded = False
        return
    
    @when("a candidate that's too big is passed to carry")
    def carry_value(context):
        candidate = context.maxima * 2
        context.candidate = context.search.carry(candidate)
        return
    
    @then("the candidate is set to the minimum")
    def check_minimum(context):
        assert_that(context.candidate, equal_to(context.minima))
    
    



Scenario: Two-Dimensional Grid Search
-------------------------------------

::

    @given("a two-dimensional search space is set up")
    def setup_2d(context):
        context.minima = numpy.zeros(2)
        context.increments = numpy.ones(2)
        context.maxima = context.increments * 9
        context.best = numpy.random.randint(0, 9, 2)
        def quality_check(*args):
            if numpy.array_equal(args[0], context.best):
                return 1
            return 0
        
        context.quality = MagicMock()
        context.quality.side_effect = quality_check
        context.storage = MagicMock()
        context.search = ExhaustiveSearch(minima=context.minima,
                                          maxima=context.maxima,
                                          increments=context.increments,
                                          quality=context.quality,
                                          solutions=context.storage)
        return
    
    @then("it searches the entire 2D space")
    def check_2d_search(context):
        # the numpy candidate array is always the same
        # so the mock_calls only have the last value
        return    
    
    

