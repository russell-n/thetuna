Testing the CheckArguments
==========================

This checks the arguments for the `check` sub-command.

.. autosummary::
   :toctree: api

   TestCheckArguments.test_constructor
   TestCheckArguments.test_configfilenames
   TestCheckArguments.test_modules
   TestCheckArguments.test_both



Testing the Check Strategy
--------------------------

.. autosummary::
   :toctree: api

   TestCheckStrategy.test_constructor
   TestCheckStrategy.test_function
   TestCheckStrategy.test_error_handling

::

    class TestCheckStrategy(unittest.TestCase):
        def setUp(self):
            self.build_ape = MagicMock()
            self.strategy = CheckStrategy()
            
            # monkey patch!
            self.strategy.build_ape = self.build_ape
            return
        
        def test_constructor(self):
            """
            Does it build?
            """
            strategy = CheckStrategy()
            self.assertIsInstance(strategy, BaseStrategy)
            return
    
        def test_function(self):
            """
            Does it execute the strategy correctly?
            """
            configfiles = 'alpha beta gamma'.split()
            ape = MagicMock()
            self.build_ape.return_value = None
            args = MagicMock()
            args.configfiles = configfiles
    
            # ape not buildable (build_ape returned None)
            self.strategy.function(args)
            self.build_ape.assert_called_with(configfiles)
            self.assertEqual(ape.mock_calls, [])
    
            # ape was built
            self.build_ape.return_value = ape
            self.strategy.function(args)
            ape.check_rep.assert_called_with()
            return
    
        def test_error_handling(self):
            """
            Does it catch exceptions?
            """
            self.build_ape.side_effect = Exception("arrrrrgh")
            args = MagicMock()
            self.strategy.function(args)
            return
    
    

