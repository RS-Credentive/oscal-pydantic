import unittest
import random
import string

from ..src.oscal_pydantic.core import datatypes


class TestDatatypes(unittest.TestCase):
    def test_boolean(self):
        true_data = [1, "1", True]
        false_data = [0, "0", False]
        junk_data = [
            "".join(random.sample(string.ascii_letters + string.digits, 1)),
            random.randint(2, 9),
        ]

        # Check the truthy values
        for item in true_data:
            bool_test = datatypes.Boolean(item)
            self.assertTrue(bool_test)

        # Check the falsy values
        for item in false_data:
            bool_test = datatypes.Boolean(item)
            self.assertFalse(bool_test)
