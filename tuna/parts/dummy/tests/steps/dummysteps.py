
# third-party
from behave import given, when, then
from hamcrest import assert_that, equal_to
from mock import call, MagicMock, patch

# this package
from tuna.parts.dummy.dummy import CALLED, ARGS, KWARGS, CALLED_ON
from tuna.parts.dummy.dummy import DummyClass
from tuna.parts.dummy.dummy import DummyConstants


@given('the DummyClass is created with "{level}" level logging')
def set_debug(context, level):
    context.args = tuple(range(4))
    context.kwargs = dict(zip('a o e'.split(), range(3)))
    context.dummy = DummyClass(level=level)
    context.log = MagicMock()
    with patch('logging.Logger.{0}'.format(level), context.log):
        context.dummy.log
    return

@when("the DummyClass is called")
def call_dummy(context):
    context.dummy(*context.args, **context.kwargs)
    return

@then('it will log the call and arguments to the "{level}" logger')
def check_debug(context, level):
    expected = [call(CALLED.format(thing=context.dummy.identifier)),
                call(ARGS.format(value=context.args)),
                call(KWARGS.format(value=context.kwargs))]
    assert_that(context.dummy.log.mock_calls, equal_to(expected))
    return


@when("the DummyClass getattr is called")
def gettattr_call(context):
    context.attribute = "aaoeusnth"
    getattr(context.dummy, context.attribute)
    return

@then('it will log the arguments to the "{level}" logger')
def check_level_arguments(context, level):
    expected = [call(CALLED_ON.format(attribute=context.attribute,
                     thing=context.dummy.identifier))]
    assert_that(context.log.mock_calls, equal_to(expected))
    return
