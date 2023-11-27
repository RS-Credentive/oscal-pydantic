import pytest
import random
import string
import sys
from typing import Any, Optional


def filter_by_type(item: Any, filtered_type: type) -> Any:
    if isinstance(item, filtered_type):
        raise Exception("Wrong Type Try Again")
    else:
        return item


@pytest.fixture
def get_test_string() -> str:
    """return a test random test string containing any printable character"""
    return "".join(
        random.sample(string.printable, k=random.randint(0, len(string.printable)))
    )


@pytest.fixture
def get_test_string_list(get_test_string: str) -> list[str]:
    """return a list of five test strings"""
    junk_strings: list[str] = []
    for _ in range(5):
        junk_strings.append(get_test_string)
    return junk_strings


@pytest.fixture
def get_test_int() -> int:
    """return a random int"""
    return random.randint(-sys.maxsize, sys.maxsize)


@pytest.fixture
def get_test_int_list(get_test_int: int) -> list[int]:
    """return a list of five test ints"""
    junk_ints: list[int] = []
    for _ in range(5):
        junk_ints.append(get_test_int)
    return junk_ints


@pytest.fixture
def get_test_float() -> float:
    """return a random float"""
    return random.uniform(sys.maxsize, -sys.maxsize)


@pytest.fixture
def get_test_float_list(get_test_float: float) -> list[float]:
    """return a list of five random flotas"""
    junk_floats: list[float] = []
    for _ in range(5):
        junk_floats.append(get_test_float)
    return junk_floats


@pytest.fixture
def get_junk_data(
    get_test_float: float,
    get_test_int: int,
    get_test_string: str,
) -> list[Any]:
    """get a random item from all of the types provided by any test fixture"""
    return random.sample(
        population=[get_test_float, get_test_int, get_test_string], k=1
    )


def get_junk_data_list(get_junk_data: Any) -> list[Any]:
    junk_data_list: list[Any] = []
    for _ in range(5):
        junk_data_list.append(get_junk_data)
    return junk_data_list


@pytest.fixture
def get_truthy_data() -> list[int | str]:
    """get a list of all objects that should be a valid and true OscalBoolean"""
    return [1, "1", True, "true"]


@pytest.fixture
def get_falsey_data() -> list[int | str]:
    """get a list of all items that should be a valid and false OscalBoolean"""
    return [0, "0", False, "false"]


@pytest.fixture
def get_junk_bool_list(
    get_test_float: float,
    get_test_int: int,
    get_test_string: str,
    get_falsey_data: list[int | str],
    get_truthy_data: list[int | str],
) -> list[Any]:
    """get a list of five items that should be invalid OscalBoolean"""
    junk_bools: list[Any] = []
    while len(junk_bools) <= 5:
        item: Any = random.sample(
            population=[get_test_float, get_test_int, get_test_string], k=1
        )
        if item not in get_truthy_data and item not in get_falsey_data:
            junk_bools.append(item)
    return junk_bools


@pytest.fixture
def get_non_negative_int(get_test_int: int) -> int:
    return random.randint(0, sys.maxsize)


@pytest.fixture
def get_positive_int(get_test_int: int) -> int:
    return random.randint(1, sys.maxsize)
