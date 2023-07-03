# Reuseable base classes for core data types
from __future__ import annotations

import uuid
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    AnyUrl,
)


class UUID(RootModel[uuid.UUID]):
    # TODO: Should there be a class that will auto generate a UUID (like this one), and a separate class that can only reference an existing UUID? (see location-uuid)
    root: uuid.UUID = Field(
        description="A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this defined property elsewhere in this or other OSCAL instances. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document.",
        default=uuid.uuid4(),
    )


class Token(RootModel[str]):
    root: str = Field(
        description="Non-colonized token type used for various identifiers",
        pattern=r"^([^\W\d]|[:_]){1}[\w\d:\-_]*$",  # "any non-numeric character, _ or :, followed by a sequence of any alphanumeric character, _, :, -, or ."
    )


class MarkupLine(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line"
        # TODO: validate that the text is HTML or MD with only the permitted tags
    )


class MarkupMultiline(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-multiline"
        # TODO: validate that the text is HTML or MD with only the permitted tags
    )


class Relation(RootModel[Token]):
    root: Token = Field(
        description="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose."
    )


class Link(BaseModel):
    href: AnyUrl = Field(description="A reference to a local or remote resource")
    rel: Relation | None = Field(default=None)
    media_type: str | None = Field(
        description="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.",
        default=None,
        alias="media-type",
    )
    resource_fragment: str | None = Field(
        description="In case where the href points to a back-matter/resource, this value will indicate the URI fragment to append to any rlink associated with the resource. This value MUST be URI encoded.",
        default=None,
    )
    text: MarkupLine | None = Field(default=None)


class Name(RootModel[Token]):
    root: Token = Field(
        description="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object."
    )


class NS(RootModel[AnyUrl]):
    root: AnyUrl = Field(
        description="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name."
    )


class Value(RootModel[str]):
    root: str


class PropertyClass(RootModel[Token]):
    root: Token = Field(
        description="A textual label that provides a sub-type or characterization of the property's name. This can be used to further distinguish or discriminate between the semantics of multiple properties of the same object with the same name and ns.",
    )


class Group(RootModel[Token]):
    root: Token = Field(
        description="An identifier for relating distinct sets of properties."
    )


class Remarks(RootModel[str]):
    root: str = Field(description="Additional commentary on the containing object.")


class Property(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Name
    uuid: UUID | None = None
    ns: NS | None = None
    value: Value
    property_class: PropertyClass | None = Field(
        default=None,
        alias="class",
    )
    group: Group | None = Field(default=None)
    remarks: Remarks | None = Field(default=None)
