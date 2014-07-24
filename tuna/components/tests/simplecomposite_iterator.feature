Feature: The SimpleComposite provides an iterable interface
   As a user
   I want to be able to traverse the SimpleComposite to get the Components
   So that I can do something other than call them without needing to remember the 'components' attribute is a list

Scenario: A SimpleComposite is traversed by a user
   Given a SimpleComposite is built with components
   When a user iterates over it
   Then it yields its components
