from contextlib import contextmanager
from contextvars import ContextVar
from . import datatypes, common


class AllowedValue:
    # A Dict of allowed values and an optional bool determining whether
    allowed_values: dict[str, list[datatypes.OscalDatatype]]
    allow_others: bool


class OscalValidationContext(ContextVar):
    def __enter__(self) -> None:
        pass

    def __exit__(self) -> None:
        pass
