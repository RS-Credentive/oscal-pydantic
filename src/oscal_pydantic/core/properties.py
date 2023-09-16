from __future__ import annotations
import warnings
from typing import ClassVar

from . import base, datatypes

from pydantic import Field, field_validator

AllowedValueList = list[dict[str, list[datatypes.OscalDatatype]]]


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
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "ns": [datatypes.OscalUri("http://csrc.nist.gov/ns/oscal")],
            "name": [datatypes.OscalToken("marking")],
        },
    ]


class LocationProperty(OscalProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "name": [datatypes.OscalToken("type")],
            "value": [datatypes.OscalString("data-center")],
            "class": [
                datatypes.OscalToken("primary"),
                datatypes.OscalToken("alternate"),
            ],
        },
    ]


class PartyProperty(OscalProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "name": [
                datatypes.OscalToken("mail-stop"),
                datatypes.OscalToken("office"),
                datatypes.OscalToken("job-title"),
            ],
        }
    ]


class ResourceProperty(OscalProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "name": [
                datatypes.OscalToken("version"),
            ],
        },
        {
            "name": [
                datatypes.OscalToken("type"),
            ],
            "value": [
                datatypes.OscalString("logo"),
                datatypes.OscalString("image"),
                datatypes.OscalString("screen-shot"),
                datatypes.OscalString("law"),
                datatypes.OscalString("regulation"),
                datatypes.OscalString("standard"),
                datatypes.OscalString("external-guidance"),
                datatypes.OscalString("acronyms"),
                datatypes.OscalString("citation"),
                datatypes.OscalString("policy"),
                datatypes.OscalString("procedure"),
                datatypes.OscalString("system-guide"),
                datatypes.OscalString("users-guide"),
                datatypes.OscalString("administrators-guide"),
                datatypes.OscalString("rules-of-behavior"),
                datatypes.OscalString("plan"),
                datatypes.OscalString("artifact"),
                datatypes.OscalString("evidence"),
                datatypes.OscalString("tool-output"),
                datatypes.OscalString("raw-data"),
                datatypes.OscalString("interview-notes"),
                datatypes.OscalString("questionnaire"),
                datatypes.OscalString("report"),
                datatypes.OscalString("agreement"),
            ],
        },
    ]


class RmfProperty(BaseProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/rmf"),
            ],
        },
    ]


class ParameterProperty(OscalProperty, RmfProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
            ],
            "name": [
                datatypes.OscalToken("label"),
                datatypes.OscalToken("sort-id"),
                datatypes.OscalToken("alt-identifier"),
                datatypes.OscalToken("alt-label"),
            ],
        },
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/rmf"),
            ],
            "name": [
                datatypes.OscalToken("aggregates"),
            ],
        },
    ]


class PartProperty(OscalProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
            ],
            "name": [
                datatypes.OscalToken("label"),
                datatypes.OscalToken("sort-id"),
                datatypes.OscalToken("alt-identifier"),
            ],
        },
    ]


class ControlProperty(OscalProperty):
    allowed_values: ClassVar[AllowedValueList] = [
        {
            "name": [
                datatypes.OscalToken("label"),
                datatypes.OscalToken("sort-id"),
                datatypes.OscalToken("alt-identifier"),
            ],
        },
        {
            "name": [
                datatypes.OscalToken("status"),
            ],
            "value": [
                datatypes.OscalToken("Withdrawn"),  # deprecated
                datatypes.OscalToken("withdrawn"),
            ],
        },
    ]

    @field_validator("value", mode="after")
    @classmethod
    def capitalized_withdrawn_deprecated(
        cls, value: datatypes.OscalToken
    ) -> datatypes.OscalToken:
        # raise a deprecationwarning if value is capitalized
        warnings.warn(
            "'Warning' is a deprecated property value for Control. Use 'warning' instead",
            DeprecationWarning,
        )
        return value
