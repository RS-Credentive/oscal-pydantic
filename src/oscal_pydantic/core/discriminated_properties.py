from __future__ import annotations
import warnings
import typing

from . import base, datatypes, datatypes_rootmodels

from pydantic import Field, field_validator


class BaseProperty(base.OscalModel):
    # NOTE: This generic Property class should be extended to provide constraints on value name
    name: datatypes.OscalToken = Field(
        description="""
            A textual label that uniquely identifies a specific attribute, characteristic, 
            or quality of the property's containing object.
            """,
    )
    uuid: datatypes.OscalUUID | None = Field(
        description="""
            A machine-oriented, globally unique identifier with cross-instance scope that 
            can be used to reference this defined property elsewhere in this or other OSCAL 
            instances. This UUID should be assigned per-subject, which means it should be 
            consistently used to identify the same subject across revisions of the document.
            """,
        default=None,
    )
    ns: datatypes.OscalUri = Field(
        description="""
            A namespace qualifying the property's name. This allows different 
            organizations to associate distinct semantics with the same name.
            """,
        default=datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
    )
    value: datatypes.OscalString = Field(
        description="""
            Indicates the value of the attribute, characteristic, or quality.
            """,
    )
    prop_class: datatypes.OscalToken | None = Field(
        description="""
            A textual label that provides a sub-type or characterization of the property's 
            name. This can be used to further distinguish or discriminate between the 
            semantics of multiple properties of the same object with the same name and ns.
            """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary on the containing object.
            """,
        default=None,
    )


class OscalProperty(BaseProperty):
    name: typing.Literal["marking"]


class LocationProperty(BaseProperty):
    name: typing.Literal["type"]
    value: typing.Literal["data-center"]
    property_class: typing.Literal["primary", "alternate"]


class PartyProperty(BaseProperty):
    name: typing.Literal["mail-stop", "office", "job-title"]


class ResourceProperty(BaseProperty):
    name: typing.Literal["version"]
    value: typing.Literal[
        "logo",
        "image",
        "screen-shot",
        "law",
        "regulation",
        "standard",
        "external-guidance",
        "acronyms",
        "citation",
        "policy",
        "procedure",
        "system-guide",
        "users-guide",
        "administrators-guide",
        "rules-of-behavior",
        "plan",
        "artifact",
        "evidence",
        "tool-output",
        "raw-data" "interview-notes",
        "questionnaire",
        "report",
        "agreement",
    ]


class RmfProperty(BaseProperty):
    ns: datatypes.OscalUri = datatypes.OscalUri("http://csrc.nist.gov/ns/rmf")


class OscalParameterProperty(BaseProperty):
    name: typing.Literal[
        "label",
        "sort-id",
        "alt-identifier",
        "alt-label",
    ]


class RmfParameterProperty(RmfProperty):
    name: typing.Literal["aggregates"]


class ControlPartProperty(BaseProperty):
    name: typing.Literal[
        "label",
        "sort-id",
        "alt-identifier",
    ]


class WithdrawnControlProperty(BaseProperty):
    name: typing.Literal["status"]
    value: typing.Literal["withdrawn", "Withdrawn"]

    @field_validator("value", mode="after")
    @classmethod
    def capitalized_withdrawn_deprecated(
        cls, value: datatypes_rootmodels.Token
    ) -> datatypes_rootmodels.Token:
        # raise a deprecationwarning if value is capitalized
        warnings.warn(
            "'Warning' is a deprecated property value for Control. Use 'warning' instead",
            DeprecationWarning,
        )
        return value
