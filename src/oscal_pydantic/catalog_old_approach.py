from __future__ import annotations

from .core import base, common, datatypes, properties

from pydantic import Field, field_validator, model_validator, AnyUrl

import warnings


#
#
#  NOTE: This is only here for reference, the approach of defining "allowed values" and feeding them
#   into a generic validation function, appears to be too complicated with the current version of
#   pydantic v2 - I am trying tagged unions instead.
#
#


class Test(base.OscalModel):
    expression: datatypes.OscalString = Field(
        description="""
            A formal (executable) expression of a constraint.
        """
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary about the containing object.
            The remarks field SHOULD not be used to store arbitrary data. Instead, a prop or 
            link should be used to annotate or reference any additional data not formally 
            supported by OSCAL.
        """,
        default=None,
    )


class Constraint(base.OscalModel):
    description: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            A textual summary of the constraint to be applied.
        """,
        default=None,
    )
    tests: list[Test] | None = Field(
        description="""
            A test expression which is expected to be evaluated by a tool.
        """,
        default=None,
    )


class Guidelines(base.OscalModel):
    prose: datatypes.OscalMarkupMultiline = Field(
        description="""
            A prose statement that provides a recommendation for the use of a parameter.
        """,
    )


class Select(base.OscalModel):
    how_many: datatypes.OscalToken | None = Field(
        description="""
            Describes the number of selections that must occur. Without this setting, only 
            one value should be assumed to be permitted.
        """,
        default=None,
    )
    choice: list[datatypes.OscalMarkupLine] | None = Field(
        description="""
             A value selection among several such options.
        """,
        default=None,
    )

    @field_validator("how_many")
    @classmethod
    def one_or_many(cls, how_many: datatypes.OscalToken) -> datatypes.OscalToken:
        permitted_values = [
            datatypes.OscalToken("one"),
            datatypes.OscalToken("one-or-many"),
        ]
        if how_many not in permitted_values:
            raise ValueError("Select/how-many must be 'one' or 'one-or-many'")
        else:
            return how_many


class Parameter(base.OscalModel):
    id: datatypes.OscalToken = Field(
        description="A unique identifier for the parameter"
    )
    parameter_class: datatypes.OscalToken | None = Field(
        description="""
            A textual label that provides a characterization of the type, purpose, use or scope of 
            the parameter.
        """,
        default=None,
    )
    depends_on: datatypes.OscalToken | None = Field(
        description="""
            (deprecated) Another parameter invoking this one. This construct has been deprecated and 
            should not be used.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            Parameters provide a mechanism for the dynamic assignment of value(s) in a control.
        """,
        default=None,
    )
    links: list[common.Link] | None = Field(
        description="""
            A reference to a local or remote resource, that has a specific relation to the containing object.
        """,
        default=None,
    )
    label: datatypes.OscalMarkupLine | None = Field(
        description="""
            A short, placeholder name for the parameter, which can be used as a substitute for a value if 
            no value is assigned.
        """,
        default=None,
    )
    usage: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Describes the purpose and use of a parameter.
        """,
        default=None,
    )
    constraints: list[Constraint] | None = Field(
        description="""
            A formal or informal expression of a constraint or test.
        """,
        default=None,
    )
    guidelines: list[Guidelines] | None = Field(
        description="""
            A prose statement that provides a recommendation for the use of a parameter.
        """,
        default=None,
    )
    values: list[datatypes.OscalString] | None = Field(
        description="""
            A parameter value or set of values.
        """,
        default=None,
    )
    select: list[Select] | None = Field(
        description="""
            Presenting a choice among alternatives.
        """,
        default=None,
    )
    remarks: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Additional commentary about the containing object.
        """,
        default=None,
    )

    @field_validator("depends_on", mode="after")
    @classmethod
    def depends_on_deprecated(
        cls, depends_on: datatypes.OscalToken
    ) -> datatypes.OscalToken:
        # raise a DeprecationWarning if depends-on is present
        warnings.warn(
            "depends-on is a deprecated field for catalog", DeprecationWarning
        )
        return depends_on


class GenericPart(base.OscalModel):
    # Parts come in a few flavors - this GenericPart defines the field, and the subclasses provide
    # appropriate validation
    # TODO: make this an abstract base class
    id: datatypes.OscalToken | None = Field(
        description="""
            A unique identifier for the part.
        """,
        default=None,
    )
    name: datatypes.OscalToken = Field(
        description="""
            A textual label that uniquely identifies the part's semantic type, which exists in a 
            value space qualified by the ns.
        """,
    )
    ns: datatypes.OscalUri = Field(
        description="""
            An optional namespace qualifying the part's name. This allows different organizations 
            to associate distinct semantics with the same name.
        """,
        default=AnyUrl("http://csrc.nist.gov/ns/oscal"),
    )
    part_class: datatypes.OscalToken | None = Field(
        description="""
            An optional textual providing a sub-type or characterization of the part's name, or a 
            category to which the part belongs.
        """,
        default=None,
    )
    title: datatypes.OscalMarkupLine | None = Field(
        description="""
            An optional name given to the part, which may be used by a tool for display and navigation.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a namespace 
            qualified name/value pair.
        """,
        default=None,
    )
    prose: datatypes.OscalMarkupMultiline | None = Field(
        description="""
            Permits multiple paragraphs, lists, tables etc.
        """,
        default=None,
    )
    parts: list[Part | NestedPart] | None = Field(
        description="""
            An annotated, markup-based textual element of a control's or catalog group's definition, or 
            a child of another part.
        """,
        default=None,
    )
    links: list[common.Link] | None = Field(
        description="""
            A reference to a local or remote resource, that has a specific relation to the containing object.
        """,
        default=None,
    )


class Part(GenericPart):
    allowed_values: list[base.AllowedValue] = [
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
            ],
            "name": [
                datatypes.OscalToken("overview"),
                datatypes.OscalToken("statement"),
                datatypes.OscalToken("guidance"),
                datatypes.OscalToken("assessment"),
                datatypes.OscalToken("assessment-method"),
            ],
        }
    ]

    @model_validator(mode="after")
    def validate_nested_part(self) -> Part:
        if self.parts is not None:
            for sub_part in self.parts:
                if (
                    sub_part.name == datatypes.OscalToken("statement")
                    and sub_part.parts is not None
                ):
                    for nested_part in sub_part.parts:
                        if type(nested_part) != NestedPart:
                            raise ValueError(
                                "Nested parts under a Part with name 'statement' can only have a name value of 'item'"
                            )

        return self

    @field_validator("name", mode="after")
    @classmethod
    def assessment_deprecated(cls, name: datatypes.OscalToken) -> datatypes.OscalToken:
        # raise a deprecationwarning if name is 'assessment'
        warnings.warn(
            "'assessment' is a deprecated property value for name. Use 'assessment-method' instead",
            DeprecationWarning,
        )
        return name


class NestedPart(GenericPart):
    allowed_values: list[base.AllowedValue] = [
        {
            "ns": [
                datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
            ],
            "name": [
                datatypes.OscalToken("item"),
            ],
        }
    ]


class ControlLink(common.Link):
    allowed_values: list[base.AllowedValue] = [
        {
            "rel": [
                datatypes.OscalToken("reference"),
                datatypes.OscalToken("related"),
                datatypes.OscalToken("required"),
                datatypes.OscalToken("incorporated-into"),
                datatypes.OscalToken("moved-to"),
            ]
        }
    ]


class Control(base.OscalModel):
    # TODO: Constraints - https://pages.nist.gov/OSCAL-Reference/models/v1.1.0/catalog/json-reference/#/catalog/controls
    # INDEX HAS KEY for link[@rel=('related','required','incorporated-into','moved-to') and starts-with(@href,'#')]this value must correspond to a listing in the index catalog-groups-controls-parts using a key constructed of key field(s) @href

    id: datatypes.OscalToken = Field(
        description="""
            Identifies a control such that it can be referenced in the defining catalog 
            and other OSCAL instances (e.g., profiles).
        """
    )
    control_class: datatypes.OscalToken | None = Field(
        description="""
            A textual label that provides a sub-type or characterization of the control.
        """,
        default=None,
    )
    title: datatypes.OscalMarkupLine = Field(
        description="""
            A name given to the control, which may be used by a tool for display and navigation.
        """
    )
    params: list[Parameter] | None = Field(
        description="""
            Parameters provide a mechanism for the dynamic assignment of value(s) in a control.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair.
        """,
        default=None,
    )
    links: list[ControlLink] | None = Field(
        description="""
            A reference to a local or remote resource, that has a specific relation to the 
            containing object.
        """,
        default=None,
    )
    parts: list[Part] | None = Field(
        description="""
            An annotated, markup-based textual element of a control's or catalog group's definition, 
            or a child of another part.
        """,
    )
    controls: list[Control] | None = Field(
        description="""
            A structured object representing a requirement or guideline, which when implemented 
            will reduce an aspect of risk related to an information system and its information.
        """,
        default=None,
    )


class Group(base.OscalModel):
    id: datatypes.OscalToken | None = Field(
        description="""
            Identifies the group for the purpose of cross-linking within the defining instance or 
            from other instances that reference the catalog.
        """,
        default=None,
    )
    group_class: datatypes.OscalToken | None = Field(
        description="""
            A textual label that provides a sub-type or characterization of the group.
        """,
        default=None,
    )
    title: datatypes.OscalMarkupLine = Field(
        description=""" 
            A name given to the group, which may be used by a tool for display and navigation.
        """,
    )
    params: list[Parameter] | None = Field(
        description="""
            Parameters provide a mechanism for the dynamic assignment of value(s) in a control.
        """,
        default=None,
    )
    props: list[properties.BaseProperty] | None = Field(
        description="""
            An attribute, characteristic, or quality of the containing object expressed as a 
            namespace qualified name/value pair.
        """,
        default=None,
    )
    links: list[common.Link] | None = Field(
        description="""
            A reference to a local or remote resource, that has a specific relation to the containing object.
        """,
        default=None,
    )
    parts: list[Part] | None = Field(
        description="""
            An annotated, markup-based textual element of a control's or catalog group's definition, or a 
            child of another part.
        """,
        default=None,
    )
    groups: list[Group] | None = Field(
        description="""
            A group of controls, or of groups of controls.
        """,
        default=None,
    )
    controls: list[Control] | None = Field(
        description="""
            A group of controls, or of groups of controls.
        """,
        default=None,
    )


class Catalog(base.OscalModel):
    uuid: datatypes.OscalUUID
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
