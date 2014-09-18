
# third-party
from behave import given, when, then
from mock import MagicMock

# this package
from tuna.commands.query import SummaryQuery


@given("a SummaryQuery has been built with a single command")
def single_command(context):
    context.command = MagicMock()
    context.storage = MagicMock()
    context.writer = MagicMock()
    context.output_file = MagicMock()
    context.commands = {'tuna': context.command}
    context.query = SummaryQuery(storage=context.storage,
                                 output_filename="test.csv",
                                 fields = ["tuna"],
                                 commands=context.commands)
    context.query._output_file = context.output_file
    context.query._writer = context.writer
    return

@when("the query is called without arguments")
def no_arguments_call(context):
    context.query()
    return

@then("it will store the statistic for the single command")
def single_statistic(context):
    return
