
# third-party
from behave import given, when, then
from mock import call

# this package
from tuna.parts.dummy.dummy import CALLED
from tuna.parts.dummy.dummy import DummyClass
from tuna.parts.dummy.dummy import DummyConstants


@given("the DummyClass is created with debug-level logging")
def set_debug(context):
    context.dummy = DummyClass(level=DummyConstants.debug_level)
    return

@when("the DummyClass is called")
def call_dummy(context):
    return

@then("it will log the arguments to the debug logger")
def check_debug(context):
    expected = [call(CALLED.format(context.dummy.identifier))]
    return
