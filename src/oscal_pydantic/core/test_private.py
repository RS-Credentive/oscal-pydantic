from __future__ import annotations

from pydantic import BaseModel, PrivateAttr, Field, model_validator

from typing import Any, Self


class PrivateBase(BaseModel):
    _default_private: list[str] = PrivateAttr(default=[])
    _explicit_private: list[str]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._explicit_private = []

    def show_private(self) -> str:
        print(f"_default_private has {len(self._default_private)} elements")
        print(f"_explicit_private has {len(self._explicit_private)} elements")
        return "OK"

    def dependent_validation(self) -> Self:
        if len(self._default_private) > 0 and len(self._explicit_private) > 0:
            print("Class is Valid")
            return self
        else:
            print("failed validation")
            raise ValueError("you have to add a value to the private variable")


class PrivateSubNoValidator(PrivateBase):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._default_private.append("sub.default")
        self._explicit_private.append("sub.explicit")


class PrivateSubClass(PrivateBase):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._default_private.append("sub.default")
        self._explicit_private.append("sub.explicit")

    @model_validator(mode="after")
    def validate_subclass(self) -> PrivateSubClass:
        print("Beginning validation of model for class" + str(self.__class__))
        return self.dependent_validation()


print("\n#####\n")

try:
    print("Attempting to create private_base")
    private_base = PrivateBase()
    print("Successfully created private_base")
except Exception as e:
    print(e)

try:
    private_base.show_private()
except Exception as e:
    print(e)

print("\n#####\n")

try:
    print("Attempting to create private_sub_nv")
    private_sub_nv = PrivateSubNoValidator()
    print("Successfully created private_sub_nv")
except Exception as e:
    print(e)

try:
    print(private_sub_nv._default_private)
    print(private_sub_nv._explicit_private)
    private_sub_nv.show_private()
    print("Running the validation function, but not decorated as @model_validator")
    print(str(private_sub_nv.dependent_validation()))
except Exception as e:
    print(e)

print("\n#####\n")

try:
    print(
        "Attempting to create private_sub, which runs the validation function as a decoratd model_validator"
    )
    private_sub = PrivateSubClass()
    print("Successfully created private_sub")
except Exception as e:
    print(e)

try:
    print(private_sub._default_private)
    print(private_sub._explicit_private)
    private_sub.show_private()
except Exception as e:
    print(e)

"""
OUTPUT:


#####

Attempting to create private_base
Successfully created private_base
_default_private has 0 elements
_explicit_private has 0 elements

#####

Attempting to create private_sub_nv
Successfully created private_sub_nv
['sub.default']
['sub.explicit']
_default_private has 1 elements
_explicit_private has 1 elements
Running the validation function, but not decorated as @model_validator
Class is Valid


#####

Attempting to create private_sub, which runs the validation function as a decoratd model_validator
Beginning validation of model for class<class '__main__.PrivateSubClass'>
failed validation
1 validation error for PrivateSubClass
  Value error, you have to add a value to the private variable [type=value_error, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.1/v/value_error
name 'private_sub' is not defined

"""


# class PrivateSubSubClass(PrivateSubClass):
#     def __init__(self, **data: Any) -> None:
#         super().__init__(**data)
#         self._default_private.append("sub.sub.default")
#         self._explicit_private.append("sub.sub.explicit")


# class PrivateSkipClass(PrivateBase):
#     id: str = Field()


# class PrivateSubSkip(PrivateSkipClass):
#     def __init__(self, **data: Any) -> None:
#         super().__init__(**data)
#         self._default_private.append("subskip.default")
#         self._explicit_private.append("subskip.explicit")


# try:
#     private_sub_sub = PrivateSubSubClass()
#     print("Successfully created private_sub")
# except Exception as e:
#     print(e)
#     exit()
# print(private_sub_sub._default_private)
# print(private_sub_sub._explicit_private)
# private_sub_sub.shared_function()

# try:
#     private_subskip = PrivateSubSkip(id="private_sub_skip")
#     print("Successfully created private_sub")
# except Exception as e:
#     print(e)
#     exit()
# print(private_subskip._default_private)
# print(private_subskip._explicit_private)
# private_subskip.shared_function()
