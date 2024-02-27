from __future__ import annotations

from .. import base, datatypes

from .base_property import BaseProperty
from typing import Self

from pydantic import field_validator, model_validator

import warnings


class OscalBaseProperty(BaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": ["http://csrc.nist.gov/ns/oscal"],
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
                    "marking",
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
                "name": ["type"],
                "value": ["data-center"],
                "prop_class": [
                    "primary",
                    "alternate",
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
                    "mail-stop",
                    "office",
                    "job-title",
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
                    "version",
                ],
            },
            {
                "name": [
                    "type",
                ],
                "value": [
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
                    "raw-data",
                    "interview-notes",
                    "questionnaire",
                    "report",
                    "agreement",
                ],
            },
            {
                "name": [
                    "published",
                ]
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @model_validator(mode="after")
    def validate_publication_date(self) -> Self:
        # for prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal') and
        # @name='published']/@value:
        # the target value must match the lexical form of the 'dateTime-with-timezone' data type.
        if self.name == "published":
            try:
                self.value
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
                    "label",
                    "sort-id",
                    "alt-identifier",
                    "alt-label",
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
                    "label",
                    "sort-id",
                    "alt-identifier",
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
                    "label",
                    "sort-id",
                    "alt-identifier",
                ],
            },
            {
                "name": [
                    "status",
                ],
                "value": [
                    "Withdrawn",  # deprecated
                    "withdrawn",
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
                    "keywords",
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
                    "method",
                ],
                "value": [
                    "INTERVIEW",
                    "EXAMINE",
                    "TEST",
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
                    "overview",
                    "instruction",
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values
