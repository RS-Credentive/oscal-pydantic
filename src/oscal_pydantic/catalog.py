# Common elements shared by all Models: Metadata, Back Matter
from __future__ import annotations
from enum import Enum

from . import core, common

from pydantic import RootModel, Field


class Expression(RootModel[str]):
    root: str = Field(description="A formal (executable) expression of a constraint.")


class Test(core.OscalModel):
    expression: Expression
    remarks: core.Remarks | None = Field(default=None)


class Constraint(core.OscalModel):
    description: core.MarkupMultiline | None = Field(
        default=None,
        description="A formal or informal expression of a constraint or test.",
    )
    tests: list[Test] | None = Field(
        default=None,
        description="A list of test expressions which are expected to be evaluated by a tool.",
    )


class Guideline(core.OscalModel):
    prose: core.MarkupMultiline = Field(
        description="A prose statement that provides a recommendation for the use of a parameter."
    )


class Value(RootModel[str]):
    root: str = Field(
        description="Indicates the value of the attribute, characteristic, or quality."
    )


class SelectionHowManyEnum(str, Enum):
    one = "one"
    one_or_more = "one-or-more"


class Selection(core.OscalModel):
    how_many: SelectionHowManyEnum | None = Field(
        default=None,
        description="Describes the number of selections that must occur. Without this setting, only one value should be assumed to be permitted.",
    )
    choice: list[core.MarkupLine] | None = Field(
        default=None, description="A value selection among several such options."
    )


class Parameter(core.OscalModel):
    id: core.Token = Field(
        description="A human-oriented, locally unique identifier with cross-instance scope that can be used to reference this defined parameter elsewhere in this or other OSCAL instances. When referenced from another OSCAL instance, this identifier must be referenced in the context of the containing resource (e.g., import-profile). This id should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document."
    )
    parameter_class: core.Token | None = Field(  # Named "parameter_class" instead of "class" which is a reserved word in python
        default=None,
        description="A textual label that provides a characterization of the parameter.",
        alias="class",
    )
    props: list[core.Property] | None = Field(
        default=None,
        description="An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair.",
    )
    links: list[core.Link] | None = Field(
        default=None,
        description="A reference to a local or remote resource, that has a specific relation to the containing object.",
    )
    label: core.MarkupLine | None = Field(
        default=None,
        description="A short, placeholder name for the parameter, which can be used as a substitute for a value if no value is assigned.",
    )
    usage: core.MarkupMultiline | None = Field(
        default=None, description="Describes the purpose and use of a parameter."
    )
    constraints: list[Constraint] | None = Field(
        default=None,
        description="A formal or informal expression of a constraint or test.",
    )
    guidelines: list[Guideline] | None = Field(default=None)
    values: list[Value] | None = Field(default=None)
    select: Selection | None = Field(
        default=None, description="Presenting a choice among alternatives."
    )
    remarks: core.MarkupMultiline | None = Field(
        default=None, description="Additional commentary about the containing object.+"
    )


class Part(core.OscalModel):
    id: core.Token | None = Field(
        default=None,
        description="A human-oriented, locally unique identifier with cross-instance scope that can be used to reference this defined part elsewhere in this or other OSCAL instances. When referenced from another OSCAL instance, this identifier must be referenced in the context of the containing resource (e.g., import-profile). This id should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document.",
    )
    name: core.Token = Field(
        description="A textual label that uniquely identifies the part's semantic type."
    )
    ns: core.UrlReference | None = Field(
        default=None,
        description="A namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name.",
    )
    part_class: core.Token | None = Field(
        default=None,
        description="A textual label that provides a sub-type or characterization of the part's name. This can be used to further distinguish or discriminate between the semantics of multiple parts of the same control with the same name and ns.",
        alias="class",
    )
    title: core.MarkupLine | None = Field(
        default=None,
        description="A name given to the part, which may be used by a tool for display and navigation.",
    )
    props: list[core.Property] | None = Field(default=None)
    prose: core.MarkupMultiline | None = Field(default=None)
    parts: list[Part] | None = Field(default=None)
    links: list[core.Link] | None = Field(default=None)


class Control(core.OscalModel):
    id: core.Token = Field(
        description="A human-oriented, locally unique identifier with instance scope that can be used to reference this control elsewhere in this and other OSCAL instances (e.g., profiles). This id should be assigned per-subject, which means it should be consistently used to identify the same control across revisions of the document."
    )
    control_class: core.Token | None = Field(
        default=None,
        description="A textual label that provides a sub-type or characterization of the control.",
        alias="class",
    )
    title: core.MarkupLine = Field(
        description="A name given to the control, which may be used by a tool for display and navigation."
    )
    params: list[Parameter] | None = Field(
        default=None,
        description="Parameters provide a mechanism for the dynamic assignment of value(s) in a control.",
    )
    props: list[core.Property] | None = Field(
        default=None,
    )
    links: list[core.Link] | None = Field(default=None)
    parts: list[Part] | None = Field(default=None)
    controls: list[Control] | None = Field(default=None)


class Group(core.OscalModel):
    id: core.Token | None = Field(
        default=None,
        description="A human-oriented, locally unique identifier with cross-instance scope that can be used to reference this defined group elsewhere in in this and other OSCAL instances (e.g., profiles). This id should be assigned per-subject, which means it should be consistently used to identify the same group across revisions of the document.",
    )
    group_class: core.Token | None = Field(
        default=None,
        alias="class",
        description="A textual label that provides a sub-type or characterization of the group.",
    )
    title: core.MarkupLine = Field(
        description="A name given to the group, which may be used by a tool for display and navigation."
    )
    params: list[Parameter] | None = Field(
        default=None,
        description="Parameters provide a mechanism for the dynamic assignment of value(s) in a control.",
    )
    props: list[core.Property] | None = Field(default=None)
    links: list[core.Link] | None = Field(default=None)
    parts: list[Part] | None = Field(default=None)
    groups: list[Group] | None = Field(default=None)
    controls: list[Control] | None = Field(default=None)


class Catalog(core.OscalModel):
    uuid: core.UUID = Field(
        description="A globally unique identifier with cross-instance scope for this catalog instance. This UUID should be changed when this document is revised."
    )
    metadata: common.Metadata
    params: list[Parameter] | None = Field(
        default=None,
        description="Parameters provide a mechanism for the dynamic assignment of value(s) in a control.",
    )
    controls: list[Control] | None = Field(
        default=None,
        description="A structured information object representing a security or privacy control. Each security or privacy control within the Catalog is defined by a distinct control instance.",
    )
    groups: list[Group] | None = Field(
        default=None, description="A group of controls, or of groups of controls."
    )
    back_matter: common.BackMatter | None = Field(
        default=None,
        description="A collection of resources, which may be included directly or by reference.",
    )
