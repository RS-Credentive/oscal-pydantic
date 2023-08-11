from __future__ import annotations
import warnings
import typing

from . import base, datatypes

from pydantic import Field, model_validator, AnyUrl, field_validator


class BaseProperty(base.OscalModel):
    # NOTE: This generic Property class should be extended to provide constraints on value name
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
        default=datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/oscal")),
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


class OscalProperty(BaseProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.append(
            {
                "ns": [datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/oscal"))],
                "name": [datatypes.Token(root="marking")],
            },
        )

    @model_validator(mode="after")
    def validate_oscal_property(self) -> OscalProperty:
        return self.base_validator(
            calling_type=OscalProperty, allowed_values=self._allowed_values
        )


class LocationProperty(OscalProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.append(
            {
                "name": [datatypes.Token(root="type")],
                "value": [datatypes.String(root="data-center")],
                "class": [
                    datatypes.Token(root="primary"),
                    datatypes.Token(root="alternate"),
                ],
            },
        )

    @model_validator(mode="after")
    def validate_location_property(self) -> LocationProperty:
        return self.base_validator(
            calling_type=LocationProperty, allowed_values=self._allowed_values
        )


class PartyProperty(OscalProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.append(
            {
                "name": [
                    datatypes.Token(root="mail-stop"),
                    datatypes.Token(root="office"),
                    datatypes.Token(root="job-title"),
                ],
            }
        )

    @model_validator(mode="after")
    def validate_party_property(self) -> typing.Self:
        return self.base_validator(
            calling_type=PartyProperty, allowed_values=self._allowed_values
        )


class ResourceProperty(OscalProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.extend(
            [
                {
                    "name": [
                        datatypes.Token(root="version"),
                    ],
                },
                {
                    "name": [
                        datatypes.Token(root="type"),
                    ],
                    "value": [
                        datatypes.String(root="logo"),
                        datatypes.String(root="image"),
                        datatypes.String(root="screen-shot"),
                        datatypes.String(root="law"),
                        datatypes.String(root="regulation"),
                        datatypes.String(root="standard"),
                        datatypes.String(root="external-guidance"),
                        datatypes.String(root="acronyms"),
                        datatypes.String(root="citation"),
                        datatypes.String(root="policy"),
                        datatypes.String(root="procedure"),
                        datatypes.String(root="system-guide"),
                        datatypes.String(root="users-guide"),
                        datatypes.String(root="administrators-guide"),
                        datatypes.String(root="rules-of-behavior"),
                        datatypes.String(root="plan"),
                        datatypes.String(root="artifact"),
                        datatypes.String(root="evidence"),
                        datatypes.String(root="tool-output"),
                        datatypes.String(root="raw-data"),
                        datatypes.String(root="interview-notes"),
                        datatypes.String(root="questionnaire"),
                        datatypes.String(root="report"),
                        datatypes.String(root="agreement"),
                    ],
                },
            ]
        )

    @model_validator(mode="after")
    def validate_resource_property(self) -> ResourceProperty:
        return self.base_validator(
            calling_type=ResourceProperty, allowed_values=self._allowed_values
        )


class RmfProperty(BaseProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.append(
            {
                "ns": [
                    datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/rmf")),
                ],
            },
        )

    @model_validator(mode="after")
    def validate_rmf_property(self) -> typing.Self:
        return self.base_validator(
            calling_type=RmfProperty, allowed_values=self._allowed_values
        )


class ParameterProperty(OscalProperty, RmfProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.extend(
            [
                {
                    "ns": [
                        datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/oscal")),
                    ],
                    "name": [
                        datatypes.Token(root="label"),
                        datatypes.Token(root="sort-id"),
                        datatypes.Token(root="alt-identifier"),
                        datatypes.Token(root="alt-label"),
                    ],
                },
                {
                    "ns": [
                        datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/rmf")),
                    ],
                    "name": [
                        datatypes.Token(root="aggregates"),
                    ],
                },
            ]
        )

    @model_validator(mode="after")
    def validate_parameter_property(self) -> typing.Self:
        return self.base_validator(
            calling_type=ParameterProperty, allowed_values=allowed_values
        )


class PartProperty(OscalProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.append(
            {
                "ns": [
                    datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/oscal")),
                ],
                "name": [
                    datatypes.Token(root="label"),
                    datatypes.Token(root="sort-id"),
                    datatypes.Token(root="alt-identifier"),
                ],
            },
        )

    @model_validator(mode="after")
    def validate_part_property(self) -> typing.Self:
        return self.base_validator(
            calling_type=PartProperty, allowed_values=allowed_values
        )


class ControlProperty(OscalProperty):
    def __init__(self, **data: typing.Any) -> None:
        super().__init__(**data)
        self._allowed_values.extend(
            [
                {
                    "name": [
                        datatypes.Token(root="label"),
                        datatypes.Token(root="sort-id"),
                        datatypes.Token(root="alt-identifier"),
                    ],
                },
                {
                    "name": [
                        datatypes.Token(root="status"),
                    ],
                    "value": [
                        datatypes.Token(root="Withdrawn"),  # deprecated
                        datatypes.Token(root="withdrawn"),
                    ],
                },
            ]
        )

    @model_validator(mode="after")
    def validate_control_property(self) -> typing.Self:
        return self.base_validator(
            calling_type=PartProperty, allowed_values=self._allowed_values
        )

    @field_validator("value", mode="after")
    @classmethod
    def capitalized_withdrawn_deprecated(
        cls, value: datatypes.Token
    ) -> datatypes.Token:
        # raise a deprecationwarning if value is capitalized
        warnings.warn(
            "'Warning' is a deprecated property value for Control. Use 'warning' instead",
            DeprecationWarning,
        )
        return value
