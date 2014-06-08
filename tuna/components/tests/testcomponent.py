
# python standard library
import unittest
import logging
import random

# third-party
from mock import MagicMock

# this package
from optimization.components.component import Component, Composite


class TestComponent(unittest.TestCase):
    def test_constructor(self):
        """
        Does it build correctly?
        """
        # no it's an abstract class
        with self.assertRaises(TypeError):
            component = Component()

        class ConcreteComponent(Component):
            def __init__(self):
                super(ConcreteComponent, self).__init__()
                return
            def __call__(self):
                return
            def check_rep(self):
                return
        c = ConcreteComponent()
        self.assertIsInstance(c.logger, logging.Logger)
        return
# end TestComponent    


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.component1 = MagicMock()
        self.component2 = MagicMock()
        self.component3 = MagicMock()
        self.components = [self.component3,
                                    self.component1,
                                    self.component2,
                                    self.component3]
        self.composite = Composite(self.components)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        components = [MagicMock(), MagicMock()]
        composite = Composite(components=components)
        self.assertEqual(components, composite.components)        
        return

    def test_add(self):
        """
        Does it correctly add the components?
        """
        composite = Composite()
        component1 = MagicMock()
        component2 = MagicMock()
        composite.add(component1)
        composite.add(component2)

        # I don't think the regular implementation allows this
        composite.add(component1)
        self.assertEqual([component1, component2, component1],
                         composite.components)
        return

    def test_remove(self):
        """
        Does it correctly remove the components from the list?
        """
        self.composite.remove(self.component2)
        self.assertEqual([self.component3,
                          self.component1,
                          self.component3],
                          self.composite.components)
        # does it ignore components not in the list?
        self.composite.remove(self.component2)

        # does it remove them in order they were added?
        self.composite.remove(self.component3)
        self.assertEqual([self.component1,
                          self.component3],
                          self.composite.components)
        return

    def test_check_rep(self):
        """
        Does it check all the reps?
        """
        self.composite.check_rep()
        for component in self.components:
            component.check_rep.assert_called_with()
        return

    def test_call(self):
        """
        Does it call all the components?
        """
        self.composite()
        for component in self.components:
            component.assert_called_with()

        with self.assertRaises(TypeError):
            self.composite(5)
        return
# end TestComposite    
