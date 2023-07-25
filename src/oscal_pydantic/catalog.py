from __future__ import annotations

from core import datatypes, common, base

from pydantic import RootModel, Field, field_validator, FieldValidationInfo, AnyUrl

from oscal_pydantic.core import property


class Catalog(base.OscalModel):
    uuid: datatypes.UUID
