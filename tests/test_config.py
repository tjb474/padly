import unittest
import json

class TestConfigFormat(unittest.TestCase):
    """
    A TestCase class for verifying the format and structure of the configuration data.
    """
    @classmethod
    def setUpClass(cls):
        """
        Load the configuration file once before all tests.
        """
        # Load the configuration file just once for all tests
        config_path = 'config/config.json'
        with open(config_path, 'r') as file:
            cls.config = json.load(file)

    def test_uk_tax_bands_format(self):
        """
        Verify that each tax band in the 'uk_tax_bands' section of the config
        contains the correct keys ('lower', 'upper', 'rate') and that each key has
        the appropriate type (int for 'lower' and 'upper', float for 'rate'). Also,
        check that 'upper' can be None for the highest band.
        """
        tax_bands = self.config.get('uk_tax_bands', [])
        for band in tax_bands:
            # Check existence and type of each key
            self.assertIn('lower', band)
            self.assertIn('upper', band)
            self.assertIn('rate', band)
            self.assertIsInstance(band['lower'], int)
            self.assertTrue(isinstance(band['upper'], int) or band['upper'] is None)
            self.assertIsInstance(band['rate'], float)

            # Additional checks can be added here, e.g., lower < upper, rate within expected range, etc.

    def test_student_loan_plans_format(self):
        """
        Verify that each student loan plan in the 'student_loan_plans' section of the
        config contains the correct keys ('threshold', 'rate') and that each key has
        the appropriate type (int for 'threshold', float for 'rate').
        """
        loan_plans = self.config.get('student_loan_plans', {})
        for plan, details in loan_plans.items():
            # Check that each plan has the expected keys and types
            self.assertIn('threshold', details)
            self.assertIn('rate', details)
            self.assertIsInstance(details['threshold'], int)
            self.assertIsInstance(details['rate'], float)

            # Additional validity checks can be added, e.g., thresholds and rates are positive, etc.

if __name__ == '__main__':
    unittest.main()
