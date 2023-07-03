# Common elements shared by all Models: Metadata, Back Matter
from __future__ import annotations

from . import core

from pydantic import (
    BaseModel,
    Field,
    RootModel,
    AwareDatetime,
    AnyUrl,
    EmailStr,
)

from enum import Enum


class Title(RootModel[core.MarkupLine]):
    root: core.MarkupLine = Field(
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
    root: str = Field(
        default="1.0.5",
        description="The OSCAL model version the document was authored against. This library currently produces 1.0.5",
        alias="oscal-version",
        pattern="^1.0.5$",
    )


class Role(BaseModel):
    id: core.Token = Field(description="A unique identifier for the role.")
    title: core.MarkupLine = Field(
        description="A name given to the role, which may be used by a tool for display and navigation."
    )
    short_name: str | None = Field(
        default=None,
        description="A short common name, abbreviation, or acronym for the role.",
    )
    description: core.MarkupMultiline | None = Field(
        default=None,
        description="A summary of the role's purpose and associated responsibilities.",
    )
    props: list[core.Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[core.Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    remarks: core.Remarks | None = Field(default=None)


class Address(BaseModel):
    type: core.Token | None = Field(
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
    uuid: core.UUID = Field(description="A unique ID for the location, for reference.")
    title: core.MarkupLine | None = Field(
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
    props: list[core.Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[core.Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    remarks: core.MarkupMultiline | None = Field(
        default=None, description="Additional commentary about the containing object."
    )


class Revision(BaseModel):
    title: Title | None = Field(default=None)
    published: Published | None = Field(default=None)
    last_modified: LastModified | None = Field(default=None)
    version: Version
    oscal_version: OscalVersion | None = Field(default=None)
    prop: list[core.Property] | None = Field(default=None)
    link: list[core.Link] | None = Field(default=None)
    remarks: core.Remarks | None = Field(default=None)


class Scheme(RootModel[AnyUrl]):
    root: AnyUrl = Field(
        description="Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters."
    )


class DocumentID(BaseModel):
    scheme: Scheme | None = Field(default=None)
    identifier: core.Token


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
    uuid: core.UUID = Field(description="A unique identifier for the party.")
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
    props: list[core.Property] | None = Field(default=None)
    links: list[core.Link] | None = Field(default=None)
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
    location_uuids: list[core.UUID] | None = Field(
        default=None,
        description="A machine-oriented identifier reference to a location defined in the metadata section of this or another OSCAL instance. The UUID of the location in the source OSCAL instance is sufficient to reference the data item locally or globally (e.g., in an imported OSCAL instance).",
        alias="location-uuids",
    )
    member_of_organizations: list[core.UUID] | None = Field(
        default=None,
        description="A machine-oriented identifier reference to another party (person or organization) that this subject is associated with. The UUID of the party in the source OSCAL instance is sufficient to reference the data item locally or globally (e.g., in an imported OSCAL instance).",
        alias="member-of-organizations",
    )
    remarks: core.MarkupMultiline | None = Field(
        default=None, description="Additional commentary on the containing object."
    )


class RoleID(RootModel[core.Token]):
    root: core.Token = Field(
        description="A human-oriented identifier reference to roles served by the user."
    )


class PartyUUID(RootModel[core.UUID]):
    root: core.UUID = Field(
        description="A machine-oriented identifier reference to another party defined in metadata. The UUID of the party in the source OSCAL instance is sufficient to reference the data item locally or globally (e.g., in an imported OSCAL instance)."
    )


class ResponsibleParty(BaseModel):
    role_id: RoleID = Field(alias="role-id")
    party_uuid: PartyUUID = Field(alias="party-uuid")
    props: list[core.Property] | None = Field(default=None)
    links: list[core.Link] | None = Field(default=None)
    remarks: core.Remarks | None = Field(default=None)


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
    props: list[core.Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[core.Link] | None = Field(
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
    responsible_parties: list[ResponsibleParty] | None = Field(
        default="None",
        description="A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.",
    )
    remarks: core.Remarks | None = Field(default=None)
