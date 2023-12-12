from .catalog import Catalog
from .core import base

from pydantic import Field


class Document(base.OscalModel):
    catalog: Catalog | None = Field(default=None)
