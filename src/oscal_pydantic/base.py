# Reuseable base classes for core data
from __future__ import annotations

from typing import Annotated
from enum import Enum
import uuid
from pydantic import (
    BaseModel,
    RootModel,
    Field,
    AwareDatetime,
    constr,
    AnyUrl,
    EmailStr,
)


class MarkupLine(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line"
    )


class MarkupMultiline(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-multiline"
    )


class Title(RootModel[MarkupLine]):
    root: MarkupLine = Field(
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
    # TODO: Should there be a class that will auto generate a UUID (like this one), and a separate class that can only reference an existing UUID? (see location-uuid)
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


class Group(RootModel[Token]):
    root: Token = Field(
        description="An identifier for relating distinct sets of properties."
    )


class Remarks(RootModel[str]):
    root: str = Field(description="Additional commentary on the containing object.")


class Property(BaseModel):
    name: Name
    uuid: UUID | None = None
    ns: NS | None = None
    value: Value
    property_class: PropertyClass | None = Field(default=None, alias="class")
    group: Group | None = Field(default=None)
    remarks: Remarks | None = Field(default=None)


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


class Revision(BaseModel):
    title: Title | None = Field(default=None)
    published: Published | None = Field(default=None)
    last_modified: LastModified | None = Field(default=None)
    version: Version
    oscal_version: OscalVersion | None = Field(default=None)
    prop: list[Property] | None = Field(default=None)
    link: list[Link] | None = Field(default=None)
    remarks: Remarks | None = Field(default=None)


class Scheme(RootModel[AnyUrl]):
    root: AnyUrl = Field(
        description="Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters."
    )


class Identifier(RootModel[str]):
    root: str = Field(
        description="A document identifier provides a globally unique identifier with a cross-instance scope that is used for a group of documents that are to be treated as different versions, representations or digital surrogates of the same document."
    )


class DocumentID(BaseModel):
    scheme: Scheme | None = Field(default=None)
    identifier: Identifier


class Role(BaseModel):
    id: Identifier = Field(description="A unique identifier for the role.")
    title: MarkupLine = Field(
        description="A name given to the role, which may be used by a tool for display and navigation."
    )
    short_name: str | None = Field(
        default=None,
        description="A short common name, abbreviation, or acronym for the role.",
    )
    description: MarkupMultiline | None = Field(
        default=None,
        description="A summary of the role's purpose and associated responsibilities.",
    )
    props: list[Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    remarks: Remarks | None = Field(default=None)


class Address(BaseModel):
    type: Token | None = Field(
        default=None, description="Indicates the type of address."
    )
    addr_lines: list[str] | None = Field(
        default=None,
        description="List of strings representing an address",
        alias="addr-lines",
    )
    city: str | None = Field(
        default=None,
        description="City, town or geographical region for the mailing address.",
    )
    state: str | None = Field(
        default=None,
        description="State, province or analogous geographical region for a mailing address.",
    )
    postal_code: str | None = Field(
        default=None,
        description="Postal or ZIP code for mailing address.",
        alias="postal-code",
    )
    country: str | None = Field(
        default=None,
        description="The ISO 3166-1 alpha-2 country code for the mailing address.",
        pattern="[A-Z]{2}",
    )


class TelephoneNumber(BaseModel):
    type: str | None = Field(
        default=None,
        description="Indicates the type of phone number. The value may be locally defined, or one of the following: home: A home phone number; office: An office phone number; mobile: A mobile phone number.",
    )
    number: str | None = Field(
        default=None,
        description="A telephone service number as defined by ITU-T E.164.",
        pattern="^[0-9]{3}[0-9]{1,12}$",
    )


class Location(BaseModel):
    uuid: UUID = Field(description="A unique ID for the location, for reference.")
    title: MarkupLine | None = Field(
        default=None,
        description="A name given to the location, which may be used by a tool for display and navigation.",
    )
    address: Address | None = Field(
        default=None,
        description="A postal address for the location.",
    )
    email_addresses: list[EmailStr] | None = Field(
        default=None,
        description="List of email addresses as defined by RFC 5322 Section 3.4.1.",
        alias="email-address",
    )
    telephone_number: list[TelephoneNumber] | None = Field(
        default=None,
        description="A list of telephone service numbers as defined by ITU-T E.164.",
        alias="telephone-number",
    )
    urls: list[AnyUrl] | None = Field(
        default=None,
        description="A list of uniform resource locators (URLs) for a web site or other resource associated with the location.",
    )
    props: list[Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    remarks: MarkupMultiline | None = Field(
        default=None, description="Additional commentary about the containing object."
    )


class PartyTypeEnum(str, Enum):
    person = "person"
    organization = "organization"


class ExternalID(BaseModel):
    scheme: AnyUrl = Field(description="Indicates the type of external identifier.")
    id: str | None = Field(
        default=None,
        description="An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID)",
    )


class Party(BaseModel):
    uuid: UUID = Field(description="A unique identifier for the party.")
    type: PartyTypeEnum = Field(
        description="A category describing the kind of party the object describes."
    )
    name: str | None = Field(
        default=None,
        description="The full name of the party. This is typically the legal name associated with the party.",
    )
    short_name: str | None = Field(
        default=None,
        description="A short common name, abbreviation, or acronym for the party.",
        alias="short-name",
    )
    external_ids: list[ExternalID] | None = Field(default=None, alias="external-ids")
    props: list[Property] | None = Field(default=None)
    links: list[Link] | None = Field(default=None)
    email_addresses: list[EmailStr] | None = Field(
        default=None,
        description="A list of email addresses as defined by RFC 5322 Section 3.4.1. This is a contact email associated with the party.",
        alias="email-addresses",
    )
    telephone_numbers: list[TelephoneNumber] | None = Field(
        default=None,
        description="Contact number by telephone",
        alias="telephone-numbers",
    )
    addresses: list[Address] | None = Field(
        default=None, description="A postal address for the location."
    )
    location_uuids: list[UUID] | None = Field(
        default=None,
        description="A machine-oriented identifier reference to a location defined in the metadata section of this or another OSCAL instance. The UUID of the location in the source OSCAL instance is sufficient to reference the data item locally or globally (e.g., in an imported OSCAL instance).",
        alias="location-uuids",
    )
    member_of_organizations: list[UUID] | None = Field(
        default=None,
        description="A machine-oriented identifier reference to another party (person or organization) that this subject is associated with. The UUID of the party in the source OSCAL instance is sufficient to reference the data item locally or globally (e.g., in an imported OSCAL instance).",
        alias="member-of-organizations",
    )
    remarks: MarkupMultiline | None = Field(
        default=None, description="Additional commentary on the containing object."
    )


class Metadata(BaseModel):
    title: Title
    published: Published | None = Field(default=None)
    last_modified: LastModified
    version: Version
    oscal_version: OscalVersion
    revisions: list[Revision] | None = Field(
        description="An entry in a sequential list of revisions to the containing document, expected to be in reverse chronological order (i.e. latest first).",
        default=None,
    )
    document_ids: list[DocumentID] | None = Field(
        default=None,
        alias="document-ids",
        description="A document identifier qualified by an identifier scheme.",
    )
    props: list[Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    roles: list[Role] | None = Field(
        default=None,
        description="Defines a function, which might be assigned to a party in a specific situation.",
    )
    locations: list[Location] | None = Field(
        default=None,
        description="A physical point of presence, which may be associated with people, organizations, or other concepts within the current or linked OSCAL document.",
    )
    parties: list[Party] | None = Field(
        default=None,
        description="A responsible entity which is either a person or an organization.",
    )


class Parameter(BaseModel):
    id: Token = Field(
        description="A human-oriented, locally unique identifier with cross-instance scope that can be used to reference this defined parameter elsewhere in this or other OSCAL instances. When referenced from another OSCAL instance, this identifier must be referenced in the context of the containing resource (e.g., import-profile). This id should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."
    )
    parameter_class: Token | None = Field(  # Named "parameter_class" instead of "class" which is a reserved word in python
        default=None,
        description="A textual label that provides a characterization of the parameter.",
        alias="class",
    )
