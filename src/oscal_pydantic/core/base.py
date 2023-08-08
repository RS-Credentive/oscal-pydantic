from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
)

from typing import TYPE_CHECKING, NamedTuple

from . import datatypes

if TYPE_CHECKING:
    from pydantic.main import IncEx


# To help with error reporting, we create a NamedTuple of the field, and the invalid value
class FieldError(NamedTuple):
    field: str
    value: datatypes.OscalDatatype


class FieldStatus(NamedTuple):
    field: str
    status: str
    error: FieldError | None


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
        * Custom __init__ that supports definition of contextvars for constraints
    """

    _validation_results: list[FieldStatus] = PrivateAttr(default=[])

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

    def validate_fields(
        self, allowed_values: dict[str, list[datatypes.OscalTypeVar]]
    ) -> list[FieldStatus]:
        field_status: list[FieldStatus] = []
        model_dict = self.model_dump()
        for field in model_dict:
            # Has the field already passed a check at a lower level(superclass)
            if field in [
                matched_field.field
                for matched_field in self._validation_results
                if matched_field.status == "match"
            ]:
                # IF so, just move on to the next field
                pass
            else:
                # Does allowed_values specify a value for this field?
                if field in allowed_values:
                    # Does the allowed value match the field contents?
                    if model_dict[field] in [
                        value.root for value in allowed_values[field]
                    ]:
                        field_status.append(
                            FieldStatus(field=field, status="match", error=None)
                        )
                    # If not, record it as an error
                    else:
                        error = FieldError(field, model_dict[field])
                        field_status.append(
                            FieldStatus(field=field, status="error", error=error)
                        )
                # IF the field is not present in the allowed values dict, the field is unchecked
                else:
                    field_status.append(
                        FieldStatus(field=field, status="unchecked", error=None)
                    )

        # after cycling through all the fields, return the field status list
        return field_status

    def print_validation_errors(self, validation_errors: list[FieldError]) -> str:
        # Create strings for each error, separated by newlines
        return "\n".join(
            [
                f"Invalid value {error.value} for field {error.field}"
                for error in validation_errors
            ]
        )
