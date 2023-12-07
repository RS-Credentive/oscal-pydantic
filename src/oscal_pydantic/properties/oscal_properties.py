from __future__ import annotations

from ..core import base, datatypes

from .base_property import BaseProperty

from pydantic import field_validator

import warnings


class OscalBaseProperty(BaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [datatypes.OscalUri("http://csrc.nist.gov/ns/oscal")],
            },
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class OscalMarkingProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [datatypes.OscalToken("marking")],
            },
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class LocationProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
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
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class PartyProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("mail-stop"),
                    datatypes.OscalToken("office"),
                    datatypes.OscalToken("job-title"),
                ],
            }
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class ActionProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("mail-stop"),
                    datatypes.OscalToken("office"),
                    datatypes.OscalToken("job-title"),
                ],
            }
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class ResourceProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
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
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class OscalParameterProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
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
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class PartProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("label"),
                    datatypes.OscalToken("sort-id"),
                    datatypes.OscalToken("alt-identifier"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class ControlProperty(OscalBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
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
        allowed_values.extend(super().get_allowed_values())
        return allowed_values

    @field_validator("value", mode="after")
    @classmethod
    def capitalized_withdrawn_deprecated(cls, value: str) -> datatypes.OscalToken:
        # raise a deprecationwarning if value is capitalized
        warnings.warn(
            "'Warning' is a deprecated property value for Control. Use 'warning' instead",
            DeprecationWarning,
        )
        return value
