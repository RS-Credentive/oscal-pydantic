from __future__ import annotations

from .core import base, common, datatypes, properties

from pydantic import Field, field_validator, AnyUrl


import warnings


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
        default=datatypes.OscalToken("one"),
    )
    choice: list[datatypes.OscalMarkupLine] | None = Field(
        description="""
             A value selection among several such options.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "how_many": [
                    datatypes.OscalToken("one"),
                    datatypes.OscalToken("one-or-more"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


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
    select: Select | None = Field(
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

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalParameterProperty,
                    properties.RmfParameterProperty,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class BasePart(base.OscalModel):
    # Parts come in a few flavors - this BasePart defines the fields, and the subclasses provide
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
    parts: list[BasePart] | None = Field(
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

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalPartProperty,
                    properties.OscalAssessmentMethodProperty,
                    properties.RmfAssessmentMethodProperty,
                ],
            },
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class OscalPart(BasePart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "ns": [
                    datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class StatementPart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("statement"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "parts": [
                    StatementItemPart,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class StatementItemPart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("item"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "parts": [
                    StatementItemPart,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class GuidancePart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("guidance"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class AssessmentObjectivePart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("assessment-objective"),
                    datatypes.OscalToken("objective"),  # TODO: Deprecated
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @field_validator("name", mode="after")
    @classmethod
    def assessment_deprecated(cls, name: datatypes.OscalToken) -> datatypes.OscalToken:
        # raise a deprecationwarning if name is 'assessment'
        if name == datatypes.OscalToken("objective"):
            warnings.warn(
                "'objective' is a deprecated property value for name. Use 'assessment-objective' instead",
                DeprecationWarning,
            )
        return name

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "parts": [
                    AssessmentObjectivePart,
                ]
            }
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class AssesmentMethodPart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("assessment"),
                    datatypes.OscalToken("assessment-method"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values

    @field_validator("name", mode="after")
    @classmethod
    def assessment_deprecated(cls, name: datatypes.OscalToken) -> datatypes.OscalToken:
        # raise a deprecationwarning if name is 'assessment'
        if name == datatypes.OscalToken("assessment"):
            warnings.warn(
                "'assessment' is a deprecated property value for name. Use 'assessment-method' instead",
                DeprecationWarning,
            )
        return name

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "parts": [
                    AssessmentObjectPart,
                ]
            },
            {
                "props": [
                    properties.OscalAssessmentMethodProperty,
                ]
            },
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


class AssessmentObjectPart(OscalPart):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "name": [
                    datatypes.OscalToken("assessment-objects"),
                    datatypes.OscalToken("objects"),  # TODO: Deprecated
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


class ControlLink(common.Link):
    @classmethod
    def get_allowed_field_values(cls) -> list[base.AllowedValue]:
        allowed_values: list[base.AllowedValue] = [
            {
                "rel": [
                    datatypes.OscalToken("reference"),
                    datatypes.OscalToken("related"),
                    datatypes.OscalToken("required"),
                    datatypes.OscalToken("incorporated-into"),
                    datatypes.OscalToken("moved-to"),
                ],
            },
        ]
        allowed_values.extend(super().get_allowed_field_values())
        return allowed_values


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
    parts: list[BasePart] | None = Field(
        description="""
            An annotated, markup-based textual element of a control's or catalog group's definition, 
            or a child of another part.
        """,
        default=None,
    )
    controls: list[Control] | None = Field(
        description="""
            A structured object representing a requirement or guideline, which when implemented 
            will reduce an aspect of risk related to an information system and its information.
        """,
        default=None,
    )

    @classmethod
    def get_allowed_subfield_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalControlProperty,
                ],
            },
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


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
    parts: list[BasePart] | None = Field(
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

    @classmethod
    def get_allowed_field_types(cls) -> list[base.AllowedFieldTypes]:
        allowed_field_types: list[base.AllowedFieldTypes] = [
            {
                "props": [
                    properties.OscalControlProperty,
                    properties.OscalGroupProperty,
                ],
            },
        ]
        allowed_field_types.extend(super().get_allowed_field_types())
        return allowed_field_types


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
