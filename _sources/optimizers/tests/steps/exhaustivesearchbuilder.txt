Feature: A builder of ExhaustiveSearch objects
==============================================


.. literalinclude:: ../exhaustivesearchbuilder.feature
   :language: gherkin

Scenario: A configuration file is used to build an ExhaustiveSearch
-------------------------------------------------------------------

::

    @given("a configuration with ExhaustiveSearch options")
    def setup_configuration(context):
        context.configuration = MagicMock()
        context.observers = MagicMock()
        context.kwargs = {}
        context.kwargs[ExhaustiveSearchConstants.minima_option] = range(4)
        context.kwargs[ExhaustiveSearchConstants.maxima_option] = range(4)
        context.kwargs[ExhaustiveSearchConstants.increments_option] = range(4)
        context.kwargs[ExhaustiveSearchConstants.datatype_option] = 'int'
        context.quality = MagicMock()
        context.solution_storage = MagicMock()
        def get(**kwargs):
            return context.kwargs[kwargs['option']]
    
        context.configuration.get_list.side_effect = get
        context.configuration.get.side_effect = get
    
    @when("the ExhaustiveSearchBuilder product is retrieved")
    def build_product(context):
        context.section_header = 'gridsearch'
        context.builder = ExhaustiveSearchBuilder(configuration=context.configu
    ration,
                                                  section_header=context.sectio
    n_header,
                                                  quality=context.quality,
                                                  observers=context.observers,
                                                  solution_storage=context.solu
    tion_storage)
        return
    
    @then("the ExhaustiveSearchBuilder product is an ExhaustiveSearch")
    def check_product(context):
        assert_that(context.configuration, is_(context.builder.configuration))
        assert_that(context.section_header, equal_to(context.builder.section_he
    ader))
        assert_that(context.builder.product, instance_of(ExhaustiveSearch))
        return
    
    



Scenario: A single increment is given with multiple minima and maxima
---------------------------------------------------------------------

::

    @given("a configuration with one increment and multiple minima and maxima")
    
    def setup_configuration(context):
        context.kwargs[ExhaustiveSearchConstants.increments_option] = [1]
        return
    
    @then("the ExhaustiveSearch has an increment of the same size as the minima
     and maxima")
    def check_increment(context):
        expected = numpy.ones(4)
        assert_that(numpy.array_equal(context.builder.product.increments,
                                      expected))
        return
    
    



Scenario: Mismatched minima and maxima sizes are given
------------------------------------------------------

::

    @given("a configuration with minima and maxima of different sizes")
    def mismatched_minima_maxima(context):
        context.kwargs[ExhaustiveSearchConstants.minima_option] = range(6)
        context.kwargs[ExhaustiveSearchConstants.maxima_option] = range(4)
        return
    
    @then("a ConfigurationError is raised")
    def check_error(context):
        return
    
    

