import uuid
import datetime
import json

from oscal_pydantic import (
    catalog,
    assessment_plan,
    assessment_results,
    complete,
    component,
    poam,
    profile,
    ssp,
)


catalog_metadata = catalog.PublicationMetadata(
    title="Common Policy",
    last_modified=catalog.LastModifiedTimestamp.parse_obj(datetime.datetime.now()),
    version=catalog.DocumentVersion.parse_obj("1.0"),
    oscal_version=catalog.OSCALVersion.parse_obj("1.0.4"),
)

catalog = catalog.Catalog(uuid=str(uuid.uuid4()), metadata=catalog_metadata)

print(catalog.json())
