# Reuseable base classes for core data types
from __future__ import annotations

from typing import Literal

import uuid
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    AnyUrl,
    field_validator,
    FieldValidationInfo,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic.main import IncEx


# Helper function to convert python_variable_name to json-attribute-name
def oscal_aliases(string: str) -> str:
    wordlist = string.split("_")
    if wordlist[-1] == "class":
        # if the original is a variant of "XXX_class", the attribute should be called "class"
        return "class"
    else:
        # otherwise just replace the "_" with "-"
        return "-".join(word for word in string.split("_"))


class OscalModel(BaseModel):
    # A utility class that defines default behaviors for all other Models
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
        alias_generator=oscal_aliases,
    )

    # Override default model_dump_json to include indentation, exclude null values and always use alias
    def model_dump_json(
        self,
        *,
        indent: int | None = 4,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super().model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
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
        pattern=r"^([^\W\d]|[:_]){1}[\w\d:\-_.]*$",  # "any non-numeric character, _ or :, followed by a sequence of any alphanumeric character, _, :, -, or ."
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


class FragmentIdentifier(RootModel[str]):
    root: str = Field(pattern=r"^#(.*)$")


class UrlReference(RootModel[AnyUrl | FragmentIdentifier]):
    root: AnyUrl | FragmentIdentifier


class Link(OscalModel):
    href: UrlReference = Field(description="A reference to a local or remote resource")
    rel: Relation | None = Field(default=None)
    media_type: str | None = Field(
        description="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.",
        default=None,
        # alias="media-type",
    )
    resource_fragment: str | None = Field(
        description="In case where the href points to a back-matter/resource, this value will indicate the URI fragment to append to any rlink associated with the resource. This value MUST be URI encoded.",
        default=None,
        # alias="resource-fragment",
    )
    text: MarkupLine | None = Field(default=None)


class PropertyNamespace(RootModel[AnyUrl]):
    root: AnyUrl = Field(
        description="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name.",
    )


class OscalNamespace(RootModel[PropertyNamespace]):
    root: PropertyNamespace = Field(
        default=AnyUrl("http://csrc.nist.gov/ns/oscal"),
    )


class PropertyName(RootModel[str]):
    root: str


class OscalPropertyName(RootModel[PropertyName]):
    root: PropertyName = Field(default=Literal["marking"])


class PropertyValue(RootModel[str]):
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


class Property(OscalModel):
    name: PropertyName
    uuid: UUID | None = Field(default=None)
    ns: OscalNamespace | PropertyNamespace = Field(default=OscalNamespace())
    value: PropertyValue
    property_class: PropertyClass | None = Field(default=None)
    group: Group | None = Field(default=None)
    remarks: Remarks | None = Field(default=None)

    allowed_names: list[str] = []

    # TODO: this function checks the values if the ns is default or blank. Should provide a way to check against custom schemas
    @field_validator("ns")
    def confirm_default_property_values(
        cls, property: OscalNamespace | PropertyNamespace, info: FieldValidationInfo
    ):
        # IF we use the nist namespace, we have to use a nist value. A blank namespace is assumed to be the NIST namespace
        if (
            "ns" in info.data.keys()
            and isinstance(info.data["ns"], OscalNamespace)
            and not isinstance(info.data["name"], OscalPropertyName)
        ):
            raise ValueError


class MediaType(RootModel[str]):
    root: str = Field(
        description="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.",
        pattern=r"^\w+/([\w-]+\.)*[\w-]+(\+[\w]+)?(;.*)?$",
    )


class Base64Binary(RootModel[str]):
    root: str = Field(
        description="A string representing arbitrary Base64-encoded binary data.",
        pattern=r"^[0-9A-Fa-f]+$",
    )
