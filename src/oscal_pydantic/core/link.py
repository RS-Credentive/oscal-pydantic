# Reuseable base classes for core data types
from __future__ import annotations

from pydantic import (
    RootModel,
    Field,
    AnyUrl,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from .datatypes import Token, MarkupLine
from .base import OscalModel


class Relation(RootModel[Token]):
    root: Token = Field(
        description="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose."
    )


class FragmentIdentifier(RootModel[str]):
    root: str = Field(pattern=r"^#(.*)$")


class UrlReference(RootModel[AnyUrl | FragmentIdentifier]):
    root: AnyUrl | FragmentIdentifier


class Link(OscalModel):
    href: UrlReference = Field(description="A reference to a local or remote resource")
    rel: Relation | None = Field(default=None)
    media_type: str | None = Field(
        description="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.",
        default=None,
    )
    resource_fragment: str | None = Field(
        description="In case where the href points to a back-matter/resource, this value will indicate the URI fragment to append to any rlink associated with the resource. This value MUST be URI encoded.",
        default=None,
    )
    text: MarkupLine | None = Field(default=None)
