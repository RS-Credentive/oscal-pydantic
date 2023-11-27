from __future__ import annotations

import uuid
from typing import Any, Union, Annotated

from pydantic import (
    NonNegativeInt,
    PositiveInt,
    EmailStr,
    AnyUrl,
    BeforeValidator,
    AfterValidator,
    constr,
)


def validate_bool(v: Any) -> bool:
    """
    validate_bool additional validation for OSCAL flavor of bool. We only accept "true" or "1" or 1 as True,
    "false" or "0" or 0 as false. This function enforces that restriction.

    Args:
        v (Any): The input to be validated. It will be a bool if constructed from python,
        it may be a bool or int if constructed from XML, and will be a str if parsed from json.
        info (ValidationInfo): validationInfo provided by pydantic

    Returns:
        Any: True or False if the validation maps to an accepted value - otherwise we return the value which
        may or may not be valid
    """

    if isinstance(v, str):
        if v == "true" or v == "1":
            return True
        elif v == "false" or v == "0":
            return False
        else:
            raise ValueError
    elif isinstance(v, int):
        if v == 1:
            return True
        elif v == 0:
            return False
        else:
            raise ValueError
    elif isinstance(v, bool):
        return v
    else:
        raise ValueError


OscalBool = Annotated[bool, BeforeValidator(validate_bool)]

OscalDecimal = float

OscalInteger = int

OscalNonNegativeInteger = NonNegativeInt

OscalPositiveInteger = PositiveInt

OscalBase64Binary = Annotated[
    str,
    constr(pattern=r"^[0-9A-Fa-f]+$"),
]

OscalDate = Annotated[
    str,
    constr(
        pattern="^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|[+-][0-9]{2}:[0-9]{2})?$"
    ),
]

# ISO 8601 pattern ^([1-9]\d{3}[\-.](0[13578]|1[02])[\-.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](0[469]|11)[\-.](0[1-9]|[12][0-9]|30) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](02)[\-.](0[1-9]|1[0-9]|2[0-8]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|(((([1-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[13579][26])00)))[\-.](02)[\-.]29 ([01]\d|2[0123]):([012345]\d):([012345]\d))$

OscalDateWithTimezone = Annotated[
    str,
    constr(
        pattern=r"^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|[+-][0-9]{2}:[0-9]{2})$"
    ),
]

OscalDateTime = Annotated[
    str,
    constr(
        pattern=r"(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T((2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?)(Z|[+-][0-9]{2}:[0-9]{2})?"
    ),
]

OscalDateTimeWithTimezone = Annotated[
    str,
    constr(
        pattern=r"(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T((2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?)(Z|[+-][0-9]{2}:[0-9]{2})",
    ),
]

OscalEmail = EmailStr

OscalHostname = Annotated[
    str,
    constr(
        pattern=r"^(([a-zA-Z]+[\d-]*[a-zA-Z0-9]+)(\.)?)+$",
    ),
]

OscalIpV4Address = Annotated[
    str,
    constr(
        pattern=r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$",
    ),
]

OscalIpV6Address = Annotated[
    str,
    constr(
        pattern=r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|[fF][eE]80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::([fF]{4}(:0{1,4}){0,1}:){0,1}((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))$",
    ),
]

OscalString = Annotated[
    str,
    constr(pattern=r"\s.\S+"),
]

OscalToken = Annotated[
    str,
    constr(
        pattern=r"^([a-zA-Z_])([A-Za-z0-9.\-_])*$",  # any non-numeric character or "_", followed by a sequence of any alphanumeric character, "_", "-", or "."
    ),
]

OscalUri = AnyUrl

OscalRelativeUri = Annotated[
    str,
    constr(
        pattern=r"^(/|//)?([^:])*$|^./(\S)*$",
    ),  # TODO: We can do much better than this, but it's a start
]

OscalUriReference = OscalUri | OscalRelativeUri

OscalUUID = uuid.UUID


def validate_markup_line(v: str) -> str:
    # TODO: validate that the text is HTML or MD with only the permitted tags
    # TODO: Parameter insertion
    return v


OscalMarkupLine = Annotated[str, AfterValidator(validate_markup_line)]


def validate_markup_multiline(v: str) -> str:
    # TODO: validate that the text is HTML or MD with only the permitted tags
    # TODO: Parameter insertion
    return v


OscalMarkupMultiline = Annotated[str, AfterValidator(validate_markup_multiline)]

OscalDatatype = Union[
    OscalBool,
    OscalDecimal,
    OscalInteger,
    OscalNonNegativeInteger,
    OscalPositiveInteger,
    OscalBase64Binary,
    OscalDate,
    OscalDateWithTimezone,
    OscalDateTime,
    OscalDateTimeWithTimezone,
    OscalEmail,
    OscalHostname,
    OscalIpV4Address,
    OscalIpV6Address,
    OscalString,
    OscalToken,
    OscalUri,
    OscalRelativeUri,
    OscalUriReference,
    OscalUUID,
    OscalMarkupLine,
    OscalMarkupMultiline,
]
