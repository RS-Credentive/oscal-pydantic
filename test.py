import uuid
import datetime
import json

from oscal_pydantic import complete


catalog_metadata = complete.PublicationMetadata(
    title="Common Policy",
    last_modified=complete.LastModifiedTimestamp.parse_obj(datetime.datetime.now()),
    version=complete.DocumentVersion.parse_obj("1.0"),
    oscal_version=complete.OSCALVersion.parse_obj("1.0.4"),
)

catalog = complete.Catalog(uuid=str(uuid.uuid4), metadata=catalog_metadata)

print(catalog)
