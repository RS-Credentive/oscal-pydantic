import datetime
import json
import uuid

from src.oscal_pydantic import common, core, catalog

# MANDATORY TYPES
title = common.Title("Title")
print(title)

last_modified = common.LastModified(datetime.datetime.now(datetime.timezone.utc))
print(last_modified)

version = common.Version("1.0.4")
print(version)

oscal_version = common.OscalVersion()
print(oscal_version)

metadata = common.Metadata(
    title=title,
    last_modified=last_modified,
    version=version,
    oscal_version=oscal_version,
)

print(metadata.model_dump_json())

prop_name = core.GenericPropertyName("name")
prop_value = core.PropertyValue("marking")
prop_class = core.PropertyClass("Testing-Class")

prop = core.Property(name=prop_name, value=prop_value, property_class=prop_class)

print(prop.model_dump_json())

back_matter = common.BackMatter()

constructed_catalog = catalog.Catalog(
    uuid=core.UUID(),
    metadata=metadata,
    back_matter=back_matter,
)

print(constructed_catalog.model_dump_json())

# try to import the 800-53 catalog
with open(
    "/workspaces/oscal-pydantic/test-data/NIST_SP-800-53_rev5_catalog.json", "r"
) as catalog_file:
    catalog_json = catalog_file.read()

catalog_dict = json.loads(catalog_json)

imported_catalog = catalog.Catalog.model_validate(catalog_dict["catalog"])

print("Hooray!")
