from __future__ import annotations

from . import base, datatypes

from pydantic import Field, model_validator, AnyUrl


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
    @model_validator(mode="after")
    def validate_oscal_property(self) -> OscalProperty:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [datatypes.Uri(root=AnyUrl("http://csrc.nist.gov/ns/oscal"))],
                "name": [datatypes.Token(root="marking")],
            },
        ]

        return self.base_validator(
            calling_type=OscalProperty, allowed_values=allowed_values
        )


class LocationProperty(OscalProperty):
    @model_validator(mode="after")
    def validate_location_property(self) -> LocationProperty:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [datatypes.Token(root="type")],
                "value": [datatypes.String(root="data-center")],
                "class": [
                    datatypes.Token(root="primary"),
                    datatypes.Token(root="alternate"),
                ],
            },
        ]

        return self.base_validator(
            calling_type=LocationProperty, allowed_values=allowed_values
        )


class PartyProperty(OscalProperty):
    @model_validator(mode="after")
    def validate_party_property(self) -> PartyProperty:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.Token(root="mail-stop"),
                    datatypes.Token(root="office"),
                    datatypes.Token(root="job-title"),
                ],
            }
        ]

        return self.base_validator(
            calling_type=PartyProperty, allowed_values=allowed_values
        )


class ResourceProperty(OscalProperty):
    @model_validator(mode="after")
    def validate_party_property(self) -> ResourceProperty:
        allowed_values: list[base.AllowedValue] = [
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

        return self.base_validator(
            calling_type=ResourceProperty, allowed_values=allowed_values
        )