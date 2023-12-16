from oscal_pydantic import document, catalog
from pathlib import Path
import pytest

RESOURCES_PATH = Path(__file__).parent.joinpath("resources")


class TestImport:
    def test_import_nested_part(self):
        with open(RESOURCES_PATH.joinpath(Path("nested_part.json"))) as part_file:
            part_bytes = part_file.read()
        test_part = catalog.BasePart.model_validate_json(part_bytes)

        assert isinstance(
            catalog.StatementItemPart.model_validate(test_part.model_dump()),
            catalog.StatementItemPart,
        )

    def test_import_invalid_nested_part(self):
        with open(
            RESOURCES_PATH.joinpath(Path("invalid_nested_part.json"))
        ) as part_file:
            part_bytes = part_file.read()

        with pytest.raises(ValueError):
            catalog.StatementItemPart.model_validate_json(part_bytes)

    def test_import_statement_part(self):
        with open(RESOURCES_PATH.joinpath(Path("statement_part.json"))) as part_file:
            part_bytes = part_file.read()
        test_part = catalog.StatementPart.model_validate_json(part_bytes)
        assert isinstance(test_part, catalog.StatementPart)

    def test_import_catalog(self):
        with open(
            RESOURCES_PATH.joinpath(Path("NIST_SP-800-53_rev5_catalog.json"))
        ) as catalog_file:
            catalog_bytes = catalog_file.read()
        test_catalog = document.Document.model_validate_json(catalog_bytes)
        assert isinstance(test_catalog, document.Document)
