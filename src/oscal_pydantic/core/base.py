from __future__ import annotations

from pydantic import BaseModel, ConfigDict, model_validator, ValidationInfo

from typing import TYPE_CHECKING, NamedTuple, Literal, TypeAlias, ClassVar


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

    @model_validator(mode="after")
    def validate_with_context(self, info: ValidationInfo) -> OscalModel:
        # If no context object is set, or it's not a list of AllowedValues,
        # there are no restrictions to check. Return immediately
        if not info.context or type(info.context) != list[AllowedValue]:
            return self

        # Otherwise check
        else:
            # Initialize the allowed_values dict containing fields and allowed values
            allowed_values: list[AllowedValue] = info.context

            # dump the current object to a dict
            this_object = self.model_dump()

            # Get all the fields that are set on the model and are included
            # in the restricted attribute list
            fields_in_this_object = this_object.keys()
            restricted_fields = self.flatten_allowed_value_keys_lists(
                allowed_values=allowed_values
            )
            restricted_fields_in_this_object = [
                field for field in fields_in_this_object if field in restricted_fields
            ]

            # If none of the fields in this object are subject to a restriction, the object
            # is valid. Return immediately
            if len(restricted_fields_in_this_object) == 0:
                return self

            # Otherwise, iterate through the allowed values list
            for allowed_value in allowed_values:
                # See if the allowed value doesn't include any of the restricted fields in this object
                # If it doesn't, move to the next allowed value
                if restricted_fields_in_this_object not in allowed_value.keys():
                    break
                else:
                    # Set a temp variable - does this particular object comply with the restrictions
                    # in this particular allowed value
                    this_object_complies_with_this_allowed_value: bool = True

                    # Check the object field against every restricted field in the allowed_value
                    for field in allowed_value.keys():
                        # If the value in the field is not an allowed value, we have failed the whole check
                        if this_object[field] not in allowed_value[field]:
                            this_object_complies_with_this_allowed_value = False
                            # TODO: Can we just break out of the enclosing 'if' here? Would speed things up.

                    # If we've checked every field and haven't found a problem, then the object passes the
                    # restriction and we can stop looking - return self to exit succesfully
                    if this_object_complies_with_this_allowed_value:
                        return self

            # If we get here, we checked all of the allowed values and none of them passed, so we throw a
            # ValueError with the information about the allowed value restrictions
            raise ValueError(
                "Object did not meets Allowed value restrictions. "
                + str(allowed_values)
            )

    def verify_allowed_values(self, allowed_values: list[AllowedValue]) -> OscalModel:
        # dump the current object to a dict
        this_object = self.model_dump()

        # Get all the fields that are set on the model and are included
        # in the restricted attribute list
        fields_in_this_object = this_object.keys()
        restricted_fields = self.flatten_allowed_value_keys_lists(
            allowed_values=allowed_values
        )
        restricted_fields_in_this_object = [
            field for field in fields_in_this_object if field in restricted_fields
        ]

        # If none of the fields in this object are subject to a restriction, the object
        # is valid. Return immediately
        if len(restricted_fields_in_this_object) == 0:
            return self

        # Otherwise, iterate through the allowed values list
        for allowed_value in allowed_values:
            # See if the allowed value doesn't include any of the restricted fields in this object
            # If it doesn't, move to the next allowed value
            if restricted_fields_in_this_object not in allowed_value.keys():
                break
            else:
                # Set a temp variable - does this particular object comply with the restrictions
                # in this particular allowed value
                this_object_complies_with_this_allowed_value: bool = True

                # Check the object field against every restricted field in the allowed_value
                for field in allowed_value.keys():
                    # If the value in the field is not an allowed value, we have failed the whole check
                    if this_object[field] not in allowed_value[field]:
                        this_object_complies_with_this_allowed_value = False
                        # TODO: Can we just break out of the enclosing 'if' here? Would speed things up.

                # If we've checked every field and haven't found a problem, then the object passes the
                # restriction and we can stop looking - return self to exit succesfully
                if this_object_complies_with_this_allowed_value:
                    return self

        # If we get here, we checked all of the allowed values and none of them passed, so we throw a
        # ValueError with the information about the allowed value restrictions
        raise ValueError(
            "Object did not meets Allowed value restrictions. " + str(allowed_values)
        )

    def flatten_allowed_value_keys_lists(
        self,
        allowed_values: list[AllowedValue],
    ) -> list[str]:
        key_list: list[str] = []
        for allowed_value in allowed_values:
            key_list += allowed_value.keys()

        return key_list
