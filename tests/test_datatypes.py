import random
import string
import unittest
from pydantic import ValidationError

from oscal_pydantic.core import datatypes


class TestDatatypes(unittest.TestCase):
    def test_boolean(self):
        # Check the truthy values
        true_data = [1, "1", True]
        for item in true_data:
            bool_test = datatypes.OscalBool(item)
            self.assertTrue(bool_test)

        # Check the falsy values
        false_data = [0, "0", False]
        for item in false_data:
            bool_test = datatypes.OscalBool(item)
            self.assertFalse(bool_test)

        # junk_data = [
        #     "".join(random.sample(string.ascii_letters + string.digits, 1)),
        #     random.randint(2, 9),
        # ]

        # Check the junk values
        # for item in junk_data:
        #     self.assertRaises(ValidationError, datatypes.OscalBool(item))


if __name__ == "__main__":
    unittest.main()
