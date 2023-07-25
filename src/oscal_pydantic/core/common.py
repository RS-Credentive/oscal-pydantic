# Common elements shared by all models:
# * Property
# * Link
# * Metadata
# * Back Matter

from __future__ import annotations
from datetime import datetime, timezone

from . import base, datatypes

from pydantic import (
    Field,
)


class Property(base.OscalModel):
    name: datatypes.Token = Field(
        description="""
            A textual label that uniquely identifies a specific attribute, characteristic, 
            or quality of the property's containing object.
            """,
    )
    uuid: datatypes.UUID | None = Field(
        description="""
            A machine-oriented, globally unique identifier with cross-instance scope that 
            can be used to reference this defined property elsewhere in this or other OSCAL 
            instances. This UUID should be assigned per-subject, which means it should be 
            consistently used to identify the same subject across revisions of the document.
            """,
        default=None,
    )
    ns: datatypes.Uri = Field(
        description="""
            A namespace qualifying the property's name. This allows different 
            organizations to associate distinct semantics with the same name.
            """,
        default="http://csrc.nist.gov/ns/oscal",
    )
    value: datatypes.String = Field(
        description="""
            Indicates the value of the attribute, characteristic, or quality.
            """,
    )
    prop_class: datatypes.Token | None = Field(
        description="""
            A textual label that provides a sub-type or characterization of the property's 
            name. This can be used to further distinguish or discriminate between the 
            semantics of multiple properties of the same object with the same name and ns.
            """,
        default=None,
    )
    remarks: datatypes.MarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
            """,
        default=None,
    )


class Link(base.OscalModel):
    # TODO: Implement Constraints (3)
    # MATCHES for .[@rel=('reference') and starts-with(@href,'#')]/@href: the target value must match the lexical form of the 'uri-reference' data type.
    # INDEX HAS KEY for .[@rel=('reference') and starts-with(@href,'#')]this value must correspond to a listing in the index index-back-matter-resource using a key constructed of key field(s) @href
    # MATCHES for .[@rel=('reference') and not(starts-with(@href,'#'))]/@href: the target value must match the lexical form of the 'uri' data type.

    href: datatypes.UriReference = Field(
        description="""
            A resolvable URL reference to a resource.
        """,
    )
    rel: datatypes.Token | None = Field(
        description="""
            Describes the type of relationship provided by the link. 
            This can be an indicator of the link's purpose.
        """
    )
    media_type: datatypes.String | None = Field(
        description="""
            Specifies a media type as defined by the Internet Assigned 
            Numbers Authority (IANA) Media Types Registry.
        """,
        default=None,
    )
    text: datatypes.MarkupLine | None = Field(
        description="""
            A textual label to associate with the link, which may be 
            used for presentation in a tool.
        """,
    )


class Revision(base.OscalModel):
    # TODO: Implement Constraint (1)
    # ALLOWED VALUES for link/@rel

    # The value may be locally defined, or one of the following:

    # canonical: The link identifies the authoritative location for this file. Defined by RFC 6596.
    # alternate: The link identifies an alternative location or format for this file. Defined by the HTML Living Standard
    # predecessor-version: This link identifies a resource containing the predecessor version in the version history. Defined by RFC 5829.
    # successor-version: This link identifies a resource containing the predecessor version in the version history. Defined by RFC 5829.

    title: datatypes.MarkupLine | None = Field(
        description="""
            A name given to the document revision, which may be used by a tool 
            for display and navigation.
        """,
        default=None,
    )
    published: datatypes.DateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was published. The date-time value must 
            be formatted according to RFC 3339 with full time and time zone included.
        """,
        default=None,
    )
    last_modified: datatypes.DateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was last modified. The date-time value must 
            be formatted according to RFC 3339 with full time and time zone included.
        """,
        default=None,
    )
    version: datatypes.String = Field(
        description="""
            A string used to distinguish the current version of the document from other 
            previous (and future) versions.
        """,
    )
    oscal_version: datatypes.String = Field(
        description="""
            The OSCAL model version the document was authored against.
        """,
    )
    props: list[Property] | None = Field(
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
    links: list[Link] | None = Field(
        description="""
            A reference to a local or remote resource.
        """,
        default=None,
    )
    remarks: datatypes.MarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )


class DocumentID(base.OscalModel):
    scheme: datatypes.Uri | None = Field(
        description="""
            Qualifies the kind of document identifier using a URI. If the scheme is not provided 
            the value of the element will be interpreted as a string of characters.
            
            The value may be locally defined, or the following:

            http://www.doi.org/: A Digital Object Identifier (DOI); use is preferred, since this 
            allows for retrieval of a full bibliographic record.
        """,
        default=None,
    )
    identifier: datatypes.String | None = Field(
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
    id: datatypes.Token = Field(
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
    title: datatypes.MarkupLine = Field(
        description="""
            A name given to the role, which may be used by a tool for display and navigation.
        """,
    )
    short_name: datatypes.String | None = Field(
        description="""
            A short common name, abbreviation, or acronym for the role.
        """,
        default=None,
    )
    description: datatypes.MarkupMultiline | None = Field(
        description="""
            A summary of the role's purpose and associated responsibilities.
        """
    )
    props: list[Property] | None = Field(
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
    remarks: datatypes.MarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
        """,
        default=None,
    )


class Location(base.OscalModel):
    # DESCRIPTION A location, with associated metadata that can be referenced.

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

    uuid: datatypes.UUID


class Metadata(base.OscalModel):
    title: datatypes.MarkupLine = Field(
        description="""
            A name given to the document, which may be used by a tool for display and navigation.
        """,
    )
    published: datatypes.DateTimeWithTimezone | None = Field(
        description="""
            The date and time the document was published.
        """,
        default=None,
    )
    last_modified: datatypes.DateTimeWithTimezone = Field(
        description="""
            Last Modified Timestamp. If no value is provided, the current time will be inserted.
        """,
        default=datetime.now(tz=timezone.utc).isoformat(),
    )
    version: datatypes.String = Field(
        description="""
            The OSCAL model version the document was authored against. Defaults to 1.0.6
        """,
    )
    oscal_version: datatypes.String = Field(
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
    props: list[Property] | None = Field(
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
