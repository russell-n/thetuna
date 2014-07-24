Feature: The SimpleComposite provides an iterable interface
===========================================================

.. literalinclude:: ../simplecomposite_iterator.feature
   :language: gherkin


   
Scenario: A SimpleComposite is traversed by a user
--------------------------------------------------

::

    @given("a SimpleComposite is built with components")
    def build_composite(context):
        components = [MagicMock(name='component {0}'.format(count))
                      for count in xrange(1, 10)]
            
        context.composite =SimpleComposite(components)
        return
    
    @when("a user iterates over it")
    def traverse_composite(context):
        context.expected = [component for component in context.composite]
        return
    
    @then("it yields its components")
    def check_components(context):
        assert_that(context.expected,
                    is_(equal_to(context.composite.components)))
        return
    

