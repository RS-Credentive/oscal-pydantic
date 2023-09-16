import unittest
from oscal_pydantic import catalog

import json


with open(
    "/workspaces/oscal-pydantic/tests/test-data/NIST_SP-800-53_rev5_catalog.json", "r"
) as cat_file:
    test_catalog = cat_file.read()


catalog_dict = json.loads(test_catalog)


class TestCatalog(unittest.TestCase):
    def test_import_known_good(self):
        catalog.Catalog.model_validate(catalog_dict["catalog"])
