
# python standard library
import logging

# third-party
from hamcrest import assert_that, instance_of, equal_to
from behave import given, when, then
from mock import call, MagicMock, patch

# this package
from tuna.parts.dummy.callclass import CallClass, CallClassConstants
from tuna.parts.dummy.callclass import ARGS, KWARGS


@given("the logging level was set to 'debug'")
def set_debug(context):
    context.call_class = CallClass(level=CallClassConstants.debug_level)
    context.args = (1,2,3)
    context.kwargs = dict(zip('a b c'.split(), range(3)))
    context.logger = MagicMock()
    with patch('logging.Logger.debug', context.logger):
        context.call_class.log_arguments
    return

@when("the CallClass is called")
def call_the_callclass(context):
    context.call_class(*context.args, **context.kwargs)
    return

@then("CallClass will send the arguments to the debug log")
def check_debug_log(context):
    expected = [call(ARGS.format(value=context.args)),
                call(KWARGS.format(value=context.kwargs))]
    assert_that(context.logger.mock_calls, equal_to(expected))
    
    return


@given("the logging level was set to 'info'")
def set_info(context):
    context.call_class = CallClass(level=CallClassConstants.info_level)
    context.args = (4,5,5)
    context.kwargs = dict(zip('a b c'.split(), range(3)))
    context.logger = MagicMock()
    with patch('logging.Logger.info', context.logger):
        context.call_class.log_arguments
    return

@then("CallClass will send the arguments to the info log")
def check_info(context):
    expected = [call(ARGS.format(value=context.args)),
                call(KWARGS.format(value=context.kwargs))]
    assert_that(context.logger.mock_calls, equal_to(expected))
        
    return
