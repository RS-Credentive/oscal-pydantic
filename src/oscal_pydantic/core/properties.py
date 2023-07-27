from __future__ import annotations
from datetime import datetime, timezone
import re
from typing import Literal

from . import base, datatypes

from pydantic import (
    Field,
    field_validator,
)

class PropertyTemplate(base.OscalModel):
    ns: datatypes.Uri 
    container: base.OscalModel 
    names: list[datatypes.Token] = []
    values: list[datatypes.String] = []
    
class OscalPropertyTemplate(PropertyTemplate):
    ns: datatypes.Uri = datatypes.Uri("http://csrc.nist.gov/ns/oscal")
    names: list[datatypes.Token] = [datatypes.Token("marking")]

class OscalMetadataPropertyTemplate(OscalPropertyTemplate):
    names: list[datatypes.Token] = [datatypes.Token("keywords")] + OscalPropertyTemplate.names

class Property(base.OscalModel):
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
        default=datatypes.Uri("http://csrc.nist.gov/ns/oscal"),
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