from __future__ import annotations

from .core import base, common, datatypes, properties

from pydantic import Field, field_validator, AnyUrl

import warnings

class Profile(base.OscalModel):
    uuid: datatypes.OscalUUID
    metadata: common.Metadata
    # imports:
    # merge:
    # modify:
    back_matter: common.BackMatter

class Import(base.OscalModel):
    href: datatypes.OscalUriReference
    # include_all: We will implement this if/when we find such an example
    include_controls: list[ChildControl] | None
    exclude_controls: list[ChildControl] | None

class ChildControl(base.OscalModel):
    with_child_controls: datatypes.OscalToken | None
    with_ids: list[datatypes.OscalToken] | None
    matching: list[WildcardPattern] | None

class WildcardPattern(base.OscalModel):
    pattern: datatypes.OscalString | None

