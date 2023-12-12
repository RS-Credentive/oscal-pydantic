from __future__ import annotations

from .. import base, datatypes

from .base_property import BaseProperty


class RmfBaseProperty(BaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [
                    datatypes.OscalUri("http://csrc.nist.gov/ns/rmf"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values


class RmfParameterProperty(RmfBaseProperty):
    @classmethod
    def get_allowed_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("aggregates"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_values())
        return allowed_values