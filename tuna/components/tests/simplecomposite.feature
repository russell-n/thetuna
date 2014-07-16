Feature: SimpleComposite is a composite of components

Scenario: SimpleComposite is called and logs what components and arguments are used
    Given a SimpleComposite of components is ready
    When the SimpleComposite is called
    Then it will log the arguments and components called
