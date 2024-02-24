# Common elements shared by all models:
# * Property
# * Link
# * Metadata
# * Back Matter

from __future__ import annotations
from datetime import datetime, timezone
from collections import Counter
import re

from . import base, datatypes, properties

from pydantic import (
    Field,
    model_validator,
)


class Link(base.OscalModel):
    # TODO: Implement Constraints (3)
    # MATCHES for .[@rel=('reference') and starts-with(@href,'#')]/@href: the target value must match the lexical form of the 'uri-reference' data type.
    # INDEX HAS KEY for .[@rel=('reference') and starts-with(@href,'#')]this value must correspond to a listing in the index index-back-matter-resource using a key constructed of key field(s) @href
    # MATCHES for .[@rel=('reference') and not(starts-with(@href,'#'))]/@href: the target value must match the lexical form of the 'uri' data type.

    href: datatypes.OscalUriReference = Field(
        description="""
            A resolvable URL reference to a resource.
        """,
    )
    rel: datatypes.OscalToken = Field(
        description="""
            Describes the type of relationship provided by the link. 
            This can be an indicator of the link's purpose.
        """
    )
    media_type: datatypes.OscalString | None = Field(
        description="""
            Specifies a media type as defined by the Internet Assigned 
            Numbers Authority (IANA) Media Types Registry.
        """,
        default=None,
    )
    text: datatypes.OscalMarkupLine | None = Field(
        description="""
            A textual label to associate with the link, which may be 
            used for presentation in a tool.
        """,
        default=None,
    )


class RevisionLink(Link):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_field_values: list[base.AllowedValue] = [
            {
                "rel": [
                    datatypes.OscalToken("canonical"),
                    datatypes.OscalToken("alternate"),
                    datatypes.OscalToken("predecessor-version"),
                    datatypes.OscalToken("successor-version"),
                    datatypes.OscalToken("version-history"),
                ],
            }
        ]
        allowed_field_values.extend(super().get_allowed_field_values())
        return allowed_field_values


class Revision(base.OscalModel):
    # TODO: Implement Constraint (1)
    # ALLOWED VALUES for link/@rel

    # The value may be locally defined, or one of the following:

    # canonical: The link identifies the authoritative location for this file. Defined by RFC 6596.
    # alternate: The link identifies an alternative location or format for this file. Defined by the HTML Living Standard
    # predecessor-version: This link identifies a resource containing the predecessor version in the version history. Defined by RFC 5829.
    # successor-version: This link identifies a resource containing the predecessor version in the version history. Defined by RFC 5829.

    title: datatypes.OscalMarkupLine | None = Field(
        description="""
            A name given to the document revision, which may be used by a tool 
            for display and navigation.
        """,
        default=None,
    )
    published: datatypes.OscalDateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was published. The date-time value must 
            be formatted according to RFC 3339 with full time and time zone included.
        """,
        default=None,
    )
    last_modified: datatypes.OscalDateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was last modified. The date-time value must 
            be formatted according to RFC 3339 with full time and time zone included.
        """,
        default=None,
    )
    version: datatypes.OscalString = Field(
        description="""
            A string used to distinguish the current version of the document from other 
            previous (and future) versions.
        """,
    )
    oscal_version: datatypes.OscalString | None = Field(
        description="""
            The OSCAL model version the document was authored against.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            Properties permit the deployment and management of arbitrary controlled values, 
            within OSCAL objects. A property can be included for any purpose useful to an 
            application or implementation. Typically, properties will be used to sort, filter, 
            select, order, and arrange OSCAL content objects, to relate OSCAL objects to one 
            another, or to associate an OSCAL object to class hierarchies, taxonomies, or 
            external authorities. Thus, the lexical composition of properties may be constrained 
            by external processes to ensure consistency.

            Property allows for associated remarks that describe why the specific property 
            value was applied to the containing object, or the significance of the value in 
            the context of the containing object.
        """,
        default=None,
    )
    links: list[RevisionLink] | None = Field(
        description="""
            A reference to a local or remote resource.
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class DocumentID(base.OscalModel):
    scheme: datatypes.OscalUri | None = Field(
        description="""
            Qualifies the kind of document identifier using a URI. If the scheme is not provided 
            the value of the element will be interpreted as a string of characters.
            
            The value may be locally defined, or the following:

            http://www.doi.org/: A Digital Object Identifier (DOI); use is preferred, since this 
            allows for retrieval of a full bibliographic record.
        """,
        default=None,
    )
    identifier: datatypes.OscalString | None = Field(
        description="""
            This element is optional, but it will always have a valid value, as if it is missing 
            the value of "document-id" is assumed to be equal to the UUID of the root. This 
            requirement allows for document creators to retroactively link an update to the 
            original version, by providing a document-id on the new document that is equal to 
            the uuid of the original document.
        """,
        default=None,
    )


class Role(base.OscalModel):
    id: datatypes.OscalToken = Field(
        description="""
            A human-oriented, locally unique identifier with cross-instance scope that can be used 
            to reference this defined role elsewhere in this or other OSCAL instances. When 
            referenced from another OSCAL instance, the locally defined ID of the Role from the 
            imported OSCAL instance must be referenced in the context of the containing resource 
            (e.g., import, import-component-definition, import-profile, import-ssp or import-ap). 
            This ID should be assigned per-subject, which means it should be consistently used to 
            identify the same subject across revisions of the document.
        """,
    )
    title: datatypes.OscalMarkupLine = Field(
        description="""
            A name given to the role, which may be used by a tool for display and navigation.
        """,
    )
    short_name: datatypes.OscalString | None = Field(
        description="""
            A short common name, abbreviation, or acronym for the role.
        """,
        default=None,
    )
    description: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            A summary of the role's purpose and associated responsibilities.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a namespace 
            qualified name/value pair. The value of a property is a simple scalar value, which may be 
            expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class Address(base.OscalModel):
    type: datatypes.OscalToken | None = Field(
        description="""
            Indicates the type of address.
        """,
        default=None,
    )
    addr_lines: list[datatypes.OscalString] | None = Field(
        description="""
            A list of Address Line: A single line of an address.       
        """,
        default=None,
    )
    city: datatypes.OscalString | None = Field(
        description="""
            City, town or geographical region for the mailing address.
        """,
        default=None,
    )
    state: datatypes.OscalString | None = Field(
        description="""
                State, province or analogous geographical region for mailing address
            """,
        default=None,
    )
    postal_code: datatypes.OscalString | None = Field(
        description="""
            Postal or ZIP code for mailing address
        """,
        default=None,
    )
    country: datatypes.OscalString | None = Field(
        description="""
            The ISO 3166-1 alpha-2 country code for the mailing address.
        """,
        default=None,
    )

    # TODO: This should be a field validator
    @model_validator(mode="after")
    def two_letter_country_code(self) -> Address:
        if self.country is not None and re.match("[A-Z]{2}", self.country) == None:
            raise ValueError("country string must have 2 letters")
        return self


class TelephoneNumber(base.OscalModel):
    """A class to represent a telephone number in OSCAL

    Attributes:
        type (datatype.String): the type of phone number
        number (datatype.String): the phone number
    """

    type: datatypes.OscalString | None = Field(
        description="""
                Indicates the type of phone number. 

                The value may be locally defined, or one of the following:

                home: A home phone number.
                office: An office phone number.
                mobile: A mobile phone number.
            """,
        default=None,
    )
    number: datatypes.OscalString | None = Field(
        description="""
            The phone number
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_field_values: list[base.AllowedValue] = [
            {
                "ns": [
                    datatypes.OscalString("home"),
                    datatypes.OscalString("office"),
                    datatypes.OscalString("mobile"),
                ],
            },
        ]
        allowed_field_values.extend(super().get_allowed_field_values())
        return allowed_field_values


class Location(base.OscalModel):
    """# DESCRIPTION A location, with associated metadata that can be referenced.

    # Constraints (3)
    # ALLOWED VALUE for prop/@name

    # The value may be locally defined, or the following:

    # type: Characterizes the kind of location.
    # ALLOWED VALUE for prop[@name='type']/@value

    # The value may be locally defined, or the following:

    # data-center: A location that contains computing assets. A class can be used to indicate the sub-type of data-center as primary or alternate.
    # ALLOWED VALUES for prop[@name='type' and @value='data-center']/@class

    # The value may be locally defined, or one of the following:

    # primary: The location is a data-center used for normal operations.
    # alternate: The location is a data-center used for fail-over or backup operations.
    """

    uuid: datatypes.OscalUUID = Field(
        description="""
            A machine-oriented, globally unique identifier with cross-instance scope that can be 
            used to reference this defined location elsewhere in this or other OSCAL instances. 
            The locally defined UUID of the location can be used to reference the data item 
            locally or globally (e.g., from an importing OSCAL instance). This UUID should be 
            assigned per-subject, which means it should be consistently used to identify the same 
            subject across revisions of the document.
        """
    )
    title: datatypes.OscalMarkupLine | None = Field(
        description="""
            A name given to the location, which may be used by a tool for display and navigation.
        """,
        default=None,
    )
    address: Address = Field(
        description="""
            A postal Address for the location
        """,
    )
    email_addresses: list[datatypes.OscalEmail] | None = Field(
        description="""
            An email address as defined by RFC 5322 Section 3.4.1
        """,
        default=None,
    )
    telephone_numbers: list[TelephoneNumber] | None = Field(
        description="""
            A list of telephone numbers for the locations
        """,
        default=None,
    )
    urls: list[datatypes.OscalUri] | None = Field(
        description="""
            The uniform resource locator (URL) for a web site or Internet presence associated with 
            the location.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair. The value of a property is a simple scalar value, 
            which may be expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalLocationProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class ExternalID(base.OscalModel):
    """An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID)

    Attributes:
        scheme (datatypes_annotated.OscalUri): Indicates the type of external identifier.
        id (datattypes.String): the ID of the party"""

    scheme: datatypes.OscalUri = Field(
        description="""
            Indicates the type of external identifier.
        """,
    )
    id: datatypes.OscalString | None = Field(
        description="""
            An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID)
        """,
        default=None,
    )


class Party(base.OscalModel):
    """A class representing an OSCAL Party

    Attributes:
        param name (param type): describe the param
    """

    uuid: datatypes.OscalUUID | None = Field(
        description="""
            A machine-oriented, globally unique identifier with cross-instance scope that can be 
            used to reference this defined party elsewhere in this or other OSCAL instances. The 
            locally defined UUID of the party can be used to reference the data item locally or 
            globally (e.g., from an importing OSCAL instance). This UUID should be assigned per-
            subject, which means it should be consistently used to identify the same subject 
            across revisions of the document.
        """,
        default=None,
    )
    type: datatypes.OscalString | None = Field(
        description="""
            A category describing the kind of party the object describes.

            Constraint (1)
            ALLOWED VALUES

            The value must be one of the following:

            person: An individual.
            organization: A group of individuals formed for a specific purpose.
        """,
        default=None,
    )
    name: datatypes.OscalString | None = Field(
        description="""
            The full name of the party. This is typically the legal name associated with the party.
        """,
        default=None,
    )
    short_name: datatypes.OscalString | None = Field(
        description="""
            A short common name, abbreviation, or acronym for the party.
        """,
        default=None,
    )
    external_ids: list[ExternalID] | None = Field(
        description="""
            An identifier for a person or organization using a designated scheme. e.g. an Open 
            Researcher and Contributor ID (ORCID)
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            Additional properties related to the party
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A list of references to local or remote resources.
        """,
        default=None,
    )
    email_addresses: list[datatypes.OscalEmail] | None = Field(
        description="""
            A list of email addresses
        """,
        default=None,
    )
    telephone_numbers: list[TelephoneNumber] | None = Field(
        description="""
            A list of telephone numbers
        """,
        default=None,
    )
    addresses: list[Address] | None = Field(
        description="""
            A list of postal addresses
        """,
        default=None,
    )
    location_uuids: list[datatypes.OscalUUID] | None = Field(
        description="""
            A list of identifier references to a location defined in the metadata section of this or another OSCAL document.
        """,
        default=None,
    )
    member_of_organizations: list[datatypes.OscalUUID] | None = Field(
        description="""
            A list of machine-oriented references to partise that this subject is associated with.
        """,
        default=None,
    )
    remarks: list[datatypes.OscalMarkupMultiline] | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_field_values: list[base.AllowedValue] = [
            {
                "type": [
                    datatypes.OscalString("person"),
                    datatypes.OscalString("organization"),
                ],
            },
        ]
        allowed_field_values.extend(super().get_allowed_field_values())
        return allowed_field_values

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalPartyProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class ResponsibleParty(base.OscalModel):
    role_id: datatypes.OscalToken = Field(
        description="""
            A human-oriented identifier reference to roles served by the user
        """,
    )
    party_uuids: list[datatypes.OscalUUID] = Field(
        description="""
            A machine-oriented identifier reference to another party defined in metadata. 
            The UUID of the party in the source OSCAL instance is sufficient to reference the data 
            item locally or globally (e.g., in an imported OSCAL instance).
        """,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair. The value of a property is a simple scalar value,
            which may be expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class Action(base.OscalModel):
    uuid: datatypes.OscalUUID = Field(
        description="""
            A unique identifier that can be used to reference this defined action elsewhere in an OSCAL document. 
            A UUID should be consistently used for a given location across revisions of the document.
        """
    )
    date: datatypes.OscalDateTimeWithTimezone | None = Field(
        description="""
            The date and time when the action occurred.
        """,
        default=None,
    )
    type: datatypes.OscalToken = Field(
        description="""
            The type of action documented by the assembly, such as an approval.
        """,
    )
    system: datatypes.OscalUri = Field(
        description="""
            Specifies the action type system used.
        """
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair. The value of a property is a simple scalar value,
            which may be expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource, that has a specific relation to the containing object.
        """,
        default=None,
    )
    responsible_parties: list[ResponsibleParty] | None = Field(
        description="""
            A reference to a set of persons and/or organizations that have responsibility for performing the 
            referenced role in the context of the containing object.
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary about the containing object.
        """
    )

    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_field_values: list[base.AllowedValue] = [
            {
                "system": [
                    datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
                ],
                "type": [
                    datatypes.OscalToken("approval"),
                    datatypes.OscalToken("request-changes"),
                ],
            }
        ]
        allowed_field_values.extend(super().get_allowed_field_values())
        return allowed_field_values

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class Metadata(base.OscalModel):
    title: datatypes.OscalMarkupLine = Field(
        description="""
            A name given to the document, which may be used by a tool for display and navigation.
        """,
    )
    published: datatypes.OscalDateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was published.
        """,
        default=None,
    )
    last_modified: datatypes.OscalDateTimeWithTimezone = Field(
        description="""
            Last Modified Timestamp. If no value is provided, the current time will be inserted.
        """,
        default=datetime.now(tz=timezone.utc).isoformat(),
    )
    version: datatypes.OscalString = Field(
        description="""
            The OSCAL model version the document was authored against. Defaults to 1.0.6
        """,
    )
    oscal_version: datatypes.OscalString = Field(
        description="""
            The OSCAL model version the document was authored against. Defaults to 1.0.6
        """,
    )
    revisions: list[Revision] | None = Field(
        description="""
            An entry in a sequential list of revisions to the containing document in reverse 
            chronological order (i.e., most recent previous revision first).
        """,
        default=None,
    )
    document_ids: list[DocumentID] | None = Field(
        description="""
            A document identifier qualified by an identifier scheme. A document identifier 
            provides a globally unique identifier with a cross-instance scope that is used 
            for a group of documents that are to be treated as different versions of the 
            same document. If this element does not appear, or if the value of this element 
            is empty, the value of "document-id" is equal to the value of the "uuid" flag of 
            the top-level root element.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair. The value of a property is a simple scalar 
            value, which may be expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource
        """,
        default=None,
    )
    roles: list[Role] | None = Field(
        description="""
            Defines a function assumed or expected to be assumed by a party in a specific situation.
        """,
        default=None,
    )
    locations: list[Location] | None = Field(
        description="""
            A list of locations, with associated metadata that can be referenced.
        """,
        default=None,
    )
    parties: list[Party] | None = Field(
        description="""
            A list of responsible entities, each of which is either a person or an organization.
        """,
        default=None,
    )
    responsible_parties: list[ResponsibleParty] | None = Field(
        description="""
            A reference to a set of organizations or persons that have responsibility for 
            performing a referenced role in the context of the containing object.
        """,
        default=None,
    )
    actions: list[Action] | None = Field(
        description="""
            An action applied by a role within a given party to the content.
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @model_validator(mode="after")
    def validate_metadata(self) -> Metadata:
        # Check that the every role-id and party-id provided in responsible-party corresponds to a defined role or party respectively
        if self.responsible_parties is not None:
            if self.parties is None or self.roles is None:
                raise ValueError(
                    "Responsible Parties defined, but no Roles defined or no Parties defined"
                )
            for party in self.responsible_parties:
                if party.role_id not in [role.id for role in self.roles]:
                    raise ValueError(f"Role ID for {party} not found in roles")

                party_uuids_from_parties = [party.uuid for party in self.parties]
                for uuid in party.party_uuids:
                    if uuid not in party_uuids_from_parties:
                        raise ValueError(f"Party UUID {uuid} not present in parties")
        return self

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMetadataProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class Citation(base.OscalModel):
    text: datatypes.OscalMarkupLine = Field(
        description="""
            A line of citation text.
        """,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An optional list of attributes, characteristics, or qualities of the containing object 
            expressed as a namespace qualified name/value pair. The value of a property is a simple 
            scalar value, which may be expressed as a list of values.
        """,
        default=None,
    )
    links: list[Link] | None = Field(
        description="""
            An optional list of references to a local or remote resource.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class Hash(base.OscalModel):
    algorithm: datatypes.OscalString | None = Field(
        description="""
            Method by which a hash is derived

            Remarks
            Any other value used MUST be a value defined in the W3C XML Security Algorithm Cross-
            Reference Digest Methods (W3C, April 2013) or RFC 6931 Section 2.1.5 New SHA Functions.

            Constraint (1)
            ALLOWED VALUES

            The value may be locally defined, or one of the following:

            SHA-224: The SHA-224 algorithm as defined by NIST FIPS 180-4.
            SHA-256: The SHA-256 algorithm as defined by NIST FIPS 180-4.
            SHA-384: The SHA-384 algorithm as defined by NIST FIPS 180-4.
            SHA-512: The SHA-512 algorithm as defined by NIST FIPS 180-4.
            SHA3-224: The SHA3-224 algorithm as defined by NIST FIPS 202.
            SHA3-256: The SHA3-256 algorithm as defined by NIST FIPS 202.
            SHA3-384: The SHA3-384 algorithm as defined by NIST FIPS 202.
            SHA3-512: The SHA3-512 algorithm as defined by NIST FIPS 202.
        """,
        default=None,
        pattern="^SHA3?-(224|256|384|512)$",
    )
    value: datatypes.OscalString | None = Field(
        description="""
            The value of the hash
        """,
        default=None,
    )

    def value_is_hex(self) -> bool:
        # Quick trick to check if a string is only HEX - try to convert it to an int.
        # If it doesn't work, there's a bad character in there.
        if self.value is not None:
            try:
                int(self.value, 16)
                return True
            except ValueError:
                return False
        else:
            return False

    @model_validator(mode="after")
    def validate_hash_for_algorithm(self) -> Hash:
        if self.algorithm is None and self.value is None:
            # No value and no algorithm is okay
            return self
        elif self.algorithm is not None and self.value is None:
            # Any algorithm must have some value
            raise ValueError("Hash Algorithm specified without a Hash Value")
        elif self.algorithm is None and self.value is not None:
            # Any algorithm must have some value
            raise ValueError("Hash Value specified without a Hash Algorithm")
        elif self.algorithm is not None and self.value is not None:
            if self.algorithm == "SHA-224" or self.algorithm == "SHA3-224":
                if len(self.value) == 28 and self.value_is_hex():
                    return self
                else:
                    raise ValueError(
                        "Hash value length or contents do not match algorithm"
                    )
            elif self.algorithm == "SHA-256" or self.algorithm == "SHA3-256":
                if len(self.value) == 32 and self.value_is_hex():
                    return self
                else:
                    raise ValueError(
                        "Hash value length or contents do not match algorithm"
                    )
            elif self.algorithm == "SHA-384" or self.algorithm == "SHA3-384":
                if len(self.value) == 48 and self.value_is_hex():
                    return self
                else:
                    raise ValueError(
                        "Hash value length or contents do not match algorithm"
                    )
            elif self.algorithm == "SHA-512" or self.algorithm == "SHA3-512":
                if len(self.value) == 64 and self.value_is_hex():
                    return self
                else:
                    raise ValueError(
                        "Hash value length or contents do not match algorithm"
                    )
            else:
                # Unrecognized Hash Algorithm and value - we have to assume they're okay
                return self
        else:
            # Not sure if there's any way get here, but pylance is complaining about a missing return value
            return self


class ResourceLink(base.OscalModel):
    href: datatypes.OscalUriReference = Field(
        description="""
            A resolvable URI reference to a resource.
        """,
    )
    media_type: datatypes.OscalString | None = Field(
        description="""
            Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) 
            Media Types Registry.
        """,
        default=None,
    )
    hashes: list[Hash] | None = Field(
        description="""
            description
        """,
        default=None,
    )


class Base64(base.OscalModel):
    filename: datatypes.OscalUriReference | None = Field(
        description="""
            Name of the file before it was encoded as Base64 to be embedded in a resource. This is 
            the name that will be assigned to the file when the file is decoded.
        """,
        default=None,
    )
    media_type: datatypes.OscalString | None = Field(
        description="""
            Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) 
            Media Types Registry.
        """,
        default=None,
    )
    value: datatypes.OscalBase64Binary | None = Field(
        description="""
            The Base64 encoded file.
        """,
        min_length=1,
        default=None,
    )


class Resource(base.OscalModel):
    uuid: datatypes.OscalUUID = Field(
        description="""
            A machine-oriented, globally unique identifier with cross-instance scope that can be 
            used to reference this defined resource elsewhere in this or other OSCAL instances. 
            This UUID should be assigned per-subject, which means it should be consistently used 
            to identify the same subject across revisions of the document.
        """,
    )
    title: datatypes.OscalMarkupLine | None = Field(
        description="""
            A name given to the resource, which may be used by a tool for display and navigation.
        """,
        default=None,
    )
    description: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            A short summary of the resource used to indicate the purpose of the resource.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An optional list of properties associated with the resource.
        """,
        default=None,
    )
    document_ids: list[DocumentID] | None = Field(
        description="""
            An optional list of document Identifiers associated with the resource
        """,
        default=None,
    )
    citation: Citation | None = Field(
        description="""
            A citation consisting of end note text and optional structured bibliographic data.
        """,
        default=None,
    )
    rlinks: list[ResourceLink] | None = Field(
        description="""
            An optional list of pointers to an external resource with an optional hash for 
            verification and change detection.
        """,
        default=None,
    )
    base64: list[Base64] | None = Field(
        description="""
            A resource encoded in Base64 and embedded in the document
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )

    @model_validator(mode="after")
    def unique_rlink(self) -> Resource:
        if self.rlinks is not None:
            links_counter = Counter([rlink.href for rlink in self.rlinks])
            duplicates = [item for item, count in links_counter.items() if count > 1]
            if len(duplicates) > 0:
                raise ValueError("Duplicate rlinks in %s: %s", self.uuid, duplicates)
        return self

    @model_validator(mode="after")
    def unique_base64(self) -> Resource:
        if self.base64 is not None:
            b64_counter = Counter([b64.value for b64 in self.base64])
            duplicates = [item for item, count in b64_counter.items() if count > 1]
            if len(duplicates) > 0:
                raise ValueError("Duplicate base64 items in %s", self.uuid)
        return self

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalResourceProperty,
                    properties.OscalMarkingProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class BackMatter(base.OscalModel):
    resources: list[Resource] | None = Field(
        description="""
            A collection of resources, which may be included directly or by reference.
        """,
        default=None,
    )
