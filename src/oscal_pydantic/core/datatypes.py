from __future__ import annotations

from datetime import date, timezone, timedelta
from typing import Annotated

import re
import uuid

from pydantic import (
    RootModel,
    Field,
    field_validator,
    ValidationError,
    StrictBool,
    NonNegativeInt,
    PositiveInt,
)

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    pass


class Boolean(RootModel[bool]):
    """
    A class used to represent an OSCAL Boolean:

    https://pages.nist.gov/OSCAL/reference/datatypes/#boolean

    A boolean value mapped in XML, JSON, and YAML as follows:
    | Value | XML | JSON | YAML |
    |:--- |:--- |:--- |:--- |
    | true | `true` or `1` | `true` | `true` |
    | false | `false` or `0` | `false` | `false` |

    Attributes:
        root: (bool, "0" or "1", or 0 or 1): A boolean value represented either as a bool, the str "0" or "1", or the int 0 or 1.

    Methods:
    [field_validator]input_to_bool(value): a field validator to convert any valid input to a python bool
    """

    # TODO: Pydantic will accept values from JSON that are invalid in oscal, including:
    # Allowed values: 'f', 'n', 'no', 'off',  't', 'y', 'on', 'yes'
    # Do I care?

    root: bool = Field(description="A boolean value")

    def __bool__(self):
        if self.root:
            return True
        else:
            return False


class Decimal(RootModel[float]):
    """
    A class to represent an OSCAL Decimal

    https://pages.nist.gov/OSCAL/reference/datatypes/#decimal

    Attributes:
        root : float
            A real number expressed using decimal numerals.
    """

    root: float = Field(description="A real number expressed using decimal numerals.")


class Integer(RootModel[int]):
    """
    A class to represent an OSCAL Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#integer

    Attributes:
        root : int
            An integer value.
    """

    root: int = Field(description="An integer value.")


class NonNegativeInteger(RootModel[NonNegativeInt]):
    """
    A class to represent an OSCAL Non-negative Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#nonnegativeinteger

    Attributes:
        root: int
            An integer value that is equal to or greater than 0.
    """

    root: NonNegativeInt = Field(
        description="An integer value that is equal to or greater than 0."
    )


class PositiveInteger(RootModel[PositiveInt]):
    """
    A class to represent an OSCAL Positive Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#positiveinteger

    Attributes:
        root: int
            A positive integer value.
    """

    root: PositiveInt = Field(description="A positive integer value.")


class Base64Binary(RootModel[str]):
    """
    A class to represent an OSCAL Base64 Binary String

    https://pages.nist.gov/OSCAL/reference/datatypes/#base64binary

    Attributes:
        root: str
            A string representing arbitrary Base64-encoded binary data
    """

    root: str = Field(
        description="A string representing arbitrary Base64-encoded binary data.",
        pattern=r"^[0-9A-Fa-f]+$",
    )


class Date(RootModel[str]):
    """
    A class to represent an OSCAL Date String with optional Timezone(expressed as offset from UTC)

    https://pages.nist.gov/OSCAL/reference/datatypes/#date

    Attributes:
        root: A string which must conform to the following

        date: datetime.date
            A date

        timezone: datetime.timedelta
            A timedelta from UTC

    Methods:
        str_to_date: str
            Accepts a string representing a 24-hour period with optional time zone. A date is formatted according to "full-date" as defined RFC3339.
            This function assumes that a valid date is provided because the pattern associated with the root field should reject any invalid dates.
    """

    # ISO 8601 pattern ^([1-9]\d{3}[\-.](0[13578]|1[02])[\-.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](0[469]|11)[\-.](0[1-9]|[12][0-9]|30) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](02)[\-.](0[1-9]|1[0-9]|2[0-8]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|(((([1-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[13579][26])00)))[\-.](02)[\-.]29 ([01]\d|2[0123]):([012345]\d):([012345]\d))$

    root: str = Field(
        description="A string representing a 24-hour period with optional time zone.",
        pattern="^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|[+-][0-9]{2}:[0-9]{2})?$",
    )

    _date: date = Field(
        description="A date.",
    )
    _timezone: timezone | None = Field(
        description="An optional timezone, expressed as an offset from UTC",
        default=None,
    )

    def model_post_init(self, __context: Any) -> None:
        patterns = re.match(
            "^([0-9]{4})-([0][1-9]|[1][0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])(Z|[+-][0-9]{2}:[0-9]{2})?$",
            self.root,
        )
        # This shouldn't happen because of the filter, but this shuts up pylint
        if patterns is not None:
            self._date = date(
                int(patterns.group(1)), int(patterns.group(2)), int(patterns.group(3))
            )
            if len(patterns.groups()) > 3:
                if patterns.group(4) == "Z":
                    self._timezone = timezone.utc
                else:
                    tz_patterns = re.match(
                        "^([+-])([01][0-9]|2[0-4])(?::([0-5][0-9]))?$",
                        patterns.group(4),
                    )
                    if tz_patterns is not None:
                        hours = float(tz_patterns.group(2))
                        minutes = float(tz_patterns.group(3))
                        if tz_patterns.group(1) == "-":
                            self._timezone = timezone(
                                timedelta(hours=-hours, minutes=minutes)
                            )
                        elif tz_patterns.group(1) == "+":
                            self._timezone = timezone(
                                timedelta(hours=hours, minutes=minutes)
                            )
                        else:
                            raise ValidationError(
                                "Invalid offset character - should be + or -"
                            )


class Token(RootModel[str]):
    root: str = Field(
        description="Non-colonized token type used for various identifiers",
        pattern=r"^([^\W\d]|[:_]){1}[\w\d:\-_.]*$",  # "any non-numeric character, _ or :, followed by a sequence of any alphanumeric character, _, :, -, or ."
    )


class Relation(RootModel[Token]):
    root: Token = Field(
        description="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose."
    )


class MediaType(RootModel[str]):
    root: str = Field(
        description="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.",
        pattern=r"^\w+/([\w-]+\.)*[\w-]+(\+[\w]+)?(;.*)?$",
    )


class UUID(RootModel[uuid.UUID]):
    """
    A class to represent an OSCAL Decimal

    https://pages.nist.gov/OSCAL/reference/datatypes/#decimal

    A real number expressed using decimal numerals.

    Attributes:
        root: (float)
    """

    root: uuid.UUID = Field(
        description="A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this defined property elsewhere in this or other OSCAL instances. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document.",
        default=uuid.uuid4(),
    )


class MarkupLine(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line"
        # TODO: validate that the text is HTML or MD with only the permitted tags
    )


class MarkupMultiline(RootModel[str]):
    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-multiline"
        # TODO: validate that the text is HTML or MD with only the permitted tags
    )
