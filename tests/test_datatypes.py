import pytest

from typing import Any

from pydantic import TypeAdapter

from oscal_pydantic.core import datatypes


class TestDatatypes:
    def test_oscal_boolean_true(self, get_truthy_data: list[Any]):
        # Check the truthy values
        for item in get_truthy_data:
            assert TypeAdapter(datatypes.OscalBool).validate_python(item)

    def test_oscal_boolean_false(self, get_falsey_data: list[Any]):
        # Check the falsy values
        for item in get_falsey_data:
            assert not TypeAdapter(datatypes.OscalBool).validate_python(item)

    def test_oscal_boolean_junk(self, get_junk_bool_list: list[Any]):
        for item in get_junk_bool_list:
            with pytest.raises(ValueError):
                TypeAdapter(datatypes.OscalBool).validate_python(item)

    def test_oscal_decimal_good(self, get_test_float_list: list[float]):
        for float_value in get_test_float_list:
            assert isinstance(
                TypeAdapter(datatypes.OscalDecimal).validate_python(float_value), float
            )

    # TODO: define function to test creating decimal from junk data

    def test_oscal_int_good(self, get_test_int_list: list[int]):
        for int_value in get_test_int_list:
            assert isinstance(
                TypeAdapter(datatypes.OscalInteger).validate_python(int_value), int
            )

    def test_oscal_non_negative_int_good(self, get_non_negative_int: int):
        assert isinstance(
            TypeAdapter(datatypes.OscalNonNegativeInteger).validate_python(
                get_non_negative_int
            ),
            int,
        )

    def test_oscal_zero_is_non_negative_int(self):
        assert isinstance(
            TypeAdapter(datatypes.OscalNonNegativeInteger).validate_python(0), int
        )

    def test_oscal_positive_int_good(self, get_positive_int: int):
        assert isinstance(
            TypeAdapter(datatypes.OscalNonNegativeInteger).validate_python(
                get_positive_int
            ),
            int,
        )

    def test_oscal_base64_binary_good(self, get_random_base64_string: bytes):
        assert isinstance(
            TypeAdapter(datatypes.OscalBase64Binary).validate_python(
                str(get_random_base64_string)
            ),
            str,
        )

    def test_oscal_date_good(self, get_random_date_string: str):
        assert isinstance(
            TypeAdapter(datatypes.OscalDate).validate_python(get_random_date_string),
            str,
        )

    def test_oscal_datetime_good(self, get_random_datetime_string: str):
        assert isinstance(
            TypeAdapter(datatypes.OscalDateTime).validate_python(
                get_random_datetime_string
            ),
            str,
        )
