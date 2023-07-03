import datetime

from src.oscal_pydantic import common, core

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

prop_name = core.Name("name")
prop_value = core.Value("Value")
prop_class = core.PropertyClass("Testing-Class")

prop = core.Property(name=prop_name, value=prop_value, property_class=prop_class)

print(prop.model_dump_json(by_alias=True, exclude_none=True))
