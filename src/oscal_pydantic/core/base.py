from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
)

from typing import TYPE_CHECKING, NamedTuple, Literal, TypeAlias


from . import datatypes

AllowedValue: TypeAlias = dict[str, list[datatypes.OscalDatatype]]

if TYPE_CHECKING:
    from pydantic.main import IncEx


# To help with error reporting, we create a NamedTuple of the field, and the invalid value
class FieldError(NamedTuple):
    field: str
    expected_value: datatypes.OscalDatatype


class FieldStatus(NamedTuple):
    field: str
    status: Literal["match", "unchecked", "error"]
    error: FieldError | None


class AllowedValueStatus(NamedTuple):
    result: Literal["pass", "fail"]
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
        * Custom __init__ that supports definition of contextvars for constraints
    """

    _validation_results: list[AllowedValueStatus] = PrivateAttr(default=[])

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

    def base_validator(self, calling_type: type, allowed_values: list[AllowedValue]):
        self.validate_fields(allowed_values=allowed_values)

        if "pass" in [result.result for result in self._validation_results]:
            return self
        else:
            if type(self) == calling_type:
                raise ValueError(
                    self.print_validation_errors(
                        validation_errors=self.validation_errors()
                    )
                )
            else:
                # This may be called from a subclass. If so, return control up
                return self

    def validate_fields(
        self,
        allowed_values: list[dict[str, list[datatypes.OscalDatatype]]],
    ) -> None:
        av_status: list[AllowedValueStatus] = []
        model_dict = self.model_dump()
        for allowed_value_dict in allowed_values:
            # Set an initial AllowedValueStatus
            av_status_result = "pass"
            av_field_status: list[FieldStatus] = []
            for field in model_dict:
                # Does allowed_values specify a value for this field?
                if field in allowed_value_dict:
                    # Does the allowed value match the field contents?
                    if model_dict[field] in [
                        value.root for value in allowed_value_dict[field]
                    ]:
                        av_field_status.append(
                            FieldStatus(field=field, status="match", error=None)
                        )
                    # If not, record it as an error
                    else:
                        for expected_value in [
                            value for value in allowed_value_dict[field]
                        ]:
                            error = FieldError(
                                field=field, expected_value=expected_value
                            )
                            av_field_status.append(
                                FieldStatus(field=field, status="error", error=error)
                            )
                        # If any field fails, the entire AllowedValueStatus result is "fail"
                        av_status_result = "fail"
                # IF the field is not present in the allowed values dict, the field is unchecked
                else:
                    av_field_status.append(
                        FieldStatus(field=field, status="unchecked", error=None)
                    )

            av_status.append(
                AllowedValueStatus(
                    result=av_status_result, fields_status=av_field_status
                )
            )

        # Finally, add the list of AllowedValueStatus results created to our private Attribute
        self._validation_results.extend(av_status)

    def validation_errors(self) -> list[FieldError]:
        final_errors: list[FieldError] = []
        # If we passed any of the validations, the whole thing is okay
        successes = [
            status for status in self._validation_results if status.result == "pass"
        ]
        if len(successes) > 0:
            return final_errors

        # Otherwise, return a list of errors
        for result in self._validation_results:
            for status in result.fields_status:
                if status.error is not None:
                    final_errors.append(status.error)

        return final_errors

    def print_validation_errors(self, validation_errors: list[FieldError]) -> str:
        # Create strings for each error, separated by newlines
        return "\n".join(
            [
                f"Expected value {error.expected_value} for field {error.field}"
                for error in validation_errors
            ]
        )
