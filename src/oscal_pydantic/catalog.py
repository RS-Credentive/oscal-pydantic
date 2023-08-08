from __future__ import annotations

from .core import base, datatypes, common

from pydantic import Field


class Parameter(base.OscalModel):
    pass


class Control(base.OscalModel):
    pass


class Group(base.OscalModel):
    pass


class Catalog(base.OscalModel):
    uuid: datatypes.UUID
    metadata: common.Metadata
    params: list[Parameter] | None = Field(
        description="""
            Parameters provide a mechanism for the dynamic assignment of value(s) in a control.
        """,
        default=None,
    )
    controls: list[Control] | None = Field(
        description="""
            A structured information object representing a security or privacy control. Each 
            security or privacy control within the Catalog is defined by a distinct control 
            instance.
        """,
        default=None,
    )
    groups: list[Group] | None = Field(
        description="""
            A group of controls, or of groups of controls.
        """,
        default=None,
    )
    back_matter: common.BackMatter
