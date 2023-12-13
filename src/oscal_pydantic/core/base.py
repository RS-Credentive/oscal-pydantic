from __future__ import annotations

from pydantic import BaseModel, ConfigDict, model_validator

from typing import TYPE_CHECKING, NamedTuple, Literal, TypeAlias, Any, TypeVar


from . import datatypes

AllowedValue: TypeAlias = dict[str, list[datatypes.OscalDatatype]]

FieldType = TypeVar("FieldType", bound="OscalModel")

AllowedFieldTypes: TypeAlias = dict[str, list[Any]]


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
        validate_assignment=False,
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

    @classmethod
    def get_allowed_subfield_types(cls) -> list[AllowedFieldTypes]:
        allowed_subfield_types: list[AllowedFieldTypes] = []
        return allowed_subfield_types

    @model_validator(mode="after")
    def validate_subfield_types(self) -> OscalModel:
        if len(self.__class__.get_allowed_subfield_types()) > 0:
            return self.verify_subfields(self.__class__.get_allowed_subfield_types())
        else:
            return self

    def verify_subfields(
        self, allowed_subfields: list[AllowedFieldTypes]
    ) -> OscalModel:
        # Flatten the list of dicts into a single dict - merges separate lists
        # of possible field types to a single list
        flattened_restricted_fields: AllowedFieldTypes = {}
        for allowed_subfield in allowed_subfields:
            for field in allowed_subfield.keys():
                if field in flattened_restricted_fields.keys():
                    flattened_restricted_fields[field].extend(allowed_subfield[field])
                else:
                    flattened_restricted_fields[field] = allowed_subfield[field]

        # Walk through the fields and validate the values
        for field in flattened_restricted_fields:
            # Only check the field content if the field exists and is not None
            if getattr(self, field, None) is not None:
                field_object: Any | list[Any] = getattr(self, field)

                # Is the object already one of the correct types?
                if type(field_object) in flattened_restricted_fields[field]:
                    return self

                # If the field_object is not a list, process it as is
                if type(field_object) != list:
                    try:
                        # Check the field agains the profided type list. If a match is found,
                        # update the field object to represent the specific type.
                        setattr(
                            self,
                            field,
                            self.check_field_type(
                                field_object=field_object,
                                types_to_check=flattened_restricted_fields[field],
                            ),
                        )

                    except:
                        # If a value error is raised, the field could not be validated against any of the provided models
                        # That means that the field, and the entire object is invalid
                        raise ValueError(
                            f"Unable to validate {field} against types provided: {flattened_restricted_fields[field]}"
                        )

                # Otherwise, the field is a list. step through it and process all the elements
                else:
                    new_field_object = []
                    for item in field_object:
                        try:
                            new_field_object.append(
                                self.check_field_type(
                                    field_object=item,
                                    types_to_check=flattened_restricted_fields[field],
                                )
                            )
                        except:
                            raise ValueError(
                                f"Unable to validate {field} against types provided: {flattened_restricted_fields[field]}"
                            )

                    # if we get through list without errors, replace the existing list with new,
                    # precisely typed list.
                    setattr(self, field, new_field_object)

        # If we get through with no errors, return the updated object
        return self

    def check_field_type(self, field_object: Any, types_to_check: list[Any]) -> Any:
        if not isinstance(field_object, OscalModel):
            raise Exception(
                "Invalid Class provided to verification class - must be instance of OscalModel of subclass"
            )
        for type_to_check in types_to_check:
            if issubclass(type_to_check, OscalModel):
                if type(field_object) == type_to_check:
                    return field_object
                else:
                    try:
                        typed_object = type_to_check.model_validate(
                            field_object.model_dump()
                        )
                        return typed_object
                    except Exception as e:
                        pass
            else:
                raise Exception(
                    "Invalid class passed to verification function. All types to check must be subclasses of OscalModel"
                )

        raise Exception(
            "Unable to instantiate the provided object as any of the provided Models"
        )

    @model_validator(mode="after")
    def validate_with_classvars(self) -> OscalModel:
        if len(self.__class__.get_allowed_values()) > 0:
            return self.verify_allowed_values(self.__class__.get_allowed_values())
        else:
            return self

    def verify_allowed_values(self, allowed_values: list[AllowedValue]) -> OscalModel:
        # dump the current object to a dict
        this_object_dict = self.model_dump()

        # Get all the fields that are set on the model and are included
        # in the restricted attribute list
        fields_in_this_object = this_object_dict.keys()
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

        # Otherwise, we have to check the fields

        # Start by getting the restricted_field_set_dict
        restricted_field_set_dict = self.get_restricted_field_set_dict(
            allowed_values_list=allowed_values
        )

        # iterate through all of entries
        for restricted_field_set in restricted_field_set_dict.keys():
            # Find all of the allowed_values that are included in this restricted_file_set frozendict
            allowed_values_to_check = [
                a_v
                for a_v in allowed_values
                if restricted_field_set.issuperset(a_v.keys())
            ]

            # iterate through the allowed_values
            for allowed_value_dict in allowed_values_to_check:
                # iterate through the keys in the dict
                for field in allowed_value_dict.keys():
                    # if the field exists in this object and the value matches, set the corresponding restricted_field_set_dict to True
                    if (
                        field in this_object_dict.keys()
                        and this_object_dict[field] in allowed_value_dict[field]
                    ):
                        restricted_field_set_dict[restricted_field_set] = True

        # We have evaluated all of the allowed_values against the object. Now we confirm that every value test passed.
        if not False in restricted_field_set_dict.values():
            # if we passed all the tests, return the object
            return self
        else:
            # Create a list of of error strings to return with the error
            value_error_listing: list[str] = []

            # Get the set of fields for every failed test
            incorrect_value_sets = [
                r_field
                for r_field in restricted_field_set_dict.keys()
                if restricted_field_set_dict[r_field] == False
            ]

            # Loop through them to construct the value_error_listing string
            for incorrect_value_set in incorrect_value_sets:
                related_allowed_values = [
                    a_v
                    for a_v in allowed_values
                    if incorrect_value_set.issuperset(a_v.keys())
                ]
                for related_allowed_value in related_allowed_values:
                    for key, value in related_allowed_value.items():
                        value_error_listing.append(
                            f"{key} may have one of the values {value}"
                        )

            raise ValueError("Incorrect value(s)" + "\n".join(value_error_listing))

    @classmethod
    def flatten_allowed_value_keys_lists(
        cls,
        allowed_values_list: list[AllowedValue],
    ) -> list[str]:
        key_list: list[str] = []
        for allowed_value in allowed_values_list:
            key_list += allowed_value.keys()

        return key_list

    @classmethod
    def get_restricted_field_set_dict(
        cls, allowed_values_list: list[AllowedValue]
    ) -> dict[frozenset[str], bool]:
        # Start by identifying the set of fields with restrictions in the "Allowed Value" list.
        # We use a 'set' to avoid duplicates, and we use 'frozenset' because a frozenset can be a dictionary key.
        restricted_fields: set[frozenset[str]] = set()
        for allowed_value in allowed_values_list:
            if len(restricted_fields) == 0:
                # if the restricted fields set is empty, no point in doing anything else
                # add this item and move on
                restricted_fields.add(frozenset(allowed_value))
            else:
                allowed_value_fs = frozenset(allowed_value.keys())
                for restricted_field in restricted_fields:
                    if allowed_value_fs.issubset(restricted_field):
                        # Don't add this to the list - it or a superset of it exists in the list already
                        # Note that a set is always a subset of itself, so this checks for equality as well
                        break
                    elif restricted_field.issubset(allowed_value_fs):
                        # If allowed_value_fs is a superset of restricted_field,
                        # replace restricted_fiedl with allowed_value_fs
                        restricted_fields.remove(restricted_field)
                        restricted_fields.add(allowed_value_fs)
                        break
                    else:
                        # this allowed_value is not related to any of the other fields,
                        # add ist to the restricted_fields set
                        restricted_fields.add(allowed_value_fs)
                        break

        # Now we have a set of attributes that need to be compared as groups.
        # Build a dictionary with the keys of the attribute sets, and a value of bool
        # if the bool is True, the values passed in have been successfully validated,
        # Otherwise they have not.
        return dict.fromkeys(restricted_fields, False)
