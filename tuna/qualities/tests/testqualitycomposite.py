
# python standard library
import unittest
import random

# third-party
from mock import MagicMock

# this package
from optimization.qualities.qualitycomposite import QualityComposite


class TestQualityComposite(unittest.TestCase):
    def setUp(self):
        self.component = MagicMock()
        self.component2 = MagicMock()
        self.components = [self.component, self.component2]     
        self.composite = QualityComposite(components=self.components)
        return   

    def test_call(self):
        # Normally I wouldn't add arguments
        # but the optimizer needs it
        argument = random.randrange(100)
        self.composite(argument)
        for component in self.components:
            component.assert_called_with(argument)

        argument2 = random.randrange(30)
        expected = random.randrange(100)
        self.component.return_value = expected
        self.component2.return_value = None
        
        output = self.composite(argument2, umma=argument)        

        for component in self.components:
            component.assert_called_with(argument2, umma=argument)
        self.assertEqual(expected, output)
        return
