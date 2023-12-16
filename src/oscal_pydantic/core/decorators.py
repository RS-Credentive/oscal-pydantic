from typing import Callable, Any
from . import base

import functools


def restricted_class(cls):
    @functools.wraps(cls)
    def get_class_restrictions(*args, **kwargs):
        get_allowed_field_values: list[
            base.AllowedValue
        ] = cls.get_allowed_field_values()
        if cls == base.BaseModel:
            return
