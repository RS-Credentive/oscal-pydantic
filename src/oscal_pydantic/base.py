# Reuseable base classes for core data
from __future__ import annotations

from typing import Annotated
import uuid
from pydantic import BaseModel, RootModel, Field, AwareDatetime, field_validator, constr, AnyUrl


class Title(RootModel[str]):
    root: str = Field(
        description="A name given to the document, which may be used by a tool for display and navigation."
    )


class Published(RootModel[AwareDatetime]):
    root: AwareDatetime = Field(
        description="(Optional) The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included."
    )


class LastModified(RootModel[AwareDatetime]):
    root: AwareDatetime = Field(
        description="The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.",
        serialization_alias="last-modified",
    )


class Version(RootModel[str]):
    root: str = Field(
        description="A string used to distinguish the current version of the document from other previous (and future) versions."
    )


class OscalVersion(RootModel[str]):
    root: Annotated[str, constr(pattern="^1.0.5$")] = Field(
        description="The OSCAL model version the document was authored against. This library currently produces 1.0.5",
        serialization_alias="oscal-version",
        default="1.0.5",
    )


class Token(RootModel[str]):
    root: str = Field(
        description="Non-colonized token type used for various identifiers",
        pattern=r"^([^\W\d]|[:_]){1}[\w\d:\-_]*$",  # "any non-numeric character, _ or :, followed by a sequence of any alphanumeric character, _, :, -, or ."
    )


class Name(RootModel[Token]):
    root: Token = Field(
        description="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object."
    )


class UUID(RootModel[uuid.UUID]):
    root: uuid.UUID = Field(
        description="A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this defined property elsewhere in this or other OSCAL instances. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document.",
        default=uuid.uuid4(),
    )


class NS(RootModel[AnyUrl]):
    root: AnyUrl = Field(
        description="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name."
    )


class Value(RootModel[str]):
    root: str = Field(
        description="Indicates the value of the attribute, characteristic, or quality."
    )


class PropertyClass(RootModel[Token]):
    root: Token = Field(
        description="A textual label that provides a sub-type or characterization of the property's name. This can be used to further distinguish or discriminate between the semantics of multiple properties of the same object with the same name and ns.",
    )


class Remarks(RootModel[str]):
    root: str = Field(description="Additional commentary on the containing object.")


# class Property
class Property(BaseModel):
    name: Name
    uuid: UUID | None = None
    ns: NS | None = None
    value: Value
    property_class: PropertyClass | None = Field(default=None, alias="class")
    remarks: Remarks | None = Field(default=None)
    # TODO START HERE


# class Link


class Revision(BaseModel):
    title: Title | None = Field(default=None)
    published: Published | None = Field(default=None)
    last_modified: LastModified | None = Field(default=None)
    version: Version
    oscal_version: OscalVersion | None = Field(default=None)
    # Property
    # Links
    remarks: Remarks | None = Field(default=None)


class Metadata(BaseModel):
    title: Title
    published: Published | None = Field(default=None)
    last_modified: LastModified
    version: Version
    oscal_version: OscalVersion
