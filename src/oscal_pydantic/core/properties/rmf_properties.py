from __future__ import annotations

from .. import base

from .base_property import BaseProperty


class RmfBaseProperty(BaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [
                    "http://csrc.nist.gov/ns/rmf",
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class RmfParameterProperty(RmfBaseProperty):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    "aggregates",
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class RmfAssessmentMethodProperty(RmfBaseProperty):
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
