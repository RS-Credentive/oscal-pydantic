from __future__ import annotations

from .. import base, datatypes

from .base_property import BaseProperty

from pydantic import field_validator, model_validator

import warnings


class OscalBaseProperty(BaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [datatypes.OscalUri("http://csrc.nist.gov/ns/oscal")],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalMarkingProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("marking"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalLocationProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [datatypes.OscalToken("type")],
                "value": [datatypes.OscalString("data-center")],
                "prop_class": [
                    datatypes.OscalToken("primary"),
                    datatypes.OscalToken("alternate"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalPartyProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("mail-stop"),
                    datatypes.OscalToken("office"),
                    datatypes.OscalToken("job-title"),
                ],
            }
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalResourceProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
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
            {
                "name": [
                    datatypes.OscalString("published"),
                ]
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @model_validator(mode="after")
    def validate_publication_date(self) -> OscalResourceProperty:
        # for prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and
        # @name='published']/@value:
        # the target value must match the lexical form of the 'dateTime-with-timezone' data type.
        if self.name == "published":
            try:
                datatypes.OscalDateTimeWithTimezone(self.value)
            except ValueError:
                raise ValueError(
                    "Value of property in resource with name 'published' must match 'OscalDateTimeWithTimezone' format"
                )
        return self


class OscalParameterProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("label"),
                    datatypes.OscalToken("sort-id"),
                    datatypes.OscalToken("alt-identifier"),
                    datatypes.OscalToken("alt-label"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalPartProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("label"),
                    datatypes.OscalToken("sort-id"),
                    datatypes.OscalToken("alt-identifier"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalControlProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
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
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @field_validator("value", mode="after")
    @classmethod
    def capitalized_withdrawn_deprecated(cls, value: str) -> datatypes.OscalToken:
        # raise a deprecationwarning if value is capitalized
        if type(value) == str and value == "Withdrawn":
            warnings.warn(
                "'Withdrawn' is a deprecated property value for Control. Use 'withdrawn' instead",
                DeprecationWarning,
            )
        return value


class OscalMetadataProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("keywords"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalAssessmentMethodProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("method"),
                ],
                "value": [
                    datatypes.OscalToken("INTERVIEW"),
                    datatypes.OscalToken("EXAMINE"),
                    datatypes.OscalToken("TEST"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class OscalGroupProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("overview"),
                    datatypes.OscalToken("instruction"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values
