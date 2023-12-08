from __future__ import annotations

from pydantic import BaseModel, ConfigDict, model_validator

from typing import TYPE_CHECKING, NamedTuple, Literal, TypeAlias


from . import datatypes

AllowedValue: TypeAlias = dict[str, list[datatypes.OscalDatatype]]


if TYPE_CHECKING:
    from pydantic.main import IncEx

    pass_fail: TypeAlias = Literal["pass", "fail"]


# To help with error reporting, we create a NamedTuple of the field, and the invalid value
class FieldError(NamedTuple):
    field: str
    expected_value: datatypes.OscalDatatype


class FieldStatus(NamedTuple):
    field: str
    status: Literal["match", "unchecked", "error"]
    error: FieldError | None


class AllowedValueStatus(NamedTuple):
    result: pass_fail
    fields_status: list[FieldStatus]


# Helper function to convert python_variable_name to json-attribute-name
def oscal_aliases(string: str) -> str:
    wordlist = string.split("_")
    if wordlist[-1] == "class":
        # if the original is a variant of "XXX_class", the attribute should be called "class"
        return "class"
    else:
        # otherwise just replace the "_" with "-"
        return "-".join(word for word in string.split("_"))


class OscalModel(BaseModel):
    """
    A utility class that defines default behaviors for all other Models:
        * Extra values forbidden
        * populate by name rather than alias
        * Validate assignments by default
        * Use a common alias generator to convert "XXX_class" to "class" and change underscores to hyphens
        * When exporting json, exclude any attributes set to "None"
        * Includes a generic function to validate restrictions
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
        alias_generator=oscal_aliases,
    )

    # Override default model_dump_json to include indentation, exclude null values and always use alias
    def model_dump_json(
        self,
        *,
        indent: int | None = 4,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super().model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )

    @classmethod
    def get_allowed_values(cls) -> list[AllowedValue]:
        allowed_values: list[AllowedValue] = []
        return allowed_values

    @model_validator(mode="after")
    def validate_with_classvars(self) -> OscalModel:
        return self.verify_allowed_values(self.__class__.get_allowed_values())

    def verify_allowed_values(self, allowed_values: list[AllowedValue]) -> OscalModel:
        # dump the current object to a dict
        this_object = self.model_dump()

        # Get all the fields that are set on the model and are included
        # in the restricted attribute list
        fields_in_this_object = this_object.keys()
        restricted_fields = self.flatten_allowed_value_keys_lists(
            allowed_values_list=allowed_values
        )
        restricted_fields_in_this_object = [
            field for field in fields_in_this_object if field in restricted_fields
        ]

        # If none of the fields in this object are subject to a restriction, the object
        # is valid. Return immediately
        if len(restricted_fields_in_this_object) == 0:
            return self

        invalid_fields: list[str] = []
        # Otherwise, iterate through the allowed values list
        for allowed_value in allowed_values:
            # Get the list of values to check, e.g. fields in the object that are restricted fields
            values_to_check = list(
                set(restricted_fields_in_this_object).intersection(allowed_value.keys())
            )
            # If the allowed value doesn't include any of the restricted fields in this object
            # move to the next allowed value
            if len(values_to_check) == 0:
                break
            else:
                # Check the object field against every restricted field in the allowed_value
                for field in allowed_value:
                    # If the value in the field is not an allowed value, we have failed the whole check
                    if this_object[field] not in allowed_value[field]:
                        invalid_fields.append(
                            f"{field} value was {this_object[field]}.\n Should be one of {allowed_value[field]}"
                        )

        if len(invalid_fields) > 0:
            error_string = "Incorrect value(s) specified in Object:\n"
            for invalid_field in invalid_fields:
                error_string += f"{invalid_field}\n"
            raise ValueError(error_string)
        else:
            return self

    def flatten_allowed_value_keys_lists(
        self,
        allowed_values_list: list[AllowedValue],
    ) -> list[str]:
        key_list: list[str] = []
        for allowed_value in allowed_values_list:
            key_list += allowed_value.keys()

        return key_list
